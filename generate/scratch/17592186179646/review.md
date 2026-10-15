# Source and changed-parameter review

## Source replay q-126881

![](images/19/19fca0188077e56d6b56048d1cd48ea840922cafe7873aaa02937c8c2845e998.png)

Consider the vector field $F=2\,j$ and a square $C$ with side length $4$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $4$
- $8$
- $-4$
- $-8$
- $0$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/3b/3bd953b7fb02b90a55a29bea6f58ff9bd8bab77d62b1df1c547ca899656d37a3.png)

Now, since the vector field $F=2\,j$ is parallel to ${C}_{1}$ and ${C}_{3},$ there is zero net flow through these two sides. Therefore,

$$
{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s={\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s=0.
$$

So, our expression for the flux reduces to

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s.
$$

Now, since the vector field is uniform, the net outflow through ${C}_{2}$ will cancel with the net inflow through ${C}_{4}.$ That is

$$
{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s=-{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s\,⟹\,{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s=0.
$$

Therefore, we conclude that

$$
{∮}_{C}F\cdot n\,\text{d}s=0.
$$

## Changed parameters q-126881

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/1cd5169c0c5344aad44b6b63417e8026e1394ad06152aa9a52ce360a39b472dd-prompt.png)

Consider the vector field $F=4\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $10$
- $40$
- $-10$
- $-40$
- $0$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/1cd5169c0c5344aad44b6b63417e8026e1394ad06152aa9a52ce360a39b472dd-solution.png)

Now, since the vector field $F=4\,j$ is parallel to ${C}_{1}$ and ${C}_{3},$ there is zero net flow through these two sides. Therefore,

$$
{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s={\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s=0.
$$

So, our expression for the flux reduces to

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s.
$$

Now, since the vector field is uniform, the net outflow through ${C}_{2}$ will cancel with the net inflow through ${C}_{4}.$ That is

$$
{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s=-{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s\,⟹\,{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s=0.
$$

Therefore, we conclude that

$$
{∮}_{C}F\cdot n\,\text{d}s=0.
$$

## Source replay q-127199

![](images/5c/5c8aef7238da3bb5aed0fd2a458f6fd9bcd42884bbd350616e58e7a25b1f0fe2.png)

Consider the vector field $F =-2xi - 2yj$ and a square $C$ with side length $6$ centered at $O$, as shown above. Calculate the flux of $F$ across $C$.

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $-64$
- $-128$
- $-72$
- $-36$
- $-144$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/87/878a9992405e5968a03a04d12f42aeb85bca52c07dc7081244b04011643a74bf.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(-2x\,i-2y\,j)\cdot i\,\text{d}s \\  & =-2{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=3\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-3,3].
$$

Therefore,

$$
\begin{aligned}-2{\int }_{{C}_{1}}x\,\text{d}s & =-2{\int }_{-3}^{3}3\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =-6{\int }_{-3}^{3}\text{d}t \\  & =-6(3-(-3)) \\  & =(-6)\cdot 6 \\  & =-36.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot (-36)=-144.
$$

## Changed parameters q-127199

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-prompt.png)

Consider the vector field $F=4x\,i+4y\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $\frac{3200}{9}$
- $\frac{6400}{9}$
- $400$
- $200$
- $800$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-solution.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(4x\,i+4y\,j)\cdot i\,\text{d}s \\  & =4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=5\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-5,5].
$$

Therefore,

$$
\begin{aligned}4{\int }_{{C}_{1}}x\,\text{d}s & =4{\int }_{-5}^{5}5\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =20{\int }_{-5}^{5}\text{d}t \\  & =20(5-(-5)) \\  & =20\cdot 10 \\  & =200.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 200=800.
$$

## Source replay q-126890

![](images/70/70a51bcda43cd04a56c6b87a10723258c995e8daae87689a2ae8af5f44112ead.png)

Consider the vector field $F=x\,i+y\,j$ and a square $C$ with side length $4$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $16$
- $20$
- $32$
- $4$
- $64$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/3b/3bd953b7fb02b90a55a29bea6f58ff9bd8bab77d62b1df1c547ca899656d37a3.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(x\,i+y\,j)\cdot i\,\text{d}s \\  & ={\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=2\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-2,2].
$$

Therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}x\,\text{d}s & ={\int }_{-2}^{2}2\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =2{\int }_{-2}^{2}\text{d}t \\  & =2(2-(-2)) \\  & =2\cdot 4 \\  & =8.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 8=32.
$$

## Changed parameters q-126890

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-prompt.png)

Consider the vector field $F=4x\,i+4y\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $400$
- $500$
- $800$
- $100$
- $1600$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-solution.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(4x\,i+4y\,j)\cdot i\,\text{d}s \\  & =4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=5\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-5,5].
$$

Therefore,

$$
\begin{aligned}4{\int }_{{C}_{1}}x\,\text{d}s & =4{\int }_{-5}^{5}5\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =20{\int }_{-5}^{5}\text{d}t \\  & =20(5-(-5)) \\  & =20\cdot 10 \\  & =200.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 200=800.
$$

## Source replay q-127190

![](images/ea/ea53225d28411f38006861d6c8dc46f8d3d1ea01b3bb6183954f68e7124c5682.png)

Consider the vector field $F=3\,i$ and a square $C$ with side length $2$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $2$
- $0$
- $-4$
- $4$
- $-2$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/1d/1de4c4c55784b4a84a0493a4cc65082c430cadcc39c3d808001b2fd27665e968.png)

Now, since the vector field $F=3\,i$ is parallel to ${C}_{2}$ and ${C}_{4},$ there is zero net flow through these two sides. Therefore,

$$
{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s={\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s=0.
$$

So, our expression for the flux reduces to

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s.
$$

Now, since the vector field is uniform, the net outflow through ${C}_{1}$ will cancel with the net inflow through ${C}_{3}.$ That is

$$
{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s=-{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s\,⟹\,{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s=0.
$$

Therefore, we conclude that

$$
{∮}_{C}F\cdot n\,\text{d}s=0.
$$

## Changed parameters q-127190

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/aad163af0c6d707e4350d68648d21680247466884380f7b939ad069cf7e48f5d-prompt.png)

Consider the vector field $F=4\,i$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $10$
- $0$
- $-20$
- $20$
- $-10$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/aad163af0c6d707e4350d68648d21680247466884380f7b939ad069cf7e48f5d-solution.png)

Now, since the vector field $F=4\,i$ is parallel to ${C}_{2}$ and ${C}_{4},$ there is zero net flow through these two sides. Therefore,

$$
{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s={\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s=0.
$$

So, our expression for the flux reduces to

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s.
$$

Now, since the vector field is uniform, the net outflow through ${C}_{1}$ will cancel with the net inflow through ${C}_{3}.$ That is

$$
{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s=-{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s\,⟹\,{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s=0.
$$

Therefore, we conclude that

$$
{∮}_{C}F\cdot n\,\text{d}s=0.
$$

## Source replay q-127194

![](images/8e/8e1767b9bea45e742df4953f0ec50b2d43c9622994035342307dc2be6abba8de.png)

Consider the vector field $F=-2\,i$ and a square $C$ with side length $6$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $0$
- $-6$
- $6$
- $12$
- $-12$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/87/878a9992405e5968a03a04d12f42aeb85bca52c07dc7081244b04011643a74bf.png)

Now, since the vector field $F=-2\,i$ is parallel to ${C}_{2}$ and ${C}_{4},$ there is zero net flow through these two sides. Therefore,

$$
{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s={\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s=0.
$$

So, our expression for the flux reduces to

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s.
$$

Now, since the vector field is uniform, the net inflow through ${C}_{1}$ will cancel with the net outflow through ${C}_{3}.$ That is

$$
{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s=-{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s\,⟹\,{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s=0.
$$

Therefore, we conclude that

$$
{∮}_{C}F\cdot n\,\text{d}s=0.
$$

## Changed parameters q-127194

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/aad163af0c6d707e4350d68648d21680247466884380f7b939ad069cf7e48f5d-prompt.png)

Consider the vector field $F=4\,i$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $0$
- $-10$
- $10$
- $40$
- $-40$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/aad163af0c6d707e4350d68648d21680247466884380f7b939ad069cf7e48f5d-solution.png)

Now, since the vector field $F=4\,i$ is parallel to ${C}_{2}$ and ${C}_{4},$ there is zero net flow through these two sides. Therefore,

$$
{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s={\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s=0.
$$

So, our expression for the flux reduces to

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s.
$$

Now, since the vector field is uniform, the net outflow through ${C}_{1}$ will cancel with the net inflow through ${C}_{3}.$ That is

$$
{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s=-{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s\,⟹\,{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s=0.
$$

Therefore, we conclude that

$$
{∮}_{C}F\cdot n\,\text{d}s=0.
$$

## Source replay q-127198

![](images/fd/fdb05b3fcbfcfdab8344eaaaf54584a95f20696618b412873ddeb219b7a401b3.png)

Consider the vector field $F=-x\,i-y\,j$ and a square $C$ with side length $4$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $-8$
- $-14$
- $-32$
- $-16$
- $-28$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/3b/3bd953b7fb02b90a55a29bea6f58ff9bd8bab77d62b1df1c547ca899656d37a3.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(-x\,i-y\,j)\cdot i\,\text{d}s \\  & =-{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=2\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-2,2].
$$

Therefore,

$$
\begin{aligned}-{\int }_{{C}_{1}}x\,\text{d}s & =-{\int }_{-2}^{2}2\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =-2{\int }_{-2}^{2}\text{d}t \\  & =-2(2-(-2)) \\  & =(-2)\cdot 4 \\  & =-8.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot (-8)=-32.
$$

## Changed parameters q-127198

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-prompt.png)

Consider the vector field $F=4x\,i+4y\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $200$
- $350$
- $800$
- $400$
- $700$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-solution.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(4x\,i+4y\,j)\cdot i\,\text{d}s \\  & =4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=5\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-5,5].
$$

Therefore,

$$
\begin{aligned}4{\int }_{{C}_{1}}x\,\text{d}s & =4{\int }_{-5}^{5}5\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =20{\int }_{-5}^{5}\text{d}t \\  & =20(5-(-5)) \\  & =20\cdot 10 \\  & =200.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 200=800.
$$

## Source replay q-226126

![](images/6f/6f827dac7ecaf3a659245d1178aa39a519ae3a40339c917004247f12554c871a.png)

Consider the vector field $F=2x\,i+2y\,j$ and a square $C$ with side length $8$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $128$
- $72$
- $288$
- $256$
- $64$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/0b/0b753318ebad9270c3fc8788d0e3949ffb29a800eb3f8dd6fb67cb271be68033.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(2x\,i+2y\,j)\cdot i\,\text{d}s \\  & =2{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=4\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-4,4].
$$

Therefore,

$$
\begin{aligned}2{\int }_{{C}_{1}}x\,\text{d}s & =2{\int }_{-4}^{4}4\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =8{\int }_{-4}^{4}\text{d}t \\  & =8(4-(-4)) \\  & =8\cdot 8 \\  & =64.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 64=256.
$$

## Changed parameters q-226126

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-prompt.png)

Consider the vector field $F=4x\,i+4y\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $400$
- $225$
- $900$
- $800$
- $200$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-solution.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(4x\,i+4y\,j)\cdot i\,\text{d}s \\  & =4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=5\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-5,5].
$$

Therefore,

$$
\begin{aligned}4{\int }_{{C}_{1}}x\,\text{d}s & =4{\int }_{-5}^{5}5\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =20{\int }_{-5}^{5}\text{d}t \\  & =20(5-(-5)) \\  & =20\cdot 10 \\  & =200.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 200=800.
$$

## Source replay q-226132

![](images/f4/f413fd04759cdb02118b320fea2f678712681a57f5b08e1bcb57a6843c0c80f0.png)

Consider the vector field $F=4x\,i+4y\,j$ and a square $C$ with side length $6$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $288$
- $144$
- $256$
- $360$
- $128$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/87/878a9992405e5968a03a04d12f42aeb85bca52c07dc7081244b04011643a74bf.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(4x\,i+4y\,j)\cdot i\,\text{d}s \\  & =4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=3\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-3,3].
$$

Therefore,

$$
\begin{aligned}4{\int }_{{C}_{1}}x\,\text{d}s & =4{\int }_{-3}^{3}3\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =12{\int }_{-3}^{3}\text{d}t \\  & =12(3-(-3)) \\  & =12\cdot 6 \\  & =72.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 72=288.
$$

## Changed parameters q-226132

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-prompt.png)

Consider the vector field $F=4x\,i+4y\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $800$
- $400$
- $\frac{6400}{9}$
- $1000$
- $\frac{3200}{9}$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-solution.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(4x\,i+4y\,j)\cdot i\,\text{d}s \\  & =4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=5\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-5,5].
$$

Therefore,

$$
\begin{aligned}4{\int }_{{C}_{1}}x\,\text{d}s & =4{\int }_{-5}^{5}5\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =20{\int }_{-5}^{5}\text{d}t \\  & =20(5-(-5)) \\  & =20\cdot 10 \\  & =200.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 200=800.
$$

## Source replay q-226115

![](images/57/575463a6fbe18d3f9b805e1a9c3d8e52bedd84a8db3a3c90d87381b8cb7abf74.png)

Consider the vector field $F=-4x\,i-4y\,j$ and a square $C$ with side length $2$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $-16$
- $-28$
- $-64$
- $-8$
- $-32$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/eb/ebe05a522f9f46acfed63e29927b46f41d78483b5df5e7a15a15ae5f33abd2f4.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(-4x\,i-4y\,j)\cdot i\,\text{d}s \\  & =-4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-1,1].
$$

Therefore,

$$
\begin{aligned}-4{\int }_{{C}_{1}}x\,\text{d}s & =-4{\int }_{-1}^{1}1\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =-4{\int }_{-1}^{1}\text{d}t \\  & =-4(1-(-1)) \\  & =(-4)\cdot 2 \\  & =-8.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot (-8)=-32.
$$

## Changed parameters q-226115

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-prompt.png)

Consider the vector field $F=4x\,i+4y\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $400$
- $700$
- $1600$
- $200$
- $800$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-solution.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(4x\,i+4y\,j)\cdot i\,\text{d}s \\  & =4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=5\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-5,5].
$$

Therefore,

$$
\begin{aligned}4{\int }_{{C}_{1}}x\,\text{d}s & =4{\int }_{-5}^{5}5\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =20{\int }_{-5}^{5}\text{d}t \\  & =20(5-(-5)) \\  & =20\cdot 10 \\  & =200.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 200=800.
$$

## Source replay q-226103

![](images/32/321c16127ae1999e4ec42024f35cd076930618588fe378b9ca16a4ee4eabd58a.png)

Consider the vector field $F=-0.5x\,i-0.5y\,j$ and a square $C$ with side length $8$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $-32$
- $-64$
- $-24$
- $-16$
- $-36$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/ab/abe90a592e098a4656577f3a2303669dccc126baff738397836c8f96c26b5389.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(-0.5x\,i-0.5y\,j)\cdot i\,\text{d}s \\  & =-0.5{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=4\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-4,4].
$$

Therefore,

$$
\begin{aligned}-0.5{\int }_{{C}_{1}}x\,\text{d}s & =-0.5{\int }_{-4}^{4}4\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =-2{\int }_{-4}^{4}\text{d}t \\  & =-2(4-(-4)) \\  & =(-2)\cdot 8 \\  & =-16.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot (-16)=-64.
$$

## Changed parameters q-226103

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-prompt.png)

Consider the vector field $F=4x\,i+4y\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*

- $400$
- $800$
- $300$
- $200$
- $450$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/8fb0e9562ee6678fa4554f62cdc8ad20ce470d986dbf704aa518ca8be8d995c7-solution.png)

First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(4x\,i+4y\,j)\cdot i\,\text{d}s \\  & =4{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=5\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-5,5].
$$

Therefore,

$$
\begin{aligned}4{\int }_{{C}_{1}}x\,\text{d}s & =4{\int }_{-5}^{5}5\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =20{\int }_{-5}^{5}\text{d}t \\  & =20(5-(-5)) \\  & =20\cdot 10 \\  & =200.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot 200=800.
$$

## Source replay q-127193

![](images/32/32d4722f4a1dd1cfae3fb22cde7399dcb66623e484bcd5989fd2de246a905b51.png)

Consider the vector field $F=-3\,j$ and a square $C$ with side length $4$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $-4$
- $4$
- $0$
- $-12$
- $12$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/3b/3bd953b7fb02b90a55a29bea6f58ff9bd8bab77d62b1df1c547ca899656d37a3.png)

Now, since the vector field $F=-3\,j$ is parallel to ${C}_{1}$ and ${C}_{3},$ there is zero net flow through these two sides. Therefore,

$$
{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s={\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s=0.
$$

So, our expression for the flux reduces to

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s.
$$

Now, since the vector field is uniform, the net inflow through ${C}_{2}$ will cancel with the net outflow through ${C}_{4}.$ That is

$$
{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s=-{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s\,⟹\,{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s=0.
$$

Therefore, we conclude that

$$
{∮}_{C}F\cdot n\,\text{d}s=0.
$$

## Changed parameters q-127193

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/1cd5169c0c5344aad44b6b63417e8026e1394ad06152aa9a52ce360a39b472dd-prompt.png)

Consider the vector field $F=4\,j$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $-10$
- $10$
- $0$
- $-40$
- $40$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179646/assets/1cd5169c0c5344aad44b6b63417e8026e1394ad06152aa9a52ce360a39b472dd-solution.png)

Now, since the vector field $F=4\,j$ is parallel to ${C}_{1}$ and ${C}_{3},$ there is zero net flow through these two sides. Therefore,

$$
{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s={\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s=0.
$$

So, our expression for the flux reduces to

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s.
$$

Now, since the vector field is uniform, the net outflow through ${C}_{2}$ will cancel with the net inflow through ${C}_{4}.$ That is

$$
{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s=-{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s\,⟹\,{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s=0.
$$

Therefore, we conclude that

$$
{∮}_{C}F\cdot n\,\text{d}s=0.
$$
