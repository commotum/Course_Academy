# Review: special-case multivariable chain rule

Raw source banks are evidence-only. Generated normal questions use complete operation banks. Radial normal questions state x>0.


## Raw source replay q-94588

If $f(x,y)=\operatorname{sin}⁡({x}^{2}+y)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 2{x}^{3}\operatorname{cos}⁡(2{x}^{2})

- 2x{sin}^{2}⁡(2x)

- ({x}^{2}+1)\operatorname{cos}⁡({x}^{2})

- 2x(x+1)\operatorname{sin}⁡({x}^{2})

- 4x\operatorname{cos}⁡(2{x}^{2}) [correct]

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x\operatorname{cos}⁡({x}^{2}+y),\,\frac{∂f}{∂y}=\operatorname{cos}⁡({x}^{2}+y)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2x\operatorname{cos}⁡({x}^{2}+{x}^{2})=2x\operatorname{cos}⁡(2{x}^{2}), \\ \frac{∂f}{∂y} & =\operatorname{cos}⁡({x}^{2}+{x}^{2})=\operatorname{cos}⁡(2{x}^{2}).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2x\operatorname{cos}⁡(2{x}^{2})+\operatorname{cos}⁡(2{x}^{2})\cdot 2x \\  & =2x\operatorname{cos}⁡(2{x}^{2})+2x\operatorname{cos}⁡(2{x}^{2}) \\  & =4x\operatorname{cos}⁡(2{x}^{2}).\end{aligned}
$$


## Generated normal sine_power a=2

If $f(x,y)=2\cdot \left(\operatorname{sin}⁡({x}^{2}+y)\right)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 0

- 4 x \cos{\left(2 x^{2} \right)}

- 8 x \cos{\left(2 x^{2} \right)} [correct]

- 2 x^{2} \cos{\left(2 x^{2} \right)} + 4 x \cos{\left(2 x^{2} \right)}

- 4 x \cos{\left(2 x^{2} \right)} + 2 \cos{\left(2 x^{2} \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left(2x\operatorname{cos}⁡({x}^{2}+y)\right),\,\frac{∂f}{∂y}=2\cdot \left(\operatorname{cos}⁡({x}^{2}+y)\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left(2x\operatorname{cos}⁡({x}^{2}+{x}^{2})\right)=2\cdot \left(2x\operatorname{cos}⁡(2{x}^{2})\right), \\ \frac{∂f}{∂y} & =2\cdot \left(\operatorname{cos}⁡({x}^{2}+{x}^{2})\right)=2\cdot \left(\operatorname{cos}⁡(2{x}^{2})\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left(2x\operatorname{cos}⁡(2{x}^{2})+\operatorname{cos}⁡(2{x}^{2})\cdot 2x\right) \\  & =2\cdot \left(2x\operatorname{cos}⁡(2{x}^{2})+2x\operatorname{cos}⁡(2{x}^{2})\right) \\  & =2\cdot \left(4x\operatorname{cos}⁡(2{x}^{2})\right).\end{aligned}
$$


## Generated normal sine_power a=-3

If $f(x,y)=-3\cdot \left(\operatorname{sin}⁡({x}^{2}+y)\right)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 0

- - 6 x \cos{\left(2 x^{2} \right)}

- - 12 x \cos{\left(2 x^{2} \right)} [correct]

- - 3 x^{2} \cos{\left(2 x^{2} \right)} - 6 x \cos{\left(2 x^{2} \right)}

- - 6 x \cos{\left(2 x^{2} \right)} - 3 \cos{\left(2 x^{2} \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left(2x\operatorname{cos}⁡({x}^{2}+y)\right),\,\frac{∂f}{∂y}=-3\cdot \left(\operatorname{cos}⁡({x}^{2}+y)\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left(2x\operatorname{cos}⁡({x}^{2}+{x}^{2})\right)=-3\cdot \left(2x\operatorname{cos}⁡(2{x}^{2})\right), \\ \frac{∂f}{∂y} & =-3\cdot \left(\operatorname{cos}⁡({x}^{2}+{x}^{2})\right)=-3\cdot \left(\operatorname{cos}⁡(2{x}^{2})\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left(2x\operatorname{cos}⁡(2{x}^{2})+\operatorname{cos}⁡(2{x}^{2})\cdot 2x\right) \\  & =-3\cdot \left(2x\operatorname{cos}⁡(2{x}^{2})+2x\operatorname{cos}⁡(2{x}^{2})\right) \\  & =-3\cdot \left(4x\operatorname{cos}⁡(2{x}^{2})\right).\end{aligned}
$$


## Raw source replay q-95121

If $f(x,y)=x\operatorname{ln}⁡(x+y)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$

- \operatorname{ln}⁡(1+{x}^{2})-\frac{1+3{x}^{2}}{1+2x}

- {x}^{2}\operatorname{ln}⁡(1+x)

- \operatorname{ln}⁡(x+{x}^{2})+\frac{1+2x}{1+x} [correct]

- \frac{1+2x}{1+x}

- \operatorname{ln}⁡(1+x)-\frac{1+2{x}^{2}}{1+{x}^{2}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\operatorname{ln}⁡(x+y)+\frac{x}{x+y},\,\frac{∂f}{∂y}=\frac{x}{x+y}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{ln}⁡(x+{x}^{2})+\frac{x}{x+{x}^{2}}, \\ \frac{∂f}{∂y} & =\frac{x}{x+{x}^{2}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\operatorname{ln}⁡(x+{x}^{2})+\frac{x}{x+{x}^{2}}+\frac{x}{x+{x}^{2}}\cdot 2x \\  & =\operatorname{ln}⁡(x+{x}^{2})+\frac{x+2{x}^{2}}{x+{x}^{2}} \\  & =\operatorname{ln}⁡(x+{x}^{2})+\frac{x(1+2x)}{x(1+x)} \\  & =\operatorname{ln}⁡(x+{x}^{2})+\frac{1+2x}{1+x}.\end{aligned}
$$


## Generated normal x_log_sum a=2

If $f(x,y)=2\cdot \left(x\operatorname{ln}⁡(x+y)\right)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$

- - \frac{4 x^{2}}{x^{2} + x} + \frac{2 x}{x^{2} + x} + 2 \ln{\left(x^{2} + x \right)}

- \frac{2 x}{x^{2} + x} + 2 \ln{\left(x^{2} + x \right)}

- \frac{4 x^{2}}{x^{2} + x} + \frac{2 x}{x^{2} + x} + 2 \ln{\left(x^{2} + x \right)} [correct]

- \frac{2 x^{3}}{x^{2} + x} + \frac{2 x}{x^{2} + x} + 2 \ln{\left(x^{2} + x \right)}

- \frac{4 x}{x^{2} + x} + 2 \ln{\left(x^{2} + x \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left(\operatorname{ln}⁡(x+y)+\frac{x}{x+y}\right),\,\frac{∂f}{∂y}=2\cdot \left(\frac{x}{x+y}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{x}{x+{x}^{2}}\right), \\ \frac{∂f}{∂y} & =2\cdot \left(\frac{x}{x+{x}^{2}}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{x}{x+{x}^{2}}+\frac{x}{x+{x}^{2}}\cdot 2x\right) \\  & =2\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{x+2{x}^{2}}{x+{x}^{2}}\right) \\  & =2\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{x(1+2x)}{x(1+x)}\right) \\  & =2\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{1+2x}{1+x}\right).\end{aligned}
$$


## Generated normal x_log_sum a=-3

If $f(x,y)=-3\cdot \left(x\operatorname{ln}⁡(x+y)\right)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$

- \frac{6 x^{2}}{x^{2} + x} - \frac{3 x}{x^{2} + x} - 3 \ln{\left(x^{2} + x \right)}

- - \frac{3 x}{x^{2} + x} - 3 \ln{\left(x^{2} + x \right)}

- - \frac{6 x^{2}}{x^{2} + x} - \frac{3 x}{x^{2} + x} - 3 \ln{\left(x^{2} + x \right)} [correct]

- - \frac{3 x^{3}}{x^{2} + x} - \frac{3 x}{x^{2} + x} - 3 \ln{\left(x^{2} + x \right)}

- - \frac{6 x}{x^{2} + x} - 3 \ln{\left(x^{2} + x \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left(\operatorname{ln}⁡(x+y)+\frac{x}{x+y}\right),\,\frac{∂f}{∂y}=-3\cdot \left(\frac{x}{x+y}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{x}{x+{x}^{2}}\right), \\ \frac{∂f}{∂y} & =-3\cdot \left(\frac{x}{x+{x}^{2}}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{x}{x+{x}^{2}}+\frac{x}{x+{x}^{2}}\cdot 2x\right) \\  & =-3\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{x+2{x}^{2}}{x+{x}^{2}}\right) \\  & =-3\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{x(1+2x)}{x(1+x)}\right) \\  & =-3\cdot \left(\operatorname{ln}⁡(x+{x}^{2})+\frac{1+2x}{1+x}\right).\end{aligned}
$$


## Raw source replay q-170670

If $f(x,y)=y\operatorname{ln}⁡({x}^{2}+1)$ and $y={x}^{2}+1,$ compute $\frac{\text{d}f}{\text{d}x}.$

- \frac{2x({x}^{2}+1)}{\operatorname{ln}⁡({x}^{2}+1)}

- 2x(1+\operatorname{ln}⁡({x}^{2}+1)) [correct]

- ({x}^{2}+1)\operatorname{ln}⁡({x}^{2}+1)

- 2x\operatorname{ln}⁡({x}^{2}+1)

- \frac{2x}{\operatorname{ln}⁡({x}^{2}+1)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{2xy}{{x}^{2}+1},\,\frac{∂f}{∂y}=\operatorname{ln}⁡({x}^{2}+1)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{2x({x}^{2}+1)}{{x}^{2}+1}=2x, \\ \frac{∂f}{∂y} & =\operatorname{ln}⁡({x}^{2}+1).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2x+\operatorname{ln}⁡({x}^{2}+1)\cdot 2x \\  & =2x(1+\operatorname{ln}⁡({x}^{2}+1)).\end{aligned}
$$


## Generated normal y_log_power a=2

If $f(x,y)=2\cdot \left(y\operatorname{ln}⁡({x}^{2}+1)\right)$ and $y={x}^{2}+1,$ compute $\frac{\text{d}f}{\text{d}x}.$

- - 4 x \ln{\left(x^{2} + 1 \right)} + 4 x

- 4 x

- 4 x \ln{\left(x^{2} + 1 \right)} + 4 x [correct]

- 4 x + 2 \left(x^{2} + 1\right) \ln{\left(x^{2} + 1 \right)}

- 4 x + 2 \ln{\left(x^{2} + 1 \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left(\frac{2xy}{{x}^{2}+1}\right),\,\frac{∂f}{∂y}=2\cdot \left(\operatorname{ln}⁡({x}^{2}+1)\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left(\frac{2x({x}^{2}+1)}{{x}^{2}+1}\right)=2\cdot \left(2x\right), \\ \frac{∂f}{∂y} & =2\cdot \left(\operatorname{ln}⁡({x}^{2}+1)\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left(2x+\operatorname{ln}⁡({x}^{2}+1)\cdot 2x\right) \\  & =2\cdot \left(2x(1+\operatorname{ln}⁡({x}^{2}+1))\right).\end{aligned}
$$


## Generated normal y_log_power a=-3

If $f(x,y)=-3\cdot \left(y\operatorname{ln}⁡({x}^{2}+1)\right)$ and $y={x}^{2}+1,$ compute $\frac{\text{d}f}{\text{d}x}.$

- 6 x \ln{\left(x^{2} + 1 \right)} - 6 x

- - 6 x

- - 6 x \ln{\left(x^{2} + 1 \right)} - 6 x [correct]

- - 6 x - 3 \left(x^{2} + 1\right) \ln{\left(x^{2} + 1 \right)}

- - 6 x - 3 \ln{\left(x^{2} + 1 \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left(\frac{2xy}{{x}^{2}+1}\right),\,\frac{∂f}{∂y}=-3\cdot \left(\operatorname{ln}⁡({x}^{2}+1)\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left(\frac{2x({x}^{2}+1)}{{x}^{2}+1}\right)=-3\cdot \left(2x\right), \\ \frac{∂f}{∂y} & =-3\cdot \left(\operatorname{ln}⁡({x}^{2}+1)\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left(2x+\operatorname{ln}⁡({x}^{2}+1)\cdot 2x\right) \\  & =-3\cdot \left(2x(1+\operatorname{ln}⁡({x}^{2}+1))\right).\end{aligned}
$$


## Raw source replay q-95088

If $f(x,y)=\frac{1}{x+y}$ and $y={e}^{-x},$ compute $\frac{\text{d}f}{\text{d}x}.$

- \frac{1-2{e}^{-x}}{(x+{e}^{-x})^{2}}

- \frac{1-{e}^{-x}}{1+x{e}^{-x}}

- \frac{2}{(x+{e}^{-x})^{2}}

- \frac{{e}^{-x}}{1+x{e}^{-x}}

- \frac{-1+{e}^{-x}}{(x+{e}^{-x})^{2}} [correct]

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-\frac{1}{(x+y)^{2}},\,\frac{∂f}{∂y}=-\frac{1}{(x+y)^{2}}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂f}{∂y}=-\frac{1}{(x+{e}^{-x})^{2}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-{e}^{-x}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-\frac{1}{(x+{e}^{-x})^{2}}-\frac{1}{(x+{e}^{-x})^{2}}\cdot (-{e}^{-x}) \\  & =-\frac{1}{(x+{e}^{-x})^{2}}+\frac{{e}^{-x}}{(x+{e}^{-x})^{2}} \\  & =\frac{-1+{e}^{-x}}{(x+{e}^{-x})^{2}}.\end{aligned}
$$


## Generated normal reciprocal_exp a=2

If $f(x,y)=2\cdot \left(\frac{1}{x+y}\right)$ and $y={e}^{-x},$ compute $\frac{\text{d}f}{\text{d}x}.$

- - \frac{2}{\left(x + e^{- x}\right)^{2}} - \frac{2 e^{- x}}{\left(x + e^{- x}\right)^{2}}

- - \frac{2}{\left(x + e^{- x}\right)^{2}}

- - \frac{2}{\left(x + e^{- x}\right)^{2}} + \frac{2 e^{- x}}{\left(x + e^{- x}\right)^{2}} [correct]

- \frac{2 e^{- x}}{\left(x + e^{- x}\right)^{2}}

- - \frac{4}{\left(x + e^{- x}\right)^{2}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left(-\frac{1}{(x+y)^{2}}\right),\,\frac{∂f}{∂y}=2\cdot \left(-\frac{1}{(x+y)^{2}}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left(-\frac{1}{(x+{e}^{-x})^{2}}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-{e}^{-x}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left(-\frac{1}{(x+{e}^{-x})^{2}}-\frac{1}{(x+{e}^{-x})^{2}}\cdot (-{e}^{-x})\right) \\  & =2\cdot \left(-\frac{1}{(x+{e}^{-x})^{2}}+\frac{{e}^{-x}}{(x+{e}^{-x})^{2}}\right) \\  & =2\cdot \left(\frac{-1+{e}^{-x}}{(x+{e}^{-x})^{2}}\right).\end{aligned}
$$


## Generated normal reciprocal_exp a=-3

If $f(x,y)=-3\cdot \left(\frac{1}{x+y}\right)$ and $y={e}^{-x},$ compute $\frac{\text{d}f}{\text{d}x}.$

- \frac{3}{\left(x + e^{- x}\right)^{2}} + \frac{3 e^{- x}}{\left(x + e^{- x}\right)^{2}}

- \frac{3}{\left(x + e^{- x}\right)^{2}}

- \frac{3}{\left(x + e^{- x}\right)^{2}} - \frac{3 e^{- x}}{\left(x + e^{- x}\right)^{2}} [correct]

- - \frac{3 e^{- x}}{\left(x + e^{- x}\right)^{2}}

- \frac{6}{\left(x + e^{- x}\right)^{2}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left(-\frac{1}{(x+y)^{2}}\right),\,\frac{∂f}{∂y}=-3\cdot \left(-\frac{1}{(x+y)^{2}}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left(-\frac{1}{(x+{e}^{-x})^{2}}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-{e}^{-x}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left(-\frac{1}{(x+{e}^{-x})^{2}}-\frac{1}{(x+{e}^{-x})^{2}}\cdot (-{e}^{-x})\right) \\  & =-3\cdot \left(-\frac{1}{(x+{e}^{-x})^{2}}+\frac{{e}^{-x}}{(x+{e}^{-x})^{2}}\right) \\  & =-3\cdot \left(\frac{-1+{e}^{-x}}{(x+{e}^{-x})^{2}}\right).\end{aligned}
$$


## Raw source replay q-95114

If $f(x,y)=\sqrt{{x}^{2}+{y}^{2}}$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$

- \frac{3{x}^{4}}{\sqrt{1+{x}^{4}}}

- \frac{1+{x}^{2}}{\sqrt{1+{x}^{4}}}

- \frac{3{x}^{2}}{\sqrt{1+{x}^{4}}}

- \frac{1+3{x}^{4}}{\sqrt{1+{x}^{4}}} [correct]

- \frac{1+3{x}^{3}}{x\sqrt{1+{x}^{4}}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{x}{\sqrt{{x}^{2}+{y}^{2}}},\,\frac{∂f}{∂y}=\frac{y}{\sqrt{{x}^{2}+{y}^{2}}}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{x}{\sqrt{{x}^{2}+{x}^{6}}} \\  & =\frac{x}{\sqrt{{x}^{2}(1+{x}^{4})}} \\  & =\frac{x}{x\sqrt{1+{x}^{4}}} \\  & =\frac{1}{\sqrt{1+{x}^{4}}}, \\ \frac{∂f}{∂y} & =\frac{{x}^{3}}{\sqrt{{x}^{2}+{x}^{6}}} \\  & =\frac{{x}^{3}}{\sqrt{{x}^{2}(1+{x}^{4})}} \\  & =\frac{{x}^{3}}{x\sqrt{1+{x}^{4}}} \\  & =\frac{{x}^{2}}{\sqrt{1+{x}^{4}}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{1}{\sqrt{1+{x}^{4}}}+\frac{{x}^{2}}{\sqrt{1+{x}^{4}}}\cdot 3{x}^{2} \\  & =\frac{1}{\sqrt{1+{x}^{4}}}+\frac{3{x}^{4}}{\sqrt{1+{x}^{4}}} \\  & =\frac{1+3{x}^{4}}{\sqrt{1+{x}^{4}}}.\end{aligned}
$$


## Generated normal radial_power a=2

If $f(x,y)=2\cdot \left(\sqrt{{x}^{2}+{y}^{2}}\right)$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$ Assume $x>0.$

- \frac{2 \left(1 - 3 x^{4}\right)}{\sqrt{x^{4} + 1}}

- \frac{2}{\sqrt{x^{4} + 1}}

- \frac{2 \left(3 x^{4} + 1\right)}{\sqrt{x^{4} + 1}} [correct]

- \frac{2 \left(x^{5} + 1\right)}{\sqrt{x^{4} + 1}}

- \frac{2 \left(x^{2} + 1\right)}{\sqrt{x^{4} + 1}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left(\frac{x}{\sqrt{{x}^{2}+{y}^{2}}}\right),\,\frac{∂f}{∂y}=2\cdot \left(\frac{y}{\sqrt{{x}^{2}+{y}^{2}}}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left(\frac{x}{\sqrt{{x}^{2}+{x}^{6}}}\right) \\  & =2\cdot \left(\frac{x}{\sqrt{{x}^{2}(1+{x}^{4})}}\right) \\  & =2\cdot \left(\frac{x}{x\sqrt{1+{x}^{4}}}\right) \\  & =2\cdot \left(\frac{1}{\sqrt{1+{x}^{4}}}\right), \\ \frac{∂f}{∂y} & =2\cdot \left(\frac{{x}^{3}}{\sqrt{{x}^{2}+{x}^{6}}}\right) \\  & =2\cdot \left(\frac{{x}^{3}}{\sqrt{{x}^{2}(1+{x}^{4})}}\right) \\  & =2\cdot \left(\frac{{x}^{3}}{x\sqrt{1+{x}^{4}}}\right) \\  & =2\cdot \left(\frac{{x}^{2}}{\sqrt{1+{x}^{4}}}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left(\frac{1}{\sqrt{1+{x}^{4}}}+\frac{{x}^{2}}{\sqrt{1+{x}^{4}}}\cdot 3{x}^{2}\right) \\  & =2\cdot \left(\frac{1}{\sqrt{1+{x}^{4}}}+\frac{3{x}^{4}}{\sqrt{1+{x}^{4}}}\right) \\  & =2\cdot \left(\frac{1+3{x}^{4}}{\sqrt{1+{x}^{4}}}\right).\end{aligned}
$$


## Generated normal radial_power a=-3

If $f(x,y)=-3\cdot \left(\sqrt{{x}^{2}+{y}^{2}}\right)$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$ Assume $x>0.$

- \frac{3 \left(3 x^{4} - 1\right)}{\sqrt{x^{4} + 1}}

- - \frac{3}{\sqrt{x^{4} + 1}}

- \frac{3 \left(- 3 x^{4} - 1\right)}{\sqrt{x^{4} + 1}} [correct]

- \frac{3 \left(- x^{5} - 1\right)}{\sqrt{x^{4} + 1}}

- \frac{3 \left(- x^{2} - 1\right)}{\sqrt{x^{4} + 1}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left(\frac{x}{\sqrt{{x}^{2}+{y}^{2}}}\right),\,\frac{∂f}{∂y}=-3\cdot \left(\frac{y}{\sqrt{{x}^{2}+{y}^{2}}}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left(\frac{x}{\sqrt{{x}^{2}+{x}^{6}}}\right) \\  & =-3\cdot \left(\frac{x}{\sqrt{{x}^{2}(1+{x}^{4})}}\right) \\  & =-3\cdot \left(\frac{x}{x\sqrt{1+{x}^{4}}}\right) \\  & =-3\cdot \left(\frac{1}{\sqrt{1+{x}^{4}}}\right), \\ \frac{∂f}{∂y} & =-3\cdot \left(\frac{{x}^{3}}{\sqrt{{x}^{2}+{x}^{6}}}\right) \\  & =-3\cdot \left(\frac{{x}^{3}}{\sqrt{{x}^{2}(1+{x}^{4})}}\right) \\  & =-3\cdot \left(\frac{{x}^{3}}{x\sqrt{1+{x}^{4}}}\right) \\  & =-3\cdot \left(\frac{{x}^{2}}{\sqrt{1+{x}^{4}}}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left(\frac{1}{\sqrt{1+{x}^{4}}}+\frac{{x}^{2}}{\sqrt{1+{x}^{4}}}\cdot 3{x}^{2}\right) \\  & =-3\cdot \left(\frac{1}{\sqrt{1+{x}^{4}}}+\frac{3{x}^{4}}{\sqrt{1+{x}^{4}}}\right) \\  & =-3\cdot \left(\frac{1+3{x}^{4}}{\sqrt{1+{x}^{4}}}\right).\end{aligned}
$$


## Raw source replay q-95117

If $f(x,y)=x{e}^{y}$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$

- {e}^{\operatorname{sin}⁡x}(1+x\operatorname{cos}⁡x) [correct]

- {e}^{\operatorname{cos}⁡x}(1+\operatorname{sin}⁡x)

- {e}^{\operatorname{sin}⁡x}(1-\operatorname{cos}⁡x)

- {e}^{\operatorname{cos}⁡x}(1-x\operatorname{sin}⁡x)

- {e}^{\operatorname{sin}⁡x}(1+x\operatorname{sin}⁡x)

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}={e}^{y},\,\frac{∂f}{∂y}=x{e}^{y}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & ={e}^{\operatorname{sin}⁡x}, \\ \frac{∂f}{∂y} & =x{e}^{\operatorname{sin}⁡x}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & ={e}^{\operatorname{sin}⁡x}+x{e}^{\operatorname{sin}⁡x}\cdot \operatorname{cos}⁡x \\  & ={e}^{\operatorname{sin}⁡x}(1+x\operatorname{cos}⁡x).\end{aligned}
$$


## Generated normal x_exp_sine a=2

If $f(x,y)=2\cdot \left(x{e}^{y}\right)$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$

- - 2 x e^{\sin{\left(x \right)}} \cos{\left(x \right)} + 2 e^{\sin{\left(x \right)}}

- 2 e^{\sin{\left(x \right)}}

- 2 x e^{\sin{\left(x \right)}} \cos{\left(x \right)} + 2 e^{\sin{\left(x \right)}} [correct]

- 2 x e^{\sin{\left(x \right)}} \sin{\left(x \right)} + 2 e^{\sin{\left(x \right)}}

- 2 x e^{\sin{\left(x \right)}} + 2 e^{\sin{\left(x \right)}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left({e}^{y}\right),\,\frac{∂f}{∂y}=2\cdot \left(x{e}^{y}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left({e}^{\operatorname{sin}⁡x}\right), \\ \frac{∂f}{∂y} & =2\cdot \left(x{e}^{\operatorname{sin}⁡x}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left({e}^{\operatorname{sin}⁡x}+x{e}^{\operatorname{sin}⁡x}\cdot \operatorname{cos}⁡x\right) \\  & =2\cdot \left({e}^{\operatorname{sin}⁡x}(1+x\operatorname{cos}⁡x)\right).\end{aligned}
$$


## Generated normal x_exp_sine a=-3

If $f(x,y)=-3\cdot \left(x{e}^{y}\right)$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$

- 3 x e^{\sin{\left(x \right)}} \cos{\left(x \right)} - 3 e^{\sin{\left(x \right)}}

- - 3 e^{\sin{\left(x \right)}}

- - 3 x e^{\sin{\left(x \right)}} \cos{\left(x \right)} - 3 e^{\sin{\left(x \right)}} [correct]

- - 3 x e^{\sin{\left(x \right)}} \sin{\left(x \right)} - 3 e^{\sin{\left(x \right)}}

- - 3 x e^{\sin{\left(x \right)}} - 3 e^{\sin{\left(x \right)}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left({e}^{y}\right),\,\frac{∂f}{∂y}=-3\cdot \left(x{e}^{y}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left({e}^{\operatorname{sin}⁡x}\right), \\ \frac{∂f}{∂y} & =-3\cdot \left(x{e}^{\operatorname{sin}⁡x}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left({e}^{\operatorname{sin}⁡x}+x{e}^{\operatorname{sin}⁡x}\cdot \operatorname{cos}⁡x\right) \\  & =-3\cdot \left({e}^{\operatorname{sin}⁡x}(1+x\operatorname{cos}⁡x)\right).\end{aligned}
$$


## Raw source replay q-95118

If $f(x,y)={x}^{2}+yx$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$

- 2x+\operatorname{sin}⁡x+\operatorname{cos}⁡x

- 2x+\operatorname{sin}⁡x-2\operatorname{sin}⁡x

- 2x+\operatorname{sin}⁡x+x\operatorname{cos}⁡x [correct]

- 2x+x\operatorname{sin}⁡x

- 2x+\operatorname{sin}⁡x+\operatorname{cos}⁡x\operatorname{sin}⁡x

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x+y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2x+\operatorname{sin}⁡x \\ \frac{∂f}{∂y} & =x.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2x+\operatorname{sin}⁡x+x\operatorname{cos}⁡x.\end{aligned}
$$


## Generated normal polynomial_sine a=2

If $f(x,y)=2\cdot \left({x}^{2}+yx\right)$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$

- - 2 x \cos{\left(x \right)} + 4 x + 2 \sin{\left(x \right)}

- 4 x + 2 \sin{\left(x \right)}

- 2 x \cos{\left(x \right)} + 4 x + 2 \sin{\left(x \right)} [correct]

- 2 x \sin{\left(x \right)} + 4 x + 2 \sin{\left(x \right)}

- 6 x + 2 \sin{\left(x \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left(2x+y\right),\,\frac{∂f}{∂y}=2\cdot \left(x\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left(2x+\operatorname{sin}⁡x\right) \\ \frac{∂f}{∂y} & =2\cdot \left(x\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left(2x+\operatorname{sin}⁡x+x\operatorname{cos}⁡x\right).\end{aligned}
$$


## Generated normal polynomial_sine a=-3

If $f(x,y)=-3\cdot \left({x}^{2}+yx\right)$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$

- 3 x \cos{\left(x \right)} - 6 x - 3 \sin{\left(x \right)}

- - 6 x - 3 \sin{\left(x \right)}

- - 3 x \cos{\left(x \right)} - 6 x - 3 \sin{\left(x \right)} [correct]

- - 3 x \sin{\left(x \right)} - 6 x - 3 \sin{\left(x \right)}

- - 9 x - 3 \sin{\left(x \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left(2x+y\right),\,\frac{∂f}{∂y}=-3\cdot \left(x\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left(2x+\operatorname{sin}⁡x\right) \\ \frac{∂f}{∂y} & =-3\cdot \left(x\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left(2x+\operatorname{sin}⁡x+x\operatorname{cos}⁡x\right).\end{aligned}
$$


## Raw source replay q-95119

If $f(x,y)=\operatorname{cos}⁡({x}^{2}+y)$ and $y=\frac{1}{x},$ compute $\frac{\text{d}f}{\text{d}x}.$

- (1-3{x}^{3})\operatorname{sin}⁡(\frac{{x}^{2}+1}{{x}^{2}})

- (\frac{1-4{x}^{3}}{x})\operatorname{cos}⁡(\frac{{x}^{3}+1}{{x}^{2}})

- (1+4{x}^{2})\operatorname{cos}⁡(\frac{{x}^{2}-1}{x})

- (\frac{2{x}^{2}+1}{x})\operatorname{sin}⁡(\frac{{x}^{3}+1}{x})

- (\frac{1-2{x}^{3}}{{x}^{2}})\operatorname{sin}⁡(\frac{{x}^{3}+1}{x}) [correct]

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-2x\operatorname{sin}⁡({x}^{2}+y),\,\frac{∂f}{∂y}=-\operatorname{sin}⁡({x}^{2}+y)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-2x\operatorname{sin}⁡({x}^{2}+\frac{1}{x}), \\ \frac{∂f}{∂y} & =-\operatorname{sin}⁡({x}^{2}+\frac{1}{x}).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{1}{{x}^{2}}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-2x\operatorname{sin}⁡({x}^{2}+\frac{1}{x})+(-\operatorname{sin}⁡({x}^{2}+\frac{1}{x}))\cdot (-\frac{1}{{x}^{2}}) \\  & =(\frac{1}{{x}^{2}}-2x)\operatorname{sin}⁡({x}^{2}+\frac{1}{x}) \\  & =(\frac{1-2{x}^{3}}{{x}^{2}})\operatorname{sin}⁡(\frac{{x}^{3}+1}{x}).\end{aligned}
$$


## Generated normal cosine_reciprocal a=2

If $f(x,y)=2\cdot \left(\operatorname{cos}⁡({x}^{2}+y)\right)$ and $y=\frac{1}{x},$ compute $\frac{\text{d}f}{\text{d}x}.$

- - 4 x \sin{\left(x^{2} + \frac{1}{x} \right)} - \frac{2 \sin{\left(x^{2} + \frac{1}{x} \right)}}{x^{2}}

- - 4 x \sin{\left(x^{2} + \frac{1}{x} \right)}

- - 4 x \sin{\left(x^{2} + \frac{1}{x} \right)} + \frac{2 \sin{\left(x^{2} + \frac{1}{x} \right)}}{x^{2}} [correct]

- - 4 x \sin{\left(x^{2} + \frac{1}{x} \right)} - \frac{2 \sin{\left(x^{2} + \frac{1}{x} \right)}}{x}

- - 4 x \sin{\left(x^{2} + \frac{1}{x} \right)} - 2 \sin{\left(x^{2} + \frac{1}{x} \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left(-2x\operatorname{sin}⁡({x}^{2}+y)\right),\,\frac{∂f}{∂y}=2\cdot \left(-\operatorname{sin}⁡({x}^{2}+y)\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left(-2x\operatorname{sin}⁡({x}^{2}+\frac{1}{x})\right), \\ \frac{∂f}{∂y} & =2\cdot \left(-\operatorname{sin}⁡({x}^{2}+\frac{1}{x})\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{1}{{x}^{2}}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left(-2x\operatorname{sin}⁡({x}^{2}+\frac{1}{x})+(-\operatorname{sin}⁡({x}^{2}+\frac{1}{x}))\cdot (-\frac{1}{{x}^{2}})\right) \\  & =2\cdot \left((\frac{1}{{x}^{2}}-2x)\operatorname{sin}⁡({x}^{2}+\frac{1}{x})\right) \\  & =2\cdot \left((\frac{1-2{x}^{3}}{{x}^{2}})\operatorname{sin}⁡(\frac{{x}^{3}+1}{x})\right).\end{aligned}
$$


## Generated normal cosine_reciprocal a=-3

If $f(x,y)=-3\cdot \left(\operatorname{cos}⁡({x}^{2}+y)\right)$ and $y=\frac{1}{x},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 6 x \sin{\left(x^{2} + \frac{1}{x} \right)} + \frac{3 \sin{\left(x^{2} + \frac{1}{x} \right)}}{x^{2}}

- 6 x \sin{\left(x^{2} + \frac{1}{x} \right)}

- 6 x \sin{\left(x^{2} + \frac{1}{x} \right)} - \frac{3 \sin{\left(x^{2} + \frac{1}{x} \right)}}{x^{2}} [correct]

- 6 x \sin{\left(x^{2} + \frac{1}{x} \right)} + \frac{3 \sin{\left(x^{2} + \frac{1}{x} \right)}}{x}

- 6 x \sin{\left(x^{2} + \frac{1}{x} \right)} + 3 \sin{\left(x^{2} + \frac{1}{x} \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left(-2x\operatorname{sin}⁡({x}^{2}+y)\right),\,\frac{∂f}{∂y}=-3\cdot \left(-\operatorname{sin}⁡({x}^{2}+y)\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left(-2x\operatorname{sin}⁡({x}^{2}+\frac{1}{x})\right), \\ \frac{∂f}{∂y} & =-3\cdot \left(-\operatorname{sin}⁡({x}^{2}+\frac{1}{x})\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{1}{{x}^{2}}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left(-2x\operatorname{sin}⁡({x}^{2}+\frac{1}{x})+(-\operatorname{sin}⁡({x}^{2}+\frac{1}{x}))\cdot (-\frac{1}{{x}^{2}})\right) \\  & =-3\cdot \left((\frac{1}{{x}^{2}}-2x)\operatorname{sin}⁡({x}^{2}+\frac{1}{x})\right) \\  & =-3\cdot \left((\frac{1-2{x}^{3}}{{x}^{2}})\operatorname{sin}⁡(\frac{{x}^{3}+1}{x})\right).\end{aligned}
$$


## Raw source replay q-95122

If $f(x,y)=\frac{y}{x+1}$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$

- \frac{x(3x+4)}{(x+1)^{2}}

- \frac{{x}^{2}(3{x}^{2}-1)}{(x+1)^{2}}

- \frac{4{x}^{2}(x-6)}{x+1}

- \frac{{x}^{2}(2x+3)}{(x+1)^{2}} [correct]

- \frac{x(4x-3)}{x+1}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-\frac{y}{(x+1)^{2}},\,\frac{∂f}{∂y}=\frac{1}{x+1}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-\frac{{x}^{3}}{(x+1)^{2}}, \\ \frac{∂f}{∂y} & =\frac{1}{x+1}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-\frac{{x}^{3}}{(x+1)^{2}}+\frac{1}{x+1}\cdot 3{x}^{2} \\  & =\frac{3{x}^{2}}{x+1}-\frac{{x}^{3}}{(x+1)^{2}} \\  & =\frac{3{x}^{2}(x+1)-{x}^{3}}{(x+1)^{2}} \\  & =\frac{3{x}^{3}+3{x}^{2}-{x}^{3}}{(x+1)^{2}} \\  & =\frac{{x}^{2}(2x+3)}{(x+1)^{2}}.\end{aligned}
$$


## Generated normal quotient_power a=2

If $f(x,y)=2\cdot \left(\frac{y}{x+1}\right)$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$

- - \frac{2 x^{3}}{\left(x + 1\right)^{2}} - \frac{6 x^{2}}{x + 1}

- - \frac{2 x^{3}}{\left(x + 1\right)^{2}}

- - \frac{2 x^{3}}{\left(x + 1\right)^{2}} + \frac{6 x^{2}}{x + 1} [correct]

- \frac{2 x^{3}}{x + 1} - \frac{2 x^{3}}{\left(x + 1\right)^{2}}

- - \frac{2 x^{3}}{\left(x + 1\right)^{2}} + \frac{2}{x + 1}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2\cdot \left(-\frac{y}{(x+1)^{2}}\right),\,\frac{∂f}{∂y}=2\cdot \left(\frac{1}{x+1}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\cdot \left(-\frac{{x}^{3}}{(x+1)^{2}}\right), \\ \frac{∂f}{∂y} & =2\cdot \left(\frac{1}{x+1}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2\cdot \left(-\frac{{x}^{3}}{(x+1)^{2}}+\frac{1}{x+1}\cdot 3{x}^{2}\right) \\  & =2\cdot \left(\frac{3{x}^{2}}{x+1}-\frac{{x}^{3}}{(x+1)^{2}}\right) \\  & =2\cdot \left(\frac{3{x}^{2}(x+1)-{x}^{3}}{(x+1)^{2}}\right) \\  & =2\cdot \left(\frac{3{x}^{3}+3{x}^{2}-{x}^{3}}{(x+1)^{2}}\right) \\  & =2\cdot \left(\frac{{x}^{2}(2x+3)}{(x+1)^{2}}\right).\end{aligned}
$$


## Generated normal quotient_power a=-3

If $f(x,y)=-3\cdot \left(\frac{y}{x+1}\right)$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$

- \frac{3 x^{3}}{\left(x + 1\right)^{2}} + \frac{9 x^{2}}{x + 1}

- \frac{3 x^{3}}{\left(x + 1\right)^{2}}

- \frac{3 x^{3}}{\left(x + 1\right)^{2}} - \frac{9 x^{2}}{x + 1} [correct]

- - \frac{3 x^{3}}{x + 1} + \frac{3 x^{3}}{\left(x + 1\right)^{2}}

- \frac{3 x^{3}}{\left(x + 1\right)^{2}} - \frac{3}{x + 1}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-3\cdot \left(-\frac{y}{(x+1)^{2}}\right),\,\frac{∂f}{∂y}=-3\cdot \left(\frac{1}{x+1}\right)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-3\cdot \left(-\frac{{x}^{3}}{(x+1)^{2}}\right), \\ \frac{∂f}{∂y} & =-3\cdot \left(\frac{1}{x+1}\right).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-3\cdot \left(-\frac{{x}^{3}}{(x+1)^{2}}+\frac{1}{x+1}\cdot 3{x}^{2}\right) \\  & =-3\cdot \left(\frac{3{x}^{2}}{x+1}-\frac{{x}^{3}}{(x+1)^{2}}\right) \\  & =-3\cdot \left(\frac{3{x}^{2}(x+1)-{x}^{3}}{(x+1)^{2}}\right) \\  & =-3\cdot \left(\frac{3{x}^{3}+3{x}^{2}-{x}^{3}}{(x+1)^{2}}\right) \\  & =-3\cdot \left(\frac{{x}^{2}(2x+3)}{(x+1)^{2}}\right).\end{aligned}
$$


## Authored missing-level weighted_polynomial_sine

If $f(x,y)=2 x^{2} - 3 x y$ and $y=2 \sin{\left(2 x \right)},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 12 x \cos{\left(2 x \right)} + 4 x - 6 \sin{\left(2 x \right)}

- 4 x - 6 \sin{\left(2 x \right)}

- - 12 x \cos{\left(2 x \right)} + 4 x - 6 \sin{\left(2 x \right)} [correct]

- - 6 x \sin{\left(2 x \right)} + 4 x - 6 \sin{\left(2 x \right)}

- x - 6 \sin{\left(2 x \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=4 x - 3 y,\,\frac{∂f}{∂y}=- 3 x\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4 x - 6 \sin{\left(2 x \right)}, \\ \frac{∂f}{∂y} & =- 3 x.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 \cos{\left(2 x \right)}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =4 x - 6 \sin{\left(2 x \right)}+\left(- 3 x\right)\cdot \left(4 \cos{\left(2 x \right)}\right) \\  & =- 12 x \cos{\left(2 x \right)} + 4 x - 6 \sin{\left(2 x \right)} \\  & =- 2 \left(6 x \cos{\left(2 x \right)} - 2 x + 3 \sin{\left(2 x \right)}\right).\end{aligned}
$$


## Authored missing-level weighted_polynomial_sine

If $f(x,y)=- 4 x^{2} + 4 x y$ and $y=- 4 \sin{\left(4 x \right)},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 64 x \cos{\left(4 x \right)} - 8 x - 16 \sin{\left(4 x \right)}

- - 8 x - 16 \sin{\left(4 x \right)}

- - 64 x \cos{\left(4 x \right)} - 8 x - 16 \sin{\left(4 x \right)} [correct]

- - 16 x \sin{\left(4 x \right)} - 8 x - 16 \sin{\left(4 x \right)}

- - 4 x - 16 \sin{\left(4 x \right)}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=- 8 x + 4 y,\,\frac{∂f}{∂y}=4 x\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =- 8 x - 16 \sin{\left(4 x \right)}, \\ \frac{∂f}{∂y} & =4 x.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 16 \cos{\left(4 x \right)}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =- 8 x - 16 \sin{\left(4 x \right)}+\left(4 x\right)\cdot \left(- 16 \cos{\left(4 x \right)}\right) \\  & =- 64 x \cos{\left(4 x \right)} - 8 x - 16 \sin{\left(4 x \right)} \\  & =- 8 \left(8 x \cos{\left(4 x \right)} + x + 2 \sin{\left(4 x \right)}\right).\end{aligned}
$$


## Authored missing-level weighted_x_exp_sine

If $f(x,y)=2 x e^{- 3 y}$ and $y=2 \sin{\left(2 x \right)},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 24 x e^{- 6 \sin{\left(2 x \right)}} \cos{\left(2 x \right)} + 2 e^{- 6 \sin{\left(2 x \right)}}

- 2 e^{- 6 \sin{\left(2 x \right)}}

- - 24 x e^{- 6 \sin{\left(2 x \right)}} \cos{\left(2 x \right)} + 2 e^{- 6 \sin{\left(2 x \right)}} [correct]

- - 12 x e^{- 6 \sin{\left(2 x \right)}} \sin{\left(2 x \right)} + 2 e^{- 6 \sin{\left(2 x \right)}}

- - 6 x e^{- 6 \sin{\left(2 x \right)}} + 2 e^{- 6 \sin{\left(2 x \right)}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2 e^{- 3 y},\,\frac{∂f}{∂y}=- 6 x e^{- 3 y}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2 e^{- 6 \sin{\left(2 x \right)}}, \\ \frac{∂f}{∂y} & =- 6 x e^{- 6 \sin{\left(2 x \right)}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 \cos{\left(2 x \right)}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2 e^{- 6 \sin{\left(2 x \right)}}+\left(- 6 x e^{- 6 \sin{\left(2 x \right)}}\right)\cdot \left(4 \cos{\left(2 x \right)}\right) \\  & =- 24 x e^{- 6 \sin{\left(2 x \right)}} \cos{\left(2 x \right)} + 2 e^{- 6 \sin{\left(2 x \right)}} \\  & =- 2 \left(12 x \cos{\left(2 x \right)} - 1\right) e^{- 6 \sin{\left(2 x \right)}}.\end{aligned}
$$


## Authored missing-level weighted_x_exp_sine

If $f(x,y)=- 4 x e^{4 y}$ and $y=- 4 \sin{\left(4 x \right)},$ compute $\frac{\text{d}f}{\text{d}x}.$

- - 256 x e^{- 16 \sin{\left(4 x \right)}} \cos{\left(4 x \right)} - 4 e^{- 16 \sin{\left(4 x \right)}}

- - 4 e^{- 16 \sin{\left(4 x \right)}}

- 256 x e^{- 16 \sin{\left(4 x \right)}} \cos{\left(4 x \right)} - 4 e^{- 16 \sin{\left(4 x \right)}} [correct]

- 64 x e^{- 16 \sin{\left(4 x \right)}} \sin{\left(4 x \right)} - 4 e^{- 16 \sin{\left(4 x \right)}}

- - 16 x e^{- 16 \sin{\left(4 x \right)}} - 4 e^{- 16 \sin{\left(4 x \right)}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=- 4 e^{4 y},\,\frac{∂f}{∂y}=- 16 x e^{4 y}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =- 4 e^{- 16 \sin{\left(4 x \right)}}, \\ \frac{∂f}{∂y} & =- 16 x e^{- 16 \sin{\left(4 x \right)}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 16 \cos{\left(4 x \right)}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =- 4 e^{- 16 \sin{\left(4 x \right)}}+\left(- 16 x e^{- 16 \sin{\left(4 x \right)}}\right)\cdot \left(- 16 \cos{\left(4 x \right)}\right) \\  & =256 x e^{- 16 \sin{\left(4 x \right)}} \cos{\left(4 x \right)} - 4 e^{- 16 \sin{\left(4 x \right)}} \\  & =4 \left(64 x \cos{\left(4 x \right)} - 1\right) e^{- 16 \sin{\left(4 x \right)}}.\end{aligned}
$$


## Authored missing-level polynomial_product_dependency

If $f(x,y)=2 x^{2} - 3 x y$ and $y=2 x \sin{\left(2 x \right)},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 3 x \left(4 x \cos{\left(2 x \right)} + 2 \sin{\left(2 x \right)}\right) - 6 x \sin{\left(2 x \right)} + 4 x

- - 6 x \sin{\left(2 x \right)} + 4 x

- - 3 x \left(4 x \cos{\left(2 x \right)} + 2 \sin{\left(2 x \right)}\right) - 6 x \sin{\left(2 x \right)} + 4 x [correct]

- - 6 x^{2} \sin{\left(2 x \right)} - 6 x \sin{\left(2 x \right)} + 4 x

- - 6 x \sin{\left(2 x \right)} + x

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=4 x - 3 y,\,\frac{∂f}{∂y}=- 3 x\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =- 6 x \sin{\left(2 x \right)} + 4 x, \\ \frac{∂f}{∂y} & =- 3 x.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(2x) & =2, \\ \frac{\text{d}}{\text{d}x}(\sin{\left(2 x \right)}) & =2 \cos{\left(2 x \right)}, \\ \frac{\text{d}y}{\text{d}x} & =2\cdot \left(\sin{\left(2 x \right)}\right)+\left(2x\right)\cdot \left(2 \cos{\left(2 x \right)}\right) \\  & =4 x \cos{\left(2 x \right)} + 2 \sin{\left(2 x \right)}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =- 6 x \sin{\left(2 x \right)} + 4 x+\left(- 3 x\right)\cdot \left(4 x \cos{\left(2 x \right)} + 2 \sin{\left(2 x \right)}\right) \\  & =- 12 x^{2} \cos{\left(2 x \right)} - 12 x \sin{\left(2 x \right)} + 4 x \\  & =- 4 x \left(3 x \cos{\left(2 x \right)} + 3 \sin{\left(2 x \right)} - 1\right).\end{aligned}
$$


## Authored missing-level polynomial_product_dependency

If $f(x,y)=- 4 x^{2} + 4 x y$ and $y=- 4 x \sin{\left(4 x \right)},$ compute $\frac{\text{d}f}{\text{d}x}.$

- - 4 x \left(- 16 x \cos{\left(4 x \right)} - 4 \sin{\left(4 x \right)}\right) - 16 x \sin{\left(4 x \right)} - 8 x

- - 16 x \sin{\left(4 x \right)} - 8 x

- 4 x \left(- 16 x \cos{\left(4 x \right)} - 4 \sin{\left(4 x \right)}\right) - 16 x \sin{\left(4 x \right)} - 8 x [correct]

- - 16 x^{2} \sin{\left(4 x \right)} - 16 x \sin{\left(4 x \right)} - 8 x

- - 16 x \sin{\left(4 x \right)} - 4 x

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=- 8 x + 4 y,\,\frac{∂f}{∂y}=4 x\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =- 16 x \sin{\left(4 x \right)} - 8 x, \\ \frac{∂f}{∂y} & =4 x.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(-4x) & =-4, \\ \frac{\text{d}}{\text{d}x}(\sin{\left(4 x \right)}) & =4 \cos{\left(4 x \right)}, \\ \frac{\text{d}y}{\text{d}x} & =-4\cdot \left(\sin{\left(4 x \right)}\right)+\left(-4x\right)\cdot \left(4 \cos{\left(4 x \right)}\right) \\  & =- 16 x \cos{\left(4 x \right)} - 4 \sin{\left(4 x \right)}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =- 16 x \sin{\left(4 x \right)} - 8 x+\left(4 x\right)\cdot \left(- 16 x \cos{\left(4 x \right)} - 4 \sin{\left(4 x \right)}\right) \\  & =- 64 x^{2} \cos{\left(4 x \right)} - 32 x \sin{\left(4 x \right)} - 8 x \\  & =- 8 x \left(8 x \cos{\left(4 x \right)} + 4 \sin{\left(4 x \right)} + 1\right).\end{aligned}
$$


## Authored missing-level exponential_product_dependency

If $f(x,y)=2 x e^{- 3 y}$ and $y=2 x \cos{\left(2 x \right)},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 6 x \left(- 4 x \sin{\left(2 x \right)} + 2 \cos{\left(2 x \right)}\right) e^{- 6 x \cos{\left(2 x \right)}} + 2 e^{- 6 x \cos{\left(2 x \right)}}

- 2 e^{- 6 x \cos{\left(2 x \right)}}

- - 6 x \left(- 4 x \sin{\left(2 x \right)} + 2 \cos{\left(2 x \right)}\right) e^{- 6 x \cos{\left(2 x \right)}} + 2 e^{- 6 x \cos{\left(2 x \right)}} [correct]

- - 12 x^{2} e^{- 6 x \cos{\left(2 x \right)}} \cos{\left(2 x \right)} + 2 e^{- 6 x \cos{\left(2 x \right)}}

- - 6 x e^{- 6 x \cos{\left(2 x \right)}} + 2 e^{- 6 x \cos{\left(2 x \right)}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2 e^{- 3 y},\,\frac{∂f}{∂y}=- 6 x e^{- 3 y}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2 e^{- 6 x \cos{\left(2 x \right)}}, \\ \frac{∂f}{∂y} & =- 6 x e^{- 6 x \cos{\left(2 x \right)}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(2x) & =2, \\ \frac{\text{d}}{\text{d}x}(\cos{\left(2 x \right)}) & =- 2 \sin{\left(2 x \right)}, \\ \frac{\text{d}y}{\text{d}x} & =2\cdot \left(\cos{\left(2 x \right)}\right)+\left(2x\right)\cdot \left(- 2 \sin{\left(2 x \right)}\right) \\  & =- 4 x \sin{\left(2 x \right)} + 2 \cos{\left(2 x \right)}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2 e^{- 6 x \cos{\left(2 x \right)}}+\left(- 6 x e^{- 6 x \cos{\left(2 x \right)}}\right)\cdot \left(- 4 x \sin{\left(2 x \right)} + 2 \cos{\left(2 x \right)}\right) \\  & =24 x^{2} e^{- 6 x \cos{\left(2 x \right)}} \sin{\left(2 x \right)} - 12 x e^{- 6 x \cos{\left(2 x \right)}} \cos{\left(2 x \right)} + 2 e^{- 6 x \cos{\left(2 x \right)}} \\  & =2 \left(12 x^{2} \sin{\left(2 x \right)} - 6 x \cos{\left(2 x \right)} + 1\right) e^{- 6 x \cos{\left(2 x \right)}}.\end{aligned}
$$


## Authored missing-level exponential_product_dependency

If $f(x,y)=- 4 x e^{4 y}$ and $y=- 4 x \cos{\left(4 x \right)},$ compute $\frac{\text{d}f}{\text{d}x}.$

- 16 x \left(16 x \sin{\left(4 x \right)} - 4 \cos{\left(4 x \right)}\right) e^{- 16 x \cos{\left(4 x \right)}} - 4 e^{- 16 x \cos{\left(4 x \right)}}

- - 4 e^{- 16 x \cos{\left(4 x \right)}}

- - 16 x \left(16 x \sin{\left(4 x \right)} - 4 \cos{\left(4 x \right)}\right) e^{- 16 x \cos{\left(4 x \right)}} - 4 e^{- 16 x \cos{\left(4 x \right)}} [correct]

- 64 x^{2} e^{- 16 x \cos{\left(4 x \right)}} \cos{\left(4 x \right)} - 4 e^{- 16 x \cos{\left(4 x \right)}}

- - 16 x e^{- 16 x \cos{\left(4 x \right)}} - 4 e^{- 16 x \cos{\left(4 x \right)}}

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=- 4 e^{4 y},\,\frac{∂f}{∂y}=- 16 x e^{4 y}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =- 4 e^{- 16 x \cos{\left(4 x \right)}}, \\ \frac{∂f}{∂y} & =- 16 x e^{- 16 x \cos{\left(4 x \right)}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(-4x) & =-4, \\ \frac{\text{d}}{\text{d}x}(\cos{\left(4 x \right)}) & =- 4 \sin{\left(4 x \right)}, \\ \frac{\text{d}y}{\text{d}x} & =-4\cdot \left(\cos{\left(4 x \right)}\right)+\left(-4x\right)\cdot \left(- 4 \sin{\left(4 x \right)}\right) \\  & =16 x \sin{\left(4 x \right)} - 4 \cos{\left(4 x \right)}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =- 4 e^{- 16 x \cos{\left(4 x \right)}}+\left(- 16 x e^{- 16 x \cos{\left(4 x \right)}}\right)\cdot \left(16 x \sin{\left(4 x \right)} - 4 \cos{\left(4 x \right)}\right) \\  & =- 256 x^{2} e^{- 16 x \cos{\left(4 x \right)}} \sin{\left(4 x \right)} + 64 x e^{- 16 x \cos{\left(4 x \right)}} \cos{\left(4 x \right)} - 4 e^{- 16 x \cos{\left(4 x \right)}} \\  & =- 4 \left(64 x^{2} \sin{\left(4 x \right)} - 16 x \cos{\left(4 x \right)} + 1\right) e^{- 16 x \cos{\left(4 x \right)}}.\end{aligned}
$$
