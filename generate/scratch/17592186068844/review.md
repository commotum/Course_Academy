# Implicit general solutions review

Original and translated observed profiles retain complete evidence banks. Standard variants use authored whole banks. Moderate/hard are explicitly authored levels.

## Original replay — exp_linear

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{e}^{y}}.$

- $2{e}^{y}={x}^{2}+C$
- ${e}^{y}={x}^{2}+C$
- $\frac{3}{2}{e}^{2y}=x+C$
- $4{e}^{y}={x}^{3}+C$
- $\frac{1}{2}{e}^{2y}=2x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2x}{{e}^{y}} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & =2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int {e}^{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2x\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int 2x\,\text{d}x \\ {e}^{y} & ={x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{y}={x}^{2}+C.
$$

## Generated standard variant — exp_linear

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{e}^{\left(y-1\right)}}.$

- $e^{y - 1}=x^{2}+C$
- $e^{y - 1}=2 x^{2}+C$
- $\frac{e^{2 y - 2}}{2}=x^{2}+C$
- $e^{y - 1}=2 x+C$
- $e^{y - 1}=- x^{2}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2x}{{e}^{\left(y-1\right)}} \\ {e}^{\left(y-1\right)}\,\frac{\text{d}y}{\text{d}x} & =2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{\left(y-1\right)}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int {e}^{\left(y-1\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2x\,\text{d}x \\ \int {e}^{\left(y-1\right)}\,\text{d}y & =\int 2x\,\text{d}x \\ {e}^{\left(y-1\right)} & ={x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{\left(y-1\right)}={x}^{2}+C.
$$

## Generated standard variant — exp_linear

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{2\left(x-4\right)}{{e}^{\left(y+5\right)}}.$

- $\frac{e^{2 y + 10}}{2}=\left(x - 4\right)^{2}+C$
- $e^{y + 5}=2 \left(x - 4\right)^{2}+C$
- $e^{y + 5}=2 x - 8+C$
- $e^{y + 5}=\left(x - 4\right)^{2}+C$
- $e^{y + 5}=- \left(x - 4\right)^{2}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2\left(x-4\right)}{{e}^{\left(y+5\right)}} \\ {e}^{\left(y+5\right)}\,\frac{\text{d}y}{\text{d}x} & =2\left(x-4\right)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{\left(y+5\right)}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\left(x-4\right)\,\text{d}x \\ \int {e}^{\left(y+5\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2\left(x-4\right)\,\text{d}x \\ \int {e}^{\left(y+5\right)}\,\text{d}y & =\int 2\left(x-4\right)\,\text{d}x \\ {e}^{\left(y+5\right)} & ={\left(x-4\right)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{\left(y+5\right)}={\left(x-4\right)}^{2}+C.
$$

## Generated observed-bank variant — exp_linear

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2\left(x-2\right)}{{e}^{\left(y+3\right)}}.$

- $\frac{1}{2}{e}^{2\left(y+3\right)}=2\left(x-2\right)+C$
- $2{e}^{\left(y+3\right)}={\left(x-2\right)}^{2}+C$
- $4{e}^{\left(y+3\right)}={\left(x-2\right)}^{3}+C$
- $\frac{3}{2}{e}^{2\left(y+3\right)}=\left(x-2\right)+C$
- ${e}^{\left(y+3\right)}={\left(x-2\right)}^{2}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2\left(x-2\right)}{{e}^{\left(y+3\right)}} \\ {e}^{\left(y+3\right)}\,\frac{\text{d}y}{\text{d}x} & =2\left(x-2\right)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{\left(y+3\right)}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\left(x-2\right)\,\text{d}x \\ \int {e}^{\left(y+3\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2\left(x-2\right)\,\text{d}x \\ \int {e}^{\left(y+3\right)}\,\text{d}y & =\int 2\left(x-2\right)\,\text{d}x \\ {e}^{\left(y+3\right)} & ={\left(x-2\right)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{\left(y+3\right)}={\left(x-2\right)}^{2}+C.
$$

## Original replay — arcsin_autonomous

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\sqrt{1-{y}^{2}}\,$ for $\,|y|<1.$

- $\operatorname{arcsin}⁡y=x+C$
- $\operatorname{sin}⁡y=x+C$
- $\operatorname{arccos}⁡y=x+C$
- $\operatorname{tan}⁡y=x+C$
- $\operatorname{arctan}⁡y=x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\sqrt{1-{y}^{2}} \\ \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{y}^{2}}}\,\text{d}y & =\int \text{d}x \\ \operatorname{arcsin}⁡y & =x+C.\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arcsin}⁡y=x+C.
$$

## Generated standard variant — arcsin_autonomous

{"h": 0, "k": 0}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\sqrt{1-{y}^{2}}\,$ for $\,|y|<1.$

- $\arctan{\left(y \right)}=x+C$
- $\sin{\left(y \right)}=x+C$
- $\arcsin{\left(y \right)}=x+C$
- $\arcsin{\left(y \right)}=- x+C$
- $\arcsin{\left(y \right)}=2 x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\sqrt{1-{y}^{2}} \\ \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{y}^{2}}}\,\text{d}y & =\int \text{d}x \\ \operatorname{arcsin}⁡y & =x+C.\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arcsin}⁡y=x+C.
$$

## Generated standard variant — arcsin_autonomous

{"h": 0, "k": -4}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\sqrt{1-{\left(y-4\right)}^{2}}\,$ for $\,|\left(y-4\right)|<1.$

- $\sin{\left(y - 4 \right)}=x+C$
- $\arcsin{\left(y - 4 \right)}=2 x+C$
- $\arctan{\left(y - 4 \right)}=x+C$
- $\arcsin{\left(y - 4 \right)}=x+C$
- $\arcsin{\left(y - 4 \right)}=- x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\sqrt{1-{\left(y-4\right)}^{2}} \\ \frac{1}{\sqrt{1-{\left(y-4\right)}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{1-{\left(y-4\right)}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{\left(y-4\right)}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{\left(y-4\right)}^{2}}}\,\text{d}y & =\int \text{d}x \\ \operatorname{arcsin}⁡\left(y-4\right) & =x+C.\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arcsin}⁡\left(y-4\right)=x+C.
$$

## Generated observed-bank variant — arcsin_autonomous

{"h": 0, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\sqrt{1-{\left(y+3\right)}^{2}}\,$ for $\,|\left(y+3\right)|<1.$

- $\operatorname{arctan}⁡\left(y+3\right)=x+C$
- $\operatorname{arcsin}⁡\left(y+3\right)=x+C$
- $\operatorname{tan}⁡\left(y+3\right)=x+C$
- $\operatorname{arccos}⁡\left(y+3\right)=x+C$
- $\operatorname{sin}⁡\left(y+3\right)=x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\sqrt{1-{\left(y+3\right)}^{2}} \\ \frac{1}{\sqrt{1-{\left(y+3\right)}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{1-{\left(y+3\right)}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{\left(y+3\right)}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{\left(y+3\right)}^{2}}}\,\text{d}y & =\int \text{d}x \\ \operatorname{arcsin}⁡\left(y+3\right) & =x+C.\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arcsin}⁡\left(y+3\right)=x+C.
$$

## Original replay — tan_exp

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{x}{cos}^{2}⁡y$ for $0<y<\frac{\pi }{2}.$

- $\operatorname{tan}⁡y={e}^{2x}+C$
- $2\operatorname{tan}⁡y={e}^{x}+C$
- $\operatorname{tan}⁡y=2{e}^{x}+C$
- $\operatorname{tan}⁡y={e}^{x}+C$
- $2\operatorname{tan}⁡y={e}^{2x}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{x}{cos}^{2}⁡y \\ \frac{1}{{cos}^{2}⁡y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{x} \\ {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x} & ={e}^{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{x}\,\text{d}x \\ \int {sec}^{2}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{x}\,\text{d}x \\ \int {sec}^{2}⁡y\,\text{d}y & =\int {e}^{x}\,\text{d}x \\ \operatorname{tan}⁡y & ={e}^{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡y={e}^{x}+C.
$$

## Generated standard variant — tan_exp

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}={e}^{x}{cos}^{2}⁡\left(y-1\right)$ for $0<\left(y-1\right)<\frac{\pi }{2}.$

- $\tan{\left(y - 1 \right)}=e^{x}+C$
- $\tan{\left(y - 1 \right)}=2 e^{x}+C$
- $y - 1=e^{x}+C$
- $\sec^{2}{\left(y - 1 \right)}=e^{x}+C$
- $\tan{\left(y - 1 \right)}=- e^{x}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{x}{cos}^{2}⁡\left(y-1\right) \\ \frac{1}{{cos}^{2}⁡\left(y-1\right)}\,\frac{\text{d}y}{\text{d}x} & ={e}^{x} \\ {sec}^{2}⁡\left(y-1\right)\,\frac{\text{d}y}{\text{d}x} & ={e}^{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡\left(y-1\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{x}\,\text{d}x \\ \int {sec}^{2}⁡\left(y-1\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{x}\,\text{d}x \\ \int {sec}^{2}⁡\left(y-1\right)\,\text{d}y & =\int {e}^{x}\,\text{d}x \\ \operatorname{tan}⁡\left(y-1\right) & ={e}^{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡\left(y-1\right)={e}^{x}+C.
$$

## Generated standard variant — tan_exp

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}={e}^{\left(x-4\right)}{cos}^{2}⁡\left(y+5\right)$ for $0<\left(y+5\right)<\frac{\pi }{2}.$

- $y + 5=e^{x - 4}+C$
- $\tan{\left(y + 5 \right)}=2 e^{x - 4}+C$
- $\sec^{2}{\left(y + 5 \right)}=e^{x - 4}+C$
- $\tan{\left(y + 5 \right)}=e^{x - 4}+C$
- $\tan{\left(y + 5 \right)}=- e^{x - 4}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{\left(x-4\right)}{cos}^{2}⁡\left(y+5\right) \\ \frac{1}{{cos}^{2}⁡\left(y+5\right)}\,\frac{\text{d}y}{\text{d}x} & ={e}^{\left(x-4\right)} \\ {sec}^{2}⁡\left(y+5\right)\,\frac{\text{d}y}{\text{d}x} & ={e}^{\left(x-4\right)}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡\left(y+5\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{\left(x-4\right)}\,\text{d}x \\ \int {sec}^{2}⁡\left(y+5\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{\left(x-4\right)}\,\text{d}x \\ \int {sec}^{2}⁡\left(y+5\right)\,\text{d}y & =\int {e}^{\left(x-4\right)}\,\text{d}x \\ \operatorname{tan}⁡\left(y+5\right) & ={e}^{\left(x-4\right)}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡\left(y+5\right)={e}^{\left(x-4\right)}+C.
$$

## Generated observed-bank variant — tan_exp

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{\left(x-2\right)}{cos}^{2}⁡\left(y+3\right)$ for $0<\left(y+3\right)<\frac{\pi }{2}.$

- $2\operatorname{tan}⁡\left(y+3\right)={e}^{2\left(x-2\right)}+C$
- $\operatorname{tan}⁡\left(y+3\right)={e}^{2\left(x-2\right)}+C$
- $\operatorname{tan}⁡\left(y+3\right)={e}^{\left(x-2\right)}+C$
- $\operatorname{tan}⁡\left(y+3\right)=2{e}^{\left(x-2\right)}+C$
- $2\operatorname{tan}⁡\left(y+3\right)={e}^{\left(x-2\right)}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{\left(x-2\right)}{cos}^{2}⁡\left(y+3\right) \\ \frac{1}{{cos}^{2}⁡\left(y+3\right)}\,\frac{\text{d}y}{\text{d}x} & ={e}^{\left(x-2\right)} \\ {sec}^{2}⁡\left(y+3\right)\,\frac{\text{d}y}{\text{d}x} & ={e}^{\left(x-2\right)}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡\left(y+3\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{\left(x-2\right)}\,\text{d}x \\ \int {sec}^{2}⁡\left(y+3\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{\left(x-2\right)}\,\text{d}x \\ \int {sec}^{2}⁡\left(y+3\right)\,\text{d}y & =\int {e}^{\left(x-2\right)}\,\text{d}x \\ \operatorname{tan}⁡\left(y+3\right) & ={e}^{\left(x-2\right)}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡\left(y+3\right)={e}^{\left(x-2\right)}+C.
$$

## Original replay — log_exp

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y{e}^{x}$ for $y\ne 0.$

- $\operatorname{ln}⁡|y|={e}^{x}+C$
- ${e}^{y}=\operatorname{ln}⁡|x|+C$
- $y={e}^{\sqrt{x}}+C$
- $y={e}^{x}+C$
- $\operatorname{ln}⁡|y|={e}^{\sqrt{x}}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y{e}^{x} \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & ={e}^{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{x}\,\text{d}x \\ \int \frac{1}{y}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{x}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {e}^{x}\,\text{d}x \\ \operatorname{ln}⁡|y| & ={e}^{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={e}^{x}+C
$$

## Generated standard variant — log_exp

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\left(y-1\right){e}^{x}$ for $\left(y-1\right)\ne 0.$

- $\ln{\left(\left|{y - 1}\right| \right)}=e^{x}+C$
- $\ln{\left(\left|{y - 1}\right| \right)}=2 e^{x}+C$
- $y - 1=e^{x}+C$
- $e^{y - 1}=e^{x}+C$
- $\ln{\left(\left|{y - 1}\right| \right)}=- e^{x}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(y-1\right){e}^{x} \\ \frac{1}{\left(y-1\right)}\cdot \frac{\text{d}y}{\text{d}x} & ={e}^{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\left(y-1\right)}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{x}\,\text{d}x \\ \int \frac{1}{\left(y-1\right)}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{x}\,\text{d}x \\ \int \frac{1}{\left(y-1\right)}\,\text{d}y & =\int {e}^{x}\,\text{d}x \\ \operatorname{ln}⁡|\left(y-1\right)| & ={e}^{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|\left(y-1\right)|={e}^{x}+C
$$

## Generated standard variant — log_exp

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\left(y+5\right){e}^{\left(x-4\right)}$ for $\left(y+5\right)\ne 0.$

- $y + 5=e^{x - 4}+C$
- $\ln{\left(\left|{y + 5}\right| \right)}=2 e^{x - 4}+C$
- $e^{y + 5}=e^{x - 4}+C$
- $\ln{\left(\left|{y + 5}\right| \right)}=e^{x - 4}+C$
- $\ln{\left(\left|{y + 5}\right| \right)}=- e^{x - 4}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(y+5\right){e}^{\left(x-4\right)} \\ \frac{1}{\left(y+5\right)}\cdot \frac{\text{d}y}{\text{d}x} & ={e}^{\left(x-4\right)}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\left(y+5\right)}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{\left(x-4\right)}\,\text{d}x \\ \int \frac{1}{\left(y+5\right)}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{\left(x-4\right)}\,\text{d}x \\ \int \frac{1}{\left(y+5\right)}\,\text{d}y & =\int {e}^{\left(x-4\right)}\,\text{d}x \\ \operatorname{ln}⁡|\left(y+5\right)| & ={e}^{\left(x-4\right)}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|\left(y+5\right)|={e}^{\left(x-4\right)}+C
$$

## Generated observed-bank variant — log_exp

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\left(y+3\right){e}^{\left(x-2\right)}$ for $\left(y+3\right)\ne 0.$

- $\operatorname{ln}⁡|\left(y+3\right)|={e}^{\sqrt{\left(x-2\right)}}+C$
- $\operatorname{ln}⁡|\left(y+3\right)|={e}^{\left(x-2\right)}+C$
- $\left(y+3\right)={e}^{\left(x-2\right)}+C$
- $\left(y+3\right)={e}^{\sqrt{\left(x-2\right)}}+C$
- ${e}^{\left(y+3\right)}=\operatorname{ln}⁡|\left(x-2\right)|+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(y+3\right){e}^{\left(x-2\right)} \\ \frac{1}{\left(y+3\right)}\cdot \frac{\text{d}y}{\text{d}x} & ={e}^{\left(x-2\right)}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\left(y+3\right)}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{\left(x-2\right)}\,\text{d}x \\ \int \frac{1}{\left(y+3\right)}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{\left(x-2\right)}\,\text{d}x \\ \int \frac{1}{\left(y+3\right)}\,\text{d}y & =\int {e}^{\left(x-2\right)}\,\text{d}x \\ \operatorname{ln}⁡|\left(y+3\right)| & ={e}^{\left(x-2\right)}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|\left(y+3\right)|={e}^{\left(x-2\right)}+C
$$

## Original replay — tan_autonomous

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{{sec}^{2}⁡y}$ for $-\frac{\pi }{2}<y<\frac{\pi }{2}.$

- $y=\operatorname{tan}⁡x+C$
- $\operatorname{sin}⁡y=x+C$
- $\operatorname{sin}⁡y=\sqrt{x}+C$
- $\operatorname{tan}⁡y=x+C$
- $\operatorname{tan}⁡y=\sqrt{x}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{sec}^{2}⁡y} \\ {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡y\,\text{d}y & =\int 1\,\text{d}x \\ \operatorname{tan}⁡y & =x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡y=x+C.
$$

## Generated standard variant — tan_autonomous

{"h": 0, "k": 0}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{1}{{sec}^{2}⁡y}$ for $-\frac{\pi }{2}<y<\frac{\pi }{2}.$

- $\sec^{2}{\left(y \right)}=x+C$
- $y=x+C$
- $\tan{\left(y \right)}=x+C$
- $\tan{\left(y \right)}=- x+C$
- $\tan{\left(y \right)}=2 x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{sec}^{2}⁡y} \\ {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡y\,\text{d}y & =\int 1\,\text{d}x \\ \operatorname{tan}⁡y & =x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡y=x+C.
$$

## Generated standard variant — tan_autonomous

{"h": 0, "k": -4}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{1}{{sec}^{2}⁡\left(y-4\right)}$ for $-\frac{\pi }{2}<\left(y-4\right)<\frac{\pi }{2}.$

- $y - 4=x+C$
- $\tan{\left(y - 4 \right)}=2 x+C$
- $\sec^{2}{\left(y - 4 \right)}=x+C$
- $\tan{\left(y - 4 \right)}=x+C$
- $\tan{\left(y - 4 \right)}=- x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{sec}^{2}⁡\left(y-4\right)} \\ {sec}^{2}⁡\left(y-4\right)\,\frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡\left(y-4\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡\left(y-4\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡\left(y-4\right)\,\text{d}y & =\int 1\,\text{d}x \\ \operatorname{tan}⁡\left(y-4\right) & =x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡\left(y-4\right)=x+C.
$$

## Generated observed-bank variant — tan_autonomous

{"h": 0, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{{sec}^{2}⁡\left(y+3\right)}$ for $-\frac{\pi }{2}<\left(y+3\right)<\frac{\pi }{2}.$

- $\operatorname{tan}⁡\left(y+3\right)=\sqrt{x}+C$
- $\left(y+3\right)=\operatorname{tan}⁡x+C$
- $\operatorname{tan}⁡\left(y+3\right)=x+C$
- $\operatorname{sin}⁡\left(y+3\right)=\sqrt{x}+C$
- $\operatorname{sin}⁡\left(y+3\right)=x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{sec}^{2}⁡\left(y+3\right)} \\ {sec}^{2}⁡\left(y+3\right)\,\frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡\left(y+3\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡\left(y+3\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡\left(y+3\right)\,\text{d}y & =\int 1\,\text{d}x \\ \operatorname{tan}⁡\left(y+3\right) & =x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡\left(y+3\right)=x+C.
$$

## Original replay — power_cube

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}}{{y}^{2}}.$

- ${y}^{3}=x+C$
- ${y}^{2}={x}^{3}+C$
- ${y}^{2}={x}^{2}+C$
- $y={x}^{3}+C$
- ${y}^{3}={x}^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{x}^{2}}{{y}^{2}} \\ {y}^{2}\frac{\text{d}y}{\text{d}x} & ={x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int {y}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {x}^{2}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ \frac{{y}^{3}}{3} & =\frac{{x}^{3}}{3}+K \\ {y}^{3} & ={x}^{3}+C,\end{aligned}
$$

where $C=3K.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{3}={x}^{3}+C.
$$

## Generated standard variant — power_cube

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}}{{\left(y-1\right)}^{2}}.$

- $\left(y - 1\right)^{3}=x^{3}+C$
- $\left(y - 1\right)^{3}=2 x^{3}+C$
- $\left(y - 1\right)^{2}=x^{3}+C$
- $\left(y - 1\right)^{3}=x^{2}+C$
- $\left(y - 1\right)^{3}=- x^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{x}^{2}}{{\left(y-1\right)}^{2}} \\ {\left(y-1\right)}^{2}\frac{\text{d}y}{\text{d}x} & ={x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {\left(y-1\right)}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int {\left(y-1\right)}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {x}^{2}\,\text{d}x \\ \int {\left(y-1\right)}^{2}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ \frac{{\left(y-1\right)}^{3}}{3} & =\frac{{x}^{3}}{3}+K \\ {\left(y-1\right)}^{3} & ={x}^{3}+C,\end{aligned}
$$

where $C=3K.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{\left(y-1\right)}^{3}={x}^{3}+C.
$$

## Generated standard variant — power_cube

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{{\left(x-4\right)}^{2}}{{\left(y+5\right)}^{2}}.$

- $\left(y + 5\right)^{2}=\left(x - 4\right)^{3}+C$
- $\left(y + 5\right)^{3}=2 \left(x - 4\right)^{3}+C$
- $\left(y + 5\right)^{3}=\left(x - 4\right)^{2}+C$
- $\left(y + 5\right)^{3}=\left(x - 4\right)^{3}+C$
- $\left(y + 5\right)^{3}=- \left(x - 4\right)^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{\left(x-4\right)}^{2}}{{\left(y+5\right)}^{2}} \\ {\left(y+5\right)}^{2}\frac{\text{d}y}{\text{d}x} & ={\left(x-4\right)}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {\left(y+5\right)}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {\left(x-4\right)}^{2}\,\text{d}x \\ \int {\left(y+5\right)}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {\left(x-4\right)}^{2}\,\text{d}x \\ \int {\left(y+5\right)}^{2}\,\text{d}y & =\int {\left(x-4\right)}^{2}\,\text{d}x \\ \frac{{\left(y+5\right)}^{3}}{3} & =\frac{{\left(x-4\right)}^{3}}{3}+K \\ {\left(y+5\right)}^{3} & ={\left(x-4\right)}^{3}+C,\end{aligned}
$$

where $C=3K.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{\left(y+5\right)}^{3}={\left(x-4\right)}^{3}+C.
$$

## Generated observed-bank variant — power_cube

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{\left(x-2\right)}^{2}}{{\left(y+3\right)}^{2}}.$

- ${\left(y+3\right)}^{3}={\left(x-2\right)}^{3}+C$
- ${\left(y+3\right)}^{3}=\left(x-2\right)+C$
- $\left(y+3\right)={\left(x-2\right)}^{3}+C$
- ${\left(y+3\right)}^{2}={\left(x-2\right)}^{2}+C$
- ${\left(y+3\right)}^{2}={\left(x-2\right)}^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{\left(x-2\right)}^{2}}{{\left(y+3\right)}^{2}} \\ {\left(y+3\right)}^{2}\frac{\text{d}y}{\text{d}x} & ={\left(x-2\right)}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {\left(y+3\right)}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {\left(x-2\right)}^{2}\,\text{d}x \\ \int {\left(y+3\right)}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {\left(x-2\right)}^{2}\,\text{d}x \\ \int {\left(y+3\right)}^{2}\,\text{d}y & =\int {\left(x-2\right)}^{2}\,\text{d}x \\ \frac{{\left(y+3\right)}^{3}}{3} & =\frac{{\left(x-2\right)}^{3}}{3}+K \\ {\left(y+3\right)}^{3} & ={\left(x-2\right)}^{3}+C,\end{aligned}
$$

where $C=3K.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{\left(y+3\right)}^{3}={\left(x-2\right)}^{3}+C.
$$

## Original replay — exp_affine

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=2{e}^{-y}(x-1).$

- ${e}^{y}={x}^{2}-2x+C$
- $y={x}^{2}-2x+C$
- ${e}^{2y}={x}^{2}-2x+C$
- $2y=\frac{1}{2}\,{x}^{2}-x+C$
- ${e}^{2y}=\frac{1}{2}\,{x}^{2}-x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2{e}^{-y}(x-1) \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & =2(x-1)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\text{d}x & =\int 2(x-1)\,\text{d}x \\ \int {e}^{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2x\,\text{d}x-\int 2\,\text{d}x \\ {e}^{y} & ={x}^{2}-2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{y}={x}^{2}-2x+C.
$$

## Generated standard variant — exp_affine

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=2{e}^{-\left(y-1\right)}(x-1).$

- $e^{y - 1}=x^{2} - 2 x+C$
- $e^{y - 1}=2 x^{2} - 4 x+C$
- $\frac{e^{2 y - 2}}{2}=x^{2} - 2 x+C$
- $e^{y - 1}=2 x - 2+C$
- $e^{y - 1}=- x^{2} + 2 x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2{e}^{-\left(y-1\right)}(x-1) \\ {e}^{\left(y-1\right)}\,\frac{\text{d}y}{\text{d}x} & =2(x-1)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{\left(y-1\right)}\,\frac{\text{d}y}{\text{d}x}\text{d}x & =\int 2(x-1)\,\text{d}x \\ \int {e}^{\left(y-1\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2x\,\text{d}x-\int 2\,\text{d}x \\ {e}^{\left(y-1\right)} & ={x}^{2}-2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{\left(y-1\right)}={x}^{2}-2x+C.
$$

## Generated standard variant — exp_affine

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=2{e}^{-\left(y+5\right)}(\left(x-4\right)-1).$

- $\frac{e^{2 y + 10}}{2}=- 2 x + \left(x - 4\right)^{2} + 8+C$
- $e^{y + 5}=- 4 x + 2 \left(x - 4\right)^{2} + 16+C$
- $e^{y + 5}=2 x - 10+C$
- $e^{y + 5}=- 2 x + \left(x - 4\right)^{2} + 8+C$
- $e^{y + 5}=2 x - \left(x - 4\right)^{2} - 8+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2{e}^{-\left(y+5\right)}(\left(x-4\right)-1) \\ {e}^{\left(y+5\right)}\,\frac{\text{d}y}{\text{d}x} & =2(\left(x-4\right)-1)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{\left(y+5\right)}\,\frac{\text{d}y}{\text{d}x}\text{d}x & =\int 2(\left(x-4\right)-1)\,\text{d}x \\ \int {e}^{\left(y+5\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2\left(x-4\right)\,\text{d}x-\int 2\,\text{d}x \\ {e}^{\left(y+5\right)} & ={\left(x-4\right)}^{2}-2\left(x-4\right)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{\left(y+5\right)}={\left(x-4\right)}^{2}-2\left(x-4\right)+C.
$$

## Generated observed-bank variant — exp_affine

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=2{e}^{-\left(y+3\right)}(\left(x-2\right)-1).$

- ${e}^{2\left(y+3\right)}=\frac{1}{2}\,{\left(x-2\right)}^{2}-\left(x-2\right)+C$
- ${e}^{\left(y+3\right)}={\left(x-2\right)}^{2}-2\left(x-2\right)+C$
- $2\left(y+3\right)=\frac{1}{2}\,{\left(x-2\right)}^{2}-\left(x-2\right)+C$
- ${e}^{2\left(y+3\right)}={\left(x-2\right)}^{2}-2\left(x-2\right)+C$
- $\left(y+3\right)={\left(x-2\right)}^{2}-2\left(x-2\right)+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2{e}^{-\left(y+3\right)}(\left(x-2\right)-1) \\ {e}^{\left(y+3\right)}\,\frac{\text{d}y}{\text{d}x} & =2(\left(x-2\right)-1)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{\left(y+3\right)}\,\frac{\text{d}y}{\text{d}x}\text{d}x & =\int 2(\left(x-2\right)-1)\,\text{d}x \\ \int {e}^{\left(y+3\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2\left(x-2\right)\,\text{d}x-\int 2\,\text{d}x \\ {e}^{\left(y+3\right)} & ={\left(x-2\right)}^{2}-2\left(x-2\right)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{\left(y+3\right)}={\left(x-2\right)}^{2}-2\left(x-2\right)+C.
$$

## Original replay — root_power

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{\sqrt{x}}{\sqrt{y}}.$

- $\sqrt{{y}^{3}}=x+C$
- $y={x}^{2}+C$
- $y=\sqrt{{x}^{3}}+C$
- ${y}^{3}=\sqrt{x}+C$
- $\sqrt{{y}^{3}}=\sqrt{{x}^{3}}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sqrt{x}}{\sqrt{y}} \\ \sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \sqrt{x}\,\text{d}x \\ \int \sqrt{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \sqrt{x}\,\text{d}x \\ \int {y}^{1/2}\,\text{d}y & =\int {x}^{1/2}\,\text{d}x \\ \frac{2{y}^{3/2}}{3} & =\frac{2{x}^{3/2}}{3}+K \\ {y}^{3/2} & ={x}^{3/2}+C \\ \sqrt{{y}^{3}} & =\sqrt{{x}^{3}}+C,\end{aligned}
$$

where $C=\frac{3K}{2}.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\sqrt{{y}^{3}}=\sqrt{{x}^{3}}+C.
$$

## Generated standard variant — root_power

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{\sqrt{x}}{\sqrt{\left(y-1\right)}}.$

- $\left(y - 1\right)^{\frac{3}{2}}=x^{\frac{3}{2}}+C$
- $\left(y - 1\right)^{\frac{3}{2}}=2 x^{\frac{3}{2}}+C$
- $\sqrt{y - 1}=x^{\frac{3}{2}}+C$
- $\left(y - 1\right)^{\frac{3}{2}}=\sqrt{x}+C$
- $\left(y - 1\right)^{\frac{3}{2}}=- x^{\frac{3}{2}}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sqrt{x}}{\sqrt{\left(y-1\right)}} \\ \sqrt{\left(y-1\right)}\,\frac{\text{d}y}{\text{d}x} & =\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{\left(y-1\right)}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \sqrt{x}\,\text{d}x \\ \int \sqrt{\left(y-1\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \sqrt{x}\,\text{d}x \\ \int {\left(y-1\right)}^{1/2}\,\text{d}y & =\int {x}^{1/2}\,\text{d}x \\ \frac{2{\left(y-1\right)}^{3/2}}{3} & =\frac{2{x}^{3/2}}{3}+K \\ {\left(y-1\right)}^{3/2} & ={x}^{3/2}+C \\ \sqrt{{\left(y-1\right)}^{3}} & =\sqrt{{x}^{3}}+C,\end{aligned}
$$

where $C=\frac{3K}{2}.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\sqrt{{\left(y-1\right)}^{3}}=\sqrt{{x}^{3}}+C.
$$

## Generated standard variant — root_power

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{\sqrt{\left(x-4\right)}}{\sqrt{\left(y+5\right)}}.$

- $\sqrt{y + 5}=\left(x - 4\right)^{\frac{3}{2}}+C$
- $\left(y + 5\right)^{\frac{3}{2}}=2 \left(x - 4\right)^{\frac{3}{2}}+C$
- $\left(y + 5\right)^{\frac{3}{2}}=\sqrt{x - 4}+C$
- $\left(y + 5\right)^{\frac{3}{2}}=\left(x - 4\right)^{\frac{3}{2}}+C$
- $\left(y + 5\right)^{\frac{3}{2}}=- \left(x - 4\right)^{\frac{3}{2}}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sqrt{\left(x-4\right)}}{\sqrt{\left(y+5\right)}} \\ \sqrt{\left(y+5\right)}\,\frac{\text{d}y}{\text{d}x} & =\sqrt{\left(x-4\right)}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{\left(y+5\right)}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \sqrt{\left(x-4\right)}\,\text{d}x \\ \int \sqrt{\left(y+5\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \sqrt{\left(x-4\right)}\,\text{d}x \\ \int {\left(y+5\right)}^{1/2}\,\text{d}y & =\int {\left(x-4\right)}^{1/2}\,\text{d}x \\ \frac{2{\left(y+5\right)}^{3/2}}{3} & =\frac{2{\left(x-4\right)}^{3/2}}{3}+K \\ {\left(y+5\right)}^{3/2} & ={\left(x-4\right)}^{3/2}+C \\ \sqrt{{\left(y+5\right)}^{3}} & =\sqrt{{\left(x-4\right)}^{3}}+C,\end{aligned}
$$

where $C=\frac{3K}{2}.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\sqrt{{\left(y+5\right)}^{3}}=\sqrt{{\left(x-4\right)}^{3}}+C.
$$

## Generated observed-bank variant — root_power

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{\sqrt{\left(x-2\right)}}{\sqrt{\left(y+3\right)}}.$

- $\sqrt{{\left(y+3\right)}^{3}}=\sqrt{{\left(x-2\right)}^{3}}+C$
- $\sqrt{{\left(y+3\right)}^{3}}=\left(x-2\right)+C$
- ${\left(y+3\right)}^{3}=\sqrt{\left(x-2\right)}+C$
- $\left(y+3\right)=\sqrt{{\left(x-2\right)}^{3}}+C$
- $\left(y+3\right)={\left(x-2\right)}^{2}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sqrt{\left(x-2\right)}}{\sqrt{\left(y+3\right)}} \\ \sqrt{\left(y+3\right)}\,\frac{\text{d}y}{\text{d}x} & =\sqrt{\left(x-2\right)}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{\left(y+3\right)}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \sqrt{\left(x-2\right)}\,\text{d}x \\ \int \sqrt{\left(y+3\right)}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \sqrt{\left(x-2\right)}\,\text{d}x \\ \int {\left(y+3\right)}^{1/2}\,\text{d}y & =\int {\left(x-2\right)}^{1/2}\,\text{d}x \\ \frac{2{\left(y+3\right)}^{3/2}}{3} & =\frac{2{\left(x-2\right)}^{3/2}}{3}+K \\ {\left(y+3\right)}^{3/2} & ={\left(x-2\right)}^{3/2}+C \\ \sqrt{{\left(y+3\right)}^{3}} & =\sqrt{{\left(x-2\right)}^{3}}+C,\end{aligned}
$$

where $C=\frac{3K}{2}.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\sqrt{{\left(y+3\right)}^{3}}=\sqrt{{\left(x-2\right)}^{3}}+C.
$$

## Original replay — sin_poly

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{3{x}^{2}}{\operatorname{cos}⁡y}.$

- $\text{ }y={x}^{3}+C$
- $\operatorname{sin}⁡y={x}^{3}+C$
- $\operatorname{sin}⁡y=\frac{1}{{x}^{3}}+C$
- $\operatorname{tan}⁡y=\frac{1}{{x}^{3}}+C$
- $\operatorname{tan}⁡y={x}^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3{x}^{2}}{\operatorname{cos}⁡y} \\ \operatorname{cos}⁡y\,\frac{\text{d}y}{\text{d}x} & =3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{cos}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 3{x}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 3{x}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡y\,\text{d}y & =\int 3{x}^{2}\,\text{d}x \\ \operatorname{sin}⁡y & ={x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sin}⁡y={x}^{3}+C.
$$

## Generated standard variant — sin_poly

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{3{x}^{2}}{\operatorname{cos}⁡\left(y-1\right)}.$

- $\sin{\left(y - 1 \right)}=x^{3}+C$
- $\sin{\left(y - 1 \right)}=2 x^{3}+C$
- $y - 1=x^{3}+C$
- $\tan{\left(y - 1 \right)}=x^{3}+C$
- $\sin{\left(y - 1 \right)}=- x^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3{x}^{2}}{\operatorname{cos}⁡\left(y-1\right)} \\ \operatorname{cos}⁡\left(y-1\right)\,\frac{\text{d}y}{\text{d}x} & =3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{cos}⁡\left(y-1\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 3{x}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡\left(y-1\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 3{x}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡\left(y-1\right)\,\text{d}y & =\int 3{x}^{2}\,\text{d}x \\ \operatorname{sin}⁡\left(y-1\right) & ={x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sin}⁡\left(y-1\right)={x}^{3}+C.
$$

## Generated standard variant — sin_poly

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{3{\left(x-4\right)}^{2}}{\operatorname{cos}⁡\left(y+5\right)}.$

- $y + 5=\left(x - 4\right)^{3}+C$
- $\sin{\left(y + 5 \right)}=2 \left(x - 4\right)^{3}+C$
- $\tan{\left(y + 5 \right)}=\left(x - 4\right)^{3}+C$
- $\sin{\left(y + 5 \right)}=\left(x - 4\right)^{3}+C$
- $\sin{\left(y + 5 \right)}=- \left(x - 4\right)^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3{\left(x-4\right)}^{2}}{\operatorname{cos}⁡\left(y+5\right)} \\ \operatorname{cos}⁡\left(y+5\right)\,\frac{\text{d}y}{\text{d}x} & =3{\left(x-4\right)}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{cos}⁡\left(y+5\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 3{\left(x-4\right)}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡\left(y+5\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 3{\left(x-4\right)}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡\left(y+5\right)\,\text{d}y & =\int 3{\left(x-4\right)}^{2}\,\text{d}x \\ \operatorname{sin}⁡\left(y+5\right) & ={\left(x-4\right)}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sin}⁡\left(y+5\right)={\left(x-4\right)}^{3}+C.
$$

## Generated observed-bank variant — sin_poly

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{3{\left(x-2\right)}^{2}}{\operatorname{cos}⁡\left(y+3\right)}.$

- $\operatorname{tan}⁡\left(y+3\right)={\left(x-2\right)}^{3}+C$
- $\text{ }\left(y+3\right)={\left(x-2\right)}^{3}+C$
- $\operatorname{tan}⁡\left(y+3\right)=\frac{1}{{\left(x-2\right)}^{3}}+C$
- $\operatorname{sin}⁡\left(y+3\right)=\frac{1}{{\left(x-2\right)}^{3}}+C$
- $\operatorname{sin}⁡\left(y+3\right)={\left(x-2\right)}^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3{\left(x-2\right)}^{2}}{\operatorname{cos}⁡\left(y+3\right)} \\ \operatorname{cos}⁡\left(y+3\right)\,\frac{\text{d}y}{\text{d}x} & =3{\left(x-2\right)}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{cos}⁡\left(y+3\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 3{\left(x-2\right)}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡\left(y+3\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 3{\left(x-2\right)}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡\left(y+3\right)\,\text{d}y & =\int 3{\left(x-2\right)}^{2}\,\text{d}x \\ \operatorname{sin}⁡\left(y+3\right) & ={\left(x-2\right)}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sin}⁡\left(y+3\right)={\left(x-2\right)}^{3}+C.
$$

## Original replay — sec_log

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{x\operatorname{sec}⁡y\operatorname{tan}⁡y}$ for $x\ne 0$ and $-\frac{\pi }{2}<y<\frac{\pi }{2}.$

- $\operatorname{sec}⁡y=\operatorname{ln}⁡|x|+C$
- $\operatorname{tan}⁡y=\frac{1}{{x}^{2}}+C$
- $\operatorname{tan}⁡y=\operatorname{ln}⁡|x|+C$
- ${sec}^{2}⁡y=\frac{1}{x}+C$
- $\operatorname{sec}⁡y=-\frac{1}{{x}^{2}}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{x\operatorname{sec}⁡y\operatorname{tan}⁡y} \\ \operatorname{sec}⁡y\operatorname{tan}⁡y\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{sec}⁡y\operatorname{tan}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{x}\,\text{d}x \\ \int \operatorname{sec}⁡y\operatorname{tan}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{x}\,\text{d}x \\ \int \operatorname{sec}⁡y\operatorname{tan}⁡y\,\text{d}y & =\int \frac{1}{x}\,\text{d}x \\ \operatorname{sec}⁡y & =\operatorname{ln}⁡|x|+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sec}⁡y=\operatorname{ln}⁡|x|+C.
$$

## Generated standard variant — sec_log

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{1}{x\operatorname{sec}⁡\left(y-1\right)\operatorname{tan}⁡\left(y-1\right)}$ for $x\ne 0$ and $-\frac{\pi }{2}<\left(y-1\right)<\frac{\pi }{2}.$ Also require $\left(y-1\right)\ne 0.$

- $\sec{\left(y - 1 \right)}=\ln{\left(\left|{x}\right| \right)}+C$
- $\sec{\left(y - 1 \right)}=2 \ln{\left(\left|{x}\right| \right)}+C$
- $\tan{\left(y - 1 \right)}=\ln{\left(\left|{x}\right| \right)}+C$
- $\sec^{2}{\left(y - 1 \right)}=\ln{\left(\left|{x}\right| \right)}+C$
- $\sec{\left(y - 1 \right)}=- \ln{\left(\left|{x}\right| \right)}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{x\operatorname{sec}⁡\left(y-1\right)\operatorname{tan}⁡\left(y-1\right)} \\ \operatorname{sec}⁡\left(y-1\right)\operatorname{tan}⁡\left(y-1\right)\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{sec}⁡\left(y-1\right)\operatorname{tan}⁡\left(y-1\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{x}\,\text{d}x \\ \int \operatorname{sec}⁡\left(y-1\right)\operatorname{tan}⁡\left(y-1\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{x}\,\text{d}x \\ \int \operatorname{sec}⁡\left(y-1\right)\operatorname{tan}⁡\left(y-1\right)\,\text{d}y & =\int \frac{1}{x}\,\text{d}x \\ \operatorname{sec}⁡\left(y-1\right) & =\operatorname{ln}⁡|x|+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sec}⁡\left(y-1\right)=\operatorname{ln}⁡|x|+C.
$$

## Generated standard variant — sec_log

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{1}{\left(x-4\right)\operatorname{sec}⁡\left(y+5\right)\operatorname{tan}⁡\left(y+5\right)}$ for $\left(x-4\right)\ne 0$ and $-\frac{\pi }{2}<\left(y+5\right)<\frac{\pi }{2}.$ Also require $\left(y+5\right)\ne 0.$

- $\tan{\left(y + 5 \right)}=\ln{\left(\left|{x - 4}\right| \right)}+C$
- $\sec{\left(y + 5 \right)}=2 \ln{\left(\left|{x - 4}\right| \right)}+C$
- $\sec^{2}{\left(y + 5 \right)}=\ln{\left(\left|{x - 4}\right| \right)}+C$
- $\sec{\left(y + 5 \right)}=\ln{\left(\left|{x - 4}\right| \right)}+C$
- $\sec{\left(y + 5 \right)}=- \ln{\left(\left|{x - 4}\right| \right)}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\left(x-4\right)\operatorname{sec}⁡\left(y+5\right)\operatorname{tan}⁡\left(y+5\right)} \\ \operatorname{sec}⁡\left(y+5\right)\operatorname{tan}⁡\left(y+5\right)\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{\left(x-4\right)}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{sec}⁡\left(y+5\right)\operatorname{tan}⁡\left(y+5\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\left(x-4\right)}\,\text{d}x \\ \int \operatorname{sec}⁡\left(y+5\right)\operatorname{tan}⁡\left(y+5\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{\left(x-4\right)}\,\text{d}x \\ \int \operatorname{sec}⁡\left(y+5\right)\operatorname{tan}⁡\left(y+5\right)\,\text{d}y & =\int \frac{1}{\left(x-4\right)}\,\text{d}x \\ \operatorname{sec}⁡\left(y+5\right) & =\operatorname{ln}⁡|\left(x-4\right)|+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sec}⁡\left(y+5\right)=\operatorname{ln}⁡|\left(x-4\right)|+C.
$$

## Generated observed-bank variant — sec_log

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{\left(x-2\right)\operatorname{sec}⁡\left(y+3\right)\operatorname{tan}⁡\left(y+3\right)}$ for $\left(x-2\right)\ne 0$ and $-\frac{\pi }{2}<\left(y+3\right)<\frac{\pi }{2}.$

- $\operatorname{sec}⁡\left(y+3\right)=-\frac{1}{{\left(x-2\right)}^{2}}+C$
- $\operatorname{sec}⁡\left(y+3\right)=\operatorname{ln}⁡|\left(x-2\right)|+C$
- ${sec}^{2}⁡\left(y+3\right)=\frac{1}{\left(x-2\right)}+C$
- $\operatorname{tan}⁡\left(y+3\right)=\operatorname{ln}⁡|\left(x-2\right)|+C$
- $\operatorname{tan}⁡\left(y+3\right)=\frac{1}{{\left(x-2\right)}^{2}}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\left(x-2\right)\operatorname{sec}⁡\left(y+3\right)\operatorname{tan}⁡\left(y+3\right)} \\ \operatorname{sec}⁡\left(y+3\right)\operatorname{tan}⁡\left(y+3\right)\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{\left(x-2\right)}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{sec}⁡\left(y+3\right)\operatorname{tan}⁡\left(y+3\right)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\left(x-2\right)}\,\text{d}x \\ \int \operatorname{sec}⁡\left(y+3\right)\operatorname{tan}⁡\left(y+3\right)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{\left(x-2\right)}\,\text{d}x \\ \int \operatorname{sec}⁡\left(y+3\right)\operatorname{tan}⁡\left(y+3\right)\,\text{d}y & =\int \frac{1}{\left(x-2\right)}\,\text{d}x \\ \operatorname{sec}⁡\left(y+3\right) & =\operatorname{ln}⁡|\left(x-2\right)|+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sec}⁡\left(y+3\right)=\operatorname{ln}⁡|\left(x-2\right)|+C.
$$

## Original replay — log_sin

{"h": 0, "k": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y\operatorname{sin}⁡x$ for $y\ne 0.$

- $\operatorname{ln}⁡|y|=\operatorname{sec}⁡x+C$
- $\frac{1}{{y}^{2}}=\operatorname{sec}⁡x+C$
- $\frac{1}{{y}^{2}}=-\operatorname{cos}⁡x+C$
- $\operatorname{ln}⁡|y|=-\operatorname{cos}⁡x+C$
- $y=\operatorname{cos}⁡x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y\operatorname{sin}⁡x \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ \int \frac{1}{y}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sin}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=-\operatorname{cos}⁡x+C
$$

## Generated standard variant — log_sin

{"h": 0, "k": -1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\left(y-1\right)\operatorname{sin}⁡x$ for $\left(y-1\right)\ne 0.$

- $\ln{\left(\left|{y - 1}\right| \right)}=- \cos{\left(x \right)}+C$
- $\ln{\left(\left|{y - 1}\right| \right)}=- 2 \cos{\left(x \right)}+C$
- $\frac{1}{y - 1}=- \cos{\left(x \right)}+C$
- $\ln{\left(\left|{y - 1}\right| \right)}=\sin{\left(x \right)}+C$
- $\ln{\left(\left|{y - 1}\right| \right)}=\cos{\left(x \right)}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(y-1\right)\operatorname{sin}⁡x \\ \frac{1}{\left(y-1\right)}\cdot \frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\left(y-1\right)}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ \int \frac{1}{\left(y-1\right)}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡x\,\text{d}x \\ \int \frac{1}{\left(y-1\right)}\,\text{d}y & =\int \operatorname{sin}⁡x\,\text{d}x \\ \operatorname{ln}⁡|\left(y-1\right)| & =-\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|\left(y-1\right)|=-\operatorname{cos}⁡x+C
$$

## Generated standard variant — log_sin

{"h": -4, "k": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\left(y+5\right)\operatorname{sin}⁡\left(x-4\right)$ for $\left(y+5\right)\ne 0.$

- $\frac{1}{y + 5}=- \cos{\left(x - 4 \right)}+C$
- $\ln{\left(\left|{y + 5}\right| \right)}=- 2 \cos{\left(x - 4 \right)}+C$
- $\ln{\left(\left|{y + 5}\right| \right)}=\sin{\left(x - 4 \right)}+C$
- $\ln{\left(\left|{y + 5}\right| \right)}=- \cos{\left(x - 4 \right)}+C$
- $\ln{\left(\left|{y + 5}\right| \right)}=\cos{\left(x - 4 \right)}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(y+5\right)\operatorname{sin}⁡\left(x-4\right) \\ \frac{1}{\left(y+5\right)}\cdot \frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡\left(x-4\right)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\left(y+5\right)}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡\left(x-4\right)\,\text{d}x \\ \int \frac{1}{\left(y+5\right)}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡\left(x-4\right)\,\text{d}x \\ \int \frac{1}{\left(y+5\right)}\,\text{d}y & =\int \operatorname{sin}⁡\left(x-4\right)\,\text{d}x \\ \operatorname{ln}⁡|\left(y+5\right)| & =-\operatorname{cos}⁡\left(x-4\right)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|\left(y+5\right)|=-\operatorname{cos}⁡\left(x-4\right)+C
$$

## Generated observed-bank variant — log_sin

{"h": -2, "k": 3}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\left(y+3\right)\operatorname{sin}⁡\left(x-2\right)$ for $\left(y+3\right)\ne 0.$

- $\left(y+3\right)=\operatorname{cos}⁡\left(x-2\right)+C$
- $\operatorname{ln}⁡|\left(y+3\right)|=\operatorname{sec}⁡\left(x-2\right)+C$
- $\operatorname{ln}⁡|\left(y+3\right)|=-\operatorname{cos}⁡\left(x-2\right)+C$
- $\frac{1}{{\left(y+3\right)}^{2}}=-\operatorname{cos}⁡\left(x-2\right)+C$
- $\frac{1}{{\left(y+3\right)}^{2}}=\operatorname{sec}⁡\left(x-2\right)+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\left(y+3\right)\operatorname{sin}⁡\left(x-2\right) \\ \frac{1}{\left(y+3\right)}\cdot \frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡\left(x-2\right)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\left(y+3\right)}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡\left(x-2\right)\,\text{d}x \\ \int \frac{1}{\left(y+3\right)}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡\left(x-2\right)\,\text{d}x \\ \int \frac{1}{\left(y+3\right)}\,\text{d}y & =\int \operatorname{sin}⁡\left(x-2\right)\,\text{d}x \\ \operatorname{ln}⁡|\left(y+3\right)| & =-\operatorname{cos}⁡\left(x-2\right)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|\left(y+3\right)|=-\operatorname{cos}⁡\left(x-2\right)+C
$$

## Generated standard variant — two_x_terms

{"a": 5, "b": 1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{5 x^{2} + 1}{y^{2}}.$ Work on an interval where $y\ne 0.$

- $\frac{y^{3}}{3}=\frac{5 x^{3}}{3} + x+C$
- $\frac{y^{3}}{3}=\frac{10 x^{3}}{3} + 2 x+C$
- $y^{2}=\frac{5 x^{3}}{3} + x+C$
- $\frac{y^{3}}{3}=\frac{5 x^{3}}{3}+C$
- $\frac{y^{3}}{3}=- \frac{5 x^{3}}{3} - x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{5 x^{2} + 1}{y^{2}} \\ (y^{2})\,\frac{\text{d}y}{\text{d}x} & =5 x^{2} + 1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int (y^{2})\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (5 x^{2} + 1)\,\text{d}x \\ \int (y^{2})\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (5 x^{2} + 1)\,\text{d}x \\ \int (y^{2})\,\text{d}y & =\int (5 x^{2} + 1)\,\text{d}x \\ \int y^2\,\text{d}y & =\int 5x^2\,\text{d}x+\int 1\,\text{d}x \\ \frac{y^3}{3} & =\frac{5x^3}{3}+1x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{3}}{3}=\frac{5 x^{3}}{3} + x+C.
$$

## Generated standard variant — two_x_terms

{"a": 3, "b": -2}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{3 x^{2} - 2}{y^{2}}.$ Work on an interval where $y\ne 0.$

- $y^{2}=x^{3} - 2 x+C$
- $\frac{y^{3}}{3}=2 x^{3} - 4 x+C$
- $\frac{y^{3}}{3}=- x^{3} + 2 x+C$
- $\frac{y^{3}}{3}=x^{3} - 2 x+C$
- $\frac{y^{3}}{3}=x^{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3 x^{2} - 2}{y^{2}} \\ (y^{2})\,\frac{\text{d}y}{\text{d}x} & =3 x^{2} - 2\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int (y^{2})\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3 x^{2} - 2)\,\text{d}x \\ \int (y^{2})\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (3 x^{2} - 2)\,\text{d}x \\ \int (y^{2})\,\text{d}y & =\int (3 x^{2} - 2)\,\text{d}x \\ \int y^2\,\text{d}y & =\int 3x^2\,\text{d}x-\int 2\,\text{d}x \\ \frac{y^3}{3} & =\frac{3x^3}{3}-2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{3}}{3}=x^{3} - 2 x+C.
$$

## Generated standard variant — two_x_terms

{"a": 4, "b": -4}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{4 x^{2} - 4}{y^{2}}.$ Work on an interval where $y\ne 0.$

- $\frac{y^{3}}{3}=\frac{4 x^{3}}{3}+C$
- $y^{2}=\frac{4 x^{3}}{3} - 4 x+C$
- $\frac{y^{3}}{3}=- \frac{4 x^{3}}{3} + 4 x+C$
- $\frac{y^{3}}{3}=\frac{8 x^{3}}{3} - 8 x+C$
- $\frac{y^{3}}{3}=\frac{4 x^{3}}{3} - 4 x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4 x^{2} - 4}{y^{2}} \\ (y^{2})\,\frac{\text{d}y}{\text{d}x} & =4 x^{2} - 4\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int (y^{2})\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (4 x^{2} - 4)\,\text{d}x \\ \int (y^{2})\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (4 x^{2} - 4)\,\text{d}x \\ \int (y^{2})\,\text{d}y & =\int (4 x^{2} - 4)\,\text{d}x \\ \int y^2\,\text{d}y & =\int 4x^2\,\text{d}x-\int 4\,\text{d}x \\ \frac{y^3}{3} & =\frac{4x^3}{3}-4x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{3}}{3}=\frac{4 x^{3}}{3} - 4 x+C.
$$

## Generated standard variant — two_sided_terms

{"a": 5, "b": 1, "d": 2}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{5 x^{2} + 1}{y^{2} + 2}.$

- $\frac{y^{3}}{3} + 2 y=\frac{5 x^{3}}{3} + x+C$
- $\frac{y^{3}}{3} + 2 y=\frac{5 x^{3}}{3}+C$
- $\frac{y^{3}}{3} + 2 y=\frac{10 x^{3}}{3} + 2 x+C$
- $\frac{y^{3}}{3}=\frac{5 x^{3}}{3} + x+C$
- $\frac{y^{3}}{3} + 2 y=- \frac{5 x^{3}}{3} - x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{5 x^{2} + 1}{y^{2} + 2} \\ (y^{2} + 2)\,\frac{\text{d}y}{\text{d}x} & =5 x^{2} + 1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int (y^{2} + 2)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (5 x^{2} + 1)\,\text{d}x \\ \int (y^{2} + 2)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (5 x^{2} + 1)\,\text{d}x \\ \int (y^{2} + 2)\,\text{d}y & =\int (5 x^{2} + 1)\,\text{d}x \\ \int y^2\,\text{d}y+\int 2\,\text{d}y & =\int 5x^2\,\text{d}x+\int 1\,\text{d}x \\ \frac{y^3}{3}+2y & =\frac{5x^3}{3}+1x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{3}}{3} + 2 y=\frac{5 x^{3}}{3} + x+C.
$$

## Generated standard variant — two_sided_terms

{"a": 3, "b": -2, "d": 5}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{3 x^{2} - 2}{y^{2} + 5}.$

- $\frac{y^{3}}{3} + 5 y=x^{3}+C$
- $\frac{y^{3}}{3}=x^{3} - 2 x+C$
- $\frac{y^{3}}{3} + 5 y=- x^{3} + 2 x+C$
- $\frac{y^{3}}{3} + 5 y=2 x^{3} - 4 x+C$
- $\frac{y^{3}}{3} + 5 y=x^{3} - 2 x+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3 x^{2} - 2}{y^{2} + 5} \\ (y^{2} + 5)\,\frac{\text{d}y}{\text{d}x} & =3 x^{2} - 2\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int (y^{2} + 5)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3 x^{2} - 2)\,\text{d}x \\ \int (y^{2} + 5)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (3 x^{2} - 2)\,\text{d}x \\ \int (y^{2} + 5)\,\text{d}y & =\int (3 x^{2} - 2)\,\text{d}x \\ \int y^2\,\text{d}y+\int 5\,\text{d}y & =\int 3x^2\,\text{d}x-\int 2\,\text{d}x \\ \frac{y^3}{3}+5y & =\frac{3x^3}{3}-2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{3}}{3} + 5 y=x^{3} - 2 x+C.
$$

## Generated standard variant — two_sided_terms

{"a": 4, "b": -4, "d": 1}

Find the general solution to the differential equation (in implicit form) $\frac{\text{d}y}{\text{d}x}=\frac{4 x^{2} - 4}{y^{2} + 1}.$

- $\frac{y^{3}}{3} + y=\frac{4 x^{3}}{3} - 4 x+C$
- $\frac{y^{3}}{3}=\frac{4 x^{3}}{3} - 4 x+C$
- $\frac{y^{3}}{3} + y=- \frac{4 x^{3}}{3} + 4 x+C$
- $\frac{y^{3}}{3} + y=\frac{8 x^{3}}{3} - 8 x+C$
- $\frac{y^{3}}{3} + y=\frac{4 x^{3}}{3}+C$

To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4 x^{2} - 4}{y^{2} + 1} \\ (y^{2} + 1)\,\frac{\text{d}y}{\text{d}x} & =4 x^{2} - 4\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int (y^{2} + 1)\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (4 x^{2} - 4)\,\text{d}x \\ \int (y^{2} + 1)\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (4 x^{2} - 4)\,\text{d}x \\ \int (y^{2} + 1)\,\text{d}y & =\int (4 x^{2} - 4)\,\text{d}x \\ \int y^2\,\text{d}y+\int 1\,\text{d}y & =\int 4x^2\,\text{d}x-\int 4\,\text{d}x \\ \frac{y^3}{3}+1y & =\frac{4x^3}{3}-4x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{3}}{3} + y=\frac{4 x^{3}}{3} - 4 x+C.
$$
