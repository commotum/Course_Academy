# Original questions and generated variants

Captured math basis 1356; source originals precede each template group. Generated entries explicitly identify authored banks and coefficient extensions.


## Original q-4019

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{y}^{2}}$ that satisfies $y(2)=\sqrt[3]{13}.$

- ${y}^{3}=\frac{1}{3}{x}^{2}-1$
- ${y}^{3}={x}^{2}+\frac{1}{3}$
- ${y}^{3}=3{x}^{2}+1$
- ${y}^{3}=\frac{1}{6}{x}^{2}+1$
- ${y}^{3}={x}^{2}+1$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2x}{{y}^{2}} \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2x \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int 2x\,\text{d}x \\ \frac{{y}^{3}}{3} & ={x}^{2}+{C}_{1} \\ {y}^{3} & =3{x}^{2}+3{C}_{1}.\end{aligned}
$$

We conclude that the general solution is

$$
{y}^{3}=3{x}^{2}+C,
$$

where $C=3{C}_{1}$  is an arbitrary constant.

We now apply the condition $y(2)=\sqrt[3]{13}$ to find $C:$

$$
\begin{aligned}{(\sqrt[3]{13})}^{3} & =3(2)^{2}+C \\ 13 & =12+C \\ C & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{y}^{2}}$ that satisfies the condition $y(2)=\sqrt[3]{13}$ is

$$
{y}^{3}=3{x}^{2}+1.
$$

### Generated easy — source_4019 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{y}^{2}}$ that satisfies $y(2)=\sqrt[3]{13}.$

- ${y}^{3}=3{x}^{2}+1$
- ${y}^{3}={x}^{2}+\frac{1}{3}$
- ${y}^{3}=\frac{1}{3}{x}^{2}-1$
- ${y}^{3}={x}^{2}+1$
- ${y}^{3}=\frac{1}{6}{x}^{2}+1$

Correct: ${y}^{3}=3{x}^{2}+1$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2x}{{y}^{2}} \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2x \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int 2x\,\text{d}x \\ \frac{{y}^{3}}{3} & ={x}^{2}+{C}_{1} \\ {y}^{3} & =3{x}^{2}+3{C}_{1}.\end{aligned}
$$

We conclude that the general solution is

$$
{y}^{3}=3{x}^{2}+C,
$$

where $C=3{C}_{1}$  is an arbitrary constant.

We now apply the condition $y(2)=\sqrt[3]{13}$ to find $C:$

$$
\begin{aligned}{(\sqrt[3]{13})}^{3} & =3(2)^{2}+C \\ 13 & =12+C \\ C & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{y}^{2}}$ that satisfies the condition $y(2)=\sqrt[3]{13}$ is

$$
{y}^{3}=3{x}^{2}+1.
$$

Author domain: y != 0; connected interval containing initial x, with (x-h)^2*3+1 != 0

### Generated easy — source_4019 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2\left(x + 2\right)}{{y}^{2}}$ that satisfies $y(0)=\sqrt[3]{13}.$

- $y^{3}=\left(x + 2\right)^{2} + 1$
- $y^{3}=3 \left(x + 2\right)^{2} + 1$
- $y^{3}=3 \left(x + 2\right)^{2} - 1$
- $y^{3}=3 \left(x + 2\right)^{2} + 13$
- $y^{3}=\frac{\left(x + 2\right)^{2}}{3} + 1$

Correct: $y^{3}=3 \left(x + 2\right)^{2} + 1$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2\left(x + 2\right)}{{y}^{2}} \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2\left(x + 2\right) \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\left(x + 2\right)\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int 2\left(x + 2\right)\,\text{d}x \\ \frac{{y}^{3}}{3} & ={\left(x + 2\right)}^{2}+{C}_{1} \\ {y}^{3} & =3{\left(x + 2\right)}^{2}+3{C}_{1}.\end{aligned}
$$

We conclude that the general solution is

$$
{y}^{3}=3{\left(x + 2\right)}^{2}+C,
$$

where $C=3{C}_{1}$  is an arbitrary constant.

We now apply the condition $y(0)=\sqrt[3]{13}$ to find $C:$

$$
\begin{aligned}{(\sqrt[3]{13})}^{3} & =3(2)^{2}+C \\ 13 & =12+C \\ C & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{2\left(x + 2\right)}{{y}^{2}}$ that satisfies the condition $y(0)=\sqrt[3]{13}$ is

$$
{y}^{3}=3{\left(x + 2\right)}^{2}+1.
$$

Author domain: y != 0; connected interval containing initial x, with (x-h)^2*3+1 != 0

### Generated easy — source_4019 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2\left(x - \frac{1}{2}\right)}{{y}^{2}}$ that satisfies $y(\frac{5}{2})=\sqrt[3]{13}.$

- $y^{3}=\left(x - \frac{1}{2}\right)^{2} + 1$
- $y^{3}=3 x^{2} - 3 x + \frac{7}{4}$
- $y^{3}=3 \left(x - \frac{1}{2}\right)^{2} - 1$
- $y^{3}=3 \left(x - \frac{1}{2}\right)^{2} + 13$
- $y^{3}=\frac{\left(x - \frac{1}{2}\right)^{2}}{3} + 1$

Correct: $y^{3}=3 x^{2} - 3 x + \frac{7}{4}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2\left(x - \frac{1}{2}\right)}{{y}^{2}} \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2\left(x - \frac{1}{2}\right) \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\left(x - \frac{1}{2}\right)\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int 2\left(x - \frac{1}{2}\right)\,\text{d}x \\ \frac{{y}^{3}}{3} & ={\left(x - \frac{1}{2}\right)}^{2}+{C}_{1} \\ {y}^{3} & =3{\left(x - \frac{1}{2}\right)}^{2}+3{C}_{1}.\end{aligned}
$$

We conclude that the general solution is

$$
{y}^{3}=3{\left(x - \frac{1}{2}\right)}^{2}+C,
$$

where $C=3{C}_{1}$  is an arbitrary constant.

We now apply the condition $y(\frac{5}{2})=\sqrt[3]{13}$ to find $C:$

$$
\begin{aligned}{(\sqrt[3]{13})}^{3} & =3(2)^{2}+C \\ 13 & =12+C \\ C & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{2\left(x - \frac{1}{2}\right)}{{y}^{2}}$ that satisfies the condition $y(\frac{5}{2})=\sqrt[3]{13}$ is

$$
{y}^{3}=3{\left(x - \frac{1}{2}\right)}^{2}+1.
$$

Author domain: y != 0; connected interval containing initial x, with (x-h)^2*3+1 != 0

### Generated easy — source_4019 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2\left(x - 3\right)}{{y}^{2}}$ that satisfies $y(5)=\sqrt[3]{13}.$

- $y^{3}=\left(x - 3\right)^{2} + 1$
- $y^{3}=3 \left(x - 3\right)^{2} + 1$
- $y^{3}=3 \left(x - 3\right)^{2} - 1$
- $y^{3}=3 \left(x - 3\right)^{2} + 13$
- $y^{3}=\frac{\left(x - 3\right)^{2}}{3} + 1$

Correct: $y^{3}=3 \left(x - 3\right)^{2} + 1$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2\left(x - 3\right)}{{y}^{2}} \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2\left(x - 3\right) \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\left(x - 3\right)\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int 2\left(x - 3\right)\,\text{d}x \\ \frac{{y}^{3}}{3} & ={\left(x - 3\right)}^{2}+{C}_{1} \\ {y}^{3} & =3{\left(x - 3\right)}^{2}+3{C}_{1}.\end{aligned}
$$

We conclude that the general solution is

$$
{y}^{3}=3{\left(x - 3\right)}^{2}+C,
$$

where $C=3{C}_{1}$  is an arbitrary constant.

We now apply the condition $y(5)=\sqrt[3]{13}$ to find $C:$

$$
\begin{aligned}{(\sqrt[3]{13})}^{3} & =3(2)^{2}+C \\ 13 & =12+C \\ C & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{2\left(x - 3\right)}{{y}^{2}}$ that satisfies the condition $y(5)=\sqrt[3]{13}$ is

$$
{y}^{3}=3{\left(x - 3\right)}^{2}+1.
$$

Author domain: y != 0; connected interval containing initial x, with (x-h)^2*3+1 != 0

## Original q-8310

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{x}$ that satisfies $y(1)=2.$ Assume that $x>0.$

- $y=\frac{2}{\operatorname{ln}⁡x-1}$
- $y=\frac{2}{1-2\operatorname{ln}⁡x}$
- $y=\frac{2}{\operatorname{ln}⁡x+1}$
- $y=\frac{2}{2\operatorname{ln}⁡x+1}$
- $y=\frac{2}{\operatorname{ln}⁡x-2}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{x} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{x} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{x}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{x}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{ln}⁡|x|+C \\ \frac{1}{y} & =-(\operatorname{ln}⁡|x|+C) \\ y & =-\frac{1}{\operatorname{ln}⁡|x|+C}\,.\end{aligned}
$$

Assuming $x>0,$ the general solution is

$$
y=-\frac{1}{\operatorname{ln}⁡x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=2$ to find $C:$

$$
\begin{aligned}y(1) & =2 \\ -\frac{1}{\operatorname{ln}⁡1+C} & =2 \\ -\frac{1}{C} & =2 \\ C & =-\frac{1}{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{x}$ that satisfies the condition $y(1)=2$ is

$$
y=\frac{-1}{(\operatorname{ln}⁡x-\frac{1}{2})}=\frac{2}{1-2\operatorname{ln}⁡x}\,.
$$

### Generated easy — source_8310 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{x}$ that satisfies $y(1)=2.$ Assume that $x>0.$

- $y=\frac{2}{\operatorname{ln}⁡x+1}$
- $y=\frac{2}{1-2\operatorname{ln}⁡x}$
- $y=\frac{2}{\operatorname{ln}⁡x-1}$
- $y=\frac{2}{\operatorname{ln}⁡x-2}$
- $y=\frac{2}{2\operatorname{ln}⁡x+1}$

Correct: $y=\frac{2}{1-2\operatorname{ln}⁡x}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{x} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{x} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{x}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{x}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{ln}⁡|x|+C \\ \frac{1}{y} & =-(\operatorname{ln}⁡|x|+C) \\ y & =-\frac{1}{\operatorname{ln}⁡|x|+C}\,.\end{aligned}
$$

Assuming $x>0,$ the general solution is

$$
y=-\frac{1}{\operatorname{ln}⁡x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=2$ to find $C:$

$$
\begin{aligned}y(1) & =2 \\ -\frac{1}{\operatorname{ln}⁡1+C} & =2 \\ -\frac{1}{C} & =2 \\ C & =-\frac{1}{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{x}$ that satisfies the condition $y(1)=2$ is

$$
y=\frac{-1}{(\operatorname{ln}⁡x-\frac{1}{2})}=\frac{2}{1-2\operatorname{ln}⁡x}\,.
$$

Author domain: x-h > 0; 1-2*log(x-h) != 0; connected interval containing h+1

### Generated easy — source_8310 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{\left(x + 2\right)}$ that satisfies $y(-1)=2.$ Assume that $\left(x + 2\right)>0.$

- $y=\frac{2}{2 \log{\left(x + 2 \right)} + 1}$
- $y=- \frac{2}{2 \log{\left(x + 2 \right)} - 1}$
- $y=\frac{2}{- 2 \log{\left(x + 2 \right)} + 2}$
- $y=- 4 \log{\left(x + 2 \right)} + 2$
- $y=\frac{2}{- \log{\left(x + 2 \right)} + 1}$

Correct: $y=- \frac{2}{2 \log{\left(x + 2 \right)} - 1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{\left(x + 2\right)} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\left(x + 2\right)} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\left(x + 2\right)}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{\left(x + 2\right)}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{ln}⁡|\left(x + 2\right)|+C \\ \frac{1}{y} & =-(\operatorname{ln}⁡|\left(x + 2\right)|+C) \\ y & =-\frac{1}{\operatorname{ln}⁡|\left(x + 2\right)|+C}\,.\end{aligned}
$$

Assuming $\left(x + 2\right)>0,$ the general solution is

$$
y=-\frac{1}{\operatorname{ln}⁡\left(x + 2\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-1)=2$ to find $C:$

$$
\begin{aligned}y(-1) & =2 \\ -\frac{1}{\operatorname{ln}⁡1+C} & =2 \\ -\frac{1}{C} & =2 \\ C & =-\frac{1}{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{\left(x + 2\right)}$ that satisfies the condition $y(-1)=2$ is

$$
y=\frac{-1}{(\operatorname{ln}⁡\left(x + 2\right)-\frac{1}{2})}=\frac{2}{1-2\operatorname{ln}⁡\left(x + 2\right)}\,.
$$

Author domain: x-h > 0; 1-2*log(x-h) != 0; connected interval containing h+1

### Generated easy — source_8310 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{\left(x - \frac{1}{2}\right)}$ that satisfies $y(\frac{3}{2})=2.$ Assume that $\left(x - \frac{1}{2}\right)>0.$

- $y=\frac{2}{2 \log{\left(x - \frac{1}{2} \right)} + 1}$
- $y=- \frac{2}{2 \log{\left(x - \frac{1}{2} \right)} - 1}$
- $y=\frac{2}{- 2 \log{\left(x - \frac{1}{2} \right)} + 2}$
- $y=- 4 \log{\left(x - \frac{1}{2} \right)} + 2$
- $y=\frac{2}{- \log{\left(x - \frac{1}{2} \right)} + 1}$

Correct: $y=- \frac{2}{2 \log{\left(x - \frac{1}{2} \right)} - 1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{\left(x - \frac{1}{2}\right)} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\left(x - \frac{1}{2}\right)} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\left(x - \frac{1}{2}\right)}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{\left(x - \frac{1}{2}\right)}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{ln}⁡|\left(x - \frac{1}{2}\right)|+C \\ \frac{1}{y} & =-(\operatorname{ln}⁡|\left(x - \frac{1}{2}\right)|+C) \\ y & =-\frac{1}{\operatorname{ln}⁡|\left(x - \frac{1}{2}\right)|+C}\,.\end{aligned}
$$

Assuming $\left(x - \frac{1}{2}\right)>0,$ the general solution is

$$
y=-\frac{1}{\operatorname{ln}⁡\left(x - \frac{1}{2}\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(\frac{3}{2})=2$ to find $C:$

$$
\begin{aligned}y(\frac{3}{2}) & =2 \\ -\frac{1}{\operatorname{ln}⁡1+C} & =2 \\ -\frac{1}{C} & =2 \\ C & =-\frac{1}{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{\left(x - \frac{1}{2}\right)}$ that satisfies the condition $y(\frac{3}{2})=2$ is

$$
y=\frac{-1}{(\operatorname{ln}⁡\left(x - \frac{1}{2}\right)-\frac{1}{2})}=\frac{2}{1-2\operatorname{ln}⁡\left(x - \frac{1}{2}\right)}\,.
$$

Author domain: x-h > 0; 1-2*log(x-h) != 0; connected interval containing h+1

### Generated easy — source_8310 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{\left(x - 3\right)}$ that satisfies $y(4)=2.$ Assume that $\left(x - 3\right)>0.$

- $y=\frac{2}{2 \log{\left(x - 3 \right)} + 1}$
- $y=- \frac{2}{2 \log{\left(x - 3 \right)} - 1}$
- $y=\frac{2}{- 2 \log{\left(x - 3 \right)} + 2}$
- $y=- 4 \log{\left(x - 3 \right)} + 2$
- $y=\frac{2}{- \log{\left(x - 3 \right)} + 1}$

Correct: $y=- \frac{2}{2 \log{\left(x - 3 \right)} - 1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{\left(x - 3\right)} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\left(x - 3\right)} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\left(x - 3\right)}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{\left(x - 3\right)}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{ln}⁡|\left(x - 3\right)|+C \\ \frac{1}{y} & =-(\operatorname{ln}⁡|\left(x - 3\right)|+C) \\ y & =-\frac{1}{\operatorname{ln}⁡|\left(x - 3\right)|+C}\,.\end{aligned}
$$

Assuming $\left(x - 3\right)>0,$ the general solution is

$$
y=-\frac{1}{\operatorname{ln}⁡\left(x - 3\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(4)=2$ to find $C:$

$$
\begin{aligned}y(4) & =2 \\ -\frac{1}{\operatorname{ln}⁡1+C} & =2 \\ -\frac{1}{C} & =2 \\ C & =-\frac{1}{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{\left(x - 3\right)}$ that satisfies the condition $y(4)=2$ is

$$
y=\frac{-1}{(\operatorname{ln}⁡\left(x - 3\right)-\frac{1}{2})}=\frac{2}{1-2\operatorname{ln}⁡\left(x - 3\right)}\,.
$$

Author domain: x-h > 0; 1-2*log(x-h) != 0; connected interval containing h+1

## Original q-168078

Let $\overset{^}{T}(t)$ be a particular solution of the differential equation from the previous part that satisfies the condition $\overset{^}{T}(0)=28.$ Find $\overset{^}{T}(t).$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $\overset{^}{T}(t)\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

- $25+3{e}^{-0.03t}$

Previously, we found that the general solution is

$$
T=25+K{e}^{-0.03t}.
$$

where $K$ is an arbitrary constant.

We now apply the condition $T(0)=28$ to find $K:$

$$
\begin{aligned}28 & =25+K\,{e}^{-0.03(0)} \\ 28 & =25+K\,{e}^{0} \\ K & =3\end{aligned}
$$

Thus, the required particular solution is

$$
\overset{^}{T}(t)=25+3{e}^{-0.03t}.
$$

### Generated easy — source_168078 (observed)

Let $\overset{^}{T}(t)$ be a particular solution of the differential equation from the previous part that satisfies the condition $\overset{^}{T}(0)=28.$ Find $\overset{^}{T}(t).$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $\overset{^}{T}(t)\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

- $25+3{e}^{-0.03t}$

Correct: $25+3{e}^{-0.03t}$

Worked solution:
Previously, we found that the general solution is

$$
T=25+K{e}^{-0.03t}.
$$

where $K$ is an arbitrary constant.

We now apply the condition $T(0)=28$ to find $K:$

$$
\begin{aligned}28 & =25+K\,{e}^{-0.03(0)} \\ 28 & =25+K\,{e}^{0} \\ K & =3\end{aligned}
$$

Thus, the required particular solution is

$$
\overset{^}{T}(t)=25+3{e}^{-0.03t}.
$$

Author domain: time t; positive decay rate 0.03; initial time 0

### Generated easy — source_168078 (blank)

The general solution of the differential equation is $T=23+Ke^{-0.03t}.$

Let $\overset{^}{T}(t)$ be a particular solution of the differential equation from the previous part that satisfies the condition $\overset{^}{T}(0)=26.$ Find $\overset{^}{T}(t).$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $\overset{^}{T}(t)\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

- $23+3{e}^{-0.03t}$

Correct: $23+3{e}^{-0.03t}$

Worked solution:
Previously, we found that the general solution is

$$
T=23+K{e}^{-0.03t}.
$$

where $K$ is an arbitrary constant.

We now apply the condition $T(0)=26$ to find $K:$

$$
\begin{aligned}26 & =23+K\,{e}^{-0.03(0)} \\ 26 & =23+K\,{e}^{0} \\ K & =3\end{aligned}
$$

Thus, the required particular solution is

$$
\overset{^}{T}(t)=23+3{e}^{-0.03t}.
$$

Author domain: time t; positive decay rate 0.03; initial time 0

### Generated easy — source_168078 (blank)

The general solution of the differential equation is $T=\frac{51}{2}+Ke^{-0.03t}.$

Let $\overset{^}{T}(t)$ be a particular solution of the differential equation from the previous part that satisfies the condition $\overset{^}{T}(0)=\frac{57}{2}.$ Find $\overset{^}{T}(t).$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $\overset{^}{T}(t)\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

- $\frac{51}{2}+3{e}^{-0.03t}$

Correct: $\frac{51}{2}+3{e}^{-0.03t}$

Worked solution:
Previously, we found that the general solution is

$$
T=\frac{51}{2}+K{e}^{-0.03t}.
$$

where $K$ is an arbitrary constant.

We now apply the condition $T(0)=\frac{57}{2}$ to find $K:$

$$
\begin{aligned}\frac{57}{2} & =\frac{51}{2}+K\,{e}^{-0.03(0)} \\ \frac{57}{2} & =\frac{51}{2}+K\,{e}^{0} \\ K & =3\end{aligned}
$$

Thus, the required particular solution is

$$
\overset{^}{T}(t)=\frac{51}{2}+3{e}^{-0.03t}.
$$

Author domain: time t; positive decay rate 0.03; initial time 0

### Generated easy — source_168078 (blank)

The general solution of the differential equation is $T=28+Ke^{-0.03t}.$

Let $\overset{^}{T}(t)$ be a particular solution of the differential equation from the previous part that satisfies the condition $\overset{^}{T}(0)=31.$ Find $\overset{^}{T}(t).$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $\overset{^}{T}(t)\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

- $28+3{e}^{-0.03t}$

Correct: $28+3{e}^{-0.03t}$

Worked solution:
Previously, we found that the general solution is

$$
T=28+K{e}^{-0.03t}.
$$

where $K$ is an arbitrary constant.

We now apply the condition $T(0)=31$ to find $K:$

$$
\begin{aligned}31 & =28+K\,{e}^{-0.03(0)} \\ 31 & =28+K\,{e}^{0} \\ K & =3\end{aligned}
$$

Thus, the required particular solution is

$$
\overset{^}{T}(t)=28+3{e}^{-0.03t}.
$$

Author domain: time t; positive decay rate 0.03; initial time 0

## Original q-104055

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡y}$ that satisfies $y(0)=\frac{\pi }{2}.$

- $\operatorname{cos}⁡2y=-2x+1$
- $\operatorname{sin}⁡y=-2x$
- $\operatorname{sin}⁡y=x$
- $\operatorname{cos}⁡y=x+1$
- $\operatorname{cos}⁡y=-x$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\operatorname{sin}⁡y} \\ \operatorname{sin}⁡y\frac{\text{d}y}{\text{d}x} & =1 \\ \int \operatorname{sin}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \operatorname{sin}⁡y\,\text{d}y & =\int \,\text{d}x \\ -\operatorname{cos}⁡y & =x+C \\ \operatorname{cos}⁡y & =-x-C.\end{aligned}
$$

We now apply the condition $y(0)=\frac{\pi }{2}$ to find $C:$

$$
\begin{aligned}\operatorname{cos}⁡(\frac{\pi }{2}) & =-0-C \\ 0 & =0-C \\ C & =0\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\operatorname{cos}⁡y=-x
$$

### Generated easy — source_104055 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡y}$ that satisfies $y(0)=\frac{\pi }{2}.$

- $\operatorname{sin}⁡y=x$
- $\operatorname{sin}⁡y=-2x$
- $\operatorname{cos}⁡2y=-2x+1$
- $\operatorname{cos}⁡y=-x$
- $\operatorname{cos}⁡y=x+1$

Correct: $\operatorname{cos}⁡y=-x$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\operatorname{sin}⁡y} \\ \operatorname{sin}⁡y\frac{\text{d}y}{\text{d}x} & =1 \\ \int \operatorname{sin}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \operatorname{sin}⁡y\,\text{d}y & =\int \,\text{d}x \\ -\operatorname{cos}⁡y & =x+C \\ \operatorname{cos}⁡y & =-x-C.\end{aligned}
$$

We now apply the condition $y(0)=\frac{\pi }{2}$ to find $C:$

$$
\begin{aligned}\operatorname{cos}⁡(\frac{\pi }{2}) & =-0-C \\ 0 & =0-C \\ C & =0\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\operatorname{cos}⁡y=-x
$$

Author domain: local branch 0<y<pi; |x-h|<1, initial y=pi/2

### Generated easy — source_104055 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡y}$ that satisfies $y(-2)=\frac{\pi }{2}.$

- $\cos{\left(y \right)}=x + 2$
- $\cos{\left(y \right)}=- x - 2$
- $\cos{\left(y \right)}=- x - 2 + \frac{\pi}{2}$
- $\cos{\left(y \right)}=- 2 x - 4$
- $\cos{\left(y \right)}=x + 3$

Correct: $\cos{\left(y \right)}=- x - 2$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\operatorname{sin}⁡y} \\ \operatorname{sin}⁡y\frac{\text{d}y}{\text{d}x} & =1 \\ \int \operatorname{sin}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \operatorname{sin}⁡y\,\text{d}y & =\int \,\text{d}x \\ -\operatorname{cos}⁡y & =\left(x + 2\right)+C \\ \operatorname{cos}⁡y & =-\left(x + 2\right)-C.\end{aligned}
$$

We now apply the condition $y(-2)=\frac{\pi }{2}$ to find $C:$

$$
\begin{aligned}\operatorname{cos}⁡(\frac{\pi }{2}) & =-0-C \\ 0 & =0-C \\ C & =0\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\operatorname{cos}⁡y=-\left(x + 2\right)
$$

Author domain: local branch 0<y<pi; |x-h|<1, initial y=pi/2

### Generated easy — source_104055 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡y}$ that satisfies $y(\frac{1}{2})=\frac{\pi }{2}.$

- $\cos{\left(y \right)}=x - \frac{1}{2}$
- $\cos{\left(y \right)}=- x + \frac{1}{2}$
- $\cos{\left(y \right)}=- x + \frac{1}{2} + \frac{\pi}{2}$
- $\cos{\left(y \right)}=- 2 x + 1$
- $\cos{\left(y \right)}=x + \frac{1}{2}$

Correct: $\cos{\left(y \right)}=- x + \frac{1}{2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\operatorname{sin}⁡y} \\ \operatorname{sin}⁡y\frac{\text{d}y}{\text{d}x} & =1 \\ \int \operatorname{sin}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \operatorname{sin}⁡y\,\text{d}y & =\int \,\text{d}x \\ -\operatorname{cos}⁡y & =\left(x - \frac{1}{2}\right)+C \\ \operatorname{cos}⁡y & =-\left(x - \frac{1}{2}\right)-C.\end{aligned}
$$

We now apply the condition $y(\frac{1}{2})=\frac{\pi }{2}$ to find $C:$

$$
\begin{aligned}\operatorname{cos}⁡(\frac{\pi }{2}) & =-0-C \\ 0 & =0-C \\ C & =0\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\operatorname{cos}⁡y=-\left(x - \frac{1}{2}\right)
$$

Author domain: local branch 0<y<pi; |x-h|<1, initial y=pi/2

### Generated easy — source_104055 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡y}$ that satisfies $y(3)=\frac{\pi }{2}.$

- $\cos{\left(y \right)}=x - 3$
- $\cos{\left(y \right)}=- x + 3$
- $\cos{\left(y \right)}=- x + \frac{\pi}{2} + 3$
- $\cos{\left(y \right)}=- 2 x + 6$
- $\cos{\left(y \right)}=x - 2$

Correct: $\cos{\left(y \right)}=- x + 3$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\operatorname{sin}⁡y} \\ \operatorname{sin}⁡y\frac{\text{d}y}{\text{d}x} & =1 \\ \int \operatorname{sin}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \operatorname{sin}⁡y\,\text{d}y & =\int \,\text{d}x \\ -\operatorname{cos}⁡y & =\left(x - 3\right)+C \\ \operatorname{cos}⁡y & =-\left(x - 3\right)-C.\end{aligned}
$$

We now apply the condition $y(3)=\frac{\pi }{2}$ to find $C:$

$$
\begin{aligned}\operatorname{cos}⁡(\frac{\pi }{2}) & =-0-C \\ 0 & =0-C \\ C & =0\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\operatorname{cos}⁡y=-\left(x - 3\right)
$$

Author domain: local branch 0<y<pi; |x-h|<1, initial y=pi/2

## Original q-14310

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ given that  $y(\frac{\pi }{2})=1.$

- $y=\operatorname{tan}⁡(x-\frac{\pi }{4})$
- $y=\operatorname{cot}⁡(x-\frac{\pi }{4})$
- $y=\operatorname{tan}⁡(x+\frac{\pi }{4})$
- $y=\operatorname{tan}⁡(x+\frac{\pi }{2})$
- $y=\operatorname{cot}⁡(x+\frac{\pi }{2})$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}={y}^{2}+1 \\ \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{arctan}⁡(y) & =x+C \\ y & =\operatorname{tan}⁡(x+C).\end{aligned}
$$

We conclude that the general solution is

$$
y=\operatorname{tan}⁡(x+C).
$$

We now apply the condition $y(\frac{\pi }{2})=1$ to find $C$:

$$
\begin{aligned}1 & =\operatorname{tan}⁡(\frac{\pi }{2}+C) \\ \operatorname{arctan}⁡(1) & =\frac{\pi }{2}+C \\ \frac{\pi }{4} & =\frac{\pi }{2}+C \\ C & =\frac{\pi }{4}-\frac{\pi }{2} \\ C & =-\frac{\pi }{4}.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ that satisfies the condition $y(\frac{\pi }{2})=1$ is

$$
y=\operatorname{tan}⁡(x-\frac{\pi }{4}).
$$

### Generated hard — source_14310 (observed)

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ given that  $y(\frac{\pi}{2})=1.$

- $y=\operatorname{tan}⁡(x+\frac{\pi }{4})$
- $y=\operatorname{cot}⁡(x-\frac{\pi }{4})$
- $y=\operatorname{tan}⁡(x-\frac{\pi }{4})$
- $y=\operatorname{cot}⁡(x+\frac{\pi }{2})$
- $y=\operatorname{tan}⁡(x+\frac{\pi }{2})$

Correct: $y=\operatorname{tan}⁡(x-\frac{\pi }{4})$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}={y}^{2}+1 \\ \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{arctan}⁡(y) & =x+C \\ y & =\operatorname{tan}⁡(x+C).\end{aligned}
$$

We conclude that the general solution is

$$
y=\operatorname{tan}⁡(x+C).
$$

We now apply the condition $y(\frac{\pi}{2})=1$ to find $C$:

$$
\begin{aligned}1 & =\operatorname{tan}⁡(\frac{\pi }{2}+C) \\ \operatorname{arctan}⁡(1) & =\frac{\pi }{2}+C \\ \frac{\pi }{4} & =\frac{\pi }{2}+C \\ C & =\frac{\pi }{4}-\frac{\pi }{2} \\ C & =-\frac{\pi }{4}.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ that satisfies the condition $y(\frac{\pi}{2})=1$ is

$$
y=\operatorname{tan}⁡(x-\frac{\pi }{4}).
$$

Author domain: tan branch containing h+pi/2; -pi/4 < x-h < 3*pi/4

### Generated hard — source_14310 (authored)

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ given that  $y(-2 + \frac{\pi}{2})=1.$

- $y=\tan{\left(x + \frac{\pi}{4} + 2 \right)}$
- $y=- \cot{\left(x + \frac{\pi}{4} + 2 \right)}$
- $y=- \cot{\left(x + 2 \right)}$
- $y=x - \frac{\pi}{4} + 2$
- $y=- \tan{\left(x + \frac{\pi}{4} + 2 \right)}$

Correct: $y=- \cot{\left(x + \frac{\pi}{4} + 2 \right)}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}={y}^{2}+1 \\ \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{arctan}⁡(y) & =\left(x + 2\right)+C \\ y & =\operatorname{tan}⁡(\left(x + 2\right)+C).\end{aligned}
$$

We conclude that the general solution is

$$
y=\operatorname{tan}⁡(\left(x + 2\right)+C).
$$

We now apply the condition $y(-2 + \frac{\pi}{2})=1$ to find $C$:

$$
\begin{aligned}1 & =\operatorname{tan}⁡(\frac{\pi }{2}+C) \\ \operatorname{arctan}⁡(1) & =\frac{\pi }{2}+C \\ \frac{\pi }{4} & =\frac{\pi }{2}+C \\ C & =\frac{\pi }{4}-\frac{\pi }{2} \\ C & =-\frac{\pi }{4}.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ that satisfies the condition $y(-2 + \frac{\pi}{2})=1$ is

$$
y=\operatorname{tan}⁡(\left(x + 2\right)-\frac{\pi }{4}).
$$

Author domain: tan branch containing h+pi/2; -pi/4 < x-h < 3*pi/4

### Generated hard — source_14310 (authored)

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ given that  $y(\frac{1}{2} + \frac{\pi}{2})=1.$

- $y=\tan{\left(x - \frac{1}{2} + \frac{\pi}{4} \right)}$
- $y=- \tan{\left(- x + \frac{1}{2} + \frac{\pi}{4} \right)}$
- $y=- \cot{\left(x - \frac{1}{2} \right)}$
- $y=x - \frac{\pi}{4} - \frac{1}{2}$
- $y=- \cot{\left(- x + \frac{1}{2} + \frac{\pi}{4} \right)}$

Correct: $y=- \tan{\left(- x + \frac{1}{2} + \frac{\pi}{4} \right)}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}={y}^{2}+1 \\ \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{arctan}⁡(y) & =\left(x - \frac{1}{2}\right)+C \\ y & =\operatorname{tan}⁡(\left(x - \frac{1}{2}\right)+C).\end{aligned}
$$

We conclude that the general solution is

$$
y=\operatorname{tan}⁡(\left(x - \frac{1}{2}\right)+C).
$$

We now apply the condition $y(\frac{1}{2} + \frac{\pi}{2})=1$ to find $C$:

$$
\begin{aligned}1 & =\operatorname{tan}⁡(\frac{\pi }{2}+C) \\ \operatorname{arctan}⁡(1) & =\frac{\pi }{2}+C \\ \frac{\pi }{4} & =\frac{\pi }{2}+C \\ C & =\frac{\pi }{4}-\frac{\pi }{2} \\ C & =-\frac{\pi }{4}.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ that satisfies the condition $y(\frac{1}{2} + \frac{\pi}{2})=1$ is

$$
y=\operatorname{tan}⁡(\left(x - \frac{1}{2}\right)-\frac{\pi }{4}).
$$

Author domain: tan branch containing h+pi/2; -pi/4 < x-h < 3*pi/4

### Generated hard — source_14310 (authored)

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ given that  $y(\frac{\pi}{2} + 3)=1.$

- $y=\tan{\left(x - 3 + \frac{\pi}{4} \right)}$
- $y=- \tan{\left(- x + \frac{\pi}{4} + 3 \right)}$
- $y=- \cot{\left(x - 3 \right)}$
- $y=x - 3 - \frac{\pi}{4}$
- $y=- \cot{\left(- x + \frac{\pi}{4} + 3 \right)}$

Correct: $y=- \tan{\left(- x + \frac{\pi}{4} + 3 \right)}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}={y}^{2}+1 \\ \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{arctan}⁡(y) & =\left(x - 3\right)+C \\ y & =\operatorname{tan}⁡(\left(x - 3\right)+C).\end{aligned}
$$

We conclude that the general solution is

$$
y=\operatorname{tan}⁡(\left(x - 3\right)+C).
$$

We now apply the condition $y(\frac{\pi}{2} + 3)=1$ to find $C$:

$$
\begin{aligned}1 & =\operatorname{tan}⁡(\frac{\pi }{2}+C) \\ \operatorname{arctan}⁡(1) & =\frac{\pi }{2}+C \\ \frac{\pi }{4} & =\frac{\pi }{2}+C \\ C & =\frac{\pi }{4}-\frac{\pi }{2} \\ C & =-\frac{\pi }{4}.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ that satisfies the condition $y(\frac{\pi}{2} + 3)=1$ is

$$
y=\operatorname{tan}⁡(\left(x - 3\right)-\frac{\pi }{4}).
$$

Author domain: tan branch containing h+pi/2; -pi/4 < x-h < 3*pi/4

## Original q-14312

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y{e}^{-x}$ that satisfies $y(0)={e}^{-1}.$

- $y={e}^{-1+x}$
- $y={e}^{-{e}^{-x}}$
- $y={e}^{{e}^{x}}$
- $y={e}^{-1-{e}^{x}}$
- $y={e}^{-1+{e}^{-x}}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y{e}^{-x} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & ={e}^{-x} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,dx & =\int {e}^{-x}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {e}^{-x}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-{e}^{-x}+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-{e}^{-x}+C} \\ |y| & ={e}^{-{e}^{-x}+C} \\ y & =\pm {e}^{-{e}^{-x}+C} \\ y & =K{e}^{-{e}^{-x}}\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)={e}^{-1}$ to find $K:$ 

$$
\begin{aligned}{e}^{-1} & =K{e}^{-{e}^{-0}} \\ {e}^{-1} & =K{e}^{-1} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y{e}^{-x}$ that satisfies the condition $y(0)={e}^{-1}$ is

$$
y={e}^{-{e}^{-x}}.
$$

### Generated easy — source_14312 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y{e}^{-x}$ that satisfies $y(0)={e}^{-1}.$

- $y={e}^{{e}^{x}}$
- $y={e}^{-{e}^{-x}}$
- $y={e}^{-1+x}$
- $y={e}^{-1+{e}^{-x}}$
- $y={e}^{-1-{e}^{x}}$

Correct: $y={e}^{-{e}^{-x}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y{e}^{-x} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & ={e}^{-x} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,dx & =\int {e}^{-x}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {e}^{-x}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-{e}^{-x}+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-{e}^{-x}+C} \\ |y| & ={e}^{-{e}^{-x}+C} \\ y & =\pm {e}^{-{e}^{-x}+C} \\ y & =K{e}^{-{e}^{-x}}\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)={e}^{-1}$ to find $K:$ 

$$
\begin{aligned}{e}^{-1} & =K{e}^{-{e}^{-0}} \\ {e}^{-1} & =K{e}^{-1} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y{e}^{-x}$ that satisfies the condition $y(0)={e}^{-1}$ is

$$
y={e}^{-{e}^{-x}}.
$$

Author domain: positive y; x real

### Generated easy — source_14312 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y{e}^{-\left(x + 2\right)}$ that satisfies $y(-2)={e}^{-1}.$

- $y=e^{e^{- x - 2}}$
- $y=e^{- e^{- x - 2}}$
- $y=e^{- e^{x + 2}}$
- $y=e^{- e^{- x - 2} - 1}$
- $y=e^{- x - 2}$

Correct: $y=e^{- e^{- x - 2}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y{e}^{-\left(x + 2\right)} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & ={e}^{-\left(x + 2\right)} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,dx & =\int {e}^{-\left(x + 2\right)}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {e}^{-\left(x + 2\right)}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-{e}^{-\left(x + 2\right)}+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-{e}^{-\left(x + 2\right)}+C} \\ |y| & ={e}^{-{e}^{-\left(x + 2\right)}+C} \\ y & =\pm {e}^{-{e}^{-\left(x + 2\right)}+C} \\ y & =K{e}^{-{e}^{-\left(x + 2\right)}}\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(-2)={e}^{-1}$ to find $K:$ 

$$
\begin{aligned}{e}^{-1} & =K{e}^{-{e}^{-0}} \\ {e}^{-1} & =K{e}^{-1} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y{e}^{-\left(x + 2\right)}$ that satisfies the condition $y(-2)={e}^{-1}$ is

$$
y={e}^{-{e}^{-\left(x + 2\right)}}.
$$

Author domain: positive y; x real

### Generated easy — source_14312 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y{e}^{-\left(x - \frac{1}{2}\right)}$ that satisfies $y(\frac{1}{2})={e}^{-1}.$

- $y=e^{e^{- x + \frac{1}{2}}}$
- $y=e^{- e^{- x + \frac{1}{2}}}$
- $y=e^{- e^{x - \frac{1}{2}}}$
- $y=e^{- e^{- x + \frac{1}{2}} - 1}$
- $y=e^{- x + \frac{1}{2}}$

Correct: $y=e^{- e^{- x + \frac{1}{2}}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y{e}^{-\left(x - \frac{1}{2}\right)} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & ={e}^{-\left(x - \frac{1}{2}\right)} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,dx & =\int {e}^{-\left(x - \frac{1}{2}\right)}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {e}^{-\left(x - \frac{1}{2}\right)}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-{e}^{-\left(x - \frac{1}{2}\right)}+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-{e}^{-\left(x - \frac{1}{2}\right)}+C} \\ |y| & ={e}^{-{e}^{-\left(x - \frac{1}{2}\right)}+C} \\ y & =\pm {e}^{-{e}^{-\left(x - \frac{1}{2}\right)}+C} \\ y & =K{e}^{-{e}^{-\left(x - \frac{1}{2}\right)}}\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(\frac{1}{2})={e}^{-1}$ to find $K:$ 

$$
\begin{aligned}{e}^{-1} & =K{e}^{-{e}^{-0}} \\ {e}^{-1} & =K{e}^{-1} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y{e}^{-\left(x - \frac{1}{2}\right)}$ that satisfies the condition $y(\frac{1}{2})={e}^{-1}$ is

$$
y={e}^{-{e}^{-\left(x - \frac{1}{2}\right)}}.
$$

Author domain: positive y; x real

### Generated easy — source_14312 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y{e}^{-\left(x - 3\right)}$ that satisfies $y(3)={e}^{-1}.$

- $y=e^{e^{- x + 3}}$
- $y=e^{- e^{- x + 3}}$
- $y=e^{- e^{x - 3}}$
- $y=e^{- e^{- x + 3} - 1}$
- $y=e^{- x + 3}$

Correct: $y=e^{- e^{- x + 3}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y{e}^{-\left(x - 3\right)} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & ={e}^{-\left(x - 3\right)} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,dx & =\int {e}^{-\left(x - 3\right)}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {e}^{-\left(x - 3\right)}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-{e}^{-\left(x - 3\right)}+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-{e}^{-\left(x - 3\right)}+C} \\ |y| & ={e}^{-{e}^{-\left(x - 3\right)}+C} \\ y & =\pm {e}^{-{e}^{-\left(x - 3\right)}+C} \\ y & =K{e}^{-{e}^{-\left(x - 3\right)}}\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(3)={e}^{-1}$ to find $K:$ 

$$
\begin{aligned}{e}^{-1} & =K{e}^{-{e}^{-0}} \\ {e}^{-1} & =K{e}^{-1} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y{e}^{-\left(x - 3\right)}$ that satisfies the condition $y(3)={e}^{-1}$ is

$$
y={e}^{-{e}^{-\left(x - 3\right)}}.
$$

Author domain: positive y; x real

## Original q-14313

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}}{{y}^{2}}$  that satisfies $y(1)=2.$

- ${y}^{3}=3{x}^{2}+5$
- ${y}^{3}={x}^{2}+3$
- ${y}^{3}={x}^{3}+7$
- ${y}^{3}=5{x}^{3}+3$
- ${y}^{3}=2{x}^{3}+2$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{x}^{2}}{{y}^{2}} \\ {y}^{2}\frac{\text{d}y}{\text{d}x} & ={x}^{2} \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ \frac{{y}^{3}}{3} & =\frac{{x}^{3}}{3}+{C}_{1} \\ {y}^{3} & ={x}^{3}+C,\end{aligned}
$$

where   $C=3{C}_{1}$ is an arbitrary constant.  

We now apply the condition $y(1)=2$ to find $C:$

$$
\begin{aligned}{2}^{3} & ={1}^{3}+C \\ 8-1 & =C \\ C & =7\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{y}^{3}={x}^{3}+7.
$$

### Generated easy — source_14313 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}}{{y}^{2}}$  that satisfies $y(1)=2.$

- ${y}^{3}={x}^{3}+7$
- ${y}^{3}={x}^{2}+3$
- ${y}^{3}=3{x}^{2}+5$
- ${y}^{3}=2{x}^{3}+2$
- ${y}^{3}=5{x}^{3}+3$

Correct: ${y}^{3}={x}^{3}+7$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{x}^{2}}{{y}^{2}} \\ {y}^{2}\frac{\text{d}y}{\text{d}x} & ={x}^{2} \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ \frac{{y}^{3}}{3} & =\frac{{x}^{3}}{3}+{C}_{1} \\ {y}^{3} & ={x}^{3}+C,\end{aligned}
$$

where   $C=3{C}_{1}$ is an arbitrary constant.  

We now apply the condition $y(1)=2$ to find $C:$

$$
\begin{aligned}{2}^{3} & ={1}^{3}+C \\ 8-1 & =C \\ C & =7\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{y}^{3}={x}^{3}+7.
$$

Author domain: y != 0; connected interval containing h+1, (x-h)^3+7 != 0

### Generated easy — source_14313 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{\left(x + 2\right)}^{2}}{{y}^{2}}$  that satisfies $y(-1)=2.$

- $y^{3}=3 \left(x + 2\right)^{2} + 7$
- $y^{3}=\left(x + 2\right)^{3} + 7$
- $y^{3}=\left(x + 2\right)^{3} - 7$
- $y^{3}=\frac{\left(x + 2\right)^{3}}{3} + 7$
- $y^{3}=\left(x + 2\right)^{3} + 8$

Correct: $y^{3}=\left(x + 2\right)^{3} + 7$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{\left(x + 2\right)}^{2}}{{y}^{2}} \\ {y}^{2}\frac{\text{d}y}{\text{d}x} & ={\left(x + 2\right)}^{2} \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {\left(x + 2\right)}^{2}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int {\left(x + 2\right)}^{2}\,\text{d}x \\ \frac{{y}^{3}}{3} & =\frac{{\left(x + 2\right)}^{3}}{3}+{C}_{1} \\ {y}^{3} & ={\left(x + 2\right)}^{3}+C,\end{aligned}
$$

where   $C=3{C}_{1}$ is an arbitrary constant.  

We now apply the condition $y(-1)=2$ to find $C:$

$$
\begin{aligned}{2}^{3} & ={1}^{3}+C \\ 8-1 & =C \\ C & =7\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{y}^{3}={\left(x + 2\right)}^{3}+7.
$$

Author domain: y != 0; connected interval containing h+1, (x-h)^3+7 != 0

### Generated easy — source_14313 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{\left(x - \frac{1}{2}\right)}^{2}}{{y}^{2}}$  that satisfies $y(\frac{3}{2})=2.$

- $y^{3}=3 \left(x - \frac{1}{2}\right)^{2} + 7$
- $y^{3}=\frac{\left(2 x - 1\right)^{3}}{8} + 7$
- $y^{3}=\left(x - \frac{1}{2}\right)^{3} - 7$
- $y^{3}=\frac{\left(x - \frac{1}{2}\right)^{3}}{3} + 7$
- $y^{3}=\left(x - \frac{1}{2}\right)^{3} + 8$

Correct: $y^{3}=\frac{\left(2 x - 1\right)^{3}}{8} + 7$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{\left(x - \frac{1}{2}\right)}^{2}}{{y}^{2}} \\ {y}^{2}\frac{\text{d}y}{\text{d}x} & ={\left(x - \frac{1}{2}\right)}^{2} \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {\left(x - \frac{1}{2}\right)}^{2}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int {\left(x - \frac{1}{2}\right)}^{2}\,\text{d}x \\ \frac{{y}^{3}}{3} & =\frac{{\left(x - \frac{1}{2}\right)}^{3}}{3}+{C}_{1} \\ {y}^{3} & ={\left(x - \frac{1}{2}\right)}^{3}+C,\end{aligned}
$$

where   $C=3{C}_{1}$ is an arbitrary constant.  

We now apply the condition $y(\frac{3}{2})=2$ to find $C:$

$$
\begin{aligned}{2}^{3} & ={1}^{3}+C \\ 8-1 & =C \\ C & =7\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{y}^{3}={\left(x - \frac{1}{2}\right)}^{3}+7.
$$

Author domain: y != 0; connected interval containing h+1, (x-h)^3+7 != 0

### Generated easy — source_14313 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{\left(x - 3\right)}^{2}}{{y}^{2}}$  that satisfies $y(4)=2.$

- $y^{3}=3 \left(x - 3\right)^{2} + 7$
- $y^{3}=\left(x - 3\right)^{3} + 7$
- $y^{3}=\left(x - 3\right)^{3} - 7$
- $y^{3}=\frac{\left(x - 3\right)^{3}}{3} + 7$
- $y^{3}=\left(x - 3\right)^{3} + 8$

Correct: $y^{3}=\left(x - 3\right)^{3} + 7$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{\left(x - 3\right)}^{2}}{{y}^{2}} \\ {y}^{2}\frac{\text{d}y}{\text{d}x} & ={\left(x - 3\right)}^{2} \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {\left(x - 3\right)}^{2}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int {\left(x - 3\right)}^{2}\,\text{d}x \\ \frac{{y}^{3}}{3} & =\frac{{\left(x - 3\right)}^{3}}{3}+{C}_{1} \\ {y}^{3} & ={\left(x - 3\right)}^{3}+C,\end{aligned}
$$

where   $C=3{C}_{1}$ is an arbitrary constant.  

We now apply the condition $y(4)=2$ to find $C:$

$$
\begin{aligned}{2}^{3} & ={1}^{3}+C \\ 8-1 & =C \\ C & =7\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{y}^{3}={\left(x - 3\right)}^{3}+7.
$$

Author domain: y != 0; connected interval containing h+1, (x-h)^3+7 != 0

## Original q-347853

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}+2{y}^{2}=0$
that satisfies the condition $y(0)=2.$

$y(x)=$
{{field-1}}

- $\frac{2}{4x+1}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+2{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-2{y}^{2} \\ -\frac{1}{{y}^{2}}\,\text{d}y & =2\,\text{d}x \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int 2\,\text{d}x \\ \frac{1}{y} & =2x+C \\ y & =\frac{1}{2x+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y(x)=\frac{1}{2x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(0)=2$ to find $C:$

$$
\begin{aligned}2 & =\frac{1}{2(0)+C} \\ C & =\frac{1}{2}\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\frac{2}{4x+1}.
$$

### Generated moderate — source_347853 (observed)

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}+2{y}^{2}=0$
that satisfies the condition $y(0)=2.$

$y(x)=$
{{field-1}}

- $\frac{2}{4x+1}$

Correct: $\frac{2}{4x+1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+2{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-2{y}^{2} \\ -\frac{1}{{y}^{2}}\,\text{d}y & =2\,\text{d}x \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int 2\,\text{d}x \\ \frac{1}{y} & =2x+C \\ y & =\frac{1}{2x+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y(x)=\frac{1}{2x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(0)=2$ to find $C:$

$$
\begin{aligned}2 & =\frac{1}{2(0)+C} \\ C & =\frac{1}{2}\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\frac{2}{4x+1}.
$$

Author domain: 4*(x-h)+1 != 0; connected interval x>h-1/4

### Generated moderate — source_347853 (blank)

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}+2{y}^{2}=0$
that satisfies the condition $y(-2)=2.$

$y(x)=$
{{field-1}}

- $\frac{2}{4\left(x + 2\right)+1}$

Correct: $\frac{2}{4\left(x + 2\right)+1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+2{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-2{y}^{2} \\ -\frac{1}{{y}^{2}}\,\text{d}y & =2\,\text{d}x \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int 2\,\text{d}x \\ \frac{1}{y} & =2\left(x + 2\right)+C \\ y & =\frac{1}{2\left(x + 2\right)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y(x)=\frac{1}{2\left(x + 2\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-2)=2$ to find $C:$

$$
\begin{aligned}2 & =\frac{1}{2(0)+C} \\ C & =\frac{1}{2}\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\frac{2}{4\left(x + 2\right)+1}.
$$

Author domain: 4*(x-h)+1 != 0; connected interval x>h-1/4

### Generated moderate — source_347853 (blank)

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}+2{y}^{2}=0$
that satisfies the condition $y(\frac{1}{2})=2.$

$y(x)=$
{{field-1}}

- $\frac{2}{4\left(x - \frac{1}{2}\right)+1}$

Correct: $\frac{2}{4\left(x - \frac{1}{2}\right)+1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+2{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-2{y}^{2} \\ -\frac{1}{{y}^{2}}\,\text{d}y & =2\,\text{d}x \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int 2\,\text{d}x \\ \frac{1}{y} & =2\left(x - \frac{1}{2}\right)+C \\ y & =\frac{1}{2\left(x - \frac{1}{2}\right)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y(x)=\frac{1}{2\left(x - \frac{1}{2}\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(\frac{1}{2})=2$ to find $C:$

$$
\begin{aligned}2 & =\frac{1}{2(0)+C} \\ C & =\frac{1}{2}\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\frac{2}{4\left(x - \frac{1}{2}\right)+1}.
$$

Author domain: 4*(x-h)+1 != 0; connected interval x>h-1/4

### Generated moderate — source_347853 (blank)

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}+2{y}^{2}=0$
that satisfies the condition $y(3)=2.$

$y(x)=$
{{field-1}}

- $\frac{2}{4\left(x - 3\right)+1}$

Correct: $\frac{2}{4\left(x - 3\right)+1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+2{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-2{y}^{2} \\ -\frac{1}{{y}^{2}}\,\text{d}y & =2\,\text{d}x \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int 2\,\text{d}x \\ \frac{1}{y} & =2\left(x - 3\right)+C \\ y & =\frac{1}{2\left(x - 3\right)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y(x)=\frac{1}{2\left(x - 3\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(3)=2$ to find $C:$

$$
\begin{aligned}2 & =\frac{1}{2(0)+C} \\ C & =\frac{1}{2}\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\frac{2}{4\left(x - 3\right)+1}.
$$

Author domain: 4*(x-h)+1 != 0; connected interval x>h-1/4

## Original q-355525

Find the particular solution to the differential equation $\operatorname{cos}⁡(3y){y}^{′}-\operatorname{sin}⁡(4x)=0$ that satisfies $y(\frac{\pi }{8})=0.$ Assume that $-\frac{\pi }{6}<y<\frac{\pi }{6}.$

$\operatorname{sin}⁡(3y)=$
{{field-1}}

- $-\frac{3}{4}\operatorname{cos}(4x)$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x}-\operatorname{sin}⁡(4x) & =0 \\ \operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(4x) \\ \operatorname{cos}⁡(3y)\,\text{d}y & =\operatorname{sin}⁡(4x)\,\text{d}x \\ \int \operatorname{cos}⁡(3y)\,\text{d}y & =\int \operatorname{sin}⁡(4x)\,\text{d}x \\ \frac{1}{3}\operatorname{sin}⁡(3y) & =-\frac{1}{4}\operatorname{cos}⁡(4x)+{C}_{1} \\ \operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4x)+C,\end{aligned}
$$

where $C=3{C}_{1}.$

We now apply the condition $y(\frac{\pi }{8})=0$ to find $C:$

$$
\begin{aligned}y(\frac{\pi }{8}) & =0 \\ \operatorname{sin}⁡(3\cdot 0) & =-\frac{3}{4}\operatorname{cos}⁡(4\cdot \frac{\pi }{8})+C \\ 0 & =-\frac{3}{4}\operatorname{cos}⁡(\frac{\pi }{2})+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4x)\end{aligned}
$$

### Generated hard — source_355525 (observed)

Find the particular solution to the differential equation $\operatorname{cos}⁡(3y){y}^{′}-\operatorname{sin}⁡(4x)=0$ that satisfies $y(\frac{\pi}{8})=0.$ Assume that $-\frac{\pi }{6}<y<\frac{\pi }{6}.$

$\operatorname{sin}⁡(3y)=$
{{field-1}}

- $-\frac{3}{4}\operatorname{cos}(4x)$

Correct: $-\frac{3}{4}\operatorname{cos}(4x)$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x}-\operatorname{sin}⁡(4x) & =0 \\ \operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(4x) \\ \operatorname{cos}⁡(3y)\,\text{d}y & =\operatorname{sin}⁡(4x)\,\text{d}x \\ \int \operatorname{cos}⁡(3y)\,\text{d}y & =\int \operatorname{sin}⁡(4x)\,\text{d}x \\ \frac{1}{3}\operatorname{sin}⁡(3y) & =-\frac{1}{4}\operatorname{cos}⁡(4x)+{C}_{1} \\ \operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4x)+C,\end{aligned}
$$

where $C=3{C}_{1}.$

We now apply the condition $y(\frac{\pi}{8})=0$ to find $C:$

$$
\begin{aligned}y(\frac{\pi}{8}) & =0 \\ \operatorname{sin}⁡(3\cdot 0) & =-\frac{3}{4}\operatorname{cos}⁡(4\cdot \frac{\pi }{8})+C \\ 0 & =-\frac{3}{4}\operatorname{cos}⁡(\frac{\pi }{2})+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4x)\end{aligned}
$$

Author domain: -pi/6 < y < pi/6; local interval containing h+pi/8

### Generated hard — source_355525 (blank)

Find the particular solution to the differential equation $\operatorname{cos}⁡(3y){y}^{′}-\operatorname{sin}⁡(4\left(x + 2\right))=0$ that satisfies $y(-2 + \frac{\pi}{8})=0.$ Assume that $-\frac{\pi }{6}<y<\frac{\pi }{6}.$

$\operatorname{sin}⁡(3y)=$
{{field-1}}

- $-\frac{3}{4}\operatorname{cos}(4\left(x + 2\right))$

Correct: $-\frac{3}{4}\operatorname{cos}(4\left(x + 2\right))$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x}-\operatorname{sin}⁡(4\left(x + 2\right)) & =0 \\ \operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(4\left(x + 2\right)) \\ \operatorname{cos}⁡(3y)\,\text{d}y & =\operatorname{sin}⁡(4\left(x + 2\right))\,\text{d}x \\ \int \operatorname{cos}⁡(3y)\,\text{d}y & =\int \operatorname{sin}⁡(4\left(x + 2\right))\,\text{d}x \\ \frac{1}{3}\operatorname{sin}⁡(3y) & =-\frac{1}{4}\operatorname{cos}⁡(4\left(x + 2\right))+{C}_{1} \\ \operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4\left(x + 2\right))+C,\end{aligned}
$$

where $C=3{C}_{1}.$

We now apply the condition $y(-2 + \frac{\pi}{8})=0$ to find $C:$

$$
\begin{aligned}y(-2 + \frac{\pi}{8}) & =0 \\ \operatorname{sin}⁡(3\cdot 0) & =-\frac{3}{4}\operatorname{cos}⁡(4\cdot \frac{\pi }{8})+C \\ 0 & =-\frac{3}{4}\operatorname{cos}⁡(\frac{\pi }{2})+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4\left(x + 2\right))\end{aligned}
$$

Author domain: -pi/6 < y < pi/6; local interval containing h+pi/8

### Generated hard — source_355525 (blank)

Find the particular solution to the differential equation $\operatorname{cos}⁡(3y){y}^{′}-\operatorname{sin}⁡(4\left(x - \frac{1}{2}\right))=0$ that satisfies $y(\frac{\pi}{8} + \frac{1}{2})=0.$ Assume that $-\frac{\pi }{6}<y<\frac{\pi }{6}.$

$\operatorname{sin}⁡(3y)=$
{{field-1}}

- $-\frac{3}{4}\operatorname{cos}(4\left(x - \frac{1}{2}\right))$

Correct: $-\frac{3}{4}\operatorname{cos}(4\left(x - \frac{1}{2}\right))$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x}-\operatorname{sin}⁡(4\left(x - \frac{1}{2}\right)) & =0 \\ \operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(4\left(x - \frac{1}{2}\right)) \\ \operatorname{cos}⁡(3y)\,\text{d}y & =\operatorname{sin}⁡(4\left(x - \frac{1}{2}\right))\,\text{d}x \\ \int \operatorname{cos}⁡(3y)\,\text{d}y & =\int \operatorname{sin}⁡(4\left(x - \frac{1}{2}\right))\,\text{d}x \\ \frac{1}{3}\operatorname{sin}⁡(3y) & =-\frac{1}{4}\operatorname{cos}⁡(4\left(x - \frac{1}{2}\right))+{C}_{1} \\ \operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4\left(x - \frac{1}{2}\right))+C,\end{aligned}
$$

where $C=3{C}_{1}.$

We now apply the condition $y(\frac{\pi}{8} + \frac{1}{2})=0$ to find $C:$

$$
\begin{aligned}y(\frac{\pi}{8} + \frac{1}{2}) & =0 \\ \operatorname{sin}⁡(3\cdot 0) & =-\frac{3}{4}\operatorname{cos}⁡(4\cdot \frac{\pi }{8})+C \\ 0 & =-\frac{3}{4}\operatorname{cos}⁡(\frac{\pi }{2})+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4\left(x - \frac{1}{2}\right))\end{aligned}
$$

Author domain: -pi/6 < y < pi/6; local interval containing h+pi/8

### Generated hard — source_355525 (blank)

Find the particular solution to the differential equation $\operatorname{cos}⁡(3y){y}^{′}-\operatorname{sin}⁡(4\left(x - 3\right))=0$ that satisfies $y(\frac{\pi}{8} + 3)=0.$ Assume that $-\frac{\pi }{6}<y<\frac{\pi }{6}.$

$\operatorname{sin}⁡(3y)=$
{{field-1}}

- $-\frac{3}{4}\operatorname{cos}(4\left(x - 3\right))$

Correct: $-\frac{3}{4}\operatorname{cos}(4\left(x - 3\right))$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x}-\operatorname{sin}⁡(4\left(x - 3\right)) & =0 \\ \operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(4\left(x - 3\right)) \\ \operatorname{cos}⁡(3y)\,\text{d}y & =\operatorname{sin}⁡(4\left(x - 3\right))\,\text{d}x \\ \int \operatorname{cos}⁡(3y)\,\text{d}y & =\int \operatorname{sin}⁡(4\left(x - 3\right))\,\text{d}x \\ \frac{1}{3}\operatorname{sin}⁡(3y) & =-\frac{1}{4}\operatorname{cos}⁡(4\left(x - 3\right))+{C}_{1} \\ \operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4\left(x - 3\right))+C,\end{aligned}
$$

where $C=3{C}_{1}.$

We now apply the condition $y(\frac{\pi}{8} + 3)=0$ to find $C:$

$$
\begin{aligned}y(\frac{\pi}{8} + 3) & =0 \\ \operatorname{sin}⁡(3\cdot 0) & =-\frac{3}{4}\operatorname{cos}⁡(4\cdot \frac{\pi }{8})+C \\ 0 & =-\frac{3}{4}\operatorname{cos}⁡(\frac{\pi }{2})+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4\left(x - 3\right))\end{aligned}
$$

Author domain: -pi/6 < y < pi/6; local interval containing h+pi/8

## Original q-355528

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}=4x\sqrt{y}$
that satisfies the condition $y(1)=9.$  Assume that $y>0.$

$y(x)=$
{{field-1}}

- $({x}^{2}+2)^{2}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4x\sqrt{y} \\ \frac{1}{\sqrt{y}}\,\text{d}y & =4x\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 4x\,\text{d}x \\ 2\sqrt{y} & =2{x}^{2}+{C}_{1} \\ \sqrt{y} & ={x}^{2}+\frac{{C}_{1}}{2} \\ y & ={({x}^{2}+\frac{{C}_{1}}{2})}^{2}.\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y(x)=({x}^{2}+C)^{2},
$$

where $C=\frac{{C}_{1}}{2}$ is an arbitrary constant.

We now apply the condition $y(1)=9$ to find $C:$

$$
\begin{aligned}9 & =((1)^{2}+C)^{2} \\ 9 & =(1+C)^{2} \\ 3 & =1+C \\ C & =2\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=({x}^{2}+2)^{2}.
$$

### Generated moderate — source_355528 (observed)

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}=4x\sqrt{y}$
that satisfies the condition $y(1)=9.$  Assume that $y>0.$

$y(x)=$
{{field-1}}

- $({x}^{2}+2)^{2}$

Correct: $({x}^{2}+2)^{2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4x\sqrt{y} \\ \frac{1}{\sqrt{y}}\,\text{d}y & =4x\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 4x\,\text{d}x \\ 2\sqrt{y} & =2{x}^{2}+{C}_{1} \\ \sqrt{y} & ={x}^{2}+\frac{{C}_{1}}{2} \\ y & ={({x}^{2}+\frac{{C}_{1}}{2})}^{2}.\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y(x)=({x}^{2}+C)^{2},
$$

where $C=\frac{{C}_{1}}{2}$ is an arbitrary constant.

We now apply the condition $y(1)=9$ to find $C:$

$$
\begin{aligned}9 & =((1)^{2}+C)^{2} \\ 9 & =(1+C)^{2} \\ 3 & =1+C \\ C & =2\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=({x}^{2}+2)^{2}.
$$

Author domain: y>0 and (x-h)^2+2>0; x real

### Generated moderate — source_355528 (blank)

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}=4\left(x + 2\right)\sqrt{y}$
that satisfies the condition $y(-1)=9.$  Assume that $y>0.$

$y(x)=$
{{field-1}}

- $({\left(x + 2\right)}^{2}+2)^{2}$

Correct: $({\left(x + 2\right)}^{2}+2)^{2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4\left(x + 2\right)\sqrt{y} \\ \frac{1}{\sqrt{y}}\,\text{d}y & =4\left(x + 2\right)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 4\left(x + 2\right)\,\text{d}x \\ 2\sqrt{y} & =2{\left(x + 2\right)}^{2}+{C}_{1} \\ \sqrt{y} & ={\left(x + 2\right)}^{2}+\frac{{C}_{1}}{2} \\ y & ={({\left(x + 2\right)}^{2}+\frac{{C}_{1}}{2})}^{2}.\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y(x)=({\left(x + 2\right)}^{2}+C)^{2},
$$

where $C=\frac{{C}_{1}}{2}$ is an arbitrary constant.

We now apply the condition $y(-1)=9$ to find $C:$

$$
\begin{aligned}9 & =((1)^{2}+C)^{2} \\ 9 & =(1+C)^{2} \\ 3 & =1+C \\ C & =2\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=({\left(x + 2\right)}^{2}+2)^{2}.
$$

Author domain: y>0 and (x-h)^2+2>0; x real

### Generated moderate — source_355528 (blank)

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}=4\left(x - \frac{1}{2}\right)\sqrt{y}$
that satisfies the condition $y(\frac{3}{2})=9.$  Assume that $y>0.$

$y(x)=$
{{field-1}}

- $({\left(x - \frac{1}{2}\right)}^{2}+2)^{2}$

Correct: $({\left(x - \frac{1}{2}\right)}^{2}+2)^{2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4\left(x - \frac{1}{2}\right)\sqrt{y} \\ \frac{1}{\sqrt{y}}\,\text{d}y & =4\left(x - \frac{1}{2}\right)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 4\left(x - \frac{1}{2}\right)\,\text{d}x \\ 2\sqrt{y} & =2{\left(x - \frac{1}{2}\right)}^{2}+{C}_{1} \\ \sqrt{y} & ={\left(x - \frac{1}{2}\right)}^{2}+\frac{{C}_{1}}{2} \\ y & ={({\left(x - \frac{1}{2}\right)}^{2}+\frac{{C}_{1}}{2})}^{2}.\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y(x)=({\left(x - \frac{1}{2}\right)}^{2}+C)^{2},
$$

where $C=\frac{{C}_{1}}{2}$ is an arbitrary constant.

We now apply the condition $y(\frac{3}{2})=9$ to find $C:$

$$
\begin{aligned}9 & =((1)^{2}+C)^{2} \\ 9 & =(1+C)^{2} \\ 3 & =1+C \\ C & =2\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=({\left(x - \frac{1}{2}\right)}^{2}+2)^{2}.
$$

Author domain: y>0 and (x-h)^2+2>0; x real

### Generated moderate — source_355528 (blank)

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}=4\left(x - 3\right)\sqrt{y}$
that satisfies the condition $y(4)=9.$  Assume that $y>0.$

$y(x)=$
{{field-1}}

- $({\left(x - 3\right)}^{2}+2)^{2}$

Correct: $({\left(x - 3\right)}^{2}+2)^{2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4\left(x - 3\right)\sqrt{y} \\ \frac{1}{\sqrt{y}}\,\text{d}y & =4\left(x - 3\right)\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 4\left(x - 3\right)\,\text{d}x \\ 2\sqrt{y} & =2{\left(x - 3\right)}^{2}+{C}_{1} \\ \sqrt{y} & ={\left(x - 3\right)}^{2}+\frac{{C}_{1}}{2} \\ y & ={({\left(x - 3\right)}^{2}+\frac{{C}_{1}}{2})}^{2}.\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y(x)=({\left(x - 3\right)}^{2}+C)^{2},
$$

where $C=\frac{{C}_{1}}{2}$ is an arbitrary constant.

We now apply the condition $y(4)=9$ to find $C:$

$$
\begin{aligned}9 & =((1)^{2}+C)^{2} \\ 9 & =(1+C)^{2} \\ 3 & =1+C \\ C & =2\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=({\left(x - 3\right)}^{2}+2)^{2}.
$$

Author domain: y>0 and (x-h)^2+2>0; x real

## Original q-355544

Find the particular solution to the differential equation ${sec}^{2}⁡(4y){y}^{′}={sec}^{2}⁡(7x)$ that satisfies $y(0)=0.$ Assume that $-\frac{\pi }{8}<y<\frac{\pi }{8}.$

$\operatorname{tan}⁡(4y)=$
{{field-1}}

- $\frac{4}{7}\operatorname{tan}(7x)$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{sec}^{2}⁡(4y)\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(7x) \\ {sec}^{2}⁡(4y)\,\text{d}y & ={sec}^{2}⁡(7x)\,\text{d}x \\ \int {sec}^{2}⁡(4y)\,\text{d}y & =\int {sec}^{2}⁡(7x)\,\text{d}x \\ \frac{1}{4}\operatorname{tan}⁡(4y) & =\frac{1}{7}\operatorname{tan}⁡(7x)+{C}_{1} \\ \operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7x)+C,\end{aligned}
$$

where $C=4{C}_{1}.$

We now apply the condition $y(0)=0$ to find $C:$

$$
\begin{aligned}y(0) & =0 \\ \operatorname{tan}⁡(4\cdot 0) & =\frac{4}{7}\operatorname{tan}⁡(7\cdot 0)+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7x)\end{aligned}
$$

### Generated hard — source_355544 (observed)

Find the particular solution to the differential equation ${sec}^{2}⁡(4y){y}^{′}={sec}^{2}⁡(7x)$ that satisfies $y(0)=0.$ Assume that $-\frac{\pi }{8}<y<\frac{\pi }{8}.$

$\operatorname{tan}⁡(4y)=$
{{field-1}}

- $\frac{4}{7}\operatorname{tan}(7x)$

Correct: $\frac{4}{7}\operatorname{tan}(7x)$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{sec}^{2}⁡(4y)\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(7x) \\ {sec}^{2}⁡(4y)\,\text{d}y & ={sec}^{2}⁡(7x)\,\text{d}x \\ \int {sec}^{2}⁡(4y)\,\text{d}y & =\int {sec}^{2}⁡(7x)\,\text{d}x \\ \frac{1}{4}\operatorname{tan}⁡(4y) & =\frac{1}{7}\operatorname{tan}⁡(7x)+{C}_{1} \\ \operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7x)+C,\end{aligned}
$$

where $C=4{C}_{1}.$

We now apply the condition $y(0)=0$ to find $C:$

$$
\begin{aligned}y(0) & =0 \\ \operatorname{tan}⁡(4\cdot 0) & =\frac{4}{7}\operatorname{tan}⁡(7\cdot 0)+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7x)\end{aligned}
$$

Author domain: -pi/8<y<pi/8; cos(7*(x-h)) !=0; -pi/14<x-h<pi/14

### Generated hard — source_355544 (blank)

Find the particular solution to the differential equation ${sec}^{2}⁡(4y){y}^{′}={sec}^{2}⁡(7\left(x + 2\right))$ that satisfies $y(-2)=0.$ Assume that $-\frac{\pi }{8}<y<\frac{\pi }{8}.$

$\operatorname{tan}⁡(4y)=$
{{field-1}}

- $\frac{4}{7}\operatorname{tan}(7\left(x + 2\right))$

Correct: $\frac{4}{7}\operatorname{tan}(7\left(x + 2\right))$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{sec}^{2}⁡(4y)\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(7\left(x + 2\right)) \\ {sec}^{2}⁡(4y)\,\text{d}y & ={sec}^{2}⁡(7\left(x + 2\right))\,\text{d}x \\ \int {sec}^{2}⁡(4y)\,\text{d}y & =\int {sec}^{2}⁡(7\left(x + 2\right))\,\text{d}x \\ \frac{1}{4}\operatorname{tan}⁡(4y) & =\frac{1}{7}\operatorname{tan}⁡(7\left(x + 2\right))+{C}_{1} \\ \operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7\left(x + 2\right))+C,\end{aligned}
$$

where $C=4{C}_{1}.$

We now apply the condition $y(-2)=0$ to find $C:$

$$
\begin{aligned}y(-2) & =0 \\ \operatorname{tan}⁡(4\cdot 0) & =\frac{4}{7}\operatorname{tan}⁡(7\cdot 0)+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7\left(x + 2\right))\end{aligned}
$$

Author domain: -pi/8<y<pi/8; cos(7*(x-h)) !=0; -pi/14<x-h<pi/14

### Generated hard — source_355544 (blank)

Find the particular solution to the differential equation ${sec}^{2}⁡(4y){y}^{′}={sec}^{2}⁡(7\left(x - \frac{1}{2}\right))$ that satisfies $y(\frac{1}{2})=0.$ Assume that $-\frac{\pi }{8}<y<\frac{\pi }{8}.$

$\operatorname{tan}⁡(4y)=$
{{field-1}}

- $\frac{4}{7}\operatorname{tan}(7\left(x - \frac{1}{2}\right))$

Correct: $\frac{4}{7}\operatorname{tan}(7\left(x - \frac{1}{2}\right))$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{sec}^{2}⁡(4y)\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(7\left(x - \frac{1}{2}\right)) \\ {sec}^{2}⁡(4y)\,\text{d}y & ={sec}^{2}⁡(7\left(x - \frac{1}{2}\right))\,\text{d}x \\ \int {sec}^{2}⁡(4y)\,\text{d}y & =\int {sec}^{2}⁡(7\left(x - \frac{1}{2}\right))\,\text{d}x \\ \frac{1}{4}\operatorname{tan}⁡(4y) & =\frac{1}{7}\operatorname{tan}⁡(7\left(x - \frac{1}{2}\right))+{C}_{1} \\ \operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7\left(x - \frac{1}{2}\right))+C,\end{aligned}
$$

where $C=4{C}_{1}.$

We now apply the condition $y(\frac{1}{2})=0$ to find $C:$

$$
\begin{aligned}y(\frac{1}{2}) & =0 \\ \operatorname{tan}⁡(4\cdot 0) & =\frac{4}{7}\operatorname{tan}⁡(7\cdot 0)+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7\left(x - \frac{1}{2}\right))\end{aligned}
$$

Author domain: -pi/8<y<pi/8; cos(7*(x-h)) !=0; -pi/14<x-h<pi/14

### Generated hard — source_355544 (blank)

Find the particular solution to the differential equation ${sec}^{2}⁡(4y){y}^{′}={sec}^{2}⁡(7\left(x - 3\right))$ that satisfies $y(3)=0.$ Assume that $-\frac{\pi }{8}<y<\frac{\pi }{8}.$

$\operatorname{tan}⁡(4y)=$
{{field-1}}

- $\frac{4}{7}\operatorname{tan}(7\left(x - 3\right))$

Correct: $\frac{4}{7}\operatorname{tan}(7\left(x - 3\right))$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{sec}^{2}⁡(4y)\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(7\left(x - 3\right)) \\ {sec}^{2}⁡(4y)\,\text{d}y & ={sec}^{2}⁡(7\left(x - 3\right))\,\text{d}x \\ \int {sec}^{2}⁡(4y)\,\text{d}y & =\int {sec}^{2}⁡(7\left(x - 3\right))\,\text{d}x \\ \frac{1}{4}\operatorname{tan}⁡(4y) & =\frac{1}{7}\operatorname{tan}⁡(7\left(x - 3\right))+{C}_{1} \\ \operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7\left(x - 3\right))+C,\end{aligned}
$$

where $C=4{C}_{1}.$

We now apply the condition $y(3)=0$ to find $C:$

$$
\begin{aligned}y(3) & =0 \\ \operatorname{tan}⁡(4\cdot 0) & =\frac{4}{7}\operatorname{tan}⁡(7\cdot 0)+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7\left(x - 3\right))\end{aligned}
$$

Author domain: -pi/8<y<pi/8; cos(7*(x-h)) !=0; -pi/14<x-h<pi/14

## Original q-355562

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=xy$  that satisfies $y(0)=1.$

$y=$
{{field-1}}

- ${e}^{{x}^{2}/2}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =xy \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =x \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,x\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{2}{x}^{2}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{x}^{2}/2+C} \\ |y| & ={e}^{{x}^{2}/2+C}\, \\ y & =\pm {e}^{{x}^{2}/2+C} \\ y & =K{e}^{{x}^{2}/2}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=xy$ that satisfies the condition $y(0)=1$ is

$$
y={e}^{{x}^{2}/2}\,.
$$

### Generated moderate — source_355562 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=xy$  that satisfies $y(0)=1.$

$y=$
{{field-1}}

- ${e}^{{x}^{2}/2}$

Correct: ${e}^{{x}^{2}/2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =xy \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =x \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,x\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{2}{x}^{2}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{x}^{2}/2+C} \\ |y| & ={e}^{{x}^{2}/2+C}\, \\ y & =\pm {e}^{{x}^{2}/2+C} \\ y & =K{e}^{{x}^{2}/2}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=xy$ that satisfies the condition $y(0)=1$ is

$$
y={e}^{{x}^{2}/2}\,.
$$

Author domain: y>0; x real

### Generated moderate — source_355562 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\left(x + 2\right)y$  that satisfies $y(-2)=1.$

$y=$
{{field-1}}

- ${e}^{{\left(x + 2\right)}^{2}/2}$

Correct: ${e}^{{\left(x + 2\right)}^{2}/2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(x + 2\right)y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\left(x + 2\right) \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\left(x + 2\right)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\left(x + 2\right)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{2}{\left(x + 2\right)}^{2}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{\left(x + 2\right)}^{2}/2+C} \\ |y| & ={e}^{{\left(x + 2\right)}^{2}/2+C}\, \\ y & =\pm {e}^{{\left(x + 2\right)}^{2}/2+C} \\ y & =K{e}^{{\left(x + 2\right)}^{2}/2}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(-2)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\left(x + 2\right)y$ that satisfies the condition $y(-2)=1$ is

$$
y={e}^{{\left(x + 2\right)}^{2}/2}\,.
$$

Author domain: y>0; x real

### Generated moderate — source_355562 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\left(x - \frac{1}{2}\right)y$  that satisfies $y(\frac{1}{2})=1.$

$y=$
{{field-1}}

- ${e}^{{\left(x - \frac{1}{2}\right)}^{2}/2}$

Correct: ${e}^{{\left(x - \frac{1}{2}\right)}^{2}/2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(x - \frac{1}{2}\right)y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\left(x - \frac{1}{2}\right) \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\left(x - \frac{1}{2}\right)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\left(x - \frac{1}{2}\right)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{2}{\left(x - \frac{1}{2}\right)}^{2}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{\left(x - \frac{1}{2}\right)}^{2}/2+C} \\ |y| & ={e}^{{\left(x - \frac{1}{2}\right)}^{2}/2+C}\, \\ y & =\pm {e}^{{\left(x - \frac{1}{2}\right)}^{2}/2+C} \\ y & =K{e}^{{\left(x - \frac{1}{2}\right)}^{2}/2}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(\frac{1}{2})=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\left(x - \frac{1}{2}\right)y$ that satisfies the condition $y(\frac{1}{2})=1$ is

$$
y={e}^{{\left(x - \frac{1}{2}\right)}^{2}/2}\,.
$$

Author domain: y>0; x real

### Generated moderate — source_355562 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\left(x - 3\right)y$  that satisfies $y(3)=1.$

$y=$
{{field-1}}

- ${e}^{{\left(x - 3\right)}^{2}/2}$

Correct: ${e}^{{\left(x - 3\right)}^{2}/2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(x - 3\right)y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\left(x - 3\right) \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\left(x - 3\right)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\left(x - 3\right)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{2}{\left(x - 3\right)}^{2}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{\left(x - 3\right)}^{2}/2+C} \\ |y| & ={e}^{{\left(x - 3\right)}^{2}/2+C}\, \\ y & =\pm {e}^{{\left(x - 3\right)}^{2}/2+C} \\ y & =K{e}^{{\left(x - 3\right)}^{2}/2}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(3)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\left(x - 3\right)y$ that satisfies the condition $y(3)=1$ is

$$
y={e}^{{\left(x - 3\right)}^{2}/2}\,.
$$

Author domain: y>0; x real

## Original q-355578

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}}=0$  that satisfies $y(1)=e.$

$y=$
{{field-1}}

- ${e}^{2-1/x}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}} & =0 \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{x}^{2}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\frac{1}{x}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-1/x+C} \\ |y| & ={e}^{-1/x+C}\, \\ |y| & ={e}^{-1/x}\cdot {e}^{C} \\ y & =K{e}^{-1/x}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(1)=e$ to find $K:$ 

$$
\begin{aligned}e & =K{e}^{-1} \\ K & ={e}^{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}}=0$ that satisfies the condition $y(1)=e$ is

$$
y={e}^{2-1/x}\,.
$$

### Generated moderate — source_355578 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}}=0$  that satisfies $y(1)=e.$

$y=$
{{field-1}}

- ${e}^{2-1/x}$

Correct: ${e}^{2-1/x}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}} & =0 \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{x}^{2}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\frac{1}{x}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-1/x+C} \\ |y| & ={e}^{-1/x+C}\, \\ |y| & ={e}^{-1/x}\cdot {e}^{C} \\ y & =K{e}^{-1/x}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(1)=e$ to find $K:$ 

$$
\begin{aligned}e & =K{e}^{-1} \\ K & ={e}^{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}}=0$ that satisfies the condition $y(1)=e$ is

$$
y={e}^{2-1/x}\,.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_355578 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x + 2\right)}^{2}}=0$  that satisfies $y(-1)=e.$

$y=$
{{field-1}}

- ${e}^{2-1/\left(x + 2\right)}$

Correct: ${e}^{2-1/\left(x + 2\right)}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x + 2\right)}^{2}} & =0 \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{\left(x + 2\right)}^{2}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{\left(x + 2\right)}^{2}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{{\left(x + 2\right)}^{2}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{{\left(x + 2\right)}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\frac{1}{\left(x + 2\right)}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-1/\left(x + 2\right)+C} \\ |y| & ={e}^{-1/\left(x + 2\right)+C}\, \\ |y| & ={e}^{-1/\left(x + 2\right)}\cdot {e}^{C} \\ y & =K{e}^{-1/\left(x + 2\right)}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(-1)=e$ to find $K:$ 

$$
\begin{aligned}e & =K{e}^{-1} \\ K & ={e}^{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x + 2\right)}^{2}}=0$ that satisfies the condition $y(-1)=e$ is

$$
y={e}^{2-1/\left(x + 2\right)}\,.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_355578 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x - \frac{1}{2}\right)}^{2}}=0$  that satisfies $y(\frac{3}{2})=e.$

$y=$
{{field-1}}

- ${e}^{2-1/\left(x - \frac{1}{2}\right)}$

Correct: ${e}^{2-1/\left(x - \frac{1}{2}\right)}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x - \frac{1}{2}\right)}^{2}} & =0 \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{\left(x - \frac{1}{2}\right)}^{2}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{\left(x - \frac{1}{2}\right)}^{2}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{{\left(x - \frac{1}{2}\right)}^{2}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{{\left(x - \frac{1}{2}\right)}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\frac{1}{\left(x - \frac{1}{2}\right)}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-1/\left(x - \frac{1}{2}\right)+C} \\ |y| & ={e}^{-1/\left(x - \frac{1}{2}\right)+C}\, \\ |y| & ={e}^{-1/\left(x - \frac{1}{2}\right)}\cdot {e}^{C} \\ y & =K{e}^{-1/\left(x - \frac{1}{2}\right)}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(\frac{3}{2})=e$ to find $K:$ 

$$
\begin{aligned}e & =K{e}^{-1} \\ K & ={e}^{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x - \frac{1}{2}\right)}^{2}}=0$ that satisfies the condition $y(\frac{3}{2})=e$ is

$$
y={e}^{2-1/\left(x - \frac{1}{2}\right)}\,.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_355578 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x - 3\right)}^{2}}=0$  that satisfies $y(4)=e.$

$y=$
{{field-1}}

- ${e}^{2-1/\left(x - 3\right)}$

Correct: ${e}^{2-1/\left(x - 3\right)}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x - 3\right)}^{2}} & =0 \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{\left(x - 3\right)}^{2}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{\left(x - 3\right)}^{2}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{{\left(x - 3\right)}^{2}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{{\left(x - 3\right)}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\frac{1}{\left(x - 3\right)}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-1/\left(x - 3\right)+C} \\ |y| & ={e}^{-1/\left(x - 3\right)+C}\, \\ |y| & ={e}^{-1/\left(x - 3\right)}\cdot {e}^{C} \\ y & =K{e}^{-1/\left(x - 3\right)}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(4)=e$ to find $K:$ 

$$
\begin{aligned}e & =K{e}^{-1} \\ K & ={e}^{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}-\frac{y}{{\left(x - 3\right)}^{2}}=0$ that satisfies the condition $y(4)=e$ is

$$
y={e}^{2-1/\left(x - 3\right)}\,.
$$

Author domain: x>h; initial x=h+1

## Original q-355579

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{x}}$  that satisfies $y(1)={e}^{2}.$

$y=$
{{field-1}}

- ${e}^{2\sqrt{x}}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{x}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{x}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{\sqrt{x}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{\sqrt{x}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\sqrt{x}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{2\sqrt{x}+C} \\ |y| & ={e}^{2\sqrt{x}+C}\, \\ |y| & ={e}^{2\sqrt{x}}\cdot {e}^{C} \\ y & =K{e}^{2\sqrt{x}}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(1)={e}^{2}$ to find $K:$ 

$$
\begin{aligned}{e}^{2} & =K{e}^{2\sqrt{1}} \\ {e}^{2} & =K{e}^{2} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{x}}$ that satisfies the condition $y(1)={e}^{2}$ is

$$
y={e}^{2\sqrt{x}}\,.
$$

### Generated moderate — source_355579 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{x}}$  that satisfies $y(1)={e}^{2}.$

$y=$
{{field-1}}

- ${e}^{2\sqrt{x}}$

Correct: ${e}^{2\sqrt{x}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{x}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{x}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{\sqrt{x}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{\sqrt{x}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\sqrt{x}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{2\sqrt{x}+C} \\ |y| & ={e}^{2\sqrt{x}+C}\, \\ |y| & ={e}^{2\sqrt{x}}\cdot {e}^{C} \\ y & =K{e}^{2\sqrt{x}}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(1)={e}^{2}$ to find $K:$ 

$$
\begin{aligned}{e}^{2} & =K{e}^{2\sqrt{1}} \\ {e}^{2} & =K{e}^{2} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{x}}$ that satisfies the condition $y(1)={e}^{2}$ is

$$
y={e}^{2\sqrt{x}}\,.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_355579 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{\left(x + 2\right)}}$  that satisfies $y(-1)={e}^{2}.$

$y=$
{{field-1}}

- ${e}^{2\sqrt{\left(x + 2\right)}}$

Correct: ${e}^{2\sqrt{\left(x + 2\right)}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{\left(x + 2\right)}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{\left(x + 2\right)}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{\sqrt{\left(x + 2\right)}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{\sqrt{\left(x + 2\right)}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\sqrt{\left(x + 2\right)}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{2\sqrt{\left(x + 2\right)}+C} \\ |y| & ={e}^{2\sqrt{\left(x + 2\right)}+C}\, \\ |y| & ={e}^{2\sqrt{\left(x + 2\right)}}\cdot {e}^{C} \\ y & =K{e}^{2\sqrt{\left(x + 2\right)}}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(-1)={e}^{2}$ to find $K:$ 

$$
\begin{aligned}{e}^{2} & =K{e}^{2\sqrt{1}} \\ {e}^{2} & =K{e}^{2} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{\left(x + 2\right)}}$ that satisfies the condition $y(-1)={e}^{2}$ is

$$
y={e}^{2\sqrt{\left(x + 2\right)}}\,.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_355579 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{\left(x - \frac{1}{2}\right)}}$  that satisfies $y(\frac{3}{2})={e}^{2}.$

$y=$
{{field-1}}

- ${e}^{2\sqrt{\left(x - \frac{1}{2}\right)}}$

Correct: ${e}^{2\sqrt{\left(x - \frac{1}{2}\right)}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{\left(x - \frac{1}{2}\right)}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{\left(x - \frac{1}{2}\right)}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{\sqrt{\left(x - \frac{1}{2}\right)}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{\sqrt{\left(x - \frac{1}{2}\right)}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\sqrt{\left(x - \frac{1}{2}\right)}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{2\sqrt{\left(x - \frac{1}{2}\right)}+C} \\ |y| & ={e}^{2\sqrt{\left(x - \frac{1}{2}\right)}+C}\, \\ |y| & ={e}^{2\sqrt{\left(x - \frac{1}{2}\right)}}\cdot {e}^{C} \\ y & =K{e}^{2\sqrt{\left(x - \frac{1}{2}\right)}}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(\frac{3}{2})={e}^{2}$ to find $K:$ 

$$
\begin{aligned}{e}^{2} & =K{e}^{2\sqrt{1}} \\ {e}^{2} & =K{e}^{2} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{\left(x - \frac{1}{2}\right)}}$ that satisfies the condition $y(\frac{3}{2})={e}^{2}$ is

$$
y={e}^{2\sqrt{\left(x - \frac{1}{2}\right)}}\,.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_355579 (blank)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{\left(x - 3\right)}}$  that satisfies $y(4)={e}^{2}.$

$y=$
{{field-1}}

- ${e}^{2\sqrt{\left(x - 3\right)}}$

Correct: ${e}^{2\sqrt{\left(x - 3\right)}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{\left(x - 3\right)}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{\left(x - 3\right)}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{\sqrt{\left(x - 3\right)}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{\sqrt{\left(x - 3\right)}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\sqrt{\left(x - 3\right)}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{2\sqrt{\left(x - 3\right)}+C} \\ |y| & ={e}^{2\sqrt{\left(x - 3\right)}+C}\, \\ |y| & ={e}^{2\sqrt{\left(x - 3\right)}}\cdot {e}^{C} \\ y & =K{e}^{2\sqrt{\left(x - 3\right)}}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(4)={e}^{2}$ to find $K:$ 

$$
\begin{aligned}{e}^{2} & =K{e}^{2\sqrt{1}} \\ {e}^{2} & =K{e}^{2} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{\left(x - 3\right)}}$ that satisfies the condition $y(4)={e}^{2}$ is

$$
y={e}^{2\sqrt{\left(x - 3\right)}}\,.
$$

Author domain: x>h; initial x=h+1

## Original q-50220

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies $y(1)=1.$

- $y=\frac{2}{x}-1$
- $y=\frac{1}{2x-1}$
- $y=\frac{2}{x+1}$
- $y=\frac{1}{x}$
- $y=\frac{1}{2-x}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-{y}^{2} \\ -\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =1 \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int \,\text{d}x \\ \frac{1}{y} & =x+C \\ y & =\frac{1}{x+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=\frac{1}{x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=1$ to find $C:$

$$
\begin{aligned}1 & =\frac{1}{1+C} \\ 1+C & =1 \\ C & =0.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies the condition $y(1)=1$ is

$$
y=\frac{1}{x}.
$$

### Generated moderate — source_50220 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies $y(1)=1.$

- $y=\frac{2}{x+1}$
- $y=\frac{1}{2x-1}$
- $y=\frac{2}{x}-1$
- $y=\frac{1}{2-x}$
- $y=\frac{1}{x}$

Correct: $y=\frac{1}{x}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-{y}^{2} \\ -\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =1 \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int \,\text{d}x \\ \frac{1}{y} & =x+C \\ y & =\frac{1}{x+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=\frac{1}{x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=1$ to find $C:$

$$
\begin{aligned}1 & =\frac{1}{1+C} \\ 1+C & =1 \\ C & =0.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies the condition $y(1)=1$ is

$$
y=\frac{1}{x}.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_50220 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies $y(-1)=1.$

- $y=- \frac{1}{x}$
- $y=\frac{1}{x + 2}$
- $y=\frac{1}{2 x + 3}$
- $y=x + 2$
- $y=\frac{1}{x + 3}$

Correct: $y=\frac{1}{x + 2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-{y}^{2} \\ -\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =1 \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int \,\text{d}x \\ \frac{1}{y} & =\left(x + 2\right)+C \\ y & =\frac{1}{\left(x + 2\right)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=\frac{1}{\left(x + 2\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-1)=1$ to find $C:$

$$
\begin{aligned}1 & =\frac{1}{1+C} \\ 1+C & =1 \\ C & =0.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies the condition $y(-1)=1$ is

$$
y=\frac{1}{\left(x + 2\right)}.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_50220 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies $y(\frac{3}{2})=1.$

- $y=\frac{1}{- x + \frac{5}{2}}$
- $y=\frac{2}{2 x - 1}$
- $y=\frac{1}{2 x - 2}$
- $y=x - \frac{1}{2}$
- $y=\frac{1}{x + \frac{1}{2}}$

Correct: $y=\frac{2}{2 x - 1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-{y}^{2} \\ -\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =1 \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int \,\text{d}x \\ \frac{1}{y} & =\left(x - \frac{1}{2}\right)+C \\ y & =\frac{1}{\left(x - \frac{1}{2}\right)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=\frac{1}{\left(x - \frac{1}{2}\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(\frac{3}{2})=1$ to find $C:$

$$
\begin{aligned}1 & =\frac{1}{1+C} \\ 1+C & =1 \\ C & =0.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies the condition $y(\frac{3}{2})=1$ is

$$
y=\frac{1}{\left(x - \frac{1}{2}\right)}.
$$

Author domain: x>h; initial x=h+1

### Generated moderate — source_50220 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies $y(4)=1.$

- $y=\frac{1}{- x + 5}$
- $y=\frac{1}{x - 3}$
- $y=\frac{1}{2 x - 7}$
- $y=x - 3$
- $y=\frac{1}{x - 2}$

Correct: $y=\frac{1}{x - 3}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-{y}^{2} \\ -\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =1 \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int \,\text{d}x \\ \frac{1}{y} & =\left(x - 3\right)+C \\ y & =\frac{1}{\left(x - 3\right)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=\frac{1}{\left(x - 3\right)+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(4)=1$ to find $C:$

$$
\begin{aligned}1 & =\frac{1}{1+C} \\ 1+C & =1 \\ C & =0.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies the condition $y(4)=1$ is

$$
y=\frac{1}{\left(x - 3\right)}.
$$

Author domain: x>h; initial x=h+1

## Original q-50566

Find the particular solution to the differential equation $y\frac{\text{d}y}{\text{d}x}=x$  that satisfies  $y(-3)=1.$  Assume that $y>0.$

- $y=\sqrt{2{x}^{2}-4}$
- $-y=\sqrt{x+4}$
- $-y=\sqrt{2x+7}$
- $y=\frac{1}{4}\sqrt{2{x}^{2}-2}$
- $y=\sqrt{{x}^{2}-8}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x} & =x \\ \int y\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int x\,\text{d}x \\ \int y\text{d}y & =\int x\text{d}x \\ \frac{{y}^{2}}{2} & =\frac{{x}^{2}}{2}+{C}_{1} \\ {y}^{2} & ={x}^{2}+2{C}_{1} \\ y & =\pm \sqrt{{x}^{2}+2{C}_{1}}\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y=\sqrt{{x}^{2}+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-3)=1$ to find $C:$

$$
\begin{aligned}1 & =\sqrt{(-3)^{2}+C} \\ 1 & =\sqrt{9+C} \\ C & =-8\end{aligned}
$$

Thus, the particular solution of $y\frac{\text{d}y}{\text{d}x}=x$ that satisfies the condition $y(-3)=1$ is

$$
y=\sqrt{{x}^{2}-8}.
$$

### Generated moderate — source_50566 (observed)

Find the particular solution to the differential equation $y\frac{\text{d}y}{\text{d}x}=x$  that satisfies  $y(-3)=1.$  Assume that $y>0.$

- $-y=\sqrt{2x+7}$
- $-y=\sqrt{x+4}$
- $y=\sqrt{2{x}^{2}-4}$
- $y=\sqrt{{x}^{2}-8}$
- $y=\frac{1}{4}\sqrt{2{x}^{2}-2}$

Correct: $y=\sqrt{{x}^{2}-8}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x} & =x \\ \int y\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int x\,\text{d}x \\ \int y\text{d}y & =\int x\text{d}x \\ \frac{{y}^{2}}{2} & =\frac{{x}^{2}}{2}+{C}_{1} \\ {y}^{2} & ={x}^{2}+2{C}_{1} \\ y & =\pm \sqrt{{x}^{2}+2{C}_{1}}\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y=\sqrt{{x}^{2}+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-3)=1$ to find $C:$

$$
\begin{aligned}1 & =\sqrt{(-3)^{2}+C} \\ 1 & =\sqrt{9+C} \\ C & =-8\end{aligned}
$$

Thus, the particular solution of $y\frac{\text{d}y}{\text{d}x}=x$ that satisfies the condition $y(-3)=1$ is

$$
y=\sqrt{{x}^{2}-8}.
$$

Author domain: y>0; x-h < -sqrt(8), connected interval containing h-3

### Generated moderate — source_50566 (authored)

Find the particular solution to the differential equation $y\frac{\text{d}y}{\text{d}x}=\left(x + 2\right)$  that satisfies  $y(-5)=1.$  Assume that $y>0.$

- $y=- \sqrt{\left(x + 2\right)^{2} - 8}$
- $y=\sqrt{\left(x + 2\right)^{2} - 8}$
- $y=\sqrt{\left(x + 2\right)^{2} + 8}$
- $y=\sqrt{\left(x + 2\right)^{2} + 1}$
- $y=\sqrt{2 \left(x + 2\right)^{2} - 17}$

Correct: $y=\sqrt{\left(x + 2\right)^{2} - 8}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x} & =\left(x + 2\right) \\ \int y\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(x + 2\right)\,\text{d}x \\ \int y\text{d}y & =\int \left(x + 2\right)\text{d}x \\ \frac{{y}^{2}}{2} & =\frac{{\left(x + 2\right)}^{2}}{2}+{C}_{1} \\ {y}^{2} & ={\left(x + 2\right)}^{2}+2{C}_{1} \\ y & =\pm \sqrt{{\left(x + 2\right)}^{2}+2{C}_{1}}\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y=\sqrt{{\left(x + 2\right)}^{2}+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-5)=1$ to find $C:$

$$
\begin{aligned}1 & =\sqrt{(-3)^{2}+C} \\ 1 & =\sqrt{9+C} \\ C & =-8\end{aligned}
$$

Thus, the particular solution of $y\frac{\text{d}y}{\text{d}x}=\left(x + 2\right)$ that satisfies the condition $y(-5)=1$ is

$$
y=\sqrt{{\left(x + 2\right)}^{2}-8}.
$$

Author domain: y>0; x-h < -sqrt(8), connected interval containing h-3

### Generated moderate — source_50566 (authored)

Find the particular solution to the differential equation $y\frac{\text{d}y}{\text{d}x}=\left(x - \frac{1}{2}\right)$  that satisfies  $y(- \frac{5}{2})=1.$  Assume that $y>0.$

- $y=- \sqrt{\left(x - \frac{1}{2}\right)^{2} - 8}$
- $y=\frac{\sqrt{\left(2 x - 1\right)^{2} - 32}}{2}$
- $y=\sqrt{\left(x - \frac{1}{2}\right)^{2} + 8}$
- $y=\sqrt{\left(x - \frac{1}{2}\right)^{2} + 1}$
- $y=\sqrt{2 \left(x - \frac{1}{2}\right)^{2} - 17}$

Correct: $y=\frac{\sqrt{\left(2 x - 1\right)^{2} - 32}}{2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x} & =\left(x - \frac{1}{2}\right) \\ \int y\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(x - \frac{1}{2}\right)\,\text{d}x \\ \int y\text{d}y & =\int \left(x - \frac{1}{2}\right)\text{d}x \\ \frac{{y}^{2}}{2} & =\frac{{\left(x - \frac{1}{2}\right)}^{2}}{2}+{C}_{1} \\ {y}^{2} & ={\left(x - \frac{1}{2}\right)}^{2}+2{C}_{1} \\ y & =\pm \sqrt{{\left(x - \frac{1}{2}\right)}^{2}+2{C}_{1}}\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y=\sqrt{{\left(x - \frac{1}{2}\right)}^{2}+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(- \frac{5}{2})=1$ to find $C:$

$$
\begin{aligned}1 & =\sqrt{(-3)^{2}+C} \\ 1 & =\sqrt{9+C} \\ C & =-8\end{aligned}
$$

Thus, the particular solution of $y\frac{\text{d}y}{\text{d}x}=\left(x - \frac{1}{2}\right)$ that satisfies the condition $y(- \frac{5}{2})=1$ is

$$
y=\sqrt{{\left(x - \frac{1}{2}\right)}^{2}-8}.
$$

Author domain: y>0; x-h < -sqrt(8), connected interval containing h-3

### Generated moderate — source_50566 (authored)

Find the particular solution to the differential equation $y\frac{\text{d}y}{\text{d}x}=\left(x - 3\right)$  that satisfies  $y(0)=1.$  Assume that $y>0.$

- $y=- \sqrt{\left(x - 3\right)^{2} - 8}$
- $y=\sqrt{\left(x - 3\right)^{2} - 8}$
- $y=\sqrt{\left(x - 3\right)^{2} + 8}$
- $y=\sqrt{\left(x - 3\right)^{2} + 1}$
- $y=\sqrt{2 \left(x - 3\right)^{2} - 17}$

Correct: $y=\sqrt{\left(x - 3\right)^{2} - 8}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x} & =\left(x - 3\right) \\ \int y\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(x - 3\right)\,\text{d}x \\ \int y\text{d}y & =\int \left(x - 3\right)\text{d}x \\ \frac{{y}^{2}}{2} & =\frac{{\left(x - 3\right)}^{2}}{2}+{C}_{1} \\ {y}^{2} & ={\left(x - 3\right)}^{2}+2{C}_{1} \\ y & =\pm \sqrt{{\left(x - 3\right)}^{2}+2{C}_{1}}\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y=\sqrt{{\left(x - 3\right)}^{2}+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(0)=1$ to find $C:$

$$
\begin{aligned}1 & =\sqrt{(-3)^{2}+C} \\ 1 & =\sqrt{9+C} \\ C & =-8\end{aligned}
$$

Thus, the particular solution of $y\frac{\text{d}y}{\text{d}x}=\left(x - 3\right)$ that satisfies the condition $y(0)=1$ is

$$
y=\sqrt{{\left(x - 3\right)}^{2}-8}.
$$

Author domain: y>0; x-h < -sqrt(8), connected interval containing h-3

## Original q-8308

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y$  that satisfies $y(0)=1.$

- $y={e}^{-x}$
- $y=1$
- $y={e}^{\operatorname{sin}⁡x}$
- $y={e}^{x}$
- $y=x+1$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{ln}⁡|y| & =x+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{x+C} \\ |y| & ={e}^{x+C}\, \\ y & =\pm {e}^{x+C} \\ y & =K{e}^{x}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y$ that satisfies the condition $y(0)=1$ is

$$
y={e}^{x}\,.
$$

### Generated easy — source_8308 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y$  that satisfies $y(0)=1.$

- $y={e}^{\operatorname{sin}⁡x}$
- $y=1$
- $y={e}^{-x}$
- $y=x+1$
- $y={e}^{x}$

Correct: $y={e}^{x}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{ln}⁡|y| & =x+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{x+C} \\ |y| & ={e}^{x+C}\, \\ y & =\pm {e}^{x+C} \\ y & =K{e}^{x}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y$ that satisfies the condition $y(0)=1$ is

$$
y={e}^{x}\,.
$$

Author domain: y>0; x real

### Generated easy — source_8308 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y$  that satisfies $y(-2)=1.$

- $y=e^{- x - 2}$
- $y=e^{x + 2}$
- $y=e^{2 x + 4}$
- $y=x + 3$
- $y=1$

Correct: $y=e^{x + 2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{ln}⁡|y| & =\left(x + 2\right)+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\left(x + 2\right)+C} \\ |y| & ={e}^{\left(x + 2\right)+C}\, \\ y & =\pm {e}^{\left(x + 2\right)+C} \\ y & =K{e}^{\left(x + 2\right)}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(-2)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y$ that satisfies the condition $y(-2)=1$ is

$$
y={e}^{\left(x + 2\right)}\,.
$$

Author domain: y>0; x real

### Generated easy — source_8308 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y$  that satisfies $y(\frac{1}{2})=1.$

- $y=e^{- x + \frac{1}{2}}$
- $y=e^{x - \frac{1}{2}}$
- $y=e^{2 x - 1}$
- $y=x + \frac{1}{2}$
- $y=1$

Correct: $y=e^{x - \frac{1}{2}}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{ln}⁡|y| & =\left(x - \frac{1}{2}\right)+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\left(x - \frac{1}{2}\right)+C} \\ |y| & ={e}^{\left(x - \frac{1}{2}\right)+C}\, \\ y & =\pm {e}^{\left(x - \frac{1}{2}\right)+C} \\ y & =K{e}^{\left(x - \frac{1}{2}\right)}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(\frac{1}{2})=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y$ that satisfies the condition $y(\frac{1}{2})=1$ is

$$
y={e}^{\left(x - \frac{1}{2}\right)}\,.
$$

Author domain: y>0; x real

### Generated easy — source_8308 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y$  that satisfies $y(3)=1.$

- $y=e^{- x + 3}$
- $y=e^{x - 3}$
- $y=e^{2 x - 6}$
- $y=x - 2$
- $y=1$

Correct: $y=e^{x - 3}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{ln}⁡|y| & =\left(x - 3\right)+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\left(x - 3\right)+C} \\ |y| & ={e}^{\left(x - 3\right)+C}\, \\ y & =\pm {e}^{\left(x - 3\right)+C} \\ y & =K{e}^{\left(x - 3\right)}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(3)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y$ that satisfies the condition $y(3)=1$ is

$$
y={e}^{\left(x - 3\right)}\,.
$$

Author domain: y>0; x real

## Original q-8309

Find the particular solution to the differential equation ${y}^{′}=\frac{\operatorname{sin}⁡(3x)}{\operatorname{cos}⁡(2y)}$ that satisfies $y(0)=0.$ Assume that $-\frac{\pi }{4}<y<\frac{\pi }{4}.$

- $3\operatorname{sin}⁡(2y)=1-\operatorname{cos}⁡(3x)$
- $5\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x))$
- $\operatorname{sin}⁡(2y)=1-\operatorname{cos}⁡(3x)$
- $3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x))$
- $\operatorname{sin}⁡(2y)=\operatorname{cos}⁡(3x)$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\operatorname{sin}⁡(3x)}{\operatorname{cos}⁡(2y)} \\ (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(3x) \\ \int (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(3x)\,\text{d}x \\ \int \operatorname{cos}⁡(2y)\,\text{d}y & =\int \operatorname{sin}⁡(3x)\,\text{d}x \\ \frac{1}{2}\operatorname{sin}⁡(2y) & =-\frac{1}{3}\operatorname{cos}⁡(3x)+C \\ \operatorname{sin}⁡(2y) & =-\frac{2}{3}\operatorname{cos}⁡(3x)+{C}_{1}\,,\end{aligned}
$$

where ${C}_{1}=2C.$

We now apply the condition $y(0)=0$ to find ${C}_{1}:$

$$
\begin{aligned}y(0) & =0 \\ \operatorname{sin}⁡(2\cdot 0) & =-\frac{2}{3}\operatorname{cos}⁡(3\cdot 0)+{C}_{1} \\ \operatorname{sin}⁡(0) & =-\frac{2}{3}\operatorname{cos}⁡(0)+{C}_{1} \\ 0 & =-\frac{2}{3}\cdot 1+{C}_{1} \\ {C}_{1} & =\frac{2}{3}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(2y) & =\frac{2}{3}-\frac{2}{3}\operatorname{cos}⁡(3x) \\  & =\frac{2}{3}(1-\operatorname{cos}⁡(3x))\end{aligned}
$$

Finally, we can write the above equation as

$$
3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x)).
$$

### Generated hard — source_8309 (observed)

Find the particular solution to the differential equation ${y}^{′}=\frac{\operatorname{sin}⁡(3x)}{\operatorname{cos}⁡(2y)}$ that satisfies $y(0)=0.$ Assume that $-\frac{\pi }{4}<y<\frac{\pi }{4}.$

- $\operatorname{sin}⁡(2y)=1-\operatorname{cos}⁡(3x)$
- $5\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x))$
- $3\operatorname{sin}⁡(2y)=1-\operatorname{cos}⁡(3x)$
- $\operatorname{sin}⁡(2y)=\operatorname{cos}⁡(3x)$
- $3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x))$

Correct: $3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x))$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\operatorname{sin}⁡(3x)}{\operatorname{cos}⁡(2y)} \\ (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(3x) \\ \int (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(3x)\,\text{d}x \\ \int \operatorname{cos}⁡(2y)\,\text{d}y & =\int \operatorname{sin}⁡(3x)\,\text{d}x \\ \frac{1}{2}\operatorname{sin}⁡(2y) & =-\frac{1}{3}\operatorname{cos}⁡(3x)+C \\ \operatorname{sin}⁡(2y) & =-\frac{2}{3}\operatorname{cos}⁡(3x)+{C}_{1}\,,\end{aligned}
$$

where ${C}_{1}=2C.$

We now apply the condition $y(0)=0$ to find ${C}_{1}:$

$$
\begin{aligned}y(0) & =0 \\ \operatorname{sin}⁡(2\cdot 0) & =-\frac{2}{3}\operatorname{cos}⁡(3\cdot 0)+{C}_{1} \\ \operatorname{sin}⁡(0) & =-\frac{2}{3}\operatorname{cos}⁡(0)+{C}_{1} \\ 0 & =-\frac{2}{3}\cdot 1+{C}_{1} \\ {C}_{1} & =\frac{2}{3}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(2y) & =\frac{2}{3}-\frac{2}{3}\operatorname{cos}⁡(3x) \\  & =\frac{2}{3}(1-\operatorname{cos}⁡(3x))\end{aligned}
$$

Finally, we can write the above equation as

$$
3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x)).
$$

Author domain: -pi/4<y<pi/4; cos(3*(x-h))> -1/2; local component containing h

### Generated hard — source_8309 (authored)

Find the particular solution to the differential equation ${y}^{′}=\frac{\operatorname{sin}⁡(3\left(x + 2\right))}{\operatorname{cos}⁡(2y)}$ that satisfies $y(-2)=0.$ Assume that $-\frac{\pi }{4}<y<\frac{\pi }{4}.$

- $3 \sin{\left(2 y \right)}=- \cos{\left(3 x + 6 \right)} + 1$
- $3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x + 6 \right)} + 2$
- $3 \sin{\left(2 y \right)}=2 \cos{\left(3 x + 6 \right)} + 2$
- $3 \sin{\left(2 y \right)}=2 \cos{\left(3 x + 6 \right)}$
- $3 \sin{\left(2 y \right)}=- 6 \cos{\left(3 x + 6 \right)} + 6$

Correct: $3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x + 6 \right)} + 2$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\operatorname{sin}⁡(3\left(x + 2\right))}{\operatorname{cos}⁡(2y)} \\ (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(3\left(x + 2\right)) \\ \int (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(3\left(x + 2\right))\,\text{d}x \\ \int \operatorname{cos}⁡(2y)\,\text{d}y & =\int \operatorname{sin}⁡(3\left(x + 2\right))\,\text{d}x \\ \frac{1}{2}\operatorname{sin}⁡(2y) & =-\frac{1}{3}\operatorname{cos}⁡(3\left(x + 2\right))+C \\ \operatorname{sin}⁡(2y) & =-\frac{2}{3}\operatorname{cos}⁡(3\left(x + 2\right))+{C}_{1}\,,\end{aligned}
$$

where ${C}_{1}=2C.$

We now apply the condition $y(-2)=0$ to find ${C}_{1}:$

$$
\begin{aligned}y(-2) & =0 \\ \operatorname{sin}⁡(2\cdot 0) & =-\frac{2}{3}\operatorname{cos}⁡(3\cdot 0)+{C}_{1} \\ \operatorname{sin}⁡(0) & =-\frac{2}{3}\operatorname{cos}⁡(0)+{C}_{1} \\ 0 & =-\frac{2}{3}\cdot 1+{C}_{1} \\ {C}_{1} & =\frac{2}{3}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(2y) & =\frac{2}{3}-\frac{2}{3}\operatorname{cos}⁡(3\left(x + 2\right)) \\  & =\frac{2}{3}(1-\operatorname{cos}⁡(3\left(x + 2\right)))\end{aligned}
$$

Finally, we can write the above equation as

$$
3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3\left(x + 2\right))).
$$

Author domain: -pi/4<y<pi/4; cos(3*(x-h))> -1/2; local component containing h

### Generated hard — source_8309 (authored)

Find the particular solution to the differential equation ${y}^{′}=\frac{\operatorname{sin}⁡(3\left(x - \frac{1}{2}\right))}{\operatorname{cos}⁡(2y)}$ that satisfies $y(\frac{1}{2})=0.$ Assume that $-\frac{\pi }{4}<y<\frac{\pi }{4}.$

- $3 \sin{\left(2 y \right)}=- \cos{\left(3 x - \frac{3}{2} \right)} + 1$
- $3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x - \frac{3}{2} \right)} + 2$
- $3 \sin{\left(2 y \right)}=2 \cos{\left(3 x - \frac{3}{2} \right)} + 2$
- $3 \sin{\left(2 y \right)}=2 \cos{\left(3 x - \frac{3}{2} \right)}$
- $3 \sin{\left(2 y \right)}=- 6 \cos{\left(3 x - \frac{3}{2} \right)} + 6$

Correct: $3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x - \frac{3}{2} \right)} + 2$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\operatorname{sin}⁡(3\left(x - \frac{1}{2}\right))}{\operatorname{cos}⁡(2y)} \\ (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(3\left(x - \frac{1}{2}\right)) \\ \int (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(3\left(x - \frac{1}{2}\right))\,\text{d}x \\ \int \operatorname{cos}⁡(2y)\,\text{d}y & =\int \operatorname{sin}⁡(3\left(x - \frac{1}{2}\right))\,\text{d}x \\ \frac{1}{2}\operatorname{sin}⁡(2y) & =-\frac{1}{3}\operatorname{cos}⁡(3\left(x - \frac{1}{2}\right))+C \\ \operatorname{sin}⁡(2y) & =-\frac{2}{3}\operatorname{cos}⁡(3\left(x - \frac{1}{2}\right))+{C}_{1}\,,\end{aligned}
$$

where ${C}_{1}=2C.$

We now apply the condition $y(\frac{1}{2})=0$ to find ${C}_{1}:$

$$
\begin{aligned}y(\frac{1}{2}) & =0 \\ \operatorname{sin}⁡(2\cdot 0) & =-\frac{2}{3}\operatorname{cos}⁡(3\cdot 0)+{C}_{1} \\ \operatorname{sin}⁡(0) & =-\frac{2}{3}\operatorname{cos}⁡(0)+{C}_{1} \\ 0 & =-\frac{2}{3}\cdot 1+{C}_{1} \\ {C}_{1} & =\frac{2}{3}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(2y) & =\frac{2}{3}-\frac{2}{3}\operatorname{cos}⁡(3\left(x - \frac{1}{2}\right)) \\  & =\frac{2}{3}(1-\operatorname{cos}⁡(3\left(x - \frac{1}{2}\right)))\end{aligned}
$$

Finally, we can write the above equation as

$$
3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3\left(x - \frac{1}{2}\right))).
$$

Author domain: -pi/4<y<pi/4; cos(3*(x-h))> -1/2; local component containing h

### Generated hard — source_8309 (authored)

Find the particular solution to the differential equation ${y}^{′}=\frac{\operatorname{sin}⁡(3\left(x - 3\right))}{\operatorname{cos}⁡(2y)}$ that satisfies $y(3)=0.$ Assume that $-\frac{\pi }{4}<y<\frac{\pi }{4}.$

- $3 \sin{\left(2 y \right)}=- \cos{\left(3 x - 9 \right)} + 1$
- $3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x - 9 \right)} + 2$
- $3 \sin{\left(2 y \right)}=2 \cos{\left(3 x - 9 \right)} + 2$
- $3 \sin{\left(2 y \right)}=2 \cos{\left(3 x - 9 \right)}$
- $3 \sin{\left(2 y \right)}=- 6 \cos{\left(3 x - 9 \right)} + 6$

Correct: $3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x - 9 \right)} + 2$

Worked solution:
We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\operatorname{sin}⁡(3\left(x - 3\right))}{\operatorname{cos}⁡(2y)} \\ (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(3\left(x - 3\right)) \\ \int (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(3\left(x - 3\right))\,\text{d}x \\ \int \operatorname{cos}⁡(2y)\,\text{d}y & =\int \operatorname{sin}⁡(3\left(x - 3\right))\,\text{d}x \\ \frac{1}{2}\operatorname{sin}⁡(2y) & =-\frac{1}{3}\operatorname{cos}⁡(3\left(x - 3\right))+C \\ \operatorname{sin}⁡(2y) & =-\frac{2}{3}\operatorname{cos}⁡(3\left(x - 3\right))+{C}_{1}\,,\end{aligned}
$$

where ${C}_{1}=2C.$

We now apply the condition $y(3)=0$ to find ${C}_{1}:$

$$
\begin{aligned}y(3) & =0 \\ \operatorname{sin}⁡(2\cdot 0) & =-\frac{2}{3}\operatorname{cos}⁡(3\cdot 0)+{C}_{1} \\ \operatorname{sin}⁡(0) & =-\frac{2}{3}\operatorname{cos}⁡(0)+{C}_{1} \\ 0 & =-\frac{2}{3}\cdot 1+{C}_{1} \\ {C}_{1} & =\frac{2}{3}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(2y) & =\frac{2}{3}-\frac{2}{3}\operatorname{cos}⁡(3\left(x - 3\right)) \\  & =\frac{2}{3}(1-\operatorname{cos}⁡(3\left(x - 3\right)))\end{aligned}
$$

Finally, we can write the above equation as

$$
3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3\left(x - 3\right))).
$$

Author domain: -pi/4<y<pi/4; cos(3*(x-h))> -1/2; local component containing h

## Original q-14309

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+1}$  that satisfies $y(1)=1.$

- $y=\frac{2}{\pi +2-4\operatorname{arctan}⁡(x)}$
- $y=\frac{4}{\pi +4-4\operatorname{arctan}⁡(x)}$
- $y=\frac{1}{\pi +1-\operatorname{arctan}⁡(x)}$
- $y=\frac{1}{\pi -4+4\operatorname{arctan}⁡(x)}$
- $y=\frac{4}{\pi -1-\operatorname{arctan}⁡(x)}$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{x}^{2}+1} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}+1} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}+1}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{{x}^{2}+1}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{arctan}⁡(x)+C \\ \frac{1}{y} & =-(\operatorname{arctan}⁡(x)+C) \\ y & =-\frac{1}{\operatorname{arctan}⁡(x)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=-\frac{1}{\operatorname{arctan}⁡(x)+C}.
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=1$ to find $C:$

$$
\begin{aligned}1 & =-\frac{1}{\operatorname{arctan}⁡(1)+C} \\ 1 & =-\frac{1}{\frac{\pi }{4}+C} \\ C & =-\frac{\pi }{4}-1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+1}$ that satisfies the condition $y(1)=1$ is

$$
y=-\frac{1}{\operatorname{arctan}⁡(x)-\frac{\pi }{4}-1}=\frac{4}{\pi +4-4\operatorname{arctan}⁡(x)}.
$$

### Generated easy — source_14309 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+1}$  that satisfies $y(1)=1.$

- $y=\frac{1}{\pi +1-\operatorname{arctan}⁡(x)}$
- $y=\frac{4}{\pi +4-4\operatorname{arctan}⁡(x)}$
- $y=\frac{2}{\pi +2-4\operatorname{arctan}⁡(x)}$
- $y=\frac{4}{\pi -1-\operatorname{arctan}⁡(x)}$
- $y=\frac{1}{\pi -4+4\operatorname{arctan}⁡(x)}$

Correct: $y=\frac{4}{\pi +4-4\operatorname{arctan}⁡(x)}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{x}^{2}+1} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}+1} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}+1}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{{x}^{2}+1}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{arctan}⁡(x)+C \\ \frac{1}{y} & =-(\operatorname{arctan}⁡(x)+C) \\ y & =-\frac{1}{\operatorname{arctan}⁡(x)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=-\frac{1}{\operatorname{arctan}⁡(x)+C}.
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=1$ to find $C:$

$$
\begin{aligned}1 & =-\frac{1}{\operatorname{arctan}⁡(1)+C} \\ 1 & =-\frac{1}{\frac{\pi }{4}+C} \\ C & =-\frac{\pi }{4}-1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+1}$ that satisfies the condition $y(1)=1$ is

$$
y=-\frac{1}{\operatorname{arctan}⁡(x)-\frac{\pi }{4}-1}=\frac{4}{\pi +4-4\operatorname{arctan}⁡(x)}.
$$

Author domain: denominator !=0; connected interval containing h+1

### Generated easy — source_14309 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{\left(x + 2\right)}^{2}+1}$  that satisfies $y(-1)=1.$

- $y=\frac{4}{4 \operatorname{atan}{\left(x + 2 \right)} + \pi + 4}$
- $y=\frac{4}{- 4 \operatorname{atan}{\left(x + 2 \right)} + \pi + 4}$
- $y=\frac{4}{- 4 \operatorname{atan}{\left(x + 2 \right)} + 4}$
- $y=- \operatorname{atan}{\left(x + 2 \right)} + \frac{\pi}{4} + 1$
- $y=\frac{4}{- 2 \operatorname{atan}{\left(x + 2 \right)} + \pi + 4}$

Correct: $y=\frac{4}{- 4 \operatorname{atan}{\left(x + 2 \right)} + \pi + 4}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{\left(x + 2\right)}^{2}+1} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{\left(x + 2\right)}^{2}+1} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{\left(x + 2\right)}^{2}+1}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{{\left(x + 2\right)}^{2}+1}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{arctan}⁡(\left(x + 2\right))+C \\ \frac{1}{y} & =-(\operatorname{arctan}⁡(\left(x + 2\right))+C) \\ y & =-\frac{1}{\operatorname{arctan}⁡(\left(x + 2\right))+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=-\frac{1}{\operatorname{arctan}⁡(\left(x + 2\right))+C}.
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-1)=1$ to find $C:$

$$
\begin{aligned}1 & =-\frac{1}{\operatorname{arctan}⁡(1)+C} \\ 1 & =-\frac{1}{\frac{\pi }{4}+C} \\ C & =-\frac{\pi }{4}-1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{\left(x + 2\right)}^{2}+1}$ that satisfies the condition $y(-1)=1$ is

$$
y=-\frac{1}{\operatorname{arctan}⁡(\left(x + 2\right))-\frac{\pi }{4}-1}=\frac{4}{\pi +4-4\operatorname{arctan}⁡(\left(x + 2\right))}.
$$

Author domain: denominator !=0; connected interval containing h+1

### Generated easy — source_14309 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{\left(x - \frac{1}{2}\right)}^{2}+1}$  that satisfies $y(\frac{3}{2})=1.$

- $y=\frac{4}{4 \operatorname{atan}{\left(x - \frac{1}{2} \right)} + \pi + 4}$
- $y=\frac{4}{- 4 \operatorname{atan}{\left(x - \frac{1}{2} \right)} + \pi + 4}$
- $y=\frac{4}{- 4 \operatorname{atan}{\left(x - \frac{1}{2} \right)} + 4}$
- $y=- \operatorname{atan}{\left(x - \frac{1}{2} \right)} + \frac{\pi}{4} + 1$
- $y=\frac{4}{- 2 \operatorname{atan}{\left(x - \frac{1}{2} \right)} + \pi + 4}$

Correct: $y=\frac{4}{- 4 \operatorname{atan}{\left(x - \frac{1}{2} \right)} + \pi + 4}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{\left(x - \frac{1}{2}\right)}^{2}+1} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{\left(x - \frac{1}{2}\right)}^{2}+1} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{\left(x - \frac{1}{2}\right)}^{2}+1}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{{\left(x - \frac{1}{2}\right)}^{2}+1}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{arctan}⁡(\left(x - \frac{1}{2}\right))+C \\ \frac{1}{y} & =-(\operatorname{arctan}⁡(\left(x - \frac{1}{2}\right))+C) \\ y & =-\frac{1}{\operatorname{arctan}⁡(\left(x - \frac{1}{2}\right))+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=-\frac{1}{\operatorname{arctan}⁡(\left(x - \frac{1}{2}\right))+C}.
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(\frac{3}{2})=1$ to find $C:$

$$
\begin{aligned}1 & =-\frac{1}{\operatorname{arctan}⁡(1)+C} \\ 1 & =-\frac{1}{\frac{\pi }{4}+C} \\ C & =-\frac{\pi }{4}-1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{\left(x - \frac{1}{2}\right)}^{2}+1}$ that satisfies the condition $y(\frac{3}{2})=1$ is

$$
y=-\frac{1}{\operatorname{arctan}⁡(\left(x - \frac{1}{2}\right))-\frac{\pi }{4}-1}=\frac{4}{\pi +4-4\operatorname{arctan}⁡(\left(x - \frac{1}{2}\right))}.
$$

Author domain: denominator !=0; connected interval containing h+1

### Generated easy — source_14309 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{\left(x - 3\right)}^{2}+1}$  that satisfies $y(4)=1.$

- $y=\frac{4}{4 \operatorname{atan}{\left(x - 3 \right)} + \pi + 4}$
- $y=\frac{4}{- 4 \operatorname{atan}{\left(x - 3 \right)} + \pi + 4}$
- $y=\frac{4}{- 4 \operatorname{atan}{\left(x - 3 \right)} + 4}$
- $y=- \operatorname{atan}{\left(x - 3 \right)} + \frac{\pi}{4} + 1$
- $y=\frac{4}{- 2 \operatorname{atan}{\left(x - 3 \right)} + \pi + 4}$

Correct: $y=\frac{4}{- 4 \operatorname{atan}{\left(x - 3 \right)} + \pi + 4}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{\left(x - 3\right)}^{2}+1} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{\left(x - 3\right)}^{2}+1} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{\left(x - 3\right)}^{2}+1}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{{\left(x - 3\right)}^{2}+1}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{arctan}⁡(\left(x - 3\right))+C \\ \frac{1}{y} & =-(\operatorname{arctan}⁡(\left(x - 3\right))+C) \\ y & =-\frac{1}{\operatorname{arctan}⁡(\left(x - 3\right))+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=-\frac{1}{\operatorname{arctan}⁡(\left(x - 3\right))+C}.
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(4)=1$ to find $C:$

$$
\begin{aligned}1 & =-\frac{1}{\operatorname{arctan}⁡(1)+C} \\ 1 & =-\frac{1}{\frac{\pi }{4}+C} \\ C & =-\frac{\pi }{4}-1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{\left(x - 3\right)}^{2}+1}$ that satisfies the condition $y(4)=1$ is

$$
y=-\frac{1}{\operatorname{arctan}⁡(\left(x - 3\right))-\frac{\pi }{4}-1}=\frac{4}{\pi +4-4\operatorname{arctan}⁡(\left(x - 3\right))}.
$$

Author domain: denominator !=0; connected interval containing h+1

## Original q-50219

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=-\frac{xy}{\operatorname{ln}⁡y}$ that satisfies $y(0)=e.$

- ${ln}^{2}⁡y=(1-x)^{2}$
- ${ln}^{2}⁡y=1-2{x}^{2}$
- ${ln}^{2}⁡y=1-{x}^{2}$
- ${ln}^{2}⁡y={x}^{2}+1$
- ${ln}^{2}⁡y=2{x}^{2}+1$

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{xy}{\operatorname{ln}⁡y} \\ \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x} & =-x \\ \int \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int x\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\,\text{d}y & =-\int x\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =-\frac{{x}^{2}}{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral in the left-hand side of this equality, we use a substitution $u=\operatorname{ln}⁡y.$ Then,  we have

$$
\frac{\text{d}u}{\text{d}y}=\frac{1}{y}\,⟹\,\text{d}u=\frac{1}{y}\,\text{d}y.
$$

So we get

$$
\begin{aligned}\int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =\int \operatorname{ln}⁡y(\frac{1}{y}\,\text{d}y) \\  & =\int u\,\text{d}u \\  & =\frac{{u}^{2}}{2}+{C}_{2} \\  & =\frac{1}{2}{ln}^{2}⁡y+{C}_{2}.\end{aligned}
$$

Hence,

$$
\begin{aligned}\frac{1}{2}{ln}^{2}⁡y+{C}_{2} & =-\frac{{x}^{2}}{2}+{C}_{1} \\ {ln}^{2}⁡y & =-{x}^{2}+2({C}_{1}-{C}_{2}) \\ {ln}^{2}⁡y & =C-{x}^{2},\end{aligned}
$$

where $C=2({C}_{1}-{C}_{2})$ is an arbitrary constant.

We now apply the condition $y(0)=e$ to find $C:$

$$
\begin{aligned}{ln}^{2}⁡e & =C-{0}^{2} \\ {1}^{2} & =C \\ C & =1\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{ln}^{2}⁡y=1-{x}^{2}.
$$

### Generated hard — source_50219 (observed)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=-\frac{xy}{\operatorname{ln}⁡y}$ that satisfies $y(0)=e.$

- ${ln}^{2}⁡y=1-{x}^{2}$
- ${ln}^{2}⁡y=1-2{x}^{2}$
- ${ln}^{2}⁡y=(1-x)^{2}$
- ${ln}^{2}⁡y=2{x}^{2}+1$
- ${ln}^{2}⁡y={x}^{2}+1$

Correct: ${ln}^{2}⁡y=1-{x}^{2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{xy}{\operatorname{ln}⁡y} \\ \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x} & =-x \\ \int \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int x\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\,\text{d}y & =-\int x\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =-\frac{{x}^{2}}{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral in the left-hand side of this equality, we use a substitution $u=\operatorname{ln}⁡y.$ Then,  we have

$$
\frac{\text{d}u}{\text{d}y}=\frac{1}{y}\,⟹\,\text{d}u=\frac{1}{y}\,\text{d}y.
$$

So we get

$$
\begin{aligned}\int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =\int \operatorname{ln}⁡y(\frac{1}{y}\,\text{d}y) \\  & =\int u\,\text{d}u \\  & =\frac{{u}^{2}}{2}+{C}_{2} \\  & =\frac{1}{2}{ln}^{2}⁡y+{C}_{2}.\end{aligned}
$$

Hence,

$$
\begin{aligned}\frac{1}{2}{ln}^{2}⁡y+{C}_{2} & =-\frac{{x}^{2}}{2}+{C}_{1} \\ {ln}^{2}⁡y & =-{x}^{2}+2({C}_{1}-{C}_{2}) \\ {ln}^{2}⁡y & =C-{x}^{2},\end{aligned}
$$

where $C=2({C}_{1}-{C}_{2})$ is an arbitrary constant.

We now apply the condition $y(0)=e$ to find $C:$

$$
\begin{aligned}{ln}^{2}⁡e & =C-{0}^{2} \\ {1}^{2} & =C \\ C & =1\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{ln}^{2}⁡y=1-{x}^{2}.
$$

Author domain: y>1, |x-h|<1; branch containing initial y=e

### Generated hard — source_50219 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=-\frac{\left(x + 2\right)y}{\operatorname{ln}⁡y}$ that satisfies $y(-2)=e.$

- $\log{\left(y \right)}^{2}=\left(x + 2\right)^{2} + 1$
- $\log{\left(y \right)}^{2}=- \left(x + 2\right)^{2} + 1$
- $\log{\left(y \right)}^{2}=\left(- x - 1\right)^{2}$
- $\log{\left(y \right)}^{2}=- \left(x + 2\right)^{2} + e$
- $\log{\left(y \right)}^{2}=- 2 \left(x + 2\right)^{2} + 1$

Correct: $\log{\left(y \right)}^{2}=- \left(x + 2\right)^{2} + 1$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{\left(x + 2\right)y}{\operatorname{ln}⁡y} \\ \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x} & =-\left(x + 2\right) \\ \int \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int \left(x + 2\right)\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\,\text{d}y & =-\int \left(x + 2\right)\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =-\frac{{\left(x + 2\right)}^{2}}{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral in the left-hand side of this equality, we use a substitution $u=\operatorname{ln}⁡y.$ Then,  we have

$$
\frac{\text{d}u}{\text{d}y}=\frac{1}{y}\,⟹\,\text{d}u=\frac{1}{y}\,\text{d}y.
$$

So we get

$$
\begin{aligned}\int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =\int \operatorname{ln}⁡y(\frac{1}{y}\,\text{d}y) \\  & =\int u\,\text{d}u \\  & =\frac{{u}^{2}}{2}+{C}_{2} \\  & =\frac{1}{2}{ln}^{2}⁡y+{C}_{2}.\end{aligned}
$$

Hence,

$$
\begin{aligned}\frac{1}{2}{ln}^{2}⁡y+{C}_{2} & =-\frac{{\left(x + 2\right)}^{2}}{2}+{C}_{1} \\ {ln}^{2}⁡y & =-{\left(x + 2\right)}^{2}+2({C}_{1}-{C}_{2}) \\ {ln}^{2}⁡y & =C-{\left(x + 2\right)}^{2},\end{aligned}
$$

where $C=2({C}_{1}-{C}_{2})$ is an arbitrary constant.

We now apply the condition $y(-2)=e$ to find $C:$

$$
\begin{aligned}{ln}^{2}⁡e & =C-{0}^{2} \\ {1}^{2} & =C \\ C & =1\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{ln}^{2}⁡y=1-{\left(x + 2\right)}^{2}.
$$

Author domain: y>1, |x-h|<1; branch containing initial y=e

### Generated hard — source_50219 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=-\frac{\left(x - \frac{1}{2}\right)y}{\operatorname{ln}⁡y}$ that satisfies $y(\frac{1}{2})=e.$

- $\log{\left(y \right)}^{2}=\left(x - \frac{1}{2}\right)^{2} + 1$
- $\log{\left(y \right)}^{2}=- x^{2} + x + \frac{3}{4}$
- $\log{\left(y \right)}^{2}=\left(- x + \frac{3}{2}\right)^{2}$
- $\log{\left(y \right)}^{2}=- \left(x - \frac{1}{2}\right)^{2} + e$
- $\log{\left(y \right)}^{2}=- 2 \left(x - \frac{1}{2}\right)^{2} + 1$

Correct: $\log{\left(y \right)}^{2}=- x^{2} + x + \frac{3}{4}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{\left(x - \frac{1}{2}\right)y}{\operatorname{ln}⁡y} \\ \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x} & =-\left(x - \frac{1}{2}\right) \\ \int \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int \left(x - \frac{1}{2}\right)\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\,\text{d}y & =-\int \left(x - \frac{1}{2}\right)\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =-\frac{{\left(x - \frac{1}{2}\right)}^{2}}{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral in the left-hand side of this equality, we use a substitution $u=\operatorname{ln}⁡y.$ Then,  we have

$$
\frac{\text{d}u}{\text{d}y}=\frac{1}{y}\,⟹\,\text{d}u=\frac{1}{y}\,\text{d}y.
$$

So we get

$$
\begin{aligned}\int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =\int \operatorname{ln}⁡y(\frac{1}{y}\,\text{d}y) \\  & =\int u\,\text{d}u \\  & =\frac{{u}^{2}}{2}+{C}_{2} \\  & =\frac{1}{2}{ln}^{2}⁡y+{C}_{2}.\end{aligned}
$$

Hence,

$$
\begin{aligned}\frac{1}{2}{ln}^{2}⁡y+{C}_{2} & =-\frac{{\left(x - \frac{1}{2}\right)}^{2}}{2}+{C}_{1} \\ {ln}^{2}⁡y & =-{\left(x - \frac{1}{2}\right)}^{2}+2({C}_{1}-{C}_{2}) \\ {ln}^{2}⁡y & =C-{\left(x - \frac{1}{2}\right)}^{2},\end{aligned}
$$

where $C=2({C}_{1}-{C}_{2})$ is an arbitrary constant.

We now apply the condition $y(\frac{1}{2})=e$ to find $C:$

$$
\begin{aligned}{ln}^{2}⁡e & =C-{0}^{2} \\ {1}^{2} & =C \\ C & =1\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{ln}^{2}⁡y=1-{\left(x - \frac{1}{2}\right)}^{2}.
$$

Author domain: y>1, |x-h|<1; branch containing initial y=e

### Generated hard — source_50219 (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=-\frac{\left(x - 3\right)y}{\operatorname{ln}⁡y}$ that satisfies $y(3)=e.$

- $\log{\left(y \right)}^{2}=\left(x - 3\right)^{2} + 1$
- $\log{\left(y \right)}^{2}=- \left(x - 3\right)^{2} + 1$
- $\log{\left(y \right)}^{2}=\left(- x + 4\right)^{2}$
- $\log{\left(y \right)}^{2}=- \left(x - 3\right)^{2} + e$
- $\log{\left(y \right)}^{2}=- 2 \left(x - 3\right)^{2} + 1$

Correct: $\log{\left(y \right)}^{2}=- \left(x - 3\right)^{2} + 1$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{\left(x - 3\right)y}{\operatorname{ln}⁡y} \\ \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x} & =-\left(x - 3\right) \\ \int \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int \left(x - 3\right)\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\,\text{d}y & =-\int \left(x - 3\right)\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =-\frac{{\left(x - 3\right)}^{2}}{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral in the left-hand side of this equality, we use a substitution $u=\operatorname{ln}⁡y.$ Then,  we have

$$
\frac{\text{d}u}{\text{d}y}=\frac{1}{y}\,⟹\,\text{d}u=\frac{1}{y}\,\text{d}y.
$$

So we get

$$
\begin{aligned}\int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =\int \operatorname{ln}⁡y(\frac{1}{y}\,\text{d}y) \\  & =\int u\,\text{d}u \\  & =\frac{{u}^{2}}{2}+{C}_{2} \\  & =\frac{1}{2}{ln}^{2}⁡y+{C}_{2}.\end{aligned}
$$

Hence,

$$
\begin{aligned}\frac{1}{2}{ln}^{2}⁡y+{C}_{2} & =-\frac{{\left(x - 3\right)}^{2}}{2}+{C}_{1} \\ {ln}^{2}⁡y & =-{\left(x - 3\right)}^{2}+2({C}_{1}-{C}_{2}) \\ {ln}^{2}⁡y & =C-{\left(x - 3\right)}^{2},\end{aligned}
$$

where $C=2({C}_{1}-{C}_{2})$ is an arbitrary constant.

We now apply the condition $y(3)=e$ to find $C:$

$$
\begin{aligned}{ln}^{2}⁡e & =C-{0}^{2} \\ {1}^{2} & =C \\ C & =1\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{ln}^{2}⁡y=1-{\left(x - 3\right)}^{2}.
$$

Author domain: y>1, |x-h|<1; branch containing initial y=e

### Generated easy — exponential_rate (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=2 y$ that satisfies $y(0)=3.$

- $y=e^{2 x}$
- $y=3 e^{2 x}$
- $y=3 e^{- 2 x}$
- $y=3 e^{\frac{x}{2}}$
- $y=6 x + 3$

Correct: $y=3 e^{2 x}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2 y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =2 \\ \int\frac{1}{y}\,\text{d}y & =\int 2\,\text{d}x \\ \ln|y| & =2 x+C\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}y & =e^{C + 2 x} \\ y & =Ke^{2 x}\end{aligned}
$$

We now apply the condition $y(0)=3$ to find $K:$

$$
\begin{aligned}3 & =K e^0 \\ K & =3\end{aligned}
$$

Thus, the particular solution is

$$
y=3 e^{2 x}.
$$

Author domain: y>0; x real

### Generated easy — exponential_rate (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=3 y$ that satisfies $y(-2)=4.$

- $y=e^{3 x + 6}$
- $y=4 e^{3 x + 6}$
- $y=4 e^{- 3 x - 6}$
- $y=4 e^{\frac{x}{3} + \frac{2}{3}}$
- $y=12 x + 28$

Correct: $y=4 e^{3 x + 6}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3 y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =3 \\ \int\frac{1}{y}\,\text{d}y & =\int 3\,\text{d}x \\ \ln|y| & =3 x + 6+C\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}y & =e^{C + 3 x + 6} \\ y & =Ke^{3 x + 6}\end{aligned}
$$

We now apply the condition $y(-2)=4$ to find $K:$

$$
\begin{aligned}4 & =K e^0 \\ K & =4\end{aligned}
$$

Thus, the particular solution is

$$
y=4 e^{3 x + 6}.
$$

Author domain: y>0; x real

### Generated easy — exponential_rate (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=4 y$ that satisfies $y(\frac{1}{2})=2.$

- $y=e^{4 x - 2}$
- $y=2 e^{4 x - 2}$
- $y=2 e^{- 4 x + 2}$
- $y=2 e^{\frac{x}{4} - \frac{1}{8}}$
- $y=8 x - 2$

Correct: $y=2 e^{4 x - 2}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =4 \\ \int\frac{1}{y}\,\text{d}y & =\int 4\,\text{d}x \\ \ln|y| & =4 x - 2+C\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}y & =e^{C + 4 x - 2} \\ y & =Ke^{4 x - 2}\end{aligned}
$$

We now apply the condition $y(\frac{1}{2})=2$ to find $K:$

$$
\begin{aligned}2 & =K e^0 \\ K & =2\end{aligned}
$$

Thus, the particular solution is

$$
y=2 e^{4 x - 2}.
$$

Author domain: y>0; x real

### Generated easy — exponential_rate (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=5 y$ that satisfies $y(3)=3.$

- $y=e^{5 x - 15}$
- $y=3 e^{5 x - 15}$
- $y=3 e^{- 5 x + 15}$
- $y=3 e^{\frac{x}{5} - \frac{3}{5}}$
- $y=15 x - 42$

Correct: $y=3 e^{5 x - 15}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =5 y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =5 \\ \int\frac{1}{y}\,\text{d}y & =\int 5\,\text{d}x \\ \ln|y| & =5 x - 15+C\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}y & =e^{C + 5 x - 15} \\ y & =Ke^{5 x - 15}\end{aligned}
$$

We now apply the condition $y(3)=3$ to find $K:$

$$
\begin{aligned}3 & =K e^0 \\ K & =3\end{aligned}
$$

Thus, the particular solution is

$$
y=3 e^{5 x - 15}.
$$

Author domain: y>0; x real

### Generated moderate — reciprocal_initial (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+2 y^{2}=0$ that satisfies $y(0)=3.$

- $y=18 x + 3$
- $y=\frac{3}{6 x + 1}$
- $y=\frac{3}{- 6 x + 1}$
- $y=\frac{3}{2 x + 1}$
- $y=\frac{1}{2 x + 3}$

Correct: $y=\frac{3}{6 x + 1}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 2 y^{2} \\ -\frac{1}{y^2}\,\text{d}y & =2\,\text{d}x \\ -\int\frac{1}{y^2}\,\text{d}y & =\int 2\,\text{d}x \\ \frac{1}{y} & =2 x+C \\ y & =\frac{1}{2 x+C}\end{aligned}
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(0)=3$ to find $C:$

$$
\begin{aligned}3 & =\frac{1}{C} \\ C & =\frac{1}{3}\end{aligned}
$$

Thus, the particular solution is

$$
y=\frac{3}{6 x + 1}.
$$

Author domain: x>-1/6; y>0; connected interval containing initial x=0

### Generated moderate — reciprocal_initial (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+3 y^{2}=0$ that satisfies $y(-2)=4.$

- $y=48 x + 100$
- $y=\frac{4}{12 x + 25}$
- $y=\frac{4}{- 12 x - 23}$
- $y=\frac{4}{3 x + 7}$
- $y=\frac{1}{3 x + 10}$

Correct: $y=\frac{4}{12 x + 25}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 3 y^{2} \\ -\frac{1}{y^2}\,\text{d}y & =3\,\text{d}x \\ -\int\frac{1}{y^2}\,\text{d}y & =\int 3\,\text{d}x \\ \frac{1}{y} & =3 x + 6+C \\ y & =\frac{1}{3 x + 6+C}\end{aligned}
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-2)=4$ to find $C:$

$$
\begin{aligned}4 & =\frac{1}{C} \\ C & =\frac{1}{4}\end{aligned}
$$

Thus, the particular solution is

$$
y=\frac{4}{12 x + 25}.
$$

Author domain: x>-25/12; y>0; connected interval containing initial x=-2

### Generated moderate — reciprocal_initial (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+4 y^{2}=0$ that satisfies $y(\frac{1}{2})=2.$

- $y=16 x - 6$
- $y=\frac{2}{8 x - 3}$
- $y=\frac{2}{- 8 x + 5}$
- $y=\frac{2}{4 x - 1}$
- $y=\frac{1}{4 x}$

Correct: $y=\frac{2}{8 x - 3}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 4 y^{2} \\ -\frac{1}{y^2}\,\text{d}y & =4\,\text{d}x \\ -\int\frac{1}{y^2}\,\text{d}y & =\int 4\,\text{d}x \\ \frac{1}{y} & =4 x - 2+C \\ y & =\frac{1}{4 x - 2+C}\end{aligned}
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(\frac{1}{2})=2$ to find $C:$

$$
\begin{aligned}2 & =\frac{1}{C} \\ C & =\frac{1}{2}\end{aligned}
$$

Thus, the particular solution is

$$
y=\frac{2}{8 x - 3}.
$$

Author domain: x>3/8; y>0; connected interval containing initial x=1/2

### Generated moderate — reciprocal_initial (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+5 y^{2}=0$ that satisfies $y(3)=3.$

- $y=45 x - 132$
- $y=\frac{3}{15 x - 44}$
- $y=\frac{3}{- 15 x + 46}$
- $y=\frac{3}{5 x - 14}$
- $y=\frac{1}{5 x - 12}$

Correct: $y=\frac{3}{15 x - 44}$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 5 y^{2} \\ -\frac{1}{y^2}\,\text{d}y & =5\,\text{d}x \\ -\int\frac{1}{y^2}\,\text{d}y & =\int 5\,\text{d}x \\ \frac{1}{y} & =5 x - 15+C \\ y & =\frac{1}{5 x - 15+C}\end{aligned}
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(3)=3$ to find $C:$

$$
\begin{aligned}3 & =\frac{1}{C} \\ C & =\frac{1}{3}\end{aligned}
$$

Thus, the particular solution is

$$
y=\frac{3}{15 x - 44}.
$$

Author domain: x>44/15; y>0; connected interval containing initial x=3

### Generated hard — trig_frequencies (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{\sin{\left(3 x \right)}}{\cos{\left(2 y \right)}}$ that satisfies $y(0)=0.$ Assume that $-\frac{\pi}{4}<y<\frac{\pi}{4}.$

- $3 \sin{\left(2 y \right)}=2 \cos{\left(3 x \right)}$
- $3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x \right)} + 2$
- $3 \sin{\left(2 y \right)}=- \cos{\left(3 x \right)} + 1$
- $3 \sin{\left(2 y \right)}=- 3 \cos{\left(3 x \right)} + 3$
- $3 \sin{\left(2 y \right)}=2 \cos{\left(3 x \right)} + 2$

Correct: $3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x \right)} + 2$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sin{\left(3 x \right)}}{\cos{\left(2 y \right)}} \\ \cos{\left(2 y \right)}\frac{\text{d}y}{\text{d}x} & =\sin{\left(3 x \right)} \\ \int \cos{\left(2 y \right)}\,\text{d}y & =\int \sin{\left(3 x \right)}\,\text{d}x \\ \frac{\sin{\left(2 y \right)}}{2} & =- \frac{\cos{\left(3 x \right)}}{3}+C \\ \sin{\left(2 y \right)} & =- \frac{2 \cos{\left(3 x \right)}}{3}+C_1\end{aligned}
$$

where $C_1=2C.$

We now apply the condition $y(0)=0$ to find $C_1:$

$$
\begin{aligned}0 & =- \frac{2}{3}+C_1 \\ C_1 & =\frac{2}{3}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
3 \sin{\left(2 y \right)}=- 2 \cos{\left(3 x \right)} + 2.
$$

Author domain: -pi/4<y<pi/4; abs(2/3*(1-cos(3*(x-(0)))))<1; connected interval containing x=0; cos(2*y)!=0

### Generated hard — trig_frequencies (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{\sin{\left(4 x + 8 \right)}}{\cos{\left(3 y \right)}}$ that satisfies $y(-2)=0.$ Assume that $-\frac{\pi}{6}<y<\frac{\pi}{6}.$

- $4 \sin{\left(3 y \right)}=3 \cos{\left(4 x + 8 \right)}$
- $4 \sin{\left(3 y \right)}=- 3 \cos{\left(4 x + 8 \right)} + 3$
- $4 \sin{\left(3 y \right)}=- \cos{\left(4 x + 8 \right)} + 1$
- $4 \sin{\left(3 y \right)}=- 4 \cos{\left(4 x + 8 \right)} + 4$
- $4 \sin{\left(3 y \right)}=3 \cos{\left(4 x + 8 \right)} + 3$

Correct: $4 \sin{\left(3 y \right)}=- 3 \cos{\left(4 x + 8 \right)} + 3$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sin{\left(4 x + 8 \right)}}{\cos{\left(3 y \right)}} \\ \cos{\left(3 y \right)}\frac{\text{d}y}{\text{d}x} & =\sin{\left(4 x + 8 \right)} \\ \int \cos{\left(3 y \right)}\,\text{d}y & =\int \sin{\left(4 x + 8 \right)}\,\text{d}x \\ \frac{\sin{\left(3 y \right)}}{3} & =- \frac{\cos{\left(4 x + 8 \right)}}{4}+C \\ \sin{\left(3 y \right)} & =- \frac{3 \cos{\left(4 x + 8 \right)}}{4}+C_1\end{aligned}
$$

where $C_1=3C.$

We now apply the condition $y(-2)=0$ to find $C_1:$

$$
\begin{aligned}0 & =- \frac{3}{4}+C_1 \\ C_1 & =\frac{3}{4}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
4 \sin{\left(3 y \right)}=- 3 \cos{\left(4 x + 8 \right)} + 3.
$$

Author domain: -pi/6<y<pi/6; abs(3/4*(1-cos(4*(x-(-2)))))<1; connected interval containing x=-2; cos(3*y)!=0

### Generated hard — trig_frequencies (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{\sin{\left(2 x - 1 \right)}}{\cos{\left(4 y \right)}}$ that satisfies $y(\frac{1}{2})=0.$ Assume that $-\frac{\pi}{8}<y<\frac{\pi}{8}.$

- $2 \sin{\left(4 y \right)}=4 \cos{\left(2 x - 1 \right)}$
- $2 \sin{\left(4 y \right)}=- 4 \cos{\left(2 x - 1 \right)} + 4$
- $2 \sin{\left(4 y \right)}=- \cos{\left(2 x - 1 \right)} + 1$
- $2 \sin{\left(4 y \right)}=- 2 \cos{\left(2 x - 1 \right)} + 2$
- $2 \sin{\left(4 y \right)}=4 \cos{\left(2 x - 1 \right)} + 4$

Correct: $2 \sin{\left(4 y \right)}=- 4 \cos{\left(2 x - 1 \right)} + 4$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sin{\left(2 x - 1 \right)}}{\cos{\left(4 y \right)}} \\ \cos{\left(4 y \right)}\frac{\text{d}y}{\text{d}x} & =\sin{\left(2 x - 1 \right)} \\ \int \cos{\left(4 y \right)}\,\text{d}y & =\int \sin{\left(2 x - 1 \right)}\,\text{d}x \\ \frac{\sin{\left(4 y \right)}}{4} & =- \frac{\cos{\left(2 x - 1 \right)}}{2}+C \\ \sin{\left(4 y \right)} & =- 2 \cos{\left(2 x - 1 \right)}+C_1\end{aligned}
$$

where $C_1=4C.$

We now apply the condition $y(\frac{1}{2})=0$ to find $C_1:$

$$
\begin{aligned}0 & =-2+C_1 \\ C_1 & =2\end{aligned}
$$

So we get the particular solution in implicit form:

$$
2 \sin{\left(4 y \right)}=- 4 \cos{\left(2 x - 1 \right)} + 4.
$$

Author domain: -pi/8<y<pi/8; abs(4/2*(1-cos(2*(x-(1/2)))))<1; connected interval containing x=1/2; cos(4*y)!=0

### Generated hard — trig_frequencies (authored)

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{\sin{\left(3 x - 9 \right)}}{\cos{\left(5 y \right)}}$ that satisfies $y(3)=0.$ Assume that $-\frac{\pi}{10}<y<\frac{\pi}{10}.$

- $3 \sin{\left(5 y \right)}=5 \cos{\left(3 x - 9 \right)}$
- $3 \sin{\left(5 y \right)}=- 5 \cos{\left(3 x - 9 \right)} + 5$
- $3 \sin{\left(5 y \right)}=- \cos{\left(3 x - 9 \right)} + 1$
- $3 \sin{\left(5 y \right)}=- 3 \cos{\left(3 x - 9 \right)} + 3$
- $3 \sin{\left(5 y \right)}=5 \cos{\left(3 x - 9 \right)} + 5$

Correct: $3 \sin{\left(5 y \right)}=- 5 \cos{\left(3 x - 9 \right)} + 5$

Worked solution:
We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sin{\left(3 x - 9 \right)}}{\cos{\left(5 y \right)}} \\ \cos{\left(5 y \right)}\frac{\text{d}y}{\text{d}x} & =\sin{\left(3 x - 9 \right)} \\ \int \cos{\left(5 y \right)}\,\text{d}y & =\int \sin{\left(3 x - 9 \right)}\,\text{d}x \\ \frac{\sin{\left(5 y \right)}}{5} & =- \frac{\cos{\left(3 x - 9 \right)}}{3}+C \\ \sin{\left(5 y \right)} & =- \frac{5 \cos{\left(3 x - 9 \right)}}{3}+C_1\end{aligned}
$$

where $C_1=5C.$

We now apply the condition $y(3)=0$ to find $C_1:$

$$
\begin{aligned}0 & =- \frac{5}{3}+C_1 \\ C_1 & =\frac{5}{3}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
3 \sin{\left(5 y \right)}=- 5 \cos{\left(3 x - 9 \right)} + 5.
$$

Author domain: -pi/10<y<pi/10; abs(5/3*(1-cos(3*(x-(3)))))<1; connected interval containing x=3; cos(5*y)!=0
