# Four-stage template extraction

## 1. Specific captured questions

Each entry below preserves the complete derivative and source bank expressions. Heights/coordinates are exact; radicals have perfect-square evaluations, logarithms evaluate at 1/e, exponentials cancel or evaluate at zero, and trigonometric arguments are familiar exact angles. No calculus rule must be derived: partial derivatives are supplied.

### q-36219 / 491a90b9-f33c-5937-8491-8e8447d7cf82

Captured difficulty: **moderate**. Point: `['1', '2', '4']`. Fixed plane: `x`. Supplied derivative: `\frac{3x+y}{\sqrt{6xy+{y}^{2}}}`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=1.$ Given that the point $P(1,2,4)$ lies on $C$, and that ${f}_{y}=\frac{3x+y}{\sqrt{6xy+{y}^{2}}}$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
{f}_{y}(1,2) & =\frac{3(1)+(2)}{\sqrt{6(1)(2)+(2)^{2}}} \\  & =\frac{5}{\sqrt{16}} \\  & =\frac{5}{4}
```

```tex
z-z{|}_{(1,2)} & =\frac{∂z}{∂y}{|}_{(1,2)}(y-2) \\ z-4 & =\frac{5}{4}(y-2) \\ z & =\frac{5}{4}y+\frac{3}{2}
```

```tex
x=1 \\ z=\frac{5}{4}y+\frac{3}{2}
```

Field 0: `36f4a259-af06-543c-939e-9833986d33ba`, key `selection`, radio, captured correct present.

- `{\begin{aligned}x=1 \\ z=\frac{4}{5}y-\frac{3}{2}\end{aligned}`
- `{\begin{aligned}x=1 \\ z=\frac{5}{4}y+\frac{3}{2}\end{aligned}` — captured correct
- `{\begin{aligned}x=1 \\ z=-\frac{5}{4}y+\frac{2}{3}\end{aligned}`
- `{\begin{aligned}x=2 \\ z=-\frac{5}{4}y+\frac{3}{2}\end{aligned}`
- `{\begin{aligned}x=1 \\ z=\frac{5}{2}y-\frac{3}{2}\end{aligned}`

### q-36369 / faf15e19-a012-50bb-842f-791131393cd4

Captured difficulty: **moderate**. Point: `['1', '1', '0']`. Fixed plane: `y`. Supplied derivative: `3x+6x\operatorname{ln}⁡(xy)`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=1.$ Given that the point $P(1,1,0)$ lies on $C$, and that ${f}_{x}=3x+6x\operatorname{ln}⁡(xy)$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
\frac{∂z}{∂x}{|}_{(1,1)} & =3(1)+6(1)\operatorname{ln}⁡(1\cdot 1) \\  & =3+6\operatorname{ln}⁡1 \\  & =3
```

```tex
z-z{|}_{(1,1)} & =\frac{∂z}{∂x}{|}_{(1,1)}(x-1) \\ z-0 & =3(x-1) \\ z & =3x-3
```

```tex
y=1 \\ z=3x-3
```

Field 0: `c9c1faf1-2d7b-5e78-a408-90a8cb93ac6e`, key `selection`, radio, **no captured correct designation**.

- `{y = 1,; z = 4x - 4`
- `{y = 1; z = 3x`
- `{y = 1; z = 2x - 2`
- `{y = 1; z = 2 - 2x`
- `{y = 1; z = 3x - 3`
Field 1: `ec17033d-7e32-53b3-b00f-f4c5e370a468`, key `selection`, radio, captured correct present.

- `{\begin{aligned}y=1 \\ z=2-2x\end{aligned}`
- `{\begin{aligned}y=1, \\ z=4x-4\end{aligned}`
- `{\begin{aligned}y=1 \\ z=3x\end{aligned}`
- `{\begin{aligned}y=1 \\ z=3x-3\end{aligned}` — captured correct
- `{\begin{aligned}y=1 \\ z=2x-2\end{aligned}`

### q-132585 / 484f8b36-97b4-5e4f-a875-d05f61c48bf6

Captured difficulty: **moderate**. Point: `['4', '-2', '5']`. Fixed plane: `y`. Supplied derivative: `y\sqrt{x}`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=-2.$ Given that the point $P(4,-2,5)$ lies on $C$, and that ${f}_{x}=y\sqrt{x}$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
\frac{∂z}{∂x}{|}_{(4,-2)} & =(-2)\sqrt{4} \\  & =-2(2) \\  & =-4
```

```tex
z-z{|}_{(4,-2)} & =\frac{∂z}{∂x}{|}_{(4,-2)}(x-4) \\ z-5 & =-4(x-4) \\ z & =-4x+21
```

```tex
y=-2 \\ z=-4x+21
```

Field 0: `49d228b2-8aea-57a5-b2ca-483e7c7b3e29`, key `selection`, radio, captured correct present.

- `{\begin{aligned}y=-2 \\ z=-4x+9\end{aligned}`
- `{\begin{aligned}y=-2 \\ z=-4x+21\end{aligned}` — captured correct
- `{\begin{aligned}y=-2 \\ z=2x+9\end{aligned}`
- `{\begin{aligned}y=-2 \\ z=-2x+15\end{aligned}`
- `{\begin{aligned}y=-2 \\ z=2x+21\end{aligned}`

### q-132587 / 1c434702-618c-5a71-8a4a-aadc6bd7fee6

Captured difficulty: **moderate**. Point: `['1', '2', '1']`. Fixed plane: `y`. Supplied derivative: `2xy+2`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=2.$ Given that the point $P(1,2,1)$ lies on $C$, and that ${f}_{x}=2xy+2$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
\frac{∂z}{∂x}{|}_{(1,2)} & =2(1)(2)+2 \\  & =4+2 \\  & =6
```

```tex
z-z{|}_{(1,2)} & =\frac{∂z}{∂x}{|}_{(1,2)}(x-1) \\ z-1 & =6(x-1) \\ z & =6x-5
```

```tex
y=2 \\ z=6x-5
```

Field 0: `edc73d7a-8739-5705-bbef-4b94db05673c`, key `selection`, radio, captured correct present.

- `{\begin{aligned}y=2 \\ z=6x-5\end{aligned}` — captured correct
- `{\begin{aligned}y=2 \\ z=3x-2\end{aligned}`
- `{\begin{aligned}y=2 \\ z=6x+3\end{aligned}`
- `{\begin{aligned}y=2 \\ z=3x-5\end{aligned}`
- `{\begin{aligned}y=2 \\ z=4x+3\end{aligned}`

### q-132589 / 5c5dd738-1c94-548e-aa53-3b5d32dc4abc

Captured difficulty: **moderate**. Point: `['e', '2', '3']`. Fixed plane: `x`. Supplied derivative: `2\operatorname{ln}⁡x-\frac{{e}^{y}}{{x}^{2}}`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=e.$ Given that the point $P(e,2,3)$ lies on $C$, and that ${f}_{y}=2\operatorname{ln}⁡x-\frac{{e}^{y}}{{x}^{2}}$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
{f}_{y}(e,2) & =2\operatorname{ln}⁡e-\frac{{e}^{2}}{{e}^{2}} \\  & =2-1 \\  & =1
```

```tex
z-z{|}_{(e,2)} & =\frac{∂z}{∂y}{|}_{(e,2)}(y-2) \\ z-3 & =1(y-2) \\ z & =y+1
```

```tex
x=e \\ z=y+1
```

Field 0: `2ab8e018-d349-5c74-b2e8-1930a7b5eded`, key `selection`, radio, captured correct present.

- `\{\begin{aligned}x=e \\ z=2y-3\end{aligned}`
- `\{\begin{aligned}x=e \\ z=y+3\end{aligned}`
- `\{\begin{aligned}x=e \\ z=2y-1\end{aligned}`
- `\{\begin{aligned}x=e \\ z=y-2\end{aligned}`
- `\{\begin{aligned}x=e \\ z=y+1\end{aligned}` — captured correct

### q-132590 / 90718d28-70a4-5587-a36e-fa57ec8d26d4

Captured difficulty: **moderate**. Point: `['-\\frac{\\pi }{2}', '2', '2\\pi ']`. Fixed plane: `y`. Supplied derivative: `\operatorname{sin}⁡x+\frac{xy}{\pi }`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=2.$ Given that the point $P(-\frac{\pi }{2},2,2\pi )$ lies on $C$, and that ${f}_{x}=\operatorname{sin}⁡x+\frac{xy}{\pi }$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
\frac{∂z}{∂x}{|}_{(-\pi /2,2)} & =\operatorname{sin}⁡(-\frac{\pi }{2})+\frac{(-\frac{\pi }{2})(2)}{\pi } \\  & =-1-1 \\  & =-2
```

```tex
z-z{|}_{(-\pi /2,2)} & =\frac{∂z}{∂x}{|}_{(-\pi /2,2)}(x-(-\frac{\pi }{2})) \\ z-2\pi  & =-2(x+\frac{\pi }{2}) \\ z & =-2x+\pi 
```

```tex
y=2 \\ z=-2x+\pi 
```

Field 0: `2a7709cb-f264-5087-8141-9df67bddfa9e`, key `selection`, radio, captured correct present.

- `{\begin{aligned}y=2 \\ z=x+2\pi \end{aligned}`
- `{\begin{aligned}y=2 \\ z=2x-2\pi \end{aligned}`
- `{\begin{aligned}y=2 \\ z=-2x+\pi \end{aligned}` — captured correct
- `{\begin{aligned}y=2 \\ z=x-\pi \end{aligned}`
- `{\begin{aligned}y=2 \\ z=-2x-\frac{\pi }{2}\end{aligned}`

### q-132593 / 22a41e65-3d40-52de-a0eb-a4c7353c0c15

Captured difficulty: **moderate**. Point: `['2', '\\frac{\\pi }{4}', '0']`. Fixed plane: `x`. Supplied derivative: `4\operatorname{sin}⁡(xy)`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=2.$ Given that the point $P(2,\frac{\pi }{4},0)$ lies on $C$, and that ${f}_{y}=4\operatorname{sin}⁡(xy)$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
{f}_{y}(2,\frac{\pi }{4}) & =4\cdot \operatorname{sin}⁡(2\cdot \frac{\pi }{4}) \\  & =4\operatorname{sin}⁡(\frac{\pi }{2}) \\  & =4\cdot 1 \\  & =4
```

```tex
z-z{|}_{(2,\pi /4)} & =\frac{∂z}{∂y}{|}_{(2,\pi /4)}(y-\frac{\pi }{4}) \\ z-0 & =4(y-\frac{\pi }{4}) \\ z & =4y-\pi 
```

```tex
x=2 \\ z=4y-\pi 
```

Field 0: `f4e7d076-c660-5037-a4ff-af8a315c239c`, key `selection`, radio, captured correct present.

- `{\begin{aligned}x=2 \\ z=4y-\pi \end{aligned}` — captured correct
- `{\begin{aligned}x=2 \\ z=2y+\pi \end{aligned}`
- `{\begin{aligned}x=2 \\ z=2y-\frac{\pi }{2}\end{aligned}`
- `{\begin{aligned}x=2 \\ z=4y-\frac{\pi }{2}\end{aligned}`
- `{\begin{aligned}x=2 \\ z=4y\end{aligned}`

### q-132595 / ac300975-45c9-5a2c-a8b5-5d2addf48a83

Captured difficulty: **moderate**. Point: `['\\sqrt{2}', '2', '\\frac{1}{2}']`. Fixed plane: `x`. Supplied derivative: `-\frac{2{x}^{2}+y}{{y}^{3}}`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=\sqrt{2}.$ Given that the point $P(\sqrt{2},2,\frac{1}{2})$ lies on $C$, and that ${f}_{y}=-\frac{2{x}^{2}+y}{{y}^{3}}$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
{f}_{y}(\sqrt{2},2) & =-\frac{2(\sqrt{2})^{2}+2}{{2}^{3}} \\  & =-\frac{4+2}{8} \\  & =-\frac{3}{4}
```

```tex
z-z{|}_{(\sqrt{2},2)} & =\frac{∂z}{∂y}{|}_{(\sqrt{2},2)}(y-2) \\ z-\frac{1}{2} & =-\frac{3}{4}(y-2) \\ z & =-\frac{3}{4}y+2
```

```tex
x=\sqrt{2} \\ z=-\frac{3}{4}y+2
```

Field 0: `92a71cca-98d2-5245-a4d1-fd31406052e5`, key `selection`, radio, captured correct present.

- `{\begin{aligned}x=\sqrt{2} \\ z=-\frac{3}{2}y+1\end{aligned}`
- `{\begin{aligned}x=\sqrt{2} \\ z=\frac{3}{2}y-1\end{aligned}`
- `{\begin{aligned}x=\sqrt{2} \\ z=-\frac{1}{4}y-2\end{aligned}`
- `{\begin{aligned}x=\sqrt{2} \\ z=\frac{1}{2}y+2\end{aligned}`
- `{\begin{aligned}x=\sqrt{2} \\ z=-\frac{3}{4}y+2\end{aligned}` — captured correct

### q-36301 / daecb367-4754-591f-93db-eaa083b20ffe

Captured difficulty: **moderate**. Point: `['-2', '0', '8']`. Fixed plane: `x`. Supplied derivative: `x\operatorname{cos}⁡y+4y+x`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=-2.$ Given that the point $P(-2,0,8)$ lies on $C$, and that ${f}_{y}=x\operatorname{cos}⁡y+4y+x$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
\frac{∂z}{∂y}{|}_{(-2,0)} & =(-2)\operatorname{cos}⁡0+4(0)+(-2) \\  & =-2-2 \\  & =-4
```

```tex
z-z{|}_{(-2,0)} & =\frac{∂z}{∂y}{|}_{(-2,0)}(y-0) \\ z-8 & =-4(y-0) \\ z & =-4y+8
```

```tex
x=-2 \\ z=-4y+8
```

Field 0: `57b4da25-e31a-52b9-9b49-54d616020d35`, key `selection`, radio, captured correct present.

- `{\begin{aligned}x=-2 \\ z=4y+8\end{aligned}`
- `{\begin{aligned}x=-2 \\ z=-4x\end{aligned}`
- `{\begin{aligned}x=-2 \\ z=-4y+8\end{aligned}` — captured correct
- `{\begin{aligned}x=-2 \\ z=4x+8\end{aligned}`
- `{\begin{aligned}x=-2 \\ z=4y-8\end{aligned}`

### q-36441 / 12d0b28e-9c11-5054-bcb2-feb86bd6fc4d

Captured difficulty: **moderate**. Point: `['0.5', '2', '4']`. Fixed plane: `x`. Supplied derivative: `y+2y\operatorname{ln}⁡(xy)+\frac{1}{x}`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=0.5.$ Given that the point $P(0.5,2,4)$ lies on $C$, and that ${f}_{y}=y+2y\operatorname{ln}⁡(xy)+\frac{1}{x}$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
\frac{∂z}{∂y}{|}_{(0.5,2)} & =2+2(2)\operatorname{ln}⁡((0.5)(2))+\frac{1}{0.5} \\  & =2+4\operatorname{ln}⁡1+2 \\  & =4
```

```tex
z-z{|}_{(0.5,2)} & =\frac{∂z}{∂y}{|}_{(0.5,2)}(y-2) \\ z-4 & =4(y-2) \\ z & =4y-4
```

```tex
x=0.5 \\ z=4y-4
```

Field 0: `41b9822b-8388-5077-b4c1-9ebc7d355fb6`, key `selection`, radio, captured correct present.

- `{\begin{aligned}x=0.5 \\ z=4x+2\end{aligned}`
- `{\begin{aligned}y=2 \\ z=4x+2\end{aligned}`
- `{\begin{aligned}x=0.5 \\ z=4y-12\end{aligned}`
- `{\begin{aligned}x=0.5 \\ z=-4y+12\end{aligned}`
- `{\begin{aligned}x=0.5 \\ z=4y-4\end{aligned}` — captured correct

### q-71209 / 3868b943-72a6-5a73-9952-d94521bce0ce

Captured difficulty: **moderate**. Point: `['-2', '2', '1']`. Fixed plane: `x`. Supplied derivative: `{x}^{2}y+2x-y`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=-2.$ Given that the point $P(-2,2,1)$ lies on $C$, and that ${f}_{y}={x}^{2}y+2x-y$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
{f}_{y}(-2,2) & =(-2)^{2}(2)+2(-2)-(2) \\  & =8-4-2 \\  & =2
```

```tex
z-z{|}_{(-2,2)} & =\frac{∂z}{∂y}{|}_{(-2,2)}(y-2) \\ z-1 & =2(y-2) \\ z & =2y-3
```

```tex
x=-2 \\ z=2y-3
```

Field 0: `335b522d-b8a5-5ac7-8b9d-2985076f5c17`, key `selection`, radio, captured correct present.

- `\{\begin{aligned}x=-2 \\ z=6y-3\end{aligned}`
- `\{\begin{aligned}x=-2 \\ z=4y-5\end{aligned}`
- `\{\begin{aligned}x=-2 \\ z=2y-3\end{aligned}` — captured correct
- `\{\begin{aligned}x=-2 \\ z=4y-3\end{aligned}`
- `\{\begin{aligned}x=-2 \\ z=2y-5\end{aligned}`

### q-71218 / ceda561f-8269-5197-b05a-efc41af9a9a2

Captured difficulty: **moderate**. Point: `['0', '1', '2']`. Fixed plane: `y`. Supplied derivative: `{x}^{2}+{y}^{2}-\operatorname{ln}⁡(x+y)`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=1.$ Given that the point $P(0,1,2)$ lies on $C$, and that ${f}_{x}={x}^{2}+{y}^{2}-\operatorname{ln}⁡(x+y)$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
\frac{∂z}{∂x}{|}_{(0,1)} & =(0)^{2}+(1)^{2}-\operatorname{ln}⁡(0+1) \\  & =1-\operatorname{ln}⁡1 \\  & =1-0 \\  & =1
```

```tex
z-z{|}_{(0,1)} & =\frac{∂z}{∂x}{|}_{(0,1)}(x-0) \\ z-2 & =1(x) \\ z & =x+2
```

```tex
y=1 \\ z=x+2
```

Field 0: `67c2ebb0-7f04-5390-9b3f-6c5b9ac02ee1`, key `selection`, radio, captured correct present.

- `{\begin{aligned}y=1 \\ z=x-2\end{aligned}`
- `{\begin{aligned}y=1 \\ z=x+2\end{aligned}` — captured correct
- `{\begin{aligned}y=1 \\ z=2\end{aligned}`
- `{\begin{aligned}y=1 \\ z=-x+2\end{aligned}`
- `{\begin{aligned}y=1 \\ z=-2\end{aligned}`

### q-36372 / 376329be-a379-553e-b714-516f831f127f

Captured difficulty: **moderate**. Point: `['2', '0', '4']`. Fixed plane: `y`. Supplied derivative: `{e}^{y}+2x\operatorname{cos}⁡y`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=0.$ Given that the point $P(2,0,4)$ lies on $C$, and that ${f}_{x}={e}^{y}+2x\operatorname{cos}⁡y$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
{f}_{x}(2,0) & ={e}^{(0)}+2(2)\operatorname{cos}⁡(0) \\  & =1+4 \\  & =5
```

```tex
z-z{|}_{(2,0)} & =\frac{∂z}{∂x}{|}_{(2,0)}(x-2) \\ z-4 & =5(x-2) \\ z & =5x-6
```

```tex
y=0 \\ z=5x-6
```

Field 0: `2712fe89-2404-5ec9-a1bd-af26bb9d16b3`, key `selection`, radio, captured correct present.

- `{\begin{aligned}y=0 \\ z=5x-14\end{aligned}`
- `{\begin{aligned}y=0 \\ z=5x-6\end{aligned}` — captured correct
- `{\begin{aligned}x=2 \\ z=5y+4\end{aligned}`
- `{\begin{aligned}y=0 \\ z=5x+6\end{aligned}`
- `{\begin{aligned}x=2 \\ z=-5x-6\end{aligned}`

### q-71216 / 05b78370-0b37-5800-aa28-6b6b17964b90

Captured difficulty: **moderate**. Point: `['1', '0', '-1']`. Fixed plane: `x`. Supplied derivative: `x{e}^{xy}-2\operatorname{cos}⁡y`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=1.$ Given that the point $P(1,0,-1)$ lies on $C$, and that ${f}_{y}=x{e}^{xy}-2\operatorname{cos}⁡y$, find the equations of the tangent line to $C$ at $P.$

Operative source blocks (full sequence):

```tex
{f}_{y}(1,0) & =1\cdot {e}^{1\cdot 0}-2\operatorname{cos}⁡0 \\  & =1\cdot 1-2\cdot 1 \\  & =-1
```

```tex
z-z{|}_{(1,0)} & =\frac{∂z}{∂y}{|}_{(1,0)}(y-0) \\ z-(-1) & =(-1)y \\ z & =-y-1
```

```tex
x=1 \\ z=-y-1
```

Field 0: `e94262ee-f4dd-5ac5-a015-9c5cf4798aa0`, key `selection`, radio, captured correct present.

- `{\begin{aligned}x=1 \\ z=-y+1\end{aligned}`
- `{\begin{aligned}x=1 \\ z=-2y-1\end{aligned}`
- `{\begin{aligned}x=1 \\ z=y-1\end{aligned}`
- `{\begin{aligned}x=1 \\ z=-2y+1\end{aligned}`
- `{\begin{aligned}x=1 \\ z=-y-1\end{aligned}` — captured correct

## 2. Generalized pattern

Select the partial derivative along the changing coordinate, evaluate it at the printed xy point, insert the printed altitude and slope into point-slope form, collect the z equation, and preserve the fixed-coordinate plane. Answers are the full intersection of two planes, rather than separately equivalent equation sides.

## 3. Components and full banks

Source point coordinates and supplied derivative are complete components. Each derivative evaluation block is retained as ordered source rows, including omission of zero terms and distinct trigonometric/logarithmic evaluation steps. The point-slope formal row, substituted row, collected row and final two-plane block are separate components. Every occurrence of the full P coordinate in prose is a slot. Shared sentences remain verbatim in moderate generation.

For every source option above, the public raw recipe is the complete affine vertical transformation of its printed relation: preserve the first plane and transform z=R(x,y) into z=c(R(x,y)−h0)+h, where h0 is the source altitude, c the supplied derivative scale, and h the new altitude. At c=1,h=h0, the source spelling is retained as a complete component slot. This maps every choice, including options using the held coordinate in the second plane. Its distractor interpretation is **opaque**: this geometric transformation preserves the evidence without claiming to recover historical error intent. Each full captured bank remains together; q-36369 retains both versions and the missing legacy ref.

Normal whole operation banks are separately authored. For changing coordinate u at u0, held coordinate v=v0, slope m and altitude h: correct z=m(u−u0)+h; negate slope z=−m(u−u0)+h; add point offset z=m(u+u0)+h; omit altitude z=m(u−u0); swap held coordinate u=u0 with z=m(v−v0)+h. When u0=0, the eligible whole profile replaces point-offset addition with altitude sign reversal z=mu−h; the five entire lines are checked for uniqueness before accepting an instance. It never constructs a bank from first-valid pooled errors. No diagnoses enter learner content.

## 4. Reusable masks and constraints

Moderate preserves its original xy coordinates, parameterizes complete altitude P slots and full point-slope components, and scales the supplied derivative plus **each** operative derivative-evaluation row. Non-final rows show c(original source RHS), retaining inner source structure; final row is collected. With c=1 the source derivative block remains unchanged. This provides 14 original source families with signed scale ±1…±3 and altitude integer −12…−1/1…12 in normal sampling (2016 nominal combinations before whole-bank rejection), while explicit normal half-integers and small pi multiples remain supported. Observed coordinates preserve square roots, familiar trig/logarithmic/exponential evaluations and rational arithmetic.

Easy and hard masks and exact guards are documented in classification.md, README.md and separate script sections. Easy uses a single supplied linear partial kx; hard uses the canonical y cos(xy)+cos(y), exact familiar pi evaluation, symbolic slope and symbolic intercept. Neither asks for tangent vectors, normals, cross products or unsupplied differentiation.

Source repairs are presentation-only in normal output (escaped system braces), plus consolidation of q-36369 duplicate radio assessments. Raw exact versus normalized normal fidelity are reported separately. Missing legacy correct designation is never counted as a matched observed designation.
