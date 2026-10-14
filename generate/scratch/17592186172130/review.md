# Source and generated review

Raw captures use explicit observed profile, including legacy omissions. Generated variants use method-derived banks and repaired learner content.


## original replay — saddle / moderate

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

- $u^{2}v^{2}\sqrt{u + v}$
- $u^{2}v^{2}\sqrt{u^{2} + v^{2} + 1}$
- $uv\sqrt{u^{2} + v^{2} + 1}$
- $uv\sqrt{uv}$
- $u^{2}v^{2}\sqrt{uv}$
- ${u}^{2}{v}^{2}\sqrt{{u}^{2}+{v}^{2}+1}$
- $uv\sqrt{{u}^{2}+{v}^{2}+1}$
- ${u}^{2}{v}^{2}\sqrt{uv}$
- $uv\sqrt{uv}$
- ${u}^{2}{v}^{2}\sqrt{u+v}$

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



## generated variant — saddle / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x y z$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,v,\,u v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $u^{2} v^{2} \sqrt{u^{2} + v^{2} + 1}$
- $u^{2} v \sqrt{u^{2} + v^{2} + 1}$
- $u^{2} v^{2}$
- $u^{2} v^{2} \left(u^{2} + v^{2} + 1\right)$
- $u v^{2} \sqrt{u^{2} + v^{2} + 1}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u v)⟩ \\  & =⟨1,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u v)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & u\end{aligned}|,\,-|\begin{aligned}1 & v \\ 0 & u\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨- v,\,- u,\,1⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨- v,\,- u,\,1⟩‖ \\  & =\sqrt{(- v)^{2}+(- u)^{2}+(1)^{2}} \\  & =\sqrt{u^{2} + v^{2} + 1}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x y z)\,{|}_{x=u\,y=v\,z=u v} \\  & =(u)\cdot v\cdot uv \\  & =u^{2} v^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,u^{2} v^{2} \sqrt{u^{2} + v^{2} + 1}\,\,\text{d}A.\end{aligned}
$$



## generated variant — saddle / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x y z$ 
over the parametric surface 

$$
r(u,v)=⟨2 u,\,v,\,u v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $6 u^{2} v \sqrt{4 u^{2} + v^{2} + 4}$
- $6 u^{2} v^{2} \left(4 u^{2} + v^{2} + 4\right)$
- $6 u^{2} v^{2} \sqrt{4 u^{2} + v^{2} + 4}$
- $6 u v^{2} \sqrt{4 u^{2} + v^{2} + 4}$
- $6 u^{2} v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2 u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u v)⟩ \\  & =⟨2,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2 u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u v)⟩ \\  & =⟨0,\,1,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2 & 0 & v \\ 0 & 1 & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 1 & u\end{aligned}|,\,-|\begin{aligned}2 & v \\ 0 & u\end{aligned}|,\,|\begin{aligned}2 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨- v,\,- 2 u,\,2⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨- v,\,- 2 u,\,2⟩‖ \\  & =\sqrt{(- v)^{2}+(- 2 u)^{2}+(2)^{2}} \\  & =\sqrt{4 u^{2} + v^{2} + 4}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x y z)\,{|}_{x=2 u\,y=v\,z=u v} \\  & =3\cdot (2 u)\cdot v\cdot uv \\  & =6 u^{2} v^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,6 u^{2} v^{2} \sqrt{4 u^{2} + v^{2} + 4}\,\,\text{d}A.\end{aligned}
$$



## original replay — cancel / easy

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

- $2({u}^{2}-{v}^{2})v\sqrt{1+8{u}^{2}}$
- $2(u+v)v\sqrt{1+8{u}^{2}}$
- $2({u}^{2}+uv+{u}^{2})v\sqrt{1+8{u}^{2}}$
- $2({u}^{2}+u)v\sqrt{1+8{u}^{2}}$
- $2{u}^{2}{v}^{2}\sqrt{1+8{u}^{2}}$

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



## generated variant — cancel / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x + y + z$ 
over the parametric surface 

$$
r(u,v)=⟨u^{2},\,u - v^{2},\,v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ Assume $v\geq0.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=2 v \sqrt{8 u^{2} + 1}.$*

- $u^{2} + u$
- $2 v \left(u^{2} - u\right) \sqrt{8 u^{2} + 1}$
- $2 v \left(u^{2} + u\right) \sqrt{8 u^{2} + 1}$
- $2 u^{2} v \sqrt{8 u^{2} + 1}$
- $\left(u^{2} + u\right) \left(32 u^{2} v^{2} + 4 v^{2}\right)$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=2 v \sqrt{8 u^{2} + 1}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x + y + z)\,{|}_{x=u^{2}\,y=u - v^{2}\,z=v^{2}} \\  & =(u^{2})+((u-v^{2})+v^{2}) \\  & =u^{2} + u\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,2 v \sqrt{8 u^{2} + 1} \left(u^{2} + u\right)\,\,\text{d}A.\end{aligned}
$$



## generated variant — cancel / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x + 2 y + 2 z$ 
over the parametric surface 

$$
r(u,v)=⟨2 u^{2},\,u - v^{2},\,v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ Assume $v\geq0.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=2 v \sqrt{32 u^{2} + 1}.$*

- $2 v \left(6 u^{2} + 2 u\right) \sqrt{32 u^{2} + 1}$
- $\left(6 u^{2} + 2 u\right) \left(128 u^{2} v^{2} + 4 v^{2}\right)$
- $6 u^{2} + 2 u$
- $12 u^{2} v \sqrt{32 u^{2} + 1}$
- $2 v \left(6 u^{2} - 2 u\right) \sqrt{32 u^{2} + 1}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=2 v \sqrt{32 u^{2} + 1}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x + 2 y + 2 z)\,{|}_{x=2 u^{2}\,y=u - v^{2}\,z=v^{2}} \\  & =3\cdot (2 u^{2})+2\cdot ((u-v^{2})+v^{2}) \\  & =6 u^{2} + 2 u\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,2 v \sqrt{32 u^{2} + 1} \left(6 u^{2} + 2 u\right)\,\,\text{d}A.\end{aligned}
$$



## original replay — cubic / easy

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

- $({v}^{3}+2v)\sqrt{16{u}^{2}+4}$
- $({u}^{3}+{v}^{3})\sqrt{16{v}^{2}+4}$
- $({v}^{2}+2u)\sqrt{16{u}^{2}+4}$
- $(u+v)\sqrt{16{u}^{2}+4}$
- $({u}^{3}+2v)\sqrt{16{u}^{2}+4}$

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



## generated variant — cubic / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x y + z$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,u^{2},\,2 v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16 u^{2} + 4}.$*

- $\sqrt{16 u^{2} + 4} \left(- u^{3} + 2 v\right)$
- $2 v \sqrt{16 u^{2} + 4}$
- $u^{3} + 2 v$
- $\left(16 u^{2} + 4\right) \left(u^{3} + 2 v\right)$
- $\sqrt{16 u^{2} + 4} \left(u^{3} + 2 v\right)$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16 u^{2} + 4}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x y + z)\,{|}_{x=u\,y=u^{2}\,z=2 v} \\  & =(u)\cdot u^{2}+2v \\  & =u^{3} + 2 v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{16 u^{2} + 4} \left(u^{3} + 2 v\right)\,\,\text{d}A.\end{aligned}
$$



## generated variant — cubic / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x y + 2 z$ 
over the parametric surface 

$$
r(u,v)=⟨2 u,\,u^{2},\,2 v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16 u^{2} + 16}.$*

- $\sqrt{16 u^{2} + 16} \left(6 u^{3} + 4 v\right)$
- $\sqrt{16 u^{2} + 16} \left(6 u^{3} - 4 v\right)$
- $6 u^{3} \sqrt{16 u^{2} + 16}$
- $\left(16 u^{2} + 16\right) \left(6 u^{3} + 4 v\right)$
- $6 u^{3} + 4 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16 u^{2} + 16}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x y + 2 z)\,{|}_{x=2 u\,y=u^{2}\,z=2 v} \\  & =3\cdot (2 u)\cdot u^{2}+2\cdot 2v \\  & =6 u^{3} + 4 v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{16 u^{2} + 16} \left(6 u^{3} + 4 v\right)\,\,\text{d}A.\end{aligned}
$$



## original replay — powers / easy

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

- $\sqrt{8}\,{u}^{3}{v}^{4}$
- $\sqrt{8}\,{u}^{4}{v}^{5}$
- $\sqrt{8}\,{u}^{5}{v}^{4}$
- $\sqrt{8}\,{u}^{2}{v}^{2}$
- $\sqrt{8}\,{u}^{3}{v}^{3}$

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



## generated variant — powers / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x^{2} y^{2} z^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨u^{2},\,v,\,v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ Assume $u\geq0.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=2 \sqrt{2} u.$*

- $2 \sqrt{2} u^{4} v^{4}$
- $2 \sqrt{2} u^{5} v^{4}$
- $u^{4} v^{4}$
- $2 \sqrt{2} u^{5} v^{3}$
- $8 u^{6} v^{4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=2 \sqrt{2} u.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x^{2} y^{2} z^{2})\,{|}_{x=u^{2}\,y=v\,z=v} \\  & =(u^{2}\cdot u^{2})\cdot v^{2}\cdot v^{2} \\  & =u^{4} v^{4}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,2 \sqrt{2} u u^{4} v^{4}\,\,\text{d}A.\end{aligned}
$$



## generated variant — powers / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x^{2} y^{2} z^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨2 u^{2},\,v,\,v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ Assume $u\geq0.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=4 \sqrt{2} u.$*

- $384 u^{6} v^{4}$
- $48 \sqrt{2} u^{4} v^{4}$
- $48 \sqrt{2} u^{5} v^{4}$
- $12 u^{4} v^{4}$
- $48 \sqrt{2} u^{5} v^{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=4 \sqrt{2} u.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x^{2} y^{2} z^{2})\,{|}_{x=2 u^{2}\,y=v\,z=v} \\  & =3\cdot (2 u^{2}\cdot 2 u^{2})\cdot v^{2}\cdot v^{2} \\  & =12 u^{4} v^{4}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,4 \sqrt{2} u 12 u^{4} v^{4}\,\,\text{d}A.\end{aligned}
$$



## original replay — product / easy

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

- $({u}^{2}+3(u+v){v}^{2})\sqrt{8{v}^{2}+1}$
- $({u}^{2}-3(u+v){v}^{2})\sqrt{8{v}^{2}+1}$
- $(-{u}^{2}+3(u+v){v}^{2})\sqrt{8{v}^{2}+1}$
- $(-{u}^{2}-3({u}^{2}+v){v}^{2})\sqrt{8{v}^{2}+1}$
- $(-{u}^{2}-3(u-v){v}^{2})\sqrt{8{v}^{2}+1}$

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



## generated variant — product / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=- x^{2} + 3 y z$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,u + v,\,v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{8 v^{2} + 1}.$*

- $\left(- u^{2} + 3 v^{2} \left(u + v\right)\right) \sqrt{8 v^{2} + 1}$
- $3 v^{2} \left(u + v\right) \sqrt{8 v^{2} + 1}$
- $\left(- u^{2} + 3 v^{2} \left(u + v\right)\right) \left(8 v^{2} + 1\right)$
- $\left(u^{2} + 3 v^{2} \left(u + v\right)\right) \sqrt{8 v^{2} + 1}$
- $- u^{2} + 3 v^{2} \left(u + v\right)$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{8 v^{2} + 1}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(- x^{2} + 3 y z)\,{|}_{x=u\,y=u + v\,z=v^{2}} \\  & =-(u\cdot u)+3\cdot (u+v)\cdot v^{2} \\  & =- u^{2} + 3 v^{2} \left(u + v\right)\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\left(- u^{2} + 3 v^{2} \left(u + v\right)\right) \sqrt{8 v^{2} + 1}\,\,\text{d}A.\end{aligned}
$$



## generated variant — product / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=- 3 x^{2} + 2 y z$ 
over the parametric surface 

$$
r(u,v)=⟨2 u,\,u + v,\,v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{20 v^{2} + 4}.$*

- $- 12 u^{2} + 2 v^{2} \left(u + v\right)$
- $\left(12 u^{2} + 2 v^{2} \left(u + v\right)\right) \sqrt{20 v^{2} + 4}$
- $\left(- 12 u^{2} + 2 v^{2} \left(u + v\right)\right) \left(20 v^{2} + 4\right)$
- $\left(- 12 u^{2} + 2 v^{2} \left(u + v\right)\right) \sqrt{20 v^{2} + 4}$
- $2 v^{2} \left(u + v\right) \sqrt{20 v^{2} + 4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{20 v^{2} + 4}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(- 3 x^{2} + 2 y z)\,{|}_{x=2 u\,y=u + v\,z=v^{2}} \\  & =-3\cdot (2 u\cdot 2 u)+2\cdot (u+v)\cdot v^{2} \\  & =- 12 u^{2} + 2 v^{2} \left(u + v\right)\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\left(- 12 u^{2} + 2 v^{2} \left(u + v\right)\right) \sqrt{20 v^{2} + 4}\,\,\text{d}A.\end{aligned}
$$



## original replay — negative_plane / moderate

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

- ${u}^{2}v\sqrt{2}$
- $({u}^{2}{v}^{2}-u)\sqrt{2}$
- $(u{v}^{2}+u)\sqrt{2u}$
- $({u}^{2}{v}^{2}+2)\sqrt{2}$
- $(uv-u)\sqrt{2u}$

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



## generated variant — negative_plane / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x^{2} z^{2} + y$ 
over the parametric surface 

$$
r(u,v)=⟨- u,\,- u,\,- v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $\sqrt{2} \left(u^{2} v^{2} - u\right)$
- $\sqrt{2} \left(u^{2} v^{2} + u\right)$
- $\sqrt{2} u^{2} v^{2}$
- $u^{2} v^{2} - u$
- $2 u^{2} v^{2} - 2 u$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(- u),\,\frac{∂}{∂u}(- u),\,\frac{∂}{∂u}(- v)⟩ \\  & =⟨-1,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(- u),\,\frac{∂}{∂v}(- u),\,\frac{∂}{∂v}(- v)⟩ \\  & =⟨0,\,0,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ -1 & -1 & 0 \\ 0 & 0 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 0 & -1\end{aligned}|,\,-|\begin{aligned}-1 & 0 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}-1 & -1 \\ 0 & 0\end{aligned}|⟩ \\  & =⟨1,\,-1,\,0⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨1,\,-1,\,0⟩‖ \\  & =\sqrt{(1)^{2}+(-1)^{2}+(0)^{2}} \\  & =\sqrt{2}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x^{2} z^{2} + y)\,{|}_{x=- u\,y=- u\,z=- v} \\  & =(- u)^{2}\cdot (-v)^{2}+(-u) \\  & =u^{2} v^{2} - u\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{2} \left(u^{2} v^{2} - u\right)\,\,\text{d}A.\end{aligned}
$$



## generated variant — negative_plane / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x^{2} z^{2} + 2 y$ 
over the parametric surface 

$$
r(u,v)=⟨- 2 u,\,- u,\,- v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $\sqrt{5} \left(12 u^{2} v^{2} + 2 u\right)$
- $12 \sqrt{5} u^{2} v^{2}$
- $\sqrt{5} \left(12 u^{2} v^{2} - 2 u\right)$
- $60 u^{2} v^{2} - 10 u$
- $12 u^{2} v^{2} - 2 u$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(- 2 u),\,\frac{∂}{∂u}(- u),\,\frac{∂}{∂u}(- v)⟩ \\  & =⟨-2,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(- 2 u),\,\frac{∂}{∂v}(- u),\,\frac{∂}{∂v}(- v)⟩ \\  & =⟨0,\,0,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ -2 & -1 & 0 \\ 0 & 0 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 0 & -1\end{aligned}|,\,-|\begin{aligned}-2 & 0 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}-2 & -1 \\ 0 & 0\end{aligned}|⟩ \\  & =⟨1,\,-2,\,0⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨1,\,-2,\,0⟩‖ \\  & =\sqrt{(1)^{2}+(-2)^{2}+(0)^{2}} \\  & =\sqrt{5}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x^{2} z^{2} + 2 y)\,{|}_{x=- 2 u\,y=- u\,z=- v} \\  & =3\cdot (- 2 u)^{2}\cdot (-v)^{2}+2\cdot (-u) \\  & =12 u^{2} v^{2} - 2 u\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{5} \left(12 u^{2} v^{2} - 2 u\right)\,\,\text{d}A.\end{aligned}
$$



## original replay — fold / moderate

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

- $({u}^{2}-{v}^{2}-2u)\sqrt{8}v$
- $({u}^{2}+2v+2u)\sqrt{8}v$
- $({u}^{2}+{v}^{2}+u)\sqrt{8v}$
- $({u}^{2}-{v}^{2})\sqrt{8}u$
- $({v}^{2}-{u}^{2}-2)\sqrt{8}$

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



## generated variant — fold / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=- x - y - z$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,- u^{2} + v^{2},\,u⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ Assume $v\geq0.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $2 \sqrt{2} v \left(- u^{2} - 2 u - v^{2}\right)$
- $u^{2} - 2 u - v^{2}$
- $2 \sqrt{2} v \left(- 2 u - v^{2}\right)$
- $2 \sqrt{2} v \left(u^{2} - 2 u - v^{2}\right)$
- $8 v^{2} \left(u^{2} - 2 u - v^{2}\right)$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(- u^{2} + v^{2}),\,\frac{∂}{∂u}(u)⟩ \\  & =⟨1,\,- 2 u,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(- u^{2} + v^{2}),\,\frac{∂}{∂v}(u)⟩ \\  & =⟨0,\,2 v,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & - 2 u & 1 \\ 0 & 2 v & 0\end{aligned}| \\  & =⟨|\begin{aligned}- 2 u & 1 \\ 2 v & 0\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 0\end{aligned}|,\,|\begin{aligned}1 & - 2 u \\ 0 & 2 v\end{aligned}|⟩ \\  & =⟨- 2 v,\,0,\,2 v⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨- 2 v,\,0,\,2 v⟩‖ \\  & =\sqrt{(- 2 v)^{2}+(0)^{2}+(2 v)^{2}} \\  & =\sqrt{4 v^{2}+4 v^{2}} \\  & =2 \sqrt{2} v.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(- x - y - z)\,{|}_{x=u\,y=- u^{2} + v^{2}\,z=u} \\  & =-(u)-(v^{2}-u^{2})-u \\  & =u^{2} - 2 u - v^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,2 \sqrt{2} v \left(u^{2} - 2 u - v^{2}\right)\,\,\text{d}A.\end{aligned}
$$



## generated variant — fold / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=- 3 x - 2 y - 2 z$ 
over the parametric surface 

$$
r(u,v)=⟨2 u,\,- u^{2} + v^{2},\,u⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ Assume $v\geq0.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $2 \sqrt{5} v \left(2 u^{2} - 2 v^{2}\right)$
- $2 u^{2} - 8 u - 2 v^{2}$
- $2 \sqrt{5} v \left(2 u^{2} + 8 u - 2 v^{2}\right)$
- $20 v^{2} \left(2 u^{2} - 8 u - 2 v^{2}\right)$
- $2 \sqrt{5} v \left(2 u^{2} - 8 u - 2 v^{2}\right)$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2 u),\,\frac{∂}{∂u}(- u^{2} + v^{2}),\,\frac{∂}{∂u}(u)⟩ \\  & =⟨2,\,- 2 u,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2 u),\,\frac{∂}{∂v}(- u^{2} + v^{2}),\,\frac{∂}{∂v}(u)⟩ \\  & =⟨0,\,2 v,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2 & - 2 u & 1 \\ 0 & 2 v & 0\end{aligned}| \\  & =⟨|\begin{aligned}- 2 u & 1 \\ 2 v & 0\end{aligned}|,\,-|\begin{aligned}2 & 1 \\ 0 & 0\end{aligned}|,\,|\begin{aligned}2 & - 2 u \\ 0 & 2 v\end{aligned}|⟩ \\  & =⟨- 2 v,\,0,\,4 v⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨- 2 v,\,0,\,4 v⟩‖ \\  & =\sqrt{(- 2 v)^{2}+(0)^{2}+(4 v)^{2}} \\  & =\sqrt{4 v^{2}+16 v^{2}} \\  & =2 \sqrt{5} v.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(- 3 x - 2 y - 2 z)\,{|}_{x=2 u\,y=- u^{2} + v^{2}\,z=u} \\  & =-3\cdot (2 u)-2\cdot (v^{2}-u^{2})-2\cdot u \\  & =2 u^{2} - 8 u - 2 v^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,2 \sqrt{5} v \left(2 u^{2} - 8 u - 2 v^{2}\right)\,\,\text{d}A.\end{aligned}
$$



## original replay — mixed / moderate

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

- $(uv+{u}^{2}{v}^{2})\sqrt{4{v}^{2}+4{v}^{4}+{u}^{2}}$
- $(v-{u}^{2}{v}^{2})\sqrt{4{v}^{2}+2{v}^{4}+u}$
- $(uv+uv)\sqrt{2{v}^{2}+4{v}^{4}-{u}^{2}}$
- $(u+{u}^{2}{v}^{2})\sqrt{{v}^{2}-4{v}^{4}-{u}^{2}}$
- $(uv+u{v}^{2})\sqrt{4{v}^{2}+{v}^{2}+{v}^{2}{u}^{2}}$

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



## generated variant — mixed / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x - y^{2} z$ 
over the parametric surface 

$$
r(u,v)=⟨u v,\,- u,\,- v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $\left(u^{2} v^{2} + u v\right) \sqrt{u^{2} + 4 v^{4} + 4 v^{2}}$
- $\left(u^{2} v^{2} + u v\right) \left(u^{2} + 4 v^{4} + 4 v^{2}\right)$
- $u^{2} v^{2} + u v$
- $u^{2} v^{2} \sqrt{u^{2} + 4 v^{4} + 4 v^{2}}$
- $\left(u^{2} v^{2} - u v\right) \sqrt{u^{2} + 4 v^{4} + 4 v^{2}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u v),\,\frac{∂}{∂u}(- u),\,\frac{∂}{∂u}(- v^{2})⟩ \\  & =⟨v,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u v),\,\frac{∂}{∂v}(- u),\,\frac{∂}{∂v}(- v^{2})⟩ \\  & =⟨u,\,0,\,- 2 v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ v & -1 & 0 \\ u & 0 & - 2 v\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 0 & - 2 v\end{aligned}|,\,-|\begin{aligned}v & 0 \\ u & - 2 v\end{aligned}|,\,|\begin{aligned}v & -1 \\ u & 0\end{aligned}|⟩ \\  & =⟨2 v,\,2 v^{2},\,u⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨2 v,\,2 v^{2},\,u⟩‖ \\  & =\sqrt{(2 v)^{2}+(2 v^{2})^{2}+(u)^{2}} \\  & =\sqrt{u^{2} + 4 v^{4} + 4 v^{2}}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x - y^{2} z)\,{|}_{x=u v\,y=- u\,z=- v^{2}} \\  & =(u v)-(-u)^{2}\cdot (-v^{2}) \\  & =u^{2} v^{2} + u v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\left(u^{2} v^{2} + u v\right) \sqrt{u^{2} + 4 v^{4} + 4 v^{2}}\,\,\text{d}A.\end{aligned}
$$



## generated variant — mixed / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x - 2 y^{2} z$ 
over the parametric surface 

$$
r(u,v)=⟨2 u v,\,- u,\,- v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $\left(2 u^{2} v^{2} + 6 u v\right) \left(4 u^{2} + 16 v^{4} + 4 v^{2}\right)$
- $\left(2 u^{2} v^{2} + 6 u v\right) \sqrt{4 u^{2} + 16 v^{4} + 4 v^{2}}$
- $2 u^{2} v^{2} + 6 u v$
- $6 u v \sqrt{4 u^{2} + 16 v^{4} + 4 v^{2}}$
- $\left(- 2 u^{2} v^{2} + 6 u v\right) \sqrt{4 u^{2} + 16 v^{4} + 4 v^{2}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2 u v),\,\frac{∂}{∂u}(- u),\,\frac{∂}{∂u}(- v^{2})⟩ \\  & =⟨2 v,\,-1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2 u v),\,\frac{∂}{∂v}(- u),\,\frac{∂}{∂v}(- v^{2})⟩ \\  & =⟨2 u,\,0,\,- 2 v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2 v & -1 & 0 \\ 2 u & 0 & - 2 v\end{aligned}| \\  & =⟨|\begin{aligned}-1 & 0 \\ 0 & - 2 v\end{aligned}|,\,-|\begin{aligned}2 v & 0 \\ 2 u & - 2 v\end{aligned}|,\,|\begin{aligned}2 v & -1 \\ 2 u & 0\end{aligned}|⟩ \\  & =⟨2 v,\,4 v^{2},\,2 u⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨2 v,\,4 v^{2},\,2 u⟩‖ \\  & =\sqrt{(2 v)^{2}+(4 v^{2})^{2}+(2 u)^{2}} \\  & =\sqrt{4 u^{2} + 16 v^{4} + 4 v^{2}}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x - 2 y^{2} z)\,{|}_{x=2 u v\,y=- u\,z=- v^{2}} \\  & =3\cdot (2 u v)-2\cdot (-u)^{2}\cdot (-v^{2}) \\  & =2 u^{2} v^{2} + 6 u v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\left(2 u^{2} v^{2} + 6 u v\right) \sqrt{4 u^{2} + 16 v^{4} + 4 v^{2}}\,\,\text{d}A.\end{aligned}
$$



## original replay — plane / moderate

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

- ${v}^{2}$
- ${u}^{2}$
- $2\sqrt{2}{u}^{2}$
- $\sqrt{2}{u}^{2}$
- ${u}^{2}+{v}^{2}$

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



## generated variant — plane / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x^{2} + y^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,u,\,v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $2 \sqrt{2} u^{2}$
- $2 \sqrt{2} v^{2}$
- $\sqrt{2} \left(u^{2} + v^{2}\right)$
- $\sqrt{2} u^{2}$
- $2 u^{2}$

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
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =⟨|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|,\,-|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 1 \\ 0 & 0\end{aligned}|⟩ \\  & =⟨1,\,-1,\,0⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨1,\,-1,\,0⟩‖ \\  & =\sqrt{(1)^{2}+(-1)^{2}+(0)^{2}} \\  & =\sqrt{1+1+0} \\  & =\sqrt{2}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x^{2} + y^{2})\,{|}_{x=u\,y=u\,z=v} \\  & =(u)^{2}+u^{2} \\  & =2 u^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{2} \cdot 2 u^{2}\,\,\text{d}A.\end{aligned}
$$



## generated variant — plane / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x^{2} + 2 y^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨2 u,\,u,\,v⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $14 u^{2}$
- $12 \sqrt{5} u^{2}$
- $14 \sqrt{5} v^{2}$
- $14 \sqrt{5} u^{2}$
- $\sqrt{5} \left(12 u^{2} + 2 v^{2}\right)$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2 u),\,\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v)⟩ \\  & =⟨2,\,1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2 u),\,\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v)⟩ \\  & =⟨0,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =⟨|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|,\,-|\begin{aligned}2 & 0 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}2 & 1 \\ 0 & 0\end{aligned}|⟩ \\  & =⟨1,\,-2,\,0⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨1,\,-2,\,0⟩‖ \\  & =\sqrt{(1)^{2}+(-2)^{2}+(0)^{2}} \\  & =\sqrt{1+4+0} \\  & =\sqrt{5}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x^{2} + 2 y^{2})\,{|}_{x=2 u\,y=u\,z=v} \\  & =3\cdot (2 u)^{2}+2\cdot u^{2} \\  & =14 u^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{5} \cdot 14 u^{2}\,\,\text{d}A.\end{aligned}
$$



## original replay — cylinder / moderate

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

- $6{v}^{2}({u}^{2}+{v}^{4})\sqrt{{v}^{2}+1}$
- ${u}^{2}(-{u}^{3}+{v}^{4})\sqrt{4uv+u}$
- $3{u}^{2}(-{u}^{3}-{v}^{4})\sqrt{4{v}^{2}+1}$
- $u(-{u}^{3}-{v}^{4})\sqrt{4{v}^{3}+u}$
- $3{u}^{2}({u}^{4}-{v}^{3})\sqrt{4{u}^{2}+1}$

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



## generated variant — cylinder / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=- x - z^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨u^{3},\,v,\,v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $- u^{3} - v^{4}$
- $3 u^{2} \left(u^{3} - v^{4}\right) \sqrt{4 v^{2} + 1}$
- $3 u^{2} \left(- u^{3} - v^{4}\right) \sqrt{4 v^{2} + 1}$
- $- 3 u^{2} v^{4} \sqrt{4 v^{2} + 1}$
- $\left(- u^{3} - v^{4}\right) \left(36 u^{4} v^{2} + 9 u^{4}\right)$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u^{3}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(v^{2})⟩ \\  & =⟨3 u^{2},\,0,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u^{3}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(v^{2})⟩ \\  & =⟨0,\,1,\,2 v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 3 u^{2} & 0 & 0 \\ 0 & 1 & 2 v\end{aligned}| \\  & =⟨|\begin{aligned}0 & 0 \\ 1 & 2 v\end{aligned}|,\,-|\begin{aligned}3 u^{2} & 0 \\ 0 & 2 v\end{aligned}|,\,|\begin{aligned}3 u^{2} & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨0,\,- 6 u^{2} v,\,3 u^{2}⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨0,\,- 6 u^{2} v,\,3 u^{2}⟩‖ \\  & =\sqrt{(0)^{2}+(- 6 u^{2} v)^{2}+(3 u^{2})^{2}} \\  & =\sqrt{36 u^{4} v^{2}+9 u^{4}} \\  & =3 u^{2} \sqrt{4 v^{2} + 1}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(- x - z^{2})\,{|}_{x=u^{3}\,y=v\,z=v^{2}} \\  & =-(u^{3})-(v^{2}\cdot v^{2}) \\  & =- u^{3} - v^{4}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,3 u^{2} \sqrt{4 v^{2} + 1} \left(- u^{3} - v^{4}\right)\,\,\text{d}A.\end{aligned}
$$



## generated variant — cylinder / moderate

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=- 3 x - 2 z^{2}$ 
over the parametric surface 

$$
r(u,v)=⟨2 u^{3},\,v,\,v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $6 u^{2} \left(6 u^{3} - 2 v^{4}\right) \sqrt{4 v^{2} + 1}$
- $\left(- 6 u^{3} - 2 v^{4}\right) \left(144 u^{4} v^{2} + 36 u^{4}\right)$
- $- 12 u^{2} v^{4} \sqrt{4 v^{2} + 1}$
- $- 6 u^{3} - 2 v^{4}$
- $6 u^{2} \left(- 6 u^{3} - 2 v^{4}\right) \sqrt{4 v^{2} + 1}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2 u^{3}),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(v^{2})⟩ \\  & =⟨6 u^{2},\,0,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2 u^{3}),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(v^{2})⟩ \\  & =⟨0,\,1,\,2 v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 6 u^{2} & 0 & 0 \\ 0 & 1 & 2 v\end{aligned}| \\  & =⟨|\begin{aligned}0 & 0 \\ 1 & 2 v\end{aligned}|,\,-|\begin{aligned}6 u^{2} & 0 \\ 0 & 2 v\end{aligned}|,\,|\begin{aligned}6 u^{2} & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨0,\,- 12 u^{2} v,\,6 u^{2}⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨0,\,- 12 u^{2} v,\,6 u^{2}⟩‖ \\  & =\sqrt{(0)^{2}+(- 12 u^{2} v)^{2}+(6 u^{2})^{2}} \\  & =\sqrt{144 u^{4} v^{2}+36 u^{4}} \\  & =6 u^{2} \sqrt{4 v^{2} + 1}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(- 3 x - 2 z^{2})\,{|}_{x=2 u^{3}\,y=v\,z=v^{2}} \\  & =-3\cdot (2 u^{3})-2\cdot (v^{2}\cdot v^{2}) \\  & =- 6 u^{3} - 2 v^{4}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,6 u^{2} \sqrt{4 v^{2} + 1} \left(- 6 u^{3} - 2 v^{4}\right)\,\,\text{d}A.\end{aligned}
$$



## original replay — signed / easy

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

- $(u{v}^{2}-{v}^{2})\sqrt{1+4{v}^{2}}$
- $(-u{v}^{2}+{v}^{2})\sqrt{1+4{v}^{2}}$
- $(-u{v}^{2}+v)\sqrt{1+4{v}^{2}}$
- $(-u{v}^{2}-v)\sqrt{1+4{v}^{2}}$
- $(-uv-v)\sqrt{1+4{v}^{2}}$

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



## generated variant — signed / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x z + y$ 
over the parametric surface 

$$
r(u,v)=⟨u,\,- v,\,- v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{4 v^{2} + 1}.$*

- $\sqrt{4 v^{2} + 1} \left(- u v^{2} + v\right)$
- $- u v^{2} - v$
- $\sqrt{4 v^{2} + 1} \left(- u v^{2} - v\right)$
- $\left(4 v^{2} + 1\right) \left(- u v^{2} - v\right)$
- $- u v^{2} \sqrt{4 v^{2} + 1}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{4 v^{2} + 1}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x z + y)\,{|}_{x=u\,y=- v\,z=- v^{2}} \\  & =(u)\cdot (-v^{2})+(-v) \\  & =- u v^{2} - v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{4 v^{2} + 1} \left(- u v^{2} - v\right)\,\,\text{d}A.\end{aligned}
$$



## generated variant — signed / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x z + 2 y$ 
over the parametric surface 

$$
r(u,v)=⟨2 u,\,- v,\,- v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16 v^{2} + 4}.$*

- $\left(16 v^{2} + 4\right) \left(- 6 u v^{2} - 2 v\right)$
- $- 6 u v^{2} - 2 v$
- $\sqrt{16 v^{2} + 4} \left(- 6 u v^{2} - 2 v\right)$
- $\sqrt{16 v^{2} + 4} \left(- 6 u v^{2} + 2 v\right)$
- $- 6 u v^{2} \sqrt{16 v^{2} + 4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16 v^{2} + 4}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x z + 2 y)\,{|}_{x=2 u\,y=- v\,z=- v^{2}} \\  & =3\cdot (2 u)\cdot (-v^{2})+2\cdot (-v) \\  & =- 6 u v^{2} - 2 v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\sqrt{16 v^{2} + 4} \left(- 6 u v^{2} - 2 v\right)\,\,\text{d}A.\end{aligned}
$$



## original replay — quadratic / easy

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

- $(uv+{v}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}$
- $uv\sqrt{{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}$
- $(uv+{u}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{2}+4{u}^{4}}$
- ${v}^{2}\sqrt{{u}^{2}{v}^{2}+4{v}^{4}+4{u}^{4}}$
- $(v+{v}^{2})\sqrt{16{u}^{2}{v}^{2}+4{v}^{2}+4{u}^{4}}$

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



## generated variant — quadratic / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=x + z$ 
over the parametric surface 

$$
r(u,v)=⟨u v,\,u^{2},\,v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{4 u^{4} + 16 u^{2} v^{2} + 4 v^{4}}.$*

- $\left(u v + v^{2}\right) \left(4 u^{4} + 16 u^{2} v^{2} + 4 v^{4}\right)$
- $u v + v^{2}$
- $\left(u v - v^{2}\right) \sqrt{4 u^{4} + 16 u^{2} v^{2} + 4 v^{4}}$
- $u v \sqrt{4 u^{4} + 16 u^{2} v^{2} + 4 v^{4}}$
- $\left(u v + v^{2}\right) \sqrt{4 u^{4} + 16 u^{2} v^{2} + 4 v^{4}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{4 u^{4} + 16 u^{2} v^{2} + 4 v^{4}}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(x + z)\,{|}_{x=u v\,y=u^{2}\,z=v^{2}} \\  & =u v + v^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\left(u v + v^{2}\right) \sqrt{4 u^{4} + 16 u^{2} v^{2} + 4 v^{4}}\,\,\text{d}A.\end{aligned}
$$



## generated variant — quadratic / easy

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=3 x + 2 z$ 
over the parametric surface 

$$
r(u,v)=⟨2 u v,\,u^{2},\,v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

*Hint: You can use the fact that $‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16 u^{4} + 16 u^{2} v^{2} + 16 v^{4}}.$*

- $\left(6 u v + 2 v^{2}\right) \sqrt{16 u^{4} + 16 u^{2} v^{2} + 16 v^{4}}$
- $6 u v \sqrt{16 u^{4} + 16 u^{2} v^{2} + 16 v^{4}}$
- $\left(6 u v + 2 v^{2}\right) \left(16 u^{4} + 16 u^{2} v^{2} + 16 v^{4}\right)$
- $6 u v + 2 v^{2}$
- $\left(6 u v - 2 v^{2}\right) \sqrt{16 u^{4} + 16 u^{2} v^{2} + 16 v^{4}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

Notice that we are told that the norm of the fundamental vector product for our surface is

$$
‖{r}_{u}^{′}\times {r}_{v}^{′}‖=\sqrt{16 u^{4} + 16 u^{2} v^{2} + 16 v^{4}}.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(3 x + 2 z)\,{|}_{x=2 u v\,y=u^{2}\,z=v^{2}} \\  & =6 u v + 2 v^{2}\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\left(6 u v + 2 v^{2}\right) \sqrt{16 u^{4} + 16 u^{2} v^{2} + 16 v^{4}}\,\,\text{d}A.\end{aligned}
$$



## authored hard variant — mixed_hard / hard

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=2 x - 3 y^{2} z$ 
over the parametric surface 

$$
r(u,v)=⟨u v,\,- 2 u,\,u - 2 v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $\left(24 u^{2} v^{2} + 2 u v\right) \sqrt{5 u^{2} + 8 u v^{2} + 16 v^{4} + 64 v^{2}}$
- $- 12 u^{3} + 24 u^{2} v^{2} + 2 u v$
- $\left(- 12 u^{3} + 24 u^{2} v^{2} + 2 u v\right) \left(5 u^{2} + 8 u v^{2} + 16 v^{4} + 64 v^{2}\right)$
- $\left(- 12 u^{3} + 24 u^{2} v^{2} + 2 u v\right) \sqrt{5 u^{2} + 8 u v^{2} + 16 v^{4} + 64 v^{2}}$
- $\left(12 u^{3} + 24 u^{2} v^{2} + 2 u v\right) \sqrt{5 u^{2} + 8 u v^{2} + 16 v^{4} + 64 v^{2}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u v),\,\frac{∂}{∂u}(- 2 u),\,\frac{∂}{∂u}(u - 2 v^{2})⟩ \\  & =⟨v,\,-2,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u v),\,\frac{∂}{∂v}(- 2 u),\,\frac{∂}{∂v}(u - 2 v^{2})⟩ \\  & =⟨u,\,0,\,- 4 v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ v & -2 & 1 \\ u & 0 & - 4 v\end{aligned}| \\  & =⟨|\begin{aligned}-2 & 1 \\ 0 & - 4 v\end{aligned}|,\,-|\begin{aligned}v & 1 \\ u & - 4 v\end{aligned}|,\,|\begin{aligned}v & -2 \\ u & 0\end{aligned}|⟩ \\  & =⟨8 v,\,u + 4 v^{2},\,2 u⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨8 v,\,u + 4 v^{2},\,2 u⟩‖ \\  & =\sqrt{(8 v)^{2}+(u + 4 v^{2})^{2}+(2 u)^{2}} \\  & =\sqrt{5 u^{2} + 8 u v^{2} + 16 v^{4} + 64 v^{2}}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(2 x - 3 y^{2} z)\,{|}_{x=u v\,y=- 2 u\,z=u - 2 v^{2}} \\  & =2 u v-3\cdot (- 2 u)^{2}\cdot (u - 2 v^{2}) \\  & =- 12 u^{3} + 24 u^{2} v^{2} + 2 u v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\left(- 12 u^{3} + 24 u^{2} v^{2} + 2 u v\right) \sqrt{5 u^{2} + 8 u v^{2} + 16 v^{4} + 64 v^{2}}\,\,\text{d}A.\end{aligned}
$$



## authored hard variant — mixed_hard / hard

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

Consider the surface integral of the function 
$f(x,y,z)=2 x - 3 y^{2} z$ 
over the parametric surface 

$$
r(u,v)=⟨2 u v,\,- 2 u,\,2 u - 2 v^{2}⟩
$$

for $(u,v)\in D⊆{R}^{2}.$ What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.

- $\left(24 u^{3} + 24 u^{2} v^{2} + 4 u v\right) \sqrt{32 u^{2} + 64 u v^{2} + 64 v^{4} + 64 v^{2}}$
- $\left(24 u^{2} v^{2} + 4 u v\right) \sqrt{32 u^{2} + 64 u v^{2} + 64 v^{4} + 64 v^{2}}$
- $- 24 u^{3} + 24 u^{2} v^{2} + 4 u v$
- $\left(- 24 u^{3} + 24 u^{2} v^{2} + 4 u v\right) \left(32 u^{2} + 64 u v^{2} + 64 v^{4} + 64 v^{2}\right)$
- $\left(- 24 u^{3} + 24 u^{2} v^{2} + 4 u v\right) \sqrt{32 u^{2} + 64 u v^{2} + 64 v^{4} + 64 v^{2}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface integral of a scalar function $f$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2 u v),\,\frac{∂}{∂u}(- 2 u),\,\frac{∂}{∂u}(2 u - 2 v^{2})⟩ \\  & =⟨2 v,\,-2,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2 u v),\,\frac{∂}{∂v}(- 2 u),\,\frac{∂}{∂v}(2 u - 2 v^{2})⟩ \\  & =⟨2 u,\,0,\,- 4 v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2 v & -2 & 2 \\ 2 u & 0 & - 4 v\end{aligned}| \\  & =⟨|\begin{aligned}-2 & 2 \\ 0 & - 4 v\end{aligned}|,\,-|\begin{aligned}2 v & 2 \\ 2 u & - 4 v\end{aligned}|,\,|\begin{aligned}2 v & -2 \\ 2 u & 0\end{aligned}|⟩ \\  & =⟨8 v,\,4 u + 8 v^{2},\,4 u⟩\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨8 v,\,4 u + 8 v^{2},\,4 u⟩‖ \\  & =\sqrt{(8 v)^{2}+(4 u + 8 v^{2})^{2}+(4 u)^{2}} \\  & =\sqrt{32 u^{2} + 64 u v^{2} + 64 v^{4} + 64 v^{2}}.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$

$$
\begin{aligned}f(r(u,v)) & =(2 x - 3 y^{2} z)\,{|}_{x=2 u v\,y=- 2 u\,z=2 u - 2 v^{2}} \\  & =4 u v-3\cdot (- 2 u)^{2}\cdot (2 u - 2 v^{2}) \\  & =- 24 u^{3} + 24 u^{2} v^{2} + 4 u v\end{aligned}
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\,\left(- 24 u^{3} + 24 u^{2} v^{2} + 4 u v\right) \sqrt{32 u^{2} + 64 u v^{2} + 64 v^{4} + 64 v^{2}}\,\,\text{d}A.\end{aligned}
$$
