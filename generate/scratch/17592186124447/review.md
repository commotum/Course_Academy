# Source and generated review

Raw originals retain missing fields. Generated examples are explicitly labeled; opaque historical bank variants are evidence only. Metadata is outside learner records.

## Original q-36144 (poly; moderate)

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & =3{x}^{2}-4y,\, &  & ∇g(x,y)=6x\text{ }i-4\text{ }j, &  &  \\ h(x,y) & =2{x}^{2}{y}^{2},\, &  & ∇h(x,y)=4x{y}^{2}\text{ }i+4{x}^{2}y\text{ }j. &  & \end{aligned}
$$

- $(24{x}^{3}{y}^{2}-16x{y}^{3})\text{ }i+(12{x}^{4}y-24{x}^{2}{y}^{2})\text{ }j$
- $-16x{y}^{3}\text{ }i+12{x}^{4}y\text{ }j$
- $(2{x}^{3}{y}^{2}-x{y}^{3})\text{ }i+({x}^{4}y-2{x}^{2}{y}^{2})\text{ }j$
- $24{x}^{3}{y}^{2}-16x{y}^{3}+12{x}^{4}y-24{x}^{2}{y}^{2}$
- $(12{x}^{4}y-24{x}^{2}{y}^{2})\text{ }i+(24{x}^{3}{y}^{2}-16x{y}^{3})\text{ }j$

The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =2{x}^{2}{y}^{2}(6x\text{ }i-4\text{ }j)+(3{x}^{2}-4y)(4x{y}^{2}\text{ }i+4{x}^{2}y\text{ }j) \\  & =(2{x}^{2}{y}^{2}\cdot 6x\text{ }i-2{x}^{2}{y}^{2}\cdot 4\text{ }j)+((3{x}^{2}-4y)\cdot 4x{y}^{2}\text{ }i+(3{x}^{2}-4y)\cdot 4{x}^{2}y\text{ }j) \\  & =12{x}^{3}{y}^{2}\text{ }i-8{x}^{2}{y}^{2}\text{ }j+(12{x}^{3}{y}^{2}-16x{y}^{3})\text{ }i+(12{x}^{4}y-16{x}^{2}{y}^{2})\text{ }j \\  & =(24{x}^{3}{y}^{2}-16x{y}^{3})\text{ }i+(12{x}^{4}y-24{x}^{2}{y}^{2})\text{ }j\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & =3{(x-4)}^{2}-4(y+6),\, &  & ∇g(x,y)=6(x-4)\text{ }i-4\text{ }j, &  &  \\ h(x,y) & =2{(x-4)}^{2}{(y+6)}^{2},\, &  & ∇h(x,y)=4(x-4){(y+6)}^{2}\text{ }i+4{(x-4)}^{2}(y+6)\text{ }j. &  & \end{aligned}
$$

- $(2 \left(x - 4\right)^{2} \left(6 x - 24\right) \left(y + 6\right)^{2})\,i+(- 8 \left(x - 4\right)^{2} \left(y + 6\right)^{2})\,j$
- $(2 \left(x - 4\right)^{2} \left(6 x - 24\right) \left(y + 6\right)^{2} - 2 \left(2 x - 8\right) \left(y + 6\right)^{2} \left(- 4 y + 3 \left(x - 4\right)^{2} - 24\right))\,i+(- 8 \left(x - 4\right)^{2} \left(y + 6\right)^{2} - 2 \left(x - 4\right)^{2} \left(2 y + 12\right) \left(- 4 y + 3 \left(x - 4\right)^{2} - 24\right))\,j$
- $(2 \left(2 x - 8\right) \left(y + 6\right)^{2} \left(- 4 y + 3 \left(x - 4\right)^{2} - 24\right))\,i+(2 \left(x - 4\right)^{2} \left(2 y + 12\right) \left(- 4 y + 3 \left(x - 4\right)^{2} - 24\right))\,j$
- $(8 \left(x - 4\right) \left(y + 6\right)^{2} \left(- 2 y + 3 \left(x - 4\right)^{2} - 12\right))\,i+(12 \left(x - 4\right)^{2} \left(y + 6\right) \left(- 2 y + \left(x - 4\right)^{2} - 12\right))\,j$
- $(12 \left(x - 4\right)^{2} \left(y + 6\right) \left(- 2 y + \left(x - 4\right)^{2} - 12\right))\,i+(8 \left(x - 4\right) \left(y + 6\right)^{2} \left(- 2 y + 3 \left(x - 4\right)^{2} - 12\right))\,j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =2{(x-4)}^{2}{(y+6)}^{2}(6(x-4)\text{ }i-4\text{ }j)+(3{(x-4)}^{2}-4(y+6))(4(x-4){(y+6)}^{2}\text{ }i+4{(x-4)}^{2}(y+6)\text{ }j) \\  & =(2{(x-4)}^{2}{(y+6)}^{2}\cdot 6(x-4)\text{ }i-2{(x-4)}^{2}{(y+6)}^{2}\cdot 4\text{ }j)+((3{(x-4)}^{2}-4(y+6))\cdot 4(x-4){(y+6)}^{2}\text{ }i+(3{(x-4)}^{2}-4(y+6))\cdot 4{(x-4)}^{2}(y+6)\text{ }j) \\  & =12{(x-4)}^{3}{(y+6)}^{2}\text{ }i-8{(x-4)}^{2}{(y+6)}^{2}\text{ }j+(12{(x-4)}^{3}{(y+6)}^{2}-16(x-4){(y+6)}^{3})\text{ }i+(12{(x-4)}^{4}(y+6)-16{(x-4)}^{2}{(y+6)}^{2})\text{ }j \\  & =(24{(x-4)}^{3}{(y+6)}^{2}-16(x-4){(y+6)}^{3})\text{ }i+(12{(x-4)}^{4}(y+6)-24{(x-4)}^{2}{(y+6)}^{2})\text{ }j\end{aligned}
$$

### Generated moderate source:q-36144

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: False.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & =3{(x-4)}^{2}-4(y+6),\, &  & ∇g(x,y)=6(x-4)\text{ }i-4\text{ }j, &  &  \\ h(x,y) & =2{(x-4)}^{2}{(y+6)}^{2},\, &  & ∇h(x,y)=4(x-4){(y+6)}^{2}\text{ }i+4{(x-4)}^{2}(y+6)\text{ }j. &  & \end{aligned}
$$

- $-16(x-4){(y+6)}^{3}\text{ }i+12{(x-4)}^{4}(y+6)\text{ }j$
- $24{(x-4)}^{3}{(y+6)}^{2}-16(x-4){(y+6)}^{3}+12{(x-4)}^{4}(y+6)-24{(x-4)}^{2}{(y+6)}^{2}$
- $(2{(x-4)}^{3}{(y+6)}^{2}-(x-4){(y+6)}^{3})\text{ }i+({(x-4)}^{4}(y+6)-2{(x-4)}^{2}{(y+6)}^{2})\text{ }j$
- $(12{(x-4)}^{4}(y+6)-24{(x-4)}^{2}{(y+6)}^{2})\text{ }i+(24{(x-4)}^{3}{(y+6)}^{2}-16(x-4){(y+6)}^{3})\text{ }j$
- $(24{(x-4)}^{3}{(y+6)}^{2}-16(x-4){(y+6)}^{3})\text{ }i+(12{(x-4)}^{4}(y+6)-24{(x-4)}^{2}{(y+6)}^{2})\text{ }j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =2{(x-4)}^{2}{(y+6)}^{2}(6(x-4)\text{ }i-4\text{ }j)+(3{(x-4)}^{2}-4(y+6))(4(x-4){(y+6)}^{2}\text{ }i+4{(x-4)}^{2}(y+6)\text{ }j) \\  & =(2{(x-4)}^{2}{(y+6)}^{2}\cdot 6(x-4)\text{ }i-2{(x-4)}^{2}{(y+6)}^{2}\cdot 4\text{ }j)+((3{(x-4)}^{2}-4(y+6))\cdot 4(x-4){(y+6)}^{2}\text{ }i+(3{(x-4)}^{2}-4(y+6))\cdot 4{(x-4)}^{2}(y+6)\text{ }j) \\  & =12{(x-4)}^{3}{(y+6)}^{2}\text{ }i-8{(x-4)}^{2}{(y+6)}^{2}\text{ }j+(12{(x-4)}^{3}{(y+6)}^{2}-16(x-4){(y+6)}^{3})\text{ }i+(12{(x-4)}^{4}(y+6)-16{(x-4)}^{2}{(y+6)}^{2})\text{ }j \\  & =(24{(x-4)}^{3}{(y+6)}^{2}-16(x-4){(y+6)}^{3})\text{ }i+(12{(x-4)}^{4}(y+6)-24{(x-4)}^{2}{(y+6)}^{2})\text{ }j\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: True.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & =3{(x-4)}^{2}-4(y+5),\, &  & ∇g(x,y)=6(x-4)\text{ }i-4\text{ }j, &  &  \\ h(x,y) & =2{(x-4)}^{2}{(y+5)}^{2},\, &  & ∇h(x,y)=4(x-4){(y+5)}^{2}\text{ }i+4{(x-4)}^{2}(y+5)\text{ }j. &  & \end{aligned}
$$

- $(2 \left(x - 4\right)^{2} \left(6 x - 24\right) \left(y + 5\right)^{2})\,i+(- 8 \left(x - 4\right)^{2} \left(y + 5\right)^{2})\,j$
- $(2 \left(x - 4\right)^{2} \left(6 x - 24\right) \left(y + 5\right)^{2} - 2 \left(2 x - 8\right) \left(y + 5\right)^{2} \left(- 4 y + 3 \left(x - 4\right)^{2} - 20\right))\,i+(- 8 \left(x - 4\right)^{2} \left(y + 5\right)^{2} - 2 \left(x - 4\right)^{2} \left(2 y + 10\right) \left(- 4 y + 3 \left(x - 4\right)^{2} - 20\right))\,j$
- $(12 \left(x - 4\right)^{2} \left(y + 5\right) \left(- 2 y + \left(x - 4\right)^{2} - 10\right))\,i+(8 \left(x - 4\right) \left(y + 5\right)^{2} \left(- 2 y + 3 \left(x - 4\right)^{2} - 10\right))\,j$
- $(2 \left(2 x - 8\right) \left(y + 5\right)^{2} \left(- 4 y + 3 \left(x - 4\right)^{2} - 20\right))\,i+(2 \left(x - 4\right)^{2} \left(2 y + 10\right) \left(- 4 y + 3 \left(x - 4\right)^{2} - 20\right))\,j$
- $(8 \left(x - 4\right) \left(y + 5\right)^{2} \left(- 2 y + 3 \left(x - 4\right)^{2} - 10\right))\,i+(12 \left(x - 4\right)^{2} \left(y + 5\right) \left(- 2 y + \left(x - 4\right)^{2} - 10\right))\,j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =2{(x-4)}^{2}{(y+5)}^{2}(6(x-4)\text{ }i-4\text{ }j)+(3{(x-4)}^{2}-4(y+5))(4(x-4){(y+5)}^{2}\text{ }i+4{(x-4)}^{2}(y+5)\text{ }j) \\  & =(2{(x-4)}^{2}{(y+5)}^{2}\cdot 6(x-4)\text{ }i-2{(x-4)}^{2}{(y+5)}^{2}\cdot 4\text{ }j)+((3{(x-4)}^{2}-4(y+5))\cdot 4(x-4){(y+5)}^{2}\text{ }i+(3{(x-4)}^{2}-4(y+5))\cdot 4{(x-4)}^{2}(y+5)\text{ }j) \\  & =12{(x-4)}^{3}{(y+5)}^{2}\text{ }i-8{(x-4)}^{2}{(y+5)}^{2}\text{ }j+(12{(x-4)}^{3}{(y+5)}^{2}-16(x-4){(y+5)}^{3})\text{ }i+(12{(x-4)}^{4}(y+5)-16{(x-4)}^{2}{(y+5)}^{2})\text{ }j \\  & =(24{(x-4)}^{3}{(y+5)}^{2}-16(x-4){(y+5)}^{3})\text{ }i+(12{(x-4)}^{4}(y+5)-24{(x-4)}^{2}{(y+5)}^{2})\text{ }j\end{aligned}
$$

### Generated moderate source:q-36144

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: False.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & =3{(x-4)}^{2}-4(y+5),\, &  & ∇g(x,y)=6(x-4)\text{ }i-4\text{ }j, &  &  \\ h(x,y) & =2{(x-4)}^{2}{(y+5)}^{2},\, &  & ∇h(x,y)=4(x-4){(y+5)}^{2}\text{ }i+4{(x-4)}^{2}(y+5)\text{ }j. &  & \end{aligned}
$$

- $24{(x-4)}^{3}{(y+5)}^{2}-16(x-4){(y+5)}^{3}+12{(x-4)}^{4}(y+5)-24{(x-4)}^{2}{(y+5)}^{2}$
- $-16(x-4){(y+5)}^{3}\text{ }i+12{(x-4)}^{4}(y+5)\text{ }j$
- $(2{(x-4)}^{3}{(y+5)}^{2}-(x-4){(y+5)}^{3})\text{ }i+({(x-4)}^{4}(y+5)-2{(x-4)}^{2}{(y+5)}^{2})\text{ }j$
- $(12{(x-4)}^{4}(y+5)-24{(x-4)}^{2}{(y+5)}^{2})\text{ }i+(24{(x-4)}^{3}{(y+5)}^{2}-16(x-4){(y+5)}^{3})\text{ }j$
- $(24{(x-4)}^{3}{(y+5)}^{2}-16(x-4){(y+5)}^{3})\text{ }i+(12{(x-4)}^{4}(y+5)-24{(x-4)}^{2}{(y+5)}^{2})\text{ }j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =2{(x-4)}^{2}{(y+5)}^{2}(6(x-4)\text{ }i-4\text{ }j)+(3{(x-4)}^{2}-4(y+5))(4(x-4){(y+5)}^{2}\text{ }i+4{(x-4)}^{2}(y+5)\text{ }j) \\  & =(2{(x-4)}^{2}{(y+5)}^{2}\cdot 6(x-4)\text{ }i-2{(x-4)}^{2}{(y+5)}^{2}\cdot 4\text{ }j)+((3{(x-4)}^{2}-4(y+5))\cdot 4(x-4){(y+5)}^{2}\text{ }i+(3{(x-4)}^{2}-4(y+5))\cdot 4{(x-4)}^{2}(y+5)\text{ }j) \\  & =12{(x-4)}^{3}{(y+5)}^{2}\text{ }i-8{(x-4)}^{2}{(y+5)}^{2}\text{ }j+(12{(x-4)}^{3}{(y+5)}^{2}-16(x-4){(y+5)}^{3})\text{ }i+(12{(x-4)}^{4}(y+5)-16{(x-4)}^{2}{(y+5)}^{2})\text{ }j \\  & =(24{(x-4)}^{3}{(y+5)}^{2}-16(x-4){(y+5)}^{3})\text{ }i+(12{(x-4)}^{4}(y+5)-24{(x-4)}^{2}{(y+5)}^{2})\text{ }j\end{aligned}
$$

## Original q-37466 (log_product; unrated)

What is the gradient of the product $f(x, y)g(x, y)$ if $f(x, y) = \ln x\ln y$ and $g(x, y) = x^{2}y^{2}$?

- $y^{2}\ln y(2\ln x + 1)i + x^{2}\ln x(2\ln y + 1)j$
- $xy^{2}\ln y(2\ln x + 1)i + x^{2}y\ln x(2\ln y + 1)j$
- $xy^{2}\ln y(\ln x + 1)i + x^{2}y\ln x(\ln y + 1)j$
- $2xy^{2}\ln x\ln yi + 2x^{2}y\ln x\ln yj$
- $xy\ln y(2\ln x + 1)i + xy\ln x(2\ln y + 1)j$

[Original worked solution, correct designation and difficulty absent.]

### Generated moderate observed

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

What is the gradient of the product $f(x, y)g(x, y)$ if $f(x, y) = \ln (x-4)\ln (y+6)$ and $g(x, y) = (x-4)^{2}(y+6)^{2}$?

- $(x-4)(y+6)^{2}\ln (y+6)(2\ln (x-4) + 1)i + (x-4)^{2}(y+6)\ln (x-4)(2\ln (y+6) + 1)j$
- $2(x-4)(y+6)^{2}\ln (x-4)\ln (y+6)i + 2(x-4)^{2}(y+6)\ln (x-4)\ln (y+6)j$
- $(x-4)(y+6)^{2}\ln (y+6)(\ln (x-4) + 1)i + (x-4)^{2}(y+6)\ln (x-4)(\ln (y+6) + 1)j$
- $(y+6)^{2}\ln (y+6)(2\ln (x-4) + 1)i + (x-4)^{2}\ln (x-4)(2\ln (y+6) + 1)j$
- $(x-4)(y+6)\ln (y+6)(2\ln (x-4) + 1)i + (x-4)(y+6)\ln (x-4)(2\ln (y+6) + 1)j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=g∇f+f∇g.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})=\frac{\ln{\left(y + 6 \right)}}{x - 4} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})=\frac{\ln{\left(x - 4 \right)}}{y + 6}\end{aligned}
$$

Hence,

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}i+\frac{∂f}{∂y}j=(\frac{\ln{\left(y + 6 \right)}}{x - 4})\,i+(\frac{\ln{\left(x - 4 \right)}}{y + 6})\,j\end{aligned}
$$

Now, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(\left(x - 4\right)^{2} \left(y + 6\right)^{2})=\left(2 x - 8\right) \left(y + 6\right)^{2} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(\left(x - 4\right)^{2} \left(y + 6\right)^{2})=\left(x - 4\right)^{2} \left(2 y + 12\right)\end{aligned}
$$

Hence,

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}i+\frac{∂g}{∂y}j=(\left(2 x - 8\right) \left(y + 6\right)^{2})\,i+(\left(x - 4\right)^{2} \left(2 y + 12\right))\,j\end{aligned}
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(\left(x - 4\right)^{2} \left(y + 6\right)^{2})((\frac{\ln{\left(y + 6 \right)}}{x - 4})\,i+(\frac{\ln{\left(x - 4 \right)}}{y + 6})\,j)+(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})((\left(2 x - 8\right) \left(y + 6\right)^{2})\,i+(\left(x - 4\right)^{2} \left(2 y + 12\right))\,j) \\  & =(\left(x - 4\right)^{2} \left(y + 6\right)^{2})(\frac{\ln{\left(y + 6 \right)}}{x - 4})i+(\left(x - 4\right)^{2} \left(y + 6\right)^{2})(\frac{\ln{\left(x - 4 \right)}}{y + 6})j+(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})(\left(2 x - 8\right) \left(y + 6\right)^{2})i+(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})(\left(x - 4\right)^{2} \left(2 y + 12\right))j \\  & =(\left(x - 4\right) \left(y + 6\right)^{2} \ln{\left(y + 6 \right)})i+(\left(x - 4\right)^{2} \left(y + 6\right) \ln{\left(x - 4 \right)})j+(2 \left(x - 4\right) \left(y + 6\right)^{2} \ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})i+(2 \left(x - 4\right)^{2} \left(y + 6\right) \ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})j \\  & =(\left(x - 4\right) \left(y + 6\right)^{2} \left(2 \ln{\left(x - 4 \right)} + 1\right) \ln{\left(y + 6 \right)})\,i+(\left(x - 4\right)^{2} \left(y + 6\right) \left(2 \ln{\left(y + 6 \right)} + 1\right) \ln{\left(x - 4 \right)})\,j\end{aligned}
$$

### Generated moderate observed

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: True.

What is the gradient of the product $f(x, y)g(x, y)$ if $f(x, y) = \ln (x-4)\ln (y+5)$ and $g(x, y) = (x-4)^{2}(y+5)^{2}$?

- $(x-4)(y+5)^{2}\ln (y+5)(2\ln (x-4) + 1)i + (x-4)^{2}(y+5)\ln (x-4)(2\ln (y+5) + 1)j$
- $2(x-4)(y+5)^{2}\ln (x-4)\ln (y+5)i + 2(x-4)^{2}(y+5)\ln (x-4)\ln (y+5)j$
- $(x-4)(y+5)\ln (y+5)(2\ln (x-4) + 1)i + (x-4)(y+5)\ln (x-4)(2\ln (y+5) + 1)j$
- $(x-4)(y+5)^{2}\ln (y+5)(\ln (x-4) + 1)i + (x-4)^{2}(y+5)\ln (x-4)(\ln (y+5) + 1)j$
- $(y+5)^{2}\ln (y+5)(2\ln (x-4) + 1)i + (x-4)^{2}\ln (x-4)(2\ln (y+5) + 1)j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=g∇f+f∇g.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(\ln{\left(x - 4 \right)} \ln{\left(y + 5 \right)})=\frac{\ln{\left(y + 5 \right)}}{x - 4} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}(\ln{\left(x - 4 \right)} \ln{\left(y + 5 \right)})=\frac{\ln{\left(x - 4 \right)}}{y + 5}\end{aligned}
$$

Hence,

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}i+\frac{∂f}{∂y}j=(\frac{\ln{\left(y + 5 \right)}}{x - 4})\,i+(\frac{\ln{\left(x - 4 \right)}}{y + 5})\,j\end{aligned}
$$

Now, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(\left(x - 4\right)^{2} \left(y + 5\right)^{2})=\left(2 x - 8\right) \left(y + 5\right)^{2} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(\left(x - 4\right)^{2} \left(y + 5\right)^{2})=\left(x - 4\right)^{2} \left(2 y + 10\right)\end{aligned}
$$

Hence,

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}i+\frac{∂g}{∂y}j=(\left(2 x - 8\right) \left(y + 5\right)^{2})\,i+(\left(x - 4\right)^{2} \left(2 y + 10\right))\,j\end{aligned}
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(\left(x - 4\right)^{2} \left(y + 5\right)^{2})((\frac{\ln{\left(y + 5 \right)}}{x - 4})\,i+(\frac{\ln{\left(x - 4 \right)}}{y + 5})\,j)+(\ln{\left(x - 4 \right)} \ln{\left(y + 5 \right)})((\left(2 x - 8\right) \left(y + 5\right)^{2})\,i+(\left(x - 4\right)^{2} \left(2 y + 10\right))\,j) \\  & =(\left(x - 4\right)^{2} \left(y + 5\right)^{2})(\frac{\ln{\left(y + 5 \right)}}{x - 4})i+(\left(x - 4\right)^{2} \left(y + 5\right)^{2})(\frac{\ln{\left(x - 4 \right)}}{y + 5})j+(\ln{\left(x - 4 \right)} \ln{\left(y + 5 \right)})(\left(2 x - 8\right) \left(y + 5\right)^{2})i+(\ln{\left(x - 4 \right)} \ln{\left(y + 5 \right)})(\left(x - 4\right)^{2} \left(2 y + 10\right))j \\  & =(\left(x - 4\right) \left(y + 5\right)^{2} \ln{\left(y + 5 \right)})i+(\left(x - 4\right)^{2} \left(y + 5\right) \ln{\left(x - 4 \right)})j+(2 \left(x - 4\right) \left(y + 5\right)^{2} \ln{\left(x - 4 \right)} \ln{\left(y + 5 \right)})i+(2 \left(x - 4\right)^{2} \left(y + 5\right) \ln{\left(x - 4 \right)} \ln{\left(y + 5 \right)})j \\  & =(\left(x - 4\right) \left(y + 5\right)^{2} \left(2 \ln{\left(x - 4 \right)} + 1\right) \ln{\left(y + 5 \right)})\,i+(\left(x - 4\right)^{2} \left(y + 5\right) \left(2 \ln{\left(y + 5 \right)} + 1\right) \ln{\left(x - 4 \right)})\,j\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

What is the gradient of the product $f(x, y)g(x, y)$ if $f(x, y) = \ln (x-4)\ln (y+6)$ and $g(x, y) = (x-4)^{2}(y+6)^{2}$?

- $(\left(x - 4\right) \left(y + 6\right)^{2} \ln{\left(y + 6 \right)})\,i+(\left(x - 4\right)^{2} \left(y + 6\right) \ln{\left(x - 4 \right)})\,j$
- $(\left(x - 4\right) \left(y + 6\right)^{2} \ln{\left(y + 6 \right)} - \left(2 x - 8\right) \left(y + 6\right)^{2} \ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})\,i+(\left(x - 4\right)^{2} \left(y + 6\right) \ln{\left(x - 4 \right)} - \left(x - 4\right)^{2} \left(2 y + 12\right) \ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})\,j$
- $(\left(2 x - 8\right) \left(y + 6\right)^{2} \ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})\,i+(\left(x - 4\right)^{2} \left(2 y + 12\right) \ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})\,j$
- $(\left(x - 4\right) \left(y + 6\right)^{2} \left(2 \ln{\left(x - 4 \right)} + 1\right) \ln{\left(y + 6 \right)})\,i+(\left(x - 4\right)^{2} \left(y + 6\right) \left(2 \ln{\left(y + 6 \right)} + 1\right) \ln{\left(x - 4 \right)})\,j$
- $(\left(x - 4\right)^{2} \left(y + 6\right) \left(2 \ln{\left(y + 6 \right)} + 1\right) \ln{\left(x - 4 \right)})\,i+(\left(x - 4\right) \left(y + 6\right)^{2} \left(2 \ln{\left(x - 4 \right)} + 1\right) \ln{\left(y + 6 \right)})\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=g∇f+f∇g.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})=\frac{\ln{\left(y + 6 \right)}}{x - 4} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})=\frac{\ln{\left(x - 4 \right)}}{y + 6}\end{aligned}
$$

Hence,

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}i+\frac{∂f}{∂y}j=(\frac{\ln{\left(y + 6 \right)}}{x - 4})\,i+(\frac{\ln{\left(x - 4 \right)}}{y + 6})\,j\end{aligned}
$$

Now, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(\left(x - 4\right)^{2} \left(y + 6\right)^{2})=\left(2 x - 8\right) \left(y + 6\right)^{2} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(\left(x - 4\right)^{2} \left(y + 6\right)^{2})=\left(x - 4\right)^{2} \left(2 y + 12\right)\end{aligned}
$$

Hence,

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}i+\frac{∂g}{∂y}j=(\left(2 x - 8\right) \left(y + 6\right)^{2})\,i+(\left(x - 4\right)^{2} \left(2 y + 12\right))\,j\end{aligned}
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(\left(x - 4\right)^{2} \left(y + 6\right)^{2})((\frac{\ln{\left(y + 6 \right)}}{x - 4})\,i+(\frac{\ln{\left(x - 4 \right)}}{y + 6})\,j)+(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})((\left(2 x - 8\right) \left(y + 6\right)^{2})\,i+(\left(x - 4\right)^{2} \left(2 y + 12\right))\,j) \\  & =(\left(x - 4\right)^{2} \left(y + 6\right)^{2})(\frac{\ln{\left(y + 6 \right)}}{x - 4})i+(\left(x - 4\right)^{2} \left(y + 6\right)^{2})(\frac{\ln{\left(x - 4 \right)}}{y + 6})j+(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})(\left(2 x - 8\right) \left(y + 6\right)^{2})i+(\ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})(\left(x - 4\right)^{2} \left(2 y + 12\right))j \\  & =(\left(x - 4\right) \left(y + 6\right)^{2} \ln{\left(y + 6 \right)})i+(\left(x - 4\right)^{2} \left(y + 6\right) \ln{\left(x - 4 \right)})j+(2 \left(x - 4\right) \left(y + 6\right)^{2} \ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})i+(2 \left(x - 4\right)^{2} \left(y + 6\right) \ln{\left(x - 4 \right)} \ln{\left(y + 6 \right)})j \\  & =(\left(x - 4\right) \left(y + 6\right)^{2} \left(2 \ln{\left(x - 4 \right)} + 1\right) \ln{\left(y + 6 \right)})\,i+(\left(x - 4\right)^{2} \left(y + 6\right) \left(2 \ln{\left(y + 6 \right)} + 1\right) \ln{\left(x - 4 \right)})\,j\end{aligned}
$$

## Original q-128521 (gaussian; hard)

What is the gradient of the product $f(x,y)g(x,y)$ if $f(x,y)=x{y}^{2}$ and $g(x,y)={e}^{-({x}^{2}+{y}^{2})}?$

- ${e}^{-({x}^{2}+{y}^{2})}({y}^{2}(1-2{x}^{2})\text{ }i+2xy(1-{y}^{2})\text{ }j)$
- ${e}^{-({x}^{2}+{y}^{2})}({y}^{2}(1-{x}^{2})\text{ }i+2xy(1-{y}^{2})\text{ }j)$
- ${e}^{-({x}^{2}+{y}^{2})}(y(1-2{x}^{2})\text{ }i+x(1+2{y}^{2})\text{ }j)$
- ${e}^{-({x}^{2}+{y}^{2})}(x(1-{y}^{2})\text{ }i+xy(1-{x}^{2})\text{ }j)$
- ${e}^{-({x}^{2}+{y}^{2})}({x}^{2}(1+{y}^{2})\text{ }i+2{y}^{2}(1+{x}^{2})\text{ }j)$

The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=f∇g+g∇f.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(x{y}^{2})={y}^{2} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}(x{y}^{2})=2xy\end{aligned}
$$

Hence, 

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}\text{ }i+\frac{∂f}{∂y}\text{ }j={y}^{2}\text{ }i+2xy\text{ }j.\end{aligned}
$$

Next, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}({e}^{-({x}^{2}+{y}^{2})})=-2x{e}^{-({x}^{2}+{y}^{2})} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}({e}^{-({x}^{2}+{y}^{2})})=-2y{e}^{-({x}^{2}+{y}^{2})}\end{aligned}
$$

Therefore, 

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}\text{ }i+\frac{∂g}{∂y}\text{ }j=-2x{e}^{-({x}^{2}+{y}^{2})}\text{ }i-2y{e}^{-({x}^{2}+{y}^{2})}\text{ }j.\end{aligned}
$$

Finally, using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =x{y}^{2}(-2x{e}^{-({x}^{2}+{y}^{2})}\text{ }i-2y{e}^{-({x}^{2}+{y}^{2})}\text{ }j)+{e}^{-({x}^{2}+{y}^{2})}({y}^{2}\text{ }i+2xy\text{ }j) \\  & ={e}^{-({x}^{2}+{y}^{2})}(-2{x}^{2}{y}^{2}\text{ }i-2x{y}^{3}\text{ }j)+{e}^{-({x}^{2}+{y}^{2})}({y}^{2}\text{ }i+2xy\text{ }j) \\  & ={e}^{-({x}^{2}+{y}^{2})}({y}^{2}(1-2{x}^{2})\text{ }i+2xy(1-{y}^{2})\text{ }j).\end{aligned}
$$

### Generated hard method

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

What is the gradient of the product $f(x,y)g(x,y)$ if $f(x,y)=(x-4){(y+6)}^{2}$ and $g(x,y)={e}^{-({(x-4)}^{2}+{(y+6)}^{2})}?$

- $(\left(y + 6\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,i+(\left(x - 4\right) \left(2 y + 12\right) e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,j$
- $(- \left(8 - 2 x\right) \left(x - 4\right) \left(y + 6\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}} + \left(y + 6\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,i+(- \left(x - 4\right) \left(- 2 y - 12\right) \left(y + 6\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}} + \left(x - 4\right) \left(2 y + 12\right) e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,j$
- $(\left(8 - 2 x\right) \left(x - 4\right) \left(y + 6\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,i+(\left(x - 4\right) \left(- 2 y - 12\right) \left(y + 6\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,j$
- $(\left(1 - 2 \left(x - 4\right)^{2}\right) \left(y + 6\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,i+(2 \left(1 - \left(y + 6\right)^{2}\right) \left(x - 4\right) \left(y + 6\right) e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,j$
- $(2 \left(1 - \left(y + 6\right)^{2}\right) \left(x - 4\right) \left(y + 6\right) e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,i+(\left(1 - 2 \left(x - 4\right)^{2}\right) \left(y + 6\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 6\right)^{2}})\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=f∇g+g∇f.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}((x-4){(y+6)}^{2})={(y+6)}^{2} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}((x-4){(y+6)}^{2})=2(x-4)(y+6)\end{aligned}
$$

Hence, 

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}\text{ }i+\frac{∂f}{∂y}\text{ }j={(y+6)}^{2}\text{ }i+2(x-4)(y+6)\text{ }j.\end{aligned}
$$

Next, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}({e}^{-({(x-4)}^{2}+{(y+6)}^{2})})=-2(x-4){e}^{-({(x-4)}^{2}+{(y+6)}^{2})} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}({e}^{-({(x-4)}^{2}+{(y+6)}^{2})})=-2(y+6){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\end{aligned}
$$

Therefore, 

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}\text{ }i+\frac{∂g}{∂y}\text{ }j=-2(x-4){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\text{ }i-2(y+6){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\text{ }j.\end{aligned}
$$

Finally, using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =(x-4){(y+6)}^{2}(-2(x-4){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\text{ }i-2(y+6){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\text{ }j)+{e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(y+6)}^{2}\text{ }i+2(x-4)(y+6)\text{ }j) \\  & ={e}^{-({(x-4)}^{2}+{(y+6)}^{2})}(-2{(x-4)}^{2}{(y+6)}^{2}\text{ }i-2(x-4){(y+6)}^{3}\text{ }j)+{e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(y+6)}^{2}\text{ }i+2(x-4)(y+6)\text{ }j) \\  & ={e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(y+6)}^{2}(1-2{(x-4)}^{2})\text{ }i+2(x-4)(y+6)(1-{(y+6)}^{2})\text{ }j).\end{aligned}
$$

### Generated hard source:q-128521

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: False.

What is the gradient of the product $f(x,y)g(x,y)$ if $f(x,y)=(x-4){(y+6)}^{2}$ and $g(x,y)={e}^{-({(x-4)}^{2}+{(y+6)}^{2})}?$

- ${e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(y+6)}^{2}(1-{(x-4)}^{2})\text{ }i+2(x-4)(y+6)(1-{(y+6)}^{2})\text{ }j)$
- ${e}^{-({(x-4)}^{2}+{(y+6)}^{2})}((x-4)(1-{(y+6)}^{2})\text{ }i+(x-4)(y+6)(1-{(x-4)}^{2})\text{ }j)$
- ${e}^{-({(x-4)}^{2}+{(y+6)}^{2})}((y+6)(1-2{(x-4)}^{2})\text{ }i+(x-4)(1+2{(y+6)}^{2})\text{ }j)$
- ${e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(x-4)}^{2}(1+{(y+6)}^{2})\text{ }i+2{(y+6)}^{2}(1+{(x-4)}^{2})\text{ }j)$
- ${e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(y+6)}^{2}(1-2{(x-4)}^{2})\text{ }i+2(x-4)(y+6)(1-{(y+6)}^{2})\text{ }j)$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=f∇g+g∇f.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}((x-4){(y+6)}^{2})={(y+6)}^{2} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}((x-4){(y+6)}^{2})=2(x-4)(y+6)\end{aligned}
$$

Hence, 

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}\text{ }i+\frac{∂f}{∂y}\text{ }j={(y+6)}^{2}\text{ }i+2(x-4)(y+6)\text{ }j.\end{aligned}
$$

Next, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}({e}^{-({(x-4)}^{2}+{(y+6)}^{2})})=-2(x-4){e}^{-({(x-4)}^{2}+{(y+6)}^{2})} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}({e}^{-({(x-4)}^{2}+{(y+6)}^{2})})=-2(y+6){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\end{aligned}
$$

Therefore, 

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}\text{ }i+\frac{∂g}{∂y}\text{ }j=-2(x-4){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\text{ }i-2(y+6){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\text{ }j.\end{aligned}
$$

Finally, using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =(x-4){(y+6)}^{2}(-2(x-4){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\text{ }i-2(y+6){e}^{-({(x-4)}^{2}+{(y+6)}^{2})}\text{ }j)+{e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(y+6)}^{2}\text{ }i+2(x-4)(y+6)\text{ }j) \\  & ={e}^{-({(x-4)}^{2}+{(y+6)}^{2})}(-2{(x-4)}^{2}{(y+6)}^{2}\text{ }i-2(x-4){(y+6)}^{3}\text{ }j)+{e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(y+6)}^{2}\text{ }i+2(x-4)(y+6)\text{ }j) \\  & ={e}^{-({(x-4)}^{2}+{(y+6)}^{2})}({(y+6)}^{2}(1-2{(x-4)}^{2})\text{ }i+2(x-4)(y+6)(1-{(y+6)}^{2})\text{ }j).\end{aligned}
$$

### Generated hard method

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: True.

What is the gradient of the product $f(x,y)g(x,y)$ if $f(x,y)=(x-4){(y+5)}^{2}$ and $g(x,y)={e}^{-({(x-4)}^{2}+{(y+5)}^{2})}?$

- $(\left(y + 5\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,i+(\left(x - 4\right) \left(2 y + 10\right) e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,j$
- $(- \left(8 - 2 x\right) \left(x - 4\right) \left(y + 5\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}} + \left(y + 5\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,i+(- \left(x - 4\right) \left(- 2 y - 10\right) \left(y + 5\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}} + \left(x - 4\right) \left(2 y + 10\right) e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,j$
- $(2 \left(1 - \left(y + 5\right)^{2}\right) \left(x - 4\right) \left(y + 5\right) e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,i+(\left(1 - 2 \left(x - 4\right)^{2}\right) \left(y + 5\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,j$
- $(\left(8 - 2 x\right) \left(x - 4\right) \left(y + 5\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,i+(\left(x - 4\right) \left(- 2 y - 10\right) \left(y + 5\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,j$
- $(\left(1 - 2 \left(x - 4\right)^{2}\right) \left(y + 5\right)^{2} e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,i+(2 \left(1 - \left(y + 5\right)^{2}\right) \left(x - 4\right) \left(y + 5\right) e^{- \left(x - 4\right)^{2} - \left(y + 5\right)^{2}})\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=f∇g+g∇f.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}((x-4){(y+5)}^{2})={(y+5)}^{2} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}((x-4){(y+5)}^{2})=2(x-4)(y+5)\end{aligned}
$$

Hence, 

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}\text{ }i+\frac{∂f}{∂y}\text{ }j={(y+5)}^{2}\text{ }i+2(x-4)(y+5)\text{ }j.\end{aligned}
$$

Next, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}({e}^{-({(x-4)}^{2}+{(y+5)}^{2})})=-2(x-4){e}^{-({(x-4)}^{2}+{(y+5)}^{2})} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}({e}^{-({(x-4)}^{2}+{(y+5)}^{2})})=-2(y+5){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\end{aligned}
$$

Therefore, 

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}\text{ }i+\frac{∂g}{∂y}\text{ }j=-2(x-4){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\text{ }i-2(y+5){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\text{ }j.\end{aligned}
$$

Finally, using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =(x-4){(y+5)}^{2}(-2(x-4){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\text{ }i-2(y+5){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\text{ }j)+{e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(y+5)}^{2}\text{ }i+2(x-4)(y+5)\text{ }j) \\  & ={e}^{-({(x-4)}^{2}+{(y+5)}^{2})}(-2{(x-4)}^{2}{(y+5)}^{2}\text{ }i-2(x-4){(y+5)}^{3}\text{ }j)+{e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(y+5)}^{2}\text{ }i+2(x-4)(y+5)\text{ }j) \\  & ={e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(y+5)}^{2}(1-2{(x-4)}^{2})\text{ }i+2(x-4)(y+5)(1-{(y+5)}^{2})\text{ }j).\end{aligned}
$$

### Generated hard source:q-128521

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: False.

What is the gradient of the product $f(x,y)g(x,y)$ if $f(x,y)=(x-4){(y+5)}^{2}$ and $g(x,y)={e}^{-({(x-4)}^{2}+{(y+5)}^{2})}?$

- ${e}^{-({(x-4)}^{2}+{(y+5)}^{2})}((x-4)(1-{(y+5)}^{2})\text{ }i+(x-4)(y+5)(1-{(x-4)}^{2})\text{ }j)$
- ${e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(y+5)}^{2}(1-{(x-4)}^{2})\text{ }i+2(x-4)(y+5)(1-{(y+5)}^{2})\text{ }j)$
- ${e}^{-({(x-4)}^{2}+{(y+5)}^{2})}((y+5)(1-2{(x-4)}^{2})\text{ }i+(x-4)(1+2{(y+5)}^{2})\text{ }j)$
- ${e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(x-4)}^{2}(1+{(y+5)}^{2})\text{ }i+2{(y+5)}^{2}(1+{(x-4)}^{2})\text{ }j)$
- ${e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(y+5)}^{2}(1-2{(x-4)}^{2})\text{ }i+2(x-4)(y+5)(1-{(y+5)}^{2})\text{ }j)$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=f∇g+g∇f.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}((x-4){(y+5)}^{2})={(y+5)}^{2} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}((x-4){(y+5)}^{2})=2(x-4)(y+5)\end{aligned}
$$

Hence, 

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}\text{ }i+\frac{∂f}{∂y}\text{ }j={(y+5)}^{2}\text{ }i+2(x-4)(y+5)\text{ }j.\end{aligned}
$$

Next, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}({e}^{-({(x-4)}^{2}+{(y+5)}^{2})})=-2(x-4){e}^{-({(x-4)}^{2}+{(y+5)}^{2})} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}({e}^{-({(x-4)}^{2}+{(y+5)}^{2})})=-2(y+5){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\end{aligned}
$$

Therefore, 

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}\text{ }i+\frac{∂g}{∂y}\text{ }j=-2(x-4){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\text{ }i-2(y+5){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\text{ }j.\end{aligned}
$$

Finally, using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =(x-4){(y+5)}^{2}(-2(x-4){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\text{ }i-2(y+5){e}^{-({(x-4)}^{2}+{(y+5)}^{2})}\text{ }j)+{e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(y+5)}^{2}\text{ }i+2(x-4)(y+5)\text{ }j) \\  & ={e}^{-({(x-4)}^{2}+{(y+5)}^{2})}(-2{(x-4)}^{2}{(y+5)}^{2}\text{ }i-2(x-4){(y+5)}^{3}\text{ }j)+{e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(y+5)}^{2}\text{ }i+2(x-4)(y+5)\text{ }j) \\  & ={e}^{-({(x-4)}^{2}+{(y+5)}^{2})}({(y+5)}^{2}(1-2{(x-4)}^{2})\text{ }i+2(x-4)(y+5)(1-{(y+5)}^{2})\text{ }j).\end{aligned}
$$

### Generated hard method

Parameters: `{"x0": 6, "y0": 2}`. Eligible for learning: True.

What is the gradient of the product $f(x,y)g(x,y)$ if $f(x,y)=(x-6){(y-2)}^{2}$ and $g(x,y)={e}^{-({(x-6)}^{2}+{(y-2)}^{2})}?$

- $(2 \left(1 - \left(y - 2\right)^{2}\right) \left(x - 6\right) \left(y - 2\right) e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,i+(\left(1 - 2 \left(x - 6\right)^{2}\right) \left(y - 2\right)^{2} e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,j$
- $(\left(12 - 2 x\right) \left(x - 6\right) \left(y - 2\right)^{2} e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,i+(\left(4 - 2 y\right) \left(x - 6\right) \left(y - 2\right)^{2} e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,j$
- $(- \left(12 - 2 x\right) \left(x - 6\right) \left(y - 2\right)^{2} e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}} + \left(y - 2\right)^{2} e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,i+(- \left(4 - 2 y\right) \left(x - 6\right) \left(y - 2\right)^{2} e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}} + \left(x - 6\right) \left(2 y - 4\right) e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,j$
- $(\left(y - 2\right)^{2} e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,i+(\left(x - 6\right) \left(2 y - 4\right) e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,j$
- $(\left(1 - 2 \left(x - 6\right)^{2}\right) \left(y - 2\right)^{2} e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,i+(2 \left(1 - \left(y - 2\right)^{2}\right) \left(x - 6\right) \left(y - 2\right) e^{- \left(x - 6\right)^{2} - \left(y - 2\right)^{2}})\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=f∇g+g∇f.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}((x-6){(y-2)}^{2})={(y-2)}^{2} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}((x-6){(y-2)}^{2})=2(x-6)(y-2)\end{aligned}
$$

Hence, 

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}\text{ }i+\frac{∂f}{∂y}\text{ }j={(y-2)}^{2}\text{ }i+2(x-6)(y-2)\text{ }j.\end{aligned}
$$

Next, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}({e}^{-({(x-6)}^{2}+{(y-2)}^{2})})=-2(x-6){e}^{-({(x-6)}^{2}+{(y-2)}^{2})} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}({e}^{-({(x-6)}^{2}+{(y-2)}^{2})})=-2(y-2){e}^{-({(x-6)}^{2}+{(y-2)}^{2})}\end{aligned}
$$

Therefore, 

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}\text{ }i+\frac{∂g}{∂y}\text{ }j=-2(x-6){e}^{-({(x-6)}^{2}+{(y-2)}^{2})}\text{ }i-2(y-2){e}^{-({(x-6)}^{2}+{(y-2)}^{2})}\text{ }j.\end{aligned}
$$

Finally, using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =(x-6){(y-2)}^{2}(-2(x-6){e}^{-({(x-6)}^{2}+{(y-2)}^{2})}\text{ }i-2(y-2){e}^{-({(x-6)}^{2}+{(y-2)}^{2})}\text{ }j)+{e}^{-({(x-6)}^{2}+{(y-2)}^{2})}({(y-2)}^{2}\text{ }i+2(x-6)(y-2)\text{ }j) \\  & ={e}^{-({(x-6)}^{2}+{(y-2)}^{2})}(-2{(x-6)}^{2}{(y-2)}^{2}\text{ }i-2(x-6){(y-2)}^{3}\text{ }j)+{e}^{-({(x-6)}^{2}+{(y-2)}^{2})}({(y-2)}^{2}\text{ }i+2(x-6)(y-2)\text{ }j) \\  & ={e}^{-({(x-6)}^{2}+{(y-2)}^{2})}({(y-2)}^{2}(1-2{(x-6)}^{2})\text{ }i+2(x-6)(y-2)(1-{(y-2)}^{2})\text{ }j).\end{aligned}
$$

### Generated hard method

Parameters: `{"x0": -6, "y0": 5}`. Eligible for learning: True.

What is the gradient of the product $f(x,y)g(x,y)$ if $f(x,y)=(x+6){(y-5)}^{2}$ and $g(x,y)={e}^{-({(x+6)}^{2}+{(y-5)}^{2})}?$

- $(- \left(- 2 x - 12\right) \left(x + 6\right) \left(y - 5\right)^{2} e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}} + \left(y - 5\right)^{2} e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,i+(- \left(10 - 2 y\right) \left(x + 6\right) \left(y - 5\right)^{2} e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}} + \left(x + 6\right) \left(2 y - 10\right) e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,j$
- $(2 \left(1 - \left(y - 5\right)^{2}\right) \left(x + 6\right) \left(y - 5\right) e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,i+(\left(1 - 2 \left(x + 6\right)^{2}\right) \left(y - 5\right)^{2} e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,j$
- $(\left(1 - 2 \left(x + 6\right)^{2}\right) \left(y - 5\right)^{2} e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,i+(2 \left(1 - \left(y - 5\right)^{2}\right) \left(x + 6\right) \left(y - 5\right) e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,j$
- $(\left(y - 5\right)^{2} e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,i+(\left(x + 6\right) \left(2 y - 10\right) e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,j$
- $(\left(- 2 x - 12\right) \left(x + 6\right) \left(y - 5\right)^{2} e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,i+(\left(10 - 2 y\right) \left(x + 6\right) \left(y - 5\right)^{2} e^{- \left(x + 6\right)^{2} - \left(y - 5\right)^{2}})\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=f∇g+g∇f.
$$

Now, we calculate the partial derivatives of $f(x,y):$

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}((x+6){(y-5)}^{2})={(y-5)}^{2} \\ \frac{∂f}{∂y} & =\frac{∂}{∂y}((x+6){(y-5)}^{2})=2(x+6)(y-5)\end{aligned}
$$

Hence, 

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}\text{ }i+\frac{∂f}{∂y}\text{ }j={(y-5)}^{2}\text{ }i+2(x+6)(y-5)\text{ }j.\end{aligned}
$$

Next, we calculate the partial derivatives of $g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}({e}^{-({(x+6)}^{2}+{(y-5)}^{2})})=-2(x+6){e}^{-({(x+6)}^{2}+{(y-5)}^{2})} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}({e}^{-({(x+6)}^{2}+{(y-5)}^{2})})=-2(y-5){e}^{-({(x+6)}^{2}+{(y-5)}^{2})}\end{aligned}
$$

Therefore, 

$$
\begin{aligned}∇g(x,y) & =\frac{∂g}{∂x}\text{ }i+\frac{∂g}{∂y}\text{ }j=-2(x+6){e}^{-({(x+6)}^{2}+{(y-5)}^{2})}\text{ }i-2(y-5){e}^{-({(x+6)}^{2}+{(y-5)}^{2})}\text{ }j.\end{aligned}
$$

Finally, using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =(x+6){(y-5)}^{2}(-2(x+6){e}^{-({(x+6)}^{2}+{(y-5)}^{2})}\text{ }i-2(y-5){e}^{-({(x+6)}^{2}+{(y-5)}^{2})}\text{ }j)+{e}^{-({(x+6)}^{2}+{(y-5)}^{2})}({(y-5)}^{2}\text{ }i+2(x+6)(y-5)\text{ }j) \\  & ={e}^{-({(x+6)}^{2}+{(y-5)}^{2})}(-2{(x+6)}^{2}{(y-5)}^{2}\text{ }i-2(x+6){(y-5)}^{3}\text{ }j)+{e}^{-({(x+6)}^{2}+{(y-5)}^{2})}({(y-5)}^{2}\text{ }i+2(x+6)(y-5)\text{ }j) \\  & ={e}^{-({(x+6)}^{2}+{(y-5)}^{2})}({(y-5)}^{2}(1-2{(x+6)}^{2})\text{ }i+2(x+6)(y-5)(1-{(y-5)}^{2})\text{ }j).\end{aligned}
$$

## Original q-128529 (reciprocal3; moderate)

Find the gradient of the product $f(x,y,z)h(x,y,z),$ given that 

$$
\begin{aligned}f(x,y,z) & =x{y}^{2}{z}^{3},\, &  & ∇f(x,y,z)={y}^{2}{z}^{3}\,i+2xy{z}^{3}\,j+3x{y}^{2}{z}^{2}\,k, &  &  \\ h(x,y,z) & =\frac{1}{xyz},\, &  & ∇h(x,y,z)=-\frac{1}{{x}^{2}yz}\,i-\frac{1}{x{y}^{2}z}\,j-\frac{1}{xy{z}^{2}}\text{ }k. &  & \end{aligned}
$$

- $3x\,i+{y}^{2}\,j-2xy\,k$
- ${y}^{2}\,i+3xy\,k$
- $x\,i-2xz\,k$
- ${z}^{2}\,j+2yz\,k$
- $x\,i-{z}^{2}\,j-2yz\,k$

The gradient of the product of two functions $f(x,y)$ and $h(x,y)$ is given by

$$
∇[fh]=h∇f+f∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y,z)h(x,y,z)] & =h(x,y,z)∇f(x,y,z)+f(x,y,z)∇h(x,y,z) \\  & =\frac{1}{xyz}({y}^{2}{z}^{3}\,i+2xy{z}^{3}\,j+3x{y}^{2}{z}^{2}\,k)+x{y}^{2}{z}^{3}(-\frac{1}{{x}^{2}yz}\,i-\frac{1}{x{y}^{2}z}\,j-\frac{1}{xy{z}^{2}}\,k) \\  & =\frac{{y}^{2}{z}^{3}}{xyz}\,i+\frac{2xy{z}^{3}}{xyz}\,j+\frac{3x{y}^{2}{z}^{2}}{xyz}\,k-\frac{x{y}^{2}{z}^{3}}{{x}^{2}yz}\,i-\frac{x{y}^{2}{z}^{3}}{x{y}^{2}z}\,j-\frac{x{y}^{2}{z}^{3}}{xy{z}^{2}}\,k \\  & =\frac{y{z}^{2}}{x}\,i+2{z}^{2}\,j+3yz\,k-\frac{y{z}^{2}}{x}\,i-{z}^{2}\,j-yz\,k \\  & ={z}^{2}\,j+2yz\,k.\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -6, "z0": 6}`. Eligible for learning: True.

Find the gradient of the product $f(x,y,z)h(x,y,z),$ given that 

$$
\begin{aligned}f(x,y,z) & =(x-4){(y+6)}^{2}{(z-6)}^{3},\, &  & ∇f(x,y,z)={(y+6)}^{2}{(z-6)}^{3}\,i+2(x-4)(y+6){(z-6)}^{3}\,j+3(x-4){(y+6)}^{2}{(z-6)}^{2}\,k, &  &  \\ h(x,y,z) & =\frac{1}{(x-4)(y+6)(z-6)},\, &  & ∇h(x,y,z)=-\frac{1}{{(x-4)}^{2}(y+6)(z-6)}\,i-\frac{1}{(x-4){(y+6)}^{2}(z-6)}\,j-\frac{1}{(x-4)(y+6){(z-6)}^{2}}\text{ }k. &  & \end{aligned}
$$

- $(\frac{\left(y + 6\right) \left(z - 6\right)^{2}}{x - 4})\,i+(\frac{\left(2 y + 12\right) \left(z - 6\right)^{2}}{y + 6})\,j+(3 \left(y + 6\right) \left(z - 6\right))\,k$
- $(\frac{2 \left(y + 6\right) \left(z - 6\right)^{2}}{x - 4})\,i+(\left(z - 6\right)^{2} + \frac{\left(2 y + 12\right) \left(z - 6\right)^{2}}{y + 6})\,j+(4 \left(y + 6\right) \left(z - 6\right))\,k$
- $(- \frac{\left(y + 6\right) \left(z - 6\right)^{2}}{x - 4})\,i+(- \left(z - 6\right)^{2})\,j+(- \left(y + 6\right) \left(z - 6\right))\,k$
- $(0)\,i+(\left(z - 6\right)^{2})\,j+(2 \left(y + 6\right) \left(z - 6\right))\,k$
- $(\left(z - 6\right)^{2})\,i+(0)\,j+(2 \left(y + 6\right) \left(z - 6\right))\,k$

Worked solution:
The gradient of the product of two functions $f(x,y,z)$ and $h(x,y,z)$ is given by

$$
∇[fh]=h∇f+f∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y,z)h(x,y,z)] & =h(x,y,z)∇f(x,y,z)+f(x,y,z)∇h(x,y,z) \\  & =\frac{1}{(x-4)(y+6)(z-6)}({(y+6)}^{2}{(z-6)}^{3}\,i+2(x-4)(y+6){(z-6)}^{3}\,j+3(x-4){(y+6)}^{2}{(z-6)}^{2}\,k)+(x-4){(y+6)}^{2}{(z-6)}^{3}(-\frac{1}{{(x-4)}^{2}(y+6)(z-6)}\,i-\frac{1}{(x-4){(y+6)}^{2}(z-6)}\,j-\frac{1}{(x-4)(y+6){(z-6)}^{2}}\,k) \\  & =\frac{{(y+6)}^{2}{(z-6)}^{3}}{(x-4)(y+6)(z-6)}\,i+\frac{2(x-4)(y+6){(z-6)}^{3}}{(x-4)(y+6)(z-6)}\,j+\frac{3(x-4){(y+6)}^{2}{(z-6)}^{2}}{(x-4)(y+6)(z-6)}\,k-\frac{(x-4){(y+6)}^{2}{(z-6)}^{3}}{{(x-4)}^{2}(y+6)(z-6)}\,i-\frac{(x-4){(y+6)}^{2}{(z-6)}^{3}}{(x-4){(y+6)}^{2}(z-6)}\,j-\frac{(x-4){(y+6)}^{2}{(z-6)}^{3}}{(x-4)(y+6){(z-6)}^{2}}\,k \\  & =\frac{(y+6){(z-6)}^{2}}{(x-4)}\,i+2{(z-6)}^{2}\,j+3(y+6)(z-6)\,k-\frac{(y+6){(z-6)}^{2}}{(x-4)}\,i-{(z-6)}^{2}\,j-(y+6)(z-6)\,k \\  & ={(z-6)}^{2}\,j+2(y+6)(z-6)\,k.\end{aligned}
$$

### Generated moderate source:q-128529

Parameters: `{"x0": 4, "y0": -6, "z0": 6}`. Eligible for learning: False.

Find the gradient of the product $f(x,y,z)h(x,y,z),$ given that 

$$
\begin{aligned}f(x,y,z) & =(x-4){(y+6)}^{2}{(z-6)}^{3},\, &  & ∇f(x,y,z)={(y+6)}^{2}{(z-6)}^{3}\,i+2(x-4)(y+6){(z-6)}^{3}\,j+3(x-4){(y+6)}^{2}{(z-6)}^{2}\,k, &  &  \\ h(x,y,z) & =\frac{1}{(x-4)(y+6)(z-6)},\, &  & ∇h(x,y,z)=-\frac{1}{{(x-4)}^{2}(y+6)(z-6)}\,i-\frac{1}{(x-4){(y+6)}^{2}(z-6)}\,j-\frac{1}{(x-4)(y+6){(z-6)}^{2}}\text{ }k. &  & \end{aligned}
$$

- ${(y+6)}^{2}\,i+3(x-4)(y+6)\,k$
- ${(z-6)}^{2}\,j+2(y+6)(z-6)\,k$
- $(x-4)\,i-2(x-4)(z-6)\,k$
- $(x-4)\,i-{(z-6)}^{2}\,j-2(y+6)(z-6)\,k$
- $3(x-4)\,i+{(y+6)}^{2}\,j-2(x-4)(y+6)\,k$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $h(x,y)$ is given by

$$
∇[fh]=h∇f+f∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y,z)h(x,y,z)] & =h(x,y,z)∇f(x,y,z)+f(x,y,z)∇h(x,y,z) \\  & =\frac{1}{(x-4)(y+6)(z-6)}({(y+6)}^{2}{(z-6)}^{3}\,i+2(x-4)(y+6){(z-6)}^{3}\,j+3(x-4){(y+6)}^{2}{(z-6)}^{2}\,k)+(x-4){(y+6)}^{2}{(z-6)}^{3}(-\frac{1}{{(x-4)}^{2}(y+6)(z-6)}\,i-\frac{1}{(x-4){(y+6)}^{2}(z-6)}\,j-\frac{1}{(x-4)(y+6){(z-6)}^{2}}\,k) \\  & =\frac{{(y+6)}^{2}{(z-6)}^{3}}{(x-4)(y+6)(z-6)}\,i+\frac{2(x-4)(y+6){(z-6)}^{3}}{(x-4)(y+6)(z-6)}\,j+\frac{3(x-4){(y+6)}^{2}{(z-6)}^{2}}{(x-4)(y+6)(z-6)}\,k-\frac{(x-4){(y+6)}^{2}{(z-6)}^{3}}{{(x-4)}^{2}(y+6)(z-6)}\,i-\frac{(x-4){(y+6)}^{2}{(z-6)}^{3}}{(x-4){(y+6)}^{2}(z-6)}\,j-\frac{(x-4){(y+6)}^{2}{(z-6)}^{3}}{(x-4)(y+6){(z-6)}^{2}}\,k \\  & =\frac{(y+6){(z-6)}^{2}}{(x-4)}\,i+2{(z-6)}^{2}\,j+3(y+6)(z-6)\,k-\frac{(y+6){(z-6)}^{2}}{(x-4)}\,i-{(z-6)}^{2}\,j-(y+6)(z-6)\,k \\  & ={(z-6)}^{2}\,j+2(y+6)(z-6)\,k.\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -5, "z0": -6}`. Eligible for learning: True.

Find the gradient of the product $f(x,y,z)h(x,y,z),$ given that 

$$
\begin{aligned}f(x,y,z) & =(x-4){(y+5)}^{2}{(z+6)}^{3},\, &  & ∇f(x,y,z)={(y+5)}^{2}{(z+6)}^{3}\,i+2(x-4)(y+5){(z+6)}^{3}\,j+3(x-4){(y+5)}^{2}{(z+6)}^{2}\,k, &  &  \\ h(x,y,z) & =\frac{1}{(x-4)(y+5)(z+6)},\, &  & ∇h(x,y,z)=-\frac{1}{{(x-4)}^{2}(y+5)(z+6)}\,i-\frac{1}{(x-4){(y+5)}^{2}(z+6)}\,j-\frac{1}{(x-4)(y+5){(z+6)}^{2}}\text{ }k. &  & \end{aligned}
$$

- $(\frac{2 \left(y + 5\right) \left(z + 6\right)^{2}}{x - 4})\,i+(\left(z + 6\right)^{2} + \frac{\left(2 y + 10\right) \left(z + 6\right)^{2}}{y + 5})\,j+(4 \left(y + 5\right) \left(z + 6\right))\,k$
- $(\left(z + 6\right)^{2})\,i+(0)\,j+(2 \left(y + 5\right) \left(z + 6\right))\,k$
- $(0)\,i+(\left(z + 6\right)^{2})\,j+(2 \left(y + 5\right) \left(z + 6\right))\,k$
- $(\frac{\left(y + 5\right) \left(z + 6\right)^{2}}{x - 4})\,i+(\frac{\left(2 y + 10\right) \left(z + 6\right)^{2}}{y + 5})\,j+(3 \left(y + 5\right) \left(z + 6\right))\,k$
- $(- \frac{\left(y + 5\right) \left(z + 6\right)^{2}}{x - 4})\,i+(- \left(z + 6\right)^{2})\,j+(- \left(y + 5\right) \left(z + 6\right))\,k$

Worked solution:
The gradient of the product of two functions $f(x,y,z)$ and $h(x,y,z)$ is given by

$$
∇[fh]=h∇f+f∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y,z)h(x,y,z)] & =h(x,y,z)∇f(x,y,z)+f(x,y,z)∇h(x,y,z) \\  & =\frac{1}{(x-4)(y+5)(z+6)}({(y+5)}^{2}{(z+6)}^{3}\,i+2(x-4)(y+5){(z+6)}^{3}\,j+3(x-4){(y+5)}^{2}{(z+6)}^{2}\,k)+(x-4){(y+5)}^{2}{(z+6)}^{3}(-\frac{1}{{(x-4)}^{2}(y+5)(z+6)}\,i-\frac{1}{(x-4){(y+5)}^{2}(z+6)}\,j-\frac{1}{(x-4)(y+5){(z+6)}^{2}}\,k) \\  & =\frac{{(y+5)}^{2}{(z+6)}^{3}}{(x-4)(y+5)(z+6)}\,i+\frac{2(x-4)(y+5){(z+6)}^{3}}{(x-4)(y+5)(z+6)}\,j+\frac{3(x-4){(y+5)}^{2}{(z+6)}^{2}}{(x-4)(y+5)(z+6)}\,k-\frac{(x-4){(y+5)}^{2}{(z+6)}^{3}}{{(x-4)}^{2}(y+5)(z+6)}\,i-\frac{(x-4){(y+5)}^{2}{(z+6)}^{3}}{(x-4){(y+5)}^{2}(z+6)}\,j-\frac{(x-4){(y+5)}^{2}{(z+6)}^{3}}{(x-4)(y+5){(z+6)}^{2}}\,k \\  & =\frac{(y+5){(z+6)}^{2}}{(x-4)}\,i+2{(z+6)}^{2}\,j+3(y+5)(z+6)\,k-\frac{(y+5){(z+6)}^{2}}{(x-4)}\,i-{(z+6)}^{2}\,j-(y+5)(z+6)\,k \\  & ={(z+6)}^{2}\,j+2(y+5)(z+6)\,k.\end{aligned}
$$

### Generated moderate source:q-128529

Parameters: `{"x0": 4, "y0": -5, "z0": -6}`. Eligible for learning: False.

Find the gradient of the product $f(x,y,z)h(x,y,z),$ given that 

$$
\begin{aligned}f(x,y,z) & =(x-4){(y+5)}^{2}{(z+6)}^{3},\, &  & ∇f(x,y,z)={(y+5)}^{2}{(z+6)}^{3}\,i+2(x-4)(y+5){(z+6)}^{3}\,j+3(x-4){(y+5)}^{2}{(z+6)}^{2}\,k, &  &  \\ h(x,y,z) & =\frac{1}{(x-4)(y+5)(z+6)},\, &  & ∇h(x,y,z)=-\frac{1}{{(x-4)}^{2}(y+5)(z+6)}\,i-\frac{1}{(x-4){(y+5)}^{2}(z+6)}\,j-\frac{1}{(x-4)(y+5){(z+6)}^{2}}\text{ }k. &  & \end{aligned}
$$

- ${(z+6)}^{2}\,j+2(y+5)(z+6)\,k$
- ${(y+5)}^{2}\,i+3(x-4)(y+5)\,k$
- $(x-4)\,i-2(x-4)(z+6)\,k$
- $(x-4)\,i-{(z+6)}^{2}\,j-2(y+5)(z+6)\,k$
- $3(x-4)\,i+{(y+5)}^{2}\,j-2(x-4)(y+5)\,k$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $h(x,y)$ is given by

$$
∇[fh]=h∇f+f∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y,z)h(x,y,z)] & =h(x,y,z)∇f(x,y,z)+f(x,y,z)∇h(x,y,z) \\  & =\frac{1}{(x-4)(y+5)(z+6)}({(y+5)}^{2}{(z+6)}^{3}\,i+2(x-4)(y+5){(z+6)}^{3}\,j+3(x-4){(y+5)}^{2}{(z+6)}^{2}\,k)+(x-4){(y+5)}^{2}{(z+6)}^{3}(-\frac{1}{{(x-4)}^{2}(y+5)(z+6)}\,i-\frac{1}{(x-4){(y+5)}^{2}(z+6)}\,j-\frac{1}{(x-4)(y+5){(z+6)}^{2}}\,k) \\  & =\frac{{(y+5)}^{2}{(z+6)}^{3}}{(x-4)(y+5)(z+6)}\,i+\frac{2(x-4)(y+5){(z+6)}^{3}}{(x-4)(y+5)(z+6)}\,j+\frac{3(x-4){(y+5)}^{2}{(z+6)}^{2}}{(x-4)(y+5)(z+6)}\,k-\frac{(x-4){(y+5)}^{2}{(z+6)}^{3}}{{(x-4)}^{2}(y+5)(z+6)}\,i-\frac{(x-4){(y+5)}^{2}{(z+6)}^{3}}{(x-4){(y+5)}^{2}(z+6)}\,j-\frac{(x-4){(y+5)}^{2}{(z+6)}^{3}}{(x-4)(y+5){(z+6)}^{2}}\,k \\  & =\frac{(y+5){(z+6)}^{2}}{(x-4)}\,i+2{(z+6)}^{2}\,j+3(y+5)(z+6)\,k-\frac{(y+5){(z+6)}^{2}}{(x-4)}\,i-{(z+6)}^{2}\,j-(y+5)(z+6)\,k \\  & ={(z+6)}^{2}\,j+2(y+5)(z+6)\,k.\end{aligned}
$$

## Original q-65131 (log; moderate)

Find the gradient of the product $f(x,y)g(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =xy,\, &  & ∇f(x,y)=y\text{ }i+x\text{ }j, &  &  \\ g(x,y) & =\operatorname{ln}⁡(xy),\, &  & ∇g(x,y)=\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j. &  & \end{aligned}
$$

- $y(\operatorname{ln}⁡(xy)+2)\text{ }i+x(\operatorname{ln}⁡(xy)+2)\text{ }j$
- $y(\operatorname{ln}⁡(xy)+1)\text{ }i+x(\operatorname{ln}⁡(xy)+1)\text{ }j$
- $x\operatorname{ln}⁡(xy)\text{ }i-y\operatorname{ln}⁡(xy)\text{ }j$
- $x\operatorname{ln}⁡(xy)\text{ }i+y\operatorname{ln}⁡(xy)\text{ }j$
- $y\operatorname{ln}⁡(xy)\text{ }i+x\operatorname{ln}⁡(xy)\text{ }j$

The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by:

$$
∇[fg]=g\,∇\,f+f\,∇\,g
$$

So, using this product rule we obtain: 

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(\operatorname{ln}⁡(xy))(y\text{ }i+x\text{ }j)+xy(\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j) \\  & =y\operatorname{ln}⁡(xy)\text{ }i+x\operatorname{ln}⁡(xy)\text{ }j+y\text{ }i+x\text{ }j \\  & =[y\operatorname{ln}⁡(xy)\text{ }i+y\text{ }i]+[x\operatorname{ln}⁡(xy)\text{ }j+x\text{ }j] \\  & =y(\operatorname{ln}⁡(xy)+1)\text{ }i+x(\operatorname{ln}⁡(xy)+1)\text{ }j\end{aligned}
$$

### Generated moderate observed

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

Find the gradient of the product $f(x,y)g(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =(x-4)(y+6),\, &  & ∇f(x,y)=(y+6)\text{ }i+(x-4)\text{ }j, &  &  \\ g(x,y) & =\operatorname{ln}⁡((x-4)(y+6)),\, &  & ∇g(x,y)=\frac{1}{(x-4)}\text{ }i+\frac{1}{(y+6)}\text{ }j. &  & \end{aligned}
$$

- $(y+6)(\operatorname{ln}⁡((x-4)(y+6))+1)\text{ }i+(x-4)(\operatorname{ln}⁡((x-4)(y+6))+1)\text{ }j$
- $(x-4)\operatorname{ln}⁡((x-4)(y+6))\text{ }i+(y+6)\operatorname{ln}⁡((x-4)(y+6))\text{ }j$
- $(x-4)\operatorname{ln}⁡((x-4)(y+6))\text{ }i-(y+6)\operatorname{ln}⁡((x-4)(y+6))\text{ }j$
- $(y+6)(\operatorname{ln}⁡((x-4)(y+6))+2)\text{ }i+(x-4)(\operatorname{ln}⁡((x-4)(y+6))+2)\text{ }j$
- $(y+6)\operatorname{ln}⁡((x-4)(y+6))\text{ }i+(x-4)\operatorname{ln}⁡((x-4)(y+6))\text{ }j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by:

$$
∇[fg]=g\,∇\,f+f\,∇\,g
$$

So, using this product rule we obtain: 

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(\operatorname{ln}⁡((x-4)(y+6)))((y+6)\text{ }i+(x-4)\text{ }j)+(x-4)(y+6)(\frac{1}{(x-4)}\text{ }i+\frac{1}{(y+6)}\text{ }j) \\  & =(y+6)\operatorname{ln}⁡((x-4)(y+6))\text{ }i+(x-4)\operatorname{ln}⁡((x-4)(y+6))\text{ }j+(y+6)\text{ }i+(x-4)\text{ }j \\  & =[(y+6)\operatorname{ln}⁡((x-4)(y+6))\text{ }i+(y+6)\text{ }i]+[(x-4)\operatorname{ln}⁡((x-4)(y+6))\text{ }j+(x-4)\text{ }j] \\  & =(y+6)(\operatorname{ln}⁡((x-4)(y+6))+1)\text{ }i+(x-4)(\operatorname{ln}⁡((x-4)(y+6))+1)\text{ }j\end{aligned}
$$

### Generated moderate observed

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: True.

Find the gradient of the product $f(x,y)g(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =(x-4)(y+5),\, &  & ∇f(x,y)=(y+5)\text{ }i+(x-4)\text{ }j, &  &  \\ g(x,y) & =\operatorname{ln}⁡((x-4)(y+5)),\, &  & ∇g(x,y)=\frac{1}{(x-4)}\text{ }i+\frac{1}{(y+5)}\text{ }j. &  & \end{aligned}
$$

- $(y+5)(\operatorname{ln}⁡((x-4)(y+5))+1)\text{ }i+(x-4)(\operatorname{ln}⁡((x-4)(y+5))+1)\text{ }j$
- $(x-4)\operatorname{ln}⁡((x-4)(y+5))\text{ }i+(y+5)\operatorname{ln}⁡((x-4)(y+5))\text{ }j$
- $(y+5)\operatorname{ln}⁡((x-4)(y+5))\text{ }i+(x-4)\operatorname{ln}⁡((x-4)(y+5))\text{ }j$
- $(x-4)\operatorname{ln}⁡((x-4)(y+5))\text{ }i-(y+5)\operatorname{ln}⁡((x-4)(y+5))\text{ }j$
- $(y+5)(\operatorname{ln}⁡((x-4)(y+5))+2)\text{ }i+(x-4)(\operatorname{ln}⁡((x-4)(y+5))+2)\text{ }j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by:

$$
∇[fg]=g\,∇\,f+f\,∇\,g
$$

So, using this product rule we obtain: 

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(\operatorname{ln}⁡((x-4)(y+5)))((y+5)\text{ }i+(x-4)\text{ }j)+(x-4)(y+5)(\frac{1}{(x-4)}\text{ }i+\frac{1}{(y+5)}\text{ }j) \\  & =(y+5)\operatorname{ln}⁡((x-4)(y+5))\text{ }i+(x-4)\operatorname{ln}⁡((x-4)(y+5))\text{ }j+(y+5)\text{ }i+(x-4)\text{ }j \\  & =[(y+5)\operatorname{ln}⁡((x-4)(y+5))\text{ }i+(y+5)\text{ }i]+[(x-4)\operatorname{ln}⁡((x-4)(y+5))\text{ }j+(x-4)\text{ }j] \\  & =(y+5)(\operatorname{ln}⁡((x-4)(y+5))+1)\text{ }i+(x-4)(\operatorname{ln}⁡((x-4)(y+5))+1)\text{ }j\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

Find the gradient of the product $f(x,y)g(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =(x-4)(y+6),\, &  & ∇f(x,y)=(y+6)\text{ }i+(x-4)\text{ }j, &  &  \\ g(x,y) & =\operatorname{ln}⁡((x-4)(y+6)),\, &  & ∇g(x,y)=\frac{1}{(x-4)}\text{ }i+\frac{1}{(y+6)}\text{ }j. &  & \end{aligned}
$$

- $(\left(y + 6\right) \ln{\left(\left(x - 4\right) \left(y + 6\right) \right)})\,i+(\left(x - 4\right) \ln{\left(\left(x - 4\right) \left(y + 6\right) \right)})\,j$
- $(- y + \left(y + 6\right) \ln{\left(\left(x - 4\right) \left(y + 6\right) \right)} - 6)\,i+(- x + \left(x - 4\right) \ln{\left(\left(x - 4\right) \left(y + 6\right) \right)} + 4)\,j$
- $(y + 6)\,i+(x - 4)\,j$
- $(y + \left(y + 6\right) \ln{\left(\left(x - 4\right) \left(y + 6\right) \right)} + 6)\,i+(x + \left(x - 4\right) \ln{\left(\left(x - 4\right) \left(y + 6\right) \right)} - 4)\,j$
- $(x + \left(x - 4\right) \ln{\left(\left(x - 4\right) \left(y + 6\right) \right)} - 4)\,i+(y + \left(y + 6\right) \ln{\left(\left(x - 4\right) \left(y + 6\right) \right)} + 6)\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by:

$$
∇[fg]=g\,∇\,f+f\,∇\,g
$$

So, using this product rule we obtain: 

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(\operatorname{ln}⁡((x-4)(y+6)))((y+6)\text{ }i+(x-4)\text{ }j)+(x-4)(y+6)(\frac{1}{(x-4)}\text{ }i+\frac{1}{(y+6)}\text{ }j) \\  & =(y+6)\operatorname{ln}⁡((x-4)(y+6))\text{ }i+(x-4)\operatorname{ln}⁡((x-4)(y+6))\text{ }j+(y+6)\text{ }i+(x-4)\text{ }j \\  & =[(y+6)\operatorname{ln}⁡((x-4)(y+6))\text{ }i+(y+6)\text{ }i]+[(x-4)\operatorname{ln}⁡((x-4)(y+6))\text{ }j+(x-4)\text{ }j] \\  & =(y+6)(\operatorname{ln}⁡((x-4)(y+6))+1)\text{ }i+(x-4)(\operatorname{ln}⁡((x-4)(y+6))+1)\text{ }j\end{aligned}
$$

## Original q-71476 (cancel; moderate)

Find the gradient of the product $f(x,y)h(x,y),$ given that 

$$
\begin{aligned}f(x,y) & ={x}^{2}y+x{y}^{2},\, &  & ∇f(x,y)=(2xy+{y}^{2})\text{ }i+({x}^{2}+2xy)\text{ }j, &  &  \\ h(x,y) & =\frac{1}{xy},\, &  & ∇h(x,y)=-\frac{1}{{x}^{2}y}\text{ }i-\frac{1}{x{y}^{2}}\text{ }j. &  & \end{aligned}
$$

- $y\text{ }i+x\text{ }j$
- $x\text{ }i+y\text{ }j$
- $\text{ }i+\text{ }j$
- $-\text{ }i+\text{ }j$
- $\text{ }i-\text{ }j$

The gradient of the product of two functions $f(x,y)$ and $h(x,y)$ is given by:

$$
∇[fh]=h\,∇\,f+f\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[f(x,y)h(x,y)] & =h(x,y)∇f(x,y)+f(x,y)∇h(x,y) \\  & =\frac{1}{xy}((2xy+{y}^{2})\text{ }i+({x}^{2}+2xy)\text{ }j)+({x}^{2}y+x{y}^{2})(-\frac{1}{{x}^{2}y}\text{ }i-\frac{1}{x{y}^{2}}\text{ }j) \\  & =(\frac{2xy+{y}^{2}}{xy}\text{ }i+\frac{{x}^{2}+2xy}{xy}\text{ }j)+(-\frac{{x}^{2}y+x{y}^{2}}{{x}^{2}y}\text{ }i-\frac{{x}^{2}y+x{y}^{2}}{x{y}^{2}}\text{ }j) \\  & =(\frac{2x+y}{x}\text{ }i+\frac{x+2y}{y}\text{ }j)+(-\frac{x+y}{x}\text{ }i-\frac{x+y}{y}\text{ }j) \\  & =(-\frac{x+y}{x}+\frac{2x+y}{x})\text{ }i+(-\frac{x+y}{y}+\frac{x+2y}{y})\text{ }j \\  & =\text{ }i+\text{ }j\end{aligned}
$$

### Generated moderate observed

Parameters: `{"a": 2, "b": 3}`. Eligible for learning: True.

Find the gradient of the product $f(x,y)h(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =2{x}^{2}y+3x{y}^{2},\, &  & ∇f(x,y)=(4xy+3{y}^{2})\text{ }i+(2{x}^{2}+6xy)\text{ }j, &  &  \\ h(x,y) & =\frac{1}{xy},\, &  & ∇h(x,y)=-\frac{1}{{x}^{2}y}\text{ }i-\frac{1}{x{y}^{2}}\text{ }j. &  & \end{aligned}
$$

- $2x\text{ }i+3y\text{ }j$
- $-2\text{ }i+3\text{ }j$
- $2\text{ }i+3\text{ }j$
- $2\text{ }i-3\text{ }j$
- $2y\text{ }i+3x\text{ }j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $h(x,y)$ is given by:

$$
∇[fh]=h\,∇\,f+f\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[f(x,y)h(x,y)] & =h(x,y)∇f(x,y)+f(x,y)∇h(x,y) \\  & =\frac{1}{xy}((4xy+3{y}^{2})\text{ }i+(2{x}^{2}+6xy)\text{ }j)+(2{x}^{2}y+3x{y}^{2})(-\frac{1}{{x}^{2}y}\text{ }i-\frac{1}{x{y}^{2}}\text{ }j) \\  & =(\frac{4xy+3{y}^{2}}{xy}\text{ }i+\frac{2{x}^{2}+6xy}{xy}\text{ }j)+(-\frac{2{x}^{2}y+3x{y}^{2}}{{x}^{2}y}\text{ }i-\frac{2{x}^{2}y+3x{y}^{2}}{x{y}^{2}}\text{ }j) \\  & =(\frac{4x+3y}{x}\text{ }i+\frac{2x+6y}{y}\text{ }j)+(-\frac{2x+3y}{x}\text{ }i-\frac{2x+3y}{y}\text{ }j) \\  & =(-\frac{2x+3y}{x}+\frac{4x+3y}{x})\text{ }i+(-\frac{2x+3y}{y}+\frac{2x+6y}{y})\text{ }j \\  & =(2)\,i+(3)\,j\end{aligned}
$$

### Generated moderate observed

Parameters: `{"a": 4, "b": 5}`. Eligible for learning: True.

Find the gradient of the product $f(x,y)h(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =4{x}^{2}y+5x{y}^{2},\, &  & ∇f(x,y)=(8xy+5{y}^{2})\text{ }i+(4{x}^{2}+10xy)\text{ }j, &  &  \\ h(x,y) & =\frac{1}{xy},\, &  & ∇h(x,y)=-\frac{1}{{x}^{2}y}\text{ }i-\frac{1}{x{y}^{2}}\text{ }j. &  & \end{aligned}
$$

- $-4\text{ }i+5\text{ }j$
- $4x\text{ }i+5y\text{ }j$
- $4\text{ }i+5\text{ }j$
- $4\text{ }i-5\text{ }j$
- $4y\text{ }i+5x\text{ }j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $h(x,y)$ is given by:

$$
∇[fh]=h\,∇\,f+f\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[f(x,y)h(x,y)] & =h(x,y)∇f(x,y)+f(x,y)∇h(x,y) \\  & =\frac{1}{xy}((8xy+5{y}^{2})\text{ }i+(4{x}^{2}+10xy)\text{ }j)+(4{x}^{2}y+5x{y}^{2})(-\frac{1}{{x}^{2}y}\text{ }i-\frac{1}{x{y}^{2}}\text{ }j) \\  & =(\frac{8xy+5{y}^{2}}{xy}\text{ }i+\frac{4{x}^{2}+10xy}{xy}\text{ }j)+(-\frac{4{x}^{2}y+5x{y}^{2}}{{x}^{2}y}\text{ }i-\frac{4{x}^{2}y+5x{y}^{2}}{x{y}^{2}}\text{ }j) \\  & =(\frac{8x+5y}{x}\text{ }i+\frac{4x+10y}{y}\text{ }j)+(-\frac{4x+5y}{x}\text{ }i-\frac{4x+5y}{y}\text{ }j) \\  & =(-\frac{4x+5y}{x}+\frac{8x+5y}{x})\text{ }i+(-\frac{4x+5y}{y}+\frac{4x+10y}{y})\text{ }j \\  & =(4)\,i+(5)\,j\end{aligned}
$$

### Generated moderate method

Parameters: `{"a": 2, "b": 3}`. Eligible for learning: True.

Find the gradient of the product $f(x,y)h(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =2{x}^{2}y+3x{y}^{2},\, &  & ∇f(x,y)=(4xy+3{y}^{2})\text{ }i+(2{x}^{2}+6xy)\text{ }j, &  &  \\ h(x,y) & =\frac{1}{xy},\, &  & ∇h(x,y)=-\frac{1}{{x}^{2}y}\text{ }i-\frac{1}{x{y}^{2}}\text{ }j. &  & \end{aligned}
$$

- $(\frac{4 x y + 3 y^{2}}{x y})\,i+(\frac{2 x^{2} + 6 x y}{x y})\,j$
- $(\frac{4 x y + 3 y^{2}}{x y} + \frac{2 x^{2} y + 3 x y^{2}}{x^{2} y})\,i+(\frac{2 x^{2} + 6 x y}{x y} + \frac{2 x^{2} y + 3 x y^{2}}{x y^{2}})\,j$
- $(- \frac{2 x^{2} y + 3 x y^{2}}{x^{2} y})\,i+(- \frac{2 x^{2} y + 3 x y^{2}}{x y^{2}})\,j$
- $(3)\,i+(2)\,j$
- $(2)\,i+(3)\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $h(x,y)$ is given by:

$$
∇[fh]=h\,∇\,f+f\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[f(x,y)h(x,y)] & =h(x,y)∇f(x,y)+f(x,y)∇h(x,y) \\  & =\frac{1}{xy}((4xy+3{y}^{2})\text{ }i+(2{x}^{2}+6xy)\text{ }j)+(2{x}^{2}y+3x{y}^{2})(-\frac{1}{{x}^{2}y}\text{ }i-\frac{1}{x{y}^{2}}\text{ }j) \\  & =(\frac{4xy+3{y}^{2}}{xy}\text{ }i+\frac{2{x}^{2}+6xy}{xy}\text{ }j)+(-\frac{2{x}^{2}y+3x{y}^{2}}{{x}^{2}y}\text{ }i-\frac{2{x}^{2}y+3x{y}^{2}}{x{y}^{2}}\text{ }j) \\  & =(\frac{4x+3y}{x}\text{ }i+\frac{2x+6y}{y}\text{ }j)+(-\frac{2x+3y}{x}\text{ }i-\frac{2x+3y}{y}\text{ }j) \\  & =(-\frac{2x+3y}{x}+\frac{4x+3y}{x})\text{ }i+(-\frac{2x+3y}{y}+\frac{2x+6y}{y})\text{ }j \\  & =(2)\,i+(3)\,j\end{aligned}
$$

## Original q-128532 (exp_linear; moderate)

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{x-y},\, &  & ∇g(x,y)={e}^{x-y}\,i-{e}^{x-y}\,j, &  &  \\ h(x,y) & ={x}^{2}-3xy,\, &  & ∇h(x,y)=(2x-3y)\,i-3x\,j. &  & \end{aligned}
$$

- ${e}^{x-y}(({x}^{2}-3xy+2x-3y)\,i-({x}^{2}-3xy+3x)\,j)$
- ${e}^{x-y}((2x-3y)\,i-3x\,j)$
- ${e}^{x-y}(({x}^{2}-3xy-y)\,i+({x}^{2}+3xy+3x)\,j)$
- ${e}^{x-y}(({x}^{2}-3xy-2x-3y)\,i+({x}^{2}+3xy+3x)\,j)$
- ${e}^{x-y}(({x}^{2}-3xy)\,i-3x\,j)$

The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by

$$
∇[gh]=h∇g+g∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({x}^{2}-3xy)({e}^{x-y}\,i-{e}^{x-y}\,j)+{e}^{x-y}((2x-3y)\,i-3x\,j) \\  & =(({x}^{2}-3xy){e}^{x-y}\,i-({x}^{2}-3xy){e}^{x-y}\,j)+((2x-3y){e}^{x-y}\,i-3x{e}^{x-y}\,j) \\  & ={e}^{x-y}({x}^{2}-3xy+2x-3y)\,i-{e}^{x-y}({x}^{2}-3xy+3x)\,j \\  & ={e}^{x-y}(({x}^{2}-3xy+2x-3y)\,i-({x}^{2}-3xy+3x)\,j).\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{(x-4)-(y+6)},\, &  & ∇g(x,y)={e}^{(x-4)-(y+6)}\,i-{e}^{(x-4)-(y+6)}\,j, &  &  \\ h(x,y) & ={(x-4)}^{2}-3(x-4)(y+6),\, &  & ∇h(x,y)=(2(x-4)-3(y+6))\,i-3(x-4)\,j. &  & \end{aligned}
$$

- $(\left(\left(x - 4\right)^{2} - \left(3 x - 12\right) \left(y + 6\right)\right) e^{x - y - 10})\,i+(- \left(\left(x - 4\right)^{2} - \left(3 x - 12\right) \left(y + 6\right)\right) e^{x - y - 10})\,j$
- $(\left(\left(x - 4\right)^{2} - \left(3 x - 12\right) \left(y + 6\right)\right) e^{x - y - 10} - \left(2 x - 3 y - 26\right) e^{x - y - 10})\,i+(- \left(12 - 3 x\right) e^{x - y - 10} - \left(\left(x - 4\right)^{2} - \left(3 x - 12\right) \left(y + 6\right)\right) e^{x - y - 10})\,j$
- $(\left(2 x - 3 y - 26\right) e^{x - y - 10})\,i+(\left(12 - 3 x\right) e^{x - y - 10})\,j$
- $(\left(x^{2} - 3 x y - 24 x + 9 y + 62\right) e^{x - y - 10})\,i+(\left(- 3 x - \left(x - 4\right)^{2} + 3 \left(x - 4\right) \left(y + 6\right) + 12\right) e^{x - y - 10})\,j$
- $(\left(- 3 x - \left(x - 4\right)^{2} + 3 \left(x - 4\right) \left(y + 6\right) + 12\right) e^{x - y - 10})\,i+(\left(x^{2} - 3 x y - 24 x + 9 y + 62\right) e^{x - y - 10})\,j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by

$$
∇[gh]=h∇g+g∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({(x-4)}^{2}-3(x-4)(y+6))({e}^{(x-4)-(y+6)}\,i-{e}^{(x-4)-(y+6)}\,j)+{e}^{(x-4)-(y+6)}((2(x-4)-3(y+6))\,i-3(x-4)\,j) \\  & =(({(x-4)}^{2}-3(x-4)(y+6)){e}^{(x-4)-(y+6)}\,i-({(x-4)}^{2}-3(x-4)(y+6)){e}^{(x-4)-(y+6)}\,j)+((2(x-4)-3(y+6)){e}^{(x-4)-(y+6)}\,i-3(x-4){e}^{(x-4)-(y+6)}\,j) \\  & ={e}^{(x-4)-(y+6)}({(x-4)}^{2}-3(x-4)(y+6)+2(x-4)-3(y+6))\,i-{e}^{(x-4)-(y+6)}({(x-4)}^{2}-3(x-4)(y+6)+3(x-4))\,j \\  & ={e}^{(x-4)-(y+6)}(({(x-4)}^{2}-3(x-4)(y+6)+2(x-4)-3(y+6))\,i-({(x-4)}^{2}-3(x-4)(y+6)+3(x-4))\,j).\end{aligned}
$$

### Generated moderate source:q-128532

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: False.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{(x-4)-(y+6)},\, &  & ∇g(x,y)={e}^{(x-4)-(y+6)}\,i-{e}^{(x-4)-(y+6)}\,j, &  &  \\ h(x,y) & ={(x-4)}^{2}-3(x-4)(y+6),\, &  & ∇h(x,y)=(2(x-4)-3(y+6))\,i-3(x-4)\,j. &  & \end{aligned}
$$

- ${e}^{(x-4)-(y+6)}((2(x-4)-3(y+6))\,i-3(x-4)\,j)$
- ${e}^{(x-4)-(y+6)}(({(x-4)}^{2}-3(x-4)(y+6)-2(x-4)-3(y+6))\,i+({(x-4)}^{2}+3(x-4)(y+6)+3(x-4))\,j)$
- ${e}^{(x-4)-(y+6)}(({(x-4)}^{2}-3(x-4)(y+6)-(y+6))\,i+({(x-4)}^{2}+3(x-4)(y+6)+3(x-4))\,j)$
- ${e}^{(x-4)-(y+6)}(({(x-4)}^{2}-3(x-4)(y+6))\,i-3(x-4)\,j)$
- ${e}^{(x-4)-(y+6)}(({(x-4)}^{2}-3(x-4)(y+6)+2(x-4)-3(y+6))\,i-({(x-4)}^{2}-3(x-4)(y+6)+3(x-4))\,j)$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by

$$
∇[gh]=h∇g+g∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({(x-4)}^{2}-3(x-4)(y+6))({e}^{(x-4)-(y+6)}\,i-{e}^{(x-4)-(y+6)}\,j)+{e}^{(x-4)-(y+6)}((2(x-4)-3(y+6))\,i-3(x-4)\,j) \\  & =(({(x-4)}^{2}-3(x-4)(y+6)){e}^{(x-4)-(y+6)}\,i-({(x-4)}^{2}-3(x-4)(y+6)){e}^{(x-4)-(y+6)}\,j)+((2(x-4)-3(y+6)){e}^{(x-4)-(y+6)}\,i-3(x-4){e}^{(x-4)-(y+6)}\,j) \\  & ={e}^{(x-4)-(y+6)}({(x-4)}^{2}-3(x-4)(y+6)+2(x-4)-3(y+6))\,i-{e}^{(x-4)-(y+6)}({(x-4)}^{2}-3(x-4)(y+6)+3(x-4))\,j \\  & ={e}^{(x-4)-(y+6)}(({(x-4)}^{2}-3(x-4)(y+6)+2(x-4)-3(y+6))\,i-({(x-4)}^{2}-3(x-4)(y+6)+3(x-4))\,j).\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: True.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{(x-4)-(y+5)},\, &  & ∇g(x,y)={e}^{(x-4)-(y+5)}\,i-{e}^{(x-4)-(y+5)}\,j, &  &  \\ h(x,y) & ={(x-4)}^{2}-3(x-4)(y+5),\, &  & ∇h(x,y)=(2(x-4)-3(y+5))\,i-3(x-4)\,j. &  & \end{aligned}
$$

- $(\left(\left(x - 4\right)^{2} - \left(3 x - 12\right) \left(y + 5\right)\right) e^{x - y - 9})\,i+(- \left(\left(x - 4\right)^{2} - \left(3 x - 12\right) \left(y + 5\right)\right) e^{x - y - 9})\,j$
- $(\left(\left(x - 4\right)^{2} - \left(3 x - 12\right) \left(y + 5\right)\right) e^{x - y - 9} - \left(2 x - 3 y - 23\right) e^{x - y - 9})\,i+(- \left(12 - 3 x\right) e^{x - y - 9} - \left(\left(x - 4\right)^{2} - \left(3 x - 12\right) \left(y + 5\right)\right) e^{x - y - 9})\,j$
- $(\left(- 3 x - \left(x - 4\right)^{2} + 3 \left(x - 4\right) \left(y + 5\right) + 12\right) e^{x - y - 9})\,i+(\left(x^{2} - 3 x y - 21 x + 9 y + 53\right) e^{x - y - 9})\,j$
- $(\left(2 x - 3 y - 23\right) e^{x - y - 9})\,i+(\left(12 - 3 x\right) e^{x - y - 9})\,j$
- $(\left(x^{2} - 3 x y - 21 x + 9 y + 53\right) e^{x - y - 9})\,i+(\left(- 3 x - \left(x - 4\right)^{2} + 3 \left(x - 4\right) \left(y + 5\right) + 12\right) e^{x - y - 9})\,j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by

$$
∇[gh]=h∇g+g∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({(x-4)}^{2}-3(x-4)(y+5))({e}^{(x-4)-(y+5)}\,i-{e}^{(x-4)-(y+5)}\,j)+{e}^{(x-4)-(y+5)}((2(x-4)-3(y+5))\,i-3(x-4)\,j) \\  & =(({(x-4)}^{2}-3(x-4)(y+5)){e}^{(x-4)-(y+5)}\,i-({(x-4)}^{2}-3(x-4)(y+5)){e}^{(x-4)-(y+5)}\,j)+((2(x-4)-3(y+5)){e}^{(x-4)-(y+5)}\,i-3(x-4){e}^{(x-4)-(y+5)}\,j) \\  & ={e}^{(x-4)-(y+5)}({(x-4)}^{2}-3(x-4)(y+5)+2(x-4)-3(y+5))\,i-{e}^{(x-4)-(y+5)}({(x-4)}^{2}-3(x-4)(y+5)+3(x-4))\,j \\  & ={e}^{(x-4)-(y+5)}(({(x-4)}^{2}-3(x-4)(y+5)+2(x-4)-3(y+5))\,i-({(x-4)}^{2}-3(x-4)(y+5)+3(x-4))\,j).\end{aligned}
$$

### Generated moderate source:q-128532

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: False.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{(x-4)-(y+5)},\, &  & ∇g(x,y)={e}^{(x-4)-(y+5)}\,i-{e}^{(x-4)-(y+5)}\,j, &  &  \\ h(x,y) & ={(x-4)}^{2}-3(x-4)(y+5),\, &  & ∇h(x,y)=(2(x-4)-3(y+5))\,i-3(x-4)\,j. &  & \end{aligned}
$$

- ${e}^{(x-4)-(y+5)}(({(x-4)}^{2}-3(x-4)(y+5)-2(x-4)-3(y+5))\,i+({(x-4)}^{2}+3(x-4)(y+5)+3(x-4))\,j)$
- ${e}^{(x-4)-(y+5)}((2(x-4)-3(y+5))\,i-3(x-4)\,j)$
- ${e}^{(x-4)-(y+5)}(({(x-4)}^{2}-3(x-4)(y+5)-(y+5))\,i+({(x-4)}^{2}+3(x-4)(y+5)+3(x-4))\,j)$
- ${e}^{(x-4)-(y+5)}(({(x-4)}^{2}-3(x-4)(y+5))\,i-3(x-4)\,j)$
- ${e}^{(x-4)-(y+5)}(({(x-4)}^{2}-3(x-4)(y+5)+2(x-4)-3(y+5))\,i-({(x-4)}^{2}-3(x-4)(y+5)+3(x-4))\,j)$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by

$$
∇[gh]=h∇g+g∇h.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({(x-4)}^{2}-3(x-4)(y+5))({e}^{(x-4)-(y+5)}\,i-{e}^{(x-4)-(y+5)}\,j)+{e}^{(x-4)-(y+5)}((2(x-4)-3(y+5))\,i-3(x-4)\,j) \\  & =(({(x-4)}^{2}-3(x-4)(y+5)){e}^{(x-4)-(y+5)}\,i-({(x-4)}^{2}-3(x-4)(y+5)){e}^{(x-4)-(y+5)}\,j)+((2(x-4)-3(y+5)){e}^{(x-4)-(y+5)}\,i-3(x-4){e}^{(x-4)-(y+5)}\,j) \\  & ={e}^{(x-4)-(y+5)}({(x-4)}^{2}-3(x-4)(y+5)+2(x-4)-3(y+5))\,i-{e}^{(x-4)-(y+5)}({(x-4)}^{2}-3(x-4)(y+5)+3(x-4))\,j \\  & ={e}^{(x-4)-(y+5)}(({(x-4)}^{2}-3(x-4)(y+5)+2(x-4)-3(y+5))\,i-({(x-4)}^{2}-3(x-4)(y+5)+3(x-4))\,j).\end{aligned}
$$

## Original q-71484 (exp_product; moderate)

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{xy},\, &  & ∇g(x,y)=y{e}^{xy}\text{ }i+x{e}^{xy}\text{ }j, &  &  \\ h(x,y) & ={x}^{2}+{y}^{2},\, &  & ∇h(x,y)=2x\text{ }i+2y\text{ }j. &  & \end{aligned}
$$

- $({x}^{2}+{y}^{2}+2x){e}^{xy}\text{ }i+({x}^{2}+{y}^{2}+2y){e}^{xy}\text{ }j$
- $({x}^{2}y+{y}^{3}){e}^{xy}\text{ }i+({x}^{3}+x{y}^{2}){e}^{xy}\text{ }j$
- $({x}^{2}y+{y}^{3}+2x){e}^{xy}\text{ }i+({x}^{3}+x{y}^{2}+2y){e}^{xy}\text{ }j$
- $({x}^{2}y+{y}^{3}+2x)\text{ }i+({x}^{3}+x{y}^{2}+2y)\text{ }j$
- $2x{e}^{xy}\text{ }i+2y{e}^{xy}\text{ }j$

The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({x}^{2}+{y}^{2})(y{e}^{xy}\text{ }i+x{e}^{xy}\text{ }j)+{e}^{xy}(2x\text{ }i+2y\text{ }j) \\  & =(({x}^{2}+{y}^{2})y{e}^{xy}\text{ }i+({x}^{2}+{y}^{2})x{e}^{xy}\text{ }j)+(2x{e}^{xy}\text{ }i+2y{e}^{xy}\text{ }j) \\  & =({x}^{2}y+{y}^{3}+2x){e}^{xy}\text{ }i+({x}^{3}+x{y}^{2}+2y){e}^{xy}\text{ }j\end{aligned}
$$

### Generated moderate observed

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{(x-4)(y+6)},\, &  & ∇g(x,y)=(y+6){e}^{(x-4)(y+6)}\text{ }i+(x-4){e}^{(x-4)(y+6)}\text{ }j, &  &  \\ h(x,y) & ={(x-4)}^{2}+{(y+6)}^{2},\, &  & ∇h(x,y)=2(x-4)\text{ }i+2(y+6)\text{ }j. &  & \end{aligned}
$$

- $({(x-4)}^{2}(y+6)+{(y+6)}^{3}){e}^{(x-4)(y+6)}\text{ }i+({(x-4)}^{3}+(x-4){(y+6)}^{2}){e}^{(x-4)(y+6)}\text{ }j$
- $({(x-4)}^{2}(y+6)+{(y+6)}^{3}+2(x-4))\text{ }i+({(x-4)}^{3}+(x-4){(y+6)}^{2}+2(y+6))\text{ }j$
- $({(x-4)}^{2}(y+6)+{(y+6)}^{3}+2(x-4)){e}^{(x-4)(y+6)}\text{ }i+({(x-4)}^{3}+(x-4){(y+6)}^{2}+2(y+6)){e}^{(x-4)(y+6)}\text{ }j$
- $({(x-4)}^{2}+{(y+6)}^{2}+2(x-4)){e}^{(x-4)(y+6)}\text{ }i+({(x-4)}^{2}+{(y+6)}^{2}+2(y+6)){e}^{(x-4)(y+6)}\text{ }j$
- $2(x-4){e}^{(x-4)(y+6)}\text{ }i+2(y+6){e}^{(x-4)(y+6)}\text{ }j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({(x-4)}^{2}+{(y+6)}^{2})((y+6){e}^{(x-4)(y+6)}\text{ }i+(x-4){e}^{(x-4)(y+6)}\text{ }j)+{e}^{(x-4)(y+6)}(2(x-4)\text{ }i+2(y+6)\text{ }j) \\  & =(({(x-4)}^{2}+{(y+6)}^{2})(y+6){e}^{(x-4)(y+6)}\text{ }i+({(x-4)}^{2}+{(y+6)}^{2})(x-4){e}^{(x-4)(y+6)}\text{ }j)+(2(x-4){e}^{(x-4)(y+6)}\text{ }i+2(y+6){e}^{(x-4)(y+6)}\text{ }j) \\  & =({(x-4)}^{2}(y+6)+{(y+6)}^{3}+2(x-4)){e}^{(x-4)(y+6)}\text{ }i+({(x-4)}^{3}+(x-4){(y+6)}^{2}+2(y+6)){e}^{(x-4)(y+6)}\text{ }j\end{aligned}
$$

### Generated moderate observed

Parameters: `{"x0": 4, "y0": -5}`. Eligible for learning: True.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{(x-4)(y+5)},\, &  & ∇g(x,y)=(y+5){e}^{(x-4)(y+5)}\text{ }i+(x-4){e}^{(x-4)(y+5)}\text{ }j, &  &  \\ h(x,y) & ={(x-4)}^{2}+{(y+5)}^{2},\, &  & ∇h(x,y)=2(x-4)\text{ }i+2(y+5)\text{ }j. &  & \end{aligned}
$$

- $({(x-4)}^{2}(y+5)+{(y+5)}^{3}){e}^{(x-4)(y+5)}\text{ }i+({(x-4)}^{3}+(x-4){(y+5)}^{2}){e}^{(x-4)(y+5)}\text{ }j$
- $({(x-4)}^{2}(y+5)+{(y+5)}^{3}+2(x-4))\text{ }i+({(x-4)}^{3}+(x-4){(y+5)}^{2}+2(y+5))\text{ }j$
- $2(x-4){e}^{(x-4)(y+5)}\text{ }i+2(y+5){e}^{(x-4)(y+5)}\text{ }j$
- $({(x-4)}^{2}(y+5)+{(y+5)}^{3}+2(x-4)){e}^{(x-4)(y+5)}\text{ }i+({(x-4)}^{3}+(x-4){(y+5)}^{2}+2(y+5)){e}^{(x-4)(y+5)}\text{ }j$
- $({(x-4)}^{2}+{(y+5)}^{2}+2(x-4)){e}^{(x-4)(y+5)}\text{ }i+({(x-4)}^{2}+{(y+5)}^{2}+2(y+5)){e}^{(x-4)(y+5)}\text{ }j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({(x-4)}^{2}+{(y+5)}^{2})((y+5){e}^{(x-4)(y+5)}\text{ }i+(x-4){e}^{(x-4)(y+5)}\text{ }j)+{e}^{(x-4)(y+5)}(2(x-4)\text{ }i+2(y+5)\text{ }j) \\  & =(({(x-4)}^{2}+{(y+5)}^{2})(y+5){e}^{(x-4)(y+5)}\text{ }i+({(x-4)}^{2}+{(y+5)}^{2})(x-4){e}^{(x-4)(y+5)}\text{ }j)+(2(x-4){e}^{(x-4)(y+5)}\text{ }i+2(y+5){e}^{(x-4)(y+5)}\text{ }j) \\  & =({(x-4)}^{2}(y+5)+{(y+5)}^{3}+2(x-4)){e}^{(x-4)(y+5)}\text{ }i+({(x-4)}^{3}+(x-4){(y+5)}^{2}+2(y+5)){e}^{(x-4)(y+5)}\text{ }j\end{aligned}
$$

### Generated moderate method

Parameters: `{"x0": 4, "y0": -6}`. Eligible for learning: True.

Find the gradient of the product $g(x,y)h(x,y),$ given that 

$$
\begin{aligned}g(x,y) & ={e}^{(x-4)(y+6)},\, &  & ∇g(x,y)=(y+6){e}^{(x-4)(y+6)}\text{ }i+(x-4){e}^{(x-4)(y+6)}\text{ }j, &  &  \\ h(x,y) & ={(x-4)}^{2}+{(y+6)}^{2},\, &  & ∇h(x,y)=2(x-4)\text{ }i+2(y+6)\text{ }j. &  & \end{aligned}
$$

- $(\left(y + 6\right) \left(\left(x - 4\right)^{2} + \left(y + 6\right)^{2}\right) e^{\left(x - 4\right) \left(y + 6\right)})\,i+(\left(x - 4\right) \left(\left(x - 4\right)^{2} + \left(y + 6\right)^{2}\right) e^{\left(x - 4\right) \left(y + 6\right)})\,j$
- $(- \left(2 x - 8\right) e^{\left(x - 4\right) \left(y + 6\right)} + \left(y + 6\right) \left(\left(x - 4\right)^{2} + \left(y + 6\right)^{2}\right) e^{\left(x - 4\right) \left(y + 6\right)})\,i+(\left(x - 4\right) \left(\left(x - 4\right)^{2} + \left(y + 6\right)^{2}\right) e^{\left(x - 4\right) \left(y + 6\right)} - \left(2 y + 12\right) e^{\left(x - 4\right) \left(y + 6\right)})\,j$
- $(\left(2 x - 8\right) e^{\left(x - 4\right) \left(y + 6\right)})\,i+(\left(2 y + 12\right) e^{\left(x - 4\right) \left(y + 6\right)})\,j$
- $(\left(2 x + \left(y + 6\right) \left(\left(x - 4\right)^{2} + \left(y + 6\right)^{2}\right) - 8\right) e^{\left(x - 4\right) \left(y + 6\right)})\,i+(\left(2 y + \left(x - 4\right) \left(\left(x - 4\right)^{2} + \left(y + 6\right)^{2}\right) + 12\right) e^{\left(x - 4\right) \left(y + 6\right)})\,j$
- $(\left(2 y + \left(x - 4\right) \left(\left(x - 4\right)^{2} + \left(y + 6\right)^{2}\right) + 12\right) e^{\left(x - 4\right) \left(y + 6\right)})\,i+(\left(2 x + \left(y + 6\right) \left(\left(x - 4\right)^{2} + \left(y + 6\right)^{2}\right) - 8\right) e^{\left(x - 4\right) \left(y + 6\right)})\,j$

Worked solution:
The gradient of the product of two functions $g(x,y)$ and $h(x,y)$ is given by:

$$
∇[gh]=h\,∇\,g+g\,∇\,h
$$

Using the product rule, we obtain:

$$
\begin{aligned}∇[g(x,y)h(x,y)] & =h(x,y)∇g(x,y)+g(x,y)∇h(x,y) \\  & =({(x-4)}^{2}+{(y+6)}^{2})((y+6){e}^{(x-4)(y+6)}\text{ }i+(x-4){e}^{(x-4)(y+6)}\text{ }j)+{e}^{(x-4)(y+6)}(2(x-4)\text{ }i+2(y+6)\text{ }j) \\  & =(({(x-4)}^{2}+{(y+6)}^{2})(y+6){e}^{(x-4)(y+6)}\text{ }i+({(x-4)}^{2}+{(y+6)}^{2})(x-4){e}^{(x-4)(y+6)}\text{ }j)+(2(x-4){e}^{(x-4)(y+6)}\text{ }i+2(y+6){e}^{(x-4)(y+6)}\text{ }j) \\  & =({(x-4)}^{2}(y+6)+{(y+6)}^{3}+2(x-4)){e}^{(x-4)(y+6)}\text{ }i+({(x-4)}^{3}+(x-4){(y+6)}^{2}+2(y+6)){e}^{(x-4)(y+6)}\text{ }j\end{aligned}
$$

## Generated authored easy

Parameters: `{"a": -3, "b": -1, "c": 3, "d": 2}`.

Find the gradient of the product $f(x,y)g(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =- 3 x - y,\quad ∇f(x,y)=(-3)\,i+(-1)\,j \\ g(x,y) & =3 x + 2 y,\quad ∇g(x,y)=(3)\,i+(2)\,j\end{aligned}
$$

- $(- 9 x - 6 y)\,i+(- 3 x - 2 y)\,j$
- $(- 18 x - 9 y)\,i+(- 9 x - 4 y)\,j$
- $(- 3 y)\,i+(3 x)\,j$
- $(- 9 x - 3 y)\,i+(- 6 x - 2 y)\,j$
- $(- 9 x - 4 y)\,i+(- 18 x - 9 y)\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=g∇f+f∇g.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(3 x + 2 y)((-3)\,i+(-1)\,j)+(- 3 x - y)((3)\,i+(2)\,j) \\  & =(3 x + 2 y)(-3)i+(3 x + 2 y)(-1)j+(- 3 x - y)(3)i+(- 3 x - y)(2)j \\  & =(- 9 x - 6 y)i+(- 3 x - 2 y)j+(- 9 x - 3 y)i+(- 6 x - 2 y)j \\  & =(- 18 x - 9 y)\,i+(- 9 x - 4 y)\,j\end{aligned}
$$

## Generated authored easy

Parameters: `{"a": -4, "b": 1, "c": -1, "d": -1}`.

Find the gradient of the product $f(x,y)g(x,y),$ given that 

$$
\begin{aligned}f(x,y) & =- 4 x + y,\quad ∇f(x,y)=(-4)\,i+(1)\,j \\ g(x,y) & =- x - y,\quad ∇g(x,y)=(-1)\,i+(-1)\,j\end{aligned}
$$

- $(3 x - 2 y)\,i+(8 x + 3 y)\,j$
- $(5 y)\,i+(- 5 x)\,j$
- $(4 x - y)\,i+(4 x - y)\,j$
- $(8 x + 3 y)\,i+(3 x - 2 y)\,j$
- $(4 x + 4 y)\,i+(- x - y)\,j$

Worked solution:
The gradient of the product of two functions $f(x,y)$ and $g(x,y)$ is given by

$$
∇[fg]=g∇f+f∇g.
$$

Using the product rule, we obtain

$$
\begin{aligned}∇[f(x,y)g(x,y)] & =g(x,y)∇f(x,y)+f(x,y)∇g(x,y) \\  & =(- x - y)((-4)\,i+(1)\,j)+(- 4 x + y)((-1)\,i+(-1)\,j) \\  & =(- x - y)(-4)i+(- x - y)(1)j+(- 4 x + y)(-1)i+(- 4 x + y)(-1)j \\  & =(4 x + 4 y)i+(- x - y)j+(4 x - y)i+(4 x - y)j \\  & =(8 x + 3 y)\,i+(3 x - 2 y)\,j\end{aligned}
$$

