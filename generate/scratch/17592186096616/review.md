# Original and generated side-by-side review

Source payload is retained verbatim. Formula notation is standardized; original instructional sentences and the derivative/evaluation stage counts are retained. Missing source solutions and field repairs are labeled in metadata.

## q-17373

### Original

Given that $y =-\frac{3}{5}\ln x$, find the slope of the tangent at $x = 1$.

No source solution.

Original bank: ['-\\frac{5}{3}', '0', '\\frac{3}{5}', '-\\frac{3}{5}', '\\frac{5}{3}']

### replay

Given that $y=-\frac{3}{5}\cdot \ln{\left(x \right)}$, find the slope of the tangent at $x=1.$

Bank: ['0', '- \\frac{3}{5}', '\\frac{3}{5}', '\\frac{5}{3}', '- \\frac{5}{3}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(-\frac{3}{5}\cdot \ln{\left(x \right)}) \\ &=-\frac{3}{5}\cdot (\frac{1}{x}) \\ &=- \frac{3}{5 x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(- \frac{3}{5 x}\right)\big|_{x=1} \\ &=- \frac{3}{5}\,.\end{aligned}
$$

Repairs: ['legacy easy classification; mathematically recovered correct ref; authored missing solution']

### variant

Given that $y=-\frac{2}{3}\cdot \ln{\left(x \right)}$, find the slope of the tangent at $x=1.$

Bank: ['0', '\\frac{2}{3}', '\\frac{3}{2}', '- \\frac{3}{2}', '- \\frac{2}{3}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(-\frac{2}{3}\cdot \ln{\left(x \right)}) \\ &=-\frac{2}{3}\cdot (\frac{1}{x}) \\ &=- \frac{2}{3 x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(- \frac{2}{3 x}\right)\big|_{x=1} \\ &=- \frac{2}{3}\,.\end{aligned}
$$

Repairs: ['legacy easy classification; mathematically recovered correct ref; authored missing solution']

## q-17395

### Original

Given that $y = \log_{3} x + 5\ln x$, find the slope of the tangent at $x = 1$.

No source solution.

Original bank: ['\\frac{1}{\\ln 3}', '\\ln 3 + 5', '0', '\\frac{5}{\\ln 3}', '\\frac{1}{\\ln 3} + 5']

### replay

Given that $y=\log_{3}x+5\cdot \ln{\left(x \right)}$, find the slope of the tangent at $x=1.$

Bank: ['\\ln{\\left(3 \\right)} + 5', '\\frac{5}{\\ln{\\left(3 \\right)}}', '0', '\\frac{1}{\\ln{\\left(3 \\right)}} + 5', '\\frac{1}{\\ln{\\left(3 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(\log_{3}x+5\cdot \ln{\left(x \right)}) \\ &=(\frac{1}{x \ln{\left(3 \right)}})+5\cdot (\frac{1}{x}) \\ &=\frac{1}{x \ln{\left(3 \right)}}+\frac{5}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{1}{x \ln{\left(3 \right)}}+\frac{5}{x}\right)\big|_{x=1} \\ &=\frac{1}{\ln{\left(3 \right)}} + 5\,.\end{aligned}
$$

Repairs: ['legacy easy classification; mathematically recovered correct ref; authored missing solution']

### variant

Given that $y=\log_{9}x+8\cdot \ln{\left(x \right)}$, find the slope of the tangent at $x=1.$

Bank: ['0', '\\frac{1}{\\ln{\\left(9 \\right)}} + 8', '\\frac{8}{\\ln{\\left(9 \\right)}}', '\\ln{\\left(9 \\right)} + 8', '\\frac{1}{\\ln{\\left(9 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(\log_{9}x+8\cdot \ln{\left(x \right)}) \\ &=(\frac{1}{x \ln{\left(9 \right)}})+8\cdot (\frac{1}{x}) \\ &=\frac{1}{x \ln{\left(9 \right)}}+\frac{8}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{1}{x \ln{\left(9 \right)}}+\frac{8}{x}\right)\big|_{x=1} \\ &=\frac{1}{\ln{\left(9 \right)}} + 8\,.\end{aligned}
$$

Repairs: ['legacy easy classification; mathematically recovered correct ref; authored missing solution']

## q-101723

### Original

Given that $y=4{e}^{x}-3{log}_{7}x$, find the slope of the tangent at $x=3.$

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=4{e}^{x}-\frac{3}{x\operatorname{ln}7}\,.
$$

Therefore, the slope  of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(4{e}^{x}-\frac{3}{x\operatorname{ln}7})|}_{x=3} \\  & =4{e}^{3}-\frac{3}{3\operatorname{ln}7} \\  & =4{e}^{3}-\frac{1}{\operatorname{ln}7}\,.\end{aligned}
$$

Original bank: []

### replay

Given that $y=4\cdot e^{x}-3\cdot \log_{7}x$, find the slope of the tangent at $x=3.$

{{field-1}}

Bank: ['- \\frac{1}{\\ln{\\left(7 \\right)}} + 4 e^{3}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=4 e^{x}- \frac{3}{x \ln{\left(7 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=3}&=\left(4 e^{x}- \frac{3}{x \ln{\left(7 \right)}}\right)\big|_{x=3} \\ &=4 e^{(3)}- \frac{3}{(3) \ln{\left(7 \right)}} \\ &=- \frac{1}{\ln{\left(7 \right)}} + 4 e^{3}\,.\end{aligned}
$$

Repairs: ['authored blank field for fieldless source; source preserved']

### variant

Given that $y=8\cdot e^{x}-8\cdot \log_{3}x$, find the slope of the tangent at $x=2.$

{{field-1}}

Bank: ['- \\frac{4}{\\ln{\\left(3 \\right)}} + 8 e^{2}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=8 e^{x}- \frac{8}{x \ln{\left(3 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(8 e^{x}- \frac{8}{x \ln{\left(3 \right)}}\right)\big|_{x=2} \\ &=8 e^{(2)}- \frac{8}{(2) \ln{\left(3 \right)}} \\ &=- \frac{4}{\ln{\left(3 \right)}} + 8 e^{2}\,.\end{aligned}
$$

Repairs: ['authored blank field for fieldless source; source preserved']

## q-340014

### Original

Given the function $y=5{x}^{2}+6\operatorname{ln}x,$ the slope of the tangent line at $x=3$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(5{x}^{2}+6\operatorname{ln}x) \\  & =5\frac{\text{d}}{\text{d}x}({x}^{2})+6\frac{\text{d}}{\text{d}x}(\operatorname{ln}x) \\  & =5\cdot 2x+6\cdot \frac{1}{x} \\  & =10x+\frac{6}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(10x+\frac{6}{x})|}_{x=3} \\  & =10\cdot 3+\frac{6}{3} \\  & =32\,.\end{aligned}
$$

Original bank: ['32']

### replay

Given the function $y=5\cdot x^{2}+6\cdot \ln{\left(x \right)},$ the slope of the tangent line at $x=3$ is{{field-1}}.

Bank: ['32']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(5\cdot x^{2}+6\cdot \ln{\left(x \right)}) \\ &=5\cdot \frac{\text{d}}{\text{d}x}(x^{2})+6\cdot \frac{\text{d}}{\text{d}x}(\ln{\left(x \right)}) \\ &=5\cdot (2 x)+6\cdot (\frac{1}{x}) \\ &=10 x+\frac{6}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=3}&=\left(10 x+\frac{6}{x}\right)\big|_{x=3} \\ &=10 (3)+\frac{6}{(3)} \\ &=32\,.\end{aligned}
$$

Repairs: []

### variant

Given the function $y=8\cdot x^{2}+8\cdot \ln{\left(x \right)},$ the slope of the tangent line at $x=1$ is{{field-1}}.

Bank: ['24']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(8\cdot x^{2}+8\cdot \ln{\left(x \right)}) \\ &=8\cdot \frac{\text{d}}{\text{d}x}(x^{2})+8\cdot \frac{\text{d}}{\text{d}x}(\ln{\left(x \right)}) \\ &=8\cdot (2 x)+8\cdot (\frac{1}{x}) \\ &=16 x+\frac{8}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(16 x+\frac{8}{x}\right)\big|_{x=1} \\ &=16 (1)+\frac{8}{(1)} \\ &=24\,.\end{aligned}
$$

Repairs: []

## q-340022

### Original

Given the function $y=5\operatorname{ln}x-2\cdot {3}^{x},$ the slope of the tangent line at $x=2$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(5\operatorname{ln}x-2\cdot {3}^{x}) \\  & =5\frac{\text{d}}{\text{d}x}(\operatorname{ln}x)-2\frac{\text{d}}{\text{d}x}({3}^{x}) \\  & =5\cdot \frac{1}{x}-2\cdot {3}^{x}\operatorname{ln}3 \\  & =\frac{5}{x}-2\operatorname{ln}3\cdot {3}^{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{5}{x}-2\operatorname{ln}3\cdot {3}^{x})|}_{x=2} \\  & =\frac{5}{2}-2\operatorname{ln}3\cdot {3}^{2} \\  & =\frac{5}{2}-18\operatorname{ln}3\,.\end{aligned}
$$

Original bank: ['\\frac{5}{2}-18\\operatorname{ln}3']

### replay

Given the function $y=5\cdot \ln{\left(x \right)}-2\cdot 3^{x},$ the slope of the tangent line at $x=2$ is{{field-1}}.

Bank: ['\\frac{5}{2} - 18 \\ln{\\left(3 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(5\cdot \ln{\left(x \right)}-2\cdot 3^{x}) \\ &=5\cdot \frac{\text{d}}{\text{d}x}(\ln{\left(x \right)})-2\cdot \frac{\text{d}}{\text{d}x}(3^{x}) \\ &=5\cdot (\frac{1}{x})-2\cdot (3^{x} \ln{\left(3 \right)}) \\ &=\frac{5}{x}- 2 \cdot 3^{x} \ln{\left(3 \right)}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(\frac{5}{x}- 2 \cdot 3^{x} \ln{\left(3 \right)}\right)\big|_{x=2} \\ &=\frac{5}{(2)}- 2 \cdot 3^{(2)} \ln{\left(3 \right)} \\ &=\frac{5}{2} - 18 \ln{\left(3 \right)}\,.\end{aligned}
$$

Repairs: []

### variant

Given the function $y=8\cdot \ln{\left(x \right)}-8\cdot 3^{x},$ the slope of the tangent line at $x=2$ is{{field-1}}.

Bank: ['4 - 72 \\ln{\\left(3 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(8\cdot \ln{\left(x \right)}-8\cdot 3^{x}) \\ &=8\cdot \frac{\text{d}}{\text{d}x}(\ln{\left(x \right)})-8\cdot \frac{\text{d}}{\text{d}x}(3^{x}) \\ &=8\cdot (\frac{1}{x})-8\cdot (3^{x} \ln{\left(3 \right)}) \\ &=\frac{8}{x}- 8 \cdot 3^{x} \ln{\left(3 \right)}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(\frac{8}{x}- 8 \cdot 3^{x} \ln{\left(3 \right)}\right)\big|_{x=2} \\ &=\frac{8}{(2)}- 8 \cdot 3^{(2)} \ln{\left(3 \right)} \\ &=4 - 72 \ln{\left(3 \right)}\,.\end{aligned}
$$

Repairs: []

## q-340109

### Original

Given the function $y=-3{e}^{x}+2{log}_{4}x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-3{e}^{x}+2{log}_{4}x) \\  & =-3\frac{\text{d}}{\text{d}x}({e}^{x})+2\frac{\text{d}}{\text{d}x}({log}_{4}x) \\  & =-3{e}^{x}+2\cdot \frac{1}{x\operatorname{ln}4} \\  & =-3{e}^{x}+\frac{2}{x\operatorname{ln}4}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(-3{e}^{x}+\frac{2}{x\operatorname{ln}4})|}_{x=2} \\  & =-3{e}^{2}+\frac{2}{2\cdot \operatorname{ln}4} \\  & =-3{e}^{2}+\frac{1}{\operatorname{ln}4}\,.\end{aligned}
$$

Original bank: ['-3{e}^{2}+\\frac{1}{\\operatorname{ln}4}', '-3e^2+\\frac{1}{\\ln4}']

### replay

Given the function $y=-3\cdot e^{x}+2\cdot \log_{4}x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

Bank: ['- 3 e^{2} + \\frac{1}{\\operatorname{ln}{\\left(4 \\right)}}', '- 3 e^{2} + \\frac{1}{\\ln{\\left(4 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(-3\cdot e^{x}+2\cdot \log_{4}x) \\ &=-3\cdot \frac{\text{d}}{\text{d}x}(e^{x})+2\cdot \frac{\text{d}}{\text{d}x}(\log_{4}x) \\ &=-3\cdot (e^{x})+2\cdot (\frac{1}{x \ln{\left(4 \right)}}) \\ &=- 3 e^{x}+\frac{2}{x \ln{\left(4 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(- 3 e^{x}+\frac{2}{x \ln{\left(4 \right)}}\right)\big|_{x=2} \\ &=- 3 e^{(2)}+\frac{2}{(2) \ln{\left(4 \right)}} \\ &=- 3 e^{2} + \frac{1}{\ln{\left(4 \right)}}\,.\end{aligned}
$$

Repairs: []

### variant

Given the function $y=-8\cdot e^{x}+8\cdot \log_{3}x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

Bank: ['- 8 e^{2} + \\frac{4}{\\ln{\\left(3 \\right)}}', '- 8 e^{2} + \\frac{4}{\\operatorname{ln}{\\left(3 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(-8\cdot e^{x}+8\cdot \log_{3}x) \\ &=-8\cdot \frac{\text{d}}{\text{d}x}(e^{x})+8\cdot \frac{\text{d}}{\text{d}x}(\log_{3}x) \\ &=-8\cdot (e^{x})+8\cdot (\frac{1}{x \ln{\left(3 \right)}}) \\ &=- 8 e^{x}+\frac{8}{x \ln{\left(3 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(- 8 e^{x}+\frac{8}{x \ln{\left(3 \right)}}\right)\big|_{x=2} \\ &=- 8 e^{(2)}+\frac{8}{(2) \ln{\left(3 \right)}} \\ &=- 8 e^{2} + \frac{4}{\ln{\left(3 \right)}}\,.\end{aligned}
$$

Repairs: []

## q-70897

### Original

Given that $y=2{log}_{2}x+{2}^{x}$, find the slope of the tangent at $x=2.$

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{2}{x\operatorname{ln}2}+{2}^{x}\operatorname{ln}2\,.
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{2}{x\operatorname{ln}2}+{2}^{x}\operatorname{ln}2)|}_{x=2} \\  & =\frac{2}{2\cdot \operatorname{ln}2}+{2}^{2}\operatorname{ln}2 \\  & =\frac{1}{\operatorname{ln}2}+4\operatorname{ln}2\,.\end{aligned}
$$

Original bank: []

### replay

Given that $y=2\cdot \log_{2}x+2^{x}$, find the slope of the tangent at $x=2.$

{{field-1}}

Bank: ['\\frac{1}{\\ln{\\left(2 \\right)}} + 4 \\ln{\\left(2 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{2}{x \ln{\left(2 \right)}}+2^{x} \ln{\left(2 \right)}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(\frac{2}{x \ln{\left(2 \right)}}+2^{x} \ln{\left(2 \right)}\right)\big|_{x=2} \\ &=\frac{2}{(2) \ln{\left(2 \right)}}+2^{(2)} \ln{\left(2 \right)} \\ &=\frac{1}{\ln{\left(2 \right)}} + 4 \ln{\left(2 \right)}\,.\end{aligned}
$$

Repairs: ['authored blank field for fieldless source; source preserved']

### variant

Given that $y=8\cdot \log_{9}x+9^{x}$, find the slope of the tangent at $x=1.$

{{field-1}}

Bank: ['\\frac{8}{\\ln{\\left(9 \\right)}} + 9 \\ln{\\left(9 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{8}{x \ln{\left(9 \right)}}+9^{x} \ln{\left(9 \right)}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{8}{x \ln{\left(9 \right)}}+9^{x} \ln{\left(9 \right)}\right)\big|_{x=1} \\ &=\frac{8}{(1) \ln{\left(9 \right)}}+9^{(1)} \ln{\left(9 \right)} \\ &=\frac{8}{\ln{\left(9 \right)}} + 9 \ln{\left(9 \right)}\,.\end{aligned}
$$

Repairs: ['authored blank field for fieldless source; source preserved']

## q-101726

### Original

Given that $y=3x-5+8{log}_{2}⁡x$, find the slope of the tangent at $x=\frac{1}{ln⁡2}.$

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3x-5+8{log}_{2}⁡x) \\  & =\frac{\text{d}}{\text{d}x}(3x)+\frac{\text{d}}{\text{d}x}(-5)+\frac{\text{d}}{\text{d}x}(8{log}_{2}⁡x) \\  & =3\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(5)+8\frac{\text{d}}{\text{d}x}({log}_{2}⁡x) \\  & =3-0+8\cdot \frac{1}{xln⁡2} \\  & =3+\frac{8}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{1}{ln⁡2}$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1/ln⁡2} & ={(3+\frac{8}{xln⁡2})|}_{x=1/ln⁡2} \\  & =3+\frac{8}{(\frac{1}{ln⁡2}\cdot ln⁡2)} \\  & =3+8 \\  & =11\,.\end{aligned}
$$

Original bank: ['4', '3+8ln\u20612', '11', '8ln\u20612-2', '6']

### replay

Given that $y=3\cdot x-5+8\cdot \log_{2}x$, find the slope of the tangent at $x=\frac{1}{\ln{\left(2 \right)}}.$

Bank: ['3 + 8 \\ln{\\left(2 \\right)}', '-2 + 8 \\ln{\\left(2 \\right)}', '11', '6', '4']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(3\cdot x-5+8\cdot \log_{2}x) \\ &=\frac{\text{d}}{\text{d}x}(3\cdot x)-\frac{\text{d}}{\text{d}x}(5)+\frac{\text{d}}{\text{d}x}(8\cdot \log_{2}x) \\ &=3\cdot \frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(5)+8\cdot \frac{\text{d}}{\text{d}x}(\log_{2}x) \\ &=3\cdot (1)-0+8\cdot (\frac{1}{x \ln{\left(2 \right)}}) \\ &=3+\frac{8}{x \ln{\left(2 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{1}{\ln{\left(2 \right)}}$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=\frac{1}{\ln{\left(2 \right)}}}&=\left(3+\frac{8}{x \ln{\left(2 \right)}}\right)\big|_{x=\frac{1}{\ln{\left(2 \right)}}} \\ &=3+\frac{8}{(\frac{1}{\ln{\left(2 \right)}}) \ln{\left(2 \right)}} \\ &=3+8 \\ &=11\,.\end{aligned}
$$

Repairs: []

### variant

Given that $y=8\cdot x-8+2\cdot \log_{4}x$, find the slope of the tangent at $x=\frac{1}{\ln{\left(4 \right)}}.$

Bank: ['2 \\ln{\\left(4 \\right)} + 8', '10', '2', '9', '2 \\ln{\\left(4 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(8\cdot x-8+2\cdot \log_{4}x) \\ &=\frac{\text{d}}{\text{d}x}(8\cdot x)-\frac{\text{d}}{\text{d}x}(8)+\frac{\text{d}}{\text{d}x}(2\cdot \log_{4}x) \\ &=8\cdot \frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(8)+2\cdot \frac{\text{d}}{\text{d}x}(\log_{4}x) \\ &=8\cdot (1)-0+2\cdot (\frac{1}{x \ln{\left(4 \right)}}) \\ &=8+\frac{2}{x \ln{\left(4 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{1}{\ln{\left(4 \right)}}$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=\frac{1}{\ln{\left(4 \right)}}}&=\left(8+\frac{2}{x \ln{\left(4 \right)}}\right)\big|_{x=\frac{1}{\ln{\left(4 \right)}}} \\ &=8+\frac{2}{(\frac{1}{\ln{\left(4 \right)}}) \ln{\left(4 \right)}} \\ &=8+2 \\ &=10\,.\end{aligned}
$$

Repairs: []

## q-17371

### Original

Given that $y=3ln⁡x+2{x}^{2}-5x$, find the slope of the tangent at $x=1.$

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3ln⁡x+2{x}^{2}-5x) \\  & =\frac{\text{d}}{\text{d}x}(3ln⁡x)+\frac{\text{d}}{\text{d}x}(2{x}^{2})-\frac{\text{d}}{\text{d}x}(5x) \\  & =3\frac{\text{d}}{\text{d}x}(ln⁡x)+\frac{\text{d}}{\text{d}x}(2{x}^{2})-\frac{\text{d}}{\text{d}x}(5x) \\  & =3\cdot \frac{1}{x}+4x-5 \\  & =\frac{3}{x}+4x-5\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{3}{x}+4x-5)|}_{x=1} \\  & =\frac{3}{1}+4\cdot 1-5 \\  & =3+4-5 \\  & =2\,.\end{aligned}
$$

Original bank: ['2', '-3', '-2', '12', '-5']

### replay

Given that $y=3\cdot \ln{\left(x \right)}+2\cdot x^{2}-5\cdot x$, find the slope of the tangent at $x=1.$

Bank: ['-3', '12', '-2', '-5', '2']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(3\cdot \ln{\left(x \right)}+2\cdot x^{2}-5\cdot x) \\ &=\frac{\text{d}}{\text{d}x}(3\cdot \ln{\left(x \right)})+\frac{\text{d}}{\text{d}x}(2\cdot x^{2})-\frac{\text{d}}{\text{d}x}(5\cdot x) \\ &=3\cdot \frac{\text{d}}{\text{d}x}(\ln{\left(x \right)})+2\cdot \frac{\text{d}}{\text{d}x}(x^{2})-5\cdot \frac{\text{d}}{\text{d}x}(x) \\ &=3\cdot (\frac{1}{x})+2\cdot (2 x)-5\cdot (1) \\ &=\frac{3}{x}+4 x-5\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{3}{x}+4 x-5\right)\big|_{x=1} \\ &=\frac{3}{(1)}+4 (1)-5 \\ &=3+4-5 \\ &=2\,.\end{aligned}
$$

Repairs: []

### variant

Given that $y=8\cdot \ln{\left(x \right)}+8\cdot x^{2}-2\cdot x$, find the slope of the tangent at $x=1.$

Bank: ['-2', '-22', '22', '26', '-8']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(8\cdot \ln{\left(x \right)}+8\cdot x^{2}-2\cdot x) \\ &=\frac{\text{d}}{\text{d}x}(8\cdot \ln{\left(x \right)})+\frac{\text{d}}{\text{d}x}(8\cdot x^{2})-\frac{\text{d}}{\text{d}x}(2\cdot x) \\ &=8\cdot \frac{\text{d}}{\text{d}x}(\ln{\left(x \right)})+8\cdot \frac{\text{d}}{\text{d}x}(x^{2})-2\cdot \frac{\text{d}}{\text{d}x}(x) \\ &=8\cdot (\frac{1}{x})+8\cdot (2 x)-2\cdot (1) \\ &=\frac{8}{x}+16 x-2\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{8}{x}+16 x-2\right)\big|_{x=1} \\ &=\frac{8}{(1)}+16 (1)-2 \\ &=8+16-2 \\ &=22\,.\end{aligned}
$$

Repairs: []

## q-340024

### Original

Given the function $y=2{x}^{3}-5{log}_{3}⁡x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2{x}^{3}-5{log}_{3}⁡x) \\  & =2\frac{\text{d}}{\text{d}x}({x}^{3})-5\frac{\text{d}}{\text{d}x}({log}_{3}⁡x) \\  & =2\cdot 3{x}^{2}-5\cdot \frac{1}{xln⁡3} \\  & =6{x}^{2}-\frac{5}{xln⁡3}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(6{x}^{2}-\frac{5}{xln⁡3})|}_{x=2} \\  & =6(2)^{2}-\frac{5}{2ln⁡3} \\  & =24-\frac{5}{2ln⁡3}\,.\end{aligned}
$$

Original bank: ['24-\\frac{5}{2\\operatorname{ln}3}']

### replay

Given the function $y=2\cdot x^{3}-5\cdot \log_{3}x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

Bank: ['24 - \\frac{5}{2 \\ln{\\left(3 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(2\cdot x^{3}-5\cdot \log_{3}x) \\ &=2\cdot \frac{\text{d}}{\text{d}x}(x^{3})-5\cdot \frac{\text{d}}{\text{d}x}(\log_{3}x) \\ &=2\cdot (3 x^{2})-5\cdot (\frac{1}{x \ln{\left(3 \right)}}) \\ &=6 x^{2}- \frac{5}{x \ln{\left(3 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(6 x^{2}- \frac{5}{x \ln{\left(3 \right)}}\right)\big|_{x=2} \\ &=6 (2)^{2}- \frac{5}{(2) \ln{\left(3 \right)}} \\ &=24 - \frac{5}{2 \ln{\left(3 \right)}}\,.\end{aligned}
$$

Repairs: []

### variant

Given the function $y=8\cdot x^{3}-8\cdot \log_{3}x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

Bank: ['96 - \\frac{4}{\\ln{\\left(3 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(8\cdot x^{3}-8\cdot \log_{3}x) \\ &=8\cdot \frac{\text{d}}{\text{d}x}(x^{3})-8\cdot \frac{\text{d}}{\text{d}x}(\log_{3}x) \\ &=8\cdot (3 x^{2})-8\cdot (\frac{1}{x \ln{\left(3 \right)}}) \\ &=24 x^{2}- \frac{8}{x \ln{\left(3 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(24 x^{2}- \frac{8}{x \ln{\left(3 \right)}}\right)\big|_{x=2} \\ &=24 (2)^{2}- \frac{8}{(2) \ln{\left(3 \right)}} \\ &=96 - \frac{4}{\ln{\left(3 \right)}}\,.\end{aligned}
$$

Repairs: []

## q-340026

### Original

Given the function $y=6{log}_{2}⁡x+4{x}^{2}-3x,$ the slope of the tangent line at $x=1$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(6{log}_{2}⁡x+4{x}^{2}-3x) \\  & =6\frac{\text{d}}{\text{d}x}({log}_{2}⁡x)+4\frac{\text{d}}{\text{d}x}({x}^{2})-3\frac{\text{d}}{\text{d}x}(x) \\  & =6\cdot \frac{1}{xln⁡2}+4\cdot 2x-3 \\  & =\frac{6}{xln⁡2}+8x-3\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{6}{xln⁡2}+8x-3)|}_{x=1} \\  & =\frac{6}{1\cdot ln⁡2}+8(1)-3 \\  & =\frac{6}{ln⁡2}+5\,.\end{aligned}
$$

Original bank: ['\\frac{6}{\\operatorname{ln}2}+5']

### replay

Given the function $y=6\cdot \log_{2}x+4\cdot x^{2}-3\cdot x,$ the slope of the tangent line at $x=1$ is{{field-1}}.

Bank: ['5 + \\frac{6}{\\ln{\\left(2 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(6\cdot \log_{2}x+4\cdot x^{2}-3\cdot x) \\ &=6\cdot \frac{\text{d}}{\text{d}x}(\log_{2}x)+4\cdot \frac{\text{d}}{\text{d}x}(x^{2})-3\cdot \frac{\text{d}}{\text{d}x}(x) \\ &=6\cdot (\frac{1}{x \ln{\left(2 \right)}})+4\cdot (2 x)-3\cdot (1) \\ &=\frac{6}{x \ln{\left(2 \right)}}+8 x-3\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{6}{x \ln{\left(2 \right)}}+8 x-3\right)\big|_{x=1} \\ &=\frac{6}{(1) \ln{\left(2 \right)}}+8 (1)-3 \\ &=5 + \frac{6}{\ln{\left(2 \right)}}\,.\end{aligned}
$$

Repairs: []

### variant

Given the function $y=8\cdot \log_{4}x+8\cdot x^{2}-2\cdot x,$ the slope of the tangent line at $x=1$ is{{field-1}}.

Bank: ['\\frac{8}{\\ln{\\left(4 \\right)}} + 14']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(8\cdot \log_{4}x+8\cdot x^{2}-2\cdot x) \\ &=8\cdot \frac{\text{d}}{\text{d}x}(\log_{4}x)+8\cdot \frac{\text{d}}{\text{d}x}(x^{2})-2\cdot \frac{\text{d}}{\text{d}x}(x) \\ &=8\cdot (\frac{1}{x \ln{\left(4 \right)}})+8\cdot (2 x)-2\cdot (1) \\ &=\frac{8}{x \ln{\left(4 \right)}}+16 x-2\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{8}{x \ln{\left(4 \right)}}+16 x-2\right)\big|_{x=1} \\ &=\frac{8}{(1) \ln{\left(4 \right)}}+16 (1)-2 \\ &=\frac{8}{\ln{\left(4 \right)}} + 14\,.\end{aligned}
$$

Repairs: []

## q-340110

### Original

Given the function $y=4{e}^{x}-3{log}_{2}⁡x+7,$ the slope of the tangent line at $x=3$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(4{e}^{x}-3{log}_{2}⁡x+7) \\  & =4\frac{\text{d}}{\text{d}x}({e}^{x})-3\frac{\text{d}}{\text{d}x}({log}_{2}⁡x)+\frac{\text{d}}{\text{d}x}(7) \\  & =4{e}^{x}-3\cdot \frac{1}{xln⁡2}+0 \\  & =4{e}^{x}-\frac{3}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(4{e}^{x}-\frac{3}{xln⁡2})|}_{x=3} \\  & =4{e}^{3}-\frac{3}{3\cdot ln⁡2} \\  & =4{e}^{3}-\frac{1}{ln⁡2}\,.\end{aligned}
$$

Original bank: ['4{e}^{3}-\\frac{1}{\\operatorname{ln}2}']

### replay

Given the function $y=4\cdot e^{x}-3\cdot \log_{2}x+7,$ the slope of the tangent line at $x=3$ is{{field-1}}.

Bank: ['- \\frac{1}{\\ln{\\left(2 \\right)}} + 4 e^{3}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(4\cdot e^{x}-3\cdot \log_{2}x+7) \\ &=4\cdot \frac{\text{d}}{\text{d}x}(e^{x})-3\cdot \frac{\text{d}}{\text{d}x}(\log_{2}x)+\frac{\text{d}}{\text{d}x}(7) \\ &=4\cdot (e^{x})-3\cdot (\frac{1}{x \ln{\left(2 \right)}})+0 \\ &=4 e^{x}- \frac{3}{x \ln{\left(2 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=3}&=\left(4 e^{x}- \frac{3}{x \ln{\left(2 \right)}}\right)\big|_{x=3} \\ &=4 e^{(3)}- \frac{3}{(3) \ln{\left(2 \right)}} \\ &=- \frac{1}{\ln{\left(2 \right)}} + 4 e^{3}\,.\end{aligned}
$$

Repairs: []

### variant

Given the function $y=8\cdot e^{x}-8\cdot \log_{3}x+3,$ the slope of the tangent line at $x=4$ is{{field-1}}.

Bank: ['- \\frac{2}{\\ln{\\left(3 \\right)}} + 8 e^{4}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(8\cdot e^{x}-8\cdot \log_{3}x+3) \\ &=8\cdot \frac{\text{d}}{\text{d}x}(e^{x})-8\cdot \frac{\text{d}}{\text{d}x}(\log_{3}x)+\frac{\text{d}}{\text{d}x}(3) \\ &=8\cdot (e^{x})-8\cdot (\frac{1}{x \ln{\left(3 \right)}})+0 \\ &=8 e^{x}- \frac{8}{x \ln{\left(3 \right)}}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=4$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=4}&=\left(8 e^{x}- \frac{8}{x \ln{\left(3 \right)}}\right)\big|_{x=4} \\ &=8 e^{(4)}- \frac{8}{(4) \ln{\left(3 \right)}} \\ &=- \frac{2}{\ln{\left(3 \right)}} + 8 e^{4}\,.\end{aligned}
$$

Repairs: []

## q-70903

### Original

Given that $y=3\operatorname{log}⁡x+{x}^{3}-4$, find the slope of the tangent at $x=3.$

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{3}{x\operatorname{ln}⁡10}+3{x}^{2}\,.
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(\frac{3}{x\operatorname{ln}⁡10}+3{x}^{2})|}_{x=3} \\  & =\frac{3}{3\cdot \operatorname{ln}⁡10}+3\cdot {3}^{2} \\  & =\frac{1}{\operatorname{ln}⁡10}+27\,.\end{aligned}
$$

Original bank: ['\\frac{9}{\\operatorname{ln}\u206110}-3', '\\frac{1}{\\operatorname{ln}\u206110}+27', '\\frac{1}{3\\operatorname{ln}\u206110}+3', '\\frac{1}{\\operatorname{ln}\u206110}-9', '\\frac{3}{\\operatorname{ln}\u206110}+9']

### replay

Given that $y=3\cdot \log_{10}x+x^{3}-4$, find the slope of the tangent at $x=3.$

Bank: ['\\frac{1}{\\ln{\\left(10 \\right)}} + 27', '-9 + \\frac{1}{\\ln{\\left(10 \\right)}}', '\\frac{1}{3 \\ln{\\left(10 \\right)}} + 3', '\\frac{3}{\\ln{\\left(10 \\right)}} + 9', '-3 + \\frac{9}{\\ln{\\left(10 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{3}{x \ln{\left(10 \right)}}+3 x^{2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=3}&=\left(\frac{3}{x \ln{\left(10 \right)}}+3 x^{2}\right)\big|_{x=3} \\ &=\frac{3}{(3) \ln{\left(10 \right)}}+3 (3)^{2} \\ &=\frac{1}{\ln{\left(10 \right)}} + 27\,.\end{aligned}
$$

Repairs: ['source solution prose says x=1, whereas prompt and calculation use x=3; normal solution uses actual input']

### variant

Given that $y=\log_{10}x+x^{3}-11$, find the slope of the tangent at $x=2.$

Bank: ['\\frac{1}{4 \\ln{\\left(10 \\right)}} + 2', '-2 + \\frac{2}{\\ln{\\left(10 \\right)}}', '-4 + \\frac{1}{2 \\ln{\\left(10 \\right)}}', '\\frac{1}{\\ln{\\left(10 \\right)}} + 4', '\\frac{1}{2 \\ln{\\left(10 \\right)}} + 12']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{1}{x \ln{\left(10 \right)}}+3 x^{2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=2}&=\left(\frac{1}{x \ln{\left(10 \right)}}+3 x^{2}\right)\big|_{x=2} \\ &=\frac{1}{(2) \ln{\left(10 \right)}}+3 (2)^{2} \\ &=\frac{1}{2 \ln{\left(10 \right)}} + 12\,.\end{aligned}
$$

Repairs: ['source solution prose says x=1, whereas prompt and calculation use x=3; normal solution uses actual input']
