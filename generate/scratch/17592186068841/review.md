# Originals and generated variants

All original records remain in source.json and source-cases.json. Observed profile reproduces source values and teaching stages as evidence; normal variants apply the documented repairs.

## Original q-8303

Find the general solution to the differential equation ${y}^{′}-\sqrt{y}=2x\sqrt{y}$ for $y\ne 0.$

- $y={(\frac{{x}^{2}+x+C}{2})}^{2}$
- $y={x}^{2}+x+C$
- $y=({x}^{2}+x)^{2}$
- $y=({x}^{2}+x+C)^{2}$
- $y={(\frac{{x}^{2}+x}{2})}^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x}-\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =2x\sqrt{y}+\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =(2x+1)\sqrt{y} \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =(2x+1)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+1)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int (2x+1)\,\text{d}x \\ 2\sqrt{y} & ={x}^{2}+x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2\sqrt{y}={x}^{2}+x+C
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & ={(\frac{{x}^{2}+x+C}{2})}^{2}.\end{aligned}
$$

### original replay q-8303

Find the general solution to the differential equation ${y}^{′}-\sqrt{y}=2x\sqrt{y}$ for $y\ne 0.$

1. $y=\left(x^{2} + x\right)^{2}$
2. $y=C + x^{2} + x$
3. $y=\left(\frac{C}{2} + \frac{x^{2}}{2} + \frac{x}{2}\right)^{2}$
4. $y=\left(\frac{x^{2}}{2} + \frac{x}{2}\right)^{2}$
5. $y=\left(C + x^{2} + x\right)^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x}-\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =2x\sqrt{y}+\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =(2x+1)\sqrt{y} \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =(2x+1)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+1)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int (2x+1)\,\text{d}x \\ 2\sqrt{y} & ={x}^{2}+x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2\sqrt{y}={x}^{2}+x+C
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & ={(\frac{{x}^{2}+x+C}{2})}^{2}.\end{aligned}
$$

### generated observed-bank evidence q-8303 a=2

Find the general solution to the differential equation ${y}^{′}-2\sqrt{y}=2x\sqrt{y}$ for $y\ne 0.$

1. $y=\left(x^{2} + 2 x\right)^{2}$
2. $y=C + x^{2} + 2 x$
3. $y=\left(C + x^{2} + 2 x\right)^{2}$
4. $y=\left(\frac{x^{2}}{2} + x\right)^{2}$
5. $y=\left(\frac{C}{2} + \frac{x^{2}}{2} + x\right)^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-2\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x}-2\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =2x\sqrt{y}+2\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =(2x+2)\sqrt{y} \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =(2x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+2)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int (2x+2)\,\text{d}x \\ 2\sqrt{y} & ={x}^{2}+2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2\sqrt{y}={x}^{2}+2x+C
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & ={(\frac{{x}^{2}+2x+C}{2})}^{2}.\end{aligned}
$$

### generated normal variant q-8303 a=2

Find the general solution to the differential equation ${y}^{′}-2\sqrt{y}=2x\sqrt{y}$ for $y\ne 0.$

Use an interval where $x^{2} + 2 x+C>0.$

1. $y=\left(x^{2} + 2 x\right)^{2}$
2. $y=C + x^{2} + 2 x$
3. $y=\left(C + x^{2} + 2 x\right)^{2}$
4. $y=\left(\frac{x^{2}}{2} + x\right)^{2}$
5. $y=\left(\frac{C}{2} + \frac{x^{2}}{2} + x\right)^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-2\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x}-2\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =2x\sqrt{y}+2\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =(2x+2)\sqrt{y} \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =(2x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+2)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int (2x+2)\,\text{d}x \\ 2\sqrt{y} & ={x}^{2}+2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2\sqrt{y}={x}^{2}+2x+C
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & ={(\frac{{x}^{2}+2x+C}{2})}^{2}.\end{aligned}
$$

### generated observed-bank evidence q-8303 a=7

Find the general solution to the differential equation ${y}^{′}-7\sqrt{y}=2x\sqrt{y}$ for $y\ne 0.$

1. $y=\left(\frac{x^{2}}{2} + \frac{7 x}{2}\right)^{2}$
2. $y=\left(\frac{C}{2} + \frac{x^{2}}{2} + \frac{7 x}{2}\right)^{2}$
3. $y=\left(C + x^{2} + 7 x\right)^{2}$
4. $y=C + x^{2} + 7 x$
5. $y=\left(x^{2} + 7 x\right)^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-7\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x}-7\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =2x\sqrt{y}+7\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =(2x+7)\sqrt{y} \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =(2x+7)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+7)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int (2x+7)\,\text{d}x \\ 2\sqrt{y} & ={x}^{2}+7x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2\sqrt{y}={x}^{2}+7x+C
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & ={(\frac{{x}^{2}+7x+C}{2})}^{2}.\end{aligned}
$$

### generated normal variant q-8303 a=7

Find the general solution to the differential equation ${y}^{′}-7\sqrt{y}=2x\sqrt{y}$ for $y\ne 0.$

Use an interval where $x^{2} + 7 x+C>0.$

1. $y=\left(\frac{x^{2}}{2} + \frac{7 x}{2}\right)^{2}$
2. $y=\left(\frac{C}{2} + \frac{x^{2}}{2} + \frac{7 x}{2}\right)^{2}$
3. $y=\left(C + x^{2} + 7 x\right)^{2}$
4. $y=C + x^{2} + 7 x$
5. $y=\left(x^{2} + 7 x\right)^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-7\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x}-7\sqrt{y} & =2x\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =2x\sqrt{y}+7\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =(2x+7)\sqrt{y} \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =(2x+7)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+7)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int (2x+7)\,\text{d}x \\ 2\sqrt{y} & ={x}^{2}+7x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2\sqrt{y}={x}^{2}+7x+C
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & ={(\frac{{x}^{2}+7x+C}{2})}^{2}.\end{aligned}
$$

## Original q-8305

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}-(\operatorname{cos}⁡x)y=0$ for $y\ne 0.$

- $y=K{e}^{-\operatorname{cos}⁡x}$
- $y={e}^{-\operatorname{cos}⁡x}+K$
- $y={e}^{\operatorname{sin}⁡x}+K$
- $y=K{e}^{\operatorname{cos}⁡x}$
- $y=K{e}^{\operatorname{sin}⁡x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-(\operatorname{cos}⁡x)y & =0 \\ \frac{\text{d}y}{\text{d}x} & =(\operatorname{cos}⁡x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{cos}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{cos}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =\operatorname{sin}⁡x+C \\ |y| & ={e}^{\operatorname{sin}⁡x+C} \\ |y| & ={e}^{\operatorname{sin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sin}⁡x}.
$$

### original replay q-8305

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}-(\operatorname{cos}⁡x)y=0$ for $y\ne 0.$

1. $y=K + e^{\sin{\left(x \right)}}$
2. $y=K + e^{- \cos{\left(x \right)}}$
3. $y=K e^{- \cos{\left(x \right)}}$
4. $y=K e^{\sin{\left(x \right)}}$
5. $y=K e^{\cos{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-(\operatorname{cos}⁡x)y & =0 \\ \frac{\text{d}y}{\text{d}x} & =(\operatorname{cos}⁡x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{cos}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{cos}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =\operatorname{sin}⁡x+C \\ |y| & ={e}^{\operatorname{sin}⁡x+C} \\ |y| & ={e}^{\operatorname{sin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sin}⁡x}.
$$

### generated observed-bank evidence q-8305 a=2

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}-(2\operatorname{cos}⁡x)y=0$ for $y\ne 0.$

1. $y=K + e^{2 \sin{\left(x \right)}}$
2. $y=K + e^{- 2 \cos{\left(x \right)}}$
3. $y=K e^{2 \cos{\left(x \right)}}$
4. $y=K e^{2 \sin{\left(x \right)}}$
5. $y=K e^{- 2 \cos{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-(2\operatorname{cos}⁡x)y & =0 \\ \frac{\text{d}y}{\text{d}x} & =(2\operatorname{cos}⁡x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =2\operatorname{cos}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\operatorname{cos}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int 2\operatorname{cos}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\operatorname{sin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=2\operatorname{sin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =2\operatorname{sin}⁡x+C \\ |y| & ={e}^{2\operatorname{sin}⁡x+C} \\ |y| & ={e}^{2\operatorname{sin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{2\operatorname{sin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{2\operatorname{sin}⁡x}.
$$

### generated normal variant q-8305 a=2

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}-(2\operatorname{cos}⁡x)y=0$ for $y\ne 0.$

1. $y=K + e^{2 \sin{\left(x \right)}}$
2. $y=K + e^{- 2 \cos{\left(x \right)}}$
3. $y=K e^{2 \cos{\left(x \right)}}$
4. $y=K e^{2 \sin{\left(x \right)}}$
5. $y=K e^{- 2 \cos{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-(2\operatorname{cos}⁡x)y & =0 \\ \frac{\text{d}y}{\text{d}x} & =(2\operatorname{cos}⁡x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =2\operatorname{cos}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\operatorname{cos}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int 2\operatorname{cos}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\operatorname{sin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=2\operatorname{sin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =2\operatorname{sin}⁡x+C \\ |y| & ={e}^{2\operatorname{sin}⁡x+C} \\ |y| & ={e}^{2\operatorname{sin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{2\operatorname{sin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{2\operatorname{sin}⁡x}.
$$

### generated observed-bank evidence q-8305 a=7

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}-(7\operatorname{cos}⁡x)y=0$ for $y\ne 0.$

1. $y=K e^{7 \sin{\left(x \right)}}$
2. $y=K e^{- 7 \cos{\left(x \right)}}$
3. $y=K e^{7 \cos{\left(x \right)}}$
4. $y=K + e^{- 7 \cos{\left(x \right)}}$
5. $y=K + e^{7 \sin{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-(7\operatorname{cos}⁡x)y & =0 \\ \frac{\text{d}y}{\text{d}x} & =(7\operatorname{cos}⁡x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =7\operatorname{cos}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 7\operatorname{cos}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int 7\operatorname{cos}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =7\operatorname{sin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=7\operatorname{sin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =7\operatorname{sin}⁡x+C \\ |y| & ={e}^{7\operatorname{sin}⁡x+C} \\ |y| & ={e}^{7\operatorname{sin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{7\operatorname{sin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{7\operatorname{sin}⁡x}.
$$

### generated normal variant q-8305 a=7

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}-(7\operatorname{cos}⁡x)y=0$ for $y\ne 0.$

1. $y=K e^{7 \sin{\left(x \right)}}$
2. $y=K e^{- 7 \cos{\left(x \right)}}$
3. $y=K e^{7 \cos{\left(x \right)}}$
4. $y=K + e^{- 7 \cos{\left(x \right)}}$
5. $y=K + e^{7 \sin{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-(7\operatorname{cos}⁡x)y & =0 \\ \frac{\text{d}y}{\text{d}x} & =(7\operatorname{cos}⁡x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =7\operatorname{cos}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 7\operatorname{cos}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int 7\operatorname{cos}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =7\operatorname{sin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=7\operatorname{sin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =7\operatorname{sin}⁡x+C \\ |y| & ={e}^{7\operatorname{sin}⁡x+C} \\ |y| & ={e}^{7\operatorname{sin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{7\operatorname{sin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{7\operatorname{sin}⁡x}.
$$

## Original q-128191

Find the general solution to the differential equation ${y}^{′}=x{y}^{2}.$ Assume that $y\ne 0$ and $K$ is an arbitrary constant.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $y=-2($ 

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $+K)^{-1}$

- ${x}^{2}$

First, we separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =x{y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =x\end{aligned}
$$

Next, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int x\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int x\,\text{d}x \\ -\frac{1}{y} & =\frac{{x}^{2}}{2}+C\end{aligned}
$$

Finally, we solve for $y.$ This gives

$$
\begin{aligned}-\frac{1}{y} & =\frac{{x}^{2}}{2}+C \\ -\frac{1}{y} & =\frac{{x}^{2}+2C}{2} \\ \frac{1}{y} & =-\frac{{x}^{2}+2C}{2} \\ y & =-\frac{2}{{x}^{2}+2C} \\ y & =-\frac{2}{{x}^{2}+K} \\ y & =-2{({x}^{2}+K)}^{-1},\end{aligned}
$$

where $K=2C$ is an arbitrary constant.

### original replay q-128191

Find the general solution to the differential equation ${y}^{′}=x{y}^{2}.$ Assume that $y\ne 0$ and $K$ is an arbitrary constant.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $y=-2($ 

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $+K)^{-1}$

1. $x^{2}$

First, we separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =x{y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =x\end{aligned}
$$

Next, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int x\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int x\,\text{d}x \\ -\frac{1}{y} & =\frac{{x}^{2}}{2}+C\end{aligned}
$$

Finally, we solve for $y.$ This gives

$$
\begin{aligned}-\frac{1}{y} & =\frac{{x}^{2}}{2}+C \\ -\frac{1}{y} & =\frac{{x}^{2}+2C}{2} \\ \frac{1}{y} & =-\frac{{x}^{2}+2C}{2} \\ y & =-\frac{2}{{x}^{2}+2C} \\ y & =-\frac{2}{{x}^{2}+K} \\ y & =-2{({x}^{2}+K)}^{-1},\end{aligned}
$$

where $K=2C$ is an arbitrary constant.

### generated observed-bank evidence q-128191 a=2

Find the general solution to the differential equation ${y}^{′}={x}^{2}{y}^{2}.$ Assume that $y\ne 0$ and $K$ is an arbitrary constant.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $y=-3($ 

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $+K)^{-1}$

1. $x^{3}$

First, we separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={x}^{2}{y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & ={x}^{2}\end{aligned}
$$

Next, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ -\frac{1}{y} & =\frac{{x}^{3}}{3}+C\end{aligned}
$$

Finally, we solve for $y.$ This gives

$$
\begin{aligned}-\frac{1}{y} & =\frac{{x}^{3}}{3}+C \\ -\frac{1}{y} & =\frac{{x}^{3}+3C}{3} \\ \frac{1}{y} & =-\frac{{x}^{3}+3C}{3} \\ y & =-\frac{3}{{x}^{3}+3C} \\ y & =-\frac{3}{{x}^{3}+K} \\ y & =-3{({x}^{3}+K)}^{-1},\end{aligned}
$$

where $K=3C$ is an arbitrary constant.

### generated normal variant q-128191 a=2

Find the general solution to the differential equation ${y}^{′}={x}^{2}{y}^{2}.$ Assume that $y\ne 0$ and $K$ is an arbitrary constant.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $y=-3($ 

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $+K)^{-1}$

Give the nonconstant polynomial term; put the integration constant in $K.$

1. $x^{3}$

First, we separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={x}^{2}{y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & ={x}^{2}\end{aligned}
$$

Next, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ -\frac{1}{y} & =\frac{{x}^{3}}{3}+C\end{aligned}
$$

Finally, we solve for $y.$ This gives

$$
\begin{aligned}-\frac{1}{y} & =\frac{{x}^{3}}{3}+C \\ -\frac{1}{y} & =\frac{{x}^{3}+3C}{3} \\ \frac{1}{y} & =-\frac{{x}^{3}+3C}{3} \\ y & =-\frac{3}{{x}^{3}+3C} \\ y & =-\frac{3}{{x}^{3}+K} \\ y & =-3{({x}^{3}+K)}^{-1},\end{aligned}
$$

where $K=3C$ is an arbitrary constant.

### generated observed-bank evidence q-128191 a=4

Find the general solution to the differential equation ${y}^{′}={x}^{4}{y}^{2}.$ Assume that $y\ne 0$ and $K$ is an arbitrary constant.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $y=-5($ 

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $+K)^{-1}$

1. $x^{5}$

First, we separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={x}^{4}{y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & ={x}^{4}\end{aligned}
$$

Next, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{4}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int {x}^{4}\,\text{d}x \\ -\frac{1}{y} & =\frac{{x}^{5}}{5}+C\end{aligned}
$$

Finally, we solve for $y.$ This gives

$$
\begin{aligned}-\frac{1}{y} & =\frac{{x}^{5}}{5}+C \\ -\frac{1}{y} & =\frac{{x}^{5}+5C}{5} \\ \frac{1}{y} & =-\frac{{x}^{5}+5C}{5} \\ y & =-\frac{5}{{x}^{5}+5C} \\ y & =-\frac{5}{{x}^{5}+K} \\ y & =-5{({x}^{5}+K)}^{-1},\end{aligned}
$$

where $K=5C$ is an arbitrary constant.

### generated normal variant q-128191 a=4

Find the general solution to the differential equation ${y}^{′}={x}^{4}{y}^{2}.$ Assume that $y\ne 0$ and $K$ is an arbitrary constant.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $y=-5($ 

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $+K)^{-1}$

Give the nonconstant polynomial term; put the integration constant in $K.$

1. $x^{5}$

First, we separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={x}^{4}{y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & ={x}^{4}\end{aligned}
$$

Next, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{4}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int {x}^{4}\,\text{d}x \\ -\frac{1}{y} & =\frac{{x}^{5}}{5}+C\end{aligned}
$$

Finally, we solve for $y.$ This gives

$$
\begin{aligned}-\frac{1}{y} & =\frac{{x}^{5}}{5}+C \\ -\frac{1}{y} & =\frac{{x}^{5}+5C}{5} \\ \frac{1}{y} & =-\frac{{x}^{5}+5C}{5} \\ y & =-\frac{5}{{x}^{5}+5C} \\ y & =-\frac{5}{{x}^{5}+K} \\ y & =-5{({x}^{5}+K)}^{-1},\end{aligned}
$$

where $K=5C$ is an arbitrary constant.

## Original q-14247

Find the general solution to the differential equation ${y}^{′}=y+3y{x}^{2}$ for $y\ne 0.$

- $y=K{e}^{\sqrt{{x}^{2}+2}}$
- $y=K{e}^{{x}^{2}+2x}$
- $y=K{e}^{\sqrt{{x}^{3}+x}}$
- $y=K{e}^{{x}^{3}+x}$
- $y=K{e}^{3{x}^{2}+x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(1+3{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =1+3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (1+3{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (1+3{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & =x+{x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+x+C \\ |y| & ={e}^{{x}^{3}+x+C} \\ |y| & ={e}^{{x}^{3}+x}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+x}\end{aligned}
$$

where $K={e}^{C}.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+x}.
$$

### original replay q-14247

Find the general solution to the differential equation ${y}^{′}=y+3y{x}^{2}$ for $y\ne 0.$

1. $y=K e^{\sqrt{x^{3} + x}}$
2. $y=K e^{x^{2} + 2 x}$
3. $y=K e^{\sqrt{x^{2} + 2}}$
4. $y=K e^{3 x^{2} + x}$
5. $y=K e^{x^{3} + x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(1+3{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =1+3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (1+3{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (1+3{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & =x+{x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+x+C \\ |y| & ={e}^{{x}^{3}+x+C} \\ |y| & ={e}^{{x}^{3}+x}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+x}\end{aligned}
$$

where $K={e}^{C}.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+x}.
$$

### generated observed-bank evidence q-14247 a=2

Find the general solution to the differential equation ${y}^{′}=2y+3y{x}^{2}$ for $y\ne 0.$

1. $y=K e^{\sqrt{x^{3} + 2 x}}$
2. $y=K e^{x^{2} + 4 x}$
3. $y=K e^{x^{3} + 2 x}$
4. $y=K e^{3 x^{2} + 2 x}$
5. $y=K e^{\sqrt{x^{2} + 4}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =2y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =2y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(2+3{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =2+3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2+3{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (2+3{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & =2x+{x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+2x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+2x+C \\ |y| & ={e}^{{x}^{3}+2x+C} \\ |y| & ={e}^{{x}^{3}+2x}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+2x}\end{aligned}
$$

where $K={e}^{C}.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+2x}.
$$

### generated authored-bank variant q-14247 a=2

Find the general solution to the differential equation ${y}^{′}=2y+3y{x}^{2}$ for $y\ne 0.$

1. $y=K + e^{x^{3} + 2 x}$
2. $y=K e^{- x^{3} - 2 x}$
3. $y=K e^{3 x^{2} + 2}$
4. $y=K e^{x^{3}}$
5. $y=K e^{x^{3} + 2 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =2y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =2y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(2+3{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =2+3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2+3{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (2+3{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & =2x+{x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+2x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+2x+C \\ |y| & ={e}^{{x}^{3}+2x+C} \\ |y| & ={e}^{{x}^{3}+2x}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+2x}\end{aligned}
$$

where $K={e}^{C}.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+2x}.
$$

### generated observed-bank evidence q-14247 a=7

Find the general solution to the differential equation ${y}^{′}=7y+3y{x}^{2}$ for $y\ne 0.$

1. $y=K e^{3 x^{2} + 7 x}$
2. $y=K e^{\sqrt{x^{2} + 14}}$
3. $y=K e^{x^{3} + 7 x}$
4. $y=K e^{x^{2} + 14 x}$
5. $y=K e^{\sqrt{x^{3} + 7 x}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =7y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =7y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(7+3{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =7+3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (7+3{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (7+3{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & =7x+{x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+7x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+7x+C \\ |y| & ={e}^{{x}^{3}+7x+C} \\ |y| & ={e}^{{x}^{3}+7x}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+7x}\end{aligned}
$$

where $K={e}^{C}.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+7x}.
$$

### generated authored-bank variant q-14247 a=7

Find the general solution to the differential equation ${y}^{′}=7y+3y{x}^{2}$ for $y\ne 0.$

1. $y=K e^{x^{3}}$
2. $y=K e^{x^{3} + 7 x}$
3. $y=K e^{3 x^{2} + 7}$
4. $y=K e^{- x^{3} - 7 x}$
5. $y=K + e^{x^{3} + 7 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =7y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =7y+3y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(7+3{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =7+3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (7+3{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (7+3{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & =7x+{x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+7x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+7x+C \\ |y| & ={e}^{{x}^{3}+7x+C} \\ |y| & ={e}^{{x}^{3}+7x}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+7x}\end{aligned}
$$

where $K={e}^{C}.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+7x}.
$$

## Original q-14253

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+2{y}^{2}x$ for $y\ne 0.$

- $y=-\frac{1}{2x+C}$
- $y=-\frac{1}{{x}^{2}+x}+C$
- $y=\frac{1}{2{x}^{2}+x}+C$
- $y=\frac{1}{{x}^{3}+C}$
- $y=-\frac{1}{{x}^{2}+x+C}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={y}^{2}+2{y}^{2}x \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(1+2x) \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =1+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (1+2x)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (1+2x)\,\text{d}x \\ -\frac{1}{y} & =x+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}={x}^{2}+x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=-\frac{1}{{x}^{2}+x+C}.
$$

### original replay q-14253

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+2{y}^{2}x$ for $y\ne 0.$

1. $y=C + \frac{1}{2 x^{2} + x}$
2. $y=C - \frac{1}{x^{2} + x}$
3. $y=- \frac{1}{C + 2 x}$
4. $y=- \frac{1}{C + x^{2} + x}$
5. $y=\frac{1}{C + x^{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={y}^{2}+2{y}^{2}x \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(1+2x) \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =1+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (1+2x)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (1+2x)\,\text{d}x \\ -\frac{1}{y} & =x+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}={x}^{2}+x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=-\frac{1}{{x}^{2}+x+C}.
$$

### generated observed-bank evidence q-14253 a=2

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=2{y}^{2}+2{y}^{2}x$ for $y\ne 0.$

1. $y=C + \frac{1}{2 x^{2} + 2 x}$
2. $y=C - \frac{1}{x^{2} + 2 x}$
3. $y=\frac{1}{C + x^{3}}$
4. $y=- \frac{1}{C + x^{2} + 2 x}$
5. $y=- \frac{1}{C + 4 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2{y}^{2}+2{y}^{2}x \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(2+2x) \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =2+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2+2x)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (2+2x)\,\text{d}x \\ -\frac{1}{y} & =2x+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}={x}^{2}+2x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=-\frac{1}{{x}^{2}+2x+C}.
$$

### generated authored-bank variant q-14253 a=2

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=2{y}^{2}+2{y}^{2}x$ for $y\ne 0.$

1. $y=- C - x^{2} - 2 x$
2. $y=\frac{1}{C + x^{2} + 2 x}$
3. $y=C - \frac{1}{x^{2} + 2 x}$
4. $y=- \frac{1}{C + 2 x + 2}$
5. $y=- \frac{1}{C + x^{2} + 2 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2{y}^{2}+2{y}^{2}x \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(2+2x) \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =2+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2+2x)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (2+2x)\,\text{d}x \\ -\frac{1}{y} & =2x+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}={x}^{2}+2x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=-\frac{1}{{x}^{2}+2x+C}.
$$

### generated observed-bank evidence q-14253 a=7

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=7{y}^{2}+2{y}^{2}x$ for $y\ne 0.$

1. $y=- \frac{1}{C + x^{2} + 7 x}$
2. $y=- \frac{1}{C + 14 x}$
3. $y=\frac{1}{C + x^{3}}$
4. $y=C - \frac{1}{x^{2} + 7 x}$
5. $y=C + \frac{1}{2 x^{2} + 7 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =7{y}^{2}+2{y}^{2}x \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(7+2x) \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =7+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (7+2x)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (7+2x)\,\text{d}x \\ -\frac{1}{y} & =7x+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}={x}^{2}+7x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=-\frac{1}{{x}^{2}+7x+C}.
$$

### generated authored-bank variant q-14253 a=7

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=7{y}^{2}+2{y}^{2}x$ for $y\ne 0.$

1. $y=- \frac{1}{C + 2 x + 7}$
2. $y=- \frac{1}{C + x^{2} + 7 x}$
3. $y=C - \frac{1}{x^{2} + 7 x}$
4. $y=\frac{1}{C + x^{2} + 7 x}$
5. $y=- C - x^{2} - 7 x$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =7{y}^{2}+2{y}^{2}x \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(7+2x) \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =7+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (7+2x)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (7+2x)\,\text{d}x \\ -\frac{1}{y} & =7x+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}={x}^{2}+7x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=-\frac{1}{{x}^{2}+7x+C}.
$$

## Original q-158009

Find the general solution to the differential equation ${x}^{2}\,{y}^{′}-y=3$ for $y\ne -3.$

- $y=K{e}^{-3/x}$
- $y=K{e}^{-x}-3$
- $y=K{e}^{1/x}+3$
- $y=K{e}^{x}+3$
- $y=K{e}^{-1/x}-3$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{x}^{2}\,{y}^{′}-y & =3 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x}-y & =3 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x} & =y+3 \\ \frac{1}{y+3}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y+3}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y+3}\,\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y+3| & =-\frac{1}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y+3|=-\frac{1}{x}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y+3| & =-\frac{1}{x}+C \\ |y+3| & ={e}^{-1/x+C} \\ |y+3| & ={e}^{-1/x}\cdot {e}^{C} \\ |y+3| & =K{e}^{-1/x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}|y+3| & =K{e}^{-1/x} \\ y+3 & =K{e}^{-1/x} \\ y & =K{e}^{-1/x}-3.\end{aligned}
$$

### original replay q-158009

Find the general solution to the differential equation ${x}^{2}\,{y}^{′}-y=3$ for $y\ne -3.$

1. $y=K e^{\frac{1}{x}} + 3$
2. $y=K e^{- x} - 3$
3. $y=K e^{- \frac{3}{x}}$
4. $y=K e^{- \frac{1}{x}} - 3$
5. $y=K e^{x} + 3$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{x}^{2}\,{y}^{′}-y & =3 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x}-y & =3 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x} & =y+3 \\ \frac{1}{y+3}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y+3}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y+3}\,\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y+3| & =-\frac{1}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y+3|=-\frac{1}{x}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y+3| & =-\frac{1}{x}+C \\ |y+3| & ={e}^{-1/x+C} \\ |y+3| & ={e}^{-1/x}\cdot {e}^{C} \\ |y+3| & =K{e}^{-1/x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}|y+3| & =K{e}^{-1/x} \\ y+3 & =K{e}^{-1/x} \\ y & =K{e}^{-1/x}-3.\end{aligned}
$$

### generated observed-bank evidence q-158009 a=2

Find the general solution to the differential equation ${x}^{2}\,{y}^{′}-y=2$ for $y\ne -2.$

1. $y=K e^{\frac{1}{x}} + 2$
2. $y=K e^{- x} - 2$
3. $y=K e^{x} + 2$
4. $y=K e^{- \frac{1}{x}} - 2$
5. $y=K e^{- \frac{2}{x}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{x}^{2}\,{y}^{′}-y & =2 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x}-y & =2 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x} & =y+2 \\ \frac{1}{y+2}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y+2}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y+2}\,\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y+2| & =-\frac{1}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y+2|=-\frac{1}{x}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y+2| & =-\frac{1}{x}+C \\ |y+2| & ={e}^{-1/x+C} \\ |y+2| & ={e}^{-1/x}\cdot {e}^{C} \\ |y+2| & =K{e}^{-1/x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}|y+2| & =K{e}^{-1/x} \\ y+2 & =K{e}^{-1/x} \\ y & =K{e}^{-1/x}-2.\end{aligned}
$$

### generated authored-bank variant q-158009 a=2

Find the general solution to the differential equation ${x}^{2}\,{y}^{′}-y=2$ for $y\ne -2.$

Assume $x\ne0.$

1. $y=K - 2 + e^{- \frac{1}{x}}$
2. $y=K e^{\frac{1}{x}} - 2$
3. $y=K e^{- \frac{1}{x}} + 2$
4. $y=K e^{\frac{1}{x^{2}}} - 2$
5. $y=K e^{- \frac{1}{x}} - 2$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{x}^{2}\,{y}^{′}-y & =2 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x}-y & =2 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x} & =y+2 \\ \frac{1}{y+2}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y+2}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y+2}\,\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y+2| & =-\frac{1}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y+2|=-\frac{1}{x}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y+2| & =-\frac{1}{x}+C \\ |y+2| & ={e}^{-1/x+C} \\ |y+2| & ={e}^{-1/x}\cdot {e}^{C} \\ |y+2| & =K{e}^{-1/x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}y+2 & =K{e}^{-1/x} \\ y & =K{e}^{-1/x}-2.\end{aligned}
$$

### generated observed-bank evidence q-158009 a=7

Find the general solution to the differential equation ${x}^{2}\,{y}^{′}-y=7$ for $y\ne -7.$

1. $y=K e^{- \frac{1}{x}} - 7$
2. $y=K e^{- \frac{7}{x}}$
3. $y=K e^{x} + 7$
4. $y=K e^{- x} - 7$
5. $y=K e^{\frac{1}{x}} + 7$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{x}^{2}\,{y}^{′}-y & =7 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x}-y & =7 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x} & =y+7 \\ \frac{1}{y+7}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y+7}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y+7}\,\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y+7| & =-\frac{1}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y+7|=-\frac{1}{x}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y+7| & =-\frac{1}{x}+C \\ |y+7| & ={e}^{-1/x+C} \\ |y+7| & ={e}^{-1/x}\cdot {e}^{C} \\ |y+7| & =K{e}^{-1/x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}|y+7| & =K{e}^{-1/x} \\ y+7 & =K{e}^{-1/x} \\ y & =K{e}^{-1/x}-7.\end{aligned}
$$

### generated authored-bank variant q-158009 a=7

Find the general solution to the differential equation ${x}^{2}\,{y}^{′}-y=7$ for $y\ne -7.$

Assume $x\ne0.$

1. $y=K e^{\frac{1}{x^{2}}} - 7$
2. $y=K e^{- \frac{1}{x}} - 7$
3. $y=K e^{- \frac{1}{x}} + 7$
4. $y=K e^{\frac{1}{x}} - 7$
5. $y=K - 7 + e^{- \frac{1}{x}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{x}^{2}\,{y}^{′}-y & =7 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x}-y & =7 \\ {x}^{2}\,\frac{\text{d}y}{\text{d}x} & =y+7 \\ \frac{1}{y+7}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y+7}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y+7}\,\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y+7| & =-\frac{1}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y+7|=-\frac{1}{x}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y+7| & =-\frac{1}{x}+C \\ |y+7| & ={e}^{-1/x+C} \\ |y+7| & ={e}^{-1/x}\cdot {e}^{C} \\ |y+7| & =K{e}^{-1/x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}y+7 & =K{e}^{-1/x} \\ y & =K{e}^{-1/x}-7.\end{aligned}
$$

## Original q-158010

Find the general solution to the differential equation $\sqrt{1-{x}^{2}}\,{y}^{′}-y=0$ for $y\ne 0$ and $|x|<1.$

- $y=K{e}^{1/\sqrt{1-{x}^{2}}}$
- $y=K{e}^{\operatorname{arcsin}⁡x}$
- $y=K{e}^{\operatorname{arctan}⁡x}$
- $y=K{e}^{\operatorname{sin}⁡x}$
- $y=K{e}^{\sqrt{1-{x}^{2}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{1-{x}^{2}}\,{y}^{′}-y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x}-y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x} & =y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{1-{x}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{1}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{arcsin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{arcsin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =\operatorname{arcsin}⁡x+C \\ |y| & ={e}^{\operatorname{arcsin}⁡x+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{arcsin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}y & =K{e}^{\operatorname{arcsin}⁡x}.\end{aligned}
$$

### original replay q-158010

Find the general solution to the differential equation $\sqrt{1-{x}^{2}}\,{y}^{′}-y=0$ for $y\ne 0$ and $|x|<1.$

1. $y=K e^{\arctan{\left(x \right)}}$
2. $y=K e^{\arcsin{\left(x \right)}}$
3. $y=K e^{\frac{1}{\sqrt{1 - x^{2}}}}$
4. $y=K e^{\sqrt{1 - x^{2}}}$
5. $y=K e^{\sin{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{1-{x}^{2}}\,{y}^{′}-y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x}-y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x} & =y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{1-{x}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{1}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{arcsin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{arcsin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =\operatorname{arcsin}⁡x+C \\ |y| & ={e}^{\operatorname{arcsin}⁡x+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{arcsin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}y & =K{e}^{\operatorname{arcsin}⁡x}.\end{aligned}
$$

### generated observed-bank evidence q-158010 a=2

Find the general solution to the differential equation $\sqrt{1-{x}^{2}}\,{y}^{′}-2y=0$ for $y\ne 0$ and $|x|<1.$

1. $y=K e^{2 \arctan{\left(x \right)}}$
2. $y=K e^{2 \arcsin{\left(x \right)}}$
3. $y=K e^{2 \sin{\left(x \right)}}$
4. $y=K e^{2 \sqrt{1 - x^{2}}}$
5. $y=K e^{\frac{2}{\sqrt{1 - x^{2}}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{1-{x}^{2}}\,{y}^{′}-2y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x}-2y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x} & =2y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{2}{\sqrt{1-{x}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{2}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{2}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\operatorname{arcsin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=2\operatorname{arcsin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =2\operatorname{arcsin}⁡x+C \\ |y| & ={e}^{2\operatorname{arcsin}⁡x+C} \\ |y| & ={e}^{2\operatorname{arcsin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{2\operatorname{arcsin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}y & =K{e}^{2\operatorname{arcsin}⁡x}.\end{aligned}
$$

### generated normal variant q-158010 a=2

Find the general solution to the differential equation $\sqrt{1-{x}^{2}}\,{y}^{′}-2y=0$ for $y\ne 0$ and $|x|<1.$

1. $y=K e^{2 \arctan{\left(x \right)}}$
2. $y=K e^{2 \arcsin{\left(x \right)}}$
3. $y=K e^{2 \sin{\left(x \right)}}$
4. $y=K e^{2 \sqrt{1 - x^{2}}}$
5. $y=K e^{\frac{2}{\sqrt{1 - x^{2}}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{1-{x}^{2}}\,{y}^{′}-2y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x}-2y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x} & =2y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{2}{\sqrt{1-{x}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{2}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{2}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\operatorname{arcsin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=2\operatorname{arcsin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =2\operatorname{arcsin}⁡x+C \\ |y| & ={e}^{2\operatorname{arcsin}⁡x+C} \\ |y| & ={e}^{2\operatorname{arcsin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{2\operatorname{arcsin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}y & =K{e}^{2\operatorname{arcsin}⁡x}.\end{aligned}
$$

### generated observed-bank evidence q-158010 a=7

Find the general solution to the differential equation $\sqrt{1-{x}^{2}}\,{y}^{′}-7y=0$ for $y\ne 0$ and $|x|<1.$

1. $y=K e^{7 \sqrt{1 - x^{2}}}$
2. $y=K e^{\frac{7}{\sqrt{1 - x^{2}}}}$
3. $y=K e^{7 \sin{\left(x \right)}}$
4. $y=K e^{7 \arcsin{\left(x \right)}}$
5. $y=K e^{7 \arctan{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{1-{x}^{2}}\,{y}^{′}-7y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x}-7y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x} & =7y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{7}{\sqrt{1-{x}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{7}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{7}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =7\operatorname{arcsin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=7\operatorname{arcsin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =7\operatorname{arcsin}⁡x+C \\ |y| & ={e}^{7\operatorname{arcsin}⁡x+C} \\ |y| & ={e}^{7\operatorname{arcsin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{7\operatorname{arcsin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}y & =K{e}^{7\operatorname{arcsin}⁡x}.\end{aligned}
$$

### generated normal variant q-158010 a=7

Find the general solution to the differential equation $\sqrt{1-{x}^{2}}\,{y}^{′}-7y=0$ for $y\ne 0$ and $|x|<1.$

1. $y=K e^{7 \sqrt{1 - x^{2}}}$
2. $y=K e^{\frac{7}{\sqrt{1 - x^{2}}}}$
3. $y=K e^{7 \sin{\left(x \right)}}$
4. $y=K e^{7 \arcsin{\left(x \right)}}$
5. $y=K e^{7 \arctan{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{1-{x}^{2}}\,{y}^{′}-7y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x}-7y & =0 \\ \sqrt{1-{x}^{2}}\,\frac{\text{d}y}{\text{d}x} & =7y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\frac{7}{\sqrt{1-{x}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{7}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{7}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =7\operatorname{arcsin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=7\operatorname{arcsin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =7\operatorname{arcsin}⁡x+C \\ |y| & ={e}^{7\operatorname{arcsin}⁡x+C} \\ |y| & ={e}^{7\operatorname{arcsin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{7\operatorname{arcsin}⁡x}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
\begin{aligned}y & =K{e}^{7\operatorname{arcsin}⁡x}.\end{aligned}
$$

## Original q-3854

Find the general solution to the differential equation ${y}^{′}=2yx+y{x}^{2}$ for $y\ne 0.$

- $y={e}^{{x}^{2}}+{e}^{{x}^{3}}+K$
- $y=K{e}^{{x}^{2}+{x}^{3}/3}$
- $y={x}^{2}+\frac{{x}^{3}}{3}+K$
- $y=\operatorname{ln}⁡{x}^{2}+\operatorname{ln}⁡\frac{{x}^{3}}{3}+K$
- $y=\operatorname{ln}⁡{x}^{2}+\operatorname{ln}⁡{x}^{3}+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(2x+{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =2x+{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (2x+{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{2}+\frac{{x}^{3}}{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3+C} \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{2}+{x}^{3}/3}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{2}+{x}^{3}/3}.
$$

### original replay q-3854

Find the general solution to the differential equation ${y}^{′}=2yx+y{x}^{2}$ for $y\ne 0.$

1. $y=K + \frac{x^{3}}{3} + x^{2}$
2. $y=K e^{\frac{x^{3}}{3} + x^{2}}$
3. $y=K + e^{x^{2}} + e^{x^{3}}$
4. $y=K + \ln{\left(x^{2} \right)} + \ln{\left(x^{3} \right)}$
5. $y=K + \ln{\left(x^{2} \right)} + \ln{\left(\frac{x^{3}}{3} \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(2x+{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =2x+{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (2x+{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{2}+\frac{{x}^{3}}{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3+C} \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{2}+{x}^{3}/3}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{2}+{x}^{3}/3}.
$$

### generated observed-bank evidence q-3854 a=2

Find the general solution to the differential equation ${y}^{′}=2yx+y{x}^{2}$ for $y\ne 0.$

1. $y=K + \frac{x^{3}}{3} + x^{2}$
2. $y=K e^{\frac{x^{3}}{3} + x^{2}}$
3. $y=K + \ln{\left(x^{2} \right)} + \ln{\left(\frac{x^{3}}{3} \right)}$
4. $y=K + \ln{\left(x^{2} \right)} + \ln{\left(x^{3} \right)}$
5. $y=K + e^{x^{2}} + e^{x^{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(2x+{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =2x+{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (2x+{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{2}+\frac{{x}^{3}}{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3+C} \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{2}+{x}^{3}/3}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{2}+{x}^{3}/3}.
$$

### generated normal variant q-3854 a=2

Find the general solution to the differential equation ${y}^{′}=2yx+y{x}^{2}$ for $y\ne 0.$

1. $y=K + \frac{x^{3}}{3} + x^{2}$
2. $y=K e^{\frac{x^{3}}{3} + x^{2}}$
3. $y=K + \ln{\left(x^{2} \right)} + \ln{\left(\frac{x^{3}}{3} \right)}$
4. $y=K + 2 \ln{\left(x^{2} \right)}$
5. $y=K + e^{x^{2}} + e^{x^{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(2x+{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =2x+{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (2x+{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{2}+\frac{{x}^{3}}{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3+C} \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{2}+{x}^{3}/3}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{2}+{x}^{3}/3}.
$$

### generated observed-bank evidence q-3854 a=7

Find the general solution to the differential equation ${y}^{′}=7yx+y{x}^{2}$ for $y\ne 0.$

1. $y=K + \ln{\left(\frac{7 x^{2}}{2} \right)} + \ln{\left(x^{3} \right)}$
2. $y=K + e^{\frac{7 x^{2}}{2}} + e^{x^{3}}$
3. $y=K + \ln{\left(\frac{7 x^{2}}{2} \right)} + \ln{\left(\frac{x^{3}}{3} \right)}$
4. $y=K e^{\frac{x^{3}}{3} + \frac{7 x^{2}}{2}}$
5. $y=K + \frac{x^{3}}{3} + \frac{7 x^{2}}{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =7yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =7yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(7x+{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =7x+{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (7x+{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (7x+{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{7{x}^{2}}{2}+\frac{{x}^{3}}{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\frac{7{x}^{2}}{2}+\frac{{x}^{3}}{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =\frac{7{x}^{2}}{2}+\frac{{x}^{3}}{3}+C \\ |y| & ={e}^{\frac{7{x}^{2}}{2}+{x}^{3}/3+C} \\ |y| & ={e}^{\frac{7{x}^{2}}{2}+{x}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{\frac{7{x}^{2}}{2}+{x}^{3}/3}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\frac{7{x}^{2}}{2}+{x}^{3}/3}.
$$

### generated normal variant q-3854 a=7

Find the general solution to the differential equation ${y}^{′}=7yx+y{x}^{2}$ for $y\ne 0.$

1. $y=K + \ln{\left(x^{2} \right)} + \ln{\left(\frac{7 x^{2}}{2} \right)}$
2. $y=K + e^{\frac{7 x^{2}}{2}} + e^{x^{3}}$
3. $y=K + \ln{\left(\frac{7 x^{2}}{2} \right)} + \ln{\left(\frac{x^{3}}{3} \right)}$
4. $y=K e^{\frac{x^{3}}{3} + \frac{7 x^{2}}{2}}$
5. $y=K + \frac{x^{3}}{3} + \frac{7 x^{2}}{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =7yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =7yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(7x+{x}^{2}) \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =7x+{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (7x+{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (7x+{x}^{2})\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{7{x}^{2}}{2}+\frac{{x}^{3}}{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\frac{7{x}^{2}}{2}+\frac{{x}^{3}}{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & =\frac{7{x}^{2}}{2}+\frac{{x}^{3}}{3}+C \\ |y| & ={e}^{\frac{7{x}^{2}}{2}+{x}^{3}/3+C} \\ |y| & ={e}^{\frac{7{x}^{2}}{2}+{x}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{\frac{7{x}^{2}}{2}+{x}^{3}/3}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\frac{7{x}^{2}}{2}+{x}^{3}/3}.
$$

## Original q-79660

Find the general solution to the differential equation $(xy)^{2}\,\frac{\text{d}y}{\text{d}x}=1$ for $x\ne 0.$

- $y=\sqrt[3]{\frac{K}{x}+1}$
- $y=\sqrt[3]{K-\frac{1}{x}}$
- $y=\sqrt{K+\frac{1}{x}}$
- $y=\sqrt{K-\frac{2}{x}}$
- $y=\sqrt[3]{K-\frac{3}{x}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}(xy)^{2}\,\frac{\text{d}y}{\text{d}x} & =1 \\ {x}^{2}{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =1 \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \frac{1}{3}{y}^{3} & =-\frac{1}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{1}{3}{y}^{3}=C-\frac{1}{x}.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{1}{3}{y}^{3} & =C-\frac{1}{x} \\ {y}^{3} & =3C-\frac{3}{x} \\ y & =\sqrt[3]{3C-\frac{3}{x}} \\ y & =\sqrt[3]{K-\frac{3}{x}}\end{aligned}
$$

where $K=3C.$

### original replay q-79660

Find the general solution to the differential equation $(xy)^{2}\,\frac{\text{d}y}{\text{d}x}=1$ for $x\ne 0.$

1. $y=\sqrt{K + \frac{1}{x}}$
2. $y=\sqrt[3]{K - \frac{1}{x}}$
3. $y=\sqrt[3]{\frac{K}{x} + 1}$
4. $y=\sqrt[3]{K - \frac{3}{x}}$
5. $y=\sqrt{K - \frac{2}{x}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}(xy)^{2}\,\frac{\text{d}y}{\text{d}x} & =1 \\ {x}^{2}{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =1 \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x \\ \frac{1}{3}{y}^{3} & =-\frac{1}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{1}{3}{y}^{3}=C-\frac{1}{x}.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{1}{3}{y}^{3} & =C-\frac{1}{x} \\ {y}^{3} & =3C-\frac{3}{x} \\ y & =\sqrt[3]{3C-\frac{3}{x}} \\ y & =\sqrt[3]{K-\frac{3}{x}}\end{aligned}
$$

where $K=3C.$

### generated observed-bank evidence q-79660 a=2

Find the general solution to the differential equation $(xy)^{2}\,\frac{\text{d}y}{\text{d}x}=2$ for $x\ne 0.$

1. $y=\sqrt{K + \frac{2}{x}}$
2. $y=\sqrt[3]{K - \frac{2}{x}}$
3. $y=\sqrt{K - \frac{4}{x}}$
4. $y=\sqrt[3]{K - \frac{6}{x}}$
5. $y=\sqrt[3]{\frac{2 K}{x} + 1}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}(xy)^{2}\,\frac{\text{d}y}{\text{d}x} & =2 \\ {x}^{2}{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2 \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =\frac{2}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{2}{{x}^{2}}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int \frac{2}{{x}^{2}}\,\text{d}x \\ \frac{1}{3}{y}^{3} & =-\frac{2}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{1}{3}{y}^{3}=C-\frac{2}{x}.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{1}{3}{y}^{3} & =C-\frac{2}{x} \\ {y}^{3} & =3C-\frac{6}{x} \\ y & =\sqrt[3]{3C-\frac{6}{x}} \\ y & =\sqrt[3]{K-\frac{6}{x}}\end{aligned}
$$

where $K=3C.$

### generated authored-bank variant q-79660 a=2

Find the general solution to the differential equation $(xy)^{2}\,\frac{\text{d}y}{\text{d}x}=2$ for $x\ne 0.$

1. $y=\sqrt{K - \frac{6}{x}}$
2. $y=\sqrt[3]{K - \frac{2}{x}}$
3. $y=K - \frac{6}{x}$
4. $y=\sqrt[3]{K + \frac{6}{x}}$
5. $y=\sqrt[3]{K - \frac{6}{x}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}(xy)^{2}\,\frac{\text{d}y}{\text{d}x} & =2 \\ {x}^{2}{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2 \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =\frac{2}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{2}{{x}^{2}}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int \frac{2}{{x}^{2}}\,\text{d}x \\ \frac{1}{3}{y}^{3} & =-\frac{2}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{1}{3}{y}^{3}=C-\frac{2}{x}.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{1}{3}{y}^{3} & =C-\frac{2}{x} \\ {y}^{3} & =3C-\frac{6}{x} \\ y & =\sqrt[3]{3C-\frac{6}{x}} \\ y & =\sqrt[3]{K-\frac{6}{x}}\end{aligned}
$$

where $K=3C.$

### generated observed-bank evidence q-79660 a=7

Find the general solution to the differential equation $(xy)^{2}\,\frac{\text{d}y}{\text{d}x}=7$ for $x\ne 0.$

1. $y=\sqrt[3]{K - \frac{21}{x}}$
2. $y=\sqrt[3]{\frac{7 K}{x} + 1}$
3. $y=\sqrt{K - \frac{14}{x}}$
4. $y=\sqrt[3]{K - \frac{7}{x}}$
5. $y=\sqrt{K + \frac{7}{x}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}(xy)^{2}\,\frac{\text{d}y}{\text{d}x} & =7 \\ {x}^{2}{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =7 \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =\frac{7}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{7}{{x}^{2}}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int \frac{7}{{x}^{2}}\,\text{d}x \\ \frac{1}{3}{y}^{3} & =-\frac{7}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{1}{3}{y}^{3}=C-\frac{7}{x}.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{1}{3}{y}^{3} & =C-\frac{7}{x} \\ {y}^{3} & =3C-\frac{21}{x} \\ y & =\sqrt[3]{3C-\frac{21}{x}} \\ y & =\sqrt[3]{K-\frac{21}{x}}\end{aligned}
$$

where $K=3C.$

### generated authored-bank variant q-79660 a=7

Find the general solution to the differential equation $(xy)^{2}\,\frac{\text{d}y}{\text{d}x}=7$ for $x\ne 0.$

1. $y=\sqrt[3]{K + \frac{21}{x}}$
2. $y=\sqrt[3]{K - \frac{21}{x}}$
3. $y=K - \frac{21}{x}$
4. $y=\sqrt[3]{K - \frac{7}{x}}$
5. $y=\sqrt{K - \frac{21}{x}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}(xy)^{2}\,\frac{\text{d}y}{\text{d}x} & =7 \\ {x}^{2}{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =7 \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =\frac{7}{{x}^{2}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{7}{{x}^{2}}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int \frac{7}{{x}^{2}}\,\text{d}x \\ \frac{1}{3}{y}^{3} & =-\frac{7}{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{1}{3}{y}^{3}=C-\frac{7}{x}.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{1}{3}{y}^{3} & =C-\frac{7}{x} \\ {y}^{3} & =3C-\frac{21}{x} \\ y & =\sqrt[3]{3C-\frac{21}{x}} \\ y & =\sqrt[3]{K-\frac{21}{x}}\end{aligned}
$$

where $K=3C.$

## Original q-79663

Find the general solution to the differential equation ${y}^{′}-2xy=3{x}^{2}y$ for $y\ne 0.$

- $y=K{e}^{\sqrt{{x}^{3}+{x}^{2}}}$
- $y=K{e}^{\sqrt{3{x}^{2}+2x}}$
- $y=K{e}^{{x}^{3}+{x}^{2}}$
- $y=K{e}^{6x+2}$
- $y=K{e}^{3{x}^{2}+2x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-2xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x}-2xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x} & =3{x}^{2}y+2xy \\ \frac{\text{d}y}{\text{d}x} & =(3{x}^{2}+2x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =3{x}^{2}+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{x}^{2}+2x)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (3{x}^{2}+2x)\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{3}+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+{x}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+{x}^{2}+C \\ |y| & ={e}^{{x}^{3}+{x}^{2}+C} \\ |y| & ={e}^{{x}^{3}+{x}^{2}}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+{x}^{2}}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+{x}^{2}}.
$$

### original replay q-79663

Find the general solution to the differential equation ${y}^{′}-2xy=3{x}^{2}y$ for $y\ne 0.$

1. $y=K e^{x^{3} + x^{2}}$
2. $y=K e^{\sqrt{3 x^{2} + 2 x}}$
3. $y=K e^{\sqrt{x^{3} + x^{2}}}$
4. $y=K e^{3 x^{2} + 2 x}$
5. $y=K e^{6 x + 2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-2xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x}-2xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x} & =3{x}^{2}y+2xy \\ \frac{\text{d}y}{\text{d}x} & =(3{x}^{2}+2x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =3{x}^{2}+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{x}^{2}+2x)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (3{x}^{2}+2x)\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{3}+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+{x}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+{x}^{2}+C \\ |y| & ={e}^{{x}^{3}+{x}^{2}+C} \\ |y| & ={e}^{{x}^{3}+{x}^{2}}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+{x}^{2}}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+{x}^{2}}.
$$

### generated observed-bank evidence q-79663 a=2

Find the general solution to the differential equation ${y}^{′}-2xy=3{x}^{2}y$ for $y\ne 0.$

1. $y=K e^{x^{3} + x^{2}}$
2. $y=K e^{\sqrt{3 x^{2} + 2 x}}$
3. $y=K e^{6 x + 2}$
4. $y=K e^{3 x^{2} + 2 x}$
5. $y=K e^{\sqrt{x^{3} + x^{2}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-2xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x}-2xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x} & =3{x}^{2}y+2xy \\ \frac{\text{d}y}{\text{d}x} & =(3{x}^{2}+2x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =3{x}^{2}+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{x}^{2}+2x)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (3{x}^{2}+2x)\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{3}+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+{x}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+{x}^{2}+C \\ |y| & ={e}^{{x}^{3}+{x}^{2}+C} \\ |y| & ={e}^{{x}^{3}+{x}^{2}}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+{x}^{2}}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+{x}^{2}}.
$$

### generated normal variant q-79663 a=2

Find the general solution to the differential equation ${y}^{′}-2xy=3{x}^{2}y$ for $y\ne 0.$

1. $y=K e^{x^{3} + x^{2}}$
2. $y=K e^{\sqrt{3 x^{2} + 2 x}}$
3. $y=K e^{6 x + 2}$
4. $y=K e^{3 x^{2} + 2 x}$
5. $y=K e^{\sqrt{x^{3} + x^{2}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-2xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x}-2xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x} & =3{x}^{2}y+2xy \\ \frac{\text{d}y}{\text{d}x} & =(3{x}^{2}+2x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =3{x}^{2}+2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{x}^{2}+2x)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (3{x}^{2}+2x)\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{3}+{x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+{x}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+{x}^{2}+C \\ |y| & ={e}^{{x}^{3}+{x}^{2}+C} \\ |y| & ={e}^{{x}^{3}+{x}^{2}}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+{x}^{2}}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+{x}^{2}}.
$$

### generated observed-bank evidence q-79663 a=7

Find the general solution to the differential equation ${y}^{′}-7xy=3{x}^{2}y$ for $y\ne 0.$

1. $y=K e^{3 x^{2} + 7 x}$
2. $y=K e^{\sqrt{x^{3} + \frac{7 x^{2}}{2}}}$
3. $y=K e^{6 x + 7}$
4. $y=K e^{\sqrt{3 x^{2} + 7 x}}$
5. $y=K e^{x^{3} + \frac{7 x^{2}}{2}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-7xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x}-7xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x} & =3{x}^{2}y+7xy \\ \frac{\text{d}y}{\text{d}x} & =(3{x}^{2}+7x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =3{x}^{2}+7x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{x}^{2}+7x)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (3{x}^{2}+7x)\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{3}+\frac{7{x}^{2}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+\frac{7{x}^{2}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+\frac{7{x}^{2}}{2}+C \\ |y| & ={e}^{{x}^{3}+\frac{7{x}^{2}}{2}+C} \\ |y| & ={e}^{{x}^{3}+\frac{7{x}^{2}}{2}}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+\frac{7{x}^{2}}{2}}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+\frac{7{x}^{2}}{2}}.
$$

### generated normal variant q-79663 a=7

Find the general solution to the differential equation ${y}^{′}-7xy=3{x}^{2}y$ for $y\ne 0.$

1. $y=K e^{3 x^{2} + 7 x}$
2. $y=K e^{\sqrt{x^{3} + \frac{7 x^{2}}{2}}}$
3. $y=K e^{6 x + 7}$
4. $y=K e^{\sqrt{3 x^{2} + 7 x}}$
5. $y=K e^{x^{3} + \frac{7 x^{2}}{2}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-7xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x}-7xy & =3{x}^{2}y \\ \frac{\text{d}y}{\text{d}x} & =3{x}^{2}y+7xy \\ \frac{\text{d}y}{\text{d}x} & =(3{x}^{2}+7x)y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =3{x}^{2}+7x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{x}^{2}+7x)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (3{x}^{2}+7x)\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{3}+\frac{7{x}^{2}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={x}^{3}+\frac{7{x}^{2}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\operatorname{ln}⁡|y| & ={x}^{3}+\frac{7{x}^{2}}{2}+C \\ |y| & ={e}^{{x}^{3}+\frac{7{x}^{2}}{2}+C} \\ |y| & ={e}^{{x}^{3}+\frac{7{x}^{2}}{2}}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}+\frac{7{x}^{2}}{2}}\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}+\frac{7{x}^{2}}{2}}.
$$

## Original q-79664

Find the general solution to the differential equation ${y}^{′}-{y}^{2}=6{x}^{2}{y}^{2}$ for $y\ne 0.$

- $y=\frac{1}{{x}^{3}+{x}^{2}}+C$
- $y=-\frac{1}{2{x}^{3}+x+C}$
- $y=\frac{1}{{x}^{2}-x}+C$
- $y=\frac{1}{{x}^{3}+{x}^{2}+C}$
- $y=-\frac{C}{2{x}^{3}+x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x}-{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =6{x}^{2}{y}^{2}+{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =(6{x}^{2}+1){y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =6{x}^{2}+1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (6{x}^{2}+1)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (6{x}^{2}+1)\,\text{d}x \\ -\frac{1}{y} & =2{x}^{3}+x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}=2{x}^{3}+x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & =-\frac{1}{2{x}^{3}+x+C}.\end{aligned}
$$

### original replay q-79664

Find the general solution to the differential equation ${y}^{′}-{y}^{2}=6{x}^{2}{y}^{2}$ for $y\ne 0.$

1. $y=C + \frac{1}{x^{2} - x}$
2. $y=- \frac{1}{C + 2 x^{3} + x}$
3. $y=C + \frac{1}{x^{3} + x^{2}}$
4. $y=- \frac{C}{2 x^{3} + x}$
5. $y=\frac{1}{C + x^{3} + x^{2}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x}-{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =6{x}^{2}{y}^{2}+{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =(6{x}^{2}+1){y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =6{x}^{2}+1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (6{x}^{2}+1)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (6{x}^{2}+1)\,\text{d}x \\ -\frac{1}{y} & =2{x}^{3}+x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}=2{x}^{3}+x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & =-\frac{1}{2{x}^{3}+x+C}.\end{aligned}
$$

### generated observed-bank evidence q-79664 a=2

Find the general solution to the differential equation ${y}^{′}-2{y}^{2}=6{x}^{2}{y}^{2}$ for $y\ne 0.$

1. $y=C + \frac{1}{x^{2} - 2 x}$
2. $y=- \frac{1}{C + 2 x^{3} + 2 x}$
3. $y=\frac{1}{C + x^{3} + 2 x^{2}}$
4. $y=- \frac{C}{2 x^{3} + 2 x}$
5. $y=C + \frac{1}{x^{3} + 2 x^{2}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-2{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x}-2{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =6{x}^{2}{y}^{2}+2{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =(6{x}^{2}+2){y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =6{x}^{2}+2\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (6{x}^{2}+2)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (6{x}^{2}+2)\,\text{d}x \\ -\frac{1}{y} & =2{x}^{3}+2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}=2{x}^{3}+2x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & =-\frac{1}{2{x}^{3}+2x+C}.\end{aligned}
$$

### generated authored-bank variant q-79664 a=2

Find the general solution to the differential equation ${y}^{′}-2{y}^{2}=6{x}^{2}{y}^{2}$ for $y\ne 0.$

1. $y=- C - 2 x^{3} - 2 x$
2. $y=\frac{1}{C + 2 x^{3} + 2 x}$
3. $y=C - \frac{1}{2 x^{3} + 2 x}$
4. $y=- \frac{1}{C + 6 x^{2} + 2}$
5. $y=- \frac{1}{C + 2 x^{3} + 2 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-2{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x}-2{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =6{x}^{2}{y}^{2}+2{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =(6{x}^{2}+2){y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =6{x}^{2}+2\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (6{x}^{2}+2)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (6{x}^{2}+2)\,\text{d}x \\ -\frac{1}{y} & =2{x}^{3}+2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}=2{x}^{3}+2x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & =-\frac{1}{2{x}^{3}+2x+C}.\end{aligned}
$$

### generated observed-bank evidence q-79664 a=7

Find the general solution to the differential equation ${y}^{′}-7{y}^{2}=6{x}^{2}{y}^{2}$ for $y\ne 0.$

1. $y=- \frac{C}{2 x^{3} + 7 x}$
2. $y=C + \frac{1}{x^{3} + 7 x^{2}}$
3. $y=\frac{1}{C + x^{3} + 7 x^{2}}$
4. $y=- \frac{1}{C + 2 x^{3} + 7 x}$
5. $y=C + \frac{1}{x^{2} - 7 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-7{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x}-7{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =6{x}^{2}{y}^{2}+7{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =(6{x}^{2}+7){y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =6{x}^{2}+7\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (6{x}^{2}+7)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (6{x}^{2}+7)\,\text{d}x \\ -\frac{1}{y} & =2{x}^{3}+7x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}=2{x}^{3}+7x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & =-\frac{1}{2{x}^{3}+7x+C}.\end{aligned}
$$

### generated authored-bank variant q-79664 a=7

Find the general solution to the differential equation ${y}^{′}-7{y}^{2}=6{x}^{2}{y}^{2}$ for $y\ne 0.$

1. $y=- \frac{1}{C + 6 x^{2} + 7}$
2. $y=- \frac{1}{C + 2 x^{3} + 7 x}$
3. $y=C - \frac{1}{2 x^{3} + 7 x}$
4. $y=\frac{1}{C + 2 x^{3} + 7 x}$
5. $y=- C - 2 x^{3} - 7 x$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′}-7{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x}-7{y}^{2} & =6{x}^{2}{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =6{x}^{2}{y}^{2}+7{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & =(6{x}^{2}+7){y}^{2} \\ \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =6{x}^{2}+7\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (6{x}^{2}+7)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int (6{x}^{2}+7)\,\text{d}x \\ -\frac{1}{y} & =2{x}^{3}+7x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
-\frac{1}{y}=2{x}^{3}+7x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y & =-\frac{1}{2{x}^{3}+7x+C}.\end{aligned}
$$

## Original q-79665

Find the general solution to the differential equation $\frac{1}{\sqrt{xy}}\,{y}^{′}=1$ for $y\ne 0.$

- $y={({x}^{3}+K)}^{2}$
- $y={(\frac{1}{3}{x}^{3/2}+K)}^{2}$
- $y=\frac{1}{9}\,{x}^{3/2}+K$
- $y=\frac{1}{9}\,{x}^{3}+K$
- $y={(3{x}^{1/2}+K)}^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{1}{\sqrt{xy}}{y}^{′} & =1 \\ \frac{1}{\sqrt{xy}}\,\frac{\text{d}y}{\text{d}x} & =1 \\ \frac{1}{\sqrt{x}}\cdot \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =1 \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \sqrt{x}\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int \sqrt{x}\,\text{d}x \\ \int {y}^{-1/2}\,\text{d}y & =\int {x}^{1/2}\,\text{d}x \\ 2{y}^{1/2} & =\frac{2}{3}{x}^{3/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2{y}^{1/2}=\frac{2}{3}{x}^{3/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}2{y}^{1/2} & =\frac{2}{3}{x}^{3/2}+C \\ {y}^{1/2} & =\frac{1}{3}{x}^{3/2}+\frac{C}{2} \\ y & ={(\frac{1}{3}{x}^{3/2}+\frac{C}{2})}^{2} \\ y & ={(\frac{1}{3}{x}^{3/2}+K)}^{2}\end{aligned}
$$

where $K=\frac{C}{2}.$

### original replay q-79665

Find the general solution to the differential equation $\frac{1}{\sqrt{xy}}\,{y}^{′}=1$ for $y\ne 0.$

1. $y=K + \frac{x^{\frac{3}{2}}}{9}$
2. $y=\left(K + \frac{x^{\frac{3}{2}}}{3}\right)^{2}$
3. $y=\left(K + x^{3}\right)^{2}$
4. $y=\left(K + 3 \sqrt{x}\right)^{2}$
5. $y=K + \frac{x^{3}}{9}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{1}{\sqrt{xy}}{y}^{′} & =1 \\ \frac{1}{\sqrt{xy}}\,\frac{\text{d}y}{\text{d}x} & =1 \\ \frac{1}{\sqrt{x}}\cdot \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =1 \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \sqrt{x}\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int \sqrt{x}\,\text{d}x \\ \int {y}^{-1/2}\,\text{d}y & =\int {x}^{1/2}\,\text{d}x \\ 2{y}^{1/2} & =\frac{2}{3}{x}^{3/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2{y}^{1/2}=\frac{2}{3}{x}^{3/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}2{y}^{1/2} & =\frac{2}{3}{x}^{3/2}+C \\ {y}^{1/2} & =\frac{1}{3}{x}^{3/2}+\frac{C}{2} \\ y & ={(\frac{1}{3}{x}^{3/2}+\frac{C}{2})}^{2} \\ y & ={(\frac{1}{3}{x}^{3/2}+K)}^{2}\end{aligned}
$$

where $K=\frac{C}{2}.$

### generated observed-bank evidence q-79665 a=2

Find the general solution to the differential equation $\frac{1}{\sqrt{xy}}\,{y}^{′}=2$ for $y\ne 0.$

1. $y=K + \frac{4 x^{\frac{3}{2}}}{9}$
2. $y=\left(K + \frac{2 x^{\frac{3}{2}}}{3}\right)^{2}$
3. $y=K + \frac{4 x^{3}}{9}$
4. $y=\left(K + 6 \sqrt{x}\right)^{2}$
5. $y=\left(K + 2 x^{3}\right)^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{1}{\sqrt{xy}}{y}^{′} & =2 \\ \frac{1}{\sqrt{xy}}\,\frac{\text{d}y}{\text{d}x} & =2 \\ \frac{1}{\sqrt{x}}\cdot \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =2 \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =2\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\sqrt{x}\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 2\sqrt{x}\,\text{d}x \\ \int {y}^{-1/2}\,\text{d}y & =\int 2{x}^{1/2}\,\text{d}x \\ 2{y}^{1/2} & =\frac{4}{3}{x}^{3/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2{y}^{1/2}=\frac{4}{3}{x}^{3/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}2{y}^{1/2} & =\frac{4}{3}{x}^{3/2}+C \\ {y}^{1/2} & =\frac{2}{3}{x}^{3/2}+\frac{C}{2} \\ y & ={(\frac{2}{3}{x}^{3/2}+\frac{C}{2})}^{2} \\ y & ={(\frac{2}{3}{x}^{3/2}+K)}^{2}\end{aligned}
$$

where $K=\frac{C}{2}.$

### generated authored-bank variant q-79665 a=2

Find the general solution to the differential equation $\frac{1}{\sqrt{xy}}\,{y}^{′}=2$ for $y\ne 0.$

Assume $x>0$ and $y>0.$

Use an interval where $\frac{2 x^{\frac{3}{2}}}{3}+K>0.$

1. $y=K + \frac{2 x^{\frac{3}{2}}}{3}$
2. $y=\left(K + \frac{4 x^{\frac{3}{2}}}{3}\right)^{2}$
3. $y=\left(K + \frac{2 x^{\frac{3}{2}}}{3}\right)^{3}$
4. $y=\left(K + 2 \sqrt{x}\right)^{2}$
5. $y=\left(K + \frac{2 x^{\frac{3}{2}}}{3}\right)^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{1}{\sqrt{xy}}{y}^{′} & =2 \\ \frac{1}{\sqrt{xy}}\,\frac{\text{d}y}{\text{d}x} & =2 \\ \frac{1}{\sqrt{x}}\cdot \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =2 \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =2\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\sqrt{x}\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 2\sqrt{x}\,\text{d}x \\ \int {y}^{-1/2}\,\text{d}y & =\int 2{x}^{1/2}\,\text{d}x \\ 2{y}^{1/2} & =\frac{4}{3}{x}^{3/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2{y}^{1/2}=\frac{4}{3}{x}^{3/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}2{y}^{1/2} & =\frac{4}{3}{x}^{3/2}+C \\ {y}^{1/2} & =\frac{2}{3}{x}^{3/2}+\frac{C}{2} \\ y & ={(\frac{2}{3}{x}^{3/2}+\frac{C}{2})}^{2} \\ y & ={(\frac{2}{3}{x}^{3/2}+K)}^{2}\end{aligned}
$$

where $K=\frac{C}{2}.$

### generated observed-bank evidence q-79665 a=7

Find the general solution to the differential equation $\frac{1}{\sqrt{xy}}\,{y}^{′}=7$ for $y\ne 0.$

1. $y=\left(K + 21 \sqrt{x}\right)^{2}$
2. $y=\left(K + 7 x^{3}\right)^{2}$
3. $y=K + \frac{49 x^{3}}{9}$
4. $y=\left(K + \frac{7 x^{\frac{3}{2}}}{3}\right)^{2}$
5. $y=K + \frac{49 x^{\frac{3}{2}}}{9}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{1}{\sqrt{xy}}{y}^{′} & =7 \\ \frac{1}{\sqrt{xy}}\,\frac{\text{d}y}{\text{d}x} & =7 \\ \frac{1}{\sqrt{x}}\cdot \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =7 \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =7\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 7\sqrt{x}\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 7\sqrt{x}\,\text{d}x \\ \int {y}^{-1/2}\,\text{d}y & =\int 7{x}^{1/2}\,\text{d}x \\ 2{y}^{1/2} & =\frac{14}{3}{x}^{3/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2{y}^{1/2}=\frac{14}{3}{x}^{3/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}2{y}^{1/2} & =\frac{14}{3}{x}^{3/2}+C \\ {y}^{1/2} & =\frac{7}{3}{x}^{3/2}+\frac{C}{2} \\ y & ={(\frac{7}{3}{x}^{3/2}+\frac{C}{2})}^{2} \\ y & ={(\frac{7}{3}{x}^{3/2}+K)}^{2}\end{aligned}
$$

where $K=\frac{C}{2}.$

### generated authored-bank variant q-79665 a=7

Find the general solution to the differential equation $\frac{1}{\sqrt{xy}}\,{y}^{′}=7$ for $y\ne 0.$

Assume $x>0$ and $y>0.$

Use an interval where $\frac{7 x^{\frac{3}{2}}}{3}+K>0.$

1. $y=\left(K + 7 \sqrt{x}\right)^{2}$
2. $y=\left(K + \frac{7 x^{\frac{3}{2}}}{3}\right)^{2}$
3. $y=\left(K + \frac{7 x^{\frac{3}{2}}}{3}\right)^{3}$
4. $y=\left(K + \frac{14 x^{\frac{3}{2}}}{3}\right)^{2}$
5. $y=K + \frac{7 x^{\frac{3}{2}}}{3}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{1}{\sqrt{xy}}{y}^{′} & =7 \\ \frac{1}{\sqrt{xy}}\,\frac{\text{d}y}{\text{d}x} & =7 \\ \frac{1}{\sqrt{x}}\cdot \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =7 \\ \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x} & =7\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{y}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 7\sqrt{x}\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 7\sqrt{x}\,\text{d}x \\ \int {y}^{-1/2}\,\text{d}y & =\int 7{x}^{1/2}\,\text{d}x \\ 2{y}^{1/2} & =\frac{14}{3}{x}^{3/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
2{y}^{1/2}=\frac{14}{3}{x}^{3/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}2{y}^{1/2} & =\frac{14}{3}{x}^{3/2}+C \\ {y}^{1/2} & =\frac{7}{3}{x}^{3/2}+\frac{C}{2} \\ y & ={(\frac{7}{3}{x}^{3/2}+\frac{C}{2})}^{2} \\ y & ={(\frac{7}{3}{x}^{3/2}+K)}^{2}\end{aligned}
$$

where $K=\frac{C}{2}.$

## Original q-79666

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}+\frac{\operatorname{sin}⁡x}{2y}=0$ for $y>0.$

- $y={e}^{\operatorname{cos}⁡x+C}$
- $y={e}^{\operatorname{sec}⁡x+C}$
- $y={e}^{\sqrt{\operatorname{cos}⁡x+C}}$
- $y=\sqrt{\operatorname{sec}⁡x+C}$
- $y=\sqrt{\operatorname{cos}⁡x+C}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+\frac{\operatorname{sin}⁡x}{2y} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-\frac{\operatorname{sin}⁡x}{2y} \\ 2y\,\frac{\text{d}y}{\text{d}x} & =-\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 2y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int \operatorname{sin}⁡x\,\text{d}x \\ \int 2y\,\text{d}y & =-\int \operatorname{sin}⁡x\,\text{d}x \\ {y}^{2} & =\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{2}=\operatorname{cos}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt{\operatorname{cos}⁡x+C}.
$$

### original replay q-79666

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}+\frac{\operatorname{sin}⁡x}{2y}=0$ for $y>0.$

1. $y=e^{\sqrt{C + \cos{\left(x \right)}}}$
2. $y=e^{C + \sec{\left(x \right)}}$
3. $y=e^{C + \cos{\left(x \right)}}$
4. $y=\sqrt{C + \cos{\left(x \right)}}$
5. $y=\sqrt{C + \sec{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+\frac{\operatorname{sin}⁡x}{2y} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-\frac{\operatorname{sin}⁡x}{2y} \\ 2y\,\frac{\text{d}y}{\text{d}x} & =-\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 2y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int \operatorname{sin}⁡x\,\text{d}x \\ \int 2y\,\text{d}y & =-\int \operatorname{sin}⁡x\,\text{d}x \\ {y}^{2} & =\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{2}=\operatorname{cos}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt{\operatorname{cos}⁡x+C}.
$$

### generated observed-bank evidence q-79666 a=2

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}+\frac{2\operatorname{sin}⁡x}{2y}=0$ for $y>0.$

1. $y=e^{\sqrt{C + 2 \cos{\left(x \right)}}}$
2. $y=e^{C + 2 \sec{\left(x \right)}}$
3. $y=\sqrt{C + 2 \sec{\left(x \right)}}$
4. $y=\sqrt{C + 2 \cos{\left(x \right)}}$
5. $y=e^{C + 2 \cos{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+\frac{2\operatorname{sin}⁡x}{2y} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-\frac{2\operatorname{sin}⁡x}{2y} \\ 2y\,\frac{\text{d}y}{\text{d}x} & =-2\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 2y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int 2\operatorname{sin}⁡x\,\text{d}x \\ \int 2y\,\text{d}y & =-\int 2\operatorname{sin}⁡x\,\text{d}x \\ {y}^{2} & =2\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{2}=2\operatorname{cos}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt{2\operatorname{cos}⁡x+C}.
$$

### generated normal variant q-79666 a=2

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}+\frac{2\operatorname{sin}⁡x}{2y}=0$ for $y>0.$

1. $y=e^{\sqrt{C + 2 \cos{\left(x \right)}}}$
2. $y=e^{C + 2 \sec{\left(x \right)}}$
3. $y=\sqrt{C + 2 \sec{\left(x \right)}}$
4. $y=\sqrt{C + 2 \cos{\left(x \right)}}$
5. $y=e^{C + 2 \cos{\left(x \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+\frac{2\operatorname{sin}⁡x}{2y} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-\frac{2\operatorname{sin}⁡x}{2y} \\ 2y\,\frac{\text{d}y}{\text{d}x} & =-2\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 2y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int 2\operatorname{sin}⁡x\,\text{d}x \\ \int 2y\,\text{d}y & =-\int 2\operatorname{sin}⁡x\,\text{d}x \\ {y}^{2} & =2\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{2}=2\operatorname{cos}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt{2\operatorname{cos}⁡x+C}.
$$

### generated observed-bank evidence q-79666 a=7

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}+\frac{7\operatorname{sin}⁡x}{2y}=0$ for $y>0.$

1. $y=\sqrt{C + 7 \cos{\left(x \right)}}$
2. $y=e^{C + 7 \cos{\left(x \right)}}$
3. $y=\sqrt{C + 7 \sec{\left(x \right)}}$
4. $y=e^{C + 7 \sec{\left(x \right)}}$
5. $y=e^{\sqrt{C + 7 \cos{\left(x \right)}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+\frac{7\operatorname{sin}⁡x}{2y} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-\frac{7\operatorname{sin}⁡x}{2y} \\ 2y\,\frac{\text{d}y}{\text{d}x} & =-7\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 2y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int 7\operatorname{sin}⁡x\,\text{d}x \\ \int 2y\,\text{d}y & =-\int 7\operatorname{sin}⁡x\,\text{d}x \\ {y}^{2} & =7\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{2}=7\operatorname{cos}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt{7\operatorname{cos}⁡x+C}.
$$

### generated normal variant q-79666 a=7

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}+\frac{7\operatorname{sin}⁡x}{2y}=0$ for $y>0.$

1. $y=\sqrt{C + 7 \cos{\left(x \right)}}$
2. $y=e^{C + 7 \cos{\left(x \right)}}$
3. $y=\sqrt{C + 7 \sec{\left(x \right)}}$
4. $y=e^{C + 7 \sec{\left(x \right)}}$
5. $y=e^{\sqrt{C + 7 \cos{\left(x \right)}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+\frac{7\operatorname{sin}⁡x}{2y} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-\frac{7\operatorname{sin}⁡x}{2y} \\ 2y\,\frac{\text{d}y}{\text{d}x} & =-7\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 2y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int 7\operatorname{sin}⁡x\,\text{d}x \\ \int 2y\,\text{d}y & =-\int 7\operatorname{sin}⁡x\,\text{d}x \\ {y}^{2} & =7\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{2}=7\operatorname{cos}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt{7\operatorname{cos}⁡x+C}.
$$

## Original q-8304

Find the general solution to the differential equation $\sqrt{xy}\,\frac{\text{d}y}{\text{d}x}=1.$

- $y=3{x}^{1/3}+K$
- $y=3{x}^{1/2}+K$
- $y={(3{x}^{1/2}+K)}^{2/3}$
- $y={({x}^{1/2}+K)}^{2/3}$
- $y={({x}^{2/3}+K)}^{1/2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{xy}\,\frac{\text{d}y}{\text{d}x} & =1 \\ \sqrt{x}\sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =1 \\ \sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{x}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\sqrt{x}}\,\text{d}x \\ \int \sqrt{y}\,\text{d}y & =\int \frac{1}{\sqrt{x}}\,\text{d}x \\ \int {y}^{1/2}\,\text{d}y & =\int {x}^{-1/2}\,\text{d}x \\ \frac{2}{3}{y}^{3/2} & =2{x}^{1/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{2}{3}{y}^{3/2}=2{x}^{1/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{2}{3}{y}^{3/2} & =2{x}^{1/2}+C \\ {y}^{3/2} & =3{x}^{1/2}+\frac{3C}{2} \\ y & ={(3{x}^{1/2}+\frac{3C}{2})}^{2/3} \\ y & ={(3{x}^{1/2}+K)}^{2/3}\end{aligned}
$$

where $K=\frac{3C}{2}.$

### original replay q-8304

Find the general solution to the differential equation $\sqrt{xy}\,\frac{\text{d}y}{\text{d}x}=1.$

1. $y=\left(K + 3 \sqrt{x}\right)^{\frac{2}{3}}$
2. $y=K + 3 \sqrt{x}$
3. $y=K + 3 \sqrt[3]{x}$
4. $y=\sqrt{K + x^{\frac{2}{3}}}$
5. $y=\left(K + \sqrt{x}\right)^{\frac{2}{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{xy}\,\frac{\text{d}y}{\text{d}x} & =1 \\ \sqrt{x}\sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =1 \\ \sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{x}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\sqrt{x}}\,\text{d}x \\ \int \sqrt{y}\,\text{d}y & =\int \frac{1}{\sqrt{x}}\,\text{d}x \\ \int {y}^{1/2}\,\text{d}y & =\int {x}^{-1/2}\,\text{d}x \\ \frac{2}{3}{y}^{3/2} & =2{x}^{1/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{2}{3}{y}^{3/2}=2{x}^{1/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{2}{3}{y}^{3/2} & =2{x}^{1/2}+C \\ {y}^{3/2} & =3{x}^{1/2}+\frac{3C}{2} \\ y & ={(3{x}^{1/2}+\frac{3C}{2})}^{2/3} \\ y & ={(3{x}^{1/2}+K)}^{2/3}\end{aligned}
$$

where $K=\frac{3C}{2}.$

### generated observed-bank evidence q-8304 a=2

Find the general solution to the differential equation $\sqrt{xy}\,\frac{\text{d}y}{\text{d}x}=2.$

1. $y=\left(K + 6 \sqrt{x}\right)^{\frac{2}{3}}$
2. $y=K + 6 \sqrt{x}$
3. $y=\left(K + 2 \sqrt{x}\right)^{\frac{2}{3}}$
4. $y=\sqrt{K + 2 x^{\frac{2}{3}}}$
5. $y=K + 6 \sqrt[3]{x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{xy}\,\frac{\text{d}y}{\text{d}x} & =2 \\ \sqrt{x}\sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =2 \\ \sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{2}{\sqrt{x}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{2}{\sqrt{x}}\,\text{d}x \\ \int \sqrt{y}\,\text{d}y & =\int \frac{2}{\sqrt{x}}\,\text{d}x \\ \int {y}^{1/2}\,\text{d}y & =\int 2{x}^{-1/2}\,\text{d}x \\ \frac{2}{3}{y}^{3/2} & =4{x}^{1/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{2}{3}{y}^{3/2}=4{x}^{1/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{2}{3}{y}^{3/2} & =4{x}^{1/2}+C \\ {y}^{3/2} & =6{x}^{1/2}+\frac{3C}{2} \\ y & ={(6{x}^{1/2}+\frac{3C}{2})}^{2/3} \\ y & ={(6{x}^{1/2}+K)}^{2/3}\end{aligned}
$$

where $K=\frac{3C}{2}.$

### generated authored-bank variant q-8304 a=2

Find the general solution to the differential equation $\sqrt{xy}\,\frac{\text{d}y}{\text{d}x}=2.$

Assume $x>0$ and $y>0.$

Use an interval where $6 \sqrt{x}+K>0.$

1. $y=\left(K + 2 \sqrt{x}\right)^{\frac{2}{3}}$
2. $y=K + 6 \sqrt{x}$
3. $y=\left(K + 6 \sqrt{x}\right)^{2}$
4. $y=\sqrt{K + 6 \sqrt{x}}$
5. $y=\left(K + 6 \sqrt{x}\right)^{\frac{2}{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{xy}\,\frac{\text{d}y}{\text{d}x} & =2 \\ \sqrt{x}\sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =2 \\ \sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{2}{\sqrt{x}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{2}{\sqrt{x}}\,\text{d}x \\ \int \sqrt{y}\,\text{d}y & =\int \frac{2}{\sqrt{x}}\,\text{d}x \\ \int {y}^{1/2}\,\text{d}y & =\int 2{x}^{-1/2}\,\text{d}x \\ \frac{2}{3}{y}^{3/2} & =4{x}^{1/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{2}{3}{y}^{3/2}=4{x}^{1/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{2}{3}{y}^{3/2} & =4{x}^{1/2}+C \\ {y}^{3/2} & =6{x}^{1/2}+\frac{3C}{2} \\ y & ={(6{x}^{1/2}+\frac{3C}{2})}^{2/3} \\ y & ={(6{x}^{1/2}+K)}^{2/3}\end{aligned}
$$

where $K=\frac{3C}{2}.$

### generated observed-bank evidence q-8304 a=7

Find the general solution to the differential equation $\sqrt{xy}\,\frac{\text{d}y}{\text{d}x}=7.$

1. $y=\sqrt{K + 7 x^{\frac{2}{3}}}$
2. $y=K + 21 \sqrt[3]{x}$
3. $y=\left(K + 7 \sqrt{x}\right)^{\frac{2}{3}}$
4. $y=K + 21 \sqrt{x}$
5. $y=\left(K + 21 \sqrt{x}\right)^{\frac{2}{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{xy}\,\frac{\text{d}y}{\text{d}x} & =7 \\ \sqrt{x}\sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =7 \\ \sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{7}{\sqrt{x}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{7}{\sqrt{x}}\,\text{d}x \\ \int \sqrt{y}\,\text{d}y & =\int \frac{7}{\sqrt{x}}\,\text{d}x \\ \int {y}^{1/2}\,\text{d}y & =\int 7{x}^{-1/2}\,\text{d}x \\ \frac{2}{3}{y}^{3/2} & =14{x}^{1/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{2}{3}{y}^{3/2}=14{x}^{1/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{2}{3}{y}^{3/2} & =14{x}^{1/2}+C \\ {y}^{3/2} & =21{x}^{1/2}+\frac{3C}{2} \\ y & ={(21{x}^{1/2}+\frac{3C}{2})}^{2/3} \\ y & ={(21{x}^{1/2}+K)}^{2/3}\end{aligned}
$$

where $K=\frac{3C}{2}.$

### generated authored-bank variant q-8304 a=7

Find the general solution to the differential equation $\sqrt{xy}\,\frac{\text{d}y}{\text{d}x}=7.$

Assume $x>0$ and $y>0.$

Use an interval where $21 \sqrt{x}+K>0.$

1. $y=\sqrt{K + 21 \sqrt{x}}$
2. $y=\left(K + 21 \sqrt{x}\right)^{\frac{2}{3}}$
3. $y=\left(K + 21 \sqrt{x}\right)^{2}$
4. $y=K + 21 \sqrt{x}$
5. $y=\left(K + 7 \sqrt{x}\right)^{\frac{2}{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\sqrt{xy}\,\frac{\text{d}y}{\text{d}x} & =7 \\ \sqrt{x}\sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =7 \\ \sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{7}{\sqrt{x}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{7}{\sqrt{x}}\,\text{d}x \\ \int \sqrt{y}\,\text{d}y & =\int \frac{7}{\sqrt{x}}\,\text{d}x \\ \int {y}^{1/2}\,\text{d}y & =\int 7{x}^{-1/2}\,\text{d}x \\ \frac{2}{3}{y}^{3/2} & =14{x}^{1/2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{2}{3}{y}^{3/2}=14{x}^{1/2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\frac{2}{3}{y}^{3/2} & =14{x}^{1/2}+C \\ {y}^{3/2} & =21{x}^{1/2}+\frac{3C}{2} \\ y & ={(21{x}^{1/2}+\frac{3C}{2})}^{2/3} \\ y & ={(21{x}^{1/2}+K)}^{2/3}\end{aligned}
$$

where $K=\frac{3C}{2}.$

## authored easy easy_linear a=3

Find the general solution to the differential equation $y'+3 xy=0$ for $y\ne0.$

1. $y=K + e^{- \frac{3 x^{2}}{2}}$
2. $y=K e^{\frac{3 x^{2}}{2}}$
3. $y=K e^{- 3 x}$
4. $y=K - \frac{3 x^{2}}{2}$
5. $y=K e^{- \frac{3 x^{2}}{2}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y'+3 xy=0 \\ \frac{\text{d}y}{\text{d}x}+3 xy & =0 \\ \frac{\text{d}y}{\text{d}x} & =- 3 xy \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =- 3 x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (- 3 x)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (- 3 x)\,\text{d}x \\ \ln|y| & =- \frac{3 x^{2}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\ln|y|=- \frac{3 x^{2}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\ln|y| & =- \frac{3 x^{2}}{2}+C \\ |y| & =e^{- \frac{3 x^{2}}{2}+C} \\ |y| & =e^{- \frac{3 x^{2}}{2}}\cdot e^C \\ |y| & =K e^{- \frac{3 x^{2}}{2}}\end{aligned}
$$

where $K=e^C$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K e^{- \frac{3 x^{2}}{2}}.
$$

## authored easy easy_linear a=-4

Find the general solution to the differential equation $y'-4 xy=0$ for $y\ne0.$

1. $y=K + e^{2 x^{2}}$
2. $y=K e^{- 2 x^{2}}$
3. $y=K e^{4 x}$
4. $y=K + 2 x^{2}$
5. $y=K e^{2 x^{2}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y'-4 xy=0 \\ \frac{\text{d}y}{\text{d}x}-4 xy & =0 \\ \frac{\text{d}y}{\text{d}x} & =4 xy \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =4 x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (4 x)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (4 x)\,\text{d}x \\ \ln|y| & =2 x^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\ln|y|=2 x^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\ln|y| & =2 x^{2}+C \\ |y| & =e^{2 x^{2}+C} \\ |y| & =e^{2 x^{2}}\cdot e^C \\ |y| & =K e^{2 x^{2}}\end{aligned}
$$

where $K=e^C$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K e^{2 x^{2}}.
$$

## authored easy easy_constant a=3

Find the general solution to the differential equation $y'+3y=0$ for $y\ne0.$

1. $y=K + e^{- 3 x}$
2. $y=K e^{3 x}$
3. $y=\frac{K}{e^{3}}$
4. $y=K - 3 x$
5. $y=K e^{- 3 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y'+3y=0 \\ \frac{\text{d}y}{\text{d}x}+3y & =0 \\ \frac{\text{d}y}{\text{d}x} & =-3y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =-3\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-3)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (-3)\,\text{d}x \\ \ln|y| & =- 3 x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\ln|y|=- 3 x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\ln|y| & =- 3 x+C \\ |y| & =e^{- 3 x+C} \\ |y| & =e^{- 3 x}\cdot e^C \\ |y| & =K e^{- 3 x}\end{aligned}
$$

where $K=e^C$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K e^{- 3 x}.
$$

## authored easy easy_constant a=-4

Find the general solution to the differential equation $y'-4y=0$ for $y\ne0.$

1. $y=K + e^{4 x}$
2. $y=K e^{- 4 x}$
3. $y=K e^{4}$
4. $y=K + 4 x$
5. $y=K e^{4 x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y'-4y=0 \\ \frac{\text{d}y}{\text{d}x}-4y & =0 \\ \frac{\text{d}y}{\text{d}x} & =4y \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =4\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (4)\,\text{d}x \\ \ln|y| & =4 x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\ln|y|=4 x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}\ln|y| & =4 x+C \\ |y| & =e^{4 x+C} \\ |y| & =e^{4 x}\cdot e^C \\ |y| & =K e^{4 x}\end{aligned}
$$

where $K=e^C$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K e^{4 x}.
$$
