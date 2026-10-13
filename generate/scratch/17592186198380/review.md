# Flux original and generated review

Database math, basis 1356. Originals are generator replays compared exactly to the capture. Generated empirical bank variants preserve complete observed density profiles; these extrapolations have unresolved error intent. Authored bank variants use explicitly defined method errors. Metadata appears in review JSON only.

## Original replay q-160845

### q-160845 / observed:q-160845

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $-1\le u\le 1$ and $0\le v\le 3.$

- $2$
- $10$
- $6$ (correct)
- $4$
- $8$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{0}^{3}{\int }_{-1}^{1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{-1}^{1}\,\text{d}u\cdot {\int }_{0}^{3}(6v-8)\,\text{d}v \\  & =[u]_{-1}^{1}\cdot [3{v}^{2}-8v]_{0}^{3} \\  & =2\cdot 3 \\  & =6.\end{aligned}
$$


## Generated empirical bank variant q-160845 1

### q-160845 / observed:q-160845

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $-1\le u\le 1$ and $0\le v\le 4.$

- $\frac{8}{3}$
- $\frac{40}{3}$
- $32$ (correct)
- $\frac{16}{3}$
- $\frac{32}{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{-1}^{1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{-1}^{1}\,\text{d}u\cdot {\int }_{0}^{4}(6v-8)\,\text{d}v \\  & =[u]_{-1}^{1}\cdot [3{v}^{2}-8v]_{0}^{4} \\  & =2\cdot 16 \\  & =32.\end{aligned}
$$


## Generated empirical bank variant q-160845 2

### q-160845 / observed:q-160845

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $-1\le u\le 1$ and $0\le v\le 5.$

- $\frac{10}{3}$
- $\frac{50}{3}$
- $70$ (correct)
- $\frac{20}{3}$
- $\frac{40}{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-1}^{1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{-1}^{1}\,\text{d}u\cdot {\int }_{0}^{5}(6v-8)\,\text{d}v \\  & =[u]_{-1}^{1}\cdot [3{v}^{2}-8v]_{0}^{5} \\  & =2\cdot 35 \\  & =70.\end{aligned}
$$


## Original replay q-160886

### q-160886 / observed:q-160886

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,-1\le v\le 2}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $36$
- $48$
- $18$ (correct)
- $24$
- $72$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{0}^{1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{-1}^{2}[12{u}^{2}v]_{0}^{1}\,\text{d}v \\  & ={\int }_{-1}^{2}12v\,\text{d}v \\  & =[6{v}^{2}]_{-1}^{2} \\  & =6({2}^{2}-(-1)^{2}) \\  & =18.\end{aligned}
$$


## Generated empirical bank variant q-160886 1

### q-160886 / observed:q-160886

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,-1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $60$
- $80$
- $90$ (correct)
- $40$
- $120$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{-1}^{4}{\int }_{0}^{1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{-1}^{4}[12{u}^{2}v]_{0}^{1}\,\text{d}v \\  & ={\int }_{-1}^{4}12v\,\text{d}v \\  & =[6{v}^{2}]_{-1}^{4} \\  & =90 \\  & =90.\end{aligned}
$$


## Generated empirical bank variant q-160886 2

### q-160886 / observed:q-160886

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,-1\le v\le 6}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $84$
- $112$
- $210$ (correct)
- $56$
- $168$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{-1}^{6}{\int }_{0}^{1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{-1}^{6}[12{u}^{2}v]_{0}^{1}\,\text{d}v \\  & ={\int }_{-1}^{6}12v\,\text{d}v \\  & =[6{v}^{2}]_{-1}^{6} \\  & =210 \\  & =210.\end{aligned}
$$


## Original replay q-161260

### q-161260 / observed:q-161260

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,0\le v\le 1}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $-\frac{5}{6}$
- $-1$
- $-\frac{1}{3}$ (correct)
- $4$
- $2$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{1}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(-v+2{v}^{2}-2{v}^{3})\text{d}v \\  & ={[-\frac{1}{2}{v}^{2}+\frac{2}{3}{v}^{3}-\frac{1}{2}{v}^{4}]}_{0}^{1} \\  & =-\frac{1}{2}+\frac{2}{3}-\frac{1}{2} \\  & =-\frac{1}{3}.\end{aligned}
$$


## Generated empirical bank variant q-161260 1

### q-161260 / observed:q-161260

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,0\le v\le 2}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $- \frac{5}{3}$
- $-2$
- $- \frac{14}{3}$ (correct)
- $8$
- $4$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{0}^{1}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{2}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{2}(-v+2{v}^{2}-2{v}^{3})\text{d}v \\  & ={[-\frac{1}{2}{v}^{2}+\frac{2}{3}{v}^{3}-\frac{1}{2}{v}^{4}]}_{0}^{2} \\  & =-2-8+\frac{16}{3} \\  & =- \frac{14}{3}.\end{aligned}
$$


## Generated empirical bank variant q-161260 2

### q-161260 / observed:q-161260

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,0\le v\le 3}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $- \frac{5}{2}$
- $-3$
- $-27$ (correct)
- $12$
- $6$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{3}{\int }_{0}^{1}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{3}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{3}(-v+2{v}^{2}-2{v}^{3})\text{d}v \\  & ={[-\frac{1}{2}{v}^{2}+\frac{2}{3}{v}^{3}-\frac{1}{2}{v}^{4}]}_{0}^{3} \\  & =- \frac{9}{2}- \frac{81}{2}+18 \\  & =-27.\end{aligned}
$$


## Original replay q-161262

### q-161262 / observed:q-161262

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le 0,\,0\le v\le 1}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $\frac{9}{4}$
- $11$
- $8$ (correct)
- $\frac{5}{3}$
- $5$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-2}^{0}{\int }_{0}^{1}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-2}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=1}\,\text{d}u \\  & =-6{\int }_{-2}^{0}(u+\frac{1}{3})\text{d}u \\  & =-6{[\frac{1}{2}{u}^{2}+\frac{1}{3}u]}_{-2}^{0} \\  & =-6(-2+\frac{2}{3}) \\  & =8.\end{aligned}
$$


## Generated empirical bank variant q-161262 1

### q-161262 / observed:q-161262

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le 0,\,0\le v\le 2}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $\frac{9}{2}$
- $22$
- $16$ (correct)
- $\frac{10}{3}$
- $10$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-2}^{0}{\int }_{0}^{2}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-2}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=2}\,\text{d}u \\  & =-6{\int }_{-2}^{0}(4 u + \frac{8}{3})\text{d}u \\  & =-6{[\frac{2 u \left(3 u + 4\right)}{3}]}_{-2}^{0} \\  & =-6(-8+\frac{16}{3}) \\  & =16.\end{aligned}
$$


## Generated empirical bank variant q-161262 2

### q-161262 / observed:q-161262

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le 0,\,0\le v\le 3}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $\frac{27}{4}$
- $33$
- $0$ (correct)
- $5$
- $15$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-2}^{0}{\int }_{0}^{3}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-2}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=3}\,\text{d}u \\  & =-6{\int }_{-2}^{0}(9 u + 9)\text{d}u \\  & =-6{[\frac{9 u \left(u + 2\right)}{2}]}_{-2}^{0} \\  & =-6(18-18) \\  & =0.\end{aligned}
$$


## Original replay q-161263

### q-161263 / observed:q-161263

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $-1\le u\le 1$ and $0\le v\le 1.$

- $-\frac{1}{2}$
- $4$
- $-3$ (correct)
- $-1$
- $\frac{5}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-1}^{1}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=-1}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(-6v)\text{d}v \\  & =[-3{v}^{2}]_{0}^{1} \\  & =-3.\end{aligned}
$$


## Generated empirical bank variant q-161263 1

### q-161263 / observed:q-161263

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $-1\le u\le 1$ and $0\le v\le 2.$

- $-1$
- $8$
- $-12$ (correct)
- $-2$
- $5$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{2}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=-1}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{2}(-6v)\text{d}v \\  & =[-3{v}^{2}]_{0}^{2} \\  & =-12.\end{aligned}
$$


## Generated empirical bank variant q-161263 2

### q-161263 / observed:q-161263

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $-1\le u\le 1$ and $0\le v\le 3.$

- $- \frac{3}{2}$
- $12$
- $-27$ (correct)
- $-3$
- $\frac{15}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{3}{\int }_{-1}^{1}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{3}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=-1}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{3}(-6v)\text{d}v \\  & =[-3{v}^{2}]_{0}^{3} \\  & =-27.\end{aligned}
$$


## Original replay q-161273

### q-161273 / observed:q-161273

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 1$ and $0\le v\le 2.$

- $\frac{1}{3}$
- $2$
- $-4$ (correct)
- $-1$
- $-\frac{4}{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{0}^{2}{\int }_{0}^{1}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{0}^{2}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =2{\int }_{0}^{2}(\frac{1}{3}-{v}^{2})\text{d}v \\  & =2{[\frac{1}{3}v-\frac{1}{3}{v}^{3}]}_{0}^{2} \\  & =2(\frac{2}{3}-\frac{8}{3}) \\  & =-4.\end{aligned}
$$


## Generated empirical bank variant q-161273 1

### q-161273 / observed:q-161273

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 1$ and $0\le v\le 3.$

- $\frac{1}{2}$
- $3$
- $-16$ (correct)
- $- \frac{3}{2}$
- $-2$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{0}^{3}{\int }_{0}^{1}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{0}^{3}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =2{\int }_{0}^{3}(\frac{1}{3}-{v}^{2})\text{d}v \\  & =2{[\frac{1}{3}v-\frac{1}{3}{v}^{3}]}_{0}^{3} \\  & =2(-9+1) \\  & =-16.\end{aligned}
$$


## Generated empirical bank variant q-161273 2

### q-161273 / observed:q-161273

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 1$ and $0\le v\le 4.$

- $\frac{2}{3}$
- $4$
- $-40$ (correct)
- $-2$
- $- \frac{8}{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{0}^{4}{\int }_{0}^{1}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{0}^{4}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =2{\int }_{0}^{4}(\frac{1}{3}-{v}^{2})\text{d}v \\  & =2{[\frac{1}{3}v-\frac{1}{3}{v}^{3}]}_{0}^{4} \\  & =2(- \frac{64}{3}+\frac{4}{3}) \\  & =-40.\end{aligned}
$$


## Original replay q-161278

### q-161278 / observed:q-161278

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $-1\le u\le 0$ and $0\le v\le 1.$

- $-4$
- $3$
- $\frac{1}{2}$ (correct)
- $-\frac{3}{2}$
- $\frac{5}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{-1}^{0}{\int }_{0}^{1}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{-1}^{0}[uv+{v}^{2}]_{v=0}^{v=1}\,\text{d}u \\  & ={\int }_{-1}^{0}(u+1)\text{d}u \\  & ={[\frac{1}{2}{u}^{2}+u]}_{-1}^{0} \\  & =-\frac{1}{2}+1 \\  & =\frac{1}{2}.\end{aligned}
$$


## Generated empirical bank variant q-161278 1

### q-161278 / observed:q-161278

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $-1\le u\le 0$ and $0\le v\le 2.$

- $-8$
- $6$
- $3$ (correct)
- $-3$
- $\frac{5}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{-1}^{0}{\int }_{0}^{2}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{-1}^{0}[uv+{v}^{2}]_{v=0}^{v=2}\,\text{d}u \\  & ={\int }_{-1}^{0}(2 u + 4)\text{d}u \\  & ={[u \left(u + 4\right)]}_{-1}^{0} \\  & =-1+4 \\  & =3.\end{aligned}
$$


## Generated empirical bank variant q-161278 2

### q-161278 / observed:q-161278

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $-1\le u\le 0$ and $0\le v\le 3.$

- $-12$
- $9$
- $\frac{15}{2}$ (correct)
- $- \frac{9}{2}$
- $\frac{15}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{-1}^{0}{\int }_{0}^{3}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{-1}^{0}[uv+{v}^{2}]_{v=0}^{v=3}\,\text{d}u \\  & ={\int }_{-1}^{0}(3 u + 9)\text{d}u \\  & ={[\frac{3 u \left(u + 6\right)}{2}]}_{-1}^{0} \\  & =9- \frac{3}{2} \\  & =\frac{15}{2}.\end{aligned}
$$


## Original replay q-161283

### q-161283 / observed:q-161283

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 1$ and $0\le v\le 1.$

- $-4$
- $3$
- $-2$ (correct)
- $-\frac{3}{2}$
- $\frac{5}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{1}{\int }_{0}^{1}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{1}u\,\text{d}u{\int }_{0}^{1}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{1}\cdot {[\frac{1}{2}{v}^{2}]}_{0}^{1} \\  & =-8(\frac{1}{2})(\frac{1}{2}) \\  & =-2.\end{aligned}
$$


## Generated empirical bank variant q-161283 1

### q-161283 / observed:q-161283

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 1$ and $0\le v\le 3.$

- $-12$
- $9$
- $-18$ (correct)
- $- \frac{9}{2}$
- $\frac{15}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{1}{\int }_{0}^{3}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{1}u\,\text{d}u{\int }_{0}^{3}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{1}\cdot {[\frac{1}{2}{v}^{2}]}_{0}^{3} \\  & =-8(\frac{1}{2})(\frac{9}{2}) \\  & =-18.\end{aligned}
$$


## Generated empirical bank variant q-161283 2

### q-161283 / observed:q-161283

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 1$ and $0\le v\le 4.$

- $-16$
- $12$
- $-32$ (correct)
- $-6$
- $5$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{1}{\int }_{0}^{4}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{1}u\,\text{d}u{\int }_{0}^{4}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{1}\cdot {[\frac{1}{2}{v}^{2}]}_{0}^{4} \\  & =-8(\frac{1}{2})(8) \\  & =-32.\end{aligned}
$$


## Original replay q-161258

### q-161258 / observed:q-161258

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,0\le v\le 1}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $\frac{17}{2}$
- $3$
- $-\frac{23}{4}$ (correct)
- $-\frac{22}{3}$
- $-5$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(-\frac{11}{2}v-3)\text{d}v \\  & ={[-\frac{11}{4}{v}^{2}-3v]}_{0}^{1} \\  & =-\frac{11}{4}-3 \\  & =-\frac{23}{4}.\end{aligned}
$$


## Generated empirical bank variant q-161258 1

### q-161258 / observed:q-161258

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,0\le v\le 2}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $17$
- $6$
- $-17$ (correct)
- $- \frac{44}{3}$
- $-10$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{0}^{1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{2}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{2}(-\frac{11}{2}v-3)\text{d}v \\  & ={[-\frac{11}{4}{v}^{2}-3v]}_{0}^{2} \\  & =-6-11 \\  & =-17.\end{aligned}
$$


## Generated empirical bank variant q-161258 2

### q-161258 / observed:q-161258

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,0\le v\le 3}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $\frac{51}{2}$
- $9$
- $- \frac{135}{4}$ (correct)
- $-22$
- $-15$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{0}^{3}{\int }_{0}^{1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{3}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{3}(-\frac{11}{2}v-3)\text{d}v \\  & ={[-\frac{11}{4}{v}^{2}-3v]}_{0}^{3} \\  & =-9- \frac{99}{4} \\  & =- \frac{135}{4}.\end{aligned}
$$


## Original replay q-162593

### q-162593 / observed:q-162593

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $0\le u\le 1$ and $0\le v\le 1.$

- $-\frac{1}{3}$
- $\frac{1}{3}$
- $-\frac{3}{2}$ (correct)
- $-\frac{1}{8}$
- $-\frac{1}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{0}^{1}{\int }_{0}^{1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{0}^{1}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =-{\int }_{0}^{1}(2v+\frac{1}{2})\text{d}v \\  & =-{[{v}^{2}+\frac{1}{2}v]}_{0}^{1} \\  & =-\frac{3}{2}.\end{aligned}
$$


## Generated empirical bank variant q-162593 1

### q-162593 / observed:q-162593

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $0\le u\le 1$ and $0\le v\le 2.$

- $- \frac{2}{3}$
- $\frac{2}{3}$
- $-5$ (correct)
- $-\frac{1}{4}$
- $- \frac{1}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{0}^{1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{0}^{2}{\int }_{0}^{1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{0}^{2}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =-{\int }_{0}^{2}(2v+\frac{1}{2})\text{d}v \\  & =-{[{v}^{2}+\frac{1}{2}v]}_{0}^{2} \\  & =-5.\end{aligned}
$$


## Generated empirical bank variant q-162593 2

### q-162593 / observed:q-162593

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $0\le u\le 1$ and $0\le v\le 3.$

- $-1$
- $1$
- $- \frac{21}{2}$ (correct)
- $- \frac{3}{8}$
- $- \frac{3}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{0}^{3}{\int }_{0}^{1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{0}^{3}{\int }_{0}^{1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{0}^{3}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =-{\int }_{0}^{3}(2v+\frac{1}{2})\text{d}v \\  & =-{[{v}^{2}+\frac{1}{2}v]}_{0}^{3} \\  & =- \frac{21}{2}.\end{aligned}
$$


## Generated authored bank q-160845 / authored_primitive / 0

### q-160845 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $21$ (correct)
- $66$
- $-21$
- $9$
- $924$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{0}^{1}\,\text{d}u\cdot {\int }_{1}^{4}(6v-8)\,\text{d}v \\  & =[u]_{0}^{1}\cdot [3{v}^{2}-8v]_{1}^{4} \\  & =1\cdot 21 \\  & =21.\end{aligned}
$$


## Generated authored bank q-160845 / authored_primitive / 1

### q-160845 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $-2\le u\le -1$ and $2\le v\le 5.$

- $1716$
- $102$
- $-39$
- $15$
- $39$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{-2}^{-1}\,\text{d}u\cdot {\int }_{2}^{5}(6v-8)\,\text{d}v \\  & =[u]_{-2}^{-1}\cdot [3{v}^{2}-8v]_{2}^{5} \\  & =1\cdot 39 \\  & =39.\end{aligned}
$$


## Generated authored bank q-160845 / authored_weighted / 0

### q-160845 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $21$ (correct)
- $\frac{21}{2}$
- $-21$
- $66$
- $33$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{0}^{1}\,\text{d}u\cdot {\int }_{1}^{4}(6v-8)\,\text{d}v \\  & =[u]_{0}^{1}\cdot [3{v}^{2}-8v]_{1}^{4} \\  & =1\cdot 21 \\  & =21.\end{aligned}
$$


## Generated authored bank q-160845 / authored_weighted / 1

### q-160845 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $-2\le u\le -1$ and $2\le v\le 5.$

- $-225$
- $- \frac{117}{2}$
- $-39$
- $150$
- $39$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{-2}^{-1}\,\text{d}u\cdot {\int }_{2}^{5}(6v-8)\,\text{d}v \\  & =[u]_{-2}^{-1}\cdot [3{v}^{2}-8v]_{2}^{5} \\  & =1\cdot 39 \\  & =39.\end{aligned}
$$


## Generated authored bank q-160845 / authored_rectangle / 0

### q-160845 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $21$ (correct)
- $-6$
- $-21$
- $48$
- $\frac{15}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{0}^{1}\,\text{d}u\cdot {\int }_{1}^{4}(6v-8)\,\text{d}v \\  & =[u]_{0}^{1}\cdot [3{v}^{2}-8v]_{1}^{4} \\  & =1\cdot 21 \\  & =21.\end{aligned}
$$


## Generated authored bank q-160845 / authored_rectangle / 1

### q-160845 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-1,\,2v,\,2-3u-2v⟩
$$

for $-2\le u\le -1$ and $2\le v\le 5.$

- $\frac{51}{2}$
- $12$
- $-39$
- $66$
- $39$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-1),\,\frac{∂}{∂u}(2v),\,\frac{∂}{∂u}(2-3u-2v)⟩ \\  & =⟨1,\,0,\,-3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-1),\,\frac{∂}{∂v}(2v),\,\frac{∂}{∂v}(2-3u-2v)⟩ \\  & =⟨0,\,2,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -3 \\ 0 & 2 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & -3 \\ 2 & -2\end{aligned}|,-|\begin{aligned}1 & -3 \\ 0 & -2\end{aligned}|,|\begin{aligned}1 & 0 \\ 0 & 2\end{aligned}|⟩ \\  & =⟨6,\,2,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩|}_{x=u-1\,y=2v\,z=2-3u-2v} \\  & =⟨3(u-1)+(2v)+(2-3u-2v),\,\frac{2v}{2}-2,\,-3(u-1)-(2-3u-2v)⟩ \\  & =⟨-1,\,v-2,\,2v+1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-1,\,v-2,\,2v+1⟩\cdot ⟨6,\,2,\,2⟩ \\  & =(-1)\cdot 6+(v-2)\cdot 2+(2v+1)\cdot 2 \\  & =-6+2v-4+4v+2 \\  & =6v-8.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x+y+z,\,\frac{y}{2}-2,\,-3x-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(6v-8)\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}(6v-8)\,\text{d}u\text{d}v \\  & ={\int }_{-2}^{-1}\,\text{d}u\cdot {\int }_{2}^{5}(6v-8)\,\text{d}v \\  & =[u]_{-2}^{-1}\cdot [3{v}^{2}-8v]_{2}^{5} \\  & =1\cdot 39 \\  & =39.\end{aligned}
$$


## Generated authored bank q-160886 / authored_primitive / 0

### q-160886 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $90$ (correct)
- $360$
- $-90$
- $40$
- $10305$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{1}^{4}[12{u}^{2}v]_{0}^{1}\,\text{d}v \\  & ={\int }_{1}^{4}12v\,\text{d}v \\  & =[6{v}^{2}]_{1}^{4} \\  & =90 \\  & =90.\end{aligned}
$$


## Generated authored bank q-160886 / authored_primitive / 1

### q-160886 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $-66717$
- $-1512$
- $378$
- $-168$
- $-378$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{2}^{5}[12{u}^{2}v]_{-2}^{-1}\,\text{d}v \\  & ={\int }_{2}^{5}- 36 v\,\text{d}v \\  & =[- 18 v^{2}]_{2}^{5} \\  & =-378 \\  & =-378.\end{aligned}
$$


## Generated authored bank q-160886 / authored_weighted / 0

### q-160886 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $90$ (correct)
- $60$
- $-90$
- $252$
- $168$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{1}^{4}[12{u}^{2}v]_{0}^{1}\,\text{d}v \\  & ={\int }_{1}^{4}12v\,\text{d}v \\  & =[6{v}^{2}]_{1}^{4} \\  & =90 \\  & =90.\end{aligned}
$$


## Generated authored bank q-160886 / authored_weighted / 1

### q-160886 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $2184$
- $588$
- $378$
- $-1404$
- $-378$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{2}^{5}[12{u}^{2}v]_{-2}^{-1}\,\text{d}v \\  & ={\int }_{2}^{5}- 36 v\,\text{d}v \\  & =[- 18 v^{2}]_{2}^{5} \\  & =-378 \\  & =-378.\end{aligned}
$$


## Generated authored bank q-160886 / authored_rectangle / 0

### q-160886 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $90$ (correct)
- $0$
- $-90$
- $288$
- $\frac{63}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{1}^{4}[12{u}^{2}v]_{0}^{1}\,\text{d}v \\  & ={\int }_{1}^{4}12v\,\text{d}v \\  & =[6{v}^{2}]_{1}^{4} \\  & =90 \\  & =90.\end{aligned}
$$


## Generated authored bank q-160886 / authored_rectangle / 1

### q-160886 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2u-1,\,uv,\,3v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.$*

- $- \frac{693}{2}$
- $-288$
- $378$
- $-360$
- $-378$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨3v,\,-6,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨2x,\,\frac{xz}{3}-2y,\,2z⟩|}_{x=2u-1\,y=uv\,z=3v} \\  & =⟨2(2u-1),\,\frac{(2u-1)(3v)}{3}-2uv,\,2(3v)⟩ \\  & =⟨4u-2,\,-v,\,6v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4u-2,\,-v,\,6v⟩\cdot ⟨3v,\,-6,\,2u⟩ \\  & =(4u-2)\cdot 3v+(-v)\cdot (-6)+6v\cdot 2u \\  & =12uv-6v+6v+12uv \\  & =24uv.\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨2x,\,\frac{xz}{3}-2y,\,2z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}24uv\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}24uv\,\text{d}u\text{d}v \\  & ={\int }_{2}^{5}[12{u}^{2}v]_{-2}^{-1}\,\text{d}v \\  & ={\int }_{2}^{5}- 36 v\,\text{d}v \\  & =[- 18 v^{2}]_{2}^{5} \\  & =-378 \\  & =-378.\end{aligned}
$$


## Generated authored bank q-161260 / authored_primitive / 0

### q-161260 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 3,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $-328$ (correct)
- $- \frac{68864}{5}$
- $328$
- $-1440$
- $- \frac{688}{5}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{0}^{3}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{4}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=0}^{u=3}\,\text{d}v \\  & ={\int }_{0}^{4}(3 v \left(- 2 v^{2} + 2 v - 3\right))\text{d}v \\  & ={[\frac{v^{2} \left(- 3 v^{2} + 4 v - 9\right)}{2}]}_{0}^{4} \\  & =128-72-384 \\  & =-328.\end{aligned}
$$


## Generated authored bank q-161260 / authored_primitive / 1

### q-161260 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le 1,\,0\le v\le 1}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $2$ (correct)
- $6$
- $-2$
- $\frac{19}{5}$
- $\frac{49}{60}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-2}^{1}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=-2}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(3 v \left(- 2 v^{2} + 2 v + 1\right))\text{d}v \\  & ={[\frac{v^{2} \left(- 3 v^{2} + 4 v + 3\right)}{2}]}_{0}^{1} \\  & =2- \frac{3}{2}+\frac{3}{2} \\  & =2.\end{aligned}
$$


## Generated authored bank q-161260 / authored_weighted / 0

### q-161260 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 3,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $-328$ (correct)
- $- \frac{8256}{5}$
- $328$
- $-528$
- $- \frac{5184}{5}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{0}^{3}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{4}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=0}^{u=3}\,\text{d}v \\  & ={\int }_{0}^{4}(3 v \left(- 2 v^{2} + 2 v - 3\right))\text{d}v \\  & ={[\frac{v^{2} \left(- 3 v^{2} + 4 v - 9\right)}{2}]}_{0}^{4} \\  & =128-72-384 \\  & =-328.\end{aligned}
$$


## Generated authored bank q-161260 / authored_weighted / 1

### q-161260 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le 1,\,0\le v\le 1}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $2$ (correct)
- $- \frac{13}{4}$
- $-2$
- $- \frac{43}{20}$
- $\frac{13}{10}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-2}^{1}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=-2}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(3 v \left(- 2 v^{2} + 2 v + 1\right))\text{d}v \\  & ={[\frac{v^{2} \left(- 3 v^{2} + 4 v + 3\right)}{2}]}_{0}^{1} \\  & =2- \frac{3}{2}+\frac{3}{2} \\  & =2.\end{aligned}
$$


## Generated authored bank q-161260 / authored_rectangle / 0

### q-161260 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 3,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $-328$ (correct)
- $-18$
- $328$
- $0$
- $-1440$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{0}^{3}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{4}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=0}^{u=3}\,\text{d}v \\  & ={\int }_{0}^{4}(3 v \left(- 2 v^{2} + 2 v - 3\right))\text{d}v \\  & ={[\frac{v^{2} \left(- 3 v^{2} + 4 v - 9\right)}{2}]}_{0}^{4} \\  & =128-72-384 \\  & =-328.\end{aligned}
$$


## Generated authored bank q-161260 / authored_rectangle / 1

### q-161260 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨u-v,\,2,\,{v}^{2}⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le 1,\,0\le v\le 1}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.$*

- $2$ (correct)
- $0$
- $-2$
- $\frac{69}{32}$
- $-6$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,-2v,\,0⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨y+z,\,x+z,\,1⟩|}_{x=u-v\,y=2\,z={v}^{2}} \\  & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2+{v}^{2},\,u-v+{v}^{2},\,1⟩\cdot ⟨0,\,-2v,\,0⟩ \\  & =(2+{v}^{2})\cdot 0+(u-v+{v}^{2})\cdot (-2v)+1\cdot 0 \\  & =-2uv+2{v}^{2}-2{v}^{3}\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨y+z,\,x+z,\,1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-2}^{1}(-2uv+2{v}^{2}-2{v}^{3})\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}[-{u}^{2}v+2u{v}^{2}-2u{v}^{3}]_{u=-2}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(3 v \left(- 2 v^{2} + 2 v + 1\right))\text{d}v \\  & ={[\frac{v^{2} \left(- 3 v^{2} + 4 v + 3\right)}{2}]}_{0}^{1} \\  & =2- \frac{3}{2}+\frac{3}{2} \\  & =2.\end{aligned}
$$


## Generated authored bank q-161262 / authored_primitive / 0

### q-161262 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-4\le u\le 0,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $\frac{7077888}{35}$
- $256$ (correct)
- $-256$
- $\frac{448}{3}$
- $1536$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-4}^{0}{\int }_{0}^{4}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-4}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=4}\,\text{d}u \\  & =-6{\int }_{-4}^{0}(16 u + \frac{64}{3})\text{d}u \\  & =-6{[\frac{8 u \left(3 u + 8\right)}{3}]}_{-4}^{0} \\  & =-6(-128+\frac{256}{3}) \\  & =256.\end{aligned}
$$


## Generated authored bank q-161262 / authored_primitive / 1

### q-161262 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-1\le u\le 0,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $-80$ (correct)
- $80$
- $-192$
- $- \frac{1859328}{35}$
- $- \frac{80}{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-1}^{0}{\int }_{0}^{4}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-1}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=4}\,\text{d}u \\  & =-6{\int }_{-1}^{0}(16 u + \frac{64}{3})\text{d}u \\  & =-6{[\frac{8 u \left(3 u + 8\right)}{3}]}_{-1}^{0} \\  & =-6(-8+\frac{64}{3}) \\  & =-80.\end{aligned}
$$


## Generated authored bank q-161262 / authored_weighted / 0

### q-161262 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-4\le u\le 0,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $- \frac{7168}{3}$
- $256$ (correct)
- $-256$
- $512$
- $-1024$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-4}^{0}{\int }_{0}^{4}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-4}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=4}\,\text{d}u \\  & =-6{\int }_{-4}^{0}(16 u + \frac{64}{3})\text{d}u \\  & =-6{[\frac{8 u \left(3 u + 8\right)}{3}]}_{-4}^{0} \\  & =-6(-128+\frac{256}{3}) \\  & =256.\end{aligned}
$$


## Generated authored bank q-161262 / authored_weighted / 1

### q-161262 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-1\le u\le 0,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $-80$ (correct)
- $80$
- $32$
- $\frac{320}{3}$
- $-256$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-1}^{0}{\int }_{0}^{4}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-1}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=4}\,\text{d}u \\  & =-6{\int }_{-1}^{0}(16 u + \frac{64}{3})\text{d}u \\  & =-6{[\frac{8 u \left(3 u + 8\right)}{3}]}_{-1}^{0} \\  & =-6(-8+\frac{64}{3}) \\  & =-80.\end{aligned}
$$


## Generated authored bank q-161262 / authored_rectangle / 0

### q-161262 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-4\le u\le 0,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $480$
- $256$ (correct)
- $-256$
- $-1536$
- $0$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-4}^{0}{\int }_{0}^{4}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-4}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=4}\,\text{d}u \\  & =-6{\int }_{-4}^{0}(16 u + \frac{64}{3})\text{d}u \\  & =-6{[\frac{8 u \left(3 u + 8\right)}{3}]}_{-4}^{0} \\  & =-6(-128+\frac{256}{3}) \\  & =256.\end{aligned}
$$


## Generated authored bank q-161262 / authored_rectangle / 1

### q-161262 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3u{v}^{2},\,u-v,\,2⟩
$$

over the domain $D={(u,v)\,:\,-1\le u\le 0,\,0\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.$*

- $-80$ (correct)
- $80$
- $0$
- $12$
- $-384$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨0,\,0,\,-6uv-3{v}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨{x}^{2},\,x+y,\,z⟩|}_{x=3u{v}^{2}\,y=u-v\,z=2} \\  & =⟨{(3u{v}^{2})}^{2},\,3u{v}^{2}+u-v,\,2⟩ \\  & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9{u}^{2}{v}^{4},\,3u{v}^{2}+u-v,\,2⟩\cdot ⟨0,\,0,\,-6uv-3{v}^{2}⟩ \\  & =9{u}^{2}{v}^{4}\cdot 0+(3u{v}^{2}+u-v)\cdot 0+2\cdot (-6uv-3{v}^{2}) \\  & =-6(2uv+{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,x+y,\,z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}-6(2uv+{v}^{2})\,\text{d}A \\  & =-6{\int }_{-1}^{0}{\int }_{0}^{4}(2uv+{v}^{2})\,\text{d}v\,\text{d}u \\  & =-6{\int }_{-1}^{0}{[u{v}^{2}+\frac{1}{3}{v}^{3}]}_{v=0}^{v=4}\,\text{d}u \\  & =-6{\int }_{-1}^{0}(16 u + \frac{64}{3})\text{d}u \\  & =-6{[\frac{8 u \left(3 u + 8\right)}{3}]}_{-1}^{0} \\  & =-6(-8+\frac{64}{3}) \\  & =-80.\end{aligned}
$$


## Generated authored bank q-161263 / authored_primitive / 0

### q-161263 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $0\le u\le 3$ and $0\le v\le 4.$

- $-324$ (correct)
- $- \frac{296568}{5}$
- $324$
- $-2448$
- $- \frac{824}{5}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{0}^{3}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{4}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=0}^{u=3}\,\text{d}v \\  & ={\int }_{0}^{4}(- \frac{81 v}{2})\text{d}v \\  & =[- \frac{81 v^{2}}{4}]_{0}^{4} \\  & =-324.\end{aligned}
$$


## Generated authored bank q-161263 / authored_primitive / 1

### q-161263 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $-2\le u\le 1$ and $0\le v\le 1.$

- $- \frac{9}{4}$ (correct)
- $15$
- $\frac{9}{4}$
- $\frac{2151}{40}$
- $- \frac{1}{6}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-2}^{1}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=-2}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(- \frac{9 v}{2})\text{d}v \\  & =[- \frac{9 v^{2}}{4}]_{0}^{1} \\  & =- \frac{9}{4}.\end{aligned}
$$


## Generated authored bank q-161263 / authored_weighted / 0

### q-161263 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $0\le u\le 3$ and $0\le v\le 4.$

- $-324$ (correct)
- $- \frac{9888}{5}$
- $324$
- $- \frac{3708}{5}$
- $-864$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{0}^{3}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{4}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=0}^{u=3}\,\text{d}v \\  & ={\int }_{0}^{4}(- \frac{81 v}{2})\text{d}v \\  & =[- \frac{81 v^{2}}{4}]_{0}^{4} \\  & =-324.\end{aligned}
$$


## Generated authored bank q-161263 / authored_weighted / 1

### q-161263 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $-2\le u\le 1$ and $0\le v\le 1.$

- $- \frac{9}{4}$ (correct)
- $- \frac{27}{20}$
- $\frac{9}{4}$
- $- \frac{9}{10}$
- $- \frac{3}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-2}^{1}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=-2}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(- \frac{9 v}{2})\text{d}v \\  & =[- \frac{9 v^{2}}{4}]_{0}^{1} \\  & =- \frac{9}{4}.\end{aligned}
$$


## Generated authored bank q-161263 / authored_rectangle / 0

### q-161263 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $0\le u\le 3$ and $0\le v\le 4.$

- $-324$ (correct)
- $- \frac{225}{8}$
- $324$
- $0$
- $-2448$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{0}^{3}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{4}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=0}^{u=3}\,\text{d}v \\  & ={\int }_{0}^{4}(- \frac{81 v}{2})\text{d}v \\  & =[- \frac{81 v^{2}}{4}]_{0}^{4} \\  & =-324.\end{aligned}
$$


## Generated authored bank q-161263 / authored_rectangle / 1

### q-161263 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨{u}^{2},\,v,\,uv⟩
$$

for $-2\le u\le 1$ and $0\le v\le 1.$

- $- \frac{9}{4}$ (correct)
- $0$
- $\frac{9}{4}$
- $- \frac{153}{128}$
- $-9$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & 0\end{aligned}|,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,|\begin{aligned}2u & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-2{u}^{2},\,2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3,\,z,\,y⟩|}_{x={u}^{2}\,y=v\,z=uv} \\  & =⟨3,\,uv,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3,\,uv,\,v⟩\cdot ⟨-v,\,-2{u}^{2},\,2u⟩ \\  & =3\cdot (-v)+uv\cdot (-2{u}^{2})+v\cdot 2u \\  & =-3v-2{u}^{3}v+2uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3,\,z,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-3v-2{u}^{3}v+2uv)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-2}^{1}(-3v-2{u}^{3}v+2uv)\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}{[-3uv-\frac{1}{2}{u}^{4}v+{u}^{2}v]}_{u=-2}^{u=1}\,\text{d}v \\  & ={\int }_{0}^{1}(- \frac{9 v}{2})\text{d}v \\  & =[- \frac{9 v^{2}}{4}]_{0}^{1} \\  & =- \frac{9}{4}.\end{aligned}
$$


## Generated authored bank q-161273 / authored_primitive / 0

### q-161273 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 4$ and $1\le v\le 5.$

- $-42240$
- $-160$ (correct)
- $160$
- $-60$
- $-480$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{1}^{5}{\int }_{0}^{4}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{1}^{5}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=4}\,\text{d}v \\  & =2{\int }_{1}^{5}(\frac{64}{3} - 4 v^{2})\text{d}v \\  & =2{[\frac{4 v \left(16 - v^{2}\right)}{3}]}_{1}^{5} \\  & =2(- \frac{496}{3}+\frac{256}{3}) \\  & =-160.\end{aligned}
$$


## Generated authored bank q-161273 / authored_primitive / 1

### q-161273 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 1$ and $1\le v\le 5.$

- $-80$ (correct)
- $80$
- $-240$
- $-12384$
- $-30$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{1}^{5}{\int }_{0}^{1}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{1}^{5}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =2{\int }_{1}^{5}(\frac{1}{3}-{v}^{2})\text{d}v \\  & =2{[\frac{1}{3}v-\frac{1}{3}{v}^{3}]}_{1}^{5} \\  & =2(- \frac{124}{3}+\frac{4}{3}) \\  & =-80.\end{aligned}
$$


## Generated authored bank q-161273 / authored_weighted / 0

### q-161273 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 4$ and $1\le v\le 5.$

- $-960$
- $-160$ (correct)
- $160$
- $-736$
- $- \frac{448}{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{1}^{5}{\int }_{0}^{4}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{1}^{5}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=4}\,\text{d}v \\  & =2{\int }_{1}^{5}(\frac{64}{3} - 4 v^{2})\text{d}v \\  & =2{[\frac{4 v \left(16 - v^{2}\right)}{3}]}_{1}^{5} \\  & =2(- \frac{496}{3}+\frac{256}{3}) \\  & =-160.\end{aligned}
$$


## Generated authored bank q-161273 / authored_weighted / 1

### q-161273 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 1$ and $1\le v\le 5.$

- $-80$ (correct)
- $80$
- $- \frac{118}{3}$
- $-150$
- $-304$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{1}^{5}{\int }_{0}^{1}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{1}^{5}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =2{\int }_{1}^{5}(\frac{1}{3}-{v}^{2})\text{d}v \\  & =2{[\frac{1}{3}v-\frac{1}{3}{v}^{3}]}_{1}^{5} \\  & =2(- \frac{124}{3}+\frac{4}{3}) \\  & =-80.\end{aligned}
$$


## Generated authored bank q-161273 / authored_rectangle / 0

### q-161273 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 4$ and $1\le v\le 5.$

- $-96$
- $-160$ (correct)
- $160$
- $-288$
- $-32$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{1}^{5}{\int }_{0}^{4}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{1}^{5}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=4}\,\text{d}v \\  & =2{\int }_{1}^{5}(\frac{64}{3} - 4 v^{2})\text{d}v \\  & =2{[\frac{4 v \left(16 - v^{2}\right)}{3}]}_{1}^{5} \\  & =2(- \frac{496}{3}+\frac{256}{3}) \\  & =-160.\end{aligned}
$$


## Generated authored bank q-161273 / authored_rectangle / 1

### q-161273 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u-v,\,v-u,\,-2uv⟩
$$

for $0\le u\le 1$ and $1\le v\le 5.$

- $-80$ (correct)
- $80$
- $-8$
- $- \frac{63}{2}$
- $-192$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-2uv)⟩ \\  & =⟨1,\,-1,\,-2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-2uv)⟩ \\  & =⟨-1,\,1,\,-2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & -2v \\ -1 & 1 & -2u\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -2v \\ 1 & -2u\end{aligned}|,-|\begin{aligned}1 & -2v \\ -1 & -2u\end{aligned}|,|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|⟩ \\  & =⟨2u+2v,\,2u+2v,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨x,\,0,\,y⟩|}_{x=u-v\,y=v-u\,z=-2uv} \\  & =⟨u-v,\,0,\,v-u⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u-v,\,0,\,v-u⟩\cdot ⟨2u+2v,\,2u+2v,\,0⟩ \\  & =(u-v)\cdot (2u+2v)+0\cdot (2u+2v)+(v-u)\cdot 0 \\  & =2({u}^{2}-{v}^{2})\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨x,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2({u}^{2}-{v}^{2})\,\text{d}A \\  & =2{\int }_{1}^{5}{\int }_{0}^{1}({u}^{2}-{v}^{2})\,\text{d}u\,\text{d}v \\  & =2{\int }_{1}^{5}{[\frac{1}{3}{u}^{3}-u{v}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =2{\int }_{1}^{5}(\frac{1}{3}-{v}^{2})\text{d}v \\  & =2{[\frac{1}{3}v-\frac{1}{3}{v}^{3}]}_{1}^{5} \\  & =2(- \frac{124}{3}+\frac{4}{3}) \\  & =-80.\end{aligned}
$$


## Generated authored bank q-161278 / authored_primitive / 0

### q-161278 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $\frac{33}{2}$ (correct)
- $33$
- $- \frac{33}{2}$
- $\frac{11}{2}$
- $99$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{1}^{4}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{0}^{1}[uv+{v}^{2}]_{v=1}^{v=4}\,\text{d}u \\  & ={\int }_{0}^{1}(3 u + 15)\text{d}u \\  & ={[\frac{3 u \left(u + 10\right)}{2}]}_{0}^{1} \\  & =15+\frac{3}{2} \\  & =\frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-161278 / authored_primitive / 1

### q-161278 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $-2\le u\le -1$ and $2\le v\le 5.$

- $99$
- $33$
- $- \frac{33}{2}$
- $\frac{11}{2}$
- $\frac{33}{2}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{2}^{5}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{-2}^{-1}[uv+{v}^{2}]_{v=2}^{v=5}\,\text{d}u \\  & ={\int }_{-2}^{-1}(3 u + 21)\text{d}u \\  & ={[\frac{3 u \left(u + 14\right)}{2}]}_{-2}^{-1} \\  & =21- \frac{9}{2} \\  & =\frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-161278 / authored_weighted / 0

### q-161278 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $\frac{33}{2}$ (correct)
- $\frac{17}{2}$
- $- \frac{33}{2}$
- $\frac{183}{4}$
- $\frac{47}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{1}^{4}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{0}^{1}[uv+{v}^{2}]_{v=1}^{v=4}\,\text{d}u \\  & ={\int }_{0}^{1}(3 u + 15)\text{d}u \\  & ={[\frac{3 u \left(u + 10\right)}{2}]}_{0}^{1} \\  & =15+\frac{3}{2} \\  & =\frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-161278 / authored_weighted / 1

### q-161278 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $-2\le u\le -1$ and $2\le v\le 5.$

- $- \frac{185}{2}$
- $- \frac{49}{2}$
- $- \frac{33}{2}$
- $\frac{249}{4}$
- $\frac{33}{2}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{2}^{5}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{-2}^{-1}[uv+{v}^{2}]_{v=2}^{v=5}\,\text{d}u \\  & ={\int }_{-2}^{-1}(3 u + 21)\text{d}u \\  & ={[\frac{3 u \left(u + 14\right)}{2}]}_{-2}^{-1} \\  & =21- \frac{9}{2} \\  & =\frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-161278 / authored_rectangle / 0

### q-161278 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $\frac{33}{2}$ (correct)
- $6$
- $- \frac{33}{2}$
- $27$
- $\frac{45}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{1}^{4}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{0}^{1}[uv+{v}^{2}]_{v=1}^{v=4}\,\text{d}u \\  & ={\int }_{0}^{1}(3 u + 15)\text{d}u \\  & ={[\frac{3 u \left(u + 10\right)}{2}]}_{0}^{1} \\  & =15+\frac{3}{2} \\  & =\frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-161278 / authored_rectangle / 1

### q-161278 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u+v,\,v-u,\,-v⟩
$$

for $-2\le u\le -1$ and $2\le v\le 5.$

- $\frac{45}{4}$
- $6$
- $- \frac{33}{2}$
- $27$
- $\frac{33}{2}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(v-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(v-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨1,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -1 & 0 \\ 1 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 1 & -1\end{aligned}|,-|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,2⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨-x-z,\,x-y,\,-z⟩|}_{x=u+v\,y=v-u\,z=-v} \\  & =⟨-(u+v)-(-v),\,u+v-(v-u),\,-(-v)⟩ \\  & =⟨-u,\,2u,\,v⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-u,\,2u,\,v⟩\cdot ⟨1,\,1,\,2⟩ \\  & =(-u)\cdot 1+2u\cdot 1+v\cdot 2 \\  & =-u+2u+2v \\  & =u+2v\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨-x-z,\,x-y,\,-z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(u+2v)\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{2}^{5}(u+2v)\,\text{d}v\,\text{d}u \\  & ={\int }_{-2}^{-1}[uv+{v}^{2}]_{v=2}^{v=5}\,\text{d}u \\  & ={\int }_{-2}^{-1}(3 u + 21)\text{d}u \\  & ={[\frac{3 u \left(u + 14\right)}{2}]}_{-2}^{-1} \\  & =21- \frac{9}{2} \\  & =\frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-161283 / authored_primitive / 0

### q-161283 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 4$ and $1\le v\le 5.$

- $-1277952$
- $-768$ (correct)
- $768$
- $- \frac{1024}{3}$
- $-3072$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{4}{\int }_{1}^{5}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{4}u\,\text{d}u{\int }_{1}^{5}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{4}\cdot {[\frac{1}{2}{v}^{2}]}_{1}^{5} \\  & =-8(8)(12) \\  & =-768.\end{aligned}
$$


## Generated authored bank q-161283 / authored_primitive / 1

### q-161283 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 1$ and $1\le v\le 5.$

- $-48$ (correct)
- $48$
- $-192$
- $-4992$
- $- \frac{64}{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{1}{\int }_{1}^{5}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{1}u\,\text{d}u{\int }_{1}^{5}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{1}\cdot {[\frac{1}{2}{v}^{2}]}_{1}^{5} \\  & =-8(\frac{1}{2})(12) \\  & =-48.\end{aligned}
$$


## Generated authored bank q-161283 / authored_weighted / 0

### q-161283 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 4$ and $1\le v\le 5.$

- $- \frac{63488}{9}$
- $-768$ (correct)
- $768$
- $- \frac{7936}{3}$
- $-2048$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{4}{\int }_{1}^{5}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{4}u\,\text{d}u{\int }_{1}^{5}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{4}\cdot {[\frac{1}{2}{v}^{2}]}_{1}^{5} \\  & =-8(8)(12) \\  & =-768.\end{aligned}
$$


## Generated authored bank q-161283 / authored_weighted / 1

### q-161283 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 1$ and $1\le v\le 5.$

- $-48$ (correct)
- $48$
- $-32$
- $- \frac{992}{9}$
- $- \frac{496}{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{1}{\int }_{1}^{5}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{1}u\,\text{d}u{\int }_{1}^{5}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{1}\cdot {[\frac{1}{2}{v}^{2}]}_{1}^{5} \\  & =-8(\frac{1}{2})(12) \\  & =-48.\end{aligned}
$$


## Generated authored bank q-161283 / authored_rectangle / 0

### q-161283 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 4$ and $1\le v\le 5.$

- $-256$
- $-768$ (correct)
- $768$
- $-2560$
- $0$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{4}{\int }_{1}^{5}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{4}u\,\text{d}u{\int }_{1}^{5}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{4}\cdot {[\frac{1}{2}{v}^{2}]}_{1}^{5} \\  & =-8(8)(12) \\  & =-768.\end{aligned}
$$


## Generated authored bank q-161283 / authored_rectangle / 1

### q-161283 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨u{v}^{2},\,-1,\,1-2u⟩
$$

for $0\le u\le 1$ and $1\le v\le 5.$

- $-48$ (correct)
- $48$
- $0$
- $-16$
- $-160$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{v}^{2}),\,\frac{∂}{∂u}(-1),\,\frac{∂}{∂u}(1-2u)⟩ \\  & =⟨{v}^{2},\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{v}^{2}),\,\frac{∂}{∂v}(-1),\,\frac{∂}{∂v}(1-2u)⟩ \\  & =⟨2uv,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {v}^{2} & 0 & -2 \\ 2uv & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 0 & 0\end{aligned}|,-|\begin{aligned}{v}^{2} & -2 \\ 2uv & 0\end{aligned}|,|\begin{aligned}{v}^{2} & 0 \\ 2uv & 0\end{aligned}|⟩ \\  & =⟨0,\,-4uv,\,0⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨z,\,2,\,-3xy⟩|}_{x=u{v}^{2}\,y=-1\,z=1-2u} \\  & =⟨1-2u,\,2,\,-3(u{v}^{2})(-1)⟩ \\  & =⟨1-2u,\,2,\,3u{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1-2u,\,2,\,3u{v}^{2}⟩\cdot ⟨0,\,-4uv,\,0⟩ \\  & =(1-2u)\cdot 0+2\cdot (-4uv)+3u{v}^{2}\cdot 0 \\  & =-8uv\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨z,\,2,\,-3xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-8uv)\,\text{d}A \\  & =-8{\int }_{0}^{1}{\int }_{1}^{5}uv\,\text{d}v\,\text{d}u \\  & =-8{\int }_{0}^{1}u\,\text{d}u{\int }_{1}^{5}v\,\text{d}v\, \\  & =-8\cdot {[\frac{1}{2}{u}^{2}]}_{0}^{1}\cdot {[\frac{1}{2}{v}^{2}]}_{1}^{5} \\  & =-8(\frac{1}{2})(12) \\  & =-48.\end{aligned}
$$


## Generated authored bank q-161258 / authored_primitive / 0

### q-161258 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $- \frac{201}{4}$ (correct)
- $-198$
- $\frac{201}{4}$
- $- \frac{87}{4}$
- $- \frac{16023}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{1}^{4}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{1}^{4}(-\frac{11}{2}v-3)\text{d}v \\  & ={[-\frac{11}{4}{v}^{2}-3v]}_{1}^{4} \\  & =-9- \frac{165}{4} \\  & =- \frac{201}{4}.\end{aligned}
$$


## Generated authored bank q-161258 / authored_primitive / 1

### q-161258 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $\frac{284001}{20}$
- $180$
- $- \frac{381}{4}$
- $\frac{141}{4}$
- $\frac{381}{4}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{2}^{5}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=-2}^{u=-1}\,\text{d}v \\  & ={\int }_{2}^{5}(\frac{13 v}{2} + 9)\text{d}v \\  & ={[\frac{v \left(13 v + 36\right)}{4}]}_{2}^{5} \\  & =27+\frac{273}{4} \\  & =\frac{381}{4}.\end{aligned}
$$


## Generated authored bank q-161258 / authored_weighted / 0

### q-161258 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $- \frac{201}{4}$ (correct)
- $- \frac{273}{8}$
- $\frac{201}{4}$
- $-138$
- $- \frac{375}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{1}^{4}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{1}^{4}(-\frac{11}{2}v-3)\text{d}v \\  & ={[-\frac{11}{4}{v}^{2}-3v]}_{1}^{4} \\  & =-9- \frac{165}{4} \\  & =- \frac{201}{4}.\end{aligned}
$$


## Generated authored bank q-161258 / authored_weighted / 1

### q-161258 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $- \frac{2109}{4}$
- $- \frac{1155}{8}$
- $- \frac{381}{4}$
- $348$
- $\frac{381}{4}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{2}^{5}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=-2}^{u=-1}\,\text{d}v \\  & ={\int }_{2}^{5}(\frac{13 v}{2} + 9)\text{d}v \\  & ={[\frac{v \left(13 v + 36\right)}{4}]}_{2}^{5} \\  & =27+\frac{273}{4} \\  & =\frac{381}{4}.\end{aligned}
$$


## Generated authored bank q-161258 / authored_rectangle / 0

### q-161258 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $- \frac{201}{4}$ (correct)
- $0$
- $\frac{201}{4}$
- $-162$
- $- \frac{1107}{64}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{1}^{4}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & ={\int }_{1}^{4}(-\frac{11}{2}v-3)\text{d}v \\  & ={[-\frac{11}{4}{v}^{2}-3v]}_{1}^{4} \\  & =-9- \frac{165}{4} \\  & =- \frac{201}{4}.\end{aligned}
$$


## Generated authored bank q-161258 / authored_rectangle / 1

### q-161258 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨3uv,\,u,\,-v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.$*

- $\frac{5481}{64}$
- $72$
- $- \frac{381}{4}$
- $108$
- $\frac{381}{4}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,3v,\,-3u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3x,\,-{y}^{2},\,2⟩|}_{x=3uv\,y=u\,z=-v} \\  & =⟨3(3uv),\,-{u}^{2},\,2⟩ \\  & =⟨9uv,\,-{u}^{2},\,2⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨9uv,\,-{u}^{2},\,2⟩\cdot ⟨-1,\,3v,\,-3u⟩ \\  & =9uv\cdot (-1)+(-{u}^{2})\cdot 3v+2\cdot (-3u) \\  & =-9uv-3{u}^{2}v-6u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3x,\,-{y}^{2},\,2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-9uv-3{u}^{2}v-6u)\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}(-9uv-3{u}^{2}v-6u)\,\text{d}u\,\text{d}v \\  & ={\int }_{2}^{5}{[-\frac{9}{2}{u}^{2}v-{u}^{3}v-3{u}^{2}]}_{u=-2}^{u=-1}\,\text{d}v \\  & ={\int }_{2}^{5}(\frac{13 v}{2} + 9)\text{d}v \\  & ={[\frac{v \left(13 v + 36\right)}{4}]}_{2}^{5} \\  & =27+\frac{273}{4} \\  & =\frac{381}{4}.\end{aligned}
$$


## Generated authored bank q-162593 / authored_primitive / 0

### q-162593 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $- \frac{33}{2}$ (correct)
- $-63$
- $\frac{33}{2}$
- $- \frac{43}{6}$
- $- \frac{99}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{1}^{4}{\int }_{0}^{1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{1}^{4}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =-{\int }_{1}^{4}(2v+\frac{1}{2})\text{d}v \\  & =-{[{v}^{2}+\frac{1}{2}v]}_{1}^{4} \\  & =- \frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-162593 / authored_primitive / 1

### q-162593 / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $-2\le u\le -1$ and $2\le v\le 5.$

- $\frac{1485}{2}$
- $261$
- $- \frac{135}{2}$
- $\frac{59}{2}$
- $\frac{135}{2}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{2}^{5}{\int }_{-2}^{-1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{2}^{5}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=-2}^{u=-1}\,\text{d}v \\  & =-{\int }_{2}^{5}(- 6 v - \frac{3}{2})\text{d}v \\  & =-{[\frac{3 v \left(- 2 v - 1\right)}{2}]}_{2}^{5} \\  & =\frac{135}{2}.\end{aligned}
$$


## Generated authored bank q-162593 / authored_weighted / 0

### q-162593 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $- \frac{33}{2}$ (correct)
- $-11$
- $\frac{33}{2}$
- $- \frac{183}{4}$
- $- \frac{61}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{1}^{4}{\int }_{0}^{1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{1}^{4}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =-{\int }_{1}^{4}(2v+\frac{1}{2})\text{d}v \\  & =-{[{v}^{2}+\frac{1}{2}v]}_{1}^{4} \\  & =- \frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-162593 / authored_weighted / 1

### q-162593 / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $-2\le u\le -1$ and $2\le v\le 5.$

- $- \frac{777}{2}$
- $-105$
- $- \frac{135}{2}$
- $\frac{999}{4}$
- $\frac{135}{2}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{2}^{5}{\int }_{-2}^{-1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{2}^{5}{\int }_{-2}^{-1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{2}^{5}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=-2}^{u=-1}\,\text{d}v \\  & =-{\int }_{2}^{5}(- 6 v - \frac{3}{2})\text{d}v \\  & =-{[\frac{3 v \left(- 2 v - 1\right)}{2}]}_{2}^{5} \\  & =\frac{135}{2}.\end{aligned}
$$


## Generated authored bank q-162593 / authored_rectangle / 0

### q-162593 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $0\le u\le 1$ and $1\le v\le 4.$

- $- \frac{33}{2}$ (correct)
- $0$
- $\frac{33}{2}$
- $-51$
- $-6$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{1}^{4}{\int }_{0}^{1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{1}^{4}{\int }_{0}^{1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{1}^{4}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=0}^{u=1}\,\text{d}v \\  & =-{\int }_{1}^{4}(2v+\frac{1}{2})\text{d}v \\  & =-{[{v}^{2}+\frac{1}{2}v]}_{1}^{4} \\  & =- \frac{33}{2}.\end{aligned}
$$


## Generated authored bank q-162593 / authored_rectangle / 1

### q-162593 / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by the equations

$$
r(u,v)=⟨-v,\,-u,\,{u}^{2}⟩
$$

for $-3\le u\le 1$ and $1\le v\le 5.$

- $240$
- $288$
- $208$ (correct)
- $-208$
- $-336$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-v),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}({u}^{2})⟩ \\  & =⟨0,\,-1,\,2u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-v),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}({u}^{2})⟩ \\  & =⟨-1,\,0,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 0 & -1 & 2u \\ -1 & 0 & 0\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 2u \\ 0 & 0\end{aligned}|,-|\begin{aligned}0 & 2u \\ -1 & 0\end{aligned}|,|\begin{aligned}0 & -1 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨0,\,-2u,\,-1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & ={⟨3z,\,-2x,\,-y⟩|}_{x=-v\,y=-u\,z={u}^{2}} \\  & =⟨3{u}^{2},\,-2(-v),\,-(-u)⟩ \\  & =⟨3{u}^{2},\,2v,\,u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3{u}^{2},\,2v,\,u⟩\cdot ⟨0,\,-2u,\,-1⟩ \\  & =3{u}^{2}\cdot 0+2v\cdot (-2u)+u\cdot (-1) \\  & =-4uv-u\end{aligned}
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}⟨3z,\,-2x,\,-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-4uv-u)\,\text{d}A \\  & ={\int }_{1}^{5}{\int }_{-3}^{1}(-4uv-u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{1}^{5}{\int }_{-3}^{1}(4uv+u)\,\text{d}u\,\text{d}v \\  & =-{\int }_{1}^{5}{[2{u}^{2}v+\frac{1}{2}{u}^{2}]}_{u=-3}^{u=1}\,\text{d}v \\  & =-{\int }_{1}^{5}(- 16 v - 4)\text{d}v \\  & =-{[4 v \left(- 2 v - 1\right)]}_{1}^{5} \\  & =208.\end{aligned}
$$


## Generated authored bank easy_affine_hint / authored_primitive / 0

### easy_affine_hint / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,x,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2 u + v + 1,\,u + v,\,u - v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.$*

- $\frac{123}{2}$ (correct)
- $114$
- $- \frac{123}{2}$
- $\frac{79}{4}$
- $861$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
F(r(u,v))=⟨u - v,\,2 u + v + 1,\,u + v⟩
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
⟨u - v,\,2 u + v + 1,\,u + v⟩\cdot ⟨-2,\,3,\,1⟩=5 u + 6 v + 3
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={\int }_{0}^{1}{\int }_{1}^{4}(5 u + 6 v + 3)\,\text{d}v\,\text{d}u \\ & ={\int }_{0}^{1}[v \left(5 u + 3 v + 3\right)]_{v=1}^{v=4}\,\text{d}u \\ & ={\int }_{0}^{1}(15 u + 54)\,\text{d}u \\ & =[\frac{3 u \left(5 u + 36\right)}{2}]_{0}^{1} \\ & =\frac{123}{2}.\end{aligned}
$$


## Generated authored bank easy_affine_hint / authored_primitive / 1

### easy_affine_hint / authored_primitive

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,x,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2 u + v + 1,\,u + v,\,u - v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.$*

- $693$
- $90$
- $- \frac{99}{2}$
- $\frac{63}{4}$
- $\frac{99}{2}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
F(r(u,v))=⟨u - v,\,2 u + v + 1,\,u + v⟩
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
⟨u - v,\,2 u + v + 1,\,u + v⟩\cdot ⟨-2,\,3,\,1⟩=5 u + 6 v + 3
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={\int }_{-2}^{-1}{\int }_{2}^{5}(5 u + 6 v + 3)\,\text{d}v\,\text{d}u \\ & ={\int }_{-2}^{-1}[v \left(5 u + 3 v + 3\right)]_{v=2}^{v=5}\,\text{d}u \\ & ={\int }_{-2}^{-1}(15 u + 72)\,\text{d}u \\ & =[\frac{3 u \left(5 u + 48\right)}{2}]_{-2}^{-1} \\ & =\frac{99}{2}.\end{aligned}
$$


## Generated authored bank easy_affine_hint / authored_weighted / 0

### easy_affine_hint / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,x,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2 u + v + 1,\,u + v,\,u - v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.$*

- $\frac{123}{2}$ (correct)
- $32$
- $- \frac{123}{2}$
- $\frac{669}{4}$
- $\frac{347}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
F(r(u,v))=⟨u - v,\,2 u + v + 1,\,u + v⟩
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
⟨u - v,\,2 u + v + 1,\,u + v⟩\cdot ⟨-2,\,3,\,1⟩=5 u + 6 v + 3
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={\int }_{0}^{1}{\int }_{1}^{4}(5 u + 6 v + 3)\,\text{d}v\,\text{d}u \\ & ={\int }_{0}^{1}[v \left(5 u + 3 v + 3\right)]_{v=1}^{v=4}\,\text{d}u \\ & ={\int }_{0}^{1}(15 u + 54)\,\text{d}u \\ & =[\frac{3 u \left(5 u + 36\right)}{2}]_{0}^{1} \\ & =\frac{123}{2}.\end{aligned}
$$


## Generated authored bank easy_affine_hint / authored_weighted / 1

### easy_affine_hint / authored_weighted

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,x,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2 u + v + 1,\,u + v,\,u - v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.$*

- $- \frac{1103}{4}$
- $-73$
- $- \frac{99}{2}$
- $\frac{747}{4}$
- $\frac{99}{2}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
F(r(u,v))=⟨u - v,\,2 u + v + 1,\,u + v⟩
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
⟨u - v,\,2 u + v + 1,\,u + v⟩\cdot ⟨-2,\,3,\,1⟩=5 u + 6 v + 3
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={\int }_{-2}^{-1}{\int }_{2}^{5}(5 u + 6 v + 3)\,\text{d}v\,\text{d}u \\ & ={\int }_{-2}^{-1}[v \left(5 u + 3 v + 3\right)]_{v=2}^{v=5}\,\text{d}u \\ & ={\int }_{-2}^{-1}(15 u + 72)\,\text{d}u \\ & =[\frac{3 u \left(5 u + 48\right)}{2}]_{-2}^{-1} \\ & =\frac{99}{2}.\end{aligned}
$$


## Generated authored bank easy_affine_hint / authored_rectangle / 0

### easy_affine_hint / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,x,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2 u + v + 1,\,u + v,\,u - v⟩
$$

over the domain $D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 4}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.$*

- $\frac{123}{2}$ (correct)
- $27$
- $- \frac{123}{2}$
- $96$
- $\frac{177}{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
F(r(u,v))=⟨u - v,\,2 u + v + 1,\,u + v⟩
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
⟨u - v,\,2 u + v + 1,\,u + v⟩\cdot ⟨-2,\,3,\,1⟩=5 u + 6 v + 3
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={\int }_{0}^{1}{\int }_{1}^{4}(5 u + 6 v + 3)\,\text{d}v\,\text{d}u \\ & ={\int }_{0}^{1}[v \left(5 u + 3 v + 3\right)]_{v=1}^{v=4}\,\text{d}u \\ & ={\int }_{0}^{1}(15 u + 54)\,\text{d}u \\ & =[\frac{3 u \left(5 u + 36\right)}{2}]_{0}^{1} \\ & =\frac{123}{2}.\end{aligned}
$$


## Generated authored bank easy_affine_hint / authored_rectangle / 1

### easy_affine_hint / authored_rectangle

Evaluate the surface integral

$$
{∬}_{S}⟨z,\,x,\,y⟩\cdot \text{d}S
$$

where the parametric surface $S$ is defined by

$$
r(u,v)=⟨2 u + v + 1,\,u + v,\,u - v⟩
$$

over the domain $D={(u,v)\,:\,-2\le u\le -1,\,2\le v\le 5}.$

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.$*

- $\frac{129}{4}$
- $15$
- $- \frac{99}{2}$
- $84$
- $\frac{99}{2}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We're given that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-2,\,3,\,1⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
F(r(u,v))=⟨u - v,\,2 u + v + 1,\,u + v⟩
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
⟨u - v,\,2 u + v + 1,\,u + v⟩\cdot ⟨-2,\,3,\,1⟩=5 u + 6 v + 3
$$

Therefore, the surface integral evaluates to

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={\int }_{-2}^{-1}{\int }_{2}^{5}(5 u + 6 v + 3)\,\text{d}v\,\text{d}u \\ & ={\int }_{-2}^{-1}[v \left(5 u + 3 v + 3\right)]_{v=2}^{v=5}\,\text{d}u \\ & ={\int }_{-2}^{-1}(15 u + 72)\,\text{d}u \\ & =[\frac{3 u \left(5 u + 48\right)}{2}]_{-2}^{-1} \\ & =\frac{99}{2}.\end{aligned}
$$
