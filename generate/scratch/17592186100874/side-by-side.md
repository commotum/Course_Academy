# Originals and changes side by side

| Source | Original parameters | Changed parameters | Profile |
|---|---|---|---|
| q-49527 | `{"a": 2, "b": -1, "c": 1, "l": "1", "h": "2"}` | `{"a": 9, "b": 1, "c": 1, "l": "0", "h": "4/9"}` | observed |
| q-49610 | `{"a": 2, "b": 1, "c": 1, "l": "1", "h": "2"}` | `{"a": 9, "b": 1, "c": 1, "l": "2/9", "h": "4/9"}` | observed |
| q-17103 | `{"a": 1, "b": 1, "c": 3, "l": "0", "h": "2"}` | `{"a": 8, "b": 1, "c": 8, "l": "0", "h": "1"}` | observed |
| q-17104 | `{"a": -1, "b": 2, "c": 1, "l": "0", "h": "1"}` | `{"a": -1, "b": 5, "c": 1, "l": "1/2", "h": "1"}` | observed |
| q-318994 | `{"a": 1, "b": 5, "c": 6, "l": "0", "h": "1"}` | `{"a": 1, "b": 4, "c": 6, "l": "1/2", "h": "1"}` | blank |
| q-336603 | `{"a": 10, "b": 7, "c": 1, "l": "-7/10", "h": "-1/5"}` | `{"a": 4, "b": 1, "c": 1, "l": "1/2", "h": "1"}` | blank |
| q-336612 | `{"a": 1, "b": 1, "c": 8, "l": "0", "h": "1"}` | `{"a": 1, "b": 4, "c": 1, "l": "1/2", "h": "1"}` | blank |
| q-336783 | `{"a": 9, "b": 2, "c": 1, "l": "0", "h": "1/3"}` | `{"a": 4, "b": 1, "c": 1, "l": "1/4", "h": "5/4"}` | blank |
| q-336788 | `{"a": 4, "b": 2, "c": 1, "l": "0", "h": "1/2"}` | `{"a": 4, "b": 1, "c": 1, "l": "1/4", "h": "5/4"}` | blank |
| q-336803 | `{"a": 1, "b": 1, "c": 2, "l": "0", "h": "sqrt(3)"}` | `{"a": 1, "b": 4, "c": 2, "l": "1/2", "h": "2*sqrt(2)"}` | blank |
| q-336804 | `{"a": 1, "b": 1, "c": 2, "l": "0", "h": "2*sqrt(2)"}` | `{"a": 1, "b": 4, "c": 2, "l": "1/2", "h": "2*sqrt(2)"}` | blank |
| q-49613 | `{"a": 5, "b": -6, "c": 1, "l": "2", "h": "3"}` | `{"a": 9, "b": 1, "c": 1, "l": "1/3", "h": "8/9"}` | observed |
| q-49622 | `{"a": 8, "b": 1, "c": 1, "l": "0", "h": "1/4"}` | `{"a": 9, "b": 1, "c": 1, "l": "0", "h": "2/9"}` | observed |

## q-49527

Original:
Calculate the definite integral $\displaystyle \int_{1}^{2}\sqrt{2x - 1}dx$.

No supplied solution or key. Raw evidence remains ineligible.

Changed:
Calculate the definite integral $\int_{0}^{\frac{4}{9}} \sqrt{9 x + 1}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u&=9 x + 1\\ \frac{\text{d}u}{\text{d}x}&=9\\ \text{d}u&=9\,\text{d}x\\ \frac{1}{9}\text{d}u&=1\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=9 x + 1.$

$$
\begin{aligned}x & 0 & \frac{4}{9}\\ u & 1 & 5\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{0}^{\frac{4}{9}} \sqrt{9 x + 1}\,\text{d}x=\int_{1}^{5} \sqrt{u}\cdot (\frac{1}{9})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{1}^{5} \sqrt{u}\cdot (\frac{1}{9})\,\text{d}u &=\frac{1}{9}\int_{1}^{5} u^{\frac{1}{2}}\,\text{d}u\\ &=\frac{2 u^{\frac{3}{2}}}{27}\big|_{1}^{5}\\ &=\frac{2}{27}((5)^{\frac{3}{2}}-(1)^{\frac{3}{2}})\\ &=\frac{10 \sqrt{5}}{27}-(\frac{2}{27})\\ &=- \frac{2}{27} + \frac{10 \sqrt{5}}{27}.\end{aligned}
$$

## q-49610

Original:
Calculate the definite integral ${\int }_{1}^{2}{(2x+1)}^{2}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u & =2x+1 \\ \frac{\text{d}u}{\text{d}x} & =2 \\ \text{d}u & =2\,\text{d}x \\ \frac{1}{2}\text{d}u & =\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=2x+1.$

$$
\begin{aligned}x & 1 & 2 \\ u & 3 & 5\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{1}^{2}{(2x+1)}^{2}\,\text{d}x={\int }_{3}^{5}{u}^{2}\cdot \frac{1}{2}\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{3}^{5}{u}^{2}\cdot \frac{1}{2}\text{d}u & =\frac{1}{2}{\int }_{3}^{5}{u}^{2}\,\text{d}u \\  & =\frac{1}{2}{\cdot \frac{1}{3}{u}^{3}|}_{3}^{5} \\  & =\frac{1}{2}\cdot \frac{{5}^{3}-{3}^{3}}{3} \\  & =\frac{1}{2}\cdot \frac{125-27}{3} \\  & =\frac{98}{6} \\  & =\frac{49}{3}.\end{aligned}
$$

Changed:
Calculate the definite integral $\int_{\frac{2}{9}}^{\frac{4}{9}} (9 x + 1)^{2}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u&=9 x + 1\\ \frac{\text{d}u}{\text{d}x}&=9\\ \text{d}u&=9\,\text{d}x\\ \frac{1}{9}\text{d}u&=1\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=9 x + 1.$

$$
\begin{aligned}x & \frac{2}{9} & \frac{4}{9}\\ u & 3 & 5\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{2}{9}}^{\frac{4}{9}} (9 x + 1)^{2}\,\text{d}x=\int_{3}^{5} (u)^{2}\cdot (\frac{1}{9})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{3}^{5} (u)^{2}\cdot (\frac{1}{9})\,\text{d}u &=\frac{1}{9}\int_{3}^{5} u^{2}\,\text{d}u\\ &=\frac{u^{3}}{27}\big|_{3}^{5}\\ &=\frac{1}{27}((5)^{3}-(3)^{3})\\ &=\frac{125}{27}-(1)\\ &=\frac{98}{27}.\end{aligned}
$$

## q-17103

Original:
${\int }_{0}^{2}3{x}^{2}\sqrt{{({x}^{3}+1)}^{3}}\,\text{d}x=$

We start by changing the variable:

$$
\begin{aligned}u & ={x}^{3}+1 \\ \frac{\text{d}u}{\text{d}x} & =3{x}^{2} \\ \text{d}u & =3{x}^{2}\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u={x}^{3}+1.$

$$
\begin{aligned}x & 0 & 2 \\ u & 1 & 9\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{2}\sqrt{{({x}^{3}+1)}^{3}}\cdot 3{x}^{2}\,\text{d}x={\int }_{1}^{9}\sqrt{{u}^{3}}\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{1}^{9}\sqrt{{u}^{3}}\,\text{d}u & ={\int }_{1}^{9}{u}^{3/2}\,\text{d}u \\  & ={\frac{2}{5}{u}^{5/2}|}_{1}^{9} \\  & =\frac{2}{5}({9}^{5/2}-{1}^{5/2}) \\  & =\frac{2}{5}(({3}^{2})^{5/2}-1) \\  & =\frac{2}{5}({3}^{5}-1) \\  & =\frac{484}{5}.\end{aligned}
$$

Changed:
$\int_{0}^{1} 8 x^{2}\cdot \sqrt{(8 x^{3} + 1)^{3}}\,\text{d}x=$

We start by changing the variable:

$$
\begin{aligned}u&=8 x^{3} + 1\\ \frac{\text{d}u}{\text{d}x}&=24 x^{2}\\ \text{d}u&=24 x^{2}\,\text{d}x\\ \frac{1}{3}\text{d}u&=8 x^{2}\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=8 x^{3} + 1.$

$$
\begin{aligned}x & 0 & 1\\ u & 1 & 9\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{0}^{1} 8 x^{2}\cdot \sqrt{(8 x^{3} + 1)^{3}}\,\text{d}x=\int_{1}^{9} \sqrt{(u)^{3}}\cdot (\frac{1}{3})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{1}^{9} \sqrt{(u)^{3}}\cdot (\frac{1}{3})\,\text{d}u &=\frac{1}{3}\int_{1}^{9} u^{\frac{3}{2}}\,\text{d}u\\ &=\frac{2 u^{\frac{5}{2}}}{15}\big|_{1}^{9}\\ &=\frac{2}{15}((9)^{\frac{5}{2}}-(1)^{\frac{5}{2}})\\ &=\frac{162}{5}-(\frac{2}{15})\\ &=\frac{484}{15}.\end{aligned}
$$

## q-17104

Original:
Evaluate the definite integral ${\int }_{0}^{1}{x}^{2}\sqrt{{(2-{x}^{3})}^{3}}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u & =2-{x}^{3} \\ \frac{\text{d}u}{\text{d}x} & =-3{x}^{2} \\ \text{d}u & =-3{x}^{2}\,\text{d}x \\ -\frac{1}{3}\text{d}u & ={x}^{2}\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=2-{x}^{3}.$

$$
\begin{aligned}x & 0 & 1 \\ u & 2 & 1\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{1}\sqrt{{(2-{x}^{3})}^{3}}\cdot {x}^{2}\,\text{d}x={\int }_{2}^{1}\sqrt{{u}^{3}}\cdot (-\frac{1}{3})\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{2}^{1}\sqrt{{u}^{3}}\cdot (-\frac{1}{3})\text{d}u & =-\frac{1}{3}{\int }_{2}^{1}{u}^{3/2}\,\text{d}u \\  & =-\frac{1}{3}\cdot {\frac{2}{5}{u}^{5/2}|}_{2}^{1} \\  & =-\frac{1}{3}\cdot \frac{2}{5}({1}^{5/2}-{2}^{5/2}) \\  & =-\frac{2}{15}(1-({2}^{5})^{1/2}) \\  & =-\frac{2}{15}(1-4\sqrt{2}) \\  & =\frac{2}{15}(4\sqrt{2}-1).\end{aligned}
$$

Changed:
Evaluate the definite integral $\int_{\frac{1}{2}}^{1} x^{2}\cdot \sqrt{(5 - x^{3})^{3}}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u&=5 - x^{3}\\ \frac{\text{d}u}{\text{d}x}&=- 3 x^{2}\\ \text{d}u&=- 3 x^{2}\,\text{d}x\\ - \frac{1}{3}\text{d}u&=x^{2}\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=5 - x^{3}.$

$$
\begin{aligned}x & \frac{1}{2} & 1\\ u & \frac{39}{8} & 4\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{2}}^{1} x^{2}\cdot \sqrt{(5 - x^{3})^{3}}\,\text{d}x=\int_{\frac{39}{8}}^{4} \sqrt{(u)^{3}}\cdot (- \frac{1}{3})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{\frac{39}{8}}^{4} \sqrt{(u)^{3}}\cdot (- \frac{1}{3})\,\text{d}u &=- \frac{1}{3}\int_{\frac{39}{8}}^{4} u^{\frac{3}{2}}\,\text{d}u\\ &=- \frac{2 u^{\frac{5}{2}}}{15}\big|_{\frac{39}{8}}^{4}\\ &=- \frac{2}{15}((4)^{\frac{5}{2}}-(\frac{39}{8})^{\frac{5}{2}})\\ &=- \frac{64}{15}-(- \frac{507 \sqrt{78}}{640})\\ &=- \frac{64}{15} + \frac{507 \sqrt{78}}{640}.\end{aligned}
$$

## q-318994

Original:
Compute the exact value of the definite integral.

${\int }_{0}^{1}6{x}^{2}\cdot {({x}^{3}+5)}^{3}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u & ={x}^{3}+5 \\ \frac{\text{d}u}{\text{d}x} & =3{x}^{2} \\ \text{d}u & =3{x}^{2}\,\text{d}x \\ 6{x}^{2}\,\text{d}x & =2\,\text{d}u\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u={x}^{3}+5.$

$$
\begin{aligned}x & 0 & 1 \\ u & 5 & 6\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{1}6{x}^{2}\cdot {({x}^{3}+5)}^{3}\,\text{d}x={\int }_{5}^{6}{u}^{3}\cdot 2\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{5}^{6}2{u}^{3}\,\text{d}u & =2{\int }_{5}^{6}{u}^{3}\,\text{d}u \\  & =2\cdot {\frac{{u}^{4}}{4}|}_{5}^{6} \\  & =2\cdot \frac{1}{4}({6}^{4}-{5}^{4}) \\  & =\frac{1}{2}(1296-625) \\  & =\frac{1}{2}\cdot 671 \\  & =\frac{671}{2}.\end{aligned}
$$

Changed:
Compute the exact value of the definite integral.

$\int_{\frac{1}{2}}^{1} 6 x^{2}\cdot (x^{3} + 4)^{3}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u&=x^{3} + 4\\ \frac{\text{d}u}{\text{d}x}&=3 x^{2}\\ \text{d}u&=3 x^{2}\,\text{d}x\\ 2\text{d}u&=6 x^{2}\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=x^{3} + 4.$

$$
\begin{aligned}x & \frac{1}{2} & 1\\ u & \frac{33}{8} & 5\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{2}}^{1} 6 x^{2}\cdot (x^{3} + 4)^{3}\,\text{d}x=\int_{\frac{33}{8}}^{5} (u)^{3}\cdot (2)\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{\frac{33}{8}}^{5} (u)^{3}\cdot (2)\,\text{d}u &=2\int_{\frac{33}{8}}^{5} u^{3}\,\text{d}u\\ &=\frac{u^{4}}{2}\big|_{\frac{33}{8}}^{5}\\ &=\frac{1}{2}((5)^{4}-(\frac{33}{8})^{4})\\ &=\frac{625}{2}-(\frac{1185921}{8192})\\ &=\frac{1374079}{8192}.\end{aligned}
$$

## q-336603

Original:
Compute the exact value of the definite integral.

${\int }_{-7/10}^{-1/5}\sqrt{10x+7}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u & =10x+7 \\ \frac{\text{d}u}{\text{d}x} & =10 \\ \text{d}u & =10\,\text{d}x \\ \frac{1}{10}\text{d}u & =\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=10x+7.$

$$
\begin{aligned}x & -\frac{7}{10} & -\frac{1}{5} \\ u & 0 & 5\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{-7/10}^{-1/5}\sqrt{10x+7}\,\text{d}x={\int }_{0}^{5}\sqrt{u}\,\cdot \frac{1}{10}\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{0}^{5}\sqrt{u}\,\cdot \frac{1}{10}\,\text{d}u & =\frac{1}{10}{\int }_{0}^{5}{u}^{1/2}\,\text{d}u \\  & =\frac{1}{10}\cdot {\frac{2}{3}{u}^{3/2}|}_{0}^{5} \\  & =\frac{1}{10}\cdot \frac{2}{3}({5}^{3/2}-{0}^{3/2}) \\  & =\frac{1}{15}(({5}^{3})^{1/2}-0) \\  & =\frac{1}{15}\cdot 5\sqrt{5} \\  & =\frac{\sqrt{5}}{3}.\end{aligned}
$$

Changed:
Compute the exact value of the definite integral.

$\int_{\frac{1}{2}}^{1} \sqrt{4 x + 1}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u&=4 x + 1\\ \frac{\text{d}u}{\text{d}x}&=4\\ \text{d}u&=4\,\text{d}x\\ \frac{1}{4}\text{d}u&=1\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=4 x + 1.$

$$
\begin{aligned}x & \frac{1}{2} & 1\\ u & 3 & 5\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{2}}^{1} \sqrt{4 x + 1}\,\text{d}x=\int_{3}^{5} \sqrt{u}\cdot (\frac{1}{4})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{3}^{5} \sqrt{u}\cdot (\frac{1}{4})\,\text{d}u &=\frac{1}{4}\int_{3}^{5} u^{\frac{1}{2}}\,\text{d}u\\ &=\frac{u^{\frac{3}{2}}}{6}\big|_{3}^{5}\\ &=\frac{1}{6}((5)^{\frac{3}{2}}-(3)^{\frac{3}{2}})\\ &=\frac{5 \sqrt{5}}{6}-(\frac{\sqrt{3}}{2})\\ &=- \frac{\sqrt{3}}{2} + \frac{5 \sqrt{5}}{6}.\end{aligned}
$$

## q-336612

Original:
Compute the exact value of the definite integral.

${\int }_{0}^{1}8{x}^{3}\cdot {({x}^{4}+1)}^{2}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u & ={x}^{4}+1 \\ \frac{\text{d}u}{\text{d}x} & =4{x}^{3} \\ \text{d}u & =4{x}^{3}\,\text{d}x \\ 8{x}^{3}\,\text{d}x & =2\,\text{d}u\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u={x}^{4}+1.$

$$
\begin{aligned}x & 0 & 1 \\ u & 1 & 2\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{1}8{x}^{3}\cdot {({x}^{4}+1)}^{2}\,\text{d}x={\int }_{1}^{2}{u}^{2}\cdot 2\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{1}^{2}2{u}^{2}\,\text{d}u & =2{\int }_{1}^{2}{u}^{2}\,\text{d}u \\  & =2\cdot {\frac{{u}^{3}}{3}|}_{1}^{2} \\  & =\frac{2}{3}({2}^{3}-{1}^{3}) \\  & =\frac{2}{3}(8-1) \\  & =\frac{2}{3}\cdot 7 \\  & =\frac{14}{3}.\end{aligned}
$$

Changed:
Compute the exact value of the definite integral.

$\int_{\frac{1}{2}}^{1} x^{3}\cdot (x^{4} + 4)^{2}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u&=x^{4} + 4\\ \frac{\text{d}u}{\text{d}x}&=4 x^{3}\\ \text{d}u&=4 x^{3}\,\text{d}x\\ \frac{1}{4}\text{d}u&=x^{3}\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=x^{4} + 4.$

$$
\begin{aligned}x & \frac{1}{2} & 1\\ u & \frac{65}{16} & 5\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{2}}^{1} x^{3}\cdot (x^{4} + 4)^{2}\,\text{d}x=\int_{\frac{65}{16}}^{5} (u)^{2}\cdot (\frac{1}{4})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{\frac{65}{16}}^{5} (u)^{2}\cdot (\frac{1}{4})\,\text{d}u &=\frac{1}{4}\int_{\frac{65}{16}}^{5} u^{2}\,\text{d}u\\ &=\frac{u^{3}}{12}\big|_{\frac{65}{16}}^{5}\\ &=\frac{1}{12}((5)^{3}-(\frac{65}{16})^{3})\\ &=\frac{125}{12}-(\frac{274625}{49152})\\ &=\frac{79125}{16384}.\end{aligned}
$$

## q-336783

Original:
Compute the exact value of the definite integral.

${\int }_{0}^{1/3}{(9x+2)}^{2}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u & =9x+2 \\ \frac{\text{d}u}{\text{d}x} & =9 \\ \text{d}u & =9\,\text{d}x \\ \frac{1}{9}\text{d}u & =\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=9x+2.$

$$
\begin{aligned}x & 0 & \frac{1}{3} \\ u & 2 & 5\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{1/3}{(9x+2)}^{2}\,\text{d}x={\int }_{2}^{5}{u}^{2}\cdot \frac{1}{9}\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{0}^{1/3}{(9x+2)}^{2}\,\text{d}x & ={\int }_{2}^{5}{u}^{2}\cdot \frac{1}{9}\text{d}u \\  & =\frac{1}{9}{\int }_{2}^{5}{u}^{2}\,\text{d}u \\  & =\frac{1}{9}\cdot {\frac{1}{3}{u}^{3}|}_{2}^{5} \\  & =\frac{1}{9}\cdot \frac{1}{3}({5}^{3}-{2}^{3}) \\  & =\frac{1}{27}(125-8) \\  & =\frac{13}{3}.\end{aligned}
$$

Changed:
Compute the exact value of the definite integral.

$\int_{\frac{1}{4}}^{\frac{5}{4}} (4 x + 1)^{2}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u&=4 x + 1\\ \frac{\text{d}u}{\text{d}x}&=4\\ \text{d}u&=4\,\text{d}x\\ \frac{1}{4}\text{d}u&=1\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=4 x + 1.$

$$
\begin{aligned}x & \frac{1}{4} & \frac{5}{4}\\ u & 2 & 6\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{4}}^{\frac{5}{4}} (4 x + 1)^{2}\,\text{d}x=\int_{2}^{6} (u)^{2}\cdot (\frac{1}{4})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{2}^{6} (u)^{2}\cdot (\frac{1}{4})\,\text{d}u &=\frac{1}{4}\int_{2}^{6} u^{2}\,\text{d}u\\ &=\frac{u^{3}}{12}\big|_{2}^{6}\\ &=\frac{1}{12}((6)^{3}-(2)^{3})\\ &=18-(\frac{2}{3})\\ &=\frac{52}{3}.\end{aligned}
$$

## q-336788

Original:
Compute the exact value of the definite integral.

${\int }_{0}^{1/2}{(4x+2)}^{3}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u & =4x+2 \\ \frac{\text{d}u}{\text{d}x} & =4 \\ \text{d}u & =4\,\text{d}x \\ \frac{1}{4}\text{d}u & =\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=4x+2.$

$$
\begin{aligned}x & 0 & \frac{1}{2} \\ u & 2 & 4\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{1/2}{(4x+2)}^{3}\,\text{d}x={\int }_{2}^{4}{u}^{3}\cdot \frac{1}{4}\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{0}^{1/2}{(4x+2)}^{3}\,\text{d}x & ={\int }_{2}^{4}{u}^{3}\cdot \frac{1}{4}\text{d}u \\  & =\frac{1}{4}{\int }_{2}^{4}{u}^{3}\,\text{d}u \\  & =\frac{1}{4}\cdot {\frac{1}{4}{u}^{4}|}_{2}^{4} \\  & =\frac{1}{4}\cdot \frac{1}{4}({4}^{4}-{2}^{4}) \\  & =\frac{1}{16}(256-16) \\  & =15.\end{aligned}
$$

Changed:
Compute the exact value of the definite integral.

$\int_{\frac{1}{4}}^{\frac{5}{4}} (4 x + 1)^{3}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u&=4 x + 1\\ \frac{\text{d}u}{\text{d}x}&=4\\ \text{d}u&=4\,\text{d}x\\ \frac{1}{4}\text{d}u&=1\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=4 x + 1.$

$$
\begin{aligned}x & \frac{1}{4} & \frac{5}{4}\\ u & 2 & 6\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{4}}^{\frac{5}{4}} (4 x + 1)^{3}\,\text{d}x=\int_{2}^{6} (u)^{3}\cdot (\frac{1}{4})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{2}^{6} (u)^{3}\cdot (\frac{1}{4})\,\text{d}u &=\frac{1}{4}\int_{2}^{6} u^{3}\,\text{d}u\\ &=\frac{u^{4}}{16}\big|_{2}^{6}\\ &=\frac{1}{16}((6)^{4}-(2)^{4})\\ &=81-(1)\\ &=80.\end{aligned}
$$

## q-336803

Original:
Compute the exact value of the definite integral.

${\int }_{0}^{\sqrt{3}}2x\sqrt{{({x}^{2}+1)}^{3}}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u & ={x}^{2}+1 \\ \frac{\text{d}u}{\text{d}x} & =2x \\ \text{d}u & =2x\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u={x}^{2}+1.$

$$
\begin{aligned}x & 0 & \sqrt{3} \\ u & 1 & 4\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{\sqrt{3}}\sqrt{{({x}^{2}+1)}^{3}}\cdot 2x\,\text{d}x={\int }_{1}^{4}\sqrt{{u}^{3}}\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{1}^{4}\sqrt{{u}^{3}}\,\text{d}u & ={\int }_{1}^{4}{u}^{3/2}\,\text{d}u \\  & ={\frac{2}{5}{u}^{5/2}|}_{1}^{4} \\  & =\frac{2}{5}({4}^{5/2}-{1}^{5/2}) \\  & =\frac{2}{5}(({2}^{2})^{5/2}-1) \\  & =\frac{2}{5}({2}^{5}-1) \\  & =\frac{62}{5}.\end{aligned}
$$

Changed:
Compute the exact value of the definite integral.

$\int_{\frac{1}{2}}^{2 \sqrt{2}} 2 x\cdot \sqrt{(x^{2} + 4)^{3}}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u&=x^{2} + 4\\ \frac{\text{d}u}{\text{d}x}&=2 x\\ \text{d}u&=2 x\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=x^{2} + 4.$

$$
\begin{aligned}x & \frac{1}{2} & 2 \sqrt{2}\\ u & \frac{17}{4} & 12\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{2}}^{2 \sqrt{2}} 2 x\cdot \sqrt{(x^{2} + 4)^{3}}\,\text{d}x=\int_{\frac{17}{4}}^{12} \sqrt{(u)^{3}}\cdot (1)\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{\frac{17}{4}}^{12} \sqrt{(u)^{3}}\cdot (1)\,\text{d}u &=1\int_{\frac{17}{4}}^{12} u^{\frac{3}{2}}\,\text{d}u\\ &=\frac{2 u^{\frac{5}{2}}}{5}\big|_{\frac{17}{4}}^{12}\\ &=\frac{2}{5}((12)^{\frac{5}{2}}-(\frac{17}{4})^{\frac{5}{2}})\\ &=\frac{576 \sqrt{3}}{5}-(\frac{289 \sqrt{17}}{80})\\ &=- \frac{289 \sqrt{17}}{80} + \frac{576 \sqrt{3}}{5}.\end{aligned}
$$

## q-336804

Original:
Compute the exact value of the definite integral.

${\int }_{0}^{2\sqrt{2}}2x\sqrt{{x}^{2}+1}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u & ={x}^{2}+1 \\ \frac{\text{d}u}{\text{d}x} & =2x \\ \text{d}u & =2x\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u={x}^{2}+1.$

$$
\begin{aligned}x & 0 & 2\sqrt{2} \\ u & 1 & 9\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{2\sqrt{2}}\sqrt{{x}^{2}+1}\cdot 2x\,\text{d}x={\int }_{1}^{9}\sqrt{u}\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{1}^{9}\sqrt{u}\,\text{d}u & ={\int }_{1}^{9}{u}^{1/2}\,\text{d}u \\  & ={\frac{2}{3}{u}^{3/2}|}_{1}^{9} \\  & =\frac{2}{3}({9}^{3/2}-{1}^{3/2}) \\  & =\frac{2}{3}(({3}^{2})^{3/2}-1) \\  & =\frac{2}{3}({3}^{3}-1) \\  & =\frac{52}{3}.\end{aligned}
$$

Changed:
Compute the exact value of the definite integral.

$\int_{\frac{1}{2}}^{2 \sqrt{2}} 2 x\cdot \sqrt{x^{2} + 4}\,\text{d}x=$
{{field-1}}

We start by changing the variable:

$$
\begin{aligned}u&=x^{2} + 4\\ \frac{\text{d}u}{\text{d}x}&=2 x\\ \text{d}u&=2 x\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=x^{2} + 4.$

$$
\begin{aligned}x & \frac{1}{2} & 2 \sqrt{2}\\ u & \frac{17}{4} & 12\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{2}}^{2 \sqrt{2}} 2 x\cdot \sqrt{x^{2} + 4}\,\text{d}x=\int_{\frac{17}{4}}^{12} \sqrt{u}\cdot (1)\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{\frac{17}{4}}^{12} \sqrt{u}\cdot (1)\,\text{d}u &=1\int_{\frac{17}{4}}^{12} u^{\frac{1}{2}}\,\text{d}u\\ &=\frac{2 u^{\frac{3}{2}}}{3}\big|_{\frac{17}{4}}^{12}\\ &=\frac{2}{3}((12)^{\frac{3}{2}}-(\frac{17}{4})^{\frac{3}{2}})\\ &=16 \sqrt{3}-(\frac{17 \sqrt{17}}{12})\\ &=- \frac{17 \sqrt{17}}{12} + 16 \sqrt{3}.\end{aligned}
$$

## q-49613

Original:
Evaluate the definite integral ${\int }_{2}^{3}\sqrt{{(5x-6)}^{3}}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u & =5x-6 \\ \frac{\text{d}u}{\text{d}x} & =5 \\ \text{d}u & =5\,\text{d}x \\ \frac{1}{5}\text{d}u & =\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=5x-6.$

$$
\begin{aligned}x & 2 & 3 \\ u & 4 & 9\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{2}^{3}\sqrt{{(5x-6)}^{3}}\,\text{d}x={\int }_{4}^{9}\sqrt{{u}^{3}}\,\cdot \frac{1}{5}\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{4}^{9}\sqrt{{u}^{3}}\,\cdot \frac{1}{5}\,\text{d}u & =\frac{1}{5}{\int }_{4}^{9}{u}^{3/2}\,\text{d}u \\  & =\frac{1}{5}\cdot {\frac{2}{5}{u}^{5/2}|}_{4}^{9} \\  & =\frac{1}{5}\cdot \frac{2}{5}({9}^{5/2}-{4}^{5/2}) \\  & =\frac{2}{25}(({3}^{2})^{5/2}-({2}^{2})^{5/2}) \\  & =\frac{2}{25}({3}^{5}-{2}^{5}) \\  & =\frac{2}{25}(243-32) \\  & =\frac{422}{25}.\end{aligned}
$$

Changed:
Evaluate the definite integral $\int_{\frac{1}{3}}^{\frac{8}{9}} \sqrt{(9 x + 1)^{3}}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u&=9 x + 1\\ \frac{\text{d}u}{\text{d}x}&=9\\ \text{d}u&=9\,\text{d}x\\ \frac{1}{9}\text{d}u&=1\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=9 x + 1.$

$$
\begin{aligned}x & \frac{1}{3} & \frac{8}{9}\\ u & 4 & 9\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{\frac{1}{3}}^{\frac{8}{9}} \sqrt{(9 x + 1)^{3}}\,\text{d}x=\int_{4}^{9} \sqrt{(u)^{3}}\cdot (\frac{1}{9})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{4}^{9} \sqrt{(u)^{3}}\cdot (\frac{1}{9})\,\text{d}u &=\frac{1}{9}\int_{4}^{9} u^{\frac{3}{2}}\,\text{d}u\\ &=\frac{2 u^{\frac{5}{2}}}{45}\big|_{4}^{9}\\ &=\frac{2}{45}((9)^{\frac{5}{2}}-(4)^{\frac{5}{2}})\\ &=\frac{54}{5}-(\frac{64}{45})\\ &=\frac{422}{45}.\end{aligned}
$$

## q-49622

Original:
Evaluate the definite integral ${\int }_{0}^{1/4}\sqrt{8x+1}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u & =8x+1 \\ \frac{\text{d}u}{\text{d}x} & =8 \\ \text{d}u & =8\,\text{d}x \\ \frac{1}{8}\text{d}u & =\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=8x+1.$

$$
\begin{aligned}x & 0 & \frac{1}{4} \\ u & 1 & 3\end{aligned}
$$

So, the integral in terms of the new variable is

$$
{\int }_{0}^{1/4}\sqrt{8x+1}\,\text{d}x={\int }_{1}^{3}\sqrt{u}\,\cdot \frac{1}{8}\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}{\int }_{1}^{3}\sqrt{u}\,\cdot \frac{1}{8}\,\text{d}u & =\frac{1}{8}{\int }_{1}^{3}{u}^{1/2}\,\text{d}u \\  & =\frac{1}{8}\cdot {\frac{2}{3}{u}^{3/2}|}_{1}^{3} \\  & =\frac{1}{8}\cdot \frac{2}{3}({3}^{3/2}-{1}^{3/2}) \\  & =\frac{1}{12}({({3}^{3})}^{1/2}-1) \\  & =\frac{1}{12}(3\sqrt{3}-1).\end{aligned}
$$

Changed:
Evaluate the definite integral $\int_{0}^{\frac{2}{9}} \sqrt{9 x + 1}\,\text{d}x.$

We start by changing the variable:

$$
\begin{aligned}u&=9 x + 1\\ \frac{\text{d}u}{\text{d}x}&=9\\ \text{d}u&=9\,\text{d}x\\ \frac{1}{9}\text{d}u&=1\,\text{d}x\end{aligned}
$$

Next, we create a table for the limits of integration using the rule $u=9 x + 1.$

$$
\begin{aligned}x & 0 & \frac{2}{9}\\ u & 1 & 3\end{aligned}
$$

So, the integral in terms of the new variable is

$$
\int_{0}^{\frac{2}{9}} \sqrt{9 x + 1}\,\text{d}x=\int_{1}^{3} \sqrt{u}\cdot (\frac{1}{9})\,\text{d}u.
$$

Finally, we can solve it and get

$$
\begin{aligned}\int_{1}^{3} \sqrt{u}\cdot (\frac{1}{9})\,\text{d}u &=\frac{1}{9}\int_{1}^{3} u^{\frac{1}{2}}\,\text{d}u\\ &=\frac{2 u^{\frac{3}{2}}}{27}\big|_{1}^{3}\\ &=\frac{2}{27}((3)^{\frac{3}{2}}-(1)^{\frac{3}{2}})\\ &=\frac{2 \sqrt{3}}{9}-(\frac{2}{27})\\ &=- \frac{2}{27} + \frac{2 \sqrt{3}}{9}.\end{aligned}
$$
