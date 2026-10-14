# Frozen basis 1356 review

Raw replay retains omissions and the source q-70903 typo. Normal records complete missing fields/keys and use explicit authored method banks.

## q-17373

### Original

Given that $y =-\frac{3}{5}\ln x$, find the slope of the tangent at $x = 1$.

Source solution omitted.

Original bank: ['-\\frac{5}{3}', '0', '\\frac{3}{5}', '-\\frac{3}{5}', '\\frac{5}{3}']

raw_parameterized_replay

Given that $y =-\frac{3}{5}\ln x$, find the slope of the tangent at $x = 1$.

['\\frac{3}{5}', '0', '\\frac{5}{3}', '-\\frac{3}{5}', '-\\frac{5}{3}']

Source solution omitted.

normal_at_original

Given that $y =-\frac{3}{5}\ln x$, find the slope of the tangent at $x = 1$.

['\\frac{5}{3}', '0', '- \\frac{3}{5}', '- \\frac{5}{3}', '\\frac{3}{5}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(-\frac{3}{5}\ln x) \\ &=-\frac{3}{5}\cdot\frac{1}{x} \\ &=-\frac{3}{5x}\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(- \frac{3}{5 x}\right)\big|_{x=1} \\ &=- \frac{3}{5}\,.\end{aligned}
$$

normal_variant

Given that $y =-\frac{9}{8}\ln x$, find the slope of the tangent at $x = 1$.

['\\frac{8}{9}', '- \\frac{8}{9}', '0', '- \\frac{9}{8}', '\\frac{9}{8}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(-\frac{9}{8}\ln x) \\ &=-\frac{9}{8}\cdot\frac{1}{x} \\ &=-\frac{9}{8x}\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(- \frac{9}{8 x}\right)\big|_{x=1} \\ &=- \frac{9}{8}\,.\end{aligned}
$$

## q-17395

### Original

Given that $y = \log_{3} x + 5\ln x$, find the slope of the tangent at $x = 1$.

Source solution omitted.

Original bank: ['\\frac{1}{\\ln 3}', '\\ln 3 + 5', '0', '\\frac{5}{\\ln 3}', '\\frac{1}{\\ln 3} + 5']

raw_parameterized_replay

Given that $y = \log_{3} x + 5\ln x$, find the slope of the tangent at $x = 1$.

['0', '\\ln 3 + 5', '\\frac{1}{\\ln 3} + 5', '\\frac{5}{\\ln 3}', '\\frac{1}{\\ln 3}']

Source solution omitted.

normal_at_original

Given that $y = \log_{3} x + 5\ln x$, find the slope of the tangent at $x = 1$.

['\\frac{1}{\\ln{\\left(3 \\right)}}', '\\frac{5}{\\ln{\\left(3 \\right)}}', '\\frac{1}{\\ln{\\left(3 \\right)}} + 5', '5', '\\ln{\\left(3 \\right)} + 5']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(\log_{3}x+5\ln x) \\ &=\frac{\text{d}}{\text{d}x}(\log_{3}x)+5\frac{\text{d}}{\text{d}x}(\ln x) \\ &=\frac{1}{x\ln 3}+\frac{5}{x}\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{1}{x \ln{\left(3 \right)}} + \frac{5}{x}\right)\big|_{x=1} \\ &=\frac{1}{\ln{\left(3 \right)}} + 5\,.\end{aligned}
$$

normal_variant

Given that $y = \log_{9} x + 6\ln x$, find the slope of the tangent at $x = 1$.

['\\frac{1}{\\ln{\\left(9 \\right)}}', '6', '\\frac{6}{\\ln{\\left(9 \\right)}}', '\\frac{1}{\\ln{\\left(9 \\right)}} + 6', '\\ln{\\left(9 \\right)} + 6']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{\text{d}}{\text{d}x}(\log_{9}x+6\ln x) \\ &=\frac{\text{d}}{\text{d}x}(\log_{9}x)+6\frac{\text{d}}{\text{d}x}(\ln x) \\ &=\frac{1}{x\ln 9}+\frac{6}{x}\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}\big|_{x=1}&=\left(\frac{1}{x \ln{\left(9 \right)}} + \frac{6}{x}\right)\big|_{x=1} \\ &=\frac{1}{\ln{\left(9 \right)}} + 6\,.\end{aligned}
$$

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

raw_parameterized_replay

Given that $y=4{e}^{x}-3{log}_{7}x$, find the slope of the tangent at $x=3.$

[]

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=4{e}^{x}-\frac{3}{x\operatorname{ln}7}\,.
$$

Therefore, the slope  of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(4{e}^{x}-\frac{3}{x\operatorname{ln}7})|}_{x=3} \\  & =4{e}^{3}-\frac{3}{3\operatorname{ln}7} \\  & =4{e}^{3}-\frac{1}{\operatorname{ln}7}\,.\end{aligned}
$$

normal_at_original

Given that $y=4{e}^{x}-3{log}_{7}x$, find the slope of the tangent at $x=3.$

{{field-1}}

['- \\frac{1}{\\ln{\\left(7 \\right)}} + 4 e^{3}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=4{e}^{x}-\frac{3}{x\operatorname{ln}7}\,.
$$

Therefore, the slope  of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(4{e}^{x}-\frac{3}{x\operatorname{ln}7})|}_{x=3} \\  & =4{e}^{3}-\frac{3}{3\operatorname{ln}7} \\  & =4{e}^{3}-\frac{1}{\operatorname{ln}7}\,.\end{aligned}
$$

normal_variant

Given that $y=9{e}^{x}-8{log}_{7}x$, find the slope of the tangent at $x=4.$

{{field-1}}

['- \\frac{2}{\\ln{\\left(7 \\right)}} + 9 e^{4}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=9{e}^{x}-\frac{8}{x\operatorname{ln}7}\,.
$$

Therefore, the slope  of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(9{e}^{x}-\frac{8}{x\operatorname{ln}7})|}_{x=4} \\  & =9{e}^{4}-\frac{8}{4\operatorname{ln}7} \\  & =9{e}^{4}-\frac{2}{\operatorname{ln}7}\,.\end{aligned}
$$

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

raw_parameterized_replay

Given the function $y=5{x}^{2}+6\operatorname{ln}x,$ the slope of the tangent line at $x=3$ is{{field-1}}.

['32']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(5{x}^{2}+6\operatorname{ln}x) \\  & =5\frac{\text{d}}{\text{d}x}({x}^{2})+6\frac{\text{d}}{\text{d}x}(\operatorname{ln}x) \\  & =5\cdot 2x+6\cdot \frac{1}{x} \\  & =10x+\frac{6}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(10x+\frac{6}{x})|}_{x=3} \\  & =10\cdot 3+\frac{6}{3} \\  & =32\,.\end{aligned}
$$

normal_at_original

Given the function $y=5{x}^{2}+6\operatorname{ln}x,$ the slope of the tangent line at $x=3$ is{{field-1}}.

['32']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(5{x}^{2}+6\operatorname{ln}x) \\  & =5\frac{\text{d}}{\text{d}x}({x}^{2})+6\frac{\text{d}}{\text{d}x}(\operatorname{ln}x) \\  & =5\cdot 2x+6\cdot \frac{1}{x} \\  & =10x+\frac{6}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(10x+\frac{6}{x})|}_{x=3} \\  & =10\cdot 3+\frac{6}{3} \\  & =32\,.\end{aligned}
$$

normal_variant

Given the function $y=9{x}^{2}+8\operatorname{ln}x,$ the slope of the tangent line at $x=4$ is{{field-1}}.

['74']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(9{x}^{2}+8\operatorname{ln}x) \\  & =9\frac{\text{d}}{\text{d}x}({x}^{2})+8\frac{\text{d}}{\text{d}x}(\operatorname{ln}x) \\  & =9\cdot 2x+8\cdot \frac{1}{x} \\  & =18x+\frac{8}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(18x+\frac{8}{x})|}_{x=4} \\  & =18\cdot 4+\frac{8}{4} \\  & =74\,.\end{aligned}
$$

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

raw_parameterized_replay

Given the function $y=5\operatorname{ln}x-2\cdot {3}^{x},$ the slope of the tangent line at $x=2$ is{{field-1}}.

['\\frac{5}{2}-18\\operatorname{ln}3']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(5\operatorname{ln}x-2\cdot {3}^{x}) \\  & =5\frac{\text{d}}{\text{d}x}(\operatorname{ln}x)-2\frac{\text{d}}{\text{d}x}({3}^{x}) \\  & =5\cdot \frac{1}{x}-2\cdot {3}^{x}\operatorname{ln}3 \\  & =\frac{5}{x}-2\operatorname{ln}3\cdot {3}^{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{5}{x}-2\operatorname{ln}3\cdot {3}^{x})|}_{x=2} \\  & =\frac{5}{2}-2\operatorname{ln}3\cdot {3}^{2} \\  & =\frac{5}{2}-18\operatorname{ln}3\,.\end{aligned}
$$

normal_at_original

Given the function $y=5\operatorname{ln}x-2\cdot {3}^{x},$ the slope of the tangent line at $x=2$ is{{field-1}}.

['\\frac{5}{2} - 18 \\ln{\\left(3 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(5\operatorname{ln}x-2\cdot {3}^{x}) \\  & =5\frac{\text{d}}{\text{d}x}(\operatorname{ln}x)-2\frac{\text{d}}{\text{d}x}({3}^{x}) \\  & =5\cdot \frac{1}{x}-2\cdot {3}^{x}\operatorname{ln}3 \\  & =\frac{5}{x}-2\operatorname{ln}3\cdot {3}^{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{5}{x}-2\operatorname{ln}3\cdot {3}^{x})|}_{x=2} \\  & =\frac{5}{2}-2\operatorname{ln}3\cdot {3}^{2} \\  & =\frac{5}{2}-18\operatorname{ln}3\,.\end{aligned}
$$

normal_variant

Given the function $y=9\operatorname{ln}x-8\cdot {7}^{x},$ the slope of the tangent line at $x=4$ is{{field-1}}.

['\\frac{9}{4} - 19208 \\ln{\\left(7 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(9\operatorname{ln}x-8\cdot {7}^{x}) \\  & =9\frac{\text{d}}{\text{d}x}(\operatorname{ln}x)-8\frac{\text{d}}{\text{d}x}({7}^{x}) \\  & =9\cdot \frac{1}{x}-8\cdot {7}^{x}\operatorname{ln}7 \\  & =\frac{9}{x}-8\operatorname{ln}7\cdot {7}^{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(\frac{9}{x}-8\operatorname{ln}7\cdot {7}^{x})|}_{x=4} \\  & =\frac{9}{4}-8\operatorname{ln}7\cdot {7}^{4} \\  & =\frac{9}{4}-19208\operatorname{ln}7\,.\end{aligned}
$$

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

raw_parameterized_replay

Given the function $y=-3{e}^{x}+2{log}_{4}x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

['-3e^2+\\frac{1}{\\ln4}', '-3{e}^{2}+\\frac{1}{\\operatorname{ln}4}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-3{e}^{x}+2{log}_{4}x) \\  & =-3\frac{\text{d}}{\text{d}x}({e}^{x})+2\frac{\text{d}}{\text{d}x}({log}_{4}x) \\  & =-3{e}^{x}+2\cdot \frac{1}{x\operatorname{ln}4} \\  & =-3{e}^{x}+\frac{2}{x\operatorname{ln}4}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(-3{e}^{x}+\frac{2}{x\operatorname{ln}4})|}_{x=2} \\  & =-3{e}^{2}+\frac{2}{2\cdot \operatorname{ln}4} \\  & =-3{e}^{2}+\frac{1}{\operatorname{ln}4}\,.\end{aligned}
$$

normal_at_original

Given the function $y=-3{e}^{x}+2{log}_{4}x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

['- 3 e^{2} + \\frac{1}{\\ln{\\left(4 \\right)}}', '- 3 e^{2} + \\frac{1}{\\operatorname{ln}{\\left(4 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-3{e}^{x}+2{log}_{4}x) \\  & =-3\frac{\text{d}}{\text{d}x}({e}^{x})+2\frac{\text{d}}{\text{d}x}({log}_{4}x) \\  & =-3{e}^{x}+2\cdot \frac{1}{x\operatorname{ln}4} \\  & =-3{e}^{x}+\frac{2}{x\operatorname{ln}4}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(-3{e}^{x}+\frac{2}{x\operatorname{ln}4})|}_{x=2} \\  & =-3{e}^{2}+\frac{2}{2\cdot \operatorname{ln}4} \\  & =-3{e}^{2}+\frac{1}{\operatorname{ln}4}\,.\end{aligned}
$$

normal_variant

Given the function $y=-9{e}^{x}+8{log}_{7}x,$ the slope of the tangent line at $x=4$ is{{field-1}}.

['- 9 e^{4} + \\frac{2}{\\ln{\\left(7 \\right)}}', '- 9 e^{4} + \\frac{2}{\\operatorname{ln}{\\left(7 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-9{e}^{x}+8{log}_{7}x) \\  & =-9\frac{\text{d}}{\text{d}x}({e}^{x})+8\frac{\text{d}}{\text{d}x}({log}_{7}x) \\  & =-9{e}^{x}+8\cdot \frac{1}{x\operatorname{ln}7} \\  & =-9{e}^{x}+\frac{8}{x\operatorname{ln}7}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(-9{e}^{x}+\frac{8}{x\operatorname{ln}7})|}_{x=4} \\  & =-9{e}^{4}+\frac{8}{4\cdot \operatorname{ln}7} \\  & =-9{e}^{4}+\frac{2}{\operatorname{ln}7}\,.\end{aligned}
$$

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

raw_parameterized_replay

Given that $y=2{log}_{2}x+{2}^{x}$, find the slope of the tangent at $x=2.$

[]

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{2}{x\operatorname{ln}2}+{2}^{x}\operatorname{ln}2\,.
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{2}{x\operatorname{ln}2}+{2}^{x}\operatorname{ln}2)|}_{x=2} \\  & =\frac{2}{2\cdot \operatorname{ln}2}+{2}^{2}\operatorname{ln}2 \\  & =\frac{1}{\operatorname{ln}2}+4\operatorname{ln}2\,.\end{aligned}
$$

normal_at_original

Given that $y=2{log}_{2}x+{2}^{x}$, find the slope of the tangent at $x=2.$

{{field-1}}

['\\frac{1}{\\ln{\\left(2 \\right)}} + 4 \\ln{\\left(2 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{2}{x\operatorname{ln}2}+{2}^{x}\operatorname{ln}2\,.
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{2}{x\operatorname{ln}2}+{2}^{x}\operatorname{ln}2)|}_{x=2} \\  & =\frac{2}{2\cdot \operatorname{ln}2}+{2}^{2}\operatorname{ln}2 \\  & =\frac{1}{\operatorname{ln}2}+4\operatorname{ln}2\,.\end{aligned}
$$

normal_variant

Given that $y=9{log}_{9}x+{9}^{x}$, find the slope of the tangent at $x=4.$

{{field-1}}

['\\frac{9}{4 \\ln{\\left(9 \\right)}} + 6561 \\ln{\\left(9 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{9}{x\operatorname{ln}9}+{9}^{x}\operatorname{ln}9\,.
$$

Therefore, the slope of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(\frac{9}{x\operatorname{ln}9}+{9}^{x}\operatorname{ln}9)|}_{x=4} \\  & =\frac{9}{4\cdot \operatorname{ln}9}+{9}^{4}\operatorname{ln}9 \\  & =\frac{\frac{9}{4}}{\operatorname{ln}9}+6561\operatorname{ln}9\,.\end{aligned}
$$

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

raw_parameterized_replay

Given that $y=3x-5+8{log}_{2}⁡x$, find the slope of the tangent at $x=\frac{1}{ln⁡2}.$

['11', '3+8ln\u20612', '6', '8ln\u20612-2', '4']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3x-5+8{log}_{2}⁡x) \\  & =\frac{\text{d}}{\text{d}x}(3x)+\frac{\text{d}}{\text{d}x}(-5)+\frac{\text{d}}{\text{d}x}(8{log}_{2}⁡x) \\  & =3\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(5)+8\frac{\text{d}}{\text{d}x}({log}_{2}⁡x) \\  & =3-0+8\cdot \frac{1}{xln⁡2} \\  & =3+\frac{8}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{1}{ln⁡2}$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1/ln⁡2} & ={(3+\frac{8}{xln⁡2})|}_{x=1/ln⁡2} \\  & =3+\frac{8}{(\frac{1}{ln⁡2}\cdot ln⁡2)} \\  & =3+8 \\  & =11\,.\end{aligned}
$$

normal_at_original

Given that $y=3x-5+8{log}_{2}⁡x$, find the slope of the tangent at $x=\frac{1}{ln⁡2}.$

['3', '6', '11', '8', '3 + 8 \\ln{\\left(2 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3x-5+8{log}_{2}⁡x) \\  & =\frac{\text{d}}{\text{d}x}(3x)+\frac{\text{d}}{\text{d}x}(-5)+\frac{\text{d}}{\text{d}x}(8{log}_{2}⁡x) \\  & =3\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(5)+8\frac{\text{d}}{\text{d}x}({log}_{2}⁡x) \\  & =3-0+8\cdot \frac{1}{xln⁡2} \\  & =3+\frac{8}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{1}{ln⁡2}$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1/ln⁡2} & ={(3+\frac{8}{xln⁡2})|}_{x=1/ln⁡2} \\  & =3+\frac{8}{(\frac{1}{ln⁡2}\cdot ln⁡2)} \\  & =3+8 \\  & =11\,.\end{aligned}
$$

normal_variant

Given that $y=9x-8+6{log}_{8}⁡x$, find the slope of the tangent at $x=\frac{1}{ln⁡8}.$

['9', '6', '7', '15', '9 + 6 \\ln{\\left(8 \\right)}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(9x-8+6{log}_{8}⁡x) \\  & =\frac{\text{d}}{\text{d}x}(9x)+\frac{\text{d}}{\text{d}x}(-8)+\frac{\text{d}}{\text{d}x}(6{log}_{8}⁡x) \\  & =9\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(8)+6\frac{\text{d}}{\text{d}x}({log}_{8}⁡x) \\  & =9-0+6\cdot \frac{1}{xln⁡8} \\  & =9+\frac{6}{xln⁡8}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{1}{ln⁡8}$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1/ln⁡8} & ={(9+\frac{6}{xln⁡8})|}_{x=1/ln⁡8} \\  & =9+\frac{6}{(\frac{1}{ln⁡8}\cdot ln⁡8)} \\  & =9+6 \\  & =15\,.\end{aligned}
$$

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

raw_parameterized_replay

Given that $y=3ln⁡x+2{x}^{2}-5x$, find the slope of the tangent at $x=1.$

['-2', '-3', '-5', '12', '2']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3ln⁡x+2{x}^{2}-5x) \\  & =\frac{\text{d}}{\text{d}x}(3ln⁡x)+\frac{\text{d}}{\text{d}x}(2{x}^{2})-\frac{\text{d}}{\text{d}x}(5x) \\  & =3\frac{\text{d}}{\text{d}x}(ln⁡x)+\frac{\text{d}}{\text{d}x}(2{x}^{2})-\frac{\text{d}}{\text{d}x}(5x) \\  & =3\cdot \frac{1}{x}+4x-5 \\  & =\frac{3}{x}+4x-5\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{3}{x}+4x-5)|}_{x=1} \\  & =\frac{3}{1}+4\cdot 1-5 \\  & =3+4-5 \\  & =2\,.\end{aligned}
$$

normal_at_original

Given that $y=3ln⁡x+2{x}^{2}-5x$, find the slope of the tangent at $x=1.$

['12', '-1', '2', '-4', '0']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3ln⁡x+2{x}^{2}-5x) \\  & =\frac{\text{d}}{\text{d}x}(3ln⁡x)+\frac{\text{d}}{\text{d}x}(2{x}^{2})-\frac{\text{d}}{\text{d}x}(5x) \\  & =3\frac{\text{d}}{\text{d}x}(ln⁡x)+\frac{\text{d}}{\text{d}x}(2{x}^{2})-\frac{\text{d}}{\text{d}x}(5x) \\  & =3\cdot \frac{1}{x}+4x-5 \\  & =\frac{3}{x}+4x-5\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{3}{x}+4x-5)|}_{x=1} \\  & =\frac{3}{1}+4\cdot 1-5 \\  & =3+4-5 \\  & =2\,.\end{aligned}
$$

normal_variant

Given that $y=9ln⁡x+8{x}^{2}-6x$, find the slope of the tangent at $x=1.$

['31', '1', '10', '19', '11']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(9ln⁡x+8{x}^{2}-6x) \\  & =\frac{\text{d}}{\text{d}x}(9ln⁡x)+\frac{\text{d}}{\text{d}x}(8{x}^{2})-\frac{\text{d}}{\text{d}x}(6x) \\  & =9\frac{\text{d}}{\text{d}x}(ln⁡x)+\frac{\text{d}}{\text{d}x}(8{x}^{2})-\frac{\text{d}}{\text{d}x}(6x) \\  & =9\cdot \frac{1}{x}+16x-6 \\  & =\frac{9}{x}+16x-6\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{9}{x}+16x-6)|}_{x=1} \\  & =\frac{9}{1}+16\cdot 1-6 \\  & =9+16-6 \\  & =19\,.\end{aligned}
$$

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

raw_parameterized_replay

Given the function $y=2{x}^{3}-5{log}_{3}⁡x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

['24-\\frac{5}{2\\operatorname{ln}3}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2{x}^{3}-5{log}_{3}⁡x) \\  & =2\frac{\text{d}}{\text{d}x}({x}^{3})-5\frac{\text{d}}{\text{d}x}({log}_{3}⁡x) \\  & =2\cdot 3{x}^{2}-5\cdot \frac{1}{xln⁡3} \\  & =6{x}^{2}-\frac{5}{xln⁡3}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(6{x}^{2}-\frac{5}{xln⁡3})|}_{x=2} \\  & =6(2)^{2}-\frac{5}{2ln⁡3} \\  & =24-\frac{5}{2ln⁡3}\,.\end{aligned}
$$

normal_at_original

Given the function $y=2{x}^{3}-5{log}_{3}⁡x,$ the slope of the tangent line at $x=2$ is{{field-1}}.

['24 - \\frac{5}{2 \\ln{\\left(3 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2{x}^{3}-5{log}_{3}⁡x) \\  & =2\frac{\text{d}}{\text{d}x}({x}^{3})-5\frac{\text{d}}{\text{d}x}({log}_{3}⁡x) \\  & =2\cdot 3{x}^{2}-5\cdot \frac{1}{xln⁡3} \\  & =6{x}^{2}-\frac{5}{xln⁡3}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(6{x}^{2}-\frac{5}{xln⁡3})|}_{x=2} \\  & =6(2)^{2}-\frac{5}{2ln⁡3} \\  & =24-\frac{5}{2ln⁡3}\,.\end{aligned}
$$

normal_variant

Given the function $y=9{x}^{3}-8{log}_{7}⁡x,$ the slope of the tangent line at $x=4$ is{{field-1}}.

['432 - \\frac{2}{\\ln{\\left(7 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(9{x}^{3}-8{log}_{7}⁡x) \\  & =9\frac{\text{d}}{\text{d}x}({x}^{3})-8\frac{\text{d}}{\text{d}x}({log}_{7}⁡x) \\  & =9\cdot 3{x}^{2}-8\cdot \frac{1}{xln⁡7} \\  & =27{x}^{2}-\frac{8}{xln⁡7}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(27{x}^{2}-\frac{8}{xln⁡7})|}_{x=4} \\  & =27(4)^{2}-\frac{8}{4ln⁡7} \\  & =432-\frac{8}{4ln⁡7}\,.\end{aligned}
$$

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

raw_parameterized_replay

Given the function $y=6{log}_{2}⁡x+4{x}^{2}-3x,$ the slope of the tangent line at $x=1$ is{{field-1}}.

['\\frac{6}{\\operatorname{ln}2}+5']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(6{log}_{2}⁡x+4{x}^{2}-3x) \\  & =6\frac{\text{d}}{\text{d}x}({log}_{2}⁡x)+4\frac{\text{d}}{\text{d}x}({x}^{2})-3\frac{\text{d}}{\text{d}x}(x) \\  & =6\cdot \frac{1}{xln⁡2}+4\cdot 2x-3 \\  & =\frac{6}{xln⁡2}+8x-3\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{6}{xln⁡2}+8x-3)|}_{x=1} \\  & =\frac{6}{1\cdot ln⁡2}+8(1)-3 \\  & =\frac{6}{ln⁡2}+5\,.\end{aligned}
$$

normal_at_original

Given the function $y=6{log}_{2}⁡x+4{x}^{2}-3x,$ the slope of the tangent line at $x=1$ is{{field-1}}.

['5 + \\frac{6}{\\ln{\\left(2 \\right)}}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(6{log}_{2}⁡x+4{x}^{2}-3x) \\  & =6\frac{\text{d}}{\text{d}x}({log}_{2}⁡x)+4\frac{\text{d}}{\text{d}x}({x}^{2})-3\frac{\text{d}}{\text{d}x}(x) \\  & =6\cdot \frac{1}{xln⁡2}+4\cdot 2x-3 \\  & =\frac{6}{xln⁡2}+8x-3\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{6}{xln⁡2}+8x-3)|}_{x=1} \\  & =\frac{6}{1\cdot ln⁡2}+8(1)-3 \\  & =\frac{6}{ln⁡2}+5\,.\end{aligned}
$$

normal_variant

Given the function $y=9{log}_{8}⁡x+8{x}^{2}-6x,$ the slope of the tangent line at $x=1$ is{{field-1}}.

['\\frac{9}{\\ln{\\left(8 \\right)}} + 10']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(9{log}_{8}⁡x+8{x}^{2}-6x) \\  & =9\frac{\text{d}}{\text{d}x}({log}_{8}⁡x)+8\frac{\text{d}}{\text{d}x}({x}^{2})-6\frac{\text{d}}{\text{d}x}(x) \\  & =9\cdot \frac{1}{xln⁡8}+8\cdot 2x-6 \\  & =\frac{9}{xln⁡8}+16x-6\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{9}{xln⁡8}+16x-6)|}_{x=1} \\  & =\frac{9}{1\cdot ln⁡8}+16(1)-6 \\  & =\frac{9}{ln⁡8}+10\,.\end{aligned}
$$

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

raw_parameterized_replay

Given the function $y=4{e}^{x}-3{log}_{2}⁡x+7,$ the slope of the tangent line at $x=3$ is{{field-1}}.

['4{e}^{3}-\\frac{1}{\\operatorname{ln}2}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(4{e}^{x}-3{log}_{2}⁡x+7) \\  & =4\frac{\text{d}}{\text{d}x}({e}^{x})-3\frac{\text{d}}{\text{d}x}({log}_{2}⁡x)+\frac{\text{d}}{\text{d}x}(7) \\  & =4{e}^{x}-3\cdot \frac{1}{xln⁡2}+0 \\  & =4{e}^{x}-\frac{3}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(4{e}^{x}-\frac{3}{xln⁡2})|}_{x=3} \\  & =4{e}^{3}-\frac{3}{3\cdot ln⁡2} \\  & =4{e}^{3}-\frac{1}{ln⁡2}\,.\end{aligned}
$$

normal_at_original

Given the function $y=4{e}^{x}-3{log}_{2}⁡x+7,$ the slope of the tangent line at $x=3$ is{{field-1}}.

['- \\frac{1}{\\ln{\\left(2 \\right)}} + 4 e^{3}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(4{e}^{x}-3{log}_{2}⁡x+7) \\  & =4\frac{\text{d}}{\text{d}x}({e}^{x})-3\frac{\text{d}}{\text{d}x}({log}_{2}⁡x)+\frac{\text{d}}{\text{d}x}(7) \\  & =4{e}^{x}-3\cdot \frac{1}{xln⁡2}+0 \\  & =4{e}^{x}-\frac{3}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(4{e}^{x}-\frac{3}{xln⁡2})|}_{x=3} \\  & =4{e}^{3}-\frac{3}{3\cdot ln⁡2} \\  & =4{e}^{3}-\frac{1}{ln⁡2}\,.\end{aligned}
$$

normal_variant

Given the function $y=9{e}^{x}-8{log}_{7}⁡x+9,$ the slope of the tangent line at $x=4$ is{{field-1}}.

['- \\frac{2}{\\ln{\\left(7 \\right)}} + 9 e^{4}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(9{e}^{x}-8{log}_{7}⁡x+9) \\  & =9\frac{\text{d}}{\text{d}x}({e}^{x})-8\frac{\text{d}}{\text{d}x}({log}_{7}⁡x)+\frac{\text{d}}{\text{d}x}(9) \\  & =9{e}^{x}-8\cdot \frac{1}{xln⁡7}+0 \\  & =9{e}^{x}-\frac{8}{xln⁡7}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(9{e}^{x}-\frac{8}{xln⁡7})|}_{x=4} \\  & =9{e}^{4}-\frac{8}{4\cdot ln⁡7} \\  & =9{e}^{4}-\frac{2}{ln⁡7}\,.\end{aligned}
$$

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

raw_parameterized_replay

Given that $y=3\operatorname{log}⁡x+{x}^{3}-4$, find the slope of the tangent at $x=3.$

['\\frac{1}{3\\operatorname{ln}\u206110}+3', '\\frac{1}{\\operatorname{ln}\u206110}+27', '\\frac{3}{\\operatorname{ln}\u206110}+9', '\\frac{1}{\\operatorname{ln}\u206110}-9', '\\frac{9}{\\operatorname{ln}\u206110}-3']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{3}{x\operatorname{ln}⁡10}+3{x}^{2}\,.
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(\frac{3}{x\operatorname{ln}⁡10}+3{x}^{2})|}_{x=3} \\  & =\frac{3}{3\cdot \operatorname{ln}⁡10}+3\cdot {3}^{2} \\  & =\frac{1}{\operatorname{ln}⁡10}+27\,.\end{aligned}
$$

normal_at_original

Given that $y=3\operatorname{log}⁡x+{x}^{3}-4$, find the slope of the tangent at $x=3.$

['28', '27', '\\frac{1}{\\ln{\\left(10 \\right)}} + 27', '\\frac{1}{\\ln{\\left(10 \\right)}} + 9', '\\frac{3}{\\ln{\\left(10 \\right)}} + 27']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{3}{x\operatorname{ln}⁡10}+3{x}^{2}\,.
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(\frac{3}{x\operatorname{ln}⁡10}+3{x}^{2})|}_{x=3} \\  & =\frac{3}{3\cdot \operatorname{ln}⁡10}+3\cdot {3}^{2} \\  & =\frac{1}{\operatorname{ln}⁡10}+27\,.\end{aligned}
$$

normal_variant

Given that $y=9\operatorname{log}⁡x+{x}^{3}-8$, find the slope of the tangent at $x=4.$

['\\frac{201}{4}', '\\frac{9}{4 \\ln{\\left(10 \\right)}} + 16', '48', '\\frac{9}{4 \\ln{\\left(10 \\right)}} + 48', '\\frac{9}{\\ln{\\left(10 \\right)}} + 48']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{9}{x\operatorname{ln}⁡10}+3{x}^{2}\,.
$$

Therefore, the slope of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(\frac{9}{x\operatorname{ln}⁡10}+3{x}^{2})|}_{x=4} \\  & =\frac{9}{4\cdot \operatorname{ln}⁡10}+3\cdot {4}^{2} \\  & =\frac{\frac{9}{4}}{\operatorname{ln}⁡10}+48\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-17373

Given that $y =-\frac{1}{4}\ln x$, find the slope of the tangent at $x = 1$.

['-\\frac{1}{4}', '\\frac{4}{1}', '-\\frac{4}{1}', '\\frac{1}{4}', '0']

Source solution omitted.

## Changed-parameter evidence profile raw:q-17395

Given that $y = \log_{2} x + 4\ln x$, find the slope of the tangent at $x = 1$.

['\\frac{4}{\\ln 2}', '\\frac{1}{\\ln 2} + 4', '\\frac{1}{\\ln 2}', '0', '\\ln 2 + 4']

Source solution omitted.

## Changed-parameter evidence profile raw:q-101723

Given that $y=1{e}^{x}-4{log}_{2}x$, find the slope of the tangent at $x=3.$

[]

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=1{e}^{x}-\frac{4}{x\operatorname{ln}2}\,.
$$

Therefore, the slope  of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(1{e}^{x}-\frac{4}{x\operatorname{ln}2})|}_{x=3} \\  & =1{e}^{3}-\frac{4}{3\operatorname{ln}2} \\  & =1{e}^{3}-\frac{\frac{4}{3}}{\operatorname{ln}2}\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-340014

Given the function $y=1{x}^{2}+4\operatorname{ln}x,$ the slope of the tangent line at $x=1$ is{{field-1}}.

['6']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(1{x}^{2}+4\operatorname{ln}x) \\  & =1\frac{\text{d}}{\text{d}x}({x}^{2})+4\frac{\text{d}}{\text{d}x}(\operatorname{ln}x) \\  & =1\cdot 2x+4\cdot \frac{1}{x} \\  & =2x+\frac{4}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(2x+\frac{4}{x})|}_{x=1} \\  & =2\cdot 1+\frac{4}{1} \\  & =6\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-340022

Given the function $y=1\operatorname{ln}x-4\cdot {2}^{x},$ the slope of the tangent line at $x=3$ is{{field-1}}.

['\\frac{1}{3}-32\\operatorname{ln}2']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(1\operatorname{ln}x-4\cdot {2}^{x}) \\  & =1\frac{\text{d}}{\text{d}x}(\operatorname{ln}x)-4\frac{\text{d}}{\text{d}x}({2}^{x}) \\  & =1\cdot \frac{1}{x}-4\cdot {2}^{x}\operatorname{ln}2 \\  & =\frac{1}{x}-4\operatorname{ln}2\cdot {2}^{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(\frac{1}{x}-4\operatorname{ln}2\cdot {2}^{x})|}_{x=3} \\  & =\frac{1}{3}-4\operatorname{ln}2\cdot {2}^{3} \\  & =\frac{1}{3}-32\operatorname{ln}2\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-340109

Given the function $y=-1{e}^{x}+4{log}_{2}x,$ the slope of the tangent line at $x=3$ is{{field-1}}.

['-1e^3+\\frac{\\frac{4}{3}}{\\ln2}', '-1{e}^{3}+\\frac{\\frac{4}{3}}{\\operatorname{ln}2}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-1{e}^{x}+4{log}_{2}x) \\  & =-1\frac{\text{d}}{\text{d}x}({e}^{x})+4\frac{\text{d}}{\text{d}x}({log}_{2}x) \\  & =-1{e}^{x}+4\cdot \frac{1}{x\operatorname{ln}2} \\  & =-1{e}^{x}+\frac{4}{x\operatorname{ln}2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(-1{e}^{x}+\frac{4}{x\operatorname{ln}2})|}_{x=3} \\  & =-1{e}^{3}+\frac{4}{3\cdot \operatorname{ln}2} \\  & =-1{e}^{3}+\frac{\frac{4}{3}}{\operatorname{ln}2}\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-70897

Given that $y=1{log}_{5}x+{5}^{x}$, find the slope of the tangent at $x=1.$

[]

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{1}{x\operatorname{ln}5}+{5}^{x}\operatorname{ln}5\,.
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{1}{x\operatorname{ln}5}+{5}^{x}\operatorname{ln}5)|}_{x=1} \\  & =\frac{1}{1\cdot \operatorname{ln}5}+{5}^{1}\operatorname{ln}5 \\  & =\frac{1}{\operatorname{ln}5}+5\operatorname{ln}5\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-101726

Given that $y=1x-4+12{log}_{2}⁡x$, find the slope of the tangent at $x=\frac{1}{ln⁡2}.$

['12ln\u20612-3', '9', '2', '13', '1+12ln\u20612']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(1x-4+12{log}_{2}⁡x) \\  & =\frac{\text{d}}{\text{d}x}(1x)+\frac{\text{d}}{\text{d}x}(-4)+\frac{\text{d}}{\text{d}x}(12{log}_{2}⁡x) \\  & =1\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(4)+12\frac{\text{d}}{\text{d}x}({log}_{2}⁡x) \\  & =1-0+12\cdot \frac{1}{xln⁡2} \\  & =1+\frac{12}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{1}{ln⁡2}$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1/ln⁡2} & ={(1+\frac{12}{xln⁡2})|}_{x=1/ln⁡2} \\  & =1+\frac{12}{(\frac{1}{ln⁡2}\cdot ln⁡2)} \\  & =1+12 \\  & =13\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-17371

Given that $y=3ln⁡x+10{x}^{2}-5x$, find the slope of the tangent at $x=1.$

['28', '-18', '-5', '18', '-3']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3ln⁡x+10{x}^{2}-5x) \\  & =\frac{\text{d}}{\text{d}x}(3ln⁡x)+\frac{\text{d}}{\text{d}x}(10{x}^{2})-\frac{\text{d}}{\text{d}x}(5x) \\  & =3\frac{\text{d}}{\text{d}x}(ln⁡x)+\frac{\text{d}}{\text{d}x}(10{x}^{2})-\frac{\text{d}}{\text{d}x}(5x) \\  & =3\cdot \frac{1}{x}+20x-5 \\  & =\frac{3}{x}+20x-5\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{3}{x}+20x-5)|}_{x=1} \\  & =\frac{3}{1}+20\cdot 1-5 \\  & =3+20-5 \\  & =18\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-340024

Given the function $y=1{x}^{3}-4{log}_{2}⁡x,$ the slope of the tangent line at $x=3$ is{{field-1}}.

['27-\\frac{4}{3\\operatorname{ln}2}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(1{x}^{3}-4{log}_{2}⁡x) \\  & =1\frac{\text{d}}{\text{d}x}({x}^{3})-4\frac{\text{d}}{\text{d}x}({log}_{2}⁡x) \\  & =1\cdot 3{x}^{2}-4\cdot \frac{1}{xln⁡2} \\  & =3{x}^{2}-\frac{4}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(3{x}^{2}-\frac{4}{xln⁡2})|}_{x=3} \\  & =3(3)^{2}-\frac{4}{3ln⁡2} \\  & =27-\frac{4}{3ln⁡2}\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-340026

Given the function $y=1{log}_{4}⁡x+12{x}^{2}-8x,$ the slope of the tangent line at $x=1$ is{{field-1}}.

['\\frac{1}{\\operatorname{ln}4}+16']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(1{log}_{4}⁡x+12{x}^{2}-8x) \\  & =1\frac{\text{d}}{\text{d}x}({log}_{4}⁡x)+12\frac{\text{d}}{\text{d}x}({x}^{2})-8\frac{\text{d}}{\text{d}x}(x) \\  & =1\cdot \frac{1}{xln⁡4}+12\cdot 2x-8 \\  & =\frac{1}{xln⁡4}+24x-8\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{1}{xln⁡4}+24x-8)|}_{x=1} \\  & =\frac{1}{1\cdot ln⁡4}+24(1)-8 \\  & =\frac{1}{ln⁡4}+16\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-340110

Given the function $y=1{e}^{x}-4{log}_{2}⁡x+3,$ the slope of the tangent line at $x=3$ is{{field-1}}.

['1{e}^{3}-\\frac{\\frac{4}{3}}{\\operatorname{ln}2}']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(1{e}^{x}-4{log}_{2}⁡x+3) \\  & =1\frac{\text{d}}{\text{d}x}({e}^{x})-4\frac{\text{d}}{\text{d}x}({log}_{2}⁡x)+\frac{\text{d}}{\text{d}x}(3) \\  & =1{e}^{x}-4\cdot \frac{1}{xln⁡2}+0 \\  & =1{e}^{x}-\frac{4}{xln⁡2}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(1{e}^{x}-\frac{4}{xln⁡2})|}_{x=3} \\  & =1{e}^{3}-\frac{4}{3\cdot ln⁡2} \\  & =1{e}^{3}-\frac{\frac{4}{3}}{ln⁡2}\,.\end{aligned}
$$

## Changed-parameter evidence profile raw:q-70903

Given that $y=12\operatorname{log}⁡x+{x}^{3}-8$, find the slope of the tangent at $x=2.$

['\\frac{12}{\\operatorname{ln}\u206110}+4', '\\frac{6}{2\\operatorname{ln}\u206110}+2', '\\frac{6}{\\operatorname{ln}\u206110}+12', '\\frac{6}{\\operatorname{ln}\u206110}-4', '\\frac{24}{\\operatorname{ln}\u206110}-2']

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{12}{x\operatorname{ln}⁡10}+3{x}^{2}\,.
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{12}{x\operatorname{ln}⁡10}+3{x}^{2})|}_{x=2} \\  & =\frac{12}{2\cdot \operatorname{ln}⁡10}+3\cdot {2}^{2} \\  & =\frac{6}{\operatorname{ln}⁡10}+12\,.\end{aligned}
$$

## Authored/default easy

Given that $y=1{log}_{8}x+{8}^{x}$, find the slope of the tangent at $x=1.$

{{field-1}}

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{1}{x\operatorname{ln}8}+{8}^{x}\operatorname{ln}8\,.
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{1}{x\operatorname{ln}8}+{8}^{x}\operatorname{ln}8)|}_{x=1} \\  & =\frac{1}{1\cdot \operatorname{ln}8}+{8}^{1}\operatorname{ln}8 \\  & =\frac{1}{\operatorname{ln}8}+8\operatorname{ln}8\,.\end{aligned}
$$

## Authored/default easy

Given the function $y=6{x}^{3}-12{log}_{5}⁡x,$ the slope of the tangent line at $x=3$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(6{x}^{3}-12{log}_{5}⁡x) \\  & =6\frac{\text{d}}{\text{d}x}({x}^{3})-12\frac{\text{d}}{\text{d}x}({log}_{5}⁡x) \\  & =6\cdot 3{x}^{2}-12\cdot \frac{1}{xln⁡5} \\  & =18{x}^{2}-\frac{12}{xln⁡5}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=3$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=3} & ={(18{x}^{2}-\frac{12}{xln⁡5})|}_{x=3} \\  & =18(3)^{2}-\frac{12}{3ln⁡5} \\  & =162-\frac{12}{3ln⁡5}\,.\end{aligned}
$$

## Authored/default moderate

Given that $y=1ln⁡x+7{x}^{2}-3x$, find the slope of the tangent at $x=2.$

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(1ln⁡x+7{x}^{2}-3x) \\  & =\frac{\text{d}}{\text{d}x}(1ln⁡x)+\frac{\text{d}}{\text{d}x}(7{x}^{2})-\frac{\text{d}}{\text{d}x}(3x) \\  & =1\frac{\text{d}}{\text{d}x}(ln⁡x)+\frac{\text{d}}{\text{d}x}(7{x}^{2})-\frac{\text{d}}{\text{d}x}(3x) \\  & =1\cdot \frac{1}{x}+14x-3 \\  & =\frac{1}{x}+14x-3\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{1}{x}+14x-3)|}_{x=2} \\  & =\frac{1}{2}+14\cdot 2-3 \\  & =\frac{1}{2}+28-3 \\  & =\frac{51}{2}\,.\end{aligned}
$$

## Authored/default moderate

Given that $y=4ln⁡x+1{x}^{2}-6x$, find the slope of the tangent at $x=4.$

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(4ln⁡x+1{x}^{2}-6x) \\  & =\frac{\text{d}}{\text{d}x}(4ln⁡x)+\frac{\text{d}}{\text{d}x}(1{x}^{2})-\frac{\text{d}}{\text{d}x}(6x) \\  & =4\frac{\text{d}}{\text{d}x}(ln⁡x)+\frac{\text{d}}{\text{d}x}(1{x}^{2})-\frac{\text{d}}{\text{d}x}(6x) \\  & =4\cdot \frac{1}{x}+2x-6 \\  & =\frac{4}{x}+2x-6\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=4$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=4} & ={(\frac{4}{x}+2x-6)|}_{x=4} \\  & =\frac{4}{4}+2\cdot 4-6 \\  & =1+8-6 \\  & =3\,.\end{aligned}
$$

## Authored/default hard

Given the function $y=1{log}_{2}⁡x+7{x}^{2}-3x,$ the slope of the tangent line at $x=\frac{2}{\ln{\left(2 \right)}}$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(1{log}_{2}⁡x+7{x}^{2}-3x) \\  & =1\frac{\text{d}}{\text{d}x}({log}_{2}⁡x)+7\frac{\text{d}}{\text{d}x}({x}^{2})-3\frac{\text{d}}{\text{d}x}(x) \\  & =1\cdot \frac{1}{xln⁡2}+7\cdot 2x-3 \\  & =\frac{1}{xln⁡2}+14x-3\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{2}{\ln{\left(2 \right)}}$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=\frac{2}{\ln{\left(2 \right)}}} & ={(\frac{1}{xln⁡2}+14x-3)|}_{x=\frac{2}{\ln{\left(2 \right)}}} \\  & =\frac{1}{\frac{2}{\ln{\left(2 \right)}}\cdot ln⁡2}+14(\frac{2}{\ln{\left(2 \right)}})-3 \\  & =- \frac{5}{2} + \frac{28}{\ln{\left(2 \right)}}\,.\end{aligned}
$$

## Authored/default hard

Given the function $y=4{log}_{7}⁡x+1{x}^{2}-6x,$ the slope of the tangent line at $x=\frac{4}{\ln{\left(7 \right)}}$ is{{field-1}}.

To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(4{log}_{7}⁡x+1{x}^{2}-6x) \\  & =4\frac{\text{d}}{\text{d}x}({log}_{7}⁡x)+1\frac{\text{d}}{\text{d}x}({x}^{2})-6\frac{\text{d}}{\text{d}x}(x) \\  & =4\cdot \frac{1}{xln⁡7}+1\cdot 2x-6 \\  & =\frac{4}{xln⁡7}+2x-6\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{4}{\ln{\left(7 \right)}}$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=\frac{4}{\ln{\left(7 \right)}}} & ={(\frac{4}{xln⁡7}+2x-6)|}_{x=\frac{4}{\ln{\left(7 \right)}}} \\  & =\frac{4}{\frac{4}{\ln{\left(7 \right)}}\cdot ln⁡7}+2(\frac{4}{\ln{\left(7 \right)}})-6 \\  & =-5 + \frac{8}{\ln{\left(7 \right)}}\,.\end{aligned}
$$
