# Source originals and generated variants

Raw captures remain in source.json; original replay choices are presentation-normalized. Two observed banks are ambiguous evidence; normal authored banks are collision-free.

## Raw original q-334916

Consider the following initial value problem.
$\frac{dy}{dx} + y = 1, y(0) =-3$

Select the correct options below.

An integrating factor for this equation is $I(x) =$ {{field-1}}.

The solution to the initial value problem is $y(x) =$ {{field-2}}.

field-1:
- `x`
- `e^{x}`
- `x^{3}`
- `\frac{1}{x}`

field-2:
- `1 - 4e^{x}`
- `1 - \frac{4}{e^{x}}`
- `-3e^{x}`
- `\frac{1}{e^{x}} - 4`
- `-\frac{3}{e^{x}}`

No captured worked solution; replay uses a separately authored derivation.

## Raw original q-335808

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{x}{2}\cdot y=x,\,y(0)=1
$$

Select the correct options below.

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-2:
- `2x+1`
- `{e}^{2{x}^{2}}`
- `2-{e}^{{x}^{2}}`
- `2-{e}^{-{x}^{2}/4}`
- `2{x}^{2}+1`

field-1:
- `\frac{1}{x}`
- `{e}^{{x}^{2}/4}`
- `{e}^{4x}`
- `{x}^{3}`

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{2}$ and $Q(x)=x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (x/2)\,\text{d}x} \\  & ={e}^{{x}^{2}/4}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{{x}^{2}/4}$ yields

$$
\begin{aligned}{e}^{{x}^{2}/4}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{2}y) & ={e}^{{x}^{2}/4}\cdot x \\ {e}^{{x}^{2}/4}\cdot \frac{\text{d}y}{\text{d}x}+\frac{x}{2}{e}^{{x}^{2}/4}\cdot y & =x{e}^{{x}^{2}/4} \\ \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/4}) & =x{e}^{{x}^{2}/4}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{{x}^{2}}{4}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/4})\text{d}x & =\int x{e}^{{x}^{2}/4}\,\text{d}x \\ y{e}^{{x}^{2}/4} & =\int 2{e}^{u}\,\text{d}u \\ y{e}^{{x}^{2}/4} & =2{e}^{u}+C \\ y{e}^{{x}^{2}/4} & =2{e}^{{x}^{2}/4}+C \\ y & =2+C{e}^{-{x}^{2}/4}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=1$ as follows:

$$
\begin{aligned}y(0) & =2+C{e}^{-{0}^{2}/4} \\ 1 & =2+C \\ C & =-1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2-{e}^{-{x}^{2}/4}.
$$

## Raw original q-335810

Consider the following initial value problem.

$$
x\frac{\text{d}y}{\text{d}x}+2y=4{x}^{2},\,y(1)=2
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- `2x`
- `{e}^{2x}`
- `{e}^{x}`
- `{x}^{2}`

field-2:
- `3{x}^{2}-\frac{1}{{x}^{2}}`
- `{x}^{2}+\frac{1}{{x}^{2}}`
- `x+\frac{1}{{x}^{2}}`
- `3x-\frac{1}{{x}^{2}}`

The first step is to write the equation in standard form,

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)\,.
$$

In doing so, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2y & =4{x}^{2} \\ \frac{1}{x}(x\frac{\text{d}y}{\text{d}x}+2y) & =\frac{1}{x}\cdot 4{x}^{2} \\ \frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y & =4x.\end{aligned}
$$

Consequently,

$$
\begin{aligned}P(x)=\frac{2}{x},\,Q(x)=4x.\end{aligned}
$$

We then compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\int (1/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡{x}^{2}} \\  & ={x}^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={x}^{2}$ yields

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & ={x}^{2}\cdot 4x \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =4{x}^{3} \\ \frac{\text{d}}{\text{d}x}(y{x}^{2}) & =4{x}^{3}.\end{aligned}
$$

$$

$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int 4{x}^{3}\,\text{d}x \\ y{x}^{2} & ={x}^{4}+C \\ y & ={x}^{2}+\frac{C}{{x}^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(1)=2$ as follows:

$$
\begin{aligned}y(1) & ={1}^{2}+\frac{C}{{1}^{2}} \\ 2 & =1+C \\ C & =1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y={x}^{2}+\frac{1}{{x}^{2}}.
$$

## Raw original q-335811

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{2y}{x}=\frac{\operatorname{cos}⁡x}{{x}^{2}},\,y(\pi )=0
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- `{e}^{{x}^{2}}`
- `{e}^{2x}`
- `{x}^{2}`
- `2x`

field-2:
- `{x}^{2}\operatorname{sin}⁡x`
- `\frac{\operatorname{sin}⁡x}{x}`
- `\frac{\operatorname{sin}x}{{x}^{2}}`
- `\frac{\operatorname{sin}⁡x}{{x}^{2}}`
- `x\operatorname{sin}⁡x`

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{\operatorname{cos}⁡x}{{x}^{2}}.$ 

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\int (1/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡{x}^{2}} \\  & ={x}^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={x}^{2}$ yields

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y) & ={x}^{2}\cdot \frac{\operatorname{cos}⁡x}{{x}^{2}} \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =\operatorname{cos}⁡x \\ \frac{\text{d}}{\text{d}x}(y{x}^{2}) & =\operatorname{cos}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int \operatorname{cos}⁡x\,\text{d}x \\ y{x}^{2} & =\operatorname{sin}⁡x+C \\ y & =\frac{\operatorname{sin}⁡x+C}{{x}^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\pi )=0$ as follows:

$$
\begin{aligned}y(\pi ) & =\frac{\operatorname{sin}⁡(\pi )+C}{{\pi }^{2}} \\ 0 & =\frac{C}{{\pi }^{2}} \\ C & =0\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{\operatorname{sin}⁡x}{{x}^{2}}.
$$

## Raw original q-335812

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y=\frac{\operatorname{sin}⁡x}{x},\,x>0,\,y(\frac{\pi }{2})=1
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-2:
- `\frac{\pi +3\operatorname{cos}⁡x}{2x}`
- `\frac{\pi +4\operatorname{cos}⁡x}{2x}`
- `\frac{\pi -\operatorname{cos}⁡x}{2x}`
- `\frac{\pi -2\operatorname{cos}x}{2x}`
- `\frac{\pi -2\operatorname{cos}⁡x}{2x}`

field-1:
- `\frac{1}{x}`
- `{e}^{x}`
- `x`
- `\operatorname{ln}⁡x`

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡x}{x}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (1/x)\,\text{d}x} \\  & ={e}^{\operatorname{ln}⁡x} \\  & =x\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x$ yields

$$
\begin{aligned}x\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y) & =x\cdot \frac{\operatorname{sin}⁡x}{x} \\ x\frac{\text{d}y}{\text{d}x}+y & =\operatorname{sin}⁡x \\ \frac{\text{d}}{\text{d}x}(yx) & =\operatorname{sin}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx)\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ yx & =-\operatorname{cos}⁡x+C \\ y & =\frac{-\operatorname{cos}⁡x+C}{x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\frac{\pi }{2})=1$ as follows:

$$
\begin{aligned}y(\frac{\pi }{2}) & =\frac{-\operatorname{cos}⁡(\frac{\pi }{2})+C}{(\frac{\pi }{2})} \\ 1 & =\frac{2C}{\pi } \\ C & =\frac{\pi }{2}\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
\begin{aligned}y & =\frac{(-\operatorname{cos}⁡x+\frac{\pi }{2})}{x} \\  & =\frac{\pi }{2x}-\frac{\operatorname{cos}⁡x}{x} \\  & =\frac{\pi -2\operatorname{cos}⁡x}{2x}.\end{aligned}
$$

## Raw original q-335806

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+y=2x{e}^{-x},\,y(0)=-2
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-2:
- `(x-2){e}^{x}`
- `({x}^{2}-2){e}^{x}`
- `-2{e}^{-x}`
- `(x-2){e}^{-x}`
- `({x}^{2}-2){e}^{-x}`

field-1:
- `{e}^{x}`
- `x`
- `{e}^{-x}`
- `{x}^{2}`

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=2x{e}^{-x}.$ 

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 1\,\text{d}x} \\  & ={e}^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{x}$ yields

$$
\begin{aligned}{e}^{x}\cdot (\frac{\text{d}y}{\text{d}x}+y) & ={e}^{x}\cdot 2x{e}^{-x} \\ {e}^{x}\frac{\text{d}y}{\text{d}x}+{e}^{x}y & =2x \\ \frac{\text{d}}{\text{d}x}(y{e}^{x}) & =2x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{x})\text{d}x & =\int 2x\,\text{d}x \\ y{e}^{x} & ={x}^{2}+C \\ y & =({x}^{2}+C){e}^{-x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =({0}^{2}+C){e}^{-0} \\ -2 & =(0+C)\cdot 1 \\ C & =-2\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=({x}^{2}-2){e}^{-x}.
$$

## Raw original q-335829

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+4y=8,\,y(0)=-1
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-2:
- `2-3{e}^{-4x}`
- `1-2{e}^{-4x}`
- `4-5{e}^{4x}`
- `-{e}^{4x}`
- `-{e}^{-4x}`

field-1:
- `{e}^{2x}`
- `4x`
- `{e}^{4x}`
- `{e}^{8x}`

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=4$ and $Q(x)=8.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 4\,\text{d}x} \\  & ={e}^{4x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{4x}$ yields

$$
\begin{aligned}{e}^{4x}\cdot (\frac{\text{d}y}{\text{d}x}+4y) & ={e}^{4x}\cdot 8 \\ {e}^{4x}\cdot \frac{\text{d}y}{\text{d}x}+4{e}^{4x}\cdot y & =8{e}^{4x} \\ \frac{\text{d}}{\text{d}x}(y{e}^{4x}) & =8{e}^{4x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{4x})\text{d}x & =\int 8{e}^{4x}\,\text{d}x \\ y{e}^{4x} & =8(\frac{1}{4}{e}^{4x})+C \\ y{e}^{4x} & =2{e}^{4x}+C \\ y & =2+C{e}^{-4x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-1$ as follows:

$$
\begin{aligned}y(0) & =2+C{e}^{-4(0)} \\ -1 & =2+C(1) \\ C & =-3\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2-3{e}^{-4x}.
$$

## Raw original q-339145

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y=x,\,y(0)=5
$$

Select the correct options below.
$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-2:
- `6-{e}^{{x}^{2}}`
- `6x+5`
- `{e}^{6{x}^{2}}`
- `6{x}^{2}+5`
- `6-{e}^{-{x}^{2}/12}`

field-1:
- `{e}^{12x}`
- `\frac{1}{x}`
- `{x}^{6}`
- `{e}^{{x}^{2}/12}`

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{6}$ and $Q(x)=x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (x/6)\,\text{d}x} \\  & ={e}^{{x}^{2}/12}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{{x}^{2}/12}$ yields

$$
\begin{aligned}{e}^{{x}^{2}/12}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y) & ={e}^{{x}^{2}/12}\cdot x \\ {e}^{{x}^{2}/12}\cdot \frac{\text{d}y}{\text{d}x}+\frac{x}{6}{e}^{{x}^{2}/12}\cdot y & =x{e}^{{x}^{2}/12} \\ \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/12}) & =x{e}^{{x}^{2}/12}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{{x}^{2}}{12}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/12})\text{d}x & =\int x{e}^{{x}^{2}/12}\,\text{d}x \\ y{e}^{{x}^{2}/12} & =\int 6{e}^{u}\,\text{d}u \\ y{e}^{{x}^{2}/12} & =6{e}^{u}+C \\ y{e}^{{x}^{2}/12} & =6{e}^{{x}^{2}/12}+C \\ y & =6+C{e}^{-{x}^{2}/12}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=5$ as follows:

$$
\begin{aligned}y(0) & =6+C{e}^{-{0}^{2}/12} \\ 5 & =6+C \\ C & =-1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=6-{e}^{-{x}^{2}/12}.
$$

## Raw original q-335830

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}-2y={e}^{2x}\operatorname{sin}⁡x,\,y(0)=4
$$

Select the correct options below.

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-2:
- `{e}^{-2x}(1+3\operatorname{cos}⁡x)`
- `2{e}^{-2x}(1+\operatorname{cos}⁡x)`
- `{e}^{2x}(5-\operatorname{cos}⁡x)`
- `{e}^{2x}(3+\operatorname{cos}⁡x)`
- `4{e}^{2x}\operatorname{cos}⁡x`

field-1:
- `{e}^{-2x}`
- `-2x`
- `{e}^{2x}`
- `2x`

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=-2$ and $Q(x)={e}^{2x}\operatorname{sin}⁡(x).$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (-2)\,\text{d}x} \\  & ={e}^{-2x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{-2x}$ yields

$$
\begin{aligned}{e}^{-2x}\cdot (\frac{\text{d}y}{\text{d}x}-2y) & ={e}^{-2x}\cdot {e}^{2x}\operatorname{sin}⁡x \\ {e}^{-2x}\cdot \frac{\text{d}y}{\text{d}x}-2{e}^{-2x}\cdot y & =\operatorname{sin}⁡x \\ \frac{\text{d}}{\text{d}x}(y{e}^{-2x}) & =\operatorname{sin}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{-2x})\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ y{e}^{-2x} & =-\operatorname{cos}⁡x+C \\ y & ={e}^{2x}(C-\operatorname{cos}⁡x)\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=4$ as follows:

$$
\begin{aligned}y(0) & ={e}^{2(0)}(C-\operatorname{cos}⁡0) \\ 4 & =C-1 \\ C & =5\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y={e}^{2x}(5-\operatorname{cos}⁡x).
$$

## Original replay q-334916

Consider the following initial value problem.
$\frac{dy}{dx} + y = 1, y(0) =-3$

Select the correct options below.

An integrating factor for this equation is $I(x) =$ {{field-1}}.

The solution to the initial value problem is $y(x) =$ {{field-2}}.

field-1:
- $x^{3}$
- $x$
- $e^{x}$
- $\frac{1}{x}$

field-2:
- $- 4 e^{x} + 1$
- $- 3 e^{- x}$
- $1 - 4 e^{- x}$
- $-4 + e^{- x}$
- $- 3 e^{x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=1.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int 1\,\text{d}x} \\  & =e^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{x}$ yields

$$
\begin{aligned}e^{x}\cdot (\frac{\text{d}y}{\text{d}x}+1y) & =e^{x}\cdot 1 \\ e^{x}\frac{\text{d}y}{\text{d}x}+e^{x}y & =e^{x} \\ \frac{\text{d}}{\text{d}x}(ye^{x}) & =e^{x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{x})\,\text{d}x & =\int e^{x}\,\text{d}x \\ ye^{x} & =1\left(1 e^{x}\right)+C \\ ye^{x} & =e^{x}+C \\ y & =\left(C + e^{x}\right) e^{- x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-3$ as follows:

$$
\begin{aligned}y(0) & =\frac{(e^{(0)})+C}{(e^{(0)})} \\ -3 & =\frac{1+C}{1} \\ C & =-4\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=1 - 4 e^{- x}.
$$

## Generated q-334916 / observed

Consider the following initial value problem.
$\frac{dy}{dx} + y = 1, y(0) =-2$

Select the correct options below.

An integrating factor for this equation is $I(x) =$ {{field-1}}.

The solution to the initial value problem is $y(x) =$ {{field-2}}.

field-1:
- $\frac{1}{x}$
- $x$
- $x^{3}$
- $e^{x}$

field-2:
- $1 - 3 e^{- x}$
- $- 3 e^{x} + 1$
- $- 2 e^{- x}$
- $-3 + e^{- x}$
- $- 2 e^{x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=1.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int 1\,\text{d}x} \\  & =e^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{x}$ yields

$$
\begin{aligned}e^{x}\cdot (\frac{\text{d}y}{\text{d}x}+1y) & =e^{x}\cdot 1 \\ e^{x}\frac{\text{d}y}{\text{d}x}+e^{x}y & =e^{x} \\ \frac{\text{d}}{\text{d}x}(ye^{x}) & =e^{x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{x})\,\text{d}x & =\int e^{x}\,\text{d}x \\ ye^{x} & =1\left(1 e^{x}\right)+C \\ ye^{x} & =e^{x}+C \\ y & =\left(C + e^{x}\right) e^{- x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =\frac{(e^{(0)})+C}{(e^{(0)})} \\ -2 & =\frac{1+C}{1} \\ C & =-3\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=1 - 3 e^{- x}.
$$

## Generated q-334916 / authored

Consider the following initial value problem.
$\frac{dy}{dx} + y = 1, y(0) =-2$

Select the correct options below.

An integrating factor for this equation is $I(x) =$ {{field-1}}.

The solution to the initial value problem is $y(x) =$ {{field-2}}.

field-1:
- $e^{2 x}$
- $e^{x}$
- $x$
- $e^{- x}$

field-2:
- $\left(e^{x} + 3\right) e^{- x}$
- $1 - 3 e^{- x}$
- $-2$
- $e^{x} - 3$
- $- 3 e^{- x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=1.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int 1\,\text{d}x} \\  & =e^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{x}$ yields

$$
\begin{aligned}e^{x}\cdot (\frac{\text{d}y}{\text{d}x}+1y) & =e^{x}\cdot 1 \\ e^{x}\frac{\text{d}y}{\text{d}x}+e^{x}y & =e^{x} \\ \frac{\text{d}}{\text{d}x}(ye^{x}) & =e^{x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{x})\,\text{d}x & =\int e^{x}\,\text{d}x \\ ye^{x} & =1\left(1 e^{x}\right)+C \\ ye^{x} & =e^{x}+C \\ y & =\left(C + e^{x}\right) e^{- x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =\frac{(e^{(0)})+C}{(e^{(0)})} \\ -2 & =\frac{1+C}{1} \\ C & =-3\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=1 - 3 e^{- x}.
$$

## Original replay q-335808

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{x}{2}\cdot y=x,\,y(0)=1
$$

Select the correct options below.

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{\frac{x^{2}}{4}}$
- $\frac{1}{x}$
- $e^{4 x}$
- $x^{3}$

field-2:
- $e^{2 x^{2}}$
- $- e^{x^{2}} + 2$
- $2 x + 1$
- $2 - e^{- \frac{x^{2}}{4}}$
- $2 x^{2} + 1$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{2}$ and $Q(x)=x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (x/2)\,\text{d}x} \\  & ={e}^{{x}^{2}/4}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{{x}^{2}/4}$ yields

$$
\begin{aligned}{e}^{{x}^{2}/4}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{2}y) & ={e}^{{x}^{2}/4}\cdot x \\ {e}^{{x}^{2}/4}\cdot \frac{\text{d}y}{\text{d}x}+\frac{x}{2}{e}^{{x}^{2}/4}\cdot y & =x{e}^{{x}^{2}/4} \\ \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/4}) & =x{e}^{{x}^{2}/4}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{{x}^{2}}{4}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/4})\text{d}x & =\int x{e}^{{x}^{2}/4}\,\text{d}x \\ y{e}^{{x}^{2}/4} & =\int 2{e}^{u}\,\text{d}u \\ y{e}^{{x}^{2}/4} & =2{e}^{u}+C \\ y{e}^{{x}^{2}/4} & =2{e}^{{x}^{2}/4}+C \\ y & =2+C{e}^{-{x}^{2}/4}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=1$ as follows:

$$
\begin{aligned}y(0) & =2+C{e}^{-{0}^{2}/4} \\ 1 & =2+C \\ C & =-1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2 - e^{- \frac{x^{2}}{4}}.
$$

## Generated q-335808 / observed

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{x}{2}\cdot y=x,\,y(0)=0
$$

Select the correct options below.

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x^{3}$
- $\frac{1}{x}$
- $e^{\frac{x^{2}}{4}}$
- $e^{4 x}$

field-2:
- $2 x$
- $e^{2 x^{2}}$
- $- 2 e^{x^{2}} + 2$
- $2 - 2 e^{- \frac{x^{2}}{4}}$
- $2 x^{2}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{2}$ and $Q(x)=x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (x/2)\,\text{d}x} \\  & ={e}^{{x}^{2}/4}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{{x}^{2}/4}$ yields

$$
\begin{aligned}{e}^{{x}^{2}/4}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{2}y) & ={e}^{{x}^{2}/4}\cdot x \\ {e}^{{x}^{2}/4}\cdot \frac{\text{d}y}{\text{d}x}+\frac{x}{2}{e}^{{x}^{2}/4}\cdot y & =x{e}^{{x}^{2}/4} \\ \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/4}) & =x{e}^{{x}^{2}/4}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{{x}^{2}}{4}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/4})\text{d}x & =\int x{e}^{{x}^{2}/4}\,\text{d}x \\ y{e}^{{x}^{2}/4} & =\int 2{e}^{u}\,\text{d}u \\ y{e}^{{x}^{2}/4} & =2{e}^{u}+C \\ y{e}^{{x}^{2}/4} & =2{e}^{{x}^{2}/4}+C \\ y & =2+C{e}^{-{x}^{2}/4}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=0$ as follows:

$$
\begin{aligned}y(0) & =2+C{e}^{-{0}^{2}/4} \\ 0 & =2+C \\ C & =-2\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2 - 2 e^{- \frac{x^{2}}{4}}.
$$

## Generated q-335808 / authored

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{x}{2}\cdot y=x,\,y(0)=3
$$

Select the correct options below.

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $\frac{x^{2}}{4}$
- $e^{\frac{x^{2}}{2}}$
- $e^{- \frac{x^{2}}{4}}$
- $e^{\frac{x^{2}}{4}}$

field-2:
- $e^{- \frac{x^{2}}{4}}$
- $2 e^{\frac{x^{2}}{4}} + 1$
- $3$
- $\left(2 e^{\frac{x^{2}}{4}} - 1\right) e^{- \frac{x^{2}}{4}}$
- $2 + e^{- \frac{x^{2}}{4}}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{2}$ and $Q(x)=x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (x/2)\,\text{d}x} \\  & ={e}^{{x}^{2}/4}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{{x}^{2}/4}$ yields

$$
\begin{aligned}{e}^{{x}^{2}/4}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{2}y) & ={e}^{{x}^{2}/4}\cdot x \\ {e}^{{x}^{2}/4}\cdot \frac{\text{d}y}{\text{d}x}+\frac{x}{2}{e}^{{x}^{2}/4}\cdot y & =x{e}^{{x}^{2}/4} \\ \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/4}) & =x{e}^{{x}^{2}/4}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{{x}^{2}}{4}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/4})\text{d}x & =\int x{e}^{{x}^{2}/4}\,\text{d}x \\ y{e}^{{x}^{2}/4} & =\int 2{e}^{u}\,\text{d}u \\ y{e}^{{x}^{2}/4} & =2{e}^{u}+C \\ y{e}^{{x}^{2}/4} & =2{e}^{{x}^{2}/4}+C \\ y & =2+C{e}^{-{x}^{2}/4}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=3$ as follows:

$$
\begin{aligned}y(0) & =2+C{e}^{-{0}^{2}/4} \\ 3 & =2+C \\ C & =1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2 + e^{- \frac{x^{2}}{4}}.
$$

## Original replay q-335810

Consider the following initial value problem.

$$
x\frac{\text{d}y}{\text{d}x}+2y=4{x}^{2},\,y(1)=2
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{x}$
- $2 x$
- $e^{2 x}$
- $x^{2}$

field-2:
- $3 x^{2} - \frac{1}{x^{2}}$
- $x^{2} + \frac{1}{x^{2}}$
- $3 x - \frac{1}{x^{2}}$
- $x + \frac{1}{x^{2}}$

The first step is to write the equation in standard form,

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)\,.
$$

In doing so, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2y & =4{x}^{2} \\ \frac{1}{x}(x\frac{\text{d}y}{\text{d}x}+2y) & =\frac{1}{x}\cdot 4{x}^{2} \\ \frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y & =4x.\end{aligned}
$$

Consequently,

$$
\begin{aligned}P(x)=\frac{2}{x},\,Q(x)=4x.\end{aligned}
$$

We then compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\int (1/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡{x}^{2}} \\  & ={x}^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={x}^{2}$ yields

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & ={x}^{2}\cdot 4x \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =4{x}^{3} \\ \frac{\text{d}}{\text{d}x}(y{x}^{2}) & =4{x}^{3}.\end{aligned}
$$

$$

$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int 4{x}^{3}\,\text{d}x \\ y{x}^{2} & ={x}^{4}+C \\ y & ={x}^{2}+\frac{C}{{x}^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(1)=2$ as follows:

$$
\begin{aligned}y(1) & ={1}^{2}+\frac{C}{{1}^{2}} \\ 2 & =1+C \\ C & =1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{x^{4} + 1}{x^{2}}.
$$

## Generated q-335810 / observed

Consider the following initial value problem.

$$
x\frac{\text{d}y}{\text{d}x}+2y=4{x}^{2},\,y(1)=3
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x^{2}$
- $2 x$
- $e^{x}$
- $e^{2 x}$

field-2:
- $4 x^{2} - \frac{2}{x^{2}}$
- $x^{2} + \frac{2}{x^{2}}$
- $4 x - \frac{2}{x^{2}}$
- $x + \frac{2}{x^{2}}$

The first step is to write the equation in standard form,

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)\,.
$$

In doing so, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2y & =4{x}^{2} \\ \frac{1}{x}(x\frac{\text{d}y}{\text{d}x}+2y) & =\frac{1}{x}\cdot 4{x}^{2} \\ \frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y & =4x.\end{aligned}
$$

Consequently,

$$
\begin{aligned}P(x)=\frac{2}{x},\,Q(x)=4x.\end{aligned}
$$

We then compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\int (1/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡{x}^{2}} \\  & ={x}^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={x}^{2}$ yields

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & ={x}^{2}\cdot 4x \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =4{x}^{3} \\ \frac{\text{d}}{\text{d}x}(y{x}^{2}) & =4{x}^{3}.\end{aligned}
$$

$$

$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int 4{x}^{3}\,\text{d}x \\ y{x}^{2} & ={x}^{4}+C \\ y & ={x}^{2}+\frac{C}{{x}^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(1)=3$ as follows:

$$
\begin{aligned}y(1) & ={1}^{2}+\frac{C}{{1}^{2}} \\ 3 & =1+C \\ C & =2\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{x^{4} + 2}{x^{2}}.
$$

## Generated q-335810 / authored

Consider the following initial value problem.

$$
x\frac{\text{d}y}{\text{d}x}+2y=4{x}^{2},\,y(1)=3
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $\frac{2}{x}$
- $x^{2}$
- $e^{x}$
- $\frac{1}{x^{2}}$

field-2:
- $\frac{x^{4} - 2}{x^{2}}$
- $\frac{x^{4} + 2}{x^{2}}$
- $x^{2} + 2$
- $x^{4} + 2$
- $\frac{2}{x^{2}}$

The first step is to write the equation in standard form,

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)\,.
$$

In doing so, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2y & =4{x}^{2} \\ \frac{1}{x}(x\frac{\text{d}y}{\text{d}x}+2y) & =\frac{1}{x}\cdot 4{x}^{2} \\ \frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y & =4x.\end{aligned}
$$

Consequently,

$$
\begin{aligned}P(x)=\frac{2}{x},\,Q(x)=4x.\end{aligned}
$$

We then compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\int (1/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡{x}^{2}} \\  & ={x}^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={x}^{2}$ yields

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & ={x}^{2}\cdot 4x \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =4{x}^{3} \\ \frac{\text{d}}{\text{d}x}(y{x}^{2}) & =4{x}^{3}.\end{aligned}
$$

$$

$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int 4{x}^{3}\,\text{d}x \\ y{x}^{2} & ={x}^{4}+C \\ y & ={x}^{2}+\frac{C}{{x}^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(1)=3$ as follows:

$$
\begin{aligned}y(1) & ={1}^{2}+\frac{C}{{1}^{2}} \\ 3 & =1+C \\ C & =2\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{x^{4} + 2}{x^{2}}.
$$

## Original replay q-335811

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{2y}{x}=\frac{\operatorname{cos}⁡x}{{x}^{2}},\,y(\pi )=0
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x^{2}$
- $e^{x^{2}}$
- $e^{2 x}$
- $2 x$

field-2:
- $x^{2} \sin{\left(x \right)}$
- $x \sin{\left(x \right)}$
- $\frac{\sin{\left(x \right)}}{x}$
- $\frac{\sin{\left(x \right)}}{x^{2}}$
- $\frac{\sin{\left(x \right)}}{x^{2}}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{\operatorname{cos}⁡x}{{x}^{2}}.$ 

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\int (1/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡{x}^{2}} \\  & ={x}^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={x}^{2}$ yields

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y) & ={x}^{2}\cdot \frac{\operatorname{cos}⁡x}{{x}^{2}} \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =\operatorname{cos}⁡x \\ \frac{\text{d}}{\text{d}x}(y{x}^{2}) & =\operatorname{cos}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int \operatorname{cos}⁡x\,\text{d}x \\ y{x}^{2} & =\operatorname{sin}⁡x+C \\ y & =\frac{\operatorname{sin}⁡x+C}{{x}^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\pi )=0$ as follows:

$$
\begin{aligned}y(\pi ) & =\frac{\operatorname{sin}⁡(\pi )+C}{{\pi }^{2}} \\ 0 & =\frac{C}{{\pi }^{2}} \\ C & =0\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{\operatorname{sin}⁡x}{{x}^{2}}.
$$

## Generated q-335811 / observed

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{2y}{x}=\frac{2\operatorname{cos}⁡x}{{x}^{2}},\,y(\pi )=0
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $2 x$
- $e^{x^{2}}$
- $x^{2}$
- $e^{2 x}$

field-2:
- $\frac{2 \sin{\left(x \right)}}{x}$
- $2 x^{2} \sin{\left(x \right)}$
- $2 x \sin{\left(x \right)}$
- $\frac{2 \sin{\left(x \right)}}{x^{2}}$
- $\frac{2 \sin{\left(x \right)}}{x^{2}}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{2\operatorname{cos}⁡x}{{x}^{2}}.$ 

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\int (1/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡{x}^{2}} \\  & ={x}^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={x}^{2}$ yields

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y) & ={x}^{2}\cdot \frac{2\operatorname{cos}⁡x}{{x}^{2}} \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =2\operatorname{cos}⁡x \\ \frac{\text{d}}{\text{d}x}(y{x}^{2}) & =2\operatorname{cos}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int 2\operatorname{cos}⁡x\,\text{d}x \\ y{x}^{2} & =2\operatorname{sin}⁡x+C \\ y & =\frac{2\operatorname{sin}⁡x+C}{{x}^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\pi )=0$ as follows:

$$
\begin{aligned}y(\pi ) & =\frac{2\operatorname{sin}⁡(\pi )+C}{{\pi }^{2}} \\ 0 & =\frac{C}{{\pi }^{2}} \\ C & =0\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{2\operatorname{sin}⁡x}{{x}^{2}}.
$$

## Generated q-335811 / authored

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{2y}{x}=\frac{2\operatorname{cos}⁡x}{{x}^{2}},\,y(\pi )=0
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $\frac{2}{x}$
- $x^{2}$
- $e^{x}$
- $\frac{1}{x^{2}}$

field-2:
- $- \frac{2 \sin{\left(x \right)}}{x^{2}}$
- $\frac{2 \sin{\left(x \right)}}{x^{2}}$
- $2 x \sin{\left(x \right)}$
- $\frac{2 \sin{\left(x \right)}}{x}$
- $2 x^{2} \sin{\left(x \right)}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{2\operatorname{cos}⁡x}{{x}^{2}}.$ 

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\int (1/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡{x}^{2}} \\  & ={x}^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={x}^{2}$ yields

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y) & ={x}^{2}\cdot \frac{2\operatorname{cos}⁡x}{{x}^{2}} \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =2\operatorname{cos}⁡x \\ \frac{\text{d}}{\text{d}x}(y{x}^{2}) & =2\operatorname{cos}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int 2\operatorname{cos}⁡x\,\text{d}x \\ y{x}^{2} & =2\operatorname{sin}⁡x+C \\ y & =\frac{2\operatorname{sin}⁡x+C}{{x}^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\pi )=0$ as follows:

$$
\begin{aligned}y(\pi ) & =\frac{2\operatorname{sin}⁡(\pi )+C}{{\pi }^{2}} \\ 0 & =\frac{C}{{\pi }^{2}} \\ C & =0\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{2\operatorname{sin}⁡x}{{x}^{2}}.
$$

## Original replay q-335812

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y=\frac{\operatorname{sin}⁡x}{x},\,x>0,\,y(\frac{\pi }{2})=1
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x$
- $\frac{1}{x}$
- $e^{x}$
- $\ln{\left(x \right)}$

field-2:
- $\frac{3 \cos{\left(x \right)} + \pi}{2 x}$
- $\frac{- \cos{\left(x \right)} + \frac{\pi}{2}}{x}$
- $\frac{4 \cos{\left(x \right)} + \pi}{2 x}$
- $\frac{- \cos{\left(x \right)} + \frac{\pi}{2}}{x}$
- $\frac{- \cos{\left(x \right)} + \pi}{2 x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡x}{x}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (1/x)\,\text{d}x} \\  & ={e}^{\operatorname{ln}⁡x} \\  & =x\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x$ yields

$$
\begin{aligned}x\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y) & =x\cdot \frac{\operatorname{sin}⁡x}{x} \\ x\frac{\text{d}y}{\text{d}x}+y & =\operatorname{sin}⁡x \\ \frac{\text{d}}{\text{d}x}(yx) & =\operatorname{sin}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx)\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ yx & =-\operatorname{cos}⁡x+C \\ y & =\frac{-\operatorname{cos}⁡x+C}{x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\frac{\pi }{2})=1$ as follows:

$$
\begin{aligned}y(\frac{\pi }{2}) & =\frac{-\operatorname{cos}⁡(\frac{\pi }{2})+C}{(\frac{\pi }{2})} \\ 1 & =\frac{2C}{\pi } \\ C & =\frac{\pi}{2}\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
\begin{aligned}y & =\frac{(-\operatorname{cos}⁡x+\frac{\pi}{2})}{x} \\  & =\frac{\pi}{2 x}-\frac{\operatorname{cos}⁡x}{x} \\  & =\frac{- \cos{\left(x \right)} + \frac{\pi}{2}}{x}.\end{aligned}
$$

## Generated q-335812 / observed

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y=\frac{\operatorname{sin}⁡x}{x},\,x>0,\,y(\frac{\pi }{2})=0
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $\ln{\left(x \right)}$
- $\frac{1}{x}$
- $x$
- $e^{x}$

field-2:
- $\frac{2 \cos{\left(x \right)}}{x}$
- $\frac{3 \cos{\left(x \right)}}{2 x}$
- $- \frac{\cos{\left(x \right)}}{x}$
- $- \frac{\cos{\left(x \right)}}{x}$
- $- \frac{\cos{\left(x \right)}}{2 x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡x}{x}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (1/x)\,\text{d}x} \\  & ={e}^{\operatorname{ln}⁡x} \\  & =x\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x$ yields

$$
\begin{aligned}x\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y) & =x\cdot \frac{\operatorname{sin}⁡x}{x} \\ x\frac{\text{d}y}{\text{d}x}+y & =\operatorname{sin}⁡x \\ \frac{\text{d}}{\text{d}x}(yx) & =\operatorname{sin}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx)\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ yx & =-\operatorname{cos}⁡x+C \\ y & =\frac{-\operatorname{cos}⁡x+C}{x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\frac{\pi }{2})=0$ as follows:

$$
\begin{aligned}y(\frac{\pi }{2}) & =\frac{-\operatorname{cos}⁡(\frac{\pi }{2})+C}{(\frac{\pi }{2})} \\ 0 & =\frac{2C}{\pi } \\ C & =0\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
\begin{aligned}y & =\frac{(-\operatorname{cos}⁡x+0)}{x} \\  & =0-\frac{\operatorname{cos}⁡x}{x} \\  & =- \frac{\cos{\left(x \right)}}{x}.\end{aligned}
$$

## Generated q-335812 / authored

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y=\frac{\operatorname{sin}⁡x}{x},\,x>0,\,y(\frac{\pi }{2})=3
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{x}$
- $\ln{\left(x \right)}$
- $\frac{1}{x}$
- $x$

field-2:
- $\frac{3 \pi}{2 x}$
- $- \cos{\left(x \right)} + \frac{3 \pi}{2}$
- $\frac{3 \pi}{2} - \frac{\cos{\left(x \right)}}{x}$
- $\frac{- \cos{\left(x \right)} - \frac{3 \pi}{2}}{x}$
- $\frac{- \cos{\left(x \right)} + \frac{3 \pi}{2}}{x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡x}{x}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (1/x)\,\text{d}x} \\  & ={e}^{\operatorname{ln}⁡x} \\  & =x\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x$ yields

$$
\begin{aligned}x\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y) & =x\cdot \frac{\operatorname{sin}⁡x}{x} \\ x\frac{\text{d}y}{\text{d}x}+y & =\operatorname{sin}⁡x \\ \frac{\text{d}}{\text{d}x}(yx) & =\operatorname{sin}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx)\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ yx & =-\operatorname{cos}⁡x+C \\ y & =\frac{-\operatorname{cos}⁡x+C}{x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\frac{\pi }{2})=3$ as follows:

$$
\begin{aligned}y(\frac{\pi }{2}) & =\frac{-\operatorname{cos}⁡(\frac{\pi }{2})+C}{(\frac{\pi }{2})} \\ 3 & =\frac{2C}{\pi } \\ C & =\frac{3 \pi}{2}\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
\begin{aligned}y & =\frac{(-\operatorname{cos}⁡x+\frac{3 \pi}{2})}{x} \\  & =\frac{3 \pi}{2 x}-\frac{\operatorname{cos}⁡x}{x} \\  & =\frac{- \cos{\left(x \right)} + \frac{3 \pi}{2}}{x}.\end{aligned}
$$

## Original replay q-335806

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+y=2x{e}^{-x},\,y(0)=-2
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{- x}$
- $e^{x}$
- $x$
- $x^{2}$

field-2:
- $\left(x - 2\right) e^{x}$
- $\left(x^{2} - 2\right) e^{- x}$
- $\left(x^{2} - 2\right) e^{x}$
- $\left(x - 2\right) e^{- x}$
- $- 2 e^{- x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=2x{e}^{-x}.$ 

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 1\,\text{d}x} \\  & ={e}^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{x}$ yields

$$
\begin{aligned}{e}^{x}\cdot (\frac{\text{d}y}{\text{d}x}+y) & ={e}^{x}\cdot 2x{e}^{-x} \\ {e}^{x}\frac{\text{d}y}{\text{d}x}+{e}^{x}y & =2x \\ \frac{\text{d}}{\text{d}x}(y{e}^{x}) & =2x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{x})\text{d}x & =\int 2x\,\text{d}x \\ y{e}^{x} & ={x}^{2}+C \\ y & =({x}^{2}+C){e}^{-x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =({0}^{2}+C){e}^{-0} \\ -2 & =(0+C)\cdot 1 \\ C & =-2\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\left(x^{2} - 2\right) e^{- x}.
$$

## Generated q-335806 / observed

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+y=2x{e}^{-x},\,y(0)=-1
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x^{2}$
- $e^{x}$
- $e^{- x}$
- $x$

field-2:
- $\left(x^{2} - 1\right) e^{x}$
- $\left(x - 1\right) e^{x}$
- $\left(x^{2} - 1\right) e^{- x}$
- $\left(x - 1\right) e^{- x}$
- $- e^{- x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=2x{e}^{-x}.$ 

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 1\,\text{d}x} \\  & ={e}^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{x}$ yields

$$
\begin{aligned}{e}^{x}\cdot (\frac{\text{d}y}{\text{d}x}+y) & ={e}^{x}\cdot 2x{e}^{-x} \\ {e}^{x}\frac{\text{d}y}{\text{d}x}+{e}^{x}y & =2x \\ \frac{\text{d}}{\text{d}x}(y{e}^{x}) & =2x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{x})\text{d}x & =\int 2x\,\text{d}x \\ y{e}^{x} & ={x}^{2}+C \\ y & =({x}^{2}+C){e}^{-x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-1$ as follows:

$$
\begin{aligned}y(0) & =({0}^{2}+C){e}^{-0} \\ -1 & =(0+C)\cdot 1 \\ C & =-1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\left(x^{2} - 1\right) e^{- x}.
$$

## Generated q-335806 / authored

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+y=2x{e}^{-x},\,y(0)=-1
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{2 x}$
- $e^{x}$
- $x$
- $e^{- x}$

field-2:
- $\left(x^{2} + 1\right) e^{- x}$
- $\left(x^{2} - 1\right) e^{- x}$
- $x^{2} e^{- x} - 1$
- $x^{2} - 1$
- $- e^{- x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=2x{e}^{-x}.$ 

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 1\,\text{d}x} \\  & ={e}^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{x}$ yields

$$
\begin{aligned}{e}^{x}\cdot (\frac{\text{d}y}{\text{d}x}+y) & ={e}^{x}\cdot 2x{e}^{-x} \\ {e}^{x}\frac{\text{d}y}{\text{d}x}+{e}^{x}y & =2x \\ \frac{\text{d}}{\text{d}x}(y{e}^{x}) & =2x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{x})\text{d}x & =\int 2x\,\text{d}x \\ y{e}^{x} & ={x}^{2}+C \\ y & =({x}^{2}+C){e}^{-x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-1$ as follows:

$$
\begin{aligned}y(0) & =({0}^{2}+C){e}^{-0} \\ -1 & =(0+C)\cdot 1 \\ C & =-1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\left(x^{2} - 1\right) e^{- x}.
$$

## Original replay q-335829

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+4y=8,\,y(0)=-1
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{4 x}$
- $e^{2 x}$
- $4 x$
- $e^{8 x}$

field-2:
- $2 - 3 e^{- 4 x}$
- $- e^{- 4 x}$
- $1 - 2 e^{- 4 x}$
- $- e^{4 x}$
- $- 5 e^{4 x} + 4$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=4$ and $Q(x)=8.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 4\,\text{d}x} \\  & ={e}^{4x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{4x}$ yields

$$
\begin{aligned}{e}^{4x}\cdot (\frac{\text{d}y}{\text{d}x}+4y) & ={e}^{4x}\cdot 8 \\ {e}^{4x}\cdot \frac{\text{d}y}{\text{d}x}+4{e}^{4x}\cdot y & =8{e}^{4x} \\ \frac{\text{d}}{\text{d}x}(y{e}^{4x}) & =8{e}^{4x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{4x})\text{d}x & =\int 8{e}^{4x}\,\text{d}x \\ y{e}^{4x} & =8(\frac{1}{4}{e}^{4x})+C \\ y{e}^{4x} & =2{e}^{4x}+C \\ y & =2+C{e}^{-4x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-1$ as follows:

$$
\begin{aligned}y(0) & =2+C{e}^{-4(0)} \\ -1 & =2+C(1) \\ C & =-3\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2 - 3 e^{- 4 x}.
$$

## Generated q-335829 / observed

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+4y=8,\,y(0)=-2
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{8 x}$
- $e^{2 x}$
- $e^{4 x}$
- $4 x$

field-2:
- $1 - 3 e^{- 4 x}$
- $2 - 4 e^{- 4 x}$
- $- 2 e^{- 4 x}$
- $- 2 e^{4 x}$
- $- 6 e^{4 x} + 4$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=4$ and $Q(x)=8.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 4\,\text{d}x} \\  & ={e}^{4x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{4x}$ yields

$$
\begin{aligned}{e}^{4x}\cdot (\frac{\text{d}y}{\text{d}x}+4y) & ={e}^{4x}\cdot 8 \\ {e}^{4x}\cdot \frac{\text{d}y}{\text{d}x}+4{e}^{4x}\cdot y & =8{e}^{4x} \\ \frac{\text{d}}{\text{d}x}(y{e}^{4x}) & =8{e}^{4x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{4x})\text{d}x & =\int 8{e}^{4x}\,\text{d}x \\ y{e}^{4x} & =8(\frac{1}{4}{e}^{4x})+C \\ y{e}^{4x} & =2{e}^{4x}+C \\ y & =2+C{e}^{-4x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =2+C{e}^{-4(0)} \\ -2 & =2+C(1) \\ C & =-4\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2 - 4 e^{- 4 x}.
$$

## Generated q-335829 / authored

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+4y=8,\,y(0)=-2
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{8 x}$
- $e^{4 x}$
- $4 x$
- $e^{- 4 x}$

field-2:
- $\left(2 e^{4 x} + 4\right) e^{- 4 x}$
- $2 - 4 e^{- 4 x}$
- $-2$
- $2 e^{4 x} - 4$
- $- 4 e^{- 4 x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=4$ and $Q(x)=8.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 4\,\text{d}x} \\  & ={e}^{4x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{4x}$ yields

$$
\begin{aligned}{e}^{4x}\cdot (\frac{\text{d}y}{\text{d}x}+4y) & ={e}^{4x}\cdot 8 \\ {e}^{4x}\cdot \frac{\text{d}y}{\text{d}x}+4{e}^{4x}\cdot y & =8{e}^{4x} \\ \frac{\text{d}}{\text{d}x}(y{e}^{4x}) & =8{e}^{4x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{4x})\text{d}x & =\int 8{e}^{4x}\,\text{d}x \\ y{e}^{4x} & =8(\frac{1}{4}{e}^{4x})+C \\ y{e}^{4x} & =2{e}^{4x}+C \\ y & =2+C{e}^{-4x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =2+C{e}^{-4(0)} \\ -2 & =2+C(1) \\ C & =-4\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2 - 4 e^{- 4 x}.
$$

## Original replay q-339145

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y=x,\,y(0)=5
$$

Select the correct options below.
$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x^{6}$
- $e^{12 x}$
- $\frac{1}{x}$
- $e^{\frac{x^{2}}{12}}$

field-2:
- $- e^{x^{2}} + 6$
- $6 - e^{- \frac{x^{2}}{12}}$
- $6 x + 5$
- $6 x^{2} + 5$
- $e^{6 x^{2}}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{6}$ and $Q(x)=x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (x/6)\,\text{d}x} \\  & ={e}^{{x}^{2}/12}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{{x}^{2}/12}$ yields

$$
\begin{aligned}{e}^{{x}^{2}/12}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y) & ={e}^{{x}^{2}/12}\cdot x \\ {e}^{{x}^{2}/12}\cdot \frac{\text{d}y}{\text{d}x}+\frac{x}{6}{e}^{{x}^{2}/12}\cdot y & =x{e}^{{x}^{2}/12} \\ \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/12}) & =x{e}^{{x}^{2}/12}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{{x}^{2}}{12}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/12})\text{d}x & =\int x{e}^{{x}^{2}/12}\,\text{d}x \\ y{e}^{{x}^{2}/12} & =\int 6{e}^{u}\,\text{d}u \\ y{e}^{{x}^{2}/12} & =6{e}^{u}+C \\ y{e}^{{x}^{2}/12} & =6{e}^{{x}^{2}/12}+C \\ y & =6+C{e}^{-{x}^{2}/12}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=5$ as follows:

$$
\begin{aligned}y(0) & =6+C{e}^{-{0}^{2}/12} \\ 5 & =6+C \\ C & =-1\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=6 - e^{- \frac{x^{2}}{12}}.
$$

## Generated q-339145 / observed

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y=x,\,y(0)=4
$$

Select the correct options below.
$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{\frac{x^{2}}{12}}$
- $e^{12 x}$
- $x^{6}$
- $\frac{1}{x}$

field-2:
- $6 x + 4$
- $- 2 e^{x^{2}} + 6$
- $6 - 2 e^{- \frac{x^{2}}{12}}$
- $6 x^{2} + 4$
- $e^{6 x^{2}}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{6}$ and $Q(x)=x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (x/6)\,\text{d}x} \\  & ={e}^{{x}^{2}/12}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{{x}^{2}/12}$ yields

$$
\begin{aligned}{e}^{{x}^{2}/12}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y) & ={e}^{{x}^{2}/12}\cdot x \\ {e}^{{x}^{2}/12}\cdot \frac{\text{d}y}{\text{d}x}+\frac{x}{6}{e}^{{x}^{2}/12}\cdot y & =x{e}^{{x}^{2}/12} \\ \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/12}) & =x{e}^{{x}^{2}/12}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{{x}^{2}}{12}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/12})\text{d}x & =\int x{e}^{{x}^{2}/12}\,\text{d}x \\ y{e}^{{x}^{2}/12} & =\int 6{e}^{u}\,\text{d}u \\ y{e}^{{x}^{2}/12} & =6{e}^{u}+C \\ y{e}^{{x}^{2}/12} & =6{e}^{{x}^{2}/12}+C \\ y & =6+C{e}^{-{x}^{2}/12}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=4$ as follows:

$$
\begin{aligned}y(0) & =6+C{e}^{-{0}^{2}/12} \\ 4 & =6+C \\ C & =-2\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=6 - 2 e^{- \frac{x^{2}}{12}}.
$$

## Generated q-339145 / authored

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y=x,\,y(0)=4
$$

Select the correct options below.
$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{\frac{x^{2}}{6}}$
- $e^{\frac{x^{2}}{12}}$
- $\frac{x^{2}}{12}$
- $e^{- \frac{x^{2}}{12}}$

field-2:
- $\left(6 e^{\frac{x^{2}}{12}} + 2\right) e^{- \frac{x^{2}}{12}}$
- $6 - 2 e^{- \frac{x^{2}}{12}}$
- $4$
- $6 e^{\frac{x^{2}}{12}} - 2$
- $- 2 e^{- \frac{x^{2}}{12}}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{6}$ and $Q(x)=x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (x/6)\,\text{d}x} \\  & ={e}^{{x}^{2}/12}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{{x}^{2}/12}$ yields

$$
\begin{aligned}{e}^{{x}^{2}/12}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y) & ={e}^{{x}^{2}/12}\cdot x \\ {e}^{{x}^{2}/12}\cdot \frac{\text{d}y}{\text{d}x}+\frac{x}{6}{e}^{{x}^{2}/12}\cdot y & =x{e}^{{x}^{2}/12} \\ \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/12}) & =x{e}^{{x}^{2}/12}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{{x}^{2}}{12}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{{x}^{2}/12})\text{d}x & =\int x{e}^{{x}^{2}/12}\,\text{d}x \\ y{e}^{{x}^{2}/12} & =\int 6{e}^{u}\,\text{d}u \\ y{e}^{{x}^{2}/12} & =6{e}^{u}+C \\ y{e}^{{x}^{2}/12} & =6{e}^{{x}^{2}/12}+C \\ y & =6+C{e}^{-{x}^{2}/12}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=4$ as follows:

$$
\begin{aligned}y(0) & =6+C{e}^{-{0}^{2}/12} \\ 4 & =6+C \\ C & =-2\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=6 - 2 e^{- \frac{x^{2}}{12}}.
$$

## Original replay q-335830

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}-2y={e}^{2x}\operatorname{sin}⁡x,\,y(0)=4
$$

Select the correct options below.

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{2 x}$
- $e^{- 2 x}$
- $- 2 x$
- $2 x$

field-2:
- $\left(3 \cos{\left(x \right)} + 1\right) e^{- 2 x}$
- $4 e^{2 x} \cos{\left(x \right)}$
- $2 \left(\cos{\left(x \right)} + 1\right) e^{- 2 x}$
- $\left(\cos{\left(x \right)} + 3\right) e^{2 x}$
- $\left(- \cos{\left(x \right)} + 5\right) e^{2 x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=-2$ and $Q(x)={e}^{2x}\operatorname{sin}⁡(x).$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (-2)\,\text{d}x} \\  & ={e}^{-2x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{-2x}$ yields

$$
\begin{aligned}{e}^{-2x}\cdot (\frac{\text{d}y}{\text{d}x}-2y) & ={e}^{-2x}\cdot {e}^{2x}\operatorname{sin}⁡x \\ {e}^{-2x}\cdot \frac{\text{d}y}{\text{d}x}-2{e}^{-2x}\cdot y & =\operatorname{sin}⁡x \\ \frac{\text{d}}{\text{d}x}(y{e}^{-2x}) & =\operatorname{sin}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{-2x})\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ y{e}^{-2x} & =-\operatorname{cos}⁡x+C \\ y & ={e}^{2x}(C-\operatorname{cos}⁡x)\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=4$ as follows:

$$
\begin{aligned}y(0) & ={e}^{2(0)}(C-\operatorname{cos}⁡0) \\ 4 & =C-1 \\ C & =5\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\left(- \cos{\left(x \right)} + 5\right) e^{2 x}.
$$

## Generated q-335830 / observed

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}-2y={e}^{2x}\operatorname{sin}⁡x,\,y(0)=5
$$

Select the correct options below.

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $2 x$
- $e^{- 2 x}$
- $e^{2 x}$
- $- 2 x$

field-2:
- $2 \left(\cos{\left(x \right)} + 1\right) e^{- 2 x}$
- $\left(3 \cos{\left(x \right)} + 1\right) e^{- 2 x}$
- $5 e^{2 x} \cos{\left(x \right)}$
- $\left(\cos{\left(x \right)} + 4\right) e^{2 x}$
- $\left(- \cos{\left(x \right)} + 6\right) e^{2 x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=-2$ and $Q(x)={e}^{2x}\operatorname{sin}⁡(x).$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (-2)\,\text{d}x} \\  & ={e}^{-2x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{-2x}$ yields

$$
\begin{aligned}{e}^{-2x}\cdot (\frac{\text{d}y}{\text{d}x}-2y) & ={e}^{-2x}\cdot {e}^{2x}\operatorname{sin}⁡x \\ {e}^{-2x}\cdot \frac{\text{d}y}{\text{d}x}-2{e}^{-2x}\cdot y & =\operatorname{sin}⁡x \\ \frac{\text{d}}{\text{d}x}(y{e}^{-2x}) & =\operatorname{sin}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{-2x})\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ y{e}^{-2x} & =-\operatorname{cos}⁡x+C \\ y & ={e}^{2x}(C-\operatorname{cos}⁡x)\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=5$ as follows:

$$
\begin{aligned}y(0) & ={e}^{2(0)}(C-\operatorname{cos}⁡0) \\ 5 & =C-1 \\ C & =6\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\left(- \cos{\left(x \right)} + 6\right) e^{2 x}.
$$

## Generated q-335830 / authored

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}-2y={e}^{2x}\operatorname{sin}⁡x,\,y(0)=5
$$

Select the correct options below.

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{- 4 x}$
- $e^{- 2 x}$
- $- 2 x$
- $e^{2 x}$

field-2:
- $\left(- \cos{\left(x \right)} - 6\right) e^{2 x}$
- $\left(- \cos{\left(x \right)} + 6\right) e^{2 x}$
- $- e^{2 x} \cos{\left(x \right)} + 6$
- $- \cos{\left(x \right)} + 6$
- $6 e^{2 x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=-2$ and $Q(x)={e}^{2x}\operatorname{sin}⁡(x).$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (-2)\,\text{d}x} \\  & ={e}^{-2x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)={e}^{-2x}$ yields

$$
\begin{aligned}{e}^{-2x}\cdot (\frac{\text{d}y}{\text{d}x}-2y) & ={e}^{-2x}\cdot {e}^{2x}\operatorname{sin}⁡x \\ {e}^{-2x}\cdot \frac{\text{d}y}{\text{d}x}-2{e}^{-2x}\cdot y & =\operatorname{sin}⁡x \\ \frac{\text{d}}{\text{d}x}(y{e}^{-2x}) & =\operatorname{sin}⁡x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(y{e}^{-2x})\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ y{e}^{-2x} & =-\operatorname{cos}⁡x+C \\ y & ={e}^{2x}(C-\operatorname{cos}⁡x)\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=5$ as follows:

$$
\begin{aligned}y(0) & ={e}^{2(0)}(C-\operatorname{cos}⁡0) \\ 5 & =C-1 \\ C & =6\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\left(- \cos{\left(x \right)} + 6\right) e^{2 x}.
$$

## Authored easy_constant seed 0

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(1\right)y=3,\quad y(0)=-6
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{x}$
- $x$
- $e^{- x}$
- $e^{2 x}$

field-2:
- $\left(3 e^{x} + 9\right) e^{- x}$
- $3 - 9 e^{- x}$
- $-6$
- $- 9 e^{- x}$
- $3 e^{x} - 9$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=3.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int 1\,\text{d}x} \\  & =e^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{x}$ yields

$$
\begin{aligned}e^{x}\cdot (\frac{\text{d}y}{\text{d}x}+1y) & =e^{x}\cdot 3 \\ e^{x}\frac{\text{d}y}{\text{d}x}+e^{x}y & =3 e^{x} \\ \frac{\text{d}}{\text{d}x}(ye^{x}) & =3 e^{x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{x})\,\text{d}x & =\int 3 e^{x}\,\text{d}x \\ ye^{x} & =3\left(1 e^{x}\right)+C \\ ye^{x} & =3 e^{x}+C \\ y & =\left(C + 3 e^{x}\right) e^{- x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-6$ as follows:

$$
\begin{aligned}y(0) & =\frac{(3 e^{(0)})+C}{(e^{(0)})} \\ -6 & =\frac{3+C}{1} \\ C & =-9\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=3 - 9 e^{- x}.
$$

## Authored easy_constant seed 1

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(1\right)y=5,\quad y(0)=-4
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x$
- $e^{2 x}$
- $e^{- x}$
- $e^{x}$

field-2:
- $5 - 9 e^{- x}$
- $- 9 e^{- x}$
- $\left(5 e^{x} + 9\right) e^{- x}$
- $-4$
- $5 e^{x} - 9$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=1$ and $Q(x)=5.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int 1\,\text{d}x} \\  & =e^{x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{x}$ yields

$$
\begin{aligned}e^{x}\cdot (\frac{\text{d}y}{\text{d}x}+1y) & =e^{x}\cdot 5 \\ e^{x}\frac{\text{d}y}{\text{d}x}+e^{x}y & =5 e^{x} \\ \frac{\text{d}}{\text{d}x}(ye^{x}) & =5 e^{x}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{x})\,\text{d}x & =\int 5 e^{x}\,\text{d}x \\ ye^{x} & =5\left(1 e^{x}\right)+C \\ ye^{x} & =5 e^{x}+C \\ y & =\left(C + 5 e^{x}\right) e^{- x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-4$ as follows:

$$
\begin{aligned}y(0) & =\frac{(5 e^{(0)})+C}{(e^{(0)})} \\ -4 & =\frac{5+C}{1} \\ C & =-9\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=5 - 9 e^{- x}.
$$

## Authored moderate_nonstandard seed 0

Consider the following initial value problem.

$$
x\frac{\text{d}y}{\text{d}x}+2y=12 x^{2},\quad x>0,\quad y(1)=-6
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x^{2}$
- $e^{x}$
- $\frac{1}{x^{2}}$
- $\frac{2}{x}$

field-2:
- $\frac{3 x^{4} + 9}{x^{2}}$
- $\frac{3 \left(x^{4} - 3\right)}{x^{2}}$
- $3 x^{2} - 9$
- $- \frac{9}{x^{2}}$
- $3 x^{4} - 9$

The first step is to write the equation in standard form,

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2y & =12 x^{2} \\ \frac{1}{x}\left(x\frac{\text{d}y}{\text{d}x}+2y\right) & =\frac{1}{x}\cdot 12 x^{2} \\ \frac{\text{d}y}{\text{d}x}+\frac{2}{x}y & =12 x\end{aligned}
$$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=12 x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{2}{x}\,\text{d}x} \\  & =e^{2 \ln{\left(x \right)}} \\  & =x^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x^{2}$ yields

$$
\begin{aligned}x^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & =x^{2}\cdot 12 x \\ x^{2}\frac{\text{d}y}{\text{d}x}+2 xy & =12 x^{3} \\ \frac{\text{d}}{\text{d}x}(yx^{2}) & =12 x^{3}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx^{2})\,\text{d}x & =\int 12 x^{3}\,\text{d}x \\ yx^{2} & =3 x^{4}+C \\ y & =\frac{C + 3 x^{4}}{x^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(1)=-6$ as follows:

$$
\begin{aligned}y(1) & =\frac{(3 (1)^{4})+C}{((1)^{2})} \\ -6 & =\frac{3+C}{1} \\ C & =-9\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{3 \left(x^{4} - 3\right)}{x^{2}}.
$$

## Authored moderate_nonstandard seed 1

Consider the following initial value problem.

$$
x\frac{\text{d}y}{\text{d}x}+2y=20 x^{2},\quad x>0,\quad y(1)=-4
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{x}$
- $\frac{2}{x}$
- $\frac{1}{x^{2}}$
- $x^{2}$

field-2:
- $\frac{5 x^{4} - 9}{x^{2}}$
- $- \frac{9}{x^{2}}$
- $\frac{5 x^{4} + 9}{x^{2}}$
- $5 x^{2} - 9$
- $5 x^{4} - 9$

The first step is to write the equation in standard form,

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2y & =20 x^{2} \\ \frac{1}{x}\left(x\frac{\text{d}y}{\text{d}x}+2y\right) & =\frac{1}{x}\cdot 20 x^{2} \\ \frac{\text{d}y}{\text{d}x}+\frac{2}{x}y & =20 x\end{aligned}
$$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=20 x.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{2}{x}\,\text{d}x} \\  & =e^{2 \ln{\left(x \right)}} \\  & =x^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x^{2}$ yields

$$
\begin{aligned}x^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & =x^{2}\cdot 20 x \\ x^{2}\frac{\text{d}y}{\text{d}x}+2 xy & =20 x^{3} \\ \frac{\text{d}}{\text{d}x}(yx^{2}) & =20 x^{3}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx^{2})\,\text{d}x & =\int 20 x^{3}\,\text{d}x \\ yx^{2} & =5 x^{4}+C \\ y & =\frac{C + 5 x^{4}}{x^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(1)=-4$ as follows:

$$
\begin{aligned}y(1) & =\frac{(5 (1)^{4})+C}{((1)^{2})} \\ -4 & =\frac{5+C}{1} \\ C & =-9\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{5 x^{4} - 9}{x^{2}}.
$$

## Authored moderate_cancellation seed 0

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(5\right)y=8 x e^{- 5 x},\quad y(0)=-2
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{5 x}$
- $5 x$
- $e^{- 5 x}$
- $e^{10 x}$

field-2:
- $4 x^{2} - 2$
- $2 \left(2 x^{2} - 1\right) e^{- 5 x}$
- $4 x^{2} e^{- 5 x} - 2$
- $\left(4 x^{2} + 2\right) e^{- 5 x}$
- $- 2 e^{- 5 x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=5$ and $Q(x)=8 x e^{- 5 x}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int 5\,\text{d}x} \\  & =e^{5 x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{5 x}$ yields

$$
\begin{aligned}e^{5 x}\cdot (\frac{\text{d}y}{\text{d}x}+5y) & =e^{5 x}\cdot 8 x e^{- 5 x} \\ e^{5 x}\frac{\text{d}y}{\text{d}x}+5 e^{5 x}y & =8 x \\ \frac{\text{d}}{\text{d}x}(ye^{5 x}) & =8 x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{5 x})\,\text{d}x & =\int 8 x\,\text{d}x \\ ye^{5 x} & =4 x^{2}+C \\ y & =\left(C + 4 x^{2}\right) e^{- 5 x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =\frac{(4 (0)^{2})+C}{(e^{5 (0)})} \\ -2 & =\frac{0+C}{1} \\ C & =-2\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=2 \left(2 x^{2} - 1\right) e^{- 5 x}.
$$

## Authored moderate_cancellation seed 1

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(5\right)y=2 x e^{- 5 x},\quad y(0)=-4
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{10 x}$
- $e^{- 5 x}$
- $e^{5 x}$
- $5 x$

field-2:
- $\left(x^{2} - 4\right) e^{- 5 x}$
- $\left(x^{2} + 4\right) e^{- 5 x}$
- $- 4 e^{- 5 x}$
- $x^{2} e^{- 5 x} - 4$
- $x^{2} - 4$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=5$ and $Q(x)=2 x e^{- 5 x}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int 5\,\text{d}x} \\  & =e^{5 x}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{5 x}$ yields

$$
\begin{aligned}e^{5 x}\cdot (\frac{\text{d}y}{\text{d}x}+5y) & =e^{5 x}\cdot 2 x e^{- 5 x} \\ e^{5 x}\frac{\text{d}y}{\text{d}x}+5 e^{5 x}y & =2 x \\ \frac{\text{d}}{\text{d}x}(ye^{5 x}) & =2 x.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{5 x})\,\text{d}x & =\int 2 x\,\text{d}x \\ ye^{5 x} & =x^{2}+C \\ y & =\left(C + x^{2}\right) e^{- 5 x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-4$ as follows:

$$
\begin{aligned}y(0) & =\frac{((0)^{2})+C}{(e^{5 (0)})} \\ -4 & =\frac{0+C}{1} \\ C & =-4\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\left(x^{2} - 4\right) e^{- 5 x}.
$$

## Authored moderate_cosine seed 0

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(\frac{2}{x}\right)y=\frac{3 \cos{\left(x \right)}}{x^{2}},\quad x>0,\quad y(\pi)=-6
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x^{2}$
- $e^{x}$
- $\frac{1}{x^{2}}$
- $\frac{2}{x}$

field-2:
- $\frac{3 \sin{\left(x \right)} + 6 \pi^{2}}{x^{2}}$
- $\frac{3 \left(\sin{\left(x \right)} - 2 \pi^{2}\right)}{x^{2}}$
- $- 6 \pi^{2} + \frac{3 \sin{\left(x \right)}}{x^{2}}$
- $- \frac{6 \pi^{2}}{x^{2}}$
- $3 \sin{\left(x \right)} - 6 \pi^{2}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{3 \cos{\left(x \right)}}{x^{2}}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{2}{x}\,\text{d}x} \\  & =e^{2 \ln{\left(x \right)}} \\  & =x^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x^{2}$ yields

$$
\begin{aligned}x^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & =x^{2}\cdot \frac{3 \cos{\left(x \right)}}{x^{2}} \\ x^{2}\frac{\text{d}y}{\text{d}x}+2 xy & =3 \cos{\left(x \right)} \\ \frac{\text{d}}{\text{d}x}(yx^{2}) & =3 \cos{\left(x \right)}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx^{2})\,\text{d}x & =\int 3 \cos{\left(x \right)}\,\text{d}x \\ yx^{2} & =3 \sin{\left(x \right)}+C \\ y & =\frac{C + 3 \sin{\left(x \right)}}{x^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\pi)=-6$ as follows:

$$
\begin{aligned}y(\pi) & =\frac{(3 \sin{\left((\pi) \right)})+C}{((\pi)^{2})} \\ -6 & =\frac{0+C}{\pi^{2}} \\ C & =- 6 \pi^{2}\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{3 \left(\sin{\left(x \right)} - 2 \pi^{2}\right)}{x^{2}}.
$$

## Authored moderate_cosine seed 1

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(\frac{2}{x}\right)y=\frac{5 \cos{\left(x \right)}}{x^{2}},\quad x>0,\quad y(\pi)=-4
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{x}$
- $\frac{2}{x}$
- $\frac{1}{x^{2}}$
- $x^{2}$

field-2:
- $\frac{5 \sin{\left(x \right)} - 4 \pi^{2}}{x^{2}}$
- $- \frac{4 \pi^{2}}{x^{2}}$
- $\frac{5 \sin{\left(x \right)} + 4 \pi^{2}}{x^{2}}$
- $- 4 \pi^{2} + \frac{5 \sin{\left(x \right)}}{x^{2}}$
- $5 \sin{\left(x \right)} - 4 \pi^{2}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{5 \cos{\left(x \right)}}{x^{2}}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{2}{x}\,\text{d}x} \\  & =e^{2 \ln{\left(x \right)}} \\  & =x^{2}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x^{2}$ yields

$$
\begin{aligned}x^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & =x^{2}\cdot \frac{5 \cos{\left(x \right)}}{x^{2}} \\ x^{2}\frac{\text{d}y}{\text{d}x}+2 xy & =5 \cos{\left(x \right)} \\ \frac{\text{d}}{\text{d}x}(yx^{2}) & =5 \cos{\left(x \right)}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx^{2})\,\text{d}x & =\int 5 \cos{\left(x \right)}\,\text{d}x \\ yx^{2} & =5 \sin{\left(x \right)}+C \\ y & =\frac{C + 5 \sin{\left(x \right)}}{x^{2}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\pi)=-4$ as follows:

$$
\begin{aligned}y(\pi) & =\frac{(5 \sin{\left((\pi) \right)})+C}{((\pi)^{2})} \\ -4 & =\frac{0+C}{\pi^{2}} \\ C & =- 4 \pi^{2}\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=\frac{5 \sin{\left(x \right)} - 4 \pi^{2}}{x^{2}}.
$$

## Authored moderate_sine seed 0

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(\frac{1}{x}\right)y=\frac{3 \sin{\left(x \right)}}{x},\quad x>0,\quad y(\frac{\pi}{2})=-6
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $x$
- $e^{x}$
- $\frac{1}{x}$
- $\ln{\left(x \right)}$

field-2:
- $\frac{- 3 \cos{\left(x \right)} + 3 \pi}{x}$
- $- \frac{3 \cos{\left(x \right)} + 3 \pi}{x}$
- $- 3 \pi - \frac{3 \cos{\left(x \right)}}{x}$
- $- \frac{3 \pi}{x}$
- $- 3 \cos{\left(x \right)} - 3 \pi$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=\frac{3 \sin{\left(x \right)}}{x}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{1}{x}\,\text{d}x} \\  & =e^{\ln{\left(x \right)}} \\  & =x\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x$ yields

$$
\begin{aligned}x\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y) & =x\cdot \frac{3 \sin{\left(x \right)}}{x} \\ x\frac{\text{d}y}{\text{d}x}+1y & =3 \sin{\left(x \right)} \\ \frac{\text{d}}{\text{d}x}(yx) & =3 \sin{\left(x \right)}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx)\,\text{d}x & =\int 3 \sin{\left(x \right)}\,\text{d}x \\ yx & =- 3 \cos{\left(x \right)}+C \\ y & =\frac{C - 3 \cos{\left(x \right)}}{x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\frac{\pi}{2})=-6$ as follows:

$$
\begin{aligned}y(\frac{\pi}{2}) & =\frac{(- 3 \cos{\left((\frac{\pi}{2}) \right)})+C}{((\frac{\pi}{2}))} \\ -6 & =\frac{0+C}{\frac{\pi}{2}} \\ C & =- 3 \pi\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=- \frac{3 \cos{\left(x \right)} + 3 \pi}{x}.
$$

## Authored moderate_sine seed 1

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(\frac{1}{x}\right)y=\frac{5 \sin{\left(x \right)}}{x},\quad x>0,\quad y(\frac{\pi}{2})=-4
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{x}$
- $\ln{\left(x \right)}$
- $\frac{1}{x}$
- $x$

field-2:
- $- \frac{5 \cos{\left(x \right)} + 2 \pi}{x}$
- $- \frac{2 \pi}{x}$
- $\frac{- 5 \cos{\left(x \right)} + 2 \pi}{x}$
- $- 2 \pi - \frac{5 \cos{\left(x \right)}}{x}$
- $- 5 \cos{\left(x \right)} - 2 \pi$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=\frac{5 \sin{\left(x \right)}}{x}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{1}{x}\,\text{d}x} \\  & =e^{\ln{\left(x \right)}} \\  & =x\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=x$ yields

$$
\begin{aligned}x\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{x}y) & =x\cdot \frac{5 \sin{\left(x \right)}}{x} \\ x\frac{\text{d}y}{\text{d}x}+1y & =5 \sin{\left(x \right)} \\ \frac{\text{d}}{\text{d}x}(yx) & =5 \sin{\left(x \right)}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(yx)\,\text{d}x & =\int 5 \sin{\left(x \right)}\,\text{d}x \\ yx & =- 5 \cos{\left(x \right)}+C \\ y & =\frac{C - 5 \cos{\left(x \right)}}{x}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(\frac{\pi}{2})=-4$ as follows:

$$
\begin{aligned}y(\frac{\pi}{2}) & =\frac{(- 5 \cos{\left((\frac{\pi}{2}) \right)})+C}{((\frac{\pi}{2}))} \\ -4 & =\frac{0+C}{\frac{\pi}{2}} \\ C & =- 2 \pi\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=- \frac{5 \cos{\left(x \right)} + 2 \pi}{x}.
$$

## Authored hard_quadratic seed 0

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(\frac{x}{6}\right)y=\frac{2 x}{3},\quad y(0)=-2
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{\frac{x^{2}}{12}}$
- $\frac{x^{2}}{12}$
- $e^{- \frac{x^{2}}{12}}$
- $e^{\frac{x^{2}}{6}}$

field-2:
- $4 e^{\frac{x^{2}}{12}} - 6$
- $4 - 6 e^{- \frac{x^{2}}{12}}$
- $-2$
- $\left(4 e^{\frac{x^{2}}{12}} + 6\right) e^{- \frac{x^{2}}{12}}$
- $- 6 e^{- \frac{x^{2}}{12}}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{6}$ and $Q(x)=\frac{2 x}{3}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{x}{6}\,\text{d}x} \\  & =e^{\frac{x^{2}}{12}}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{\frac{x^{2}}{12}}$ yields

$$
\begin{aligned}e^{\frac{x^{2}}{12}}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y) & =e^{\frac{x^{2}}{12}}\cdot \frac{2 x}{3} \\ e^{\frac{x^{2}}{12}}\frac{\text{d}y}{\text{d}x}+\frac{x e^{\frac{x^{2}}{12}}}{6}y & =\frac{2 x e^{\frac{x^{2}}{12}}}{3} \\ \frac{\text{d}}{\text{d}x}(ye^{\frac{x^{2}}{12}}) & =\frac{2 x e^{\frac{x^{2}}{12}}}{3}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{x^{2}}{12}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{\frac{x^{2}}{12}})\,\text{d}x & =\int \frac{2 x e^{\frac{x^{2}}{12}}}{3}\,\text{d}x \\ ye^{\frac{x^{2}}{12}} & =\int 4e^u\,\text{d}u \\ ye^{\frac{x^{2}}{12}} & =4e^u+C \\ ye^{\frac{x^{2}}{12}} & =4 e^{\frac{x^{2}}{12}}+C \\ y & =\left(C + 4 e^{\frac{x^{2}}{12}}\right) e^{- \frac{x^{2}}{12}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =\frac{(4 e^{\frac{(0)^{2}}{12}})+C}{(e^{\frac{(0)^{2}}{12}})} \\ -2 & =\frac{4+C}{1} \\ C & =-6\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=4 - 6 e^{- \frac{x^{2}}{12}}.
$$

## Authored hard_quadratic seed 1

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(\frac{x}{6}\right)y=\frac{x}{6},\quad y(0)=-4
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{\frac{x^{2}}{6}}$
- $e^{- \frac{x^{2}}{12}}$
- $e^{\frac{x^{2}}{12}}$
- $\frac{x^{2}}{12}$

field-2:
- $1 - 5 e^{- \frac{x^{2}}{12}}$
- $\left(e^{\frac{x^{2}}{12}} + 5\right) e^{- \frac{x^{2}}{12}}$
- $- 5 e^{- \frac{x^{2}}{12}}$
- $-4$
- $e^{\frac{x^{2}}{12}} - 5$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x}{6}$ and $Q(x)=\frac{x}{6}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{x}{6}\,\text{d}x} \\  & =e^{\frac{x^{2}}{12}}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{\frac{x^{2}}{12}}$ yields

$$
\begin{aligned}e^{\frac{x^{2}}{12}}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x}{6}y) & =e^{\frac{x^{2}}{12}}\cdot \frac{x}{6} \\ e^{\frac{x^{2}}{12}}\frac{\text{d}y}{\text{d}x}+\frac{x e^{\frac{x^{2}}{12}}}{6}y & =\frac{x e^{\frac{x^{2}}{12}}}{6} \\ \frac{\text{d}}{\text{d}x}(ye^{\frac{x^{2}}{12}}) & =\frac{x e^{\frac{x^{2}}{12}}}{6}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{x^{2}}{12}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{\frac{x^{2}}{12}})\,\text{d}x & =\int \frac{x e^{\frac{x^{2}}{12}}}{6}\,\text{d}x \\ ye^{\frac{x^{2}}{12}} & =\int 1e^u\,\text{d}u \\ ye^{\frac{x^{2}}{12}} & =1e^u+C \\ ye^{\frac{x^{2}}{12}} & =e^{\frac{x^{2}}{12}}+C \\ y & =\left(C + e^{\frac{x^{2}}{12}}\right) e^{- \frac{x^{2}}{12}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-4$ as follows:

$$
\begin{aligned}y(0) & =\frac{(e^{\frac{(0)^{2}}{12}})+C}{(e^{\frac{(0)^{2}}{12}})} \\ -4 & =\frac{1+C}{1} \\ C & =-5\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=1 - 5 e^{- \frac{x^{2}}{12}}.
$$

## Authored hard_cubic seed 0

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(\frac{x^{2}}{4}\right)y=x^{2},\quad y(0)=-2
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{\frac{x^{3}}{12}}$
- $e^{\frac{x^{3}}{6}}$
- $e^{- \frac{x^{3}}{12}}$
- $\frac{x^{3}}{12}$

field-2:
- $4 e^{\frac{x^{3}}{12}} - 6$
- $4 - 6 e^{- \frac{x^{3}}{12}}$
- $- 6 e^{- \frac{x^{3}}{12}}$
- $\left(4 e^{\frac{x^{3}}{12}} + 6\right) e^{- \frac{x^{3}}{12}}$
- $-2$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=\frac{x^{2}}{4}$ and $Q(x)=x^{2}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int \frac{x^{2}}{4}\,\text{d}x} \\  & =e^{\frac{x^{3}}{12}}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{\frac{x^{3}}{12}}$ yields

$$
\begin{aligned}e^{\frac{x^{3}}{12}}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{x^{2}}{4}y) & =e^{\frac{x^{3}}{12}}\cdot x^{2} \\ e^{\frac{x^{3}}{12}}\frac{\text{d}y}{\text{d}x}+\frac{x^{2} e^{\frac{x^{3}}{12}}}{4}y & =x^{2} e^{\frac{x^{3}}{12}} \\ \frac{\text{d}}{\text{d}x}(ye^{\frac{x^{3}}{12}}) & =x^{2} e^{\frac{x^{3}}{12}}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{x^{3}}{12}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{\frac{x^{3}}{12}})\,\text{d}x & =\int x^{2} e^{\frac{x^{3}}{12}}\,\text{d}x \\ ye^{\frac{x^{3}}{12}} & =\int 4e^u\,\text{d}u \\ ye^{\frac{x^{3}}{12}} & =4e^u+C \\ ye^{\frac{x^{3}}{12}} & =4 e^{\frac{x^{3}}{12}}+C \\ y & =\left(C + 4 e^{\frac{x^{3}}{12}}\right) e^{- \frac{x^{3}}{12}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-2$ as follows:

$$
\begin{aligned}y(0) & =\frac{(4 e^{\frac{(0)^{3}}{12}})+C}{(e^{\frac{(0)^{3}}{12}})} \\ -2 & =\frac{4+C}{1} \\ C & =-6\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=4 - 6 e^{- \frac{x^{3}}{12}}.
$$

## Authored hard_cubic seed 1

Consider the following initial value problem.

$$
\frac{\text{d}y}{\text{d}x}+\left(x^{2}\right)y=3 x^{2},\quad y(0)=-4
$$

Select the correct options below.

An integrating factor for this equation is $I(x)=$ {{field-1}}.

The solution to the initial value problem is $y(x)=$ {{field-2}}.

field-1:
- $e^{\frac{2 x^{3}}{3}}$
- $\frac{x^{3}}{3}$
- $e^{- \frac{x^{3}}{3}}$
- $e^{\frac{x^{3}}{3}}$

field-2:
- $\left(3 e^{\frac{x^{3}}{3}} + 7\right) e^{- \frac{x^{3}}{3}}$
- $- 7 e^{- \frac{x^{3}}{3}}$
- $3 - 7 e^{- \frac{x^{3}}{3}}$
- $-4$
- $3 e^{\frac{x^{3}}{3}} - 7$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x),
$$

with $P(x)=x^{2}$ and $Q(x)=3 x^{2}.$

We compute an integrating factor using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,\text{d}x} \\  & =e^{\int x^{2}\,\text{d}x} \\  & =e^{\frac{x^{3}}{3}}\end{aligned}
$$

Multiplying both sides of the equation in standard form by $I(x)=e^{\frac{x^{3}}{3}}$ yields

$$
\begin{aligned}e^{\frac{x^{3}}{3}}\cdot (\frac{\text{d}y}{\text{d}x}+x^{2}y) & =e^{\frac{x^{3}}{3}}\cdot 3 x^{2} \\ e^{\frac{x^{3}}{3}}\frac{\text{d}y}{\text{d}x}+x^{2} e^{\frac{x^{3}}{3}}y & =3 x^{2} e^{\frac{x^{3}}{3}} \\ \frac{\text{d}}{\text{d}x}(ye^{\frac{x^{3}}{3}}) & =3 x^{2} e^{\frac{x^{3}}{3}}.\end{aligned}
$$

Now, we integrate with respect to $x,$ making use of the substitution $u=\frac{x^{3}}{3}:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(ye^{\frac{x^{3}}{3}})\,\text{d}x & =\int 3 x^{2} e^{\frac{x^{3}}{3}}\,\text{d}x \\ ye^{\frac{x^{3}}{3}} & =\int 3e^u\,\text{d}u \\ ye^{\frac{x^{3}}{3}} & =3e^u+C \\ ye^{\frac{x^{3}}{3}} & =3 e^{\frac{x^{3}}{3}}+C \\ y & =\left(C + 3 e^{\frac{x^{3}}{3}}\right) e^{- \frac{x^{3}}{3}}\end{aligned}
$$

This is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y(0)=-4$ as follows:

$$
\begin{aligned}y(0) & =\frac{(3 e^{\frac{(0)^{3}}{3}})+C}{(e^{\frac{(0)^{3}}{3}})} \\ -4 & =\frac{3+C}{1} \\ C & =-7\end{aligned}
$$

Therefore, the solution to the initial value problem is

$$
y=3 - 7 e^{- \frac{x^{3}}{3}}.
$$

