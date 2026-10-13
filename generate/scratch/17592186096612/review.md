# Review

Raw source evidence is source.json. Original replay is labeled separately from authored variants.


## original replay q-11732 (authored solution; source absent)

Given that $f(x) = 5 \cdot 2^{x}$, find $f^{′}(x)$.

- $f^{′}(x) = 5 \cdot 2^{x}$

- $f^{′}(x) = \frac{5 \cdot 2^{x}}{\ln 2}$

- $f^{′}(x) = \frac{5\ln 2}{2^{x}}$

- $f^{′}(x) = 5\ln 2 \cdot 2^{x}$ (correct)

Applying the formula, we get

$$
\begin{aligned}f^{′}(x)&=\frac{\text{d}}{\text{d}x}(5 \cdot 2^{x}) \\ &=5\frac{\text{d}}{\text{d}x}(2^{x}) \\ &=5\cdot 2^{x}\ln 2 \\ &=5\ln 2\cdot 2^{x}.\end{aligned}
$$


## generated variant q-11732

Given that $f(x) = 1 \cdot 9^{x}$, find $f^{′}(x)$.

- $f^{′}(x) = \frac{1\ln 9}{9^{x}}$

- $f^{′}(x) = 1\ln 9 \cdot 9^{x}$ (correct)

- $f^{′}(x) = \frac{1 \cdot 9^{x}}{\ln 9}$

- $f^{′}(x) = 1 \cdot 9^{x}$

Applying the formula, we get

$$
\begin{aligned}f^{′}(x)&=\frac{\text{d}}{\text{d}x}(1 \cdot 9^{x}) \\ &=1\frac{\text{d}}{\text{d}x}(9^{x}) \\ &=1\cdot 9^{x}\ln 9 \\ &=1\ln 9\cdot 9^{x}.\end{aligned}
$$


## generated variant q-11732

Given that $f(x) = 10 \cdot 4^{x}$, find $f^{′}(x)$.

- $f^{′}(x) = \frac{10\ln 4}{4^{x}}$

- $f^{′}(x) = \frac{10 \cdot 4^{x}}{\ln 4}$

- $f^{′}(x) = 10\ln 4 \cdot 4^{x}$ (correct)

- $f^{′}(x) = 10 \cdot 4^{x}$

Applying the formula, we get

$$
\begin{aligned}f^{′}(x)&=\frac{\text{d}}{\text{d}x}(10 \cdot 4^{x}) \\ &=10\frac{\text{d}}{\text{d}x}(4^{x}) \\ &=10\cdot 4^{x}\ln 4 \\ &=10\ln 4\cdot 4^{x}.\end{aligned}
$$


## original replay q-1917 (authored solution; source absent)

Given that $f(x) = 4^{x} + 3e^{x}$, find $f^{′}(x)$.

- $f^{′}(x) = 4^{x} - \ln 4 + 3e^{x}$

- $f^{′}(x) = 4^{x}\ln 4 + 3e^{x}$ (correct)

- $f^{′}(x) = \ln 4 + 3e^{x}$

- $f^{′}(x) = 4^{x} + 3e^{x}$

- $f^{′}(x) = 4^{x}\ln x + 3e^{x}$

Applying the formula, we get

$$
\begin{aligned}f^{′}(x)&=\frac{\text{d}}{\text{d}x}(4^{x}+3e^{x}) \\ &=\frac{\text{d}}{\text{d}x}(4^{x})+\frac{\text{d}}{\text{d}x}(3e^{x}) \\ &=\frac{\text{d}}{\text{d}x}(4^{x})+3\frac{\text{d}}{\text{d}x}(e^{x}) \\ &=4^{x}\ln 4+3e^{x}.\end{aligned}
$$


## generated variant q-1917

Given that $f(x) = 2^{x} + 8e^{x}$, find $f^{′}(x)$.

- $f^{′}(x) = \ln 2 + 8e^{x}$

- $f^{′}(x) = 2^{x} - \ln 2 + 8e^{x}$

- $f^{′}(x) = 2^{x} + 8e^{x}$

- $f^{′}(x) = 2^{x}\ln x + 8e^{x}$

- $f^{′}(x) = 2^{x}\ln 2 + 8e^{x}$ (correct)

Applying the formula, we get

$$
\begin{aligned}f^{′}(x)&=\frac{\text{d}}{\text{d}x}(2^{x}+8e^{x}) \\ &=\frac{\text{d}}{\text{d}x}(2^{x})+\frac{\text{d}}{\text{d}x}(8e^{x}) \\ &=\frac{\text{d}}{\text{d}x}(2^{x})+8\frac{\text{d}}{\text{d}x}(e^{x}) \\ &=2^{x}\ln 2+8e^{x}.\end{aligned}
$$


## generated variant q-1917

Given that $f(x) = 4^{x} + 2e^{x}$, find $f^{′}(x)$.

- $f^{′}(x) = 4^{x}\ln 4 + 2e^{x}$ (correct)

- $f^{′}(x) = 4^{x} - \ln 4 + 2e^{x}$

- $f^{′}(x) = 4^{x} + 2e^{x}$

- $f^{′}(x) = 4^{x}\ln x + 2e^{x}$

- $f^{′}(x) = \ln 4 + 2e^{x}$

Applying the formula, we get

$$
\begin{aligned}f^{′}(x)&=\frac{\text{d}}{\text{d}x}(4^{x}+2e^{x}) \\ &=\frac{\text{d}}{\text{d}x}(4^{x})+\frac{\text{d}}{\text{d}x}(2e^{x}) \\ &=\frac{\text{d}}{\text{d}x}(4^{x})+2\frac{\text{d}}{\text{d}x}(e^{x}) \\ &=4^{x}\ln 4+2e^{x}.\end{aligned}
$$


## original replay q-11735

Given that $f(x)={6}^{x}-5{x}^{2}+6x-19$, find ${f}^{′}(x).$

- ${6}^{x}ln⁡6-10x+6$ (correct)

- ${6}^{x}ln⁡6-10{x}^{2}+6x$

- ${6}^{x}-10{x}^{2}+6x-19$

- ${6}^{x}ln⁡6-10{x}^{2}+6x-19$

- ${6}^{x}-10x+6$

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({6}^{x}-5{x}^{2}+6x-19) \\  & =\frac{\text{d}}{\text{d}x}({6}^{x})-\frac{\text{d}}{\text{d}x}(5{x}^{2})+\frac{\text{d}}{\text{d}x}(6x)-\frac{\text{d}}{\text{d}x}(19) \\  & =\frac{\text{d}}{\text{d}x}({6}^{x})-5\frac{\text{d}}{\text{d}x}({x}^{2})+6\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(19) \\  & =ln⁡6\cdot {6}^{x}-5(2x)+6(1)-0 \\  & ={6}^{x}ln⁡6-10x+6.\end{aligned}
$$


## generated variant q-11735

Given that $f(x)={2}^{x}-8{x}^{2}+2x-13$, find ${f}^{′}(x).$

- ${2}^{x}\ln 2-16{x}^{2}+2x-13$

- ${2}^{x}\ln 2-16x+2$ (correct)

- ${2}^{x}-16x+2$

- ${2}^{x}\ln 2-16{x}^{2}+2x$

- ${2}^{x}-16{x}^{2}+2x-13$

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({2}^{x}-8{x}^{2}+2x-13) \\  & =\frac{\text{d}}{\text{d}x}({2}^{x})-\frac{\text{d}}{\text{d}x}(8{x}^{2})+\frac{\text{d}}{\text{d}x}(2x)-\frac{\text{d}}{\text{d}x}(13) \\  & =\frac{\text{d}}{\text{d}x}({2}^{x})-8\frac{\text{d}}{\text{d}x}({x}^{2})+2\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(13) \\  & =\ln 2\cdot {2}^{x}-8(2x)+2(1)-0 \\  & ={2}^{x}\ln 2-16x+2.\end{aligned}
$$


## generated variant q-11735

Given that $f(x)={4}^{x}-2{x}^{2}+4x-15$, find ${f}^{′}(x).$

- ${4}^{x}-4{x}^{2}+4x-15$

- ${4}^{x}-4x+4$

- ${4}^{x}\ln 4-4{x}^{2}+4x$

- ${4}^{x}\ln 4-4{x}^{2}+4x-15$

- ${4}^{x}\ln 4-4x+4$ (correct)

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({4}^{x}-2{x}^{2}+4x-15) \\  & =\frac{\text{d}}{\text{d}x}({4}^{x})-\frac{\text{d}}{\text{d}x}(2{x}^{2})+\frac{\text{d}}{\text{d}x}(4x)-\frac{\text{d}}{\text{d}x}(15) \\  & =\frac{\text{d}}{\text{d}x}({4}^{x})-2\frac{\text{d}}{\text{d}x}({x}^{2})+4\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(15) \\  & =\ln 4\cdot {4}^{x}-2(2x)+4(1)-0 \\  & ={4}^{x}\ln 4-4x+4.\end{aligned}
$$


## original replay q-17388

Given that $f(x)={3}^{x}+5{e}^{x}$, find the instantaneous rate of change at $x=0.$

- $ln⁡3+5e$

- $6$

- $ln⁡3+5$ (correct)

- $5$

- $ln⁡3$

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({3}^{x}+5{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({3}^{x})+\frac{\text{d}y}{\text{d}x}(5{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({3}^{x})+5\frac{\text{d}y}{\text{d}x}({e}^{x}) \\  & ={3}^{x}ln⁡3+5{e}^{x}\,.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={({3}^{x}ln⁡3+5{e}^{x})|}_{x=0} \\  & ={3}^{0}ln⁡3+5{e}^{0} \\  & =1\cdot ln⁡3+5\cdot 1 \\  & =ln⁡3+5.\end{aligned}
$$


## generated variant q-17388

Given that $f(x)={2}^{x}+8{e}^{x}$, find the instantaneous rate of change at $x=0.$

- $\ln 2+8$ (correct)

- $\ln 2+8e$

- $8$

- $\ln 2$

- $9$

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({2}^{x}+8{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({2}^{x})+\frac{\text{d}}{\text{d}x}(8{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({2}^{x})+8\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & ={2}^{x}\ln 2+8{e}^{x}\,.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={({2}^{x}\ln 2+8{e}^{x})|}_{x=0} \\  & ={2}^{0}\ln 2+8{e}^{0} \\  & =1\cdot \ln 2+8\cdot 1 \\  & =\ln 2+8.\end{aligned}
$$


## generated variant q-17388

Given that $f(x)={4}^{x}+2{e}^{x}$, find the instantaneous rate of change at $x=0.$

- $3$

- $\ln 4+2e$

- $2$

- $\ln 4$

- $\ln 4+2$ (correct)

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({4}^{x}+2{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({4}^{x})+\frac{\text{d}}{\text{d}x}(2{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({4}^{x})+2\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & ={4}^{x}\ln 4+2{e}^{x}\,.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={({4}^{x}\ln 4+2{e}^{x})|}_{x=0} \\  & ={4}^{0}\ln 4+2{e}^{0} \\  & =1\cdot \ln 4+2\cdot 1 \\  & =\ln 4+2.\end{aligned}
$$


## original replay q-304038

Given that $f(x)=3\cdot {8}^{x}+12x+10$, find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}}

- $3\operatorname{ln}(8){8}^{x}+12$ (correct)

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3\cdot {8}^{x}+12x+10) \\  & =\frac{\text{d}}{\text{d}x}(3\cdot {8}^{x})+\frac{\text{d}}{\text{d}x}(12x)+\frac{\text{d}}{\text{d}x}(10) \\  & =3\frac{\text{d}}{\text{d}x}({8}^{x})+12\frac{\text{d}}{\text{d}x}(x)+\frac{\text{d}}{\text{d}x}(10) \\  & =3(ln⁡(8){8}^{x})+12(1)+0 \\  & =3ln⁡(8){8}^{x}+12.\end{aligned}
$$


## generated variant q-304038

Given that $f(x)=1\cdot {9}^{x}+2x+13$, find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}}

- $1\operatorname{ln}(9){9}^{x}+2$ (correct)

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(1\cdot {9}^{x}+2x+13) \\  & =\frac{\text{d}}{\text{d}x}(1\cdot {9}^{x})+\frac{\text{d}}{\text{d}x}(2x)+\frac{\text{d}}{\text{d}x}(13) \\  & =1\frac{\text{d}}{\text{d}x}({9}^{x})+2\frac{\text{d}}{\text{d}x}(x)+\frac{\text{d}}{\text{d}x}(13) \\  & =1(\ln (9){9}^{x})+2(1)+0 \\  & =1\ln (9){9}^{x}+2.\end{aligned}
$$


## generated variant q-304038

Given that $f(x)=10\cdot {4}^{x}+2x+8$, find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}}

- $10\operatorname{ln}(4){4}^{x}+2$ (correct)

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(10\cdot {4}^{x}+2x+8) \\  & =\frac{\text{d}}{\text{d}x}(10\cdot {4}^{x})+\frac{\text{d}}{\text{d}x}(2x)+\frac{\text{d}}{\text{d}x}(8) \\  & =10\frac{\text{d}}{\text{d}x}({4}^{x})+2\frac{\text{d}}{\text{d}x}(x)+\frac{\text{d}}{\text{d}x}(8) \\  & =10(\ln (4){4}^{x})+2(1)+0 \\  & =10\ln (4){4}^{x}+2.\end{aligned}
$$


## original replay q-340272

Given that $f(x)=7-2\cdot {8}^{x}$, find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}}

- $-2\operatorname{ln}(8){8}^{x}$ (correct)

- $-2\cdot8^{x}\ln8$

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(7-2\cdot {8}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(7)-\frac{\text{d}}{\text{d}x}(2\cdot {8}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(7)-2\frac{\text{d}}{\text{d}x}({8}^{x}) \\  & =0-2(ln⁡(8){8}^{x}) \\  & =-2ln⁡(8){8}^{x}.\end{aligned}
$$


## generated variant q-340272

Given that $f(x)=4-8\cdot {2}^{x}$, find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}}

- $-8\operatorname{ln}(2){2}^{x}$ (correct)

- $-8\cdot2^{x}\ln2$

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(4-8\cdot {2}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(4)-\frac{\text{d}}{\text{d}x}(8\cdot {2}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(4)-8\frac{\text{d}}{\text{d}x}({2}^{x}) \\  & =0-8(\ln (2){2}^{x}) \\  & =-8\ln (2){2}^{x}.\end{aligned}
$$


## generated variant q-340272

Given that $f(x)=8-2\cdot {4}^{x}$, find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}}

- $-2\operatorname{ln}(4){4}^{x}$ (correct)

- $-2\cdot4^{x}\ln4$

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(8-2\cdot {4}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(8)-\frac{\text{d}}{\text{d}x}(2\cdot {4}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(8)-2\frac{\text{d}}{\text{d}x}({4}^{x}) \\  & =0-2(\ln (4){4}^{x}) \\  & =-2\ln (4){4}^{x}.\end{aligned}
$$


## original replay q-340280

Given that $f(x)={5}^{x}-6{x}^{3}+4x-1$, the slope of the tangent at $x=0$ is{{field-1}}.

- $\operatorname{ln}(5)+4$ (correct)

- $5^{x}\ln5-18x^2+4$

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({5}^{x}-6{x}^{3}+4x-1) \\  & =\frac{\text{d}}{\text{d}x}({5}^{x})-\frac{\text{d}}{\text{d}x}(6{x}^{3})+\frac{\text{d}}{\text{d}x}(4x)-\frac{\text{d}}{\text{d}x}(1) \\  & =\frac{\text{d}}{\text{d}x}({5}^{x})-6\frac{\text{d}}{\text{d}x}({x}^{3})+4\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(1) \\  & =ln⁡(5)\cdot {5}^{x}-6(3{x}^{2})+4(1)-0 \\  & =ln⁡(5)\cdot {5}^{x}-18{x}^{2}+4.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(ln⁡(5)\cdot {5}^{x}-18{x}^{2}+4)|}_{x=0} \\  & =ln⁡(5)\cdot {5}^{0}-18(0)^{2}+4 \\  & =ln⁡(5)\cdot 1-0+4 \\  & =ln⁡(5)+4.\end{aligned}
$$


## generated variant q-340280

Given that $f(x)={2}^{x}-8{x}^{3}+2x-1$, the slope of the tangent at $x=0$ is{{field-1}}.

- $\operatorname{ln}(2)+2$ (correct)

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({2}^{x}-8{x}^{3}+2x-1) \\  & =\frac{\text{d}}{\text{d}x}({2}^{x})-\frac{\text{d}}{\text{d}x}(8{x}^{3})+\frac{\text{d}}{\text{d}x}(2x)-\frac{\text{d}}{\text{d}x}(13) \\  & =\frac{\text{d}}{\text{d}x}({2}^{x})-8\frac{\text{d}}{\text{d}x}({x}^{3})+2\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(13) \\  & =\ln (2)\cdot {2}^{x}-8(3{x}^{2})+2(1)-0 \\  & =\ln (2)\cdot {2}^{x}-24{x}^{2}+2.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(\ln (2)\cdot {2}^{x}-24{x}^{2}+2)|}_{x=0} \\  & =\ln (2)\cdot {2}^{0}-24(0)^{2}+2 \\  & =\ln (2)\cdot 1-0+2 \\  & =\ln (2)+2.\end{aligned}
$$


## generated variant q-340280

Given that $f(x)={4}^{x}-2{x}^{3}+4x-1$, the slope of the tangent at $x=0$ is{{field-1}}.

- $\operatorname{ln}(4)+4$ (correct)

Applying the formula, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({4}^{x}-2{x}^{3}+4x-1) \\  & =\frac{\text{d}}{\text{d}x}({4}^{x})-\frac{\text{d}}{\text{d}x}(2{x}^{3})+\frac{\text{d}}{\text{d}x}(4x)-\frac{\text{d}}{\text{d}x}(15) \\  & =\frac{\text{d}}{\text{d}x}({4}^{x})-2\frac{\text{d}}{\text{d}x}({x}^{3})+4\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(15) \\  & =\ln (4)\cdot {4}^{x}-2(3{x}^{2})+4(1)-0 \\  & =\ln (4)\cdot {4}^{x}-6{x}^{2}+4.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(\ln (4)\cdot {4}^{x}-6{x}^{2}+4)|}_{x=0} \\  & =\ln (4)\cdot {4}^{0}-6(0)^{2}+4 \\  & =\ln (4)\cdot 1-0+4 \\  & =\ln (4)+4.\end{aligned}
$$


## authored hard variant

Given that $f(x)=3\cdot {6}^{x}+1\cdot {2}^{x}-4x^2+8$, find the instantaneous rate of change at $x=2.$

{{field-1}}

- $-16 + 4 \ln{\left(2 \right)} + 108 \ln{\left(6 \right)}$ (correct)

Applying the formula, we get

$$
\begin{aligned}f'(x)&=\frac{\text{d}}{\text{d}x}(3\cdot {6}^{x}+1\cdot {2}^{x}-4x^2+8) \\ &=3\frac{\text{d}}{\text{d}x}({6}^{x})+1\frac{\text{d}}{\text{d}x}({2}^{x})-4\frac{\text{d}}{\text{d}x}(x^2)+\frac{\text{d}}{\text{d}x}(8) \\ &=3({6}^{x}\ln(6))+1({2}^{x}\ln(2))-4(2x)+0 \\ &=3\ln(6)\cdot {6}^{x}+1\ln(2)\cdot {2}^{x}-8x.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=2$ is

$$
\begin{aligned}f'(2)&=3\ln(6)\cdot {6}^{(2)}+1\ln(2)\cdot {2}^{(2)}-8(2) \\ &=3(36)\ln(6)+1(4)\ln(2)-(8)(2) \\ &=-16 + 4 \ln{\left(2 \right)} + 108 \ln{\left(6 \right)}.\end{aligned}
$$


## authored hard variant

Given that $f(x)=3\cdot {2}^{x}+2\cdot {6}^{x}-3x^2+5$, find the instantaneous rate of change at $x=-1.$

{{field-1}}

- $\frac{\ln{\left(6 \right)}}{3} + \frac{3 \ln{\left(2 \right)}}{2} + 6$ (correct)

Applying the formula, we get

$$
\begin{aligned}f'(x)&=\frac{\text{d}}{\text{d}x}(3\cdot {2}^{x}+2\cdot {6}^{x}-3x^2+5) \\ &=3\frac{\text{d}}{\text{d}x}({2}^{x})+2\frac{\text{d}}{\text{d}x}({6}^{x})-3\frac{\text{d}}{\text{d}x}(x^2)+\frac{\text{d}}{\text{d}x}(5) \\ &=3({2}^{x}\ln(2))+2({6}^{x}\ln(6))-3(2x)+0 \\ &=3\ln(2)\cdot {2}^{x}+2\ln(6)\cdot {6}^{x}-6x.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=-1$ is

$$
\begin{aligned}f'(-1)&=3\ln(2)\cdot {2}^{(-1)}+2\ln(6)\cdot {6}^{(-1)}-6(-1) \\ &=3(\frac{1}{2})\ln(2)+2(\frac{1}{6})\ln(6)-(6)(-1) \\ &=\frac{\ln{\left(6 \right)}}{3} + \frac{3 \ln{\left(2 \right)}}{2} + 6.\end{aligned}
$$
