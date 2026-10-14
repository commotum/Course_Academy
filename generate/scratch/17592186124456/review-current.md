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

### symmetric_quadratic / current_coordinate_bank — authored_missing_level

Evidence only: False; parameters: {'D': 2, 'm': 2, 'r': 1}

At which points on the curve $4 x y + 2 y^{2}=4 x^{2} + 12$ is the tangent vector to the curve perpendicular to the vector $j$?

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $(-1,-2)$
- **II.** $(0,2)$
- **III.** $(\frac{1}{2},2)$
- **IV.** $(1,0)$
- **V.** $(1,1)$
- **VI.** $(1,2)$

false

**CORRECT** true

**CORRECT** false

true

**CORRECT** false

true

**CORRECT** false

true

**CORRECT** false

true

false

**CORRECT** true

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

### symmetric_quadratic / current_coordinate_bank — authored_missing_level

Evidence only: False; parameters: {'D': 2, 'm': 4, 'r': 1}

At which points on the curve $8 x y + 2 y^{2}=16 x^{2} + 48$ is the tangent vector to the curve perpendicular to the vector $j$?

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $(-1,-4)$
- **II.** $(0,4)$
- **III.** $(\frac{1}{2},4)$
- **IV.** $(1,0)$
- **V.** $(1,2)$
- **VI.** $(1,4)$

false

**CORRECT** true

**CORRECT** false

true

**CORRECT** false

true

**CORRECT** false

true

**CORRECT** false

true

false

**CORRECT** true

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

### factor_quadratic / current_coordinate_bank — authored_bank_same_observed_hard_method

Evidence only: False; parameters: {'a': -5, 'b': -2}

At which points on the curve $x^{2} + 2 x y=7 y + 10$ is the tangent vector to the curve perpendicular to the vector $j$?

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $(2,-5)$
- **II.** $(2,-2)$
- **III.** $(1,-2)$
- **IV.** $(5,-5)$
- **V.** $(5,-2)$
- **VI.** $(-5,-5)$
- **VII.** $(-2,2)$

**CORRECT** false

true

false

**CORRECT** true

**CORRECT** false

true

false

**CORRECT** true

**CORRECT** false

true

**CORRECT** false

true

**CORRECT** false

true

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

### factor_quadratic / current_coordinate_bank — authored_bank_same_observed_hard_method

Evidence only: False; parameters: {'a': 1, 'b': 3}

At which points on the curve $x^{2} + 2 x y=3 - 4 y$ is the tangent vector to the curve perpendicular to the vector $j$?

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $(-3,1)$
- **II.** $(-3,3)$
- **III.** $(- \frac{3}{2},3)$
- **IV.** $(-1,1)$
- **V.** $(-1,3)$
- **VI.** $(1,1)$
- **VII.** $(3,-3)$

**CORRECT** false

true

false

**CORRECT** true

**CORRECT** false

true

false

**CORRECT** true

**CORRECT** false

true

**CORRECT** false

true

**CORRECT** false

true

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