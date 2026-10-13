# Tangent-vector review

Raw originals retain source errors and missing keys. Completions and opaque variants remain evidence only. The six authored examples are eligible complete method banks.

## Original raw q-36391

### q-36391 — unrated — observed evidence replay

Evidence only: True; profile: `raw:q-36391`

Consider the plane curve $x^{2}y = xy + 4$. Find a tangent vector to that curve at the point $(2, 2)$.

Field `selection` (:answer-field.type/radio):

- $6i + 2j$
- $2i - 6j$
- $6i$
- $6i - j$
- $3i + 2j$

[Worked solution absent in raw source.]

## Minimal supported completion q-36391

### q-36391 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-36391`

Consider the plane curve $x^{2}y = xy + 4$. Find a tangent vector to that curve at the point $(2, 2)$.

Field `selection` (:answer-field.type/radio):

- $6i + 2j$
- $2i - 6j$ ✓
- $6i$
- $6i - j$
- $3i + 2j$

First, if we set $f(x,y)=x^{2} y - x y,$ our curve can be viewed as the level curve $f(x,y)=4.$

A tangent vector to the level curve that passes through the point $(2,2)$ can be computed as follows:

$$
t(2,2)=f_y(2,2)i-f_x(2,2)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(2,2):$

$$
\begin{aligned}t(x,y)&=\frac{\partial}{\partial y}(x^{2} y - x y)\,i-\frac{\partial}{\partial x}(x^{2} y - x y)\,j \\ &=(x^{2} - x)\,i-(2 x y - y)\,j \\ t(2,2)&=(\left(2\right)^{2} - \left(2\right))\,i-(2 \left(2\right) \left(2\right) - \left(2\right))\,j \\ &=(2)\,i-(6)\,j \\ &=2\, i-6\, j\end{aligned}
$$

Therefore, our tangent vector is $2\, i-6\, j.$

## Changed-parameter observed-mask evidence q-36391

### q-36391 — unrated — observed evidence replay

Evidence only: True; profile: `raw:q-36391`

Consider the plane curve $x^{2}y = xy + 4$. Find a tangent vector to that curve at the point $(-1, 2)$.

Field `selection` (:answer-field.type/radio):

- $6i + 2j$
- $2\, i+6\, j$
- $6i$
- $6i - j$
- $3i + 2j$

[Worked solution absent in raw source.]

## Original raw q-65204

### q-65204 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-65204`

Consider the plane curve $\operatorname{cos}⁡x\operatorname{cos}⁡y=\operatorname{sin}⁡(xy).$ Find a tangent vector to that curve at the point $(0,\frac{\pi }{2}).$

Field `selection` (:answer-field.type/radio):

- $i + \frac{π}{2}j$
- $-\frac{π}{2}i + j$
- $-i - j$
- $-i + \frac{π}{2}j$
- $-\frac{π}{2}i - j$
Field `selection` (:answer-field.type/radio):

- $-i+\frac{\pi }{2}\,j$ ✓
- $i+\frac{\pi }{2}\,j$
- $-\frac{\pi }{2}\,i+j$
- $-i-j$
- $-\frac{\pi }{2}\,i-j$

First, we bring all variables to one side:

$$
\begin{aligned}\operatorname{cos}⁡x\operatorname{cos}⁡y & =\operatorname{sin}⁡xy \\ \operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy) & =0\end{aligned}
$$

If we set $f(x,y)=\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡xy$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(0,\frac{\pi }{2})$ can be computed as follows:

$$
t(0,\frac{\pi }{2})={f}_{y}(0,\frac{\pi }{2})i-{f}_{x}(0,\frac{\pi }{2})j
$$

So, we calculate $t(x,y)$ and evaluate it at $(0,\frac{\pi }{2}):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy))\,i-\frac{∂}{∂x}(\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy))\,j \\  & =(-\operatorname{cos}⁡x\operatorname{sin}⁡y-x\operatorname{cos}⁡(xy))i-(-\operatorname{sin}⁡x\operatorname{cos}⁡y-y\operatorname{cos}⁡(xy))\,j \\ t(0,\frac{\pi }{2}) & =(-\operatorname{cos}⁡(0)\operatorname{sin}⁡(\frac{\pi }{2})-0\operatorname{cos}⁡(0\cdot \frac{\pi }{2}))i-(-\operatorname{sin}⁡(0)\operatorname{cos}⁡(\frac{\pi }{2})-\frac{\pi }{2}\operatorname{cos}⁡(0\cdot \frac{\pi }{2}))j \\  & =-i+\frac{\pi }{2}\,j\end{aligned}
$$

Therefore, our tangent vector is $-i+\frac{\pi }{2}\,j.$

## Minimal supported completion q-65204

### q-65204 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-65204`

Consider the plane curve $\operatorname{cos}⁡x\operatorname{cos}⁡y=\operatorname{sin}⁡(xy).$ Find a tangent vector to that curve at the point $(0,\frac{\pi }{2}).$

Field `selection` (:answer-field.type/radio):

- $-i+\frac{\pi }{2}\,j$ ✓
- $i+\frac{\pi }{2}\,j$
- $-\frac{\pi }{2}\,i+j$
- $-i-j$
- $-\frac{\pi }{2}\,i-j$

First, we bring all variables to one side:

$$
\begin{aligned}\operatorname{cos}⁡x\operatorname{cos}⁡y & =\operatorname{sin}⁡xy \\ \operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy) & =0\end{aligned}
$$

If we set $f(x,y)=\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡xy$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(0,\frac{\pi }{2})$ can be computed as follows:

$$
t(0,\frac{\pi }{2})={f}_{y}(0,\frac{\pi }{2})i-{f}_{x}(0,\frac{\pi }{2})j
$$

So, we calculate $t(x,y)$ and evaluate it at $(0,\frac{\pi }{2}):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy))\,i-\frac{∂}{∂x}(\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy))\,j \\  & =(-\operatorname{cos}⁡x\operatorname{sin}⁡y-x\operatorname{cos}⁡(xy))i-(-\operatorname{sin}⁡x\operatorname{cos}⁡y-y\operatorname{cos}⁡(xy))\,j \\ t(0,\frac{\pi }{2}) & =(-\operatorname{cos}⁡(0)\operatorname{sin}⁡(\frac{\pi }{2})-0\operatorname{cos}⁡(0\cdot \frac{\pi }{2}))i-(-\operatorname{sin}⁡(0)\operatorname{cos}⁡(\frac{\pi }{2})-\frac{\pi }{2}\operatorname{cos}⁡(0\cdot \frac{\pi }{2}))j \\  & =-i+\frac{\pi }{2}\,j\end{aligned}
$$

Therefore, our tangent vector is $-i+\frac{\pi }{2}\,j.$

## Changed-parameter observed-mask evidence q-65204

### q-65204 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-65204`

Consider the plane curve $\operatorname{cos}⁡x\operatorname{cos}⁡y=\operatorname{sin}⁡(xy).$ Find a tangent vector to that curve at the point $(0,- \frac{\pi}{2}).$

Field `selection` (:answer-field.type/radio):

- $i + \frac{π}{2}j$
- $-\frac{π}{2}i + j$
- $-i - j$
- $i-\frac{\pi}{2}\, j$
- $-\frac{π}{2}i - j$
Field `selection` (:answer-field.type/radio):

- $i-\frac{\pi}{2}\, j$ ✓
- $i+\frac{\pi }{2}\,j$
- $-\frac{\pi }{2}\,i+j$
- $-i-j$
- $-\frac{\pi }{2}\,i-j$

First, we bring all variables to one side:

$$
\begin{aligned}\operatorname{cos}⁡x\operatorname{cos}⁡y & =\operatorname{sin}⁡xy \\ \operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy) & =0\end{aligned}
$$

If we set $f(x,y)=\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡xy$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(0,- \frac{\pi}{2})$ can be computed as follows:

$$
t(0,- \frac{\pi}{2})={f}_{y}(0,- \frac{\pi}{2})i-{f}_{x}(0,- \frac{\pi}{2})j
$$

So, we calculate $t(x,y)$ and evaluate it at $(0,- \frac{\pi}{2}):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy))\,i-\frac{∂}{∂x}(\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{sin}⁡(xy))\,j \\  & =(-\operatorname{cos}⁡x\operatorname{sin}⁡y-x\operatorname{cos}⁡(xy))i-(-\operatorname{sin}⁡x\operatorname{cos}⁡y-y\operatorname{cos}⁡(xy))\,j \\ t(0,- \frac{\pi}{2}) & =(-\operatorname{cos}⁡(0)\operatorname{sin}⁡((- \frac{\pi}{2}))-0\operatorname{cos}⁡(0\cdot (- \frac{\pi}{2})))i-(-\operatorname{sin}⁡(0)\operatorname{cos}⁡((- \frac{\pi}{2}))-(- \frac{\pi}{2})\operatorname{cos}⁡(0\cdot (- \frac{\pi}{2})))j \\  & =i-\frac{\pi}{2}\, j\end{aligned}
$$

Therefore, our tangent vector is $i-\frac{\pi}{2}\, j.$

## Original raw q-130198

### q-130198 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130198`

Consider the plane curve $x\operatorname{cos}⁡y=-y\operatorname{sin}⁡x+\frac{\pi }{2}.$ Find a tangent vector to that curve at the point $(\frac{\pi }{2},0).$

Field `selection` (:answer-field.type/radio):

- $i-j$ ✓
- $-2\,i+j$
- $\frac{\pi }{2}\,i+j$
- $-i-\frac{\pi }{2}\,j$
- $i+2\,j$

First, we bring all variables to one side:

$$
\begin{aligned}x\operatorname{cos}⁡y & =-y\operatorname{sin}⁡x+\frac{\pi }{2} \\ x\operatorname{cos}⁡y+y\operatorname{sin}⁡x & =\frac{\pi }{2}\end{aligned}
$$

If we set $f(x,y)=x\operatorname{cos}⁡y+y\operatorname{sin}⁡x,$ our curve can be viewed as the level curve $f(x,y)=\frac{\pi }{2}.$ 

A tangent vector to the level curve that passes through the point $(\frac{\pi }{2},0)$ can be computed as follows:

$$
t(\frac{\pi }{2},0)={f}_{y}(\frac{\pi }{2},0)i-{f}_{x}(\frac{\pi }{2},0)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(\frac{\pi }{2},0):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x\operatorname{cos}⁡y+y\operatorname{sin}⁡x)i-\frac{∂}{∂x}(x\operatorname{cos}⁡y+y\operatorname{sin}⁡x)j \\  & =(-x\operatorname{sin}⁡y+\operatorname{sin}⁡x)i-(\operatorname{cos}⁡y+y\operatorname{cos}⁡x)j \\ t(\frac{\pi }{2},0) & =(-\frac{\pi }{2}\operatorname{sin}⁡0+\operatorname{sin}⁡(\frac{\pi }{2}))i-(\operatorname{cos}⁡0+0\operatorname{cos}⁡(\frac{\pi }{2}))j \\  & =i-j\end{aligned}
$$

Therefore, our tangent vector is $i-j.$

## Minimal supported completion q-130198

### q-130198 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-130198`

Consider the plane curve $x\operatorname{cos}⁡y=-y\operatorname{sin}⁡x+\frac{\pi }{2}.$ Find a tangent vector to that curve at the point $(\frac{\pi }{2},0).$

Field `selection` (:answer-field.type/radio):

- $i-j$ ✓
- $-2\,i+j$
- $\frac{\pi }{2}\,i+j$
- $-i-\frac{\pi }{2}\,j$
- $i+2\,j$

First, we bring all variables to one side:

$$
\begin{aligned}x\operatorname{cos}⁡y & =-y\operatorname{sin}⁡x+\frac{\pi }{2} \\ x\operatorname{cos}⁡y+y\operatorname{sin}⁡x & =\frac{\pi }{2}\end{aligned}
$$

If we set $f(x,y)=x\operatorname{cos}⁡y+y\operatorname{sin}⁡x,$ our curve can be viewed as the level curve $f(x,y)=\frac{\pi }{2}.$ 

A tangent vector to the level curve that passes through the point $(\frac{\pi }{2},0)$ can be computed as follows:

$$
t(\frac{\pi }{2},0)={f}_{y}(\frac{\pi }{2},0)i-{f}_{x}(\frac{\pi }{2},0)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(\frac{\pi }{2},0):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x\operatorname{cos}⁡y+y\operatorname{sin}⁡x)i-\frac{∂}{∂x}(x\operatorname{cos}⁡y+y\operatorname{sin}⁡x)j \\  & =(-x\operatorname{sin}⁡y+\operatorname{sin}⁡x)i-(\operatorname{cos}⁡y+y\operatorname{cos}⁡x)j \\ t(\frac{\pi }{2},0) & =(-\frac{\pi }{2}\operatorname{sin}⁡0+\operatorname{sin}⁡(\frac{\pi }{2}))i-(\operatorname{cos}⁡0+0\operatorname{cos}⁡(\frac{\pi }{2}))j \\  & =i-j\end{aligned}
$$

Therefore, our tangent vector is $i-j.$

## Changed-parameter observed-mask evidence q-130198

### q-130198 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130198`

Consider the plane curve $x\operatorname{cos}⁡y=-y\operatorname{sin}⁡x+\left(- \frac{\pi}{2}\right).$ Find a tangent vector to that curve at the point $(- \frac{\pi}{2},0).$

Field `selection` (:answer-field.type/radio):

- $-i-j$ ✓
- $-2\,i+j$
- $\frac{\pi }{2}\,i+j$
- $-i-\frac{\pi }{2}\,j$
- $i+2\,j$

First, we bring all variables to one side:

$$
\begin{aligned}x\operatorname{cos}⁡y & =-y\operatorname{sin}⁡x+\left(- \frac{\pi}{2}\right) \\ x\operatorname{cos}⁡y+y\operatorname{sin}⁡x & =\left(- \frac{\pi}{2}\right)\end{aligned}
$$

If we set $f(x,y)=x\operatorname{cos}⁡y+y\operatorname{sin}⁡x,$ our curve can be viewed as the level curve $f(x,y)=\left(- \frac{\pi}{2}\right).$ 

A tangent vector to the level curve that passes through the point $(- \frac{\pi}{2},0)$ can be computed as follows:

$$
t(- \frac{\pi}{2},0)={f}_{y}(- \frac{\pi}{2},0)i-{f}_{x}(- \frac{\pi}{2},0)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(- \frac{\pi}{2},0):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x\operatorname{cos}⁡y+y\operatorname{sin}⁡x)i-\frac{∂}{∂x}(x\operatorname{cos}⁡y+y\operatorname{sin}⁡x)j \\  & =(-x\operatorname{sin}⁡y+\operatorname{sin}⁡x)i-(\operatorname{cos}⁡y+y\operatorname{cos}⁡x)j \\ t(- \frac{\pi}{2},0) & =(-(- \frac{\pi}{2})\operatorname{sin}⁡0+\operatorname{sin}⁡((- \frac{\pi}{2})))i-(\operatorname{cos}⁡0+0\operatorname{cos}⁡((- \frac{\pi}{2})))j \\  & =-i-j\end{aligned}
$$

Therefore, our tangent vector is $-i-j.$

## Original raw q-130200

### q-130200 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130200`

Consider the plane curve $x{e}^{{y}^{2}+1}=e-y.$ Find a tangent vector to that curve at the point $(1,0).$

Field `selection` (:answer-field.type/radio):

- $i+{e}^{2}\,j$
- $i-e\,j$ ✓
- $2\,i$
- $-j$
- $2e\,i+j$

First, we bring all variables to one side:

$$
\begin{aligned}x{e}^{{y}^{2}+1} & =e-y \\ x{e}^{{y}^{2}+1}+y & =e\end{aligned}
$$

If we set $f(x,y)=x{e}^{{y}^{2}+1}+y,$ our curve can be viewed as the level curve $f(x,y)=e.$ 

A tangent vector to the level curve that passes through the point $(1,0)$ can be computed as follows:

$$
t(1,0)={f}_{y}(1,0)i-{f}_{x}(1,0)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,0):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x{e}^{{y}^{2}+1}+y)i-\frac{∂}{∂x}(x{e}^{{y}^{2}+1}+y)j \\  & =(2xy{e}^{{y}^{2}+1}+1)i-{e}^{{y}^{2}+1}\,j \\ t(1,0) & =(2(1)(0){e}^{0+1}+1)i-{e}^{0+1}\,j \\  & =i-e\,j\end{aligned}
$$

Therefore, our tangent vector is $i-e\,j.$

## Minimal supported completion q-130200

### q-130200 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-130200`

Consider the plane curve $x{e}^{{y}^{2}+1}=e-y.$ Find a tangent vector to that curve at the point $(1,0).$

Field `selection` (:answer-field.type/radio):

- $i+{e}^{2}\,j$
- $i-e\,j$ ✓
- $2\,i$
- $-j$
- $2e\,i+j$

First, we bring all variables to one side:

$$
\begin{aligned}x{e}^{{y}^{2}+1} & =e-y \\ x{e}^{{y}^{2}+1}+y & =e\end{aligned}
$$

If we set $f(x,y)=x{e}^{{y}^{2}+1}+y,$ our curve can be viewed as the level curve $f(x,y)=e.$ 

A tangent vector to the level curve that passes through the point $(1,0)$ can be computed as follows:

$$
t(1,0)={f}_{y}(1,0)i-{f}_{x}(1,0)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,0):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x{e}^{{y}^{2}+1}+y)i-\frac{∂}{∂x}(x{e}^{{y}^{2}+1}+y)j \\  & =(2xy{e}^{{y}^{2}+1}+1)i-{e}^{{y}^{2}+1}\,j \\ t(1,0) & =(2(1)(0){e}^{0+1}+1)i-{e}^{0+1}\,j \\  & =i-e\,j\end{aligned}
$$

Therefore, our tangent vector is $i-e\,j.$

## Changed-parameter observed-mask evidence q-130200

### q-130200 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130200`

Consider the plane curve $x{e}^{{y}^{2}+1}=\left(- e\right)-y.$ Find a tangent vector to that curve at the point $(-1,0).$

Field `selection` (:answer-field.type/radio):

- $i+{e}^{2}\,j$
- $i-e\,j$ ✓
- $2\,i$
- $-j$
- $2e\,i+j$

First, we bring all variables to one side:

$$
\begin{aligned}x{e}^{{y}^{2}+1} & =\left(- e\right)-y \\ x{e}^{{y}^{2}+1}+y & =\left(- e\right)\end{aligned}
$$

If we set $f(x,y)=x{e}^{{y}^{2}+1}+y,$ our curve can be viewed as the level curve $f(x,y)=\left(- e\right).$ 

A tangent vector to the level curve that passes through the point $(-1,0)$ can be computed as follows:

$$
t(-1,0)={f}_{y}(-1,0)i-{f}_{x}(-1,0)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,0):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x{e}^{{y}^{2}+1}+y)i-\frac{∂}{∂x}(x{e}^{{y}^{2}+1}+y)j \\  & =(2xy{e}^{{y}^{2}+1}+1)i-{e}^{{y}^{2}+1}\,j \\ t(-1,0) & =(2((-1))(0){e}^{0+1}+1)i-{e}^{0+1}\,j \\  & =i-e\,j\end{aligned}
$$

Therefore, our tangent vector is $i-e\,j.$

## Original raw q-37516

### q-37516 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-37516`

Consider the plane curve $2x\operatorname{ln}⁡y=8xy+2-8e.$ Find a tangent vector to that curve at the point $(1,e).$

Field `selection` (:answer-field.type/radio):

- $(2e-8)\,i+(\frac{e}{2}-8)j$
- $(1-4e)\,i+(\frac{2}{e}-8)j$
- $(2-8e)\,i+(2-8e)j$
- $(\frac{2}{e}-8)i+(8e-2)\,j$ ✓
- $(8-2e)\,i+(\frac{8}{e}-2)j$

First, we bring all variables to one side:

$$
\begin{aligned}2x\operatorname{ln}⁡y & =8xy+2-8e \\ 2x\operatorname{ln}⁡y-8xy & =2-8e\end{aligned}
$$

If we set $f(x,y)=2x\operatorname{ln}⁡y-8xy$, our curve can be viewed as the level curve $f(x,y)=2-8e.$ 

A tangent vector to the level curve that passes through the point $(1,e)$ can be computed as follows:

$$
t(1,e)={f}_{y}(1,e)\,i-{f}_{x}(1,e)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,e):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(2x\operatorname{ln}⁡y-8xy)\,i-\frac{∂}{∂x}(2x\operatorname{ln}⁡y-8xy)\,j \\  & =(\frac{2x}{y}-8x)i-(2\operatorname{ln}⁡y-8y)\,j \\ t(1,e) & =(\frac{2(1)}{e}-8(1))i-(2\operatorname{ln}⁡e-8(e))\,j \\  & =(\frac{2}{e}-8)i+(8e-2)j\end{aligned}
$$

  

Therefore, our tangent vector is $(\frac{2}{e}-8)i+(8e-2)\,j.$

## Minimal supported completion q-37516

### q-37516 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-37516`

Consider the plane curve $2x\operatorname{ln}⁡y=8xy+2-8e.$ Find a tangent vector to that curve at the point $(1,e).$

Field `selection` (:answer-field.type/radio):

- $(2e-8)\,i+(\frac{e}{2}-8)j$
- $(1-4e)\,i+(\frac{2}{e}-8)j$
- $(2-8e)\,i+(2-8e)j$
- $(\frac{2}{e}-8)i+(8e-2)\,j$ ✓
- $(8-2e)\,i+(\frac{8}{e}-2)j$

First, we bring all variables to one side:

$$
\begin{aligned}2x\operatorname{ln}⁡y & =8xy+2-8e \\ 2x\operatorname{ln}⁡y-8xy & =2-8e\end{aligned}
$$

If we set $f(x,y)=2x\operatorname{ln}⁡y-8xy$, our curve can be viewed as the level curve $f(x,y)=2-8e.$ 

A tangent vector to the level curve that passes through the point $(1,e)$ can be computed as follows:

$$
t(1,e)={f}_{y}(1,e)\,i-{f}_{x}(1,e)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,e):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(2x\operatorname{ln}⁡y-8xy)\,i-\frac{∂}{∂x}(2x\operatorname{ln}⁡y-8xy)\,j \\  & =(\frac{2x}{y}-8x)i-(2\operatorname{ln}⁡y-8y)\,j \\ t(1,e) & =(\frac{2(1)}{e}-8(1))i-(2\operatorname{ln}⁡e-8(e))\,j \\  & =(\frac{2}{e}-8)i+(8e-2)j\end{aligned}
$$

  

Therefore, our tangent vector is $(\frac{2}{e}-8)i+(8e-2)\,j.$

## Changed-parameter observed-mask evidence q-37516

### q-37516 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-37516`

Consider the plane curve $2x\operatorname{ln}⁡y=8xy+\left(-2 + 8 e\right).$ Find a tangent vector to that curve at the point $(-1,e).$

Field `selection` (:answer-field.type/radio):

- $(2e-8)\,i+(\frac{e}{2}-8)j$
- $(1-4e)\,i+(\frac{2}{e}-8)j$
- $(2-8e)\,i+(2-8e)j$
- $\left(8 - \frac{2}{e}\right)\, i-\left(2 - 8 e\right)\, j$ ✓
- $(8-2e)\,i+(\frac{8}{e}-2)j$

First, we bring all variables to one side:

$$
\begin{aligned}2x\operatorname{ln}⁡y & =8xy+\left(-2 + 8 e\right) \\ 2x\operatorname{ln}⁡y-8xy & =\left(-2 + 8 e\right)\end{aligned}
$$

If we set $f(x,y)=2x\operatorname{ln}⁡y-8xy$, our curve can be viewed as the level curve $f(x,y)=\left(-2 + 8 e\right).$ 

A tangent vector to the level curve that passes through the point $(-1,e)$ can be computed as follows:

$$
t(-1,e)={f}_{y}(-1,e)\,i-{f}_{x}(-1,e)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,e):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(2x\operatorname{ln}⁡y-8xy)\,i-\frac{∂}{∂x}(2x\operatorname{ln}⁡y-8xy)\,j \\  & =(\frac{2x}{y}-8x)i-(2\operatorname{ln}⁡y-8y)\,j \\ t(-1,e) & =(\frac{2((-1))}{e}-8((-1)))i-(2\operatorname{ln}⁡e-8(e))\,j \\  & =\left(8 - \frac{2}{e}\right)\, i-\left(2 - 8 e\right)\, j\end{aligned}
$$

  

Therefore, our tangent vector is $\left(8 - \frac{2}{e}\right)\, i-\left(2 - 8 e\right)\, j.$

## Original raw q-72400

### q-72400 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-72400`

Consider the plane curve ${x}^{2}+{y}^{2}=2xy+9.$ Find a tangent vector to that curve at the point $(-1,2).$

Field `selection` (:answer-field.type/radio):

- $6\,i+6\,j$ ✓
- $i-j$
- $2\,i-j$
- $i+6\,j$
- $2\,i-6\,j$

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}+{y}^{2} & =2xy+9 \\ {x}^{2}+{y}^{2}-2xy-9 & =0\end{aligned}
$$

If we set $f(x,y)={x}^{2}+{y}^{2}-2xy-9$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(-1,2)$ can be computed as follows:

$$
t(-1,2)={f}_{y}(-1,2)\,i-{f}_{x}(-1,2)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,2):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}+{y}^{2}-2xy-9)\,i-\frac{∂}{∂x}({x}^{2}+{y}^{2}-2xy-9)\,j \\  & =(2y-2x)\,i-(2x-2y)\,j \\ t(-1,2) & =(2(2)-2(-1))\,i-(2(-1)-2(2))\,j \\  & =6\,i+6\,j\end{aligned}
$$

Therefore, our tangent vector is $6\,i+6\,j.$

## Minimal supported completion q-72400

### q-72400 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-72400`

Consider the plane curve ${x}^{2}+{y}^{2}=2xy+9.$ Find a tangent vector to that curve at the point $(-1,2).$

Field `selection` (:answer-field.type/radio):

- $6\,i+6\,j$ ✓
- $i-j$
- $2\,i-j$
- $i+6\,j$
- $2\,i-6\,j$

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}+{y}^{2} & =2xy+9 \\ {x}^{2}+{y}^{2}-2xy-9 & =0\end{aligned}
$$

If we set $f(x,y)={x}^{2}+{y}^{2}-2xy-9$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(-1,2)$ can be computed as follows:

$$
t(-1,2)={f}_{y}(-1,2)\,i-{f}_{x}(-1,2)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,2):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}+{y}^{2}-2xy-9)\,i-\frac{∂}{∂x}({x}^{2}+{y}^{2}-2xy-9)\,j \\  & =(2y-2x)\,i-(2x-2y)\,j \\ t(-1,2) & =(2(2)-2(-1))\,i-(2(-1)-2(2))\,j \\  & =6\,i+6\,j\end{aligned}
$$

Therefore, our tangent vector is $6\,i+6\,j.$

## Changed-parameter observed-mask evidence q-72400

### q-72400 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-72400`

Consider the plane curve ${x}^{2}+{y}^{2}=2xy+9.$ Find a tangent vector to that curve at the point $(-2,1).$

Field `selection` (:answer-field.type/radio):

- $6\,i+6\,j$ ✓
- $i-j$
- $2\,i-j$
- $i+6\,j$
- $2\,i-6\,j$

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}+{y}^{2} & =2xy+9 \\ {x}^{2}+{y}^{2}-2xy-9 & =0\end{aligned}
$$

If we set $f(x,y)={x}^{2}+{y}^{2}-2xy-9$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(-2,1)$ can be computed as follows:

$$
t(-2,1)={f}_{y}(-2,1)\,i-{f}_{x}(-2,1)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-2,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}+{y}^{2}-2xy-9)\,i-\frac{∂}{∂x}({x}^{2}+{y}^{2}-2xy-9)\,j \\  & =(2y-2x)\,i-(2x-2y)\,j \\ t(-2,1) & =(2((1))-2((-2)))\,i-(2((-2))-2((1)))\,j \\  & =6\,i+6\,j\end{aligned}
$$

Therefore, our tangent vector is $6\,i+6\,j.$

## Original raw q-72463

### q-72463 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-72463`

Consider the plane curve $2{x}^{3}{y}^{2}-4xy=1-3x.$ Find a tangent vector to that curve at the point $(1,1).$

Field `selection` (:answer-field.type/radio):

- $5\,i-5\,j$
- $i$
- $i+5\,j$
- $5\,i-j$
- $-5\,j$ ✓

First, we bring all variables to one side:

$$
\begin{aligned}2{x}^{3}{y}^{2}-4xy & =1-3x \\ 2{x}^{3}{y}^{2}-4xy+3x & =1\end{aligned}
$$

If we set $f(x,y)=2{x}^{3}{y}^{2}-4xy+3x$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(1,1)$ can be computed as follows:

$$
t(1,1)={f}_{y}(1,1)i-{f}_{x}(1,1)j
$$

 

So, we calculate $t(x,y)$ and evaluate it at $(1,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(2{x}^{3}{y}^{2}-4xy+3x)i-\frac{∂}{∂x}(2{x}^{3}{y}^{2}-4xy+3x)j \\  & =(4y{x}^{3}-4x)i-(6{x}^{2}{y}^{2}-4y+3)j \\ t(1,1) & =(4(1)(1)^{3}-4(1))i-(6(1)^{2}(1)^{2}-4(1)+3)j \\  & =-5\,j\end{aligned}
$$

Therefore, our tangent vector is $-5\,j.$

## Minimal supported completion q-72463

### q-72463 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-72463`

Consider the plane curve $2{x}^{3}{y}^{2}-4xy=1-3x.$ Find a tangent vector to that curve at the point $(1,1).$

Field `selection` (:answer-field.type/radio):

- $5\,i-5\,j$
- $i$
- $i+5\,j$
- $5\,i-j$
- $-5\,j$ ✓

First, we bring all variables to one side:

$$
\begin{aligned}2{x}^{3}{y}^{2}-4xy & =1-3x \\ 2{x}^{3}{y}^{2}-4xy+3x & =1\end{aligned}
$$

If we set $f(x,y)=2{x}^{3}{y}^{2}-4xy+3x$, our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve that passes through the point $(1,1)$ can be computed as follows:

$$
t(1,1)={f}_{y}(1,1)i-{f}_{x}(1,1)j
$$

 

So, we calculate $t(x,y)$ and evaluate it at $(1,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(2{x}^{3}{y}^{2}-4xy+3x)i-\frac{∂}{∂x}(2{x}^{3}{y}^{2}-4xy+3x)j \\  & =(4y{x}^{3}-4x)i-(6{x}^{2}{y}^{2}-4y+3)j \\ t(1,1) & =(4(1)(1)^{3}-4(1))i-(6(1)^{2}(1)^{2}-4(1)+3)j \\  & =-5\,j\end{aligned}
$$

Therefore, our tangent vector is $-5\,j.$

## Changed-parameter observed-mask evidence q-72463

### q-72463 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-72463`

Consider the plane curve $2{x}^{3}{y}^{2}-4xy=\left(-1\right)-3x.$ Find a tangent vector to that curve at the point $(-1,1).$

Field `selection` (:answer-field.type/radio):

- $5\,i-5\,j$
- $i$
- $i+5\,j$
- $5\,i-j$
- $-5\,j$ ✓

First, we bring all variables to one side:

$$
\begin{aligned}2{x}^{3}{y}^{2}-4xy & =\left(-1\right)-3x \\ 2{x}^{3}{y}^{2}-4xy+3x & =\left(-1\right)\end{aligned}
$$

If we set $f(x,y)=2{x}^{3}{y}^{2}-4xy+3x$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(-1,1)$ can be computed as follows:

$$
t(-1,1)={f}_{y}(-1,1)i-{f}_{x}(-1,1)j
$$

 

So, we calculate $t(x,y)$ and evaluate it at $(-1,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(2{x}^{3}{y}^{2}-4xy+3x)i-\frac{∂}{∂x}(2{x}^{3}{y}^{2}-4xy+3x)j \\  & =(4y{x}^{3}-4x)i-(6{x}^{2}{y}^{2}-4y+3)j \\ t(-1,1) & =(4(1)((-1))^{3}-4((-1)))i-(6((-1))^{2}(1)^{2}-4(1)+3)j \\  & =-5\,j\end{aligned}
$$

Therefore, our tangent vector is $-5\,j.$

## Original raw q-130201

### q-130201 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130201`

Consider the plane curve $xy=3-{x}^{2}-{y}^{3}.$ Find a tangent vector to that curve at the point $(-1,-1).$

Field `selection` (:answer-field.type/radio):

- $3\,j$
- $i-2\,j$
- $3\,i-2\,j$
- $-2\,i$
- $2\,i+3\,j$ ✓

First, we bring all variables to one side:

$$
\begin{aligned}xy & =3-{x}^{2}-{y}^{3} \\ xy+{x}^{2}+{y}^{3} & =3\end{aligned}
$$

If we set $f(x,y)=xy+{x}^{2}+{y}^{3},$ our curve can be viewed as the level curve $f(x,y)=3.$ 

A tangent vector to the level curve that passes through the point $(-1,-1)$ can be computed as follows:

$$
t(-1,-1)={f}_{y}(-1,-1)i-{f}_{x}(-1,-1)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,-1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(xy+{x}^{2}+{y}^{3})i-\frac{∂}{∂x}(xy+{x}^{2}+{y}^{3})j \\  & =(x+3{y}^{2})i-(y+2x)j \\ t(-1,-1) & =(-1+3(-1)^{2})i-(-1+2(-1))j \\  & =2\,i+3\,j\end{aligned}
$$

Therefore, our tangent vector is $2\,i+3\,j.$

## Minimal supported completion q-130201

### q-130201 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-130201`

Consider the plane curve $xy=1-{x}^{2}-{y}^{3}.$ Find a tangent vector to that curve at the point $(-1,-1).$

Field `selection` (:answer-field.type/radio):

- $3\,j$
- $i-2\,j$
- $3\,i-2\,j$
- $-2\,i$
- $2\,i+3\,j$ ✓

First, we bring all variables to one side:

$$
\begin{aligned}xy & =1-{x}^{2}-{y}^{3} \\ xy+{x}^{2}+{y}^{3} & =1\end{aligned}
$$

If we set $f(x,y)=xy+{x}^{2}+{y}^{3},$ our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve that passes through the point $(-1,-1)$ can be computed as follows:

$$
t(-1,-1)={f}_{y}(-1,-1)i-{f}_{x}(-1,-1)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,-1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(xy+{x}^{2}+{y}^{3})i-\frac{∂}{∂x}(xy+{x}^{2}+{y}^{3})j \\  & =(x+3{y}^{2})i-(y+2x)j \\ t(-1,-1) & =(-1+3(-1)^{2})i-(-1+2(-1))j \\  & =2\,i+3\,j\end{aligned}
$$

Therefore, our tangent vector is $2\,i+3\,j.$

## Changed-parameter observed-mask evidence q-130201

### q-130201 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130201`

Consider the plane curve $xy=\left(1\right)-{x}^{2}-{y}^{3}.$ Find a tangent vector to that curve at the point $(1,-1).$

Field `selection` (:answer-field.type/radio):

- $3\,j$
- $i-2\,j$
- $3\,i-2\,j$
- $-2\,i$
- $4\, i-j$ ✓

First, we bring all variables to one side:

$$
\begin{aligned}xy & =\left(1\right)-{x}^{2}-{y}^{3} \\ xy+{x}^{2}+{y}^{3} & =\left(1\right)\end{aligned}
$$

If we set $f(x,y)=xy+{x}^{2}+{y}^{3},$ our curve can be viewed as the level curve $f(x,y)=\left(1\right).$ 

A tangent vector to the level curve that passes through the point $(1,-1)$ can be computed as follows:

$$
t(1,-1)={f}_{y}(1,-1)i-{f}_{x}(1,-1)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,-1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(xy+{x}^{2}+{y}^{3})i-\frac{∂}{∂x}(xy+{x}^{2}+{y}^{3})j \\  & =(x+3{y}^{2})i-(y+2x)j \\ t(1,-1) & =((1)+3(-1)^{2})i-(-1+2((1)))j \\  & =4\, i-j\end{aligned}
$$

Therefore, our tangent vector is $4\, i-j.$

## Original raw q-72388

### q-72388 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-72388`

Consider the plane curve $x+1={x}^{2}y.$ Find a tangent vector to that curve at the point $(1,2).$

Field `selection` (:answer-field.type/radio):

- $i-j$
- $i-3\,j$ ✓
- $3\,i-2\,j$
- $2\,i+j$
- $2\,i+3\,j$

First, we bring all variables to one side:

$$
\begin{aligned}x+1 & ={x}^{2}y \\ {x}^{2}y-x-1 & =0\end{aligned}
$$

If we set $f(x,y)={x}^{2}y-x-1$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(1,2)$ can be computed as follows:

$$
t(1,2)={f}_{y}(1,2)i-{f}_{x}(1,2)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,2):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}y-x-1)i-\frac{∂}{∂x}({x}^{2}y-x-1)j \\  & ={x}^{2}\,i-(2xy-1)j \\ t(1,2) & =(1)^{2}\,i-(2(1)(2)-1)j \\  & =i-3\,j\end{aligned}
$$

Therefore, our tangent vector is $i-3\,j.$

## Minimal supported completion q-72388

### q-72388 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-72388`

Consider the plane curve $x+1={x}^{2}y.$ Find a tangent vector to that curve at the point $(1,2).$

Field `selection` (:answer-field.type/radio):

- $i-j$
- $i-3\,j$ ✓
- $3\,i-2\,j$
- $2\,i+j$
- $2\,i+3\,j$

First, we bring all variables to one side:

$$
\begin{aligned}x+1 & ={x}^{2}y \\ {x}^{2}y-x-1 & =0\end{aligned}
$$

If we set $f(x,y)={x}^{2}y-x-1$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(1,2)$ can be computed as follows:

$$
t(1,2)={f}_{y}(1,2)i-{f}_{x}(1,2)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,2):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}y-x-1)i-\frac{∂}{∂x}({x}^{2}y-x-1)j \\  & ={x}^{2}\,i-(2xy-1)j \\ t(1,2) & =(1)^{2}\,i-(2(1)(2)-1)j \\  & =i-3\,j\end{aligned}
$$

Therefore, our tangent vector is $i-3\,j.$

## Changed-parameter observed-mask evidence q-72388

### q-72388 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-72388`

Consider the plane curve $x+\left(3\right)={x}^{2}y.$ Find a tangent vector to that curve at the point $(-1,2).$

Field `selection` (:answer-field.type/radio):

- $i-j$
- $i+5\, j$ ✓
- $3\,i-2\,j$
- $2\,i+j$
- $2\,i+3\,j$

First, we bring all variables to one side:

$$
\begin{aligned}x+\left(3\right) & ={x}^{2}y \\ {x}^{2}y-x-\left(3\right) & =0\end{aligned}
$$

If we set $f(x,y)={x}^{2}y-x-\left(3\right)$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve that passes through the point $(-1,2)$ can be computed as follows:

$$
t(-1,2)={f}_{y}(-1,2)i-{f}_{x}(-1,2)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,2):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}y-x-\left(3\right))i-\frac{∂}{∂x}({x}^{2}y-x-\left(3\right))j \\  & ={x}^{2}\,i-(2xy-1)j \\ t(-1,2) & =((-1))^{2}\,i-(2((-1))(2)-1)j \\  & =i+5\, j\end{aligned}
$$

Therefore, our tangent vector is $i+5\, j.$

## Original raw q-130192

### q-130192 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130192`

Consider the plane curve ${x}^{2}y={y}^{2}+3.$ Find a tangent vector to that curve at the point $(2,1).$

Field `selection` (:answer-field.type/radio):

- $2\,j$
- $3\,i$
- $2\,i-4\,j$ ✓
- $2\,i-j$
- $i+2\,j$

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}y & ={y}^{2}+3 \\ {x}^{2}y-{y}^{2} & =3\end{aligned}
$$

If we set $f(x,y)={x}^{2}y-{y}^{2},$ our curve can be viewed as the level curve $f(x,y)=3.$ 

A tangent vector to the level curve that passes through the point $(2,1)$ can be computed as follows:

$$
t(2,1)={f}_{y}(2,1)\,i-{f}_{x}(2,1)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(2,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}y-{y}^{2})\,i-\frac{∂}{∂x}({x}^{2}y-{y}^{2})\,j \\  & =({x}^{2}-2y)\,i-2xy\,j \\ t(2,1) & =({2}^{2}-2(1))\,i-2(2)(1)\,j \\  & =2\,i-4\,j\end{aligned}
$$

Therefore, our tangent vector is $2\,i-4\,j.$

## Minimal supported completion q-130192

### q-130192 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-130192`

Consider the plane curve ${x}^{2}y={y}^{2}+3.$ Find a tangent vector to that curve at the point $(2,1).$

Field `selection` (:answer-field.type/radio):

- $2\,j$
- $3\,i$
- $2\,i-4\,j$ ✓
- $2\,i-j$
- $i+2\,j$

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}y & ={y}^{2}+3 \\ {x}^{2}y-{y}^{2} & =3\end{aligned}
$$

If we set $f(x,y)={x}^{2}y-{y}^{2},$ our curve can be viewed as the level curve $f(x,y)=3.$ 

A tangent vector to the level curve that passes through the point $(2,1)$ can be computed as follows:

$$
t(2,1)={f}_{y}(2,1)\,i-{f}_{x}(2,1)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(2,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}y-{y}^{2})\,i-\frac{∂}{∂x}({x}^{2}y-{y}^{2})\,j \\  & =({x}^{2}-2y)\,i-2xy\,j \\ t(2,1) & =({2}^{2}-2(1))\,i-2(2)(1)\,j \\  & =2\,i-4\,j\end{aligned}
$$

Therefore, our tangent vector is $2\,i-4\,j.$

## Changed-parameter observed-mask evidence q-130192

### q-130192 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130192`

Consider the plane curve ${x}^{2}y={y}^{2}+3.$ Find a tangent vector to that curve at the point $(-2,1).$

Field `selection` (:answer-field.type/radio):

- $2\,j$
- $3\,i$
- $2\, i+4\, j$ ✓
- $2\,i-j$
- $i+2\,j$

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}y & ={y}^{2}+3 \\ {x}^{2}y-{y}^{2} & =3\end{aligned}
$$

If we set $f(x,y)={x}^{2}y-{y}^{2},$ our curve can be viewed as the level curve $f(x,y)=3.$ 

A tangent vector to the level curve that passes through the point $(-2,1)$ can be computed as follows:

$$
t(-2,1)={f}_{y}(-2,1)\,i-{f}_{x}(-2,1)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-2,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}({x}^{2}y-{y}^{2})\,i-\frac{∂}{∂x}({x}^{2}y-{y}^{2})\,j \\  & =({x}^{2}-2y)\,i-2xy\,j \\ t(-2,1) & =({(-2)}^{2}-2(1))\,i-2((-2))(1)\,j \\  & =2\, i+4\, j\end{aligned}
$$

Therefore, our tangent vector is $2\, i+4\, j.$

## Original raw q-130194

### q-130194 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130194`

Consider the plane curve $x\operatorname{ln}⁡y={x}^{2}-1.$ Find a tangent vector to that curve at the point $(-1,1).$

Field `selection` (:answer-field.type/radio):

- $2i$
- $-i+j$
- $-i-2\,j$ ✓
- $j$
- $2i+j$

First, we bring all variables to one side:

$$
\begin{aligned}x\operatorname{ln}⁡y & ={x}^{2}-1 \\ x\operatorname{ln}⁡y-{x}^{2} & =-1\end{aligned}
$$

If we set $f(x,y)=x\operatorname{ln}⁡y-{x}^{2},$ our curve can be viewed as the level curve $f(x,y)=-1.$ 

A tangent vector to the level curve that passes through the point $(-1,1)$ can be computed as follows:

$$
t(-1,1)={f}_{y}(-1,1)\,i-{f}_{x}(-1,1)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x\operatorname{ln}⁡y-{x}^{2})\,i-\frac{∂}{∂x}(x\operatorname{ln}⁡y-{x}^{2})\,j \\  & =\frac{x}{y}\,i-(\operatorname{ln}⁡y-2x)\,j \\ t(-1,1) & =\frac{(-1)}{1}\,i-(\operatorname{ln}⁡1-2(-1))\,j \\  & =-i-2\,j\end{aligned}
$$

Therefore, our tangent vector is $-i-2\,j.$

## Minimal supported completion q-130194

### q-130194 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `completed:q-130194`

Consider the plane curve $x\operatorname{ln}⁡y={x}^{2}-1.$ Find a tangent vector to that curve at the point $(-1,1).$

Field `selection` (:answer-field.type/radio):

- $2i$
- $-i+j$
- $-i-2\,j$ ✓
- $j$
- $2i+j$

First, we bring all variables to one side:

$$
\begin{aligned}x\operatorname{ln}⁡y & ={x}^{2}-1 \\ x\operatorname{ln}⁡y-{x}^{2} & =-1\end{aligned}
$$

If we set $f(x,y)=x\operatorname{ln}⁡y-{x}^{2},$ our curve can be viewed as the level curve $f(x,y)=-1.$ 

A tangent vector to the level curve that passes through the point $(-1,1)$ can be computed as follows:

$$
t(-1,1)={f}_{y}(-1,1)\,i-{f}_{x}(-1,1)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x\operatorname{ln}⁡y-{x}^{2})\,i-\frac{∂}{∂x}(x\operatorname{ln}⁡y-{x}^{2})\,j \\  & =\frac{x}{y}\,i-(\operatorname{ln}⁡y-2x)\,j \\ t(-1,1) & =\frac{(-1)}{1}\,i-(\operatorname{ln}⁡1-2(-1))\,j \\  & =-i-2\,j\end{aligned}
$$

Therefore, our tangent vector is $-i-2\,j.$

## Changed-parameter observed-mask evidence q-130194

### q-130194 — :question.difficulty/moderate — observed evidence replay

Evidence only: True; profile: `raw:q-130194`

Consider the plane curve $x\operatorname{ln}⁡y={x}^{2}-1.$ Find a tangent vector to that curve at the point $(1,1).$

Field `selection` (:answer-field.type/radio):

- $2i$
- $-i+j$
- $i+2\, j$ ✓
- $j$
- $2i+j$

First, we bring all variables to one side:

$$
\begin{aligned}x\operatorname{ln}⁡y & ={x}^{2}-1 \\ x\operatorname{ln}⁡y-{x}^{2} & =-1\end{aligned}
$$

If we set $f(x,y)=x\operatorname{ln}⁡y-{x}^{2},$ our curve can be viewed as the level curve $f(x,y)=-1.$ 

A tangent vector to the level curve that passes through the point $(1,1)$ can be computed as follows:

$$
t(1,1)={f}_{y}(1,1)\,i-{f}_{x}(1,1)\,j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,1):$

$$
\begin{aligned}t(x,y) & =\frac{∂}{∂y}(x\operatorname{ln}⁡y-{x}^{2})\,i-\frac{∂}{∂x}(x\operatorname{ln}⁡y-{x}^{2})\,j \\  & =\frac{x}{y}\,i-(\operatorname{ln}⁡y-2x)\,j \\ t(1,1) & =\frac{((1))}{1}\,i-(\operatorname{ln}⁡1-2((1)))\,j \\  & =i+2\, j\end{aligned}
$$

Therefore, our tangent vector is $i+2\, j.$

## Authored easy variant 1

### quadratic — :question.difficulty/easy — authored

Evidence only: False; profile: `method-bank`

Consider the plane curve $3 x^{2} + 3 x y - 4 y=1.$ Find a tangent vector to that curve at the point $(1,2).$

Field `selection` (:answer-field.type/radio):

- $-i-12\, j$ ✓
- $-i-6\, j$
- $12\, i-j$
- $-i+12\, j$
- $-12\, i-j$

First, if we set $f(x,y)=3 x^{2} + 3 x y - 4 y,$ our curve can be viewed as the level curve $f(x,y)=1.$

A tangent vector to the level curve that passes through the point $(1,2)$ can be computed as follows:

$$
t(1,2)=f_y(1,2)i-f_x(1,2)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,2):$

$$
\begin{aligned}t(x,y)&=\frac{\partial}{\partial y}(3 x^{2} + 3 x y - 4 y)\,i-\frac{\partial}{\partial x}(3 x^{2} + 3 x y - 4 y)\,j \\ &=(3 x - 4)\,i-(6 x + 3 y)\,j \\ t(1,2)&=(3 \left(1\right) - 4)\,i-(6 \left(1\right) + 3 \left(2\right))\,j \\ &=(-1)\,i-(12)\,j \\ &=-i-12\, j\end{aligned}
$$

Therefore, our tangent vector is $-i-12\, j.$

## Authored easy variant 2

### quadratic — :question.difficulty/easy — authored

Evidence only: False; profile: `method-bank`

Consider the plane curve $- 2 x^{2} - 3 x y + y=6.$ Find a tangent vector to that curve at the point $(-2,2).$

Field `selection` (:answer-field.type/radio):

- $7\, i-2\, j$ ✓
- $2\, i+7\, j$
- $7\, i+2\, j$
- $7\, i+6\, j$
- $-2\, i+7\, j$

First, if we set $f(x,y)=- 2 x^{2} - 3 x y + y,$ our curve can be viewed as the level curve $f(x,y)=6.$

A tangent vector to the level curve that passes through the point $(-2,2)$ can be computed as follows:

$$
t(-2,2)=f_y(-2,2)i-f_x(-2,2)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-2,2):$

$$
\begin{aligned}t(x,y)&=\frac{\partial}{\partial y}(- 2 x^{2} - 3 x y + y)\,i-\frac{\partial}{\partial x}(- 2 x^{2} - 3 x y + y)\,j \\ &=(1 - 3 x)\,i-(- 4 x - 3 y)\,j \\ t(-2,2)&=(1 - 3 \left(-2\right))\,i-(- 4 \left(-2\right) - 3 \left(2\right))\,j \\ &=(7)\,i-(2)\,j \\ &=7\, i-2\, j\end{aligned}
$$

Therefore, our tangent vector is $7\, i-2\, j.$

## Authored moderate variant 1

### mixed-polynomial — :question.difficulty/moderate — authored

Evidence only: False; profile: `method-bank`

Consider the plane curve $3 x^{2} y - 4 x y + 3 y^{2}=10.$ Find a tangent vector to that curve at the point $(1,2).$

Field `selection` (:answer-field.type/radio):

- $11\, i-4\, j$ ✓
- $8\, i+8\, j$
- $4\, i+11\, j$
- $11\, i+4\, j$
- $-4\, i+11\, j$

First, if we set $f(x,y)=3 x^{2} y - 4 x y + 3 y^{2},$ our curve can be viewed as the level curve $f(x,y)=10.$

A tangent vector to the level curve that passes through the point $(1,2)$ can be computed as follows:

$$
t(1,2)=f_y(1,2)i-f_x(1,2)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,2):$

$$
\begin{aligned}t(x,y)&=\frac{\partial}{\partial y}(3 x^{2} y - 4 x y + 3 y^{2})\,i-\frac{\partial}{\partial x}(3 x^{2} y - 4 x y + 3 y^{2})\,j \\ &=(3 x^{2} - 4 x + 6 y)\,i-(6 x y - 4 y)\,j \\ t(1,2)&=(3 \left(1\right)^{2} - 4 \left(1\right) + 6 \left(2\right))\,i-(6 \left(1\right) \left(2\right) - 4 \left(2\right))\,j \\ &=(11)\,i-(4)\,j \\ &=11\, i-4\, j\end{aligned}
$$

Therefore, our tangent vector is $11\, i-4\, j.$

## Authored moderate variant 2

### mixed-polynomial — :question.difficulty/moderate — authored

Evidence only: False; profile: `method-bank`

Consider the plane curve $- 2 x^{2} y + x y - 3 y^{2}=-32.$ Find a tangent vector to that curve at the point $(-2,2).$

Field `selection` (:answer-field.type/radio):

- $-22\, i-18\, j$ ✓
- $18\, i-22\, j$
- $-22\, i+18\, j$
- $-14\, i-2\, j$
- $-18\, i-22\, j$

First, if we set $f(x,y)=- 2 x^{2} y + x y - 3 y^{2},$ our curve can be viewed as the level curve $f(x,y)=-32.$

A tangent vector to the level curve that passes through the point $(-2,2)$ can be computed as follows:

$$
t(-2,2)=f_y(-2,2)i-f_x(-2,2)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-2,2):$

$$
\begin{aligned}t(x,y)&=\frac{\partial}{\partial y}(- 2 x^{2} y + x y - 3 y^{2})\,i-\frac{\partial}{\partial x}(- 2 x^{2} y + x y - 3 y^{2})\,j \\ &=(- 2 x^{2} + x - 6 y)\,i-(- 4 x y + y)\,j \\ t(-2,2)&=(- 2 \left(-2\right)^{2} + \left(-2\right) - 6 \left(2\right))\,i-(- 4 \left(-2\right) \left(2\right) + \left(2\right))\,j \\ &=(-22)\,i-(18)\,j \\ &=-22\, i-18\, j\end{aligned}
$$

Therefore, our tangent vector is $-22\, i-18\, j.$

## Authored hard variant 1

### log-product — :question.difficulty/hard — authored

Evidence only: False; profile: `method-bank`

Consider the plane curve $- 4 x^{2} + 3 x y + 3 x \ln{\left(y \right)}=2 + 3 e^{2}.$ Find a tangent vector to that curve at the point $(1,e^{2}).$

Field `selection` (:answer-field.type/radio):

- $\left(\frac{3}{e^{2}} + 3\right)\, i+\left(2 - 3 e^{2}\right)\, j$ ✓
- $3\, i+\left(8 - 3 e^{2}\right)\, j$
- $-\left(2 - 3 e^{2}\right)\, i+\left(\frac{3}{e^{2}} + 3\right)\, j$
- $\left(\frac{3}{e^{2}} + 3\right)\, i-\left(2 - 3 e^{2}\right)\, j$
- $\left(2 - 3 e^{2}\right)\, i+\left(\frac{3}{e^{2}} + 3\right)\, j$

First, if we set $f(x,y)=- 4 x^{2} + 3 x y + 3 x \ln{\left(y \right)},$ our curve can be viewed as the level curve $f(x,y)=2 + 3 e^{2}.$

A tangent vector to the level curve that passes through the point $(1,e^{2})$ can be computed as follows:

$$
t(1,e^{2})=f_y(1,e^{2})i-f_x(1,e^{2})j
$$

So, we calculate $t(x,y)$ and evaluate it at $(1,e^{2}):$

$$
\begin{aligned}t(x,y)&=\frac{\partial}{\partial y}(- 4 x^{2} + 3 x y + 3 x \ln{\left(y \right)})\,i-\frac{\partial}{\partial x}(- 4 x^{2} + 3 x y + 3 x \ln{\left(y \right)})\,j \\ &=(3 x + \frac{3 x}{y})\,i-(- 8 x + 3 y + 3 \ln{\left(y \right)})\,j \\ t(1,e^{2})&=(3 \left(1\right) + \frac{3 \left(1\right)}{\left(e^{2}\right)})\,i-(- 8 \left(1\right) + 3 \left(e^{2}\right) + 3 \ln{\left(\left(e^{2}\right) \right)})\,j \\ &=(\frac{3}{e^{2}} + 3)\,i-(-2 + 3 e^{2})\,j \\ &=\left(\frac{3}{e^{2}} + 3\right)\, i+\left(2 - 3 e^{2}\right)\, j\end{aligned}
$$

Therefore, our tangent vector is $\left(\frac{3}{e^{2}} + 3\right)\, i+\left(2 - 3 e^{2}\right)\, j.$

## Authored hard variant 2

### log-product — :question.difficulty/hard — authored

Evidence only: False; profile: `method-bank`

Consider the plane curve $3 x^{2} + 4 x y + 4 x \ln{\left(y \right)}=- 4 e - 1.$ Find a tangent vector to that curve at the point $(-1,e).$

Field `selection` (:answer-field.type/radio):

- $-4\, i+\left(6 - 4 e\right)\, j$
- $-\left(\frac{4}{e} + 4\right)\, i-\left(2 - 4 e\right)\, j$
- $-\left(2 - 4 e\right)\, i-\left(\frac{4}{e} + 4\right)\, j$
- $-\left(\frac{4}{e} + 4\right)\, i+\left(2 - 4 e\right)\, j$ ✓
- $\left(2 - 4 e\right)\, i-\left(\frac{4}{e} + 4\right)\, j$

First, if we set $f(x,y)=3 x^{2} + 4 x y + 4 x \ln{\left(y \right)},$ our curve can be viewed as the level curve $f(x,y)=- 4 e - 1.$

A tangent vector to the level curve that passes through the point $(-1,e)$ can be computed as follows:

$$
t(-1,e)=f_y(-1,e)i-f_x(-1,e)j
$$

So, we calculate $t(x,y)$ and evaluate it at $(-1,e):$

$$
\begin{aligned}t(x,y)&=\frac{\partial}{\partial y}(3 x^{2} + 4 x y + 4 x \ln{\left(y \right)})\,i-\frac{\partial}{\partial x}(3 x^{2} + 4 x y + 4 x \ln{\left(y \right)})\,j \\ &=(4 x + \frac{4 x}{y})\,i-(6 x + 4 y + 4 \ln{\left(y \right)})\,j \\ t(-1,e)&=(4 \left(-1\right) + \frac{4 \left(-1\right)}{\left(e\right)})\,i-(6 \left(-1\right) + 4 \left(e\right) + 4 \ln{\left(\left(e\right) \right)})\,j \\ &=(-4 - \frac{4}{e})\,i-(-2 + 4 e)\,j \\ &=-\left(\frac{4}{e} + 4\right)\, i+\left(2 - 4 e\right)\, j\end{aligned}
$$

Therefore, our tangent vector is $-\left(\frac{4}{e} + 4\right)\, i+\left(2 - 4 e\right)\, j.$
