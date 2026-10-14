# Template extraction

## Stage1 — specific captured objects

The following source prompts, restrictions, field layouts and every option are captured at one frozen basis. source.json preserves complete raw evidence. Every bank is five math options. Correct presence is reported separately from inferred mathematical correctness.

### saddle — q-160711

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=xyz$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,v,\,uv⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨1,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & u\end{aligned}|,\,-|\begin{aligned}1 & v \\ 0 & u\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-v,\,-u,\,1⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-v,\,-u,\,1⟩‖ \\  & =\sqrt{(-v)^{2}+(-u)^{2}+(1)^{2}} \\  & =\sqrt{{u}^{2}+{v}^{2}+1}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(xyz)\,{|}_{x=u\,y=v\,z=uv} \\  & =u\cdot v\cdot uv \\  & ={u}^{2}{v}^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,{u}^{2}{v}^{2}\sqrt{{u}^{2}+{v}^{2}+1}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field 8b5413c5-cd70-5f06-8ea5-ec7c6d11e516 / correct ABSENT

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|9be70133-e143-555a-b316-c857cb78e325|`u^{2}v^{2}\sqrt{u^{2} + v^{2} + 1}`|`k(u^{2}v^{2}\sqrt{u^{2} + v^{2} + 1})`|

|a6c62bb4-f2b7-5a28-bab7-5df3a9504149|`uv\sqrt{u^{2} + v^{2} + 1}`|`k(uv\sqrt{u^{2} + v^{2} + 1})`|

|cdf2f94a-1a8b-5d99-8a70-f07f6c82f8fd|`u^{2}v^{2}\sqrt{uv}`|`k(u^{2}v^{2}\sqrt{uv})`|

|0966e2fa-eeb2-5012-9af2-d57f5e7b0e1f|`u^{2}v^{2}\sqrt{u + v}`|`k(u^{2}v^{2}\sqrt{u + v})`|

|2e1bec9b-3572-5c9b-a9e1-b8bf0036f7d4|`uv\sqrt{uv}`|`k(uv\sqrt{uv})`|

Bank 1 / field 5b5472ad-00ad-5af8-bfaf-97021ee46355 / correct {u}^{2}{v}^{2}\sqrt{{u}^{2}+{v}^{2}+1}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|4c6491ad-31df-5c44-8510-45289f4f4d41|`{u}^{2}{v}^{2}\sqrt{u+v}`|`k({u}^{2}{v}^{2}\sqrt{u+v})`|

|ae2a58c0-318a-559b-8de4-48cf1599122b|`{u}^{2}{v}^{2}\sqrt{uv}`|`k({u}^{2}{v}^{2}\sqrt{uv})`|

|66a3fc66-6953-52e2-8b17-93c3ff13ddf6|`uv\sqrt{uv}`|`k(uv\sqrt{uv})`|

|c9fed922-03a1-59c5-b2d8-bcf5a4514733|`uv\sqrt{{u}^{2}+{v}^{2}+1}`|`k(uv\sqrt{{u}^{2}+{v}^{2}+1})`|

|ecef412c-1fbd-55f7-a2eb-dcc4e3d8418d|`{u}^{2}{v}^{2}\sqrt{{u}^{2}+{v}^{2}+1}`|`k({u}^{2}{v}^{2}\sqrt{{u}^{2}+{v}^{2}+1})`|

### cancel — q-160712

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x+y+z$ 
over the parametric surface 

$$
r(u,v)=⟨{u}^{2},\,u-{v}^{2},\,{v}^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=2v\sqrt{1+8{u}^{2}}.$*

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{{u}^{2}+{v}^{2}+1}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x+y+z)\,{|}_{x={u}^{2}\,y=u-{v}^{2}\,z={v}^{2}} \\  & ={u}^{2}+(u-{v}^{2})+{v}^{2} \\  & ={u}^{2}+u\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,2({u}^{2}+u)v\sqrt{1+8{u}^{2}}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field 758915d5-fc00-56c4-ac7b-2a8b40d5ac5f / correct 2({u}^{2}+u)v\sqrt{1+8{u}^{2}}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|0a6318e5-3878-5d26-b61b-739d349729a7|`2({u}^{2}+u)v\sqrt{1+8{u}^{2}}`|`k(2({u}^{2}+u)v\sqrt{1+8{u}^{2}})`|

|2913e3a7-4834-5ae0-8725-8cf0ddd19bbe|`2({u}^{2}+uv+{u}^{2})v\sqrt{1+8{u}^{2}}`|`k(2({u}^{2}+uv+{u}^{2})v\sqrt{1+8{u}^{2}})`|

|4635f4d0-2e93-54c6-a194-c7414540fea3|`2({u}^{2}-{v}^{2})v\sqrt{1+8{u}^{2}}`|`k(2({u}^{2}-{v}^{2})v\sqrt{1+8{u}^{2}})`|

|8e7629cd-993c-5b5b-a5b5-4827bb2f0380|`2{u}^{2}{v}^{2}\sqrt{1+8{u}^{2}}`|`k(2{u}^{2}{v}^{2}\sqrt{1+8{u}^{2}})`|

|fa861672-33f6-547e-b490-0aa338df3abc|`2(u+v)v\sqrt{1+8{u}^{2}}`|`k(2(u+v)v\sqrt{1+8{u}^{2}})`|

### cubic — q-161132

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=xy+z$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,{u}^{2},\,2v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16{u}^{2}+4}$*

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16{u}^{2}+4}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(xy+z)\,{|}_{x=u\,y={u}^{2}\,z=2v} \\  & =u.{u}^{2}+2v \\  & ={u}^{3}+2v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,({u}^{3}+2v)\sqrt{16{u}^{2}+4}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field 6e029e9e-eb95-5dc6-b173-809d27542530 / correct ({u}^{3}+2v)\sqrt{16{u}^{2}+4}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|407b054a-ad2a-5003-b975-08ebe629a652|`({v}^{3}+2v)\sqrt{16{u}^{2}+4}`|`k(({v}^{3}+2v)\sqrt{16{u}^{2}+4})`|

|4c0afc67-2eaf-50ff-a740-16da7f2c7971|`({u}^{3}+{v}^{3})\sqrt{16{v}^{2}+4}`|`k(({u}^{3}+{v}^{3})\sqrt{16{v}^{2}+4})`|

|533273b3-79e7-5ab4-8e9c-12dbf680ea3c|`({v}^{2}+2u)\sqrt{16{u}^{2}+4}`|`k(({v}^{2}+2u)\sqrt{16{u}^{2}+4})`|

|6262307b-481e-5435-ad06-56dd718d0e29|`(u+v)\sqrt{16{u}^{2}+4}`|`k((u+v)\sqrt{16{u}^{2}+4})`|

|ae06b05f-02ef-5a1f-88b5-160bedb18ca3|`({u}^{3}+2v)\sqrt{16{u}^{2}+4}`|`k(({u}^{3}+2v)\sqrt{16{u}^{2}+4})`|

### powers — q-161134

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)={x}^{2}{y}^{2}{z}^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨{u}^{2},\,v,\,v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{8}u.$*

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{8}u.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =({x}^{2}{y}^{2}{z}^{2})\,{|}_{x={u}^{2}\,y=v\,z=v} \\  & =({u}^{2}\cdot {u}^{2})\cdot {v}^{2}\cdot {v}^{2}\, \\  & ={u}^{4}{v}^{4}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{8}\,{u}^{5}{v}^{4}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field e911c170-af03-582c-ad47-4ba84716458b / correct \sqrt{8}\,{u}^{5}{v}^{4}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|40de9f5d-9bb8-505f-856c-ce2c6913769b|`\sqrt{8}\,{u}^{3}{v}^{4}`|`k(\sqrt{8}\,{u}^{3}{v}^{4})`|

|9a30988f-5c27-5ce0-8684-641402fd6ea6|`\sqrt{8}\,{u}^{4}{v}^{5}`|`k(\sqrt{8}\,{u}^{4}{v}^{5})`|

|c2412b0e-122f-55ad-9a36-81cdc271d082|`\sqrt{8}\,{u}^{2}{v}^{2}`|`k(\sqrt{8}\,{u}^{2}{v}^{2})`|

|d49654d0-756c-5b91-9e96-98d9917a2ace|`\sqrt{8}\,{u}^{3}{v}^{3}`|`k(\sqrt{8}\,{u}^{3}{v}^{3})`|

|ea08dbc3-4809-5054-a017-c2a23b383426|`\sqrt{8}\,{u}^{5}{v}^{4}`|`k(\sqrt{8}\,{u}^{5}{v}^{4})`|

### product — q-161136

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=-{x}^{2}+3yz$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,u+v,\,{v}^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{8{v}^{2}+1}.$*

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{8{v}^{2}+1}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(-{x}^{2}+3yz)\,{|}_{x=u\,y=u+v\,z={v}^{2}} \\  & =-(u\cdot u)+3\cdot (u+v)\cdot ({v}^{2}) \\  & =-{u}^{2}+3(u+v){v}^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,(-{u}^{2}+3(u+v){v}^{2})\sqrt{8{v}^{2}+1}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field eebba4c6-890d-5236-a8b1-f85351eb3247 / correct (-{u}^{2}+3(u+v){v}^{2})\sqrt{8{v}^{2}+1}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|60908e82-b692-599f-82b9-892161866329|`(-{u}^{2}+3(u+v){v}^{2})\sqrt{8{v}^{2}+1}`|`k((-{u}^{2}+3(u+v){v}^{2})\sqrt{8{v}^{2}+1})`|

|708462c8-f5ae-5b10-8bc2-cbaa9b1a5f89|`(-{u}^{2}-3(u-v){v}^{2})\sqrt{8{v}^{2}+1}`|`k((-{u}^{2}-3(u-v){v}^{2})\sqrt{8{v}^{2}+1})`|

|7755f123-28ec-560e-a4c0-0541364afe71|`({u}^{2}-3(u+v){v}^{2})\sqrt{8{v}^{2}+1}`|`k(({u}^{2}-3(u+v){v}^{2})\sqrt{8{v}^{2}+1})`|

|7f3e8ea1-6b77-5aea-ae14-47ac28753c57|`(-{u}^{2}-3({u}^{2}+v){v}^{2})\sqrt{8{v}^{2}+1}`|`k((-{u}^{2}-3({u}^{2}+v){v}^{2})\sqrt{8{v}^{2}+1})`|

|a35498bf-e5d4-5d74-b5ee-fd684180144f|`({u}^{2}+3(u+v){v}^{2})\sqrt{8{v}^{2}+1}`|`k(({u}^{2}+3(u+v){v}^{2})\sqrt{8{v}^{2}+1})`|

### negative_plane — q-161285

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)={x}^{2}{z}^{2}+y$ 
over the parametric surface 

$$
r(u,v)=⟨-u,\,-u,\,-v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}(-v)⟩ \\  & =⟨-1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}(-v)⟩ \\  & =⟨0,\,0,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ -1 & -1 & 0 \\ 0 & 0 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & -0 \\ 0 & -1\end{aligned}|,\,-|\begin{aligned}-1 & 0 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}-1 & -1 \\ 0 & 0\end{aligned}|⟩ \\  & =⟨1,\,-1,\,0⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨1,\,-1,\,0⟩‖ \\  & =\sqrt{(1)^{2}+(-1)^{2}+(0)^{2}} \\  & =\sqrt{2}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =({x}^{2}{z}^{2}+y)\,{|}_{x=-u\,y=-u\,z=-v} \\  & =(-u)^{2}\cdot (-v)^{2}-u \\  & ={u}^{2}{v}^{2}-u\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,({u}^{2}{v}^{2}-u)\sqrt{2}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field dc456dfe-3c1e-58f1-9083-307a9c6e88a7 / correct ({u}^{2}{v}^{2}-u)\sqrt{2}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|02421d75-88be-52d7-b6a4-7091fc5bc066|`({u}^{2}{v}^{2}-u)\sqrt{2}`|`k(({u}^{2}{v}^{2}-u)\sqrt{2})`|

|37a3b016-ad87-55b8-92c0-56d4b344f479|`(uv-u)\sqrt{2u}`|`k((uv-u)\sqrt{2u})`|

|4f430a34-697b-5af8-a53f-71af555ef03e|`{u}^{2}v\sqrt{2}`|`k({u}^{2}v\sqrt{2})`|

|67494c52-64b3-56cb-b6c1-1db2880ed8b4|`({u}^{2}{v}^{2}+2)\sqrt{2}`|`k(({u}^{2}{v}^{2}+2)\sqrt{2})`|

|f4d8f707-b205-57cd-849c-7a0bdc24dc3b|`(u{v}^{2}+u)\sqrt{2u}`|`k((u{v}^{2}+u)\sqrt{2u})`|

### fold — q-161286

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=-x-y-z$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,{v}^{2}-{u}^{2},\,u⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}({v}^{2}-{u}^{2}),\,\frac{∂}{∂u}(u)⟩ \\  & =⟨1,\,-2u,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}({v}^{2}-{u}^{2}),\,\frac{∂}{∂v}(u)⟩ \\  & =⟨0,\,2v,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -2u & 1 \\ 0 & 2v & 0\end{aligned}| \\  & =⟨|\begin{aligned}-2u & 1 \\ 2v & 0\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 0\end{aligned}|,\,|\begin{aligned}1 & -2u \\ 0 & 2v\end{aligned}|⟩ \\  & =⟨-2u,\,0,\,2v⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-2v,\,0,\,2v⟩‖ \\  & =\sqrt{(-2v)^{2}+(0)^{2}+(2v)^{2}} \\  & =\sqrt{4{v}^{2}+4{v}^{2}} \\  & =\sqrt{8}v.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(-x-y-z)\,{|}_{x=u\,y={v}^{2}-{u}^{2}\,z=u} \\  & =-u-({v}^{2}-{u}^{2})-u \\  & ={u}^{2}-{v}^{2}-2u\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,({u}^{2}-{v}^{2}-2u)\sqrt{8}v\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field 67ccc538-716e-5741-af32-020559500c0f / correct ({u}^{2}-{v}^{2}-2u)\sqrt{8}v

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|0e8eb946-bade-52e7-a628-5f87cb28e35c|`({u}^{2}+{v}^{2}+u)\sqrt{8v}`|`k(({u}^{2}+{v}^{2}+u)\sqrt{8v})`|

|12277fa3-1146-5aca-a0ac-a0f443b4ecd4|`({v}^{2}-{u}^{2}-2)\sqrt{8}`|`k(({v}^{2}-{u}^{2}-2)\sqrt{8})`|

|905035c0-ecb9-5958-a0aa-abb13fc99ee9|`({u}^{2}-{v}^{2})\sqrt{8}u`|`k(({u}^{2}-{v}^{2})\sqrt{8}u)`|

|aa693649-bf12-5748-af20-c60686051053|`({u}^{2}-{v}^{2}-2u)\sqrt{8}v`|`k(({u}^{2}-{v}^{2}-2u)\sqrt{8}v)`|

|f72b9498-2b49-5473-af2a-31b5ee8fb2c3|`({u}^{2}+2v+2u)\sqrt{8}v`|`k(({u}^{2}+2v+2u)\sqrt{8}v)`|

### mixed — q-161290

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x-{y}^{2}z$ 
over the parametric surface 

$$
r(u,v)=⟨uv,\,-u,\,-{v}^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(uv),\,\frac{∂}{∂u}(-u),\,\frac{∂}{∂u}(-{v}^{2})⟩ \\  & =⟨v,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(uv),\,\frac{∂}{∂v}(-u),\,\frac{∂}{∂v}(-{v}^{2})⟩ \\  & =⟨u,\,0,\,-2v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ v & -1 & 0 \\ u & 0 & -2v\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 0 & -2v\end{aligned}|,\,-|\begin{aligned}v & 0 \\ u & -2v\end{aligned}|,\,|\begin{aligned}v & -1 \\ u & 0\end{aligned}|⟩ \\  & =⟨2v,\,2{v}^{2},\,u⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨2v,\,2{v}^{2},\,u⟩‖ \\  & =\sqrt{(2v)^{2}+(2{v}^{2})^{2}+(u)^{2}} \\  & =\sqrt{4{v}^{2}+4{v}^{4}+{u}^{2}}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x-{y}^{2}z)\,{|}_{x=uv\,y=-u\,z=-{v}^{2}} \\  & =uv-(-u)^{2}\cdot -{v}^{2} \\  & =uv+{u}^{2}{v}^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,(uv+{u}^{2}{v}^{2})\sqrt{4{v}^{2}+4{v}^{4}+{u}^{2}}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field 04191987-1090-56e3-a6b5-b166d86bb243 / correct (uv+{u}^{2}{v}^{2})\sqrt{4{v}^{2}+4{v}^{4}+{u}^{2}}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|6af8c537-e57b-5716-8d12-63fcd367dcd4|`(uv+uv)\sqrt{2{v}^{2}+4{v}^{4}-{u}^{2}}`|`k((uv+uv)\sqrt{2{v}^{2}+4{v}^{4}-{u}^{2}})`|

|764eb8f7-0869-594c-952a-68e04921067e|`(v-{u}^{2}{v}^{2})\sqrt{4{v}^{2}+2{v}^{4}+u}`|`k((v-{u}^{2}{v}^{2})\sqrt{4{v}^{2}+2{v}^{4}+u})`|

|7b524c5d-049b-59c5-aed7-b77cbc36dee4|`(u+{u}^{2}{v}^{2})\sqrt{{v}^{2}-4{v}^{4}-{u}^{2}}`|`k((u+{u}^{2}{v}^{2})\sqrt{{v}^{2}-4{v}^{4}-{u}^{2}})`|

|dafd65c0-be97-5117-b59c-70e2892517b6|`(uv+{u}^{2}{v}^{2})\sqrt{4{v}^{2}+4{v}^{4}+{u}^{2}}`|`k((uv+{u}^{2}{v}^{2})\sqrt{4{v}^{2}+4{v}^{4}+{u}^{2}})`|

|fe7356ca-baea-56e4-9138-a82a9af96807|`(uv+u{v}^{2})\sqrt{4{v}^{2}+{v}^{2}+{v}^{2}{u}^{2}}`|`k((uv+u{v}^{2})\sqrt{4{v}^{2}+{v}^{2}+{v}^{2}{u}^{2}})`|

### plane — q-161124

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)={x}^{2}+{y}^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,u,\,v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v)⟩ \\  & =⟨1,\,1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v)⟩ \\  & =⟨0,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =⟨|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|,\,-|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 1 \\ 0 & 0\end{aligned}|⟩ \\  & =⟨1,\,-1,\,0⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨1,\,-1,\,0⟩‖ \\  & =\sqrt{(1)^{2}+(-1)^{2}+(0)^{2}} \\  & =\sqrt{1+1+0} \\  & =\sqrt{2}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =({x}^{2}+{y}^{2})\,{|}_{x=u\,y=u\,z=v} \\  & ={u}^{2}+{u}^{2} \\  & =2{u}^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,2\sqrt{2}{u}^{2}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field 16fadbea-4516-5df4-9f64-8b7cc353d5a0 / correct 2\sqrt{2}{u}^{2}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|31c23b1e-7cd7-5e7a-8c99-254c33c9229b|`{v}^{2}`|`k({v}^{2})`|

|b146a4db-c677-57ea-92f8-07f41239596d|`2\sqrt{2}{u}^{2}`|`k(2\sqrt{2}{u}^{2})`|

|b723dafe-f5a6-5a70-be14-953187b88dde|`{u}^{2}`|`k({u}^{2})`|

|c87217ff-e3d3-5223-ac71-463a0c197918|`\sqrt{2}{u}^{2}`|`k(\sqrt{2}{u}^{2})`|

|e4f2c71c-8604-5aa1-9ce7-1663a5f2e6db|`{u}^{2}+{v}^{2}`|`k({u}^{2}+{v}^{2})`|

### cylinder — q-161288

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=-x-{z}^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨{u}^{3},\,v,\,{v}^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{3}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}({v}^{2})⟩ \\  & =⟨3{u}^{2},\,0,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{3}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}({v}^{2})⟩ \\  & =⟨0,\,1,\,2v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 3{u}^{2} & 0 & 0 \\ 0 & 1 & 2v\end{aligned}| \\  & =⟨|\begin{aligned}0 & 0 \\ 1 & 2v\end{aligned}|,\,-|\begin{aligned}3{u}^{2} & 0 \\ 0 & 2v\end{aligned}|,\,|\begin{aligned}3{u}^{2} & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨0,\,-6v{u}^{2},\,3{u}^{2}⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨0,\,-6v{u}^{2},\,3{u}^{2}⟩‖ \\  & =\sqrt{(0)^{2}+(-6v{u}^{2})^{2}+(3{u}^{2})^{2}} \\  & =\sqrt{36{v}^{2}{u}^{4}+9{u}^{4}} \\  & =3{u}^{2}\sqrt{4{v}^{2}+1}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(-x-{z}^{2})\,{|}_{x={u}^{3}\,y=v\,z={v}^{2}} \\  & =-{u}^{3}-({v}^{2}\cdot {v}^{2}) \\  & =-{u}^{3}-{v}^{4}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,3{u}^{2}(-{u}^{3}-{v}^{4})\sqrt{4{v}^{2}+1}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field 72a815fc-9d19-53b2-b0ae-b65abcc40317 / correct 3{u}^{2}(-{u}^{3}-{v}^{4})\sqrt{4{v}^{2}+1}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|0cd71aa2-2da0-53d3-a18e-57cc7dd66fe2|`{u}^{2}(-{u}^{3}+{v}^{4})\sqrt{4uv+u}`|`k({u}^{2}(-{u}^{3}+{v}^{4})\sqrt{4uv+u})`|

|6a78c70d-c252-5fa1-b3b9-b5253f7112ea|`3{u}^{2}(-{u}^{3}-{v}^{4})\sqrt{4{v}^{2}+1}`|`k(3{u}^{2}(-{u}^{3}-{v}^{4})\sqrt{4{v}^{2}+1})`|

|a93dd97e-74c6-56c8-a6b1-3cdadc7213e0|`3{u}^{2}({u}^{4}-{v}^{3})\sqrt{4{u}^{2}+1}`|`k(3{u}^{2}({u}^{4}-{v}^{3})\sqrt{4{u}^{2}+1})`|

|cb42e303-0573-52db-81ce-d57e99e6f761|`6{v}^{2}({u}^{2}+{v}^{4})\sqrt{{v}^{2}+1}`|`k(6{v}^{2}({u}^{2}+{v}^{4})\sqrt{{v}^{2}+1})`|

|d505a7da-72d5-5c19-aa46-75ea67cf0bb1|`u(-{u}^{3}-{v}^{4})\sqrt{4{v}^{3}+u}`|`k(u(-{u}^{3}-{v}^{4})\sqrt{4{v}^{3}+u})`|

### signed — q-161135

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=xz+y$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,-v,\,-{v}^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{1+4{v}^{2}}.$*

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{1+4{v}^{2}}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(xz+y)\,{|}_{x=u\,y=-v\,z={v}^{2}} \\  & =u\cdot (-{v}^{2})+(-v) \\  & =-u{v}^{2}-v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,(-u{v}^{2}-v)\sqrt{1+4{v}^{2}}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field de80caed-f292-5fbc-ae6d-5bf6abf46eda / correct (-u{v}^{2}-v)\sqrt{1+4{v}^{2}}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|059c12fe-eab5-50d3-812e-daede28e5fce|`(-uv-v)\sqrt{1+4{v}^{2}}`|`k((-uv-v)\sqrt{1+4{v}^{2}})`|

|a69adeb6-2c36-5a75-b29d-f701876ba59a|`(-u{v}^{2}+v)\sqrt{1+4{v}^{2}}`|`k((-u{v}^{2}+v)\sqrt{1+4{v}^{2}})`|

|cbbd9a36-5d62-5a45-a0b6-211a1e349cc3|`(u{v}^{2}-{v}^{2})\sqrt{1+4{v}^{2}}`|`k((u{v}^{2}-{v}^{2})\sqrt{1+4{v}^{2}})`|

|ded9ba33-54e3-5794-92a9-b6db153210e8|`(-u{v}^{2}-v)\sqrt{1+4{v}^{2}}`|`k((-u{v}^{2}-v)\sqrt{1+4{v}^{2}})`|

|e264331f-dc93-54c6-bb93-c8cd29731c14|`(-u{v}^{2}+{v}^{2})\sqrt{1+4{v}^{2}}`|`k((-u{v}^{2}+{v}^{2})\sqrt{1+4{v}^{2}})`|

### quadratic — q-161133

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x+z$ 
over the parametric surface 

$$
r(u,v)=⟨uv,\,{u}^{2},\,{v}^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression?

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}.$*

Exact worked solution:

```text
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x+z)\,{|}_{x=uv\,y={u}^{2}\,z={v}^{2}} \\  & =uv+{v}^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,(uv+{v}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}\,\,\text{d}A.\end{aligned}
$$
```

Bank 0 / field 39e51a49-d535-578a-8167-c77ca61f8305 / correct (uv+{v}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}

|Original answer ID|Exact value|Parameterized observed expression|

|---|---|---|

|1796399c-8c6d-5f22-bede-36efd1a03f5a|`uv\sqrt{{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}`|`k(uv\sqrt{{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}})`|

|8e82d031-e34f-52ca-aadf-8e8d59c47bb2|`(uv+{v}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}`|`k((uv+{v}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}})`|

|bdf13d7f-d54d-59f5-9209-239de83443e0|`(v+{v}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{2}+4{u}^{4}}`|`k((v+{v}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{2}+4{u}^{4}})`|

|bf1e4b2c-7a9b-5b87-a6e2-85dd90a414fd|`(uv+{u}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{2}+4{u}^{4}}`|`k((uv+{u}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{2}+4{u}^{4}})`|

|d04576fc-a1ab-5d09-bca6-54a80b70447c|`{v}^{2}\sqrt{{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}`|`k({v}^{2}\sqrt{{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}})`|

## Stage2 — shared mathematical pattern

Construct f(r(u,v)) ||r_u×r_v|| as a scalar function on the parameter domain. The response is the missing pointwise integrand, rather than any definite-integral value. Easy is supplied the norm; moderate performs the complete held-coordinate tangent, signed-minor, norm and pullback calculation. Each variant keeps its source’s own coordinate products, signs, cancellation and reduction rather than introducing another method.

## Stage3 — components and banks

Prompt slots are complete scalar-function expressions, complete vectors, hint norms, and supported domain clauses. Normal source-shaped families use a (first coordinate scale1..3), p and q (nonzero scalar-function term weights1..4). saddle and powers have no second term: q=1 is enforced and excluded from task variety. Source observed profiles instead expose k (nonzero integer magnitude≤5), multiply the entire scalar function and entire observed bank, and preserve every fixed surface derivative block and raw solution component. This genuine scalar linearity recipe explains whole-expression covariance, not the historical author’s error intentions. Opaque square-root/variable substitutions remain explicitly uninterpreted; their exact source operations are mapped in every table above. Raw profiles stay ineligible.

Normal banks are complete authored method-derived profiles. Multi-term pullbacks: correct product; omit metric; omit one explicitly ordered pullback term; reverse that term’s sign; use squared metric. The monomial saddle/powers families: correct product; omit metric; omit one actual u factor; omit one actual v factor; use squared metric. The plane family combines two squared coordinate contributions into a single monomial, so its separate profile uses: correct product; omit metric; omit y² contribution; use v for both coordinates; use v for y only. All bank members are built from actual displayed coordinates/function; no arbitrary constant perturbations or pooled replacement. A collision rejects the entire instance.

## Stage4 — reusable masks and constraints

raw_content compiles source full-expression masks, parameterizes f, every operative pullback expression and final integrand, and scales all exact source answer expressions. No branch returns a source question payload. At k=1 the masks reproduce the full prompt and solution exactly; parameter2 checks verify scaling through the same public generate interface. Source fields use owned UUID identities, preserve missing refs, retain both legacy layouts, normalize nested enum maps to local enum strings, and deterministically shuffle each whole bank.

normal_content replaces complete source math blocks while retaining all common source prose. Dynamic formal operators retain held-coordinate zero contributions; cross products retain determinant, three signed minors, and signed vector; norm retains squared component substitution and source-specific additional expanded/factored rows for plane/fold/cylinder; pullback retains coordinate restriction, original family ordered products/cancellation and reduction; final integral remains the original two-stage construction. The quadratic family retains its two-row pullback without a redundant reduction. Normalized TeX spacing and equivalent factor spelling are documented presentation changes; raw profiles remain byte-exact.

Each source norm’s factor convention is retained. Cylinder uses3a u²sqrt(4v²+1); fold uses2v sqrt(a²+1) on v≥0; powers uses sqrt(8)a u on u≥0; cancel uses2v sqrt(1+8a²u²) on v≥0. Unevaluated product/cancellation masks are verified before final simplification.

Hard coefficients a,b,c,d,p,q are1..3, all nonzero: r=⟨a uv,-b u,c u-d v²⟩, f=p x-q y²z. The same displayed block/prose route as observed mixed applies, with the extra mixed-coordinate derivative contribution and expanded pullback. This is authored scope, never a recovered source difficulty. Explicit inputs obey all bounds and exact key sets.

Identity uses actual displayed prompt, solution, complete bank and level; seed/order changes do not alter IDs. Mathematical fingerprint omits bank/profile and includes actual printed f/r and norm-given-versus-computed demand. No unused q aliases are permitted. No generated graph assets or database writes.
