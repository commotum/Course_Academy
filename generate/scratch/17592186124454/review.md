# Tangent line generator review

Original raw records preserve absent difficulty/correct keys. Inferred completions retain opaque or ambiguous banks and are **evidence only**. Generated learning variants use explicitly authored safe banks. Correct native designations are marked; equivalent historical options are listed in validation, independently of their native key.

### Original raw q-36383 — unrated — observed raw

Given the function $f(x, y) = 3x^{2} + 2xy^{2} - y$, find the equation of the tangent line to the level curve that passes through the point where $(x, y) = (-1, 1)$.

- [ ] $⟨5, 4⟩ \cdot ⟨x + 1, y - 1⟩ = 0$
- [ ] $⟨5, 3⟩ \cdot ⟨x + 1, y - 1⟩ = 0$
- [ ] $⟨2,-1⟩ \cdot ⟨x + 1, y - 1⟩ = 0$
- [ ] $⟨6, 2⟩ \cdot ⟨x + 1, y - 1⟩ = 0$
- [ ] $⟨ - 4,-5⟩ \cdot ⟨x + 1, y - 1⟩ = 0$

*Original worked solution absent.*

*Original correct designation absent; the separate completion shows the inferred gradient representation.*

### Inferred completion / opaque evidence q-36383 — :question.difficulty/easy — inferred completion; opaque bank

Given the function $f(x, y) = 3x^{2} + 2xy^{2} - y$, find the equation of the tangent line to the level curve that passes through the point where $(x, y) = (-1, 1)$.

- [ ] $⟨5, 4⟩ \cdot ⟨x + 1, y - 1⟩ = 0$
- [ ] $⟨5, 3⟩ \cdot ⟨x + 1, y - 1⟩ = 0$
- [ ] $⟨2,-1⟩ \cdot ⟨x + 1, y - 1⟩ = 0$
- [ ] $⟨6, 2⟩ \cdot ⟨x + 1, y - 1⟩ = 0$
- [x] $⟨ - 4,-5⟩ \cdot ⟨x + 1, y - 1⟩ = 0$ **correct**

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-1,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x^{2} + 2 x y^{2} - y)\,i+\frac{∂}{∂y}(3 x^{2} + 2 x y^{2} - y)\,j \\  & =(6 x + 2 y^{2})\,i+(4 x y - 1)\,j \\ ∇f(-1,1) & =(6 (-1) + 2 (1)^{2})\,i+(4 (-1) (1) - 1)\,j \\  & =(-4)\,i+(-5)\,j \\  & =⟨-4,-5⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-1,1)\cdot ⟨x-(-1),\,y-(1)⟩ & =0 \\ ⟨-4,-5⟩\cdot ⟨x + 1,\,y - 1⟩ & =0.\end{aligned}
$$

### Generated raw coordinate pullback q-36383 — unrated — observed raw

Given the function $f(x, y) = 3(2x)^{2} + 2(2x)(3y)^{2} - (3y)$, find the equation of the tangent line to the level curve that passes through the point where $(x, y) = (- \frac{1}{2},\frac{1}{3})$.

- [ ] $⟨10,12⟩ \cdot ⟨x + \frac{1}{2},\,y - \frac{1}{3}⟩ = 0$
- [ ] $⟨10,9⟩ \cdot ⟨x + \frac{1}{2},\,y - \frac{1}{3}⟩ = 0$
- [ ] $⟨4,-3⟩ \cdot ⟨x + \frac{1}{2},\,y - \frac{1}{3}⟩ = 0$
- [ ] $⟨12,6⟩ \cdot ⟨x + \frac{1}{2},\,y - \frac{1}{3}⟩ = 0$
- [ ] $⟨-8,-15⟩ \cdot ⟨x + \frac{1}{2},\,y - \frac{1}{3}⟩ = 0$

*Original worked solution absent.*

*Original correct designation absent; the separate completion shows the inferred gradient representation.*

### Generated authored safe bank q-36383 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=3 x^{2} + 4 x y^{2} + 3 y$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(2,-1).$

- [ ] $⟨-13,16⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [x] $⟨16,-13⟩\cdot ⟨x - 2,\,y + 1⟩=0$ **correct**
- [ ] $⟨-16,-13⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [ ] $⟨16,-13⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨16,-13⟩\cdot ⟨x + 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(2,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x^{2} + 4 x y^{2} + 3 y)\,i+\frac{∂}{∂y}(3 x^{2} + 4 x y^{2} + 3 y)\,j \\  & =(6 x + 4 y^{2})\,i+(8 x y + 3)\,j \\ ∇f(2,-1) & =(6 (2) + 4 (-1)^{2})\,i+(8 (2) (-1) + 3)\,j \\  & =(16)\,i+(-13)\,j \\  & =⟨16,-13⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(2,-1)\cdot ⟨x-(2),\,y-(-1)⟩ & =0 \\ ⟨16,-13⟩\cdot ⟨x - 2,\,y + 1⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-36383 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=5 x^{2} - 4 x y^{2} + 5 y$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-2,1).$

- [ ] $⟨24,21⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [ ] $⟨-24,21⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨21,-24⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [x] $⟨-24,21⟩\cdot ⟨x + 2,\,y - 1⟩=0$ **correct**
- [ ] $⟨-24,21⟩\cdot ⟨x + 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-2,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5 x^{2} - 4 x y^{2} + 5 y)\,i+\frac{∂}{∂y}(5 x^{2} - 4 x y^{2} + 5 y)\,j \\  & =(10 x - 4 y^{2})\,i+(- 8 x y + 5)\,j \\ ∇f(-2,1) & =(10 (-2) - 4 (1)^{2})\,i+(- 8 (-2) (1) + 5)\,j \\  & =(-24)\,i+(21)\,j \\  & =⟨-24,21⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-2,1)\cdot ⟨x-(-2),\,y-(1)⟩ & =0 \\ ⟨-24,21⟩\cdot ⟨x + 2,\,y - 1⟩ & =0.\end{aligned}
$$

### Original raw q-37517 — unrated — observed raw

Given the function $f(x, y) = \cos (x^{2}) - 3y^{3}$, find the equation of the tangent line to the level curve that passes through the point where $(x, y) = (\sqrt{π}, 2)$.

- [ ] $⟨36, 0⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$
- [ ] $⟨6, 9⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$
- [ ] $⟨0, 1⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$
- [ ] $⟨0,-36⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$
- [ ] $⟨0, 12⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$

*Original worked solution absent.*

*Original correct designation absent; the separate completion shows the inferred gradient representation.*

### Inferred completion / opaque evidence q-37517 — :question.difficulty/easy — inferred completion; opaque bank

Given the function $f(x, y) = \cos (x^{2}) - 3y^{3}$, find the equation of the tangent line to the level curve that passes through the point where $(x, y) = (\sqrt{π}, 2)$.

- [ ] $⟨36, 0⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$
- [ ] $⟨6, 9⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$
- [ ] $⟨0, 1⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$
- [x] $⟨0,-36⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$ **correct**
- [ ] $⟨0, 12⟩ \cdot ⟨x - \sqrt{π}, y - 2⟩ = 0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(\sqrt{\pi},2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- 3 y^{3} + \cos{\left(x^{2} \right)})\,i+\frac{∂}{∂y}(- 3 y^{3} + \cos{\left(x^{2} \right)})\,j \\  & =(- 2 x \sin{\left(x^{2} \right)})\,i+(- 9 y^{2})\,j \\ ∇f(\sqrt{\pi},2) & =(- 2 (\sqrt{\pi}) \sin{\left((\sqrt{\pi})^{2} \right)})\,i+(- 9 (2)^{2})\,j \\  & =(0)\,i+(-36)\,j \\  & =⟨0,-36⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(\sqrt{\pi},2)\cdot ⟨x-(\sqrt{\pi}),\,y-(2)⟩ & =0 \\ ⟨0,-36⟩\cdot ⟨x - \sqrt{\pi},\,y - 2⟩ & =0.\end{aligned}
$$

### Generated raw coordinate pullback q-37517 — unrated — observed raw

Given the function $f(x, y) = \cos ((2x)^{2}) - 3(3y)^{3}$, find the equation of the tangent line to the level curve that passes through the point where $(x, y) = (\frac{\sqrt{\pi}}{2},\frac{2}{3})$.

- [ ] $⟨72,0⟩ \cdot ⟨x - \frac{\sqrt{\pi}}{2},\,y - \frac{2}{3}⟩ = 0$
- [ ] $⟨12,27⟩ \cdot ⟨x - \frac{\sqrt{\pi}}{2},\,y - \frac{2}{3}⟩ = 0$
- [ ] $⟨0,3⟩ \cdot ⟨x - \frac{\sqrt{\pi}}{2},\,y - \frac{2}{3}⟩ = 0$
- [ ] $⟨0,-108⟩ \cdot ⟨x - \frac{\sqrt{\pi}}{2},\,y - \frac{2}{3}⟩ = 0$
- [ ] $⟨0,36⟩ \cdot ⟨x - \frac{\sqrt{\pi}}{2},\,y - \frac{2}{3}⟩ = 0$

*Original worked solution absent.*

*Original correct designation absent; the separate completion shows the inferred gradient representation.*

### Generated authored safe bank q-37517 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=4 y^{3} + \cos{\left(x^{2} \right)}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(\sqrt{\pi},-1).$

- [ ] $⟨- 2 \sqrt{\pi},12⟩\cdot ⟨x - \sqrt{\pi},\,y + 1⟩=0$
- [x] $⟨0,12⟩\cdot ⟨x - \sqrt{\pi},\,y + 1⟩=0$ **correct**
- [ ] $⟨12,0⟩\cdot ⟨x - \sqrt{\pi},\,y + 1⟩=0$
- [ ] $⟨0,12⟩\cdot ⟨x - \sqrt{\pi},\,y - 1⟩=0$
- [ ] $⟨0,12⟩\cdot ⟨x - \sqrt{\pi},\,y⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(\sqrt{\pi},-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(4 y^{3} + \cos{\left(x^{2} \right)})\,i+\frac{∂}{∂y}(4 y^{3} + \cos{\left(x^{2} \right)})\,j \\  & =(- 2 x \sin{\left(x^{2} \right)})\,i+(12 y^{2})\,j \\ ∇f(\sqrt{\pi},-1) & =(- 2 (\sqrt{\pi}) \sin{\left((\sqrt{\pi})^{2} \right)})\,i+(12 (-1)^{2})\,j \\  & =(0)\,i+(12)\,j \\  & =⟨0,12⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(\sqrt{\pi},-1)\cdot ⟨x-(\sqrt{\pi}),\,y-(-1)⟩ & =0 \\ ⟨0,12⟩\cdot ⟨x - \sqrt{\pi},\,y + 1⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-37517 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=- 4 y^{3} + \cos{\left(x^{2} \right)}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(\sqrt{\pi},1).$

- [ ] $⟨-12,0⟩\cdot ⟨x - \sqrt{\pi},\,y - 1⟩=0$
- [ ] $⟨0,-12⟩\cdot ⟨x - \sqrt{\pi},\,y⟩=0$
- [ ] $⟨- 2 \sqrt{\pi},-12⟩\cdot ⟨x - \sqrt{\pi},\,y - 1⟩=0$
- [x] $⟨0,-12⟩\cdot ⟨x - \sqrt{\pi},\,y - 1⟩=0$ **correct**
- [ ] $⟨0,-12⟩\cdot ⟨x - \sqrt{\pi},\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(\sqrt{\pi},1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- 4 y^{3} + \cos{\left(x^{2} \right)})\,i+\frac{∂}{∂y}(- 4 y^{3} + \cos{\left(x^{2} \right)})\,j \\  & =(- 2 x \sin{\left(x^{2} \right)})\,i+(- 12 y^{2})\,j \\ ∇f(\sqrt{\pi},1) & =(- 2 (\sqrt{\pi}) \sin{\left((\sqrt{\pi})^{2} \right)})\,i+(- 12 (1)^{2})\,j \\  & =(0)\,i+(-12)\,j \\  & =⟨0,-12⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(\sqrt{\pi},1)\cdot ⟨x-(\sqrt{\pi}),\,y-(1)⟩ & =0 \\ ⟨0,-12⟩\cdot ⟨x - \sqrt{\pi},\,y - 1⟩ & =0.\end{aligned}
$$

### Original raw q-130096 — :question.difficulty/easy — observed raw

Given the function $f(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}+1),$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-1,0).$

- [ ] $⟨1,-1⟩\cdot ⟨x+1,\,y⟩=0$
- [ ] $⟨-1,1⟩\cdot ⟨x+1,\,y⟩=0$
- [ ] $⟨2,0⟩\cdot ⟨x+1,\,y⟩=0$
- [ ] $⟨0,-2⟩\cdot ⟨x+1,\,y⟩=0$
- [x] $⟨-1,0⟩\cdot ⟨x+1,\,y⟩=0$ **correct**

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-1,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+1))\,i+\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+1))\,j \\  & =\frac{2x}{{x}^{2}+{y}^{2}+1}\,i+\frac{2y}{{x}^{2}+{y}^{2}+1}\,j \\ ∇f(-1,0) & =\frac{2(-1)}{(-1)^{2}+{0}^{2}+1}\,i+\frac{2(0)}{(-1)^{2}+{0}^{2}+1}\,j \\  & =(-1)i+0\,j \\  & =⟨-1,0⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-1,0)\cdot ⟨x-(-1),\,y-0⟩ & =0 \\ ⟨-1,0⟩\cdot ⟨x+1,\,y⟩ & =0.\end{aligned}
$$

### Inferred completion / opaque evidence q-130096 — :question.difficulty/easy — inferred completion; opaque bank

Given the function $f(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}+1),$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-1,0).$

- [ ] $⟨1,-1⟩\cdot ⟨x+1,\,y⟩=0$
- [ ] $⟨-1,1⟩\cdot ⟨x+1,\,y⟩=0$
- [ ] $⟨2,0⟩\cdot ⟨x+1,\,y⟩=0$
- [ ] $⟨0,-2⟩\cdot ⟨x+1,\,y⟩=0$
- [x] $⟨-1,0⟩\cdot ⟨x+1,\,y⟩=0$ **correct**

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-1,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+1))\,i+\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+1))\,j \\  & =\frac{2x}{{x}^{2}+{y}^{2}+1}\,i+\frac{2y}{{x}^{2}+{y}^{2}+1}\,j \\ ∇f(-1,0) & =\frac{2(-1)}{(-1)^{2}+{0}^{2}+1}\,i+\frac{2(0)}{(-1)^{2}+{0}^{2}+1}\,j \\  & =(-1)i+0\,j \\  & =⟨-1,0⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-1,0)\cdot ⟨x-(-1),\,y-0⟩ & =0 \\ ⟨-1,0⟩\cdot ⟨x+1,\,y⟩ & =0.\end{aligned}
$$

### Generated raw coordinate pullback q-130096 — :question.difficulty/easy — observed raw

Given the function $f(x,y)=\operatorname{ln}⁡({(2x)}^{2}+{(3y)}^{2}+1),$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(- \frac{1}{2},0).$

- [ ] $⟨2,-3⟩\cdot ⟨x + \frac{1}{2},\,y⟩=0$
- [ ] $⟨-2,3⟩\cdot ⟨x + \frac{1}{2},\,y⟩=0$
- [ ] $⟨4,0⟩\cdot ⟨x + \frac{1}{2},\,y⟩=0$
- [ ] $⟨0,-6⟩\cdot ⟨x + \frac{1}{2},\,y⟩=0$
- [x] $⟨-2,0⟩\cdot ⟨x + \frac{1}{2},\,y⟩=0$ **correct**

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(- \frac{1}{2},0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡({(2x)}^{2}+{(3y)}^{2}+1))\,i+\frac{∂}{∂y}(\operatorname{ln}⁡({(2x)}^{2}+{(3y)}^{2}+1))\,j \\  & =2(\frac{2(2x)}{{(2x)}^{2}+{(3y)}^{2}+1})\,i+3(\frac{2(3y)}{{(2x)}^{2}+{(3y)}^{2}+1})\,j \\ ∇f(- \frac{1}{2},0) & =(\frac{8 (- \frac{1}{2})}{4 (- \frac{1}{2})^{2} + 9 (0)^{2} + 1})\,i+(\frac{18 (0)}{4 (- \frac{1}{2})^{2} + 9 (0)^{2} + 1})\,j \\  & =(-2)\,i+(0)\,j \\  & =⟨-2,0⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(- \frac{1}{2},0)\cdot ⟨x-(- \frac{1}{2}),\,y-(0)⟩ & =0 \\ ⟨-2,0⟩\cdot ⟨x + \frac{1}{2},\,y⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-130096 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=\ln{\left(3 x^{2} + 4 y^{2} + 3 \right)}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(2,-1).$

- [ ] $⟨- \frac{8}{19},\frac{12}{19}⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [x] $⟨\frac{12}{19},- \frac{8}{19}⟩\cdot ⟨x - 2,\,y + 1⟩=0$ **correct**
- [ ] $⟨- \frac{12}{19},- \frac{8}{19}⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [ ] $⟨\frac{12}{19},- \frac{8}{19}⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨\frac{12}{19},- \frac{8}{19}⟩\cdot ⟨x + 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(2,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\ln{\left(3 x^{2} + 4 y^{2} + 3 \right)})\,i+\frac{∂}{∂y}(\ln{\left(3 x^{2} + 4 y^{2} + 3 \right)})\,j \\  & =(\frac{6 x}{3 x^{2} + 4 y^{2} + 3})\,i+(\frac{8 y}{3 x^{2} + 4 y^{2} + 3})\,j \\ ∇f(2,-1) & =(\frac{6 (2)}{3 (2)^{2} + 4 (-1)^{2} + 3})\,i+(\frac{8 (-1)}{3 (2)^{2} + 4 (-1)^{2} + 3})\,j \\  & =(\frac{12}{19})\,i+(- \frac{8}{19})\,j \\  & =⟨\frac{12}{19},- \frac{8}{19}⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(2,-1)\cdot ⟨x-(2),\,y-(-1)⟩ & =0 \\ ⟨\frac{12}{19},- \frac{8}{19}⟩\cdot ⟨x - 2,\,y + 1⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-130096 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=\ln{\left(3 x^{2} + 4 y^{2} + 4 \right)}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(2,1).$

- [ ] $⟨- \frac{3}{5},\frac{2}{5}⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨\frac{3}{5},\frac{2}{5}⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [ ] $⟨\frac{2}{5},\frac{3}{5}⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [x] $⟨\frac{3}{5},\frac{2}{5}⟩\cdot ⟨x - 2,\,y - 1⟩=0$ **correct**
- [ ] $⟨\frac{3}{5},\frac{2}{5}⟩\cdot ⟨x - 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(2,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\ln{\left(3 x^{2} + 4 y^{2} + 4 \right)})\,i+\frac{∂}{∂y}(\ln{\left(3 x^{2} + 4 y^{2} + 4 \right)})\,j \\  & =(\frac{6 x}{3 x^{2} + 4 y^{2} + 4})\,i+(\frac{8 y}{3 x^{2} + 4 y^{2} + 4})\,j \\ ∇f(2,1) & =(\frac{6 (2)}{3 (2)^{2} + 4 (1)^{2} + 4})\,i+(\frac{8 (1)}{3 (2)^{2} + 4 (1)^{2} + 4})\,j \\  & =(\frac{3}{5})\,i+(\frac{2}{5})\,j \\  & =⟨\frac{3}{5},\frac{2}{5}⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(2,1)\cdot ⟨x-(2),\,y-(1)⟩ & =0 \\ ⟨\frac{3}{5},\frac{2}{5}⟩\cdot ⟨x - 2,\,y - 1⟩ & =0.\end{aligned}
$$

### Original raw q-130104 — :question.difficulty/easy — observed raw

Given the function $f(x,y)={x}^{2}-4xy+5{y}^{2}$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-1,-1).$

- [ ] $⟨-2,4⟩\cdot ⟨x+1,\,y+1⟩=0$
- [ ] $⟨0,-1⟩\cdot ⟨x+1,\,y+1⟩=0$
- [ ] $⟨2,0⟩\cdot ⟨x+1,\,y+1⟩=0$
- [x] $⟨2,-6⟩\cdot ⟨x+1,\,y+1⟩=0$ **correct**
- [ ] $⟨3,1⟩\cdot ⟨x+1,\,y+1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-1,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({x}^{2}-4xy+5{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}-4xy+5{y}^{2})\,j \\  & =(2x-4y)\,i+(10y-4x)\,j \\ ∇f(-1,-1) & =(2(-1)-4(-1))\,i+(10(-1)-4(-1))\,j \\  & =2\,i-6\,j \\  & =⟨2,-6⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-1,-1)\cdot ⟨x-(-1),\,y-(-1)⟩ & =0 \\ ⟨2,-6⟩\cdot ⟨x+1,\,y+1⟩ & =0.\end{aligned}
$$

### Inferred completion / opaque evidence q-130104 — :question.difficulty/easy — inferred completion; opaque bank

Given the function $f(x,y)={x}^{2}-4xy+5{y}^{2}$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-1,-1).$

- [ ] $⟨-2,4⟩\cdot ⟨x+1,\,y+1⟩=0$
- [ ] $⟨0,-1⟩\cdot ⟨x+1,\,y+1⟩=0$
- [ ] $⟨2,0⟩\cdot ⟨x+1,\,y+1⟩=0$
- [x] $⟨2,-6⟩\cdot ⟨x+1,\,y+1⟩=0$ **correct**
- [ ] $⟨3,1⟩\cdot ⟨x+1,\,y+1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-1,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({x}^{2}-4xy+5{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}-4xy+5{y}^{2})\,j \\  & =(2x-4y)\,i+(10y-4x)\,j \\ ∇f(-1,-1) & =(2(-1)-4(-1))\,i+(10(-1)-4(-1))\,j \\  & =2\,i-6\,j \\  & =⟨2,-6⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-1,-1)\cdot ⟨x-(-1),\,y-(-1)⟩ & =0 \\ ⟨2,-6⟩\cdot ⟨x+1,\,y+1⟩ & =0.\end{aligned}
$$

### Generated raw coordinate pullback q-130104 — :question.difficulty/easy — observed raw

Given the function $f(x,y)={(2x)}^{2}-4(2x)(3y)+5{(3y)}^{2}$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(- \frac{1}{2},- \frac{1}{3}).$

- [ ] $⟨-4,12⟩\cdot ⟨x + \frac{1}{2},\,y + \frac{1}{3}⟩=0$
- [ ] $⟨0,-3⟩\cdot ⟨x + \frac{1}{2},\,y + \frac{1}{3}⟩=0$
- [ ] $⟨4,0⟩\cdot ⟨x + \frac{1}{2},\,y + \frac{1}{3}⟩=0$
- [x] $⟨4,-18⟩\cdot ⟨x + \frac{1}{2},\,y + \frac{1}{3}⟩=0$ **correct**
- [ ] $⟨6,3⟩\cdot ⟨x + \frac{1}{2},\,y + \frac{1}{3}⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(- \frac{1}{2},- \frac{1}{3}):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({(2x)}^{2}-4(2x)(3y)+5{(3y)}^{2})\,i+\frac{∂}{∂y}({(2x)}^{2}-4(2x)(3y)+5{(3y)}^{2})\,j \\  & =2((2(2x)-4(3y)))\,i+3((10(3y)-4(2x)))\,j \\ ∇f(- \frac{1}{2},- \frac{1}{3}) & =(8 (- \frac{1}{2}) - 24 (- \frac{1}{3}))\,i+(- 24 (- \frac{1}{2}) + 90 (- \frac{1}{3}))\,j \\  & =(4)\,i+(-18)\,j \\  & =⟨4,-18⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(- \frac{1}{2},- \frac{1}{3})\cdot ⟨x-(- \frac{1}{2}),\,y-(- \frac{1}{3})⟩ & =0 \\ ⟨4,-18⟩\cdot ⟨x + \frac{1}{2},\,y + \frac{1}{3}⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-130104 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=3 x^{2} + 4 x y + 3 y^{2}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(2,-1).$

- [ ] $⟨2,8⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [x] $⟨8,2⟩\cdot ⟨x - 2,\,y + 1⟩=0$ **correct**
- [ ] $⟨-8,2⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [ ] $⟨8,2⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨8,2⟩\cdot ⟨x + 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(2,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x^{2} + 4 x y + 3 y^{2})\,i+\frac{∂}{∂y}(3 x^{2} + 4 x y + 3 y^{2})\,j \\  & =(6 x + 4 y)\,i+(4 x + 6 y)\,j \\ ∇f(2,-1) & =(6 (2) + 4 (-1))\,i+(4 (2) + 6 (-1))\,j \\  & =(8)\,i+(2)\,j \\  & =⟨8,2⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(2,-1)\cdot ⟨x-(2),\,y-(-1)⟩ & =0 \\ ⟨8,2⟩\cdot ⟨x - 2,\,y + 1⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-130104 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=5 x^{2} - 4 x y + 5 y^{2}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-2,1).$

- [ ] $⟨24,18⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [ ] $⟨-24,18⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨18,-24⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [x] $⟨-24,18⟩\cdot ⟨x + 2,\,y - 1⟩=0$ **correct**
- [ ] $⟨-24,18⟩\cdot ⟨x + 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-2,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5 x^{2} - 4 x y + 5 y^{2})\,i+\frac{∂}{∂y}(5 x^{2} - 4 x y + 5 y^{2})\,j \\  & =(10 x - 4 y)\,i+(- 4 x + 10 y)\,j \\ ∇f(-2,1) & =(10 (-2) - 4 (1))\,i+(- 4 (-2) + 10 (1))\,j \\  & =(-24)\,i+(18)\,j \\  & =⟨-24,18⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-2,1)\cdot ⟨x-(-2),\,y-(1)⟩ & =0 \\ ⟨-24,18⟩\cdot ⟨x + 2,\,y - 1⟩ & =0.\end{aligned}
$$

### Original raw q-72371 — :question.difficulty/easy — observed raw

Given the function $f(x,y)={x}^{2}{y}^{2}+xy$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,2).$

- [ ] $⟨-10,15⟩\cdot ⟨x-1,\,y-2⟩=0$
- [ ] $⟨5,10⟩\cdot ⟨x-1,\,y-2⟩=0$
- [ ] $⟨8,5⟩\cdot ⟨x-1,\,y-2⟩=0$
- [x] $⟨10,5⟩\cdot ⟨x-1,\,y-2⟩=0$ **correct**
- [ ] $⟨15,10⟩\cdot ⟨x-1,\,y-2⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as 

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(1,2):$

$$
\begin{aligned}∇\,f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({x}^{2}{y}^{2}+xy)\,i+\frac{∂}{∂y}({x}^{2}{y}^{2}+xy)\,j \\  & =(2x{y}^{2}+y)\,i+(2y{x}^{2}+x)\,j \\ ∇\,f(1,2) & =(2(1)(2)^{2}+(2))\,i+(2(2)(1)^{2}+(1))\,j \\  & =10\,i+5\,j \\  & =⟨10,5⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(1,2)\cdot ⟨x-1,\,y-2⟩ & =0 \\ ⟨10,5⟩\cdot ⟨x-1,\,y-2⟩ & =0\end{aligned}
$$

### Inferred completion / opaque evidence q-72371 — :question.difficulty/easy — inferred completion; opaque bank

Given the function $f(x,y)={x}^{2}{y}^{2}+xy$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,2).$

- [ ] $⟨-10,15⟩\cdot ⟨x-1,\,y-2⟩=0$
- [ ] $⟨5,10⟩\cdot ⟨x-1,\,y-2⟩=0$
- [ ] $⟨8,5⟩\cdot ⟨x-1,\,y-2⟩=0$
- [x] $⟨10,5⟩\cdot ⟨x-1,\,y-2⟩=0$ **correct**
- [ ] $⟨15,10⟩\cdot ⟨x-1,\,y-2⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as 

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(1,2):$

$$
\begin{aligned}∇\,f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({x}^{2}{y}^{2}+xy)\,i+\frac{∂}{∂y}({x}^{2}{y}^{2}+xy)\,j \\  & =(2x{y}^{2}+y)\,i+(2y{x}^{2}+x)\,j \\ ∇\,f(1,2) & =(2(1)(2)^{2}+(2))\,i+(2(2)(1)^{2}+(1))\,j \\  & =10\,i+5\,j \\  & =⟨10,5⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(1,2)\cdot ⟨x-1,\,y-2⟩ & =0 \\ ⟨10,5⟩\cdot ⟨x-1,\,y-2⟩ & =0\end{aligned}
$$

### Generated raw coordinate pullback q-72371 — :question.difficulty/easy — observed raw

Given the function $f(x,y)={(2x)}^{2}{(3y)}^{2}+(2x)(3y)$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(\frac{1}{2},\frac{2}{3}).$

- [ ] $⟨-20,45⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{2}{3}⟩=0$
- [ ] $⟨10,30⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{2}{3}⟩=0$
- [ ] $⟨16,15⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{2}{3}⟩=0$
- [x] $⟨20,15⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{2}{3}⟩=0$ **correct**
- [ ] $⟨30,30⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{2}{3}⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as 

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(\frac{1}{2},\frac{2}{3}):$

$$
\begin{aligned}∇\,f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({(2x)}^{2}{(3y)}^{2}+(2x)(3y))\,i+\frac{∂}{∂y}({(2x)}^{2}{(3y)}^{2}+(2x)(3y))\,j \\  & =2((2(2x){(3y)}^{2}+(3y)))\,i+3((2(3y){(2x)}^{2}+(2x)))\,j \\ ∇\,f(\frac{1}{2},\frac{2}{3}) & =(72 (\frac{1}{2}) (\frac{2}{3})^{2} + 6 (\frac{2}{3}))\,i+(72 (\frac{1}{2})^{2} (\frac{2}{3}) + 6 (\frac{1}{2}))\,j \\  & =(20)\,i+(15)\,j \\  & =⟨20,15⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(\frac{1}{2},\frac{2}{3})\cdot ⟨x-(\frac{1}{2}),\,y-(\frac{2}{3})⟩ & =0 \\ ⟨20,15⟩\cdot ⟨x-(\frac{1}{2}),\,y-(\frac{2}{3})⟩ & =0\end{aligned}
$$

### Generated authored safe bank q-72371 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=3 x^{2} y^{2} + 4 x y$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(2,-1).$

- [ ] $⟨8,-24⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [x] $⟨8,-16⟩\cdot ⟨x - 2,\,y + 1⟩=0$ **correct**
- [ ] $⟨12,-16⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [ ] $⟨-8,-16⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [ ] $⟨-16,8⟩\cdot ⟨x - 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(2,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x^{2} y^{2} + 4 x y)\,i+\frac{∂}{∂y}(3 x^{2} y^{2} + 4 x y)\,j \\  & =(6 x y^{2} + 4 y)\,i+(6 x^{2} y + 4 x)\,j \\ ∇f(2,-1) & =(6 (2) (-1)^{2} + 4 (-1))\,i+(6 (2)^{2} (-1) + 4 (2))\,j \\  & =(8)\,i+(-16)\,j \\  & =⟨8,-16⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(2,-1)\cdot ⟨x-(2),\,y-(-1)⟩ & =0 \\ ⟨8,-16⟩\cdot ⟨x - 2,\,y + 1⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-72371 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=5 x^{2} y^{2} - 4 x y$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-2,1).$

- [ ] $⟨-20,48⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [ ] $⟨48,-24⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [ ] $⟨-24,40⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [x] $⟨-24,48⟩\cdot ⟨x + 2,\,y - 1⟩=0$ **correct**
- [ ] $⟨24,48⟩\cdot ⟨x + 2,\,y - 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-2,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5 x^{2} y^{2} - 4 x y)\,i+\frac{∂}{∂y}(5 x^{2} y^{2} - 4 x y)\,j \\  & =(10 x y^{2} - 4 y)\,i+(10 x^{2} y - 4 x)\,j \\ ∇f(-2,1) & =(10 (-2) (1)^{2} - 4 (1))\,i+(10 (-2)^{2} (1) - 4 (-2))\,j \\  & =(-24)\,i+(48)\,j \\  & =⟨-24,48⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-2,1)\cdot ⟨x-(-2),\,y-(1)⟩ & =0 \\ ⟨-24,48⟩\cdot ⟨x + 2,\,y - 1⟩ & =0.\end{aligned}
$$

### Original raw q-130094 — :question.difficulty/easy — observed raw

Given the function $f(x,y)=x{y}^{2}-x+y,$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,-1).$

- [ ] $⟨-1,1⟩\cdot ⟨x-1,\,y+1⟩=0$
- [ ] $⟨-1,0⟩\cdot ⟨x-1,\,y+1⟩=0$
- [ ] $⟨1,0⟩\cdot ⟨x-1,\,y+1⟩=0$
- [x] $⟨0,-1⟩\cdot ⟨x-1,\,y+1⟩=0$ **correct**
- [ ] $⟨1,-1⟩\cdot ⟨x-1,\,y+1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(1,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x{y}^{2}-x+y)\,i+\frac{∂}{∂y}(x{y}^{2}-x+y)\,j \\  & =({y}^{2}-1)\text{ }i+(2xy+1)\text{ }j \\ ∇f(1,-1) & =((-1)^{2}-1)\,i+(2(1)(-1)+1)\,j \\  & =0\,i-j \\  & =⟨0,-1⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(1,-1)\cdot ⟨x-1,\,y-(-1)⟩ & =0 \\ ⟨0,-1⟩\cdot ⟨x-1,\,y+1⟩ & =0.\end{aligned}
$$

### Inferred completion / opaque evidence q-130094 — :question.difficulty/easy — inferred completion; opaque bank

Given the function $f(x,y)=x{y}^{2}-x+y,$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,-1).$

- [ ] $⟨-1,1⟩\cdot ⟨x-1,\,y+1⟩=0$
- [ ] $⟨-1,0⟩\cdot ⟨x-1,\,y+1⟩=0$
- [ ] $⟨1,0⟩\cdot ⟨x-1,\,y+1⟩=0$
- [x] $⟨0,-1⟩\cdot ⟨x-1,\,y+1⟩=0$ **correct**
- [ ] $⟨1,-1⟩\cdot ⟨x-1,\,y+1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(1,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x{y}^{2}-x+y)\,i+\frac{∂}{∂y}(x{y}^{2}-x+y)\,j \\  & =({y}^{2}-1)\text{ }i+(2xy+1)\text{ }j \\ ∇f(1,-1) & =((-1)^{2}-1)\,i+(2(1)(-1)+1)\,j \\  & =0\,i-j \\  & =⟨0,-1⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(1,-1)\cdot ⟨x-1,\,y-(-1)⟩ & =0 \\ ⟨0,-1⟩\cdot ⟨x-1,\,y+1⟩ & =0.\end{aligned}
$$

### Generated raw coordinate pullback q-130094 — :question.difficulty/easy — observed raw

Given the function $f(x,y)=(2x){(3y)}^{2}-(2x)+(3y),$ find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(\frac{1}{2},- \frac{1}{3}).$

- [ ] $⟨-2,3⟩\cdot ⟨x - \frac{1}{2},\,y + \frac{1}{3}⟩=0$
- [ ] $⟨-2,0⟩\cdot ⟨x - \frac{1}{2},\,y + \frac{1}{3}⟩=0$
- [ ] $⟨2,0⟩\cdot ⟨x - \frac{1}{2},\,y + \frac{1}{3}⟩=0$
- [x] $⟨0,-3⟩\cdot ⟨x - \frac{1}{2},\,y + \frac{1}{3}⟩=0$ **correct**
- [ ] $⟨2,-3⟩\cdot ⟨x - \frac{1}{2},\,y + \frac{1}{3}⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(\frac{1}{2},- \frac{1}{3}):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}((2x){(3y)}^{2}-(2x)+(3y))\,i+\frac{∂}{∂y}((2x){(3y)}^{2}-(2x)+(3y))\,j \\  & =2(({(3y)}^{2}-1))\text{ }i+3((2(2x)(3y)+1))\text{ }j \\ ∇f(\frac{1}{2},- \frac{1}{3}) & =(18 (- \frac{1}{3})^{2} - 2)\,i+(36 (\frac{1}{2}) (- \frac{1}{3}) + 3)\,j \\  & =(0)\,i+(-3)\,j \\  & =⟨0,-3⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(\frac{1}{2},- \frac{1}{3})\cdot ⟨x-(\frac{1}{2}),\,y-(- \frac{1}{3})⟩ & =0 \\ ⟨0,-3⟩\cdot ⟨x - \frac{1}{2},\,y + \frac{1}{3}⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-130094 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=3 x y^{2} + 4 x + 3 y$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(2,-1).$

- [ ] $⟨-9,7⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [x] $⟨7,-9⟩\cdot ⟨x - 2,\,y + 1⟩=0$ **correct**
- [ ] $⟨-7,-9⟩\cdot ⟨x - 2,\,y + 1⟩=0$
- [ ] $⟨7,-9⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨7,-9⟩\cdot ⟨x + 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(2,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x y^{2} + 4 x + 3 y)\,i+\frac{∂}{∂y}(3 x y^{2} + 4 x + 3 y)\,j \\  & =(3 y^{2} + 4)\,i+(6 x y + 3)\,j \\ ∇f(2,-1) & =(3 (-1)^{2} + 4)\,i+(6 (2) (-1) + 3)\,j \\  & =(7)\,i+(-9)\,j \\  & =⟨7,-9⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(2,-1)\cdot ⟨x-(2),\,y-(-1)⟩ & =0 \\ ⟨7,-9⟩\cdot ⟨x - 2,\,y + 1⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-130094 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=5 x y^{2} - 4 x + 5 y$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-2,1).$

- [ ] $⟨-1,-15⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [ ] $⟨1,-15⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨-15,1⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [x] $⟨1,-15⟩\cdot ⟨x + 2,\,y - 1⟩=0$ **correct**
- [ ] $⟨1,-15⟩\cdot ⟨x + 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-2,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5 x y^{2} - 4 x + 5 y)\,i+\frac{∂}{∂y}(5 x y^{2} - 4 x + 5 y)\,j \\  & =(5 y^{2} - 4)\,i+(10 x y + 5)\,j \\ ∇f(-2,1) & =(5 (1)^{2} - 4)\,i+(10 (-2) (1) + 5)\,j \\  & =(1)\,i+(-15)\,j \\  & =⟨1,-15⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-2,1)\cdot ⟨x-(-2),\,y-(1)⟩ & =0 \\ ⟨1,-15⟩\cdot ⟨x + 2,\,y - 1⟩ & =0.\end{aligned}
$$

### Original raw q-72377 — :question.difficulty/easy — observed raw

Given the function $f(x,y)=2x{y}^{2}+xy+2x$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,1).$

- [ ] $⟨-5,5⟩\cdot ⟨x-1,\,y-1⟩=0$
- [ ] $⟨4,5⟩\cdot ⟨x-1,\,y-1⟩=0$
- [ ] $⟨3,2⟩\cdot ⟨x-1,\,y-1⟩=0$
- [x] $⟨5,5⟩\cdot ⟨x-1,\,y-1⟩=0$ **correct**
- [ ] $⟨2,3⟩\cdot ⟨x-1,\,y-1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(1,1):$

$$
\begin{aligned}∇\,f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2x{y}^{2}+xy+2x)\,i+\frac{∂}{∂y}(2x{y}^{2}+xy+2x)\,j \\  & =(2{y}^{2}+y+2)\,i+(4xy+x)\,j \\ ∇\,f(1,1) & =(2(1)^{2}+(1)+2)\,i+(4(1)(1)+(1))\,j \\  & =5\,i+5\,j \\  & =⟨5,5⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(1,1)\cdot ⟨x-1,\,y-1⟩ & =0 \\ ⟨5,5⟩\cdot ⟨x-1,\,y-1⟩ & =0\end{aligned}
$$

### Inferred completion / opaque evidence q-72377 — :question.difficulty/easy — inferred completion; opaque bank

Given the function $f(x,y)=2x{y}^{2}+xy+2x$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,1).$

- [ ] $⟨-5,5⟩\cdot ⟨x-1,\,y-1⟩=0$
- [ ] $⟨4,5⟩\cdot ⟨x-1,\,y-1⟩=0$
- [ ] $⟨3,2⟩\cdot ⟨x-1,\,y-1⟩=0$
- [x] $⟨5,5⟩\cdot ⟨x-1,\,y-1⟩=0$ **correct**
- [ ] $⟨2,3⟩\cdot ⟨x-1,\,y-1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(1,1):$

$$
\begin{aligned}∇\,f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2x{y}^{2}+xy+2x)\,i+\frac{∂}{∂y}(2x{y}^{2}+xy+2x)\,j \\  & =(2{y}^{2}+y+2)\,i+(4xy+x)\,j \\ ∇\,f(1,1) & =(2(1)^{2}+(1)+2)\,i+(4(1)(1)+(1))\,j \\  & =5\,i+5\,j \\  & =⟨5,5⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(1,1)\cdot ⟨x-1,\,y-1⟩ & =0 \\ ⟨5,5⟩\cdot ⟨x-1,\,y-1⟩ & =0\end{aligned}
$$

### Generated raw coordinate pullback q-72377 — :question.difficulty/easy — observed raw

Given the function $f(x,y)=2(2x){(3y)}^{2}+(2x)(3y)+2(2x)$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(\frac{1}{2},\frac{1}{3}).$

- [ ] $⟨-10,15⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{1}{3}⟩=0$
- [ ] $⟨8,15⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{1}{3}⟩=0$
- [ ] $⟨6,6⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{1}{3}⟩=0$
- [x] $⟨10,15⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{1}{3}⟩=0$ **correct**
- [ ] $⟨4,9⟩\cdot ⟨x - \frac{1}{2},\,y - \frac{1}{3}⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(\frac{1}{2},\frac{1}{3}):$

$$
\begin{aligned}∇\,f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2(2x){(3y)}^{2}+(2x)(3y)+2(2x))\,i+\frac{∂}{∂y}(2(2x){(3y)}^{2}+(2x)(3y)+2(2x))\,j \\  & =2((2{(3y)}^{2}+(3y)+2))\,i+3((4(2x)(3y)+(2x)))\,j \\ ∇\,f(\frac{1}{2},\frac{1}{3}) & =(36 (\frac{1}{3})^{2} + 6 (\frac{1}{3}) + 4)\,i+(72 (\frac{1}{2}) (\frac{1}{3}) + 6 (\frac{1}{2}))\,j \\  & =(10)\,i+(15)\,j \\  & =⟨10,15⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(\frac{1}{2},\frac{1}{3})\cdot ⟨x-(\frac{1}{2}),\,y-(\frac{1}{3})⟩ & =0 \\ ⟨10,15⟩\cdot ⟨x-(\frac{1}{2}),\,y-(\frac{1}{3})⟩ & =0\end{aligned}
$$

### Generated authored safe bank q-72377 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=- 3 x y^{2} + 4 x y + 3 x$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(-1,-2).$

- [ ] $⟨-16,-17⟩\cdot ⟨x + 1,\,y + 2⟩=0$
- [x] $⟨-17,-16⟩\cdot ⟨x + 1,\,y + 2⟩=0$ **correct**
- [ ] $⟨17,-16⟩\cdot ⟨x + 1,\,y + 2⟩=0$
- [ ] $⟨-17,-16⟩\cdot ⟨x + 1,\,y - 2⟩=0$
- [ ] $⟨-17,-16⟩\cdot ⟨x - 1,\,y + 2⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(-1,-2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- 3 x y^{2} + 4 x y + 3 x)\,i+\frac{∂}{∂y}(- 3 x y^{2} + 4 x y + 3 x)\,j \\  & =(- 3 y^{2} + 4 y + 3)\,i+(- 6 x y + 4 x)\,j \\ ∇f(-1,-2) & =(- 3 (-2)^{2} + 4 (-2) + 3)\,i+(- 6 (-1) (-2) + 4 (-1))\,j \\  & =(-17)\,i+(-16)\,j \\  & =⟨-17,-16⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(-1,-2)\cdot ⟨x-(-1),\,y-(-2)⟩ & =0 \\ ⟨-17,-16⟩\cdot ⟨x + 1,\,y + 2⟩ & =0.\end{aligned}
$$

### Generated authored safe bank q-72377 — :question.difficulty/easy — observed family / authored bank

Given the function $f(x,y)=3 x y^{2} + 4 x y - 4 x$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(2,1).$

- [ ] $⟨-3,20⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [ ] $⟨3,20⟩\cdot ⟨x + 2,\,y - 1⟩=0$
- [ ] $⟨20,3⟩\cdot ⟨x - 2,\,y - 1⟩=0$
- [x] $⟨3,20⟩\cdot ⟨x - 2,\,y - 1⟩=0$ **correct**
- [ ] $⟨3,20⟩\cdot ⟨x - 2,\,y + 1⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(2,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x y^{2} + 4 x y - 4 x)\,i+\frac{∂}{∂y}(3 x y^{2} + 4 x y - 4 x)\,j \\  & =(3 y^{2} + 4 y - 4)\,i+(6 x y + 4 x)\,j \\ ∇f(2,1) & =(3 (1)^{2} + 4 (1) - 4)\,i+(6 (2) (1) + 4 (2))\,j \\  & =(3)\,i+(20)\,j \\  & =⟨3,20⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(2,1)\cdot ⟨x-(2),\,y-(1)⟩ & =0 \\ ⟨3,20⟩\cdot ⟨x - 2,\,y - 1⟩ & =0.\end{aligned}
$$

### Generated authored moderate — :question.difficulty/moderate — authored missing-level family

Given the function $f(x,y)=2 x^{2} + 2 x y^{2} + 3 y^{2}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(1,2).$

- [ ] $⟨20,12⟩\cdot ⟨x - 1,\,y - 2⟩=0$
- [x] $⟨12,20⟩\cdot ⟨x - 1,\,y - 2⟩=0$ **correct**
- [ ] $⟨-12,20⟩\cdot ⟨x - 1,\,y - 2⟩=0$
- [ ] $⟨12,20⟩\cdot ⟨x - 1,\,y + 2⟩=0$
- [ ] $⟨12,20⟩\cdot ⟨x + 1,\,y - 2⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(1,2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2 x^{2} + 2 x y^{2} + 3 y^{2})\,i+\frac{∂}{∂y}(2 x^{2} + 2 x y^{2} + 3 y^{2})\,j \\  & =(4 x + 2 y^{2})\,i+(4 x y + 6 y)\,j \\ ∇f(1,2) & =(4 (1) + 2 (2)^{2})\,i+(4 (1) (2) + 6 (2))\,j \\  & =(12)\,i+(20)\,j \\  & =⟨12,20⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(1,2)\cdot ⟨x-(1),\,y-(2)⟩ & =0 \\ ⟨12,20⟩\cdot ⟨x - 1,\,y - 2⟩ & =0.\end{aligned}
$$

### Generated authored moderate — :question.difficulty/moderate — authored missing-level family

Given the function $f(x,y)=5 x^{2} - 5 x y^{2} + 4 y^{2}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(2,3).$

- [ ] $⟨25,-36⟩\cdot ⟨x - 2,\,y - 3⟩=0$
- [ ] $⟨-25,-36⟩\cdot ⟨x + 2,\,y - 3⟩=0$
- [ ] $⟨-36,-25⟩\cdot ⟨x - 2,\,y - 3⟩=0$
- [x] $⟨-25,-36⟩\cdot ⟨x - 2,\,y - 3⟩=0$ **correct**
- [ ] $⟨-25,-36⟩\cdot ⟨x - 2,\,y + 3⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(2,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5 x^{2} - 5 x y^{2} + 4 y^{2})\,i+\frac{∂}{∂y}(5 x^{2} - 5 x y^{2} + 4 y^{2})\,j \\  & =(10 x - 5 y^{2})\,i+(- 10 x y + 8 y)\,j \\ ∇f(2,3) & =(10 (2) - 5 (3)^{2})\,i+(- 10 (2) (3) + 8 (3))\,j \\  & =(-25)\,i+(-36)\,j \\  & =⟨-25,-36⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(2,3)\cdot ⟨x-(2),\,y-(3)⟩ & =0 \\ ⟨-25,-36⟩\cdot ⟨x - 2,\,y - 3⟩ & =0.\end{aligned}
$$

### Generated authored hard — :question.difficulty/hard — authored missing-level family

Given the function $f(x,y)=2 x^{2} + 2 x y^{2} + 3 y^{2}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(\frac{5}{3},- \frac{1}{3}).$

- [ ] $⟨- \frac{38}{9},\frac{62}{9}⟩\cdot ⟨x - \frac{5}{3},\,y + \frac{1}{3}⟩=0$
- [x] $⟨\frac{62}{9},- \frac{38}{9}⟩\cdot ⟨x - \frac{5}{3},\,y + \frac{1}{3}⟩=0$ **correct**
- [ ] $⟨- \frac{62}{9},- \frac{38}{9}⟩\cdot ⟨x - \frac{5}{3},\,y + \frac{1}{3}⟩=0$
- [ ] $⟨\frac{62}{9},- \frac{38}{9}⟩\cdot ⟨x - \frac{5}{3},\,y - \frac{1}{3}⟩=0$
- [ ] $⟨\frac{62}{9},- \frac{38}{9}⟩\cdot ⟨x + \frac{5}{3},\,y + \frac{1}{3}⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(\frac{5}{3},- \frac{1}{3}):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2 x^{2} + 2 x y^{2} + 3 y^{2})\,i+\frac{∂}{∂y}(2 x^{2} + 2 x y^{2} + 3 y^{2})\,j \\  & =(4 x + 2 y^{2})\,i+(4 x y + 6 y)\,j \\ ∇f(\frac{5}{3},- \frac{1}{3}) & =(4 (\frac{5}{3}) + 2 (- \frac{1}{3})^{2})\,i+(4 (\frac{5}{3}) (- \frac{1}{3}) + 6 (- \frac{1}{3}))\,j \\  & =(\frac{62}{9})\,i+(- \frac{38}{9})\,j \\  & =⟨\frac{62}{9},- \frac{38}{9}⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(\frac{5}{3},- \frac{1}{3})\cdot ⟨x-(\frac{5}{3}),\,y-(- \frac{1}{3})⟩ & =0 \\ ⟨\frac{62}{9},- \frac{38}{9}⟩\cdot ⟨x - \frac{5}{3},\,y + \frac{1}{3}⟩ & =0.\end{aligned}
$$

### Generated authored hard — :question.difficulty/hard — authored missing-level family

Given the function $f(x,y)=5 x^{2} - 5 x y^{2} + 4 y^{2}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=(\frac{5}{3},\frac{2}{3}).$

- [ ] $⟨- \frac{130}{9},- \frac{52}{9}⟩\cdot ⟨x - \frac{5}{3},\,y - \frac{2}{3}⟩=0$
- [ ] $⟨\frac{130}{9},- \frac{52}{9}⟩\cdot ⟨x + \frac{5}{3},\,y - \frac{2}{3}⟩=0$
- [ ] $⟨- \frac{52}{9},\frac{130}{9}⟩\cdot ⟨x - \frac{5}{3},\,y - \frac{2}{3}⟩=0$
- [x] $⟨\frac{130}{9},- \frac{52}{9}⟩\cdot ⟨x - \frac{5}{3},\,y - \frac{2}{3}⟩=0$ **correct**
- [ ] $⟨\frac{130}{9},- \frac{52}{9}⟩\cdot ⟨x - \frac{5}{3},\,y + \frac{2}{3}⟩=0$

The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as

$$
∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.
$$

First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=(\frac{5}{3},\frac{2}{3}):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5 x^{2} - 5 x y^{2} + 4 y^{2})\,i+\frac{∂}{∂y}(5 x^{2} - 5 x y^{2} + 4 y^{2})\,j \\  & =(10 x - 5 y^{2})\,i+(- 10 x y + 8 y)\,j \\ ∇f(\frac{5}{3},\frac{2}{3}) & =(10 (\frac{5}{3}) - 5 (\frac{2}{3})^{2})\,i+(- 10 (\frac{5}{3}) (\frac{2}{3}) + 8 (\frac{2}{3}))\,j \\  & =(\frac{130}{9})\,i+(- \frac{52}{9})\,j \\  & =⟨\frac{130}{9},- \frac{52}{9}⟩\end{aligned}
$$

Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as

$$
\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ ∇f(\frac{5}{3},\frac{2}{3})\cdot ⟨x-(\frac{5}{3}),\,y-(\frac{2}{3})⟩ & =0 \\ ⟨\frac{130}{9},- \frac{52}{9}⟩\cdot ⟨x - \frac{5}{3},\,y - \frac{2}{3}⟩ & =0.\end{aligned}
$$

