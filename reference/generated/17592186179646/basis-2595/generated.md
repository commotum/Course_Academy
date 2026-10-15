![](images/e4/e46488d991bf461eacc51ecfcd490497bf13fcdf2b7ff998b54fdc501caf40ab.png)

Consider the vector field $F=3\,i$ and a square $C$ with side length $10$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$

- $30$
- $-30$
- $0$
- $-10$
- $10$

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$ In this case, we have

$$
{∮}_{C}F\cdot n\,\text{d}s={\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s+{\int }_{{C}_{2}}F\cdot {n}_{2}\,\text{d}s+{\int }_{{C}_{3}}F\cdot {n}_{3}\,\text{d}s+{\int }_{{C}_{4}}F\cdot {n}_{4}\,\text{d}s,
$$

where the sides ${C}_{i}$ and unit vectors ${n}_{i}$ are shown below.

![](images/a2/a2964076c4126d6277625260c45479d1a4fb2028f7e75223a0f5942b15f5a2d2.png)

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
