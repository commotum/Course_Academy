# Review: originals, evidence completions and authored variants

## q-36332 original raw / unrated

### q-36332 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve $2xy + 3y^{2} = x^{2} + 4$ is the tangent vector to the curve perpendicular to the vector $j$?

$(0, 1)$ and $(-1, 0)$

$(1, 1)$ and $(-1,-1)$

$(1,-1)$ only

$(-1, 0)$ only

$(0, 1)$ only

Original correct designation absent; inferred value retained in author metadata only.

Original worked solution absent.

## q-36332 translated observed_raw

### q-36332 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve $2(x-2)(y+1) + 3(y+1)^{2} = (x-2)^{2} + 4$ is the tangent vector to the curve perpendicular to the vector $j$?

$(2,0)$ and $(1,-1)$

$(3,0)$ and $(1,-2)$

$(3,-2)$ only

$(1,-1)$ only

$(2,0)$ only

Original correct designation absent; inferred value retained in author metadata only.

Original worked solution absent.

## q-36332 translated observed_raw

### q-36332 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve $2(x+3)(y-3) + 3(y-3)^{2} = (x+3)^{2} + 4$ is the tangent vector to the curve perpendicular to the vector $j$?

$(-3,4)$ and $(-4,3)$

$(-2,4)$ and $(-4,2)$

$(-2,2)$ only

$(-4,3)$ only

$(-3,4)$ only

Original correct designation absent; inferred value retained in author metadata only.

Original worked solution absent.

## q-36332 translated observed_completed

### q-36332 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve $2(x-2)(y+1) + 3(y+1)^{2} = (x-2)^{2} + 4$ is the tangent vector to the curve perpendicular to the vector $j$?

$(2,0)$ and $(1,-1)$

**CORRECT** $(3,0)$ and $(1,-2)$

$(3,-2)$ only

$(1,-1)$ only

$(2,0)$ only

First, we bring all variables to one side:

$$- (x-2)^{2} + 2 (x-2) (y+1) + 3 (y+1)^{2} - 4=0$$

If we set $f(x,y)=- (x-2)^{2} + 2 (x-2) (y+1) + 3 (y+1)^{2} - 4$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(- (x-2)^{2} + 2 (x-2) (y+1) + 3 (y+1)^{2} - 4)\,i-\frac{∂}{∂x}(- (x-2)^{2} + 2 (x-2) (y+1) + 3 (y+1)^{2} - 4)\,j\\&=(2 (x-2) + 6 (y+1))\,i-(- 2 (x-2) + 2 (y+1))\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\2 (x-2) - 2 (y+1)&=0\\(y+1)&=(x-2)\end{aligned}$$

Substituting $(y+1)=(x-2)$ into the equation of our curve gives:

$$\begin{aligned}2(x-2)((x-2))+3((x-2))^{2}-(x-2)^{2}-4&=0\\4(x-2)^{2}&=4\\(x-2)^{2}&=1\\(x-2)&=\pm 1\end{aligned}$$

Finally, the corresponding points are $(1,-2)$ and $(3,0)$.

## q-36332 translated observed_completed

### q-36332 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve $2(x+3)(y-3) + 3(y-3)^{2} = (x+3)^{2} + 4$ is the tangent vector to the curve perpendicular to the vector $j$?

$(-3,4)$ and $(-4,3)$

**CORRECT** $(-2,4)$ and $(-4,2)$

$(-2,2)$ only

$(-4,3)$ only

$(-3,4)$ only

First, we bring all variables to one side:

$$- (x+3)^{2} + 2 (x+3) (y-3) + 3 (y-3)^{2} - 4=0$$

If we set $f(x,y)=- (x+3)^{2} + 2 (x+3) (y-3) + 3 (y-3)^{2} - 4$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(- (x+3)^{2} + 2 (x+3) (y-3) + 3 (y-3)^{2} - 4)\,i-\frac{∂}{∂x}(- (x+3)^{2} + 2 (x+3) (y-3) + 3 (y-3)^{2} - 4)\,j\\&=(2 (x+3) + 6 (y-3))\,i-(- 2 (x+3) + 2 (y-3))\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\2 (x+3) - 2 (y-3)&=0\\(y-3)&=(x+3)\end{aligned}$$

Substituting $(y-3)=(x+3)$ into the equation of our curve gives:

$$\begin{aligned}2(x+3)((x+3))+3((x+3))^{2}-(x+3)^{2}-4&=0\\4(x+3)^{2}&=4\\(x+3)^{2}&=1\\(x+3)&=\pm 1\end{aligned}$$

Finally, the corresponding points are $(-4,2)$ and $(-2,4)$.

## q-36332 completed evidence only

### q-36332 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve $2xy + 3y^{2} = x^{2} + 4$ is the tangent vector to the curve perpendicular to the vector $j$?

$(0, 1)$ and $(-1, 0)$

**CORRECT** $(1, 1)$ and $(-1,-1)$

$(1,-1)$ only

$(-1, 0)$ only

$(0, 1)$ only

First, we bring all variables to one side:

$$- x^{2} + 2 x y + 3 y^{2} - 4=0$$

If we set $f(x,y)=- x^{2} + 2 x y + 3 y^{2} - 4$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(- x^{2} + 2 x y + 3 y^{2} - 4)\,i-\frac{∂}{∂x}(- x^{2} + 2 x y + 3 y^{2} - 4)\,j\\&=(2 x + 6 y)\,i-(- 2 x + 2 y)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\2 x - 2 y&=0\\y&=x\end{aligned}$$

Substituting $y=x$ into the equation of our curve gives:

$$\begin{aligned}2x(x)+3(x)^{2}-x^{2}-4&=0\\4x^{2}&=4\\x^{2}&=1\\x&=\pm 1\end{aligned}$$

Finally, the corresponding points are $(-1,-1)$ and $(1,1)$.

## q-65208 original raw / unrated

### q-65208 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve $9x^{2}y = 3y^{3} - 6x$ is the tangent vector to the curve perpendicular to the vector $i$?

$(0, 0)$ and $(1, 1)$ only

$(0, 0)$ and $(1,-1)$ only

$(1,-1)$ only

$(0, 0)$, $(-1,-1)$, and $(1, 1)$

$(0, 0)$, $(-1, 1)$, and $(1,-1)$

Original correct designation absent; inferred value retained in author metadata only.

Original worked solution absent.

## q-65208 translated observed_raw

### q-65208 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve $9(x-2)^{2}(y+1) = 3(y+1)^{3} - 6(x-2)$ is the tangent vector to the curve perpendicular to the vector $i$?

$(2,-1)$ and $(3,0)$ only

$(2,-1)$ and $(3,-2)$ only

$(3,-2)$ only

$(2,-1)$, $(1,-2)$, and $(3,0)$

$(2,-1)$, $(1,0)$, and $(3,-2)$

Original correct designation absent; inferred value retained in author metadata only.

Original worked solution absent.

## q-65208 translated observed_raw

### q-65208 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve $9(x+3)^{2}(y-3) = 3(y-3)^{3} - 6(x+3)$ is the tangent vector to the curve perpendicular to the vector $i$?

$(-3,3)$ and $(-2,4)$ only

$(-3,3)$ and $(-2,2)$ only

$(-2,2)$ only

$(-3,3)$, $(-4,2)$, and $(-2,4)$

$(-3,3)$, $(-4,4)$, and $(-2,2)$

Original correct designation absent; inferred value retained in author metadata only.

Original worked solution absent.

## q-65208 translated observed_completed

### q-65208 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve $9(x-2)^{2}(y+1) = 3(y+1)^{3} - 6(x-2)$ is the tangent vector to the curve perpendicular to the vector $i$?

$(2,-1)$ and $(3,0)$ only

$(2,-1)$ and $(3,-2)$ only

$(3,-2)$ only

$(2,-1)$, $(1,-2)$, and $(3,0)$

**CORRECT** $(2,-1)$, $(1,0)$, and $(3,-2)$

First, we bring all variables to one side:

$$9 (x-2)^{2} (y+1) + 6 (x-2) - 3 (y+1)^{3}=0$$

If we set $f(x,y)=9 (x-2)^{2} (y+1) + 6 (x-2) - 3 (y+1)^{3}$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(9 (x-2)^{2} (y+1) + 6 (x-2) - 3 (y+1)^{3})\,i-\frac{∂}{∂x}(9 (x-2)^{2} (y+1) + 6 (x-2) - 3 (y+1)^{3})\,j\\&=(9 (x-2)^{2} - 9 (y+1)^{2})\,i-(18 (x-2) (y+1) + 6)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$\begin{aligned}t(x,y)\cdot i&=0\\9 (x-2)^{2} - 9 (y+1)^{2}&=0\\(y+1)&=(x-2)\text{ or }(y+1)=-(x-2)\end{aligned}$$

Substituting $(y+1)=(x-2)\text{ or }(y+1)=-(x-2)$ into the equation of our curve gives:

$$\begin{aligned}9(x-2)^{2}((x-2))-3((x-2))^{3}+6(x-2)&=0\\6(x-2)((x-2)^{2}+1)&=0\\(x-2)&=0\end{aligned}$$

For the second relation $(y+1)=-(x-2)$, substitution gives:

$$\begin{aligned}9(x-2)^{2}(-(x-2))-3(-(x-2))^{3}+6(x-2)&=0\\-6(x-2)^{3}+6(x-2)&=0\\-6(x-2)((x-2)-1)((x-2)+1)&=0\\(x-2)&=0,1,-1\end{aligned}$$

Finally, the corresponding points are $(1,0)$ and $(2,-1)$ and $(3,-2)$.

## q-65208 translated observed_completed

### q-65208 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve $9(x+3)^{2}(y-3) = 3(y-3)^{3} - 6(x+3)$ is the tangent vector to the curve perpendicular to the vector $i$?

$(-3,3)$ and $(-2,4)$ only

$(-3,3)$ and $(-2,2)$ only

$(-2,2)$ only

$(-3,3)$, $(-4,2)$, and $(-2,4)$

**CORRECT** $(-3,3)$, $(-4,4)$, and $(-2,2)$

First, we bring all variables to one side:

$$9 (x+3)^{2} (y-3) + 6 (x+3) - 3 (y-3)^{3}=0$$

If we set $f(x,y)=9 (x+3)^{2} (y-3) + 6 (x+3) - 3 (y-3)^{3}$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(9 (x+3)^{2} (y-3) + 6 (x+3) - 3 (y-3)^{3})\,i-\frac{∂}{∂x}(9 (x+3)^{2} (y-3) + 6 (x+3) - 3 (y-3)^{3})\,j\\&=(9 (x+3)^{2} - 9 (y-3)^{2})\,i-(18 (x+3) (y-3) + 6)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$\begin{aligned}t(x,y)\cdot i&=0\\9 (x+3)^{2} - 9 (y-3)^{2}&=0\\(y-3)&=(x+3)\text{ or }(y-3)=-(x+3)\end{aligned}$$

Substituting $(y-3)=(x+3)\text{ or }(y-3)=-(x+3)$ into the equation of our curve gives:

$$\begin{aligned}9(x+3)^{2}((x+3))-3((x+3))^{3}+6(x+3)&=0\\6(x+3)((x+3)^{2}+1)&=0\\(x+3)&=0\end{aligned}$$

For the second relation $(y-3)=-(x+3)$, substitution gives:

$$\begin{aligned}9(x+3)^{2}(-(x+3))-3(-(x+3))^{3}+6(x+3)&=0\\-6(x+3)^{3}+6(x+3)&=0\\-6(x+3)((x+3)-1)((x+3)+1)&=0\\(x+3)&=0,1,-1\end{aligned}$$

Finally, the corresponding points are $(-4,4)$ and $(-3,3)$ and $(-2,2)$.

## q-65208 completed evidence only

### q-65208 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve $9x^{2}y = 3y^{3} - 6x$ is the tangent vector to the curve perpendicular to the vector $i$?

$(0, 0)$ and $(1, 1)$ only

$(0, 0)$ and $(1,-1)$ only

$(1,-1)$ only

$(0, 0)$, $(-1,-1)$, and $(1, 1)$

**CORRECT** $(0, 0)$, $(-1, 1)$, and $(1,-1)$

First, we bring all variables to one side:

$$9 x^{2} y + 6 x - 3 y^{3}=0$$

If we set $f(x,y)=9 x^{2} y + 6 x - 3 y^{3}$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(9 x^{2} y + 6 x - 3 y^{3})\,i-\frac{∂}{∂x}(9 x^{2} y + 6 x - 3 y^{3})\,j\\&=(9 x^{2} - 9 y^{2})\,i-(18 x y + 6)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$\begin{aligned}t(x,y)\cdot i&=0\\9 x^{2} - 9 y^{2}&=0\\y&=x\text{ or }y=-x\end{aligned}$$

Substituting $y=x\text{ or }y=-x$ into the equation of our curve gives:

$$\begin{aligned}9x^{2}(x)-3(x)^{3}+6x&=0\\6x(x^{2}+1)&=0\\x&=0\end{aligned}$$

For the second relation $y=-x$, substitution gives:

$$\begin{aligned}9x^{2}(-x)-3(-x)^{3}+6x&=0\\-6x^{3}+6x&=0\\-6x(x-1)(x+1)&=0\\x&=0,1,-1\end{aligned}$$

Finally, the corresponding points are $(-1,1)$ and $(0,0)$ and $(1,-1)$.

## q-130223 original raw / hard

### q-130223 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which point on the curve ${x}^{2}y=-8x-4$ is the tangent vector to the curve perpendicular to the vector $j?$

(2,-5)

**CORRECT** (-1,4)

(-2,3)

(1,-12)

(-3,3)

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}y & =-8x-4 \\ {x}^{2}y+8x & =-4\end{aligned}
$$

If we set $f(x,y)={x}^{2}y+8x,$ our curve can be viewed as the level curve $f(x,y)=-4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({x}^{2}y+8x)\,i-\frac{∂}{∂x}({x}^{2}y+8x)\,j \\  & ={x}^{2}\,i-(2xy+8)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ({x}^{2}\,i-(2xy+8)\,j)\cdot j & =0 \\ -(2xy+8) & =0 \\ xy+4 & =0 \\ y & =-\frac{4}{x}\end{aligned}
$$

Substituting $y=-\frac{4}{x}$ into the equation of our curve gives

$$
\begin{aligned}{x}^{2}y & =-8x-4 \\ {x}^{2}(-\frac{4}{x}) & =-8x-4 \\ -4x & =-8x-4 \\ 4x & =-4 \\ x & =-1.\end{aligned}
$$

Finally, for $x=-1,$ we get $y=4,$ and the corresponding point is $(-1,4).$

## q-130223 translated observed_raw

### q-130223 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which point on the curve ${(x-2)}^{2}(y+1)=-8(x-2)-4$ is the tangent vector to the curve perpendicular to the vector $j?$

(4,-6)

**CORRECT** (1,3)

(0,2)

(3,-13)

(-1,2)

First, we bring all variables to one side:

$$
\begin{aligned}{(x-2)}^{2}(y+1) & =-8(x-2)-4 \\ {(x-2)}^{2}(y+1)+8(x-2) & =-4\end{aligned}
$$

If we set $f(x,y)={(x-2)}^{2}(y+1)+8(x-2),$ our curve can be viewed as the level curve $f(x,y)=-4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(x-2)}^{2}(y+1)+8(x-2))\,i-\frac{∂}{∂x}({(x-2)}^{2}(y+1)+8(x-2))\,j \\  & ={(x-2)}^{2}\,i-(2(x-2)(y+1)+8)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ({(x-2)}^{2}\,i-(2(x-2)(y+1)+8)\,j)\cdot j & =0 \\ -(2(x-2)(y+1)+8) & =0 \\ (x-2)(y+1)+4 & =0 \\ (y+1) & =-\frac{4}{(x-2)}\end{aligned}
$$

Substituting $(y+1)=-\frac{4}{(x-2)}$ into the equation of our curve gives

$$
\begin{aligned}{(x-2)}^{2}(y+1) & =-8(x-2)-4 \\ {(x-2)}^{2}(-\frac{4}{(x-2)}) & =-8(x-2)-4 \\ -4(x-2) & =-8(x-2)-4 \\ 4(x-2) & =-4 \\ (x-2) & =-1.\end{aligned}
$$

Finally, for $(x-2)=-1,$ we get $(y+1)=4,$ and the corresponding point is $(1,3).$

## q-130223 translated observed_raw

### q-130223 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which point on the curve ${(x+3)}^{2}(y-3)=-8(x+3)-4$ is the tangent vector to the curve perpendicular to the vector $j?$

(-1,-2)

**CORRECT** (-4,7)

(-5,6)

(-2,-9)

(-6,6)

First, we bring all variables to one side:

$$
\begin{aligned}{(x+3)}^{2}(y-3) & =-8(x+3)-4 \\ {(x+3)}^{2}(y-3)+8(x+3) & =-4\end{aligned}
$$

If we set $f(x,y)={(x+3)}^{2}(y-3)+8(x+3),$ our curve can be viewed as the level curve $f(x,y)=-4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(x+3)}^{2}(y-3)+8(x+3))\,i-\frac{∂}{∂x}({(x+3)}^{2}(y-3)+8(x+3))\,j \\  & ={(x+3)}^{2}\,i-(2(x+3)(y-3)+8)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ({(x+3)}^{2}\,i-(2(x+3)(y-3)+8)\,j)\cdot j & =0 \\ -(2(x+3)(y-3)+8) & =0 \\ (x+3)(y-3)+4 & =0 \\ (y-3) & =-\frac{4}{(x+3)}\end{aligned}
$$

Substituting $(y-3)=-\frac{4}{(x+3)}$ into the equation of our curve gives

$$
\begin{aligned}{(x+3)}^{2}(y-3) & =-8(x+3)-4 \\ {(x+3)}^{2}(-\frac{4}{(x+3)}) & =-8(x+3)-4 \\ -4(x+3) & =-8(x+3)-4 \\ 4(x+3) & =-4 \\ (x+3) & =-1.\end{aligned}
$$

Finally, for $(x+3)=-1,$ we get $(y-3)=4,$ and the corresponding point is $(-4,7).$

## q-130223 translated observed_completed

### q-130223 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which point on the curve ${(x-2)}^{2}(y+1)=-8(x-2)-4$ is the tangent vector to the curve perpendicular to the vector $j?$

(4,-6)

**CORRECT** (1,3)

(0,2)

(3,-13)

(-1,2)

First, we bring all variables to one side:

$$
\begin{aligned}{(x-2)}^{2}(y+1) & =-8(x-2)-4 \\ {(x-2)}^{2}(y+1)+8(x-2) & =-4\end{aligned}
$$

If we set $f(x,y)={(x-2)}^{2}(y+1)+8(x-2),$ our curve can be viewed as the level curve $f(x,y)=-4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(x-2)}^{2}(y+1)+8(x-2))\,i-\frac{∂}{∂x}({(x-2)}^{2}(y+1)+8(x-2))\,j \\  & ={(x-2)}^{2}\,i-(2(x-2)(y+1)+8)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ({(x-2)}^{2}\,i-(2(x-2)(y+1)+8)\,j)\cdot j & =0 \\ -(2(x-2)(y+1)+8) & =0 \\ (x-2)(y+1)+4 & =0 \\ (y+1) & =-\frac{4}{(x-2)}\end{aligned}
$$

Substituting $(y+1)=-\frac{4}{(x-2)}$ into the equation of our curve gives

$$
\begin{aligned}{(x-2)}^{2}(y+1) & =-8(x-2)-4 \\ {(x-2)}^{2}(-\frac{4}{(x-2)}) & =-8(x-2)-4 \\ -4(x-2) & =-8(x-2)-4 \\ 4(x-2) & =-4 \\ (x-2) & =-1.\end{aligned}
$$

Finally, for $(x-2)=-1,$ we get $(y+1)=4,$ and the corresponding point is $(1,3).$

## q-130223 translated observed_completed

### q-130223 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which point on the curve ${(x+3)}^{2}(y-3)=-8(x+3)-4$ is the tangent vector to the curve perpendicular to the vector $j?$

(-1,-2)

**CORRECT** (-4,7)

(-5,6)

(-2,-9)

(-6,6)

First, we bring all variables to one side:

$$
\begin{aligned}{(x+3)}^{2}(y-3) & =-8(x+3)-4 \\ {(x+3)}^{2}(y-3)+8(x+3) & =-4\end{aligned}
$$

If we set $f(x,y)={(x+3)}^{2}(y-3)+8(x+3),$ our curve can be viewed as the level curve $f(x,y)=-4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(x+3)}^{2}(y-3)+8(x+3))\,i-\frac{∂}{∂x}({(x+3)}^{2}(y-3)+8(x+3))\,j \\  & ={(x+3)}^{2}\,i-(2(x+3)(y-3)+8)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ({(x+3)}^{2}\,i-(2(x+3)(y-3)+8)\,j)\cdot j & =0 \\ -(2(x+3)(y-3)+8) & =0 \\ (x+3)(y-3)+4 & =0 \\ (y-3) & =-\frac{4}{(x+3)}\end{aligned}
$$

Substituting $(y-3)=-\frac{4}{(x+3)}$ into the equation of our curve gives

$$
\begin{aligned}{(x+3)}^{2}(y-3) & =-8(x+3)-4 \\ {(x+3)}^{2}(-\frac{4}{(x+3)}) & =-8(x+3)-4 \\ -4(x+3) & =-8(x+3)-4 \\ 4(x+3) & =-4 \\ (x+3) & =-1.\end{aligned}
$$

Finally, for $(x+3)=-1,$ we get $(y-3)=4,$ and the corresponding point is $(-4,7).$

## q-130223 completed evidence only

### q-130223 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which point on the curve ${x}^{2}y=-8x-4$ is the tangent vector to the curve perpendicular to the vector $j?$

(2,-5)

**CORRECT** (-1,4)

(-2,3)

(1,-12)

(-3,3)

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}y & =-8x-4 \\ {x}^{2}y+8x & =-4\end{aligned}
$$

If we set $f(x,y)={x}^{2}y+8x,$ our curve can be viewed as the level curve $f(x,y)=-4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({x}^{2}y+8x)\,i-\frac{∂}{∂x}({x}^{2}y+8x)\,j \\  & ={x}^{2}\,i-(2xy+8)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ({x}^{2}\,i-(2xy+8)\,j)\cdot j & =0 \\ -(2xy+8) & =0 \\ xy+4 & =0 \\ y & =-\frac{4}{x}\end{aligned}
$$

Substituting $y=-\frac{4}{x}$ into the equation of our curve gives

$$
\begin{aligned}{x}^{2}y & =-8x-4 \\ {x}^{2}(-\frac{4}{x}) & =-8x-4 \\ -4x & =-8x-4 \\ 4x & =-4 \\ x & =-1.\end{aligned}
$$

Finally, for $x=-1,$ we get $y=4,$ and the corresponding point is $(-1,4).$

## q-72410 original raw / hard

### q-72410 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${y}^{2}+2xy={x}^{2}+8$ is the tangent vector to the curve perpendicular to the vector $j?$

**CORRECT** $(2,2)$ and $(-2,-2)$

$(0,2)$ only

$(0,2)$ and $(1,2)$

$(2,0)$  and $(0,2)$

$(1,2)$ and $(2,1)$

First, we bring all variables to one side:

$$
\begin{aligned}{y}^{2}+2xy & ={x}^{2}+8 \\ {y}^{2}+2xy-{x}^{2} & =8\end{aligned}
$$

If we set $f(x,y)={y}^{2}+2xy-{x}^{2}$, our curve can be viewed as the level curve $f(x,y)=8.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({y}^{2}+2xy-{x}^{2})i-\frac{∂}{∂x}({y}^{2}+2xy-{x}^{2})j \\  & =2(y+x)\,i-2(y-x)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ (2(y+x)\,i-2(y-x)\,j)\cdot j & =0 \\ -2(y-x) & =0 \\ y & =x\end{aligned}
$$

Substituting $y=x$ into the equation of our curve gives:  

$$
\begin{aligned}{y}^{2}+2xy-{x}^{2} & =8 \\ (x)^{2}+2x(x)-{x}^{2} & =8 \\ {x}^{2}+2{x}^{2}-{x}^{2} & =8 \\ 2{x}^{2} & =8 \\ {x}^{2} & =4 \\ x & =\pm 2\end{aligned}
$$

Finally:

- If $x=2$, we get $y=2$ and the corresponding point is $(2,2).$

- If $x=-2$, we get $y=-2$ and the corresponding point is $(-2,-2).$

## q-72410 translated observed_raw

### q-72410 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(y+1)}^{2}+2(x-2)(y+1)={(x-2)}^{2}+8$ is the tangent vector to the curve perpendicular to the vector $j?$

**CORRECT** $(4,1)$ and $(0,-3)$

$(2,1)$ only

$(2,1)$ and $(3,1)$

$(4,-1)$  and $(2,1)$

$(3,1)$ and $(4,0)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y+1)}^{2}+2(x-2)(y+1) & ={(x-2)}^{2}+8 \\ {(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2} & =8\end{aligned}
$$

If we set $f(x,y)={(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2}$, our curve can be viewed as the level curve $f(x,y)=8.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2})i-\frac{∂}{∂x}({(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2})j \\  & =2((y+1)+(x-2))\,i-2((y+1)-(x-2))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ (2((y+1)+(x-2))\,i-2((y+1)-(x-2))\,j)\cdot j & =0 \\ -2((y+1)-(x-2)) & =0 \\ (y+1) & =(x-2)\end{aligned}
$$

Substituting $(y+1)=(x-2)$ into the equation of our curve gives:  

$$
\begin{aligned}{(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2} & =8 \\ ((x-2))^{2}+2(x-2)((x-2))-{(x-2)}^{2} & =8 \\ {(x-2)}^{2}+2{(x-2)}^{2}-{(x-2)}^{2} & =8 \\ 2{(x-2)}^{2} & =8 \\ {(x-2)}^{2} & =4 \\ (x-2) & =\pm 2\end{aligned}
$$

Finally:

- If $(x-2)=2$, we get $(y+1)=2$ and the corresponding point is $(4,1).$

- If $(x-2)=-2$, we get $(y+1)=-2$ and the corresponding point is $(0,-3).$

## q-72410 translated observed_raw

### q-72410 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(y-3)}^{2}+2(x+3)(y-3)={(x+3)}^{2}+8$ is the tangent vector to the curve perpendicular to the vector $j?$

**CORRECT** $(-1,5)$ and $(-5,1)$

$(-3,5)$ only

$(-3,5)$ and $(-2,5)$

$(-1,3)$  and $(-3,5)$

$(-2,5)$ and $(-1,4)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y-3)}^{2}+2(x+3)(y-3) & ={(x+3)}^{2}+8 \\ {(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2} & =8\end{aligned}
$$

If we set $f(x,y)={(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2}$, our curve can be viewed as the level curve $f(x,y)=8.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2})i-\frac{∂}{∂x}({(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2})j \\  & =2((y-3)+(x+3))\,i-2((y-3)-(x+3))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ (2((y-3)+(x+3))\,i-2((y-3)-(x+3))\,j)\cdot j & =0 \\ -2((y-3)-(x+3)) & =0 \\ (y-3) & =(x+3)\end{aligned}
$$

Substituting $(y-3)=(x+3)$ into the equation of our curve gives:  

$$
\begin{aligned}{(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2} & =8 \\ ((x+3))^{2}+2(x+3)((x+3))-{(x+3)}^{2} & =8 \\ {(x+3)}^{2}+2{(x+3)}^{2}-{(x+3)}^{2} & =8 \\ 2{(x+3)}^{2} & =8 \\ {(x+3)}^{2} & =4 \\ (x+3) & =\pm 2\end{aligned}
$$

Finally:

- If $(x+3)=2$, we get $(y-3)=2$ and the corresponding point is $(-1,5).$

- If $(x+3)=-2$, we get $(y-3)=-2$ and the corresponding point is $(-5,1).$

## q-72410 translated observed_completed

### q-72410 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(y+1)}^{2}+2(x-2)(y+1)={(x-2)}^{2}+8$ is the tangent vector to the curve perpendicular to the vector $j?$

**CORRECT** $(4,1)$ and $(0,-3)$

$(2,1)$ only

$(2,1)$ and $(3,1)$

$(4,-1)$  and $(2,1)$

$(3,1)$ and $(4,0)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y+1)}^{2}+2(x-2)(y+1) & ={(x-2)}^{2}+8 \\ {(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2} & =8\end{aligned}
$$

If we set $f(x,y)={(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2}$, our curve can be viewed as the level curve $f(x,y)=8.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2})i-\frac{∂}{∂x}({(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2})j \\  & =2((y+1)+(x-2))\,i-2((y+1)-(x-2))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ (2((y+1)+(x-2))\,i-2((y+1)-(x-2))\,j)\cdot j & =0 \\ -2((y+1)-(x-2)) & =0 \\ (y+1) & =(x-2)\end{aligned}
$$

Substituting $(y+1)=(x-2)$ into the equation of our curve gives:  

$$
\begin{aligned}{(y+1)}^{2}+2(x-2)(y+1)-{(x-2)}^{2} & =8 \\ ((x-2))^{2}+2(x-2)((x-2))-{(x-2)}^{2} & =8 \\ {(x-2)}^{2}+2{(x-2)}^{2}-{(x-2)}^{2} & =8 \\ 2{(x-2)}^{2} & =8 \\ {(x-2)}^{2} & =4 \\ (x-2) & =\pm 2\end{aligned}
$$

Finally:

- If $(x-2)=2$, we get $(y+1)=2$ and the corresponding point is $(4,1).$

- If $(x-2)=-2$, we get $(y+1)=-2$ and the corresponding point is $(0,-3).$

## q-72410 translated observed_completed

### q-72410 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(y-3)}^{2}+2(x+3)(y-3)={(x+3)}^{2}+8$ is the tangent vector to the curve perpendicular to the vector $j?$

**CORRECT** $(-1,5)$ and $(-5,1)$

$(-3,5)$ only

$(-3,5)$ and $(-2,5)$

$(-1,3)$  and $(-3,5)$

$(-2,5)$ and $(-1,4)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y-3)}^{2}+2(x+3)(y-3) & ={(x+3)}^{2}+8 \\ {(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2} & =8\end{aligned}
$$

If we set $f(x,y)={(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2}$, our curve can be viewed as the level curve $f(x,y)=8.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2})i-\frac{∂}{∂x}({(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2})j \\  & =2((y-3)+(x+3))\,i-2((y-3)-(x+3))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ (2((y-3)+(x+3))\,i-2((y-3)-(x+3))\,j)\cdot j & =0 \\ -2((y-3)-(x+3)) & =0 \\ (y-3) & =(x+3)\end{aligned}
$$

Substituting $(y-3)=(x+3)$ into the equation of our curve gives:  

$$
\begin{aligned}{(y-3)}^{2}+2(x+3)(y-3)-{(x+3)}^{2} & =8 \\ ((x+3))^{2}+2(x+3)((x+3))-{(x+3)}^{2} & =8 \\ {(x+3)}^{2}+2{(x+3)}^{2}-{(x+3)}^{2} & =8 \\ 2{(x+3)}^{2} & =8 \\ {(x+3)}^{2} & =4 \\ (x+3) & =\pm 2\end{aligned}
$$

Finally:

- If $(x+3)=2$, we get $(y-3)=2$ and the corresponding point is $(-1,5).$

- If $(x+3)=-2$, we get $(y-3)=-2$ and the corresponding point is $(-5,1).$

## q-72410 completed evidence only

### q-72410 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${y}^{2}+2xy={x}^{2}+8$ is the tangent vector to the curve perpendicular to the vector $j?$

**CORRECT** $(2,2)$ and $(-2,-2)$

$(0,2)$ only

$(0,2)$ and $(1,2)$

$(2,0)$  and $(0,2)$

$(1,2)$ and $(2,1)$

First, we bring all variables to one side:

$$
\begin{aligned}{y}^{2}+2xy & ={x}^{2}+8 \\ {y}^{2}+2xy-{x}^{2} & =8\end{aligned}
$$

If we set $f(x,y)={y}^{2}+2xy-{x}^{2}$, our curve can be viewed as the level curve $f(x,y)=8.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({y}^{2}+2xy-{x}^{2})i-\frac{∂}{∂x}({y}^{2}+2xy-{x}^{2})j \\  & =2(y+x)\,i-2(y-x)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ (2(y+x)\,i-2(y-x)\,j)\cdot j & =0 \\ -2(y-x) & =0 \\ y & =x\end{aligned}
$$

Substituting $y=x$ into the equation of our curve gives:  

$$
\begin{aligned}{y}^{2}+2xy-{x}^{2} & =8 \\ (x)^{2}+2x(x)-{x}^{2} & =8 \\ {x}^{2}+2{x}^{2}-{x}^{2} & =8 \\ 2{x}^{2} & =8 \\ {x}^{2} & =4 \\ x & =\pm 2\end{aligned}
$$

Finally:

- If $x=2$, we get $y=2$ and the corresponding point is $(2,2).$

- If $x=-2$, we get $y=-2$ and the corresponding point is $(-2,-2).$

## q-72440 original raw / hard

### q-72440 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${x}^{2}+2xy=-5y+4$ is the tangent vector to the curve perpendicular to the vector $j?$

$(1,1)$ and  $(4,-4)$ only

$(-1,4)$ and  $(-4,1)$ only

$(1,1)$ and  $(-2,4)$ only

$(-1,4)$ only

**CORRECT** $(-1,1)$ and  $(-4,4)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}+2xy & =-5y+4 \\ {x}^{2}+2xy+5y & =4\end{aligned}
$$

If we set $f(x,y)={x}^{2}+2xy+5y$, our curve can be viewed as the level curve $f(x,y)=4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({x}^{2}+2xy+5y)i-\frac{∂}{∂x}({x}^{2}+2xy+5y)j \\  & =(2x+5)\,i-(2x+2y)\,j\end{aligned}
$$

  

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2x+5)\,i-(2x+2y)\,j)\cdot j & =0 \\ -(2x+2y) & =0 \\ x & =-y\end{aligned}
$$

Substituting $x=-y$ into the equation of our curve gives:    

$$
\begin{aligned}{x}^{2}+2xy+5y & =4 \\ (-y)^{2}+2(-y)y+5y & =4 \\ {y}^{2}-2{y}^{2}+5y & =4 \\ -{y}^{2}+5y-4 & =0 \\ {y}^{2}-5y+4 & =0 \\ (y-1)(y-4) & =0 \\ y & =1\,\text{or}\,y=4\end{aligned}
$$

Finally:

- If $y=1$, we get $x=-1$ and the corresponding point is $(-1,1).$

- If $y=4$, we get $x=-4$ and the corresponding point is $(-4,4).$

## q-72440 translated observed_raw

### q-72440 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(x-2)}^{2}+2(x-2)(y+1)=-5(y+1)+4$ is the tangent vector to the curve perpendicular to the vector $j?$

$(3,0)$ and  $(6,-5)$ only

$(1,3)$ and  $(-2,0)$ only

$(3,0)$ and  $(0,3)$ only

$(1,3)$ only

**CORRECT** $(1,0)$ and  $(-2,3)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{(x-2)}^{2}+2(x-2)(y+1) & =-5(y+1)+4 \\ {(x-2)}^{2}+2(x-2)(y+1)+5(y+1) & =4\end{aligned}
$$

If we set $f(x,y)={(x-2)}^{2}+2(x-2)(y+1)+5(y+1)$, our curve can be viewed as the level curve $f(x,y)=4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(x-2)}^{2}+2(x-2)(y+1)+5(y+1))i-\frac{∂}{∂x}({(x-2)}^{2}+2(x-2)(y+1)+5(y+1))j \\  & =(2(x-2)+5)\,i-(2(x-2)+2(y+1))\,j\end{aligned}
$$

  

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2(x-2)+5)\,i-(2(x-2)+2(y+1))\,j)\cdot j & =0 \\ -(2(x-2)+2(y+1)) & =0 \\ (x-2) & =-(y+1)\end{aligned}
$$

Substituting $(x-2)=-(y+1)$ into the equation of our curve gives:    

$$
\begin{aligned}{(x-2)}^{2}+2(x-2)(y+1)+5(y+1) & =4 \\ (-(y+1))^{2}+2(-(y+1))(y+1)+5(y+1) & =4 \\ {(y+1)}^{2}-2{(y+1)}^{2}+5(y+1) & =4 \\ -{(y+1)}^{2}+5(y+1)-4 & =0 \\ {(y+1)}^{2}-5(y+1)+4 & =0 \\ ((y+1)-1)((y+1)-4) & =0 \\ (y+1) & =1\,\text{or}\,(y+1)=4\end{aligned}
$$

Finally:

- If $(y+1)=1$, we get $(x-2)=-1$ and the corresponding point is $(1,0).$

- If $(y+1)=4$, we get $(x-2)=-4$ and the corresponding point is $(-2,3).$

## q-72440 translated observed_raw

### q-72440 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(x+3)}^{2}+2(x+3)(y-3)=-5(y-3)+4$ is the tangent vector to the curve perpendicular to the vector $j?$

$(-2,4)$ and  $(1,-1)$ only

$(-4,7)$ and  $(-7,4)$ only

$(-2,4)$ and  $(-5,7)$ only

$(-4,7)$ only

**CORRECT** $(-4,4)$ and  $(-7,7)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{(x+3)}^{2}+2(x+3)(y-3) & =-5(y-3)+4 \\ {(x+3)}^{2}+2(x+3)(y-3)+5(y-3) & =4\end{aligned}
$$

If we set $f(x,y)={(x+3)}^{2}+2(x+3)(y-3)+5(y-3)$, our curve can be viewed as the level curve $f(x,y)=4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(x+3)}^{2}+2(x+3)(y-3)+5(y-3))i-\frac{∂}{∂x}({(x+3)}^{2}+2(x+3)(y-3)+5(y-3))j \\  & =(2(x+3)+5)\,i-(2(x+3)+2(y-3))\,j\end{aligned}
$$

  

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2(x+3)+5)\,i-(2(x+3)+2(y-3))\,j)\cdot j & =0 \\ -(2(x+3)+2(y-3)) & =0 \\ (x+3) & =-(y-3)\end{aligned}
$$

Substituting $(x+3)=-(y-3)$ into the equation of our curve gives:    

$$
\begin{aligned}{(x+3)}^{2}+2(x+3)(y-3)+5(y-3) & =4 \\ (-(y-3))^{2}+2(-(y-3))(y-3)+5(y-3) & =4 \\ {(y-3)}^{2}-2{(y-3)}^{2}+5(y-3) & =4 \\ -{(y-3)}^{2}+5(y-3)-4 & =0 \\ {(y-3)}^{2}-5(y-3)+4 & =0 \\ ((y-3)-1)((y-3)-4) & =0 \\ (y-3) & =1\,\text{or}\,(y-3)=4\end{aligned}
$$

Finally:

- If $(y-3)=1$, we get $(x+3)=-1$ and the corresponding point is $(-4,4).$

- If $(y-3)=4$, we get $(x+3)=-4$ and the corresponding point is $(-7,7).$

## q-72440 translated observed_completed

### q-72440 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(x-2)}^{2}+2(x-2)(y+1)=-5(y+1)+4$ is the tangent vector to the curve perpendicular to the vector $j?$

$(3,0)$ and  $(6,-5)$ only

$(1,3)$ and  $(-2,0)$ only

$(3,0)$ and  $(0,3)$ only

$(1,3)$ only

**CORRECT** $(1,0)$ and  $(-2,3)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{(x-2)}^{2}+2(x-2)(y+1) & =-5(y+1)+4 \\ {(x-2)}^{2}+2(x-2)(y+1)+5(y+1) & =4\end{aligned}
$$

If we set $f(x,y)={(x-2)}^{2}+2(x-2)(y+1)+5(y+1)$, our curve can be viewed as the level curve $f(x,y)=4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(x-2)}^{2}+2(x-2)(y+1)+5(y+1))i-\frac{∂}{∂x}({(x-2)}^{2}+2(x-2)(y+1)+5(y+1))j \\  & =(2(x-2)+5)\,i-(2(x-2)+2(y+1))\,j\end{aligned}
$$

  

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2(x-2)+5)\,i-(2(x-2)+2(y+1))\,j)\cdot j & =0 \\ -(2(x-2)+2(y+1)) & =0 \\ (x-2) & =-(y+1)\end{aligned}
$$

Substituting $(x-2)=-(y+1)$ into the equation of our curve gives:    

$$
\begin{aligned}{(x-2)}^{2}+2(x-2)(y+1)+5(y+1) & =4 \\ (-(y+1))^{2}+2(-(y+1))(y+1)+5(y+1) & =4 \\ {(y+1)}^{2}-2{(y+1)}^{2}+5(y+1) & =4 \\ -{(y+1)}^{2}+5(y+1)-4 & =0 \\ {(y+1)}^{2}-5(y+1)+4 & =0 \\ ((y+1)-1)((y+1)-4) & =0 \\ (y+1) & =1\,\text{or}\,(y+1)=4\end{aligned}
$$

Finally:

- If $(y+1)=1$, we get $(x-2)=-1$ and the corresponding point is $(1,0).$

- If $(y+1)=4$, we get $(x-2)=-4$ and the corresponding point is $(-2,3).$

## q-72440 translated observed_completed

### q-72440 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(x+3)}^{2}+2(x+3)(y-3)=-5(y-3)+4$ is the tangent vector to the curve perpendicular to the vector $j?$

$(-2,4)$ and  $(1,-1)$ only

$(-4,7)$ and  $(-7,4)$ only

$(-2,4)$ and  $(-5,7)$ only

$(-4,7)$ only

**CORRECT** $(-4,4)$ and  $(-7,7)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{(x+3)}^{2}+2(x+3)(y-3) & =-5(y-3)+4 \\ {(x+3)}^{2}+2(x+3)(y-3)+5(y-3) & =4\end{aligned}
$$

If we set $f(x,y)={(x+3)}^{2}+2(x+3)(y-3)+5(y-3)$, our curve can be viewed as the level curve $f(x,y)=4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(x+3)}^{2}+2(x+3)(y-3)+5(y-3))i-\frac{∂}{∂x}({(x+3)}^{2}+2(x+3)(y-3)+5(y-3))j \\  & =(2(x+3)+5)\,i-(2(x+3)+2(y-3))\,j\end{aligned}
$$

  

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2(x+3)+5)\,i-(2(x+3)+2(y-3))\,j)\cdot j & =0 \\ -(2(x+3)+2(y-3)) & =0 \\ (x+3) & =-(y-3)\end{aligned}
$$

Substituting $(x+3)=-(y-3)$ into the equation of our curve gives:    

$$
\begin{aligned}{(x+3)}^{2}+2(x+3)(y-3)+5(y-3) & =4 \\ (-(y-3))^{2}+2(-(y-3))(y-3)+5(y-3) & =4 \\ {(y-3)}^{2}-2{(y-3)}^{2}+5(y-3) & =4 \\ -{(y-3)}^{2}+5(y-3)-4 & =0 \\ {(y-3)}^{2}-5(y-3)+4 & =0 \\ ((y-3)-1)((y-3)-4) & =0 \\ (y-3) & =1\,\text{or}\,(y-3)=4\end{aligned}
$$

Finally:

- If $(y-3)=1$, we get $(x+3)=-1$ and the corresponding point is $(-4,4).$

- If $(y-3)=4$, we get $(x+3)=-4$ and the corresponding point is $(-7,7).$

## q-72440 completed evidence only

### q-72440 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${x}^{2}+2xy=-5y+4$ is the tangent vector to the curve perpendicular to the vector $j?$

$(1,1)$ and  $(4,-4)$ only

$(-1,4)$ and  $(-4,1)$ only

$(1,1)$ and  $(-2,4)$ only

$(-1,4)$ only

**CORRECT** $(-1,1)$ and  $(-4,4)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}+2xy & =-5y+4 \\ {x}^{2}+2xy+5y & =4\end{aligned}
$$

If we set $f(x,y)={x}^{2}+2xy+5y$, our curve can be viewed as the level curve $f(x,y)=4.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({x}^{2}+2xy+5y)i-\frac{∂}{∂x}({x}^{2}+2xy+5y)j \\  & =(2x+5)\,i-(2x+2y)\,j\end{aligned}
$$

  

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2x+5)\,i-(2x+2y)\,j)\cdot j & =0 \\ -(2x+2y) & =0 \\ x & =-y\end{aligned}
$$

Substituting $x=-y$ into the equation of our curve gives:    

$$
\begin{aligned}{x}^{2}+2xy+5y & =4 \\ (-y)^{2}+2(-y)y+5y & =4 \\ {y}^{2}-2{y}^{2}+5y & =4 \\ -{y}^{2}+5y-4 & =0 \\ {y}^{2}-5y+4 & =0 \\ (y-1)(y-4) & =0 \\ y & =1\,\text{or}\,y=4\end{aligned}
$$

Finally:

- If $y=1$, we get $x=-1$ and the corresponding point is $(-1,1).$

- If $y=4$, we get $x=-4$ and the corresponding point is $(-4,4).$

## q-72416 original raw / hard

### q-72416 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve $2xy-3{x}^{2}=-y$ is the tangent vector to the curve perpendicular to the vector $j?$

$(0,3)$ and $(0,-3)$

**CORRECT** $(0,0)$ and $(-1,-3)$

$(0,-1)$ and $(0,-3)$

$(0,1)$ and $(1,-3)$

$(3,0)$ and $(-1,0)$

First, we bring all variables to one side:

$$
\begin{aligned}2xy-3{x}^{2}=-y \\ 2xy-3{x}^{2}+y & =0\end{aligned}
$$

If we set $f(x,y)=2xy-3{x}^{2}+y$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}(2xy-3{x}^{2}+y)i-\frac{∂}{∂x}(2xy-3{x}^{2}+y)j \\  & =(2x+1)\,i-2(y-3x)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2x+1)\,i-2(y-3x)\,j)\cdot j & =0 \\ -2(y-3x) & =0 \\ y & =3x\end{aligned}
$$

Substituting $y=3x$ into the equation of our curve gives:  

$$
\begin{aligned}2xy-3{x}^{2}+y & =0 \\ 2x(3x)-3{x}^{2}+3x & =0 \\ 6{x}^{2}-3{x}^{2}+3x & =0 \\ 3{x}^{2}+3x & =0 \\ 3x(x+1) & =0 \\ x & =0\,\text{or}\,x=-1\end{aligned}
$$

Finally:

- If $x=0$, we get $y=0$ and the corresponding point is $(0,0).$

- If $x=-1$, we get $y=-3$ and the corresponding point is $(-1,-3).$

## q-72416 translated observed_raw

### q-72416 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve $2(x-2)(y+1)-3{(x-2)}^{2}=-(y+1)$ is the tangent vector to the curve perpendicular to the vector $j?$

$(2,2)$ and $(2,-4)$

**CORRECT** $(2,-1)$ and $(1,-4)$

$(2,-2)$ and $(2,-4)$

$(2,0)$ and $(3,-4)$

$(5,-1)$ and $(1,-1)$

First, we bring all variables to one side:

$$
\begin{aligned}2(x-2)(y+1)-3{(x-2)}^{2}=-(y+1) \\ 2(x-2)(y+1)-3{(x-2)}^{2}+(y+1) & =0\end{aligned}
$$

If we set $f(x,y)=2(x-2)(y+1)-3{(x-2)}^{2}+(y+1)$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}(2(x-2)(y+1)-3{(x-2)}^{2}+(y+1))i-\frac{∂}{∂x}(2(x-2)(y+1)-3{(x-2)}^{2}+(y+1))j \\  & =(2(x-2)+1)\,i-2((y+1)-3(x-2))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2(x-2)+1)\,i-2((y+1)-3(x-2))\,j)\cdot j & =0 \\ -2((y+1)-3(x-2)) & =0 \\ (y+1) & =3(x-2)\end{aligned}
$$

Substituting $(y+1)=3(x-2)$ into the equation of our curve gives:  

$$
\begin{aligned}2(x-2)(y+1)-3{(x-2)}^{2}+(y+1) & =0 \\ 2(x-2)(3(x-2))-3{(x-2)}^{2}+3(x-2) & =0 \\ 6{(x-2)}^{2}-3{(x-2)}^{2}+3(x-2) & =0 \\ 3{(x-2)}^{2}+3(x-2) & =0 \\ 3(x-2)((x-2)+1) & =0 \\ (x-2) & =0\,\text{or}\,(x-2)=-1\end{aligned}
$$

Finally:

- If $(x-2)=0$, we get $(y+1)=0$ and the corresponding point is $(2,-1).$

- If $(x-2)=-1$, we get $(y+1)=-3$ and the corresponding point is $(1,-4).$

## q-72416 translated observed_raw

### q-72416 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve $2(x+3)(y-3)-3{(x+3)}^{2}=-(y-3)$ is the tangent vector to the curve perpendicular to the vector $j?$

$(-3,6)$ and $(-3,0)$

**CORRECT** $(-3,3)$ and $(-4,0)$

$(-3,2)$ and $(-3,0)$

$(-3,4)$ and $(-2,0)$

$(0,3)$ and $(-4,3)$

First, we bring all variables to one side:

$$
\begin{aligned}2(x+3)(y-3)-3{(x+3)}^{2}=-(y-3) \\ 2(x+3)(y-3)-3{(x+3)}^{2}+(y-3) & =0\end{aligned}
$$

If we set $f(x,y)=2(x+3)(y-3)-3{(x+3)}^{2}+(y-3)$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}(2(x+3)(y-3)-3{(x+3)}^{2}+(y-3))i-\frac{∂}{∂x}(2(x+3)(y-3)-3{(x+3)}^{2}+(y-3))j \\  & =(2(x+3)+1)\,i-2((y-3)-3(x+3))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2(x+3)+1)\,i-2((y-3)-3(x+3))\,j)\cdot j & =0 \\ -2((y-3)-3(x+3)) & =0 \\ (y-3) & =3(x+3)\end{aligned}
$$

Substituting $(y-3)=3(x+3)$ into the equation of our curve gives:  

$$
\begin{aligned}2(x+3)(y-3)-3{(x+3)}^{2}+(y-3) & =0 \\ 2(x+3)(3(x+3))-3{(x+3)}^{2}+3(x+3) & =0 \\ 6{(x+3)}^{2}-3{(x+3)}^{2}+3(x+3) & =0 \\ 3{(x+3)}^{2}+3(x+3) & =0 \\ 3(x+3)((x+3)+1) & =0 \\ (x+3) & =0\,\text{or}\,(x+3)=-1\end{aligned}
$$

Finally:

- If $(x+3)=0$, we get $(y-3)=0$ and the corresponding point is $(-3,3).$

- If $(x+3)=-1$, we get $(y-3)=-3$ and the corresponding point is $(-4,0).$

## q-72416 translated observed_completed

### q-72416 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve $2(x-2)(y+1)-3{(x-2)}^{2}=-(y+1)$ is the tangent vector to the curve perpendicular to the vector $j?$

$(2,2)$ and $(2,-4)$

**CORRECT** $(2,-1)$ and $(1,-4)$

$(2,-2)$ and $(2,-4)$

$(2,0)$ and $(3,-4)$

$(5,-1)$ and $(1,-1)$

First, we bring all variables to one side:

$$
\begin{aligned}2(x-2)(y+1)-3{(x-2)}^{2}=-(y+1) \\ 2(x-2)(y+1)-3{(x-2)}^{2}+(y+1) & =0\end{aligned}
$$

If we set $f(x,y)=2(x-2)(y+1)-3{(x-2)}^{2}+(y+1)$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}(2(x-2)(y+1)-3{(x-2)}^{2}+(y+1))i-\frac{∂}{∂x}(2(x-2)(y+1)-3{(x-2)}^{2}+(y+1))j \\  & =(2(x-2)+1)\,i-2((y+1)-3(x-2))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2(x-2)+1)\,i-2((y+1)-3(x-2))\,j)\cdot j & =0 \\ -2((y+1)-3(x-2)) & =0 \\ (y+1) & =3(x-2)\end{aligned}
$$

Substituting $(y+1)=3(x-2)$ into the equation of our curve gives:  

$$
\begin{aligned}2(x-2)(y+1)-3{(x-2)}^{2}+(y+1) & =0 \\ 2(x-2)(3(x-2))-3{(x-2)}^{2}+3(x-2) & =0 \\ 6{(x-2)}^{2}-3{(x-2)}^{2}+3(x-2) & =0 \\ 3{(x-2)}^{2}+3(x-2) & =0 \\ 3(x-2)((x-2)+1) & =0 \\ (x-2) & =0\,\text{or}\,(x-2)=-1\end{aligned}
$$

Finally:

- If $(x-2)=0$, we get $(y+1)=0$ and the corresponding point is $(2,-1).$

- If $(x-2)=-1$, we get $(y+1)=-3$ and the corresponding point is $(1,-4).$

## q-72416 translated observed_completed

### q-72416 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve $2(x+3)(y-3)-3{(x+3)}^{2}=-(y-3)$ is the tangent vector to the curve perpendicular to the vector $j?$

$(-3,6)$ and $(-3,0)$

**CORRECT** $(-3,3)$ and $(-4,0)$

$(-3,2)$ and $(-3,0)$

$(-3,4)$ and $(-2,0)$

$(0,3)$ and $(-4,3)$

First, we bring all variables to one side:

$$
\begin{aligned}2(x+3)(y-3)-3{(x+3)}^{2}=-(y-3) \\ 2(x+3)(y-3)-3{(x+3)}^{2}+(y-3) & =0\end{aligned}
$$

If we set $f(x,y)=2(x+3)(y-3)-3{(x+3)}^{2}+(y-3)$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}(2(x+3)(y-3)-3{(x+3)}^{2}+(y-3))i-\frac{∂}{∂x}(2(x+3)(y-3)-3{(x+3)}^{2}+(y-3))j \\  & =(2(x+3)+1)\,i-2((y-3)-3(x+3))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2(x+3)+1)\,i-2((y-3)-3(x+3))\,j)\cdot j & =0 \\ -2((y-3)-3(x+3)) & =0 \\ (y-3) & =3(x+3)\end{aligned}
$$

Substituting $(y-3)=3(x+3)$ into the equation of our curve gives:  

$$
\begin{aligned}2(x+3)(y-3)-3{(x+3)}^{2}+(y-3) & =0 \\ 2(x+3)(3(x+3))-3{(x+3)}^{2}+3(x+3) & =0 \\ 6{(x+3)}^{2}-3{(x+3)}^{2}+3(x+3) & =0 \\ 3{(x+3)}^{2}+3(x+3) & =0 \\ 3(x+3)((x+3)+1) & =0 \\ (x+3) & =0\,\text{or}\,(x+3)=-1\end{aligned}
$$

Finally:

- If $(x+3)=0$, we get $(y-3)=0$ and the corresponding point is $(-3,3).$

- If $(x+3)=-1$, we get $(y-3)=-3$ and the corresponding point is $(-4,0).$

## q-72416 completed evidence only

### q-72416 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve $2xy-3{x}^{2}=-y$ is the tangent vector to the curve perpendicular to the vector $j?$

$(0,3)$ and $(0,-3)$

**CORRECT** $(0,0)$ and $(-1,-3)$

$(0,-1)$ and $(0,-3)$

$(0,1)$ and $(1,-3)$

$(3,0)$ and $(-1,0)$

First, we bring all variables to one side:

$$
\begin{aligned}2xy-3{x}^{2}=-y \\ 2xy-3{x}^{2}+y & =0\end{aligned}
$$

If we set $f(x,y)=2xy-3{x}^{2}+y$, our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}(2xy-3{x}^{2}+y)i-\frac{∂}{∂x}(2xy-3{x}^{2}+y)j \\  & =(2x+1)\,i-2(y-3x)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((2x+1)\,i-2(y-3x)\,j)\cdot j & =0 \\ -2(y-3x) & =0 \\ y & =3x\end{aligned}
$$

Substituting $y=3x$ into the equation of our curve gives:  

$$
\begin{aligned}2xy-3{x}^{2}+y & =0 \\ 2x(3x)-3{x}^{2}+3x & =0 \\ 6{x}^{2}-3{x}^{2}+3x & =0 \\ 3{x}^{2}+3x & =0 \\ 3x(x+1) & =0 \\ x & =0\,\text{or}\,x=-1\end{aligned}
$$

Finally:

- If $x=0$, we get $y=0$ and the corresponding point is $(0,0).$

- If $x=-1$, we get $y=-3$ and the corresponding point is $(-1,-3).$

## q-130225 original raw / hard

### q-130225 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve $2{x}^{2}-3{y}^{2}=-y$ is the tangent vector to the curve perpendicular to the vector $j?$

$(0,\frac{1}{3})$ only

$(-1,1)$ and $(0,0)$

$(-1,1)$ and $(1,1)$

$(1,1)$ only

**CORRECT** $(0,0)$ and $(0,\frac{1}{3})$

First, we bring all variables to one side:

$$
\begin{aligned}2{x}^{2}-3{y}^{2} & =-y \\ 2{x}^{2}-3{y}^{2}+y & =0\end{aligned}
$$

If we set $f(x,y)=2{x}^{2}-3{y}^{2}+y,$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}(2{x}^{2}-3{y}^{2}+y)\,i-\frac{∂}{∂x}(2{x}^{2}-3{y}^{2}+y)\,j \\  & =(-6y+1)\,i-4x\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((-6y+1)\,i-4x\,j)\cdot j & =0 \\ -4x & =0 \\ x & =0\end{aligned}
$$

Substituting $x=0$ into the equation of our curve gives

$$
\begin{aligned}2{x}^{2}-3{y}^{2} & =-y \\ 2({0}^{2})-3{y}^{2} & =-y \\ 3{y}^{2}-y & =0 \\ y(3y-1) & =0 \\ y & =0,\frac{1}{3}.\end{aligned}
$$

Finally, the corresponding points are $(0,0)$ and $(0,\frac{1}{3}).$

## q-130225 translated observed_raw

### q-130225 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve $2{(x-2)}^{2}-3{(y+1)}^{2}=-(y+1)$ is the tangent vector to the curve perpendicular to the vector $j?$

$(2,- \frac{2}{3})$ only

$(1,0)$ and $(2,-1)$

$(1,0)$ and $(3,0)$

$(3,0)$ only

**CORRECT** $(2,-1)$ and $(2,- \frac{2}{3})$

First, we bring all variables to one side:

$$
\begin{aligned}2{(x-2)}^{2}-3{(y+1)}^{2} & =-(y+1) \\ 2{(x-2)}^{2}-3{(y+1)}^{2}+(y+1) & =0\end{aligned}
$$

If we set $f(x,y)=2{(x-2)}^{2}-3{(y+1)}^{2}+(y+1),$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}(2{(x-2)}^{2}-3{(y+1)}^{2}+(y+1))\,i-\frac{∂}{∂x}(2{(x-2)}^{2}-3{(y+1)}^{2}+(y+1))\,j \\  & =(-6(y+1)+1)\,i-4(x-2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((-6(y+1)+1)\,i-4(x-2)\,j)\cdot j & =0 \\ -4(x-2) & =0 \\ (x-2) & =0\end{aligned}
$$

Substituting $(x-2)=0$ into the equation of our curve gives

$$
\begin{aligned}2{(x-2)}^{2}-3{(y+1)}^{2} & =-(y+1) \\ 2({0}^{2})-3{(y+1)}^{2} & =-(y+1) \\ 3{(y+1)}^{2}-(y+1) & =0 \\ (y+1)(3(y+1)-1) & =0 \\ (y+1) & =0,\frac{1}{3}.\end{aligned}
$$

Finally, the corresponding points are $(2,-1)$ and $(2,- \frac{2}{3}).$

## q-130225 translated observed_raw

### q-130225 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve $2{(x+3)}^{2}-3{(y-3)}^{2}=-(y-3)$ is the tangent vector to the curve perpendicular to the vector $j?$

$(-3,\frac{10}{3})$ only

$(-4,4)$ and $(-3,3)$

$(-4,4)$ and $(-2,4)$

$(-2,4)$ only

**CORRECT** $(-3,3)$ and $(-3,\frac{10}{3})$

First, we bring all variables to one side:

$$
\begin{aligned}2{(x+3)}^{2}-3{(y-3)}^{2} & =-(y-3) \\ 2{(x+3)}^{2}-3{(y-3)}^{2}+(y-3) & =0\end{aligned}
$$

If we set $f(x,y)=2{(x+3)}^{2}-3{(y-3)}^{2}+(y-3),$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}(2{(x+3)}^{2}-3{(y-3)}^{2}+(y-3))\,i-\frac{∂}{∂x}(2{(x+3)}^{2}-3{(y-3)}^{2}+(y-3))\,j \\  & =(-6(y-3)+1)\,i-4(x+3)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((-6(y-3)+1)\,i-4(x+3)\,j)\cdot j & =0 \\ -4(x+3) & =0 \\ (x+3) & =0\end{aligned}
$$

Substituting $(x+3)=0$ into the equation of our curve gives

$$
\begin{aligned}2{(x+3)}^{2}-3{(y-3)}^{2} & =-(y-3) \\ 2({0}^{2})-3{(y-3)}^{2} & =-(y-3) \\ 3{(y-3)}^{2}-(y-3) & =0 \\ (y-3)(3(y-3)-1) & =0 \\ (y-3) & =0,\frac{1}{3}.\end{aligned}
$$

Finally, the corresponding points are $(-3,3)$ and $(-3,\frac{10}{3}).$

## q-130225 translated observed_completed

### q-130225 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve $2{(x-2)}^{2}-3{(y+1)}^{2}=-(y+1)$ is the tangent vector to the curve perpendicular to the vector $j?$

$(2,- \frac{2}{3})$ only

$(1,0)$ and $(2,-1)$

$(1,0)$ and $(3,0)$

$(3,0)$ only

**CORRECT** $(2,-1)$ and $(2,- \frac{2}{3})$

First, we bring all variables to one side:

$$
\begin{aligned}2{(x-2)}^{2}-3{(y+1)}^{2} & =-(y+1) \\ 2{(x-2)}^{2}-3{(y+1)}^{2}+(y+1) & =0\end{aligned}
$$

If we set $f(x,y)=2{(x-2)}^{2}-3{(y+1)}^{2}+(y+1),$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}(2{(x-2)}^{2}-3{(y+1)}^{2}+(y+1))\,i-\frac{∂}{∂x}(2{(x-2)}^{2}-3{(y+1)}^{2}+(y+1))\,j \\  & =(-6(y+1)+1)\,i-4(x-2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((-6(y+1)+1)\,i-4(x-2)\,j)\cdot j & =0 \\ -4(x-2) & =0 \\ (x-2) & =0\end{aligned}
$$

Substituting $(x-2)=0$ into the equation of our curve gives

$$
\begin{aligned}2{(x-2)}^{2}-3{(y+1)}^{2} & =-(y+1) \\ 2({0}^{2})-3{(y+1)}^{2} & =-(y+1) \\ 3{(y+1)}^{2}-(y+1) & =0 \\ (y+1)(3(y+1)-1) & =0 \\ (y+1) & =0,\frac{1}{3}.\end{aligned}
$$

Finally, the corresponding points are $(2,-1)$ and $(2,- \frac{2}{3}).$

## q-130225 translated observed_completed

### q-130225 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve $2{(x+3)}^{2}-3{(y-3)}^{2}=-(y-3)$ is the tangent vector to the curve perpendicular to the vector $j?$

$(-3,\frac{10}{3})$ only

$(-4,4)$ and $(-3,3)$

$(-4,4)$ and $(-2,4)$

$(-2,4)$ only

**CORRECT** $(-3,3)$ and $(-3,\frac{10}{3})$

First, we bring all variables to one side:

$$
\begin{aligned}2{(x+3)}^{2}-3{(y-3)}^{2} & =-(y-3) \\ 2{(x+3)}^{2}-3{(y-3)}^{2}+(y-3) & =0\end{aligned}
$$

If we set $f(x,y)=2{(x+3)}^{2}-3{(y-3)}^{2}+(y-3),$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}(2{(x+3)}^{2}-3{(y-3)}^{2}+(y-3))\,i-\frac{∂}{∂x}(2{(x+3)}^{2}-3{(y-3)}^{2}+(y-3))\,j \\  & =(-6(y-3)+1)\,i-4(x+3)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((-6(y-3)+1)\,i-4(x+3)\,j)\cdot j & =0 \\ -4(x+3) & =0 \\ (x+3) & =0\end{aligned}
$$

Substituting $(x+3)=0$ into the equation of our curve gives

$$
\begin{aligned}2{(x+3)}^{2}-3{(y-3)}^{2} & =-(y-3) \\ 2({0}^{2})-3{(y-3)}^{2} & =-(y-3) \\ 3{(y-3)}^{2}-(y-3) & =0 \\ (y-3)(3(y-3)-1) & =0 \\ (y-3) & =0,\frac{1}{3}.\end{aligned}
$$

Finally, the corresponding points are $(-3,3)$ and $(-3,\frac{10}{3}).$

## q-130225 completed evidence only

### q-130225 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve $2{x}^{2}-3{y}^{2}=-y$ is the tangent vector to the curve perpendicular to the vector $j?$

$(0,\frac{1}{3})$ only

$(-1,1)$ and $(0,0)$

$(-1,1)$ and $(1,1)$

$(1,1)$ only

**CORRECT** $(0,0)$ and $(0,\frac{1}{3})$

First, we bring all variables to one side:

$$
\begin{aligned}2{x}^{2}-3{y}^{2} & =-y \\ 2{x}^{2}-3{y}^{2}+y & =0\end{aligned}
$$

If we set $f(x,y)=2{x}^{2}-3{y}^{2}+y,$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}(2{x}^{2}-3{y}^{2}+y)\,i-\frac{∂}{∂x}(2{x}^{2}-3{y}^{2}+y)\,j \\  & =(-6y+1)\,i-4x\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $j,$ we must have $t\cdot j=0.$

$$
\begin{aligned}t(x,y)\cdot j & =0 \\ ((-6y+1)\,i-4x\,j)\cdot j & =0 \\ -4x & =0 \\ x & =0\end{aligned}
$$

Substituting $x=0$ into the equation of our curve gives

$$
\begin{aligned}2{x}^{2}-3{y}^{2} & =-y \\ 2({0}^{2})-3{y}^{2} & =-y \\ 3{y}^{2}-y & =0 \\ y(3y-1) & =0 \\ y & =0,\frac{1}{3}.\end{aligned}
$$

Finally, the corresponding points are $(0,0)$ and $(0,\frac{1}{3}).$

## q-72427 original raw / hard

### q-72427 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${y}^{2}+2x=2xy+2y-2$ is the tangent vector to the curve perpendicular to the vector $i?$

$(1,1)$ and $(2,0)$

$(-1,2)$ and $(1,0)$

$(1,-2)$ and $(0,1)$

**CORRECT** $(1,2)$ and $(-1,0)$

$(-1,-2)$ and $(1,0)$

First, we bring all variables to one side:

$$
\begin{aligned}{y}^{2}+2x & =2xy+2y-2 \\ {y}^{2}+2x-2xy-2y & =-2\end{aligned}
$$

If we set $f(x,y)={y}^{2}+2x-2xy-2y$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({y}^{2}+2x-2xy-2y)i-\frac{∂}{∂x}({y}^{2}+2x-2xy-2y)j \\  & =(2y-2x-2)\,i-(2-2y)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ ((2y-2x-2)\,i-(2-2y)\,j)\cdot i & =0 \\ 2y-2x-2 & =0 \\ 2(y-x-1) & =0 \\ y & =x+1\end{aligned}
$$

Substituting $y=x+1$ into the equation of our curve gives:  

$$
\begin{aligned}{y}^{2}+2x-2xy-2y & =-2 \\ (x+1)^{2}+2x-2x(x+1)-2(x+1)+2 & =0 \\ (x+1)^{2}-2x(x+1)-2(x+1)+2(x+1) & =0 \\ (x+1)^{2}-2x(x+1)-\cancel{2(x+1)}+\cancel{2(x+1)} & =0 \\ (x+1)^{2}-2x(x+1) & =0 \\ (x+1)(x+1-2x) & =0 \\ (x+1)(-x+1) & =0 \\ x & =\pm 1\end{aligned}
$$

Finally:

- If $x=1$, we get $y=2$ and the corresponding point is $(1,2).$

- If $x=-1$, we get $y=0$ and the corresponding point is $(-1,0).$

## q-72427 translated observed_raw

### q-72427 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(y+1)}^{2}+2(x-2)=2(x-2)(y+1)+2(y+1)-2$ is the tangent vector to the curve perpendicular to the vector $i?$

$(3,0)$ and $(4,-1)$

$(1,1)$ and $(3,-1)$

$(3,-3)$ and $(2,0)$

**CORRECT** $(3,1)$ and $(1,-1)$

$(1,-3)$ and $(3,-1)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y+1)}^{2}+2(x-2) & =2(x-2)(y+1)+2(y+1)-2 \\ {(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1) & =-2\end{aligned}
$$

If we set $f(x,y)={(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1)$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1))i-\frac{∂}{∂x}({(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1))j \\  & =(2(y+1)-2(x-2)-2)\,i-(2-2(y+1))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ ((2(y+1)-2(x-2)-2)\,i-(2-2(y+1))\,j)\cdot i & =0 \\ 2(y+1)-2(x-2)-2 & =0 \\ 2((y+1)-(x-2)-1) & =0 \\ (y+1) & =(x-2)+1\end{aligned}
$$

Substituting $(y+1)=(x-2)+1$ into the equation of our curve gives:  

$$
\begin{aligned}{(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1) & =-2 \\ ((x-2)+1)^{2}+2(x-2)-2(x-2)((x-2)+1)-2((x-2)+1)+2 & =0 \\ ((x-2)+1)^{2}-2(x-2)((x-2)+1)-2((x-2)+1)+2((x-2)+1) & =0 \\ ((x-2)+1)^{2}-2(x-2)((x-2)+1)-\cancel{2((x-2)+1)}+\cancel{2((x-2)+1)} & =0 \\ ((x-2)+1)^{2}-2(x-2)((x-2)+1) & =0 \\ ((x-2)+1)((x-2)+1-2(x-2)) & =0 \\ ((x-2)+1)(-(x-2)+1) & =0 \\ (x-2) & =\pm 1\end{aligned}
$$

Finally:

- If $(x-2)=1$, we get $(y+1)=2$ and the corresponding point is $(3,1).$

- If $(x-2)=-1$, we get $(y+1)=0$ and the corresponding point is $(1,-1).$

## q-72427 translated observed_raw

### q-72427 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(y-3)}^{2}+2(x+3)=2(x+3)(y-3)+2(y-3)-2$ is the tangent vector to the curve perpendicular to the vector $i?$

$(-2,4)$ and $(-1,3)$

$(-4,5)$ and $(-2,3)$

$(-2,1)$ and $(-3,4)$

**CORRECT** $(-2,5)$ and $(-4,3)$

$(-4,1)$ and $(-2,3)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y-3)}^{2}+2(x+3) & =2(x+3)(y-3)+2(y-3)-2 \\ {(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3) & =-2\end{aligned}
$$

If we set $f(x,y)={(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3)$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3))i-\frac{∂}{∂x}({(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3))j \\  & =(2(y-3)-2(x+3)-2)\,i-(2-2(y-3))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ ((2(y-3)-2(x+3)-2)\,i-(2-2(y-3))\,j)\cdot i & =0 \\ 2(y-3)-2(x+3)-2 & =0 \\ 2((y-3)-(x+3)-1) & =0 \\ (y-3) & =(x+3)+1\end{aligned}
$$

Substituting $(y-3)=(x+3)+1$ into the equation of our curve gives:  

$$
\begin{aligned}{(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3) & =-2 \\ ((x+3)+1)^{2}+2(x+3)-2(x+3)((x+3)+1)-2((x+3)+1)+2 & =0 \\ ((x+3)+1)^{2}-2(x+3)((x+3)+1)-2((x+3)+1)+2((x+3)+1) & =0 \\ ((x+3)+1)^{2}-2(x+3)((x+3)+1)-\cancel{2((x+3)+1)}+\cancel{2((x+3)+1)} & =0 \\ ((x+3)+1)^{2}-2(x+3)((x+3)+1) & =0 \\ ((x+3)+1)((x+3)+1-2(x+3)) & =0 \\ ((x+3)+1)(-(x+3)+1) & =0 \\ (x+3) & =\pm 1\end{aligned}
$$

Finally:

- If $(x+3)=1$, we get $(y-3)=2$ and the corresponding point is $(-2,5).$

- If $(x+3)=-1$, we get $(y-3)=0$ and the corresponding point is $(-4,3).$

## q-72427 translated observed_completed

### q-72427 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(y+1)}^{2}+2(x-2)=2(x-2)(y+1)+2(y+1)-2$ is the tangent vector to the curve perpendicular to the vector $i?$

$(3,0)$ and $(4,-1)$

$(1,1)$ and $(3,-1)$

$(3,-3)$ and $(2,0)$

**CORRECT** $(3,1)$ and $(1,-1)$

$(1,-3)$ and $(3,-1)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y+1)}^{2}+2(x-2) & =2(x-2)(y+1)+2(y+1)-2 \\ {(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1) & =-2\end{aligned}
$$

If we set $f(x,y)={(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1)$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1))i-\frac{∂}{∂x}({(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1))j \\  & =(2(y+1)-2(x-2)-2)\,i-(2-2(y+1))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ ((2(y+1)-2(x-2)-2)\,i-(2-2(y+1))\,j)\cdot i & =0 \\ 2(y+1)-2(x-2)-2 & =0 \\ 2((y+1)-(x-2)-1) & =0 \\ (y+1) & =(x-2)+1\end{aligned}
$$

Substituting $(y+1)=(x-2)+1$ into the equation of our curve gives:  

$$
\begin{aligned}{(y+1)}^{2}+2(x-2)-2(x-2)(y+1)-2(y+1) & =-2 \\ ((x-2)+1)^{2}+2(x-2)-2(x-2)((x-2)+1)-2((x-2)+1)+2 & =0 \\ ((x-2)+1)^{2}-2(x-2)((x-2)+1)-2((x-2)+1)+2((x-2)+1) & =0 \\ ((x-2)+1)^{2}-2(x-2)((x-2)+1)-\cancel{2((x-2)+1)}+\cancel{2((x-2)+1)} & =0 \\ ((x-2)+1)^{2}-2(x-2)((x-2)+1) & =0 \\ ((x-2)+1)((x-2)+1-2(x-2)) & =0 \\ ((x-2)+1)(-(x-2)+1) & =0 \\ (x-2) & =\pm 1\end{aligned}
$$

Finally:

- If $(x-2)=1$, we get $(y+1)=2$ and the corresponding point is $(3,1).$

- If $(x-2)=-1$, we get $(y+1)=0$ and the corresponding point is $(1,-1).$

## q-72427 translated observed_completed

### q-72427 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(y-3)}^{2}+2(x+3)=2(x+3)(y-3)+2(y-3)-2$ is the tangent vector to the curve perpendicular to the vector $i?$

$(-2,4)$ and $(-1,3)$

$(-4,5)$ and $(-2,3)$

$(-2,1)$ and $(-3,4)$

**CORRECT** $(-2,5)$ and $(-4,3)$

$(-4,1)$ and $(-2,3)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y-3)}^{2}+2(x+3) & =2(x+3)(y-3)+2(y-3)-2 \\ {(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3) & =-2\end{aligned}
$$

If we set $f(x,y)={(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3)$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3))i-\frac{∂}{∂x}({(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3))j \\  & =(2(y-3)-2(x+3)-2)\,i-(2-2(y-3))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ ((2(y-3)-2(x+3)-2)\,i-(2-2(y-3))\,j)\cdot i & =0 \\ 2(y-3)-2(x+3)-2 & =0 \\ 2((y-3)-(x+3)-1) & =0 \\ (y-3) & =(x+3)+1\end{aligned}
$$

Substituting $(y-3)=(x+3)+1$ into the equation of our curve gives:  

$$
\begin{aligned}{(y-3)}^{2}+2(x+3)-2(x+3)(y-3)-2(y-3) & =-2 \\ ((x+3)+1)^{2}+2(x+3)-2(x+3)((x+3)+1)-2((x+3)+1)+2 & =0 \\ ((x+3)+1)^{2}-2(x+3)((x+3)+1)-2((x+3)+1)+2((x+3)+1) & =0 \\ ((x+3)+1)^{2}-2(x+3)((x+3)+1)-\cancel{2((x+3)+1)}+\cancel{2((x+3)+1)} & =0 \\ ((x+3)+1)^{2}-2(x+3)((x+3)+1) & =0 \\ ((x+3)+1)((x+3)+1-2(x+3)) & =0 \\ ((x+3)+1)(-(x+3)+1) & =0 \\ (x+3) & =\pm 1\end{aligned}
$$

Finally:

- If $(x+3)=1$, we get $(y-3)=2$ and the corresponding point is $(-2,5).$

- If $(x+3)=-1$, we get $(y-3)=0$ and the corresponding point is $(-4,3).$

## q-72427 completed evidence only

### q-72427 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${y}^{2}+2x=2xy+2y-2$ is the tangent vector to the curve perpendicular to the vector $i?$

$(1,1)$ and $(2,0)$

$(-1,2)$ and $(1,0)$

$(1,-2)$ and $(0,1)$

**CORRECT** $(1,2)$ and $(-1,0)$

$(-1,-2)$ and $(1,0)$

First, we bring all variables to one side:

$$
\begin{aligned}{y}^{2}+2x & =2xy+2y-2 \\ {y}^{2}+2x-2xy-2y & =-2\end{aligned}
$$

If we set $f(x,y)={y}^{2}+2x-2xy-2y$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({y}^{2}+2x-2xy-2y)i-\frac{∂}{∂x}({y}^{2}+2x-2xy-2y)j \\  & =(2y-2x-2)\,i-(2-2y)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ ((2y-2x-2)\,i-(2-2y)\,j)\cdot i & =0 \\ 2y-2x-2 & =0 \\ 2(y-x-1) & =0 \\ y & =x+1\end{aligned}
$$

Substituting $y=x+1$ into the equation of our curve gives:  

$$
\begin{aligned}{y}^{2}+2x-2xy-2y & =-2 \\ (x+1)^{2}+2x-2x(x+1)-2(x+1)+2 & =0 \\ (x+1)^{2}-2x(x+1)-2(x+1)+2(x+1) & =0 \\ (x+1)^{2}-2x(x+1)-\cancel{2(x+1)}+\cancel{2(x+1)} & =0 \\ (x+1)^{2}-2x(x+1) & =0 \\ (x+1)(x+1-2x) & =0 \\ (x+1)(-x+1) & =0 \\ x & =\pm 1\end{aligned}
$$

Finally:

- If $x=1$, we get $y=2$ and the corresponding point is $(1,2).$

- If $x=-1$, we get $y=0$ and the corresponding point is $(-1,0).$

## q-130209 original raw / hard

### q-130209 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which point on the curve $2{x}^{2}=y+1$ is the tangent vector to the curve perpendicular to the vector $i+j?$

(0,-1)

**CORRECT** (-\frac{1}{4},-\frac{7}{8})

(1,1)

(\frac{1}{2},-\frac{1}{2})

(-1,1)

First, we bring all variables to one side:

$$
\begin{aligned}2{x}^{2} & =y+1 \\ 2{x}^{2}-y & =1\end{aligned}
$$

If we set $f(x,y)=2{x}^{2}-y,$ our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}(2{x}^{2}-y)\,i-\frac{∂}{∂x}(2{x}^{2}-y)\,j \\  & =-i-4x\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i+j,$ we must have $t\cdot (i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (i+j) & =0 \\ (-i-4x\,j)\cdot (i+j) & =0 \\ -1-4x & =0 \\ x & =-\frac{1}{4}\end{aligned}
$$

Substituting $x=-\frac{1}{4}$ into the equation of our curve gives

$$
\begin{aligned}2{x}^{2} & =y+1 \\ 2{(-\frac{1}{4})}^{2} & =y+1 \\ \frac{1}{8} & =y+1 \\ y & =-\frac{7}{8}.\end{aligned}
$$

Finally, the corresponding point is $(-\frac{1}{4},-\frac{7}{8}).$

## q-130209 translated observed_raw

### q-130209 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which point on the curve $2{(x-2)}^{2}=(y+1)+1$ is the tangent vector to the curve perpendicular to the vector $i+j?$

(2,-2)

**CORRECT** (\frac{7}{4},- \frac{15}{8})

(3,0)

(\frac{5}{2},- \frac{3}{2})

(1,0)

First, we bring all variables to one side:

$$
\begin{aligned}2{(x-2)}^{2} & =(y+1)+1 \\ 2{(x-2)}^{2}-(y+1) & =1\end{aligned}
$$

If we set $f(x,y)=2{(x-2)}^{2}-(y+1),$ our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}(2{(x-2)}^{2}-(y+1))\,i-\frac{∂}{∂x}(2{(x-2)}^{2}-(y+1))\,j \\  & =-i-4(x-2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i+j,$ we must have $t\cdot (i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (i+j) & =0 \\ (-i-4(x-2)\,j)\cdot (i+j) & =0 \\ -1-4(x-2) & =0 \\ (x-2) & =-\frac{1}{4}\end{aligned}
$$

Substituting $(x-2)=-\frac{1}{4}$ into the equation of our curve gives

$$
\begin{aligned}2{(x-2)}^{2} & =(y+1)+1 \\ 2{(-\frac{1}{4})}^{2} & =(y+1)+1 \\ \frac{1}{8} & =(y+1)+1 \\ (y+1) & =-\frac{7}{8}.\end{aligned}
$$

Finally, the corresponding point is $(\frac{7}{4},- \frac{15}{8}).$

## q-130209 translated observed_raw

### q-130209 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which point on the curve $2{(x+3)}^{2}=(y-3)+1$ is the tangent vector to the curve perpendicular to the vector $i+j?$

(-3,2)

**CORRECT** (- \frac{13}{4},\frac{17}{8})

(-2,4)

(- \frac{5}{2},\frac{5}{2})

(-4,4)

First, we bring all variables to one side:

$$
\begin{aligned}2{(x+3)}^{2} & =(y-3)+1 \\ 2{(x+3)}^{2}-(y-3) & =1\end{aligned}
$$

If we set $f(x,y)=2{(x+3)}^{2}-(y-3),$ our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}(2{(x+3)}^{2}-(y-3))\,i-\frac{∂}{∂x}(2{(x+3)}^{2}-(y-3))\,j \\  & =-i-4(x+3)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i+j,$ we must have $t\cdot (i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (i+j) & =0 \\ (-i-4(x+3)\,j)\cdot (i+j) & =0 \\ -1-4(x+3) & =0 \\ (x+3) & =-\frac{1}{4}\end{aligned}
$$

Substituting $(x+3)=-\frac{1}{4}$ into the equation of our curve gives

$$
\begin{aligned}2{(x+3)}^{2} & =(y-3)+1 \\ 2{(-\frac{1}{4})}^{2} & =(y-3)+1 \\ \frac{1}{8} & =(y-3)+1 \\ (y-3) & =-\frac{7}{8}.\end{aligned}
$$

Finally, the corresponding point is $(- \frac{13}{4},\frac{17}{8}).$

## q-130209 translated observed_completed

### q-130209 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which point on the curve $2{(x-2)}^{2}=(y+1)+1$ is the tangent vector to the curve perpendicular to the vector $i+j?$

(2,-2)

**CORRECT** (\frac{7}{4},- \frac{15}{8})

(3,0)

(\frac{5}{2},- \frac{3}{2})

(1,0)

First, we bring all variables to one side:

$$
\begin{aligned}2{(x-2)}^{2} & =(y+1)+1 \\ 2{(x-2)}^{2}-(y+1) & =1\end{aligned}
$$

If we set $f(x,y)=2{(x-2)}^{2}-(y+1),$ our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}(2{(x-2)}^{2}-(y+1))\,i-\frac{∂}{∂x}(2{(x-2)}^{2}-(y+1))\,j \\  & =-i-4(x-2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i+j,$ we must have $t\cdot (i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (i+j) & =0 \\ (-i-4(x-2)\,j)\cdot (i+j) & =0 \\ -1-4(x-2) & =0 \\ (x-2) & =-\frac{1}{4}\end{aligned}
$$

Substituting $(x-2)=-\frac{1}{4}$ into the equation of our curve gives

$$
\begin{aligned}2{(x-2)}^{2} & =(y+1)+1 \\ 2{(-\frac{1}{4})}^{2} & =(y+1)+1 \\ \frac{1}{8} & =(y+1)+1 \\ (y+1) & =-\frac{7}{8}.\end{aligned}
$$

Finally, the corresponding point is $(\frac{7}{4},- \frac{15}{8}).$

## q-130209 translated observed_completed

### q-130209 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which point on the curve $2{(x+3)}^{2}=(y-3)+1$ is the tangent vector to the curve perpendicular to the vector $i+j?$

(-3,2)

**CORRECT** (- \frac{13}{4},\frac{17}{8})

(-2,4)

(- \frac{5}{2},\frac{5}{2})

(-4,4)

First, we bring all variables to one side:

$$
\begin{aligned}2{(x+3)}^{2} & =(y-3)+1 \\ 2{(x+3)}^{2}-(y-3) & =1\end{aligned}
$$

If we set $f(x,y)=2{(x+3)}^{2}-(y-3),$ our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}(2{(x+3)}^{2}-(y-3))\,i-\frac{∂}{∂x}(2{(x+3)}^{2}-(y-3))\,j \\  & =-i-4(x+3)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i+j,$ we must have $t\cdot (i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (i+j) & =0 \\ (-i-4(x+3)\,j)\cdot (i+j) & =0 \\ -1-4(x+3) & =0 \\ (x+3) & =-\frac{1}{4}\end{aligned}
$$

Substituting $(x+3)=-\frac{1}{4}$ into the equation of our curve gives

$$
\begin{aligned}2{(x+3)}^{2} & =(y-3)+1 \\ 2{(-\frac{1}{4})}^{2} & =(y-3)+1 \\ \frac{1}{8} & =(y-3)+1 \\ (y-3) & =-\frac{7}{8}.\end{aligned}
$$

Finally, the corresponding point is $(- \frac{13}{4},\frac{17}{8}).$

## q-130209 completed evidence only

### q-130209 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which point on the curve $2{x}^{2}=y+1$ is the tangent vector to the curve perpendicular to the vector $i+j?$

(0,-1)

**CORRECT** (-\frac{1}{4},-\frac{7}{8})

(1,1)

(\frac{1}{2},-\frac{1}{2})

(-1,1)

First, we bring all variables to one side:

$$
\begin{aligned}2{x}^{2} & =y+1 \\ 2{x}^{2}-y & =1\end{aligned}
$$

If we set $f(x,y)=2{x}^{2}-y,$ our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}(2{x}^{2}-y)\,i-\frac{∂}{∂x}(2{x}^{2}-y)\,j \\  & =-i-4x\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i+j,$ we must have $t\cdot (i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (i+j) & =0 \\ (-i-4x\,j)\cdot (i+j) & =0 \\ -1-4x & =0 \\ x & =-\frac{1}{4}\end{aligned}
$$

Substituting $x=-\frac{1}{4}$ into the equation of our curve gives

$$
\begin{aligned}2{x}^{2} & =y+1 \\ 2{(-\frac{1}{4})}^{2} & =y+1 \\ \frac{1}{8} & =y+1 \\ y & =-\frac{7}{8}.\end{aligned}
$$

Finally, the corresponding point is $(-\frac{1}{4},-\frac{7}{8}).$

## q-130217 original raw / hard

### q-130217 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${x}^{2}+{y}^{2}=2y-2x$ is the tangent vector to the curve perpendicular to the vector $-i+j?$

$(0,2)$ only

**CORRECT** $(-2,2)$ and $(0,0)$

$(0,0)$ only

$(-2,0)$ and $(0,2)$

$(-2,0)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}+{y}^{2} & =2y-2x \\ {x}^{2}+{y}^{2}+2x-2y & =0\end{aligned}
$$

If we set $f(x,y)={x}^{2}+{y}^{2}+2x-2y,$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({x}^{2}+{y}^{2}+2x-2y)\,i-\frac{∂}{∂x}({x}^{2}+{y}^{2}+2x-2y)\,j \\  & =(2y-2)\,i-(2x+2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $-i+j,$ we must have $t\cdot (-i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (-i+j) & =0 \\ ((2y-2)\,i-(2x+2)\,j)\cdot (-i+j) & =0 \\ -(2y-2)-(2x+2) & =0 \\ -2y-2x & =0 \\ y & =-x\end{aligned}
$$

Substituting $y=-x$ into the equation of our curve gives

$$
\begin{aligned}{x}^{2}+{y}^{2} & =2y-2x \\ {x}^{2}+(-x)^{2} & =2(-x)-2x \\ 2{x}^{2} & =-4x \\ 2{x}^{2}+4x & =0 \\ 2x(x+2) & =0 \\ x & =-2,0.\end{aligned}
$$

Finally:

- For $x=-2,$ we get $y=2,$ and the corresponding point is $(-2,2).$

- For $x=0,$ we get $y=0,$ and the corresponding point is $(0,0).$

## q-130217 translated observed_raw

### q-130217 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(x-2)}^{2}+{(y+1)}^{2}=2(y+1)-2(x-2)$ is the tangent vector to the curve perpendicular to the vector $-i+j?$

$(2,1)$ only

**CORRECT** $(0,1)$ and $(2,-1)$

$(2,-1)$ only

$(0,-1)$ and $(2,1)$

$(0,-1)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{(x-2)}^{2}+{(y+1)}^{2} & =2(y+1)-2(x-2) \\ {(x-2)}^{2}+{(y+1)}^{2}+2(x-2)-2(y+1) & =0\end{aligned}
$$

If we set $f(x,y)={(x-2)}^{2}+{(y+1)}^{2}+2(x-2)-2(y+1),$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(x-2)}^{2}+{(y+1)}^{2}+2(x-2)-2(y+1))\,i-\frac{∂}{∂x}({(x-2)}^{2}+{(y+1)}^{2}+2(x-2)-2(y+1))\,j \\  & =(2(y+1)-2)\,i-(2(x-2)+2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $-i+j,$ we must have $t\cdot (-i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (-i+j) & =0 \\ ((2(y+1)-2)\,i-(2(x-2)+2)\,j)\cdot (-i+j) & =0 \\ -(2(y+1)-2)-(2(x-2)+2) & =0 \\ -2(y+1)-2(x-2) & =0 \\ (y+1) & =-(x-2)\end{aligned}
$$

Substituting $(y+1)=-(x-2)$ into the equation of our curve gives

$$
\begin{aligned}{(x-2)}^{2}+{(y+1)}^{2} & =2(y+1)-2(x-2) \\ {(x-2)}^{2}+(-(x-2))^{2} & =2(-(x-2))-2(x-2) \\ 2{(x-2)}^{2} & =-4(x-2) \\ 2{(x-2)}^{2}+4(x-2) & =0 \\ 2(x-2)((x-2)+2) & =0 \\ (x-2) & =-2,0.\end{aligned}
$$

Finally:

- For $(x-2)=-2,$ we get $(y+1)=2,$ and the corresponding point is $(0,1).$

- For $(x-2)=0,$ we get $(y+1)=0,$ and the corresponding point is $(2,-1).$

## q-130217 translated observed_raw

### q-130217 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(x+3)}^{2}+{(y-3)}^{2}=2(y-3)-2(x+3)$ is the tangent vector to the curve perpendicular to the vector $-i+j?$

$(-3,5)$ only

**CORRECT** $(-5,5)$ and $(-3,3)$

$(-3,3)$ only

$(-5,3)$ and $(-3,5)$

$(-5,3)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{(x+3)}^{2}+{(y-3)}^{2} & =2(y-3)-2(x+3) \\ {(x+3)}^{2}+{(y-3)}^{2}+2(x+3)-2(y-3) & =0\end{aligned}
$$

If we set $f(x,y)={(x+3)}^{2}+{(y-3)}^{2}+2(x+3)-2(y-3),$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(x+3)}^{2}+{(y-3)}^{2}+2(x+3)-2(y-3))\,i-\frac{∂}{∂x}({(x+3)}^{2}+{(y-3)}^{2}+2(x+3)-2(y-3))\,j \\  & =(2(y-3)-2)\,i-(2(x+3)+2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $-i+j,$ we must have $t\cdot (-i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (-i+j) & =0 \\ ((2(y-3)-2)\,i-(2(x+3)+2)\,j)\cdot (-i+j) & =0 \\ -(2(y-3)-2)-(2(x+3)+2) & =0 \\ -2(y-3)-2(x+3) & =0 \\ (y-3) & =-(x+3)\end{aligned}
$$

Substituting $(y-3)=-(x+3)$ into the equation of our curve gives

$$
\begin{aligned}{(x+3)}^{2}+{(y-3)}^{2} & =2(y-3)-2(x+3) \\ {(x+3)}^{2}+(-(x+3))^{2} & =2(-(x+3))-2(x+3) \\ 2{(x+3)}^{2} & =-4(x+3) \\ 2{(x+3)}^{2}+4(x+3) & =0 \\ 2(x+3)((x+3)+2) & =0 \\ (x+3) & =-2,0.\end{aligned}
$$

Finally:

- For $(x+3)=-2,$ we get $(y-3)=2,$ and the corresponding point is $(-5,5).$

- For $(x+3)=0,$ we get $(y-3)=0,$ and the corresponding point is $(-3,3).$

## q-130217 translated observed_completed

### q-130217 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(x-2)}^{2}+{(y+1)}^{2}=2(y+1)-2(x-2)$ is the tangent vector to the curve perpendicular to the vector $-i+j?$

$(2,1)$ only

**CORRECT** $(0,1)$ and $(2,-1)$

$(2,-1)$ only

$(0,-1)$ and $(2,1)$

$(0,-1)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{(x-2)}^{2}+{(y+1)}^{2} & =2(y+1)-2(x-2) \\ {(x-2)}^{2}+{(y+1)}^{2}+2(x-2)-2(y+1) & =0\end{aligned}
$$

If we set $f(x,y)={(x-2)}^{2}+{(y+1)}^{2}+2(x-2)-2(y+1),$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(x-2)}^{2}+{(y+1)}^{2}+2(x-2)-2(y+1))\,i-\frac{∂}{∂x}({(x-2)}^{2}+{(y+1)}^{2}+2(x-2)-2(y+1))\,j \\  & =(2(y+1)-2)\,i-(2(x-2)+2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $-i+j,$ we must have $t\cdot (-i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (-i+j) & =0 \\ ((2(y+1)-2)\,i-(2(x-2)+2)\,j)\cdot (-i+j) & =0 \\ -(2(y+1)-2)-(2(x-2)+2) & =0 \\ -2(y+1)-2(x-2) & =0 \\ (y+1) & =-(x-2)\end{aligned}
$$

Substituting $(y+1)=-(x-2)$ into the equation of our curve gives

$$
\begin{aligned}{(x-2)}^{2}+{(y+1)}^{2} & =2(y+1)-2(x-2) \\ {(x-2)}^{2}+(-(x-2))^{2} & =2(-(x-2))-2(x-2) \\ 2{(x-2)}^{2} & =-4(x-2) \\ 2{(x-2)}^{2}+4(x-2) & =0 \\ 2(x-2)((x-2)+2) & =0 \\ (x-2) & =-2,0.\end{aligned}
$$

Finally:

- For $(x-2)=-2,$ we get $(y+1)=2,$ and the corresponding point is $(0,1).$

- For $(x-2)=0,$ we get $(y+1)=0,$ and the corresponding point is $(2,-1).$

## q-130217 translated observed_completed

### q-130217 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(x+3)}^{2}+{(y-3)}^{2}=2(y-3)-2(x+3)$ is the tangent vector to the curve perpendicular to the vector $-i+j?$

$(-3,5)$ only

**CORRECT** $(-5,5)$ and $(-3,3)$

$(-3,3)$ only

$(-5,3)$ and $(-3,5)$

$(-5,3)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{(x+3)}^{2}+{(y-3)}^{2} & =2(y-3)-2(x+3) \\ {(x+3)}^{2}+{(y-3)}^{2}+2(x+3)-2(y-3) & =0\end{aligned}
$$

If we set $f(x,y)={(x+3)}^{2}+{(y-3)}^{2}+2(x+3)-2(y-3),$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(x+3)}^{2}+{(y-3)}^{2}+2(x+3)-2(y-3))\,i-\frac{∂}{∂x}({(x+3)}^{2}+{(y-3)}^{2}+2(x+3)-2(y-3))\,j \\  & =(2(y-3)-2)\,i-(2(x+3)+2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $-i+j,$ we must have $t\cdot (-i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (-i+j) & =0 \\ ((2(y-3)-2)\,i-(2(x+3)+2)\,j)\cdot (-i+j) & =0 \\ -(2(y-3)-2)-(2(x+3)+2) & =0 \\ -2(y-3)-2(x+3) & =0 \\ (y-3) & =-(x+3)\end{aligned}
$$

Substituting $(y-3)=-(x+3)$ into the equation of our curve gives

$$
\begin{aligned}{(x+3)}^{2}+{(y-3)}^{2} & =2(y-3)-2(x+3) \\ {(x+3)}^{2}+(-(x+3))^{2} & =2(-(x+3))-2(x+3) \\ 2{(x+3)}^{2} & =-4(x+3) \\ 2{(x+3)}^{2}+4(x+3) & =0 \\ 2(x+3)((x+3)+2) & =0 \\ (x+3) & =-2,0.\end{aligned}
$$

Finally:

- For $(x+3)=-2,$ we get $(y-3)=2,$ and the corresponding point is $(-5,5).$

- For $(x+3)=0,$ we get $(y-3)=0,$ and the corresponding point is $(-3,3).$

## q-130217 completed evidence only

### q-130217 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${x}^{2}+{y}^{2}=2y-2x$ is the tangent vector to the curve perpendicular to the vector $-i+j?$

$(0,2)$ only

**CORRECT** $(-2,2)$ and $(0,0)$

$(0,0)$ only

$(-2,0)$ and $(0,2)$

$(-2,0)$ only

First, we bring all variables to one side:

$$
\begin{aligned}{x}^{2}+{y}^{2} & =2y-2x \\ {x}^{2}+{y}^{2}+2x-2y & =0\end{aligned}
$$

If we set $f(x,y)={x}^{2}+{y}^{2}+2x-2y,$ our curve can be viewed as the level curve $f(x,y)=0.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({x}^{2}+{y}^{2}+2x-2y)\,i-\frac{∂}{∂x}({x}^{2}+{y}^{2}+2x-2y)\,j \\  & =(2y-2)\,i-(2x+2)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $-i+j,$ we must have $t\cdot (-i+j)=0.$

$$
\begin{aligned}t(x,y)\cdot (-i+j) & =0 \\ ((2y-2)\,i-(2x+2)\,j)\cdot (-i+j) & =0 \\ -(2y-2)-(2x+2) & =0 \\ -2y-2x & =0 \\ y & =-x\end{aligned}
$$

Substituting $y=-x$ into the equation of our curve gives

$$
\begin{aligned}{x}^{2}+{y}^{2} & =2y-2x \\ {x}^{2}+(-x)^{2} & =2(-x)-2x \\ 2{x}^{2} & =-4x \\ 2{x}^{2}+4x & =0 \\ 2x(x+2) & =0 \\ x & =-2,0.\end{aligned}
$$

Finally:

- For $x=-2,$ we get $y=2,$ and the corresponding point is $(-2,2).$

- For $x=0,$ we get $y=0,$ and the corresponding point is $(0,0).$

## q-72412 original raw / hard

### q-72412 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${y}^{2}-4xy=-5{x}^{2}+1$ is the tangent vector to the curve perpendicular to the vector $i?$

**CORRECT** $(1,2)$ and $(-1,-2)$

$(1,1)$ and $(-1,-1)$

$(3,2)$ and $(-1,3)$

$(1,3)$ and $(3,-2)$

$(-1,2)$ and $(1,-2)$

First, we bring all variables to one side:

$$
\begin{aligned}{y}^{2}-4xy & =-5{x}^{2}+1 \\ {y}^{2}-4xy+5{x}^{2} & =1\end{aligned}
$$

If we set $f(x,y)={y}^{2}-4xy+5{x}^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({y}^{2}-4xy+5{x}^{2})i-\frac{∂}{∂x}({y}^{2}-4xy+5{x}^{2})j \\  & =2(y-2x)\,i-(10x-4y)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ (2(y-2x)\,i-(10x-4y)\,j)\cdot i & =0 \\ 2(y-2x) & =0 \\ y & =2x\end{aligned}
$$

Substituting $y=2x$ into the equation of our curve gives:  

$$
\begin{aligned}{y}^{2}-4xy+5{x}^{2} & =1 \\ (2x)^{2}-4x(2x)+5{x}^{2} & =1 \\ 4{x}^{2}-8{x}^{2}+5{x}^{2} & =1 \\ {x}^{2} & =1 \\ x & =\pm 1\end{aligned}
$$

Finally:

- If $x=1$, we get $y=2$ and the corresponding point is $(1,2).$

- If $x=-1$, we get $y=-2$ and the corresponding point is $(-1,-2).$

## q-72412 translated observed_raw

### q-72412 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(y+1)}^{2}-4(x-2)(y+1)=-5{(x-2)}^{2}+1$ is the tangent vector to the curve perpendicular to the vector $i?$

**CORRECT** $(3,1)$ and $(1,-3)$

$(3,0)$ and $(1,-2)$

$(5,1)$ and $(1,2)$

$(3,2)$ and $(5,-3)$

$(1,1)$ and $(3,-3)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y+1)}^{2}-4(x-2)(y+1) & =-5{(x-2)}^{2}+1 \\ {(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2} & =1\end{aligned}
$$

If we set $f(x,y)={(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2})i-\frac{∂}{∂x}({(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2})j \\  & =2((y+1)-2(x-2))\,i-(10(x-2)-4(y+1))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ (2((y+1)-2(x-2))\,i-(10(x-2)-4(y+1))\,j)\cdot i & =0 \\ 2((y+1)-2(x-2)) & =0 \\ (y+1) & =2(x-2)\end{aligned}
$$

Substituting $(y+1)=2(x-2)$ into the equation of our curve gives:  

$$
\begin{aligned}{(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2} & =1 \\ (2(x-2))^{2}-4(x-2)(2(x-2))+5{(x-2)}^{2} & =1 \\ 4{(x-2)}^{2}-8{(x-2)}^{2}+5{(x-2)}^{2} & =1 \\ {(x-2)}^{2} & =1 \\ (x-2) & =\pm 1\end{aligned}
$$

Finally:

- If $(x-2)=1$, we get $(y+1)=2$ and the corresponding point is $(3,1).$

- If $(x-2)=-1$, we get $(y+1)=-2$ and the corresponding point is $(1,-3).$

## q-72412 translated observed_raw

### q-72412 / observed_raw — observed_raw

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(y-3)}^{2}-4(x+3)(y-3)=-5{(x+3)}^{2}+1$ is the tangent vector to the curve perpendicular to the vector $i?$

**CORRECT** $(-2,5)$ and $(-4,1)$

$(-2,4)$ and $(-4,2)$

$(0,5)$ and $(-4,6)$

$(-2,6)$ and $(0,1)$

$(-4,5)$ and $(-2,1)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y-3)}^{2}-4(x+3)(y-3) & =-5{(x+3)}^{2}+1 \\ {(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2} & =1\end{aligned}
$$

If we set $f(x,y)={(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2})i-\frac{∂}{∂x}({(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2})j \\  & =2((y-3)-2(x+3))\,i-(10(x+3)-4(y-3))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ (2((y-3)-2(x+3))\,i-(10(x+3)-4(y-3))\,j)\cdot i & =0 \\ 2((y-3)-2(x+3)) & =0 \\ (y-3) & =2(x+3)\end{aligned}
$$

Substituting $(y-3)=2(x+3)$ into the equation of our curve gives:  

$$
\begin{aligned}{(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2} & =1 \\ (2(x+3))^{2}-4(x+3)(2(x+3))+5{(x+3)}^{2} & =1 \\ 4{(x+3)}^{2}-8{(x+3)}^{2}+5{(x+3)}^{2} & =1 \\ {(x+3)}^{2} & =1 \\ (x+3) & =\pm 1\end{aligned}
$$

Finally:

- If $(x+3)=1$, we get $(y-3)=2$ and the corresponding point is $(-2,5).$

- If $(x+3)=-1$, we get $(y-3)=-2$ and the corresponding point is $(-4,1).$

## q-72412 translated observed_completed

### q-72412 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 2, 'k': -1}

At which points on the curve ${(y+1)}^{2}-4(x-2)(y+1)=-5{(x-2)}^{2}+1$ is the tangent vector to the curve perpendicular to the vector $i?$

**CORRECT** $(3,1)$ and $(1,-3)$

$(3,0)$ and $(1,-2)$

$(5,1)$ and $(1,2)$

$(3,2)$ and $(5,-3)$

$(1,1)$ and $(3,-3)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y+1)}^{2}-4(x-2)(y+1) & =-5{(x-2)}^{2}+1 \\ {(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2} & =1\end{aligned}
$$

If we set $f(x,y)={(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y+1)}((x-2),(y+1))\,i-{f}_{(x-2)}((x-2),(y+1))\,j \\  & =\frac{∂}{∂y}({(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2})i-\frac{∂}{∂x}({(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2})j \\  & =2((y+1)-2(x-2))\,i-(10(x-2)-4(y+1))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ (2((y+1)-2(x-2))\,i-(10(x-2)-4(y+1))\,j)\cdot i & =0 \\ 2((y+1)-2(x-2)) & =0 \\ (y+1) & =2(x-2)\end{aligned}
$$

Substituting $(y+1)=2(x-2)$ into the equation of our curve gives:  

$$
\begin{aligned}{(y+1)}^{2}-4(x-2)(y+1)+5{(x-2)}^{2} & =1 \\ (2(x-2))^{2}-4(x-2)(2(x-2))+5{(x-2)}^{2} & =1 \\ 4{(x-2)}^{2}-8{(x-2)}^{2}+5{(x-2)}^{2} & =1 \\ {(x-2)}^{2} & =1 \\ (x-2) & =\pm 1\end{aligned}
$$

Finally:

- If $(x-2)=1$, we get $(y+1)=2$ and the corresponding point is $(3,1).$

- If $(x-2)=-1$, we get $(y+1)=-2$ and the corresponding point is $(1,-3).$

## q-72412 translated observed_completed

### q-72412 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': -3, 'k': 3}

At which points on the curve ${(y-3)}^{2}-4(x+3)(y-3)=-5{(x+3)}^{2}+1$ is the tangent vector to the curve perpendicular to the vector $i?$

**CORRECT** $(-2,5)$ and $(-4,1)$

$(-2,4)$ and $(-4,2)$

$(0,5)$ and $(-4,6)$

$(-2,6)$ and $(0,1)$

$(-4,5)$ and $(-2,1)$

First, we bring all variables to one side:

$$
\begin{aligned}{(y-3)}^{2}-4(x+3)(y-3) & =-5{(x+3)}^{2}+1 \\ {(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2} & =1\end{aligned}
$$

If we set $f(x,y)={(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{(y-3)}((x+3),(y-3))\,i-{f}_{(x+3)}((x+3),(y-3))\,j \\  & =\frac{∂}{∂y}({(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2})i-\frac{∂}{∂x}({(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2})j \\  & =2((y-3)-2(x+3))\,i-(10(x+3)-4(y-3))\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ (2((y-3)-2(x+3))\,i-(10(x+3)-4(y-3))\,j)\cdot i & =0 \\ 2((y-3)-2(x+3)) & =0 \\ (y-3) & =2(x+3)\end{aligned}
$$

Substituting $(y-3)=2(x+3)$ into the equation of our curve gives:  

$$
\begin{aligned}{(y-3)}^{2}-4(x+3)(y-3)+5{(x+3)}^{2} & =1 \\ (2(x+3))^{2}-4(x+3)(2(x+3))+5{(x+3)}^{2} & =1 \\ 4{(x+3)}^{2}-8{(x+3)}^{2}+5{(x+3)}^{2} & =1 \\ {(x+3)}^{2} & =1 \\ (x+3) & =\pm 1\end{aligned}
$$

Finally:

- If $(x+3)=1$, we get $(y-3)=2$ and the corresponding point is $(-2,5).$

- If $(x+3)=-1$, we get $(y-3)=-2$ and the corresponding point is $(-4,1).$

## q-72412 completed evidence only

### q-72412 / observed_completed — observed_bank_with_inferred_completion

Evidence only: True; parameters: {'h': 0, 'k': 0}

At which points on the curve ${y}^{2}-4xy=-5{x}^{2}+1$ is the tangent vector to the curve perpendicular to the vector $i?$

**CORRECT** $(1,2)$ and $(-1,-2)$

$(1,1)$ and $(-1,-1)$

$(3,2)$ and $(-1,3)$

$(1,3)$ and $(3,-2)$

$(-1,2)$ and $(1,-2)$

First, we bring all variables to one side:

$$
\begin{aligned}{y}^{2}-4xy & =-5{x}^{2}+1 \\ {y}^{2}-4xy+5{x}^{2} & =1\end{aligned}
$$

If we set $f(x,y)={y}^{2}-4xy+5{x}^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$ 

A tangent vector to the level curve can be computed as follows:

$$
t(x,y)={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j
$$

So, we calculate $t(x,y):$

$$
\begin{aligned}t(x,y) & ={f}_{y}(x,y)\,i-{f}_{x}(x,y)\,j \\  & =\frac{∂}{∂y}({y}^{2}-4xy+5{x}^{2})i-\frac{∂}{∂x}({y}^{2}-4xy+5{x}^{2})j \\  & =2(y-2x)\,i-(10x-4y)\,j\end{aligned}
$$

Since our tangent vector needs to be perpendicular to $i$, we must have $t\cdot i=0.$

$$
\begin{aligned}t(x,y)\cdot i & =0 \\ (2(y-2x)\,i-(10x-4y)\,j)\cdot i & =0 \\ 2(y-2x) & =0 \\ y & =2x\end{aligned}
$$

Substituting $y=2x$ into the equation of our curve gives:  

$$
\begin{aligned}{y}^{2}-4xy+5{x}^{2} & =1 \\ (2x)^{2}-4x(2x)+5{x}^{2} & =1 \\ 4{x}^{2}-8{x}^{2}+5{x}^{2} & =1 \\ {x}^{2} & =1 \\ x & =\pm 1\end{aligned}
$$

Finally:

- If $x=1$, we get $y=2$ and the corresponding point is $(1,2).$

- If $x=-1$, we get $y=-2$ and the corresponding point is $(-1,-2).$

## easy authored generated

### canonical_linear / authored_method_bank — authored_missing_level

Evidence only: False; parameters: {'A': 3, 'b': 2, 'r': -6}

At which point on the curve $6 x y + 3 y^{2}=- 3 x^{2} + 2 y - 12$ is the tangent vector to the curve perpendicular to the vector $j$?

$(-6,0)$ only

$(-6,-6)$ only

$(-12,12)$ only

**CORRECT** $(-6,6)$ only

$(6,-6)$ only

First, we bring all variables to one side:

$$\begin{aligned}6 x y + 3 y^{2}&=- 3 x^{2} + 2 y - 12\\3 x^{2} + 6 x y + 3 y^{2} - 2 y + 12&=0\end{aligned}$$

If we set $f(x,y)=3 x^{2} + 6 x y + 3 y^{2} - 2 y + 12$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(3 x^{2} + 6 x y + 3 y^{2} - 2 y + 12)\,i-\frac{∂}{∂x}(3 x^{2} + 6 x y + 3 y^{2} - 2 y + 12)\,j\\&=(6 x + 6 y - 2)\,i-(6 x + 6 y)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\- 6 x - 6 y&=0\\y&=-x\end{aligned}$$

Substituting $y=-x$ into the equation of our curve gives:

$$\begin{aligned}3(x+(-x))^{2}-2(-x)-(-12)&=0\\2x-(-12)&=0\\2x&=-12\\x&=-6\end{aligned}$$

Finally, the corresponding point is $(-6,6)$.

## easy authored generated

### canonical_linear / authored_method_bank — authored_missing_level

Evidence only: False; parameters: {'A': 4, 'b': 2, 'r': -4}

At which point on the curve $8 x y + 4 y^{2}=- 4 x^{2} + 2 y - 8$ is the tangent vector to the curve perpendicular to the vector $j$?

$(4,-4)$ only

$(-4,-4)$ only

$(-4,0)$ only

**CORRECT** $(-4,4)$ only

$(-8,8)$ only

First, we bring all variables to one side:

$$\begin{aligned}8 x y + 4 y^{2}&=- 4 x^{2} + 2 y - 8\\4 x^{2} + 8 x y + 4 y^{2} - 2 y + 8&=0\end{aligned}$$

If we set $f(x,y)=4 x^{2} + 8 x y + 4 y^{2} - 2 y + 8$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(4 x^{2} + 8 x y + 4 y^{2} - 2 y + 8)\,i-\frac{∂}{∂x}(4 x^{2} + 8 x y + 4 y^{2} - 2 y + 8)\,j\\&=(8 x + 8 y - 2)\,i-(8 x + 8 y)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\- 8 x - 8 y&=0\\y&=-x\end{aligned}$$

Substituting $y=-x$ into the equation of our curve gives:

$$\begin{aligned}4(x+(-x))^{2}-2(-x)-(-8)&=0\\2x-(-8)&=0\\2x&=-8\\x&=-4\end{aligned}$$

Finally, the corresponding point is $(-4,4)$.

## moderate authored generated

### symmetric_quadratic / authored_method_bank — authored_missing_level

Evidence only: False; parameters: {'D': 2, 'm': 2, 'r': 1}

At which points on the curve $4 x y + 2 y^{2}=4 x^{2} + 12$ is the tangent vector to the curve perpendicular to the vector $j$?

$(2,1)$ and $(-2,-1)$

$(1,2)$ only

$(1,-2)$ and $(-1,2)$

**CORRECT** $(1,2)$ and $(-1,-2)$

$(-1,-2)$ only

First, we bring all variables to one side:

$$\begin{aligned}4 x y + 2 y^{2}&=4 x^{2} + 12\\- 4 x^{2} + 4 x y + 2 y^{2} - 12&=0\end{aligned}$$

If we set $f(x,y)=- 4 x^{2} + 4 x y + 2 y^{2} - 12$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(- 4 x^{2} + 4 x y + 2 y^{2} - 12)\,i-\frac{∂}{∂x}(- 4 x^{2} + 4 x y + 2 y^{2} - 12)\,j\\&=(4 x + 4 y)\,i-(- 8 x + 4 y)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\8 x - 4 y&=0\\y&=2x\end{aligned}$$

Substituting $y=2x$ into the equation of our curve gives:

$$\begin{aligned}2(2x)^{2}+4x(2x)-4x^{2}-12&=0\\12x^{2}-12&=0\\x^{2}&=1\\x&=\pm 1\end{aligned}$$

Finally, the corresponding points are $(1,2)$ and $(-1,-2)$.

## moderate authored generated

### symmetric_quadratic / authored_method_bank — authored_missing_level

Evidence only: False; parameters: {'D': 2, 'm': 4, 'r': 1}

At which points on the curve $8 x y + 2 y^{2}=16 x^{2} + 48$ is the tangent vector to the curve perpendicular to the vector $j$?

$(-1,-4)$ only

$(1,4)$ only

$(4,1)$ and $(-4,-1)$

**CORRECT** $(1,4)$ and $(-1,-4)$

$(1,-4)$ and $(-1,4)$

First, we bring all variables to one side:

$$\begin{aligned}8 x y + 2 y^{2}&=16 x^{2} + 48\\- 16 x^{2} + 8 x y + 2 y^{2} - 48&=0\end{aligned}$$

If we set $f(x,y)=- 16 x^{2} + 8 x y + 2 y^{2} - 48$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(- 16 x^{2} + 8 x y + 2 y^{2} - 48)\,i-\frac{∂}{∂x}(- 16 x^{2} + 8 x y + 2 y^{2} - 48)\,j\\&=(8 x + 4 y)\,i-(- 32 x + 8 y)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\32 x - 8 y&=0\\y&=4x\end{aligned}$$

Substituting $y=4x$ into the equation of our curve gives:

$$\begin{aligned}2(4x)^{2}+8x(4x)-16x^{2}-48&=0\\48x^{2}-48&=0\\x^{2}&=1\\x&=\pm 1\end{aligned}$$

Finally, the corresponding points are $(1,4)$ and $(-1,-4)$.

## hard authored generated

### factor_quadratic / authored_method_bank — authored_bank_same_observed_hard_method

Evidence only: False; parameters: {'a': -5, 'b': -2}

At which points on the curve $x^{2} + 2 x y=7 y + 10$ is the tangent vector to the curve perpendicular to the vector $j$?

$(-5,5)$ and $(-2,2)$

$(5,-5)$ only

$(-5,-5)$ and $(-2,-2)$

**CORRECT** $(5,-5)$ and $(2,-2)$

$(2,-2)$ only

First, we bring all variables to one side:

$$\begin{aligned}x^{2} + 2 x y&=7 y + 10\\x^{2} + 2 x y - 7 y - 10&=0\end{aligned}$$

If we set $f(x,y)=x^{2} + 2 x y - 7 y - 10$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(x^{2} + 2 x y - 7 y - 10)\,i-\frac{∂}{∂x}(x^{2} + 2 x y - 7 y - 10)\,j\\&=(2 x - 7)\,i-(2 x + 2 y)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\- 2 x - 2 y&=0\\x&=-y\end{aligned}$$

Substituting $x=-y$ into the equation of our curve gives:

$$\begin{aligned}(-y)^{2}+2(-y)y+(-7)y-(10)&=0\\-y^{2}+(-7)y-(10)&=0\\y^{2}-(-7)y+(10)&=0\\(y-(-5))(y-(-2))&=0\\y&=-5\text{ or }-2\end{aligned}$$

Finally, the corresponding points are $(5,-5)$ and $(2,-2)$.

## hard authored generated

### factor_quadratic / authored_method_bank — authored_bank_same_observed_hard_method

Evidence only: False; parameters: {'a': 1, 'b': 3}

At which points on the curve $x^{2} + 2 x y=3 - 4 y$ is the tangent vector to the curve perpendicular to the vector $j$?

$(-3,3)$ only

$(-1,1)$ only

$(1,-1)$ and $(3,-3)$

**CORRECT** $(-1,1)$ and $(-3,3)$

$(1,1)$ and $(3,3)$

First, we bring all variables to one side:

$$\begin{aligned}x^{2} + 2 x y&=3 - 4 y\\x^{2} + 2 x y + 4 y - 3&=0\end{aligned}$$

If we set $f(x,y)=x^{2} + 2 x y + 4 y - 3$, our curve can be viewed as the level curve $f(x,y)=0.$

A tangent vector to the level curve can be computed as follows:

$$t(x,y)=f_y(x,y)\,i-f_x(x,y)\,j$$

So, we calculate $t(x,y):$

$$\begin{aligned}t(x,y)&=\frac{∂}{∂y}(x^{2} + 2 x y + 4 y - 3)\,i-\frac{∂}{∂x}(x^{2} + 2 x y + 4 y - 3)\,j\\&=(2 x + 4)\,i-(2 x + 2 y)\,j\end{aligned}$$

Since our tangent vector needs to be perpendicular to $j$, we must have $t\cdot j=0.$

$$\begin{aligned}t(x,y)\cdot j&=0\\- 2 x - 2 y&=0\\x&=-y\end{aligned}$$

Substituting $x=-y$ into the equation of our curve gives:

$$\begin{aligned}(-y)^{2}+2(-y)y+(4)y-(3)&=0\\-y^{2}+(4)y-(3)&=0\\y^{2}-(4)y+(3)&=0\\(y-(1))(y-(3))&=0\\y&=1\text{ or }3\end{aligned}$$

Finally, the corresponding points are $(-1,1)$ and $(-3,3)$.
