## q-103374 — easy

{"a": 3, "b": 6, "d": 2}

Calculate $\int \frac{3{x}^{2}-6}{2x}\,dx.$

- $\frac{3 x^{2}}{4} - 3 \ln|x|+C$ **correct**

- $\frac{3 x^{2}}{2} - \ln|3 x|+C$

- $3 x^{2} + \ln|3 x|+C$

- $\frac{3 x^{2}}{2} + 3 \ln|x|+C$

- $\frac{3 x^{2}}{4} - \ln|3 x|+C$

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int \frac{3{x}^{2}-6}{2x}\,\text{d}x & =\int (\frac{3{x}^{2}}{2x}-\frac{3}{x})\text{d}x \\  & =\int (\frac{3}{2}x-\frac{3}{x})\text{d}x \\  & =\frac{3}{2}\int x\,\text{d}x-3\int \frac{1}{x}\,\text{d}x \\  & =\frac{3}{4}{x}^{2}-3\ln|x|+C.\end{aligned}
$$

---

## q-103374 — easy

{"a": 2, "b": 4, "d": 2}

Calculate $\int \frac{2{x}^{2}-4}{2x}\,dx.$

- $\frac{x^{2}}{2} - 2 \ln|x|+C$ **correct**

- $x^{2} - \ln|2 x|+C$

- $2 x^{2} + \ln|2 x|+C$

- $x^{2} + 2 \ln|x|+C$

- $\frac{x^{2}}{2} - \ln|2 x|+C$

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int \frac{2{x}^{2}-4}{2x}\,\text{d}x & =\int (\frac{2{x}^{2}}{2x}-\frac{2}{x})\text{d}x \\  & =\int (1x-\frac{2}{x})\text{d}x \\  & =1\int x\,\text{d}x-2\int \frac{1}{x}\,\text{d}x \\  & =\frac{1}{2}{x}^{2}-2\ln|x|+C.\end{aligned}
$$

---

## q-103593 — easy

{"p": "3/2", "b": "1/2"}

Calculate $\int ({x}^{3/2}+\frac{1}{2}{x}^{-1})\,\text{d}x.$

- $\frac{2 x^{\frac{5}{2}}}{5} + \frac{\ln|x|}{2}+C$ **correct**

- $\frac{5 x^{\frac{5}{2}}}{2} + 2 \ln|x|+C$

- $\frac{5 x^{\frac{3}{2}}}{2} + \frac{\ln|x|}{2}+C$

- $\frac{3 x^{\frac{5}{2}}}{2} + 2 \ln|x|+C$

- $\frac{3 x^{\frac{3}{2}}}{2} + 2 \ln|x|+C$

First, we apply the sum rule and get

$$
\int ({x}^{3/2}+\frac{1}{2}{x}^{-1})\,\text{d}x=\int {x}^{3/2}\,\text{d}x+\frac{1}{2}\int \frac{1}{x}\,\text{d}x
$$

Now, using the power rule in the first term, and taking out the coefficient in the second term, we get

$$
\begin{aligned}\int {x}^{3/2}\,\text{d}x+\frac{1}{2}\int \frac{1}{x}\,\text{d}x & =\frac{{x}^{3/2+1}}{\frac{3}{2}+1}+\frac{1}{2}\ln|x|+C \\  & =\frac{2}{5}{x}^{5/2}+\frac{1}{2}\ln|x|+C.\end{aligned}
$$

---

## q-103593 — easy

{"p": "1/2", "b": "1/2"}

Calculate $\int ({x}^{1/2}+\frac{1}{2}{x}^{-1})\,\text{d}x.$

- $\frac{2 x^{\frac{3}{2}}}{3} + \frac{\ln|x|}{2}+C$ **correct**

- $\frac{3 x^{\frac{3}{2}}}{2} + 2 \ln|x|+C$

- $\frac{3 \sqrt{x}}{2} + \frac{\ln|x|}{2}+C$

- $\frac{x^{\frac{3}{2}}}{2} + 2 \ln|x|+C$

- $\frac{\sqrt{x}}{2} + 2 \ln|x|+C$

First, we apply the sum rule and get

$$
\int ({x}^{1/2}+\frac{1}{2}{x}^{-1})\,\text{d}x=\int {x}^{1/2}\,\text{d}x+\frac{1}{2}\int \frac{1}{x}\,\text{d}x
$$

Now, using the power rule in the first term, and taking out the coefficient in the second term, we get

$$
\begin{aligned}\int {x}^{1/2}\,\text{d}x+\frac{1}{2}\int \frac{1}{x}\,\text{d}x & =\frac{{x}^{1/2+1}}{\frac{1}{2}+1}+\frac{1}{2}\ln|x|+C \\  & =\frac{2}{3}{x}^{3/2}+\frac{1}{2}\ln|x|+C.\end{aligned}
$$

---

## q-29885 — easy

{"n": 2, "r": 2}

Calculate $\int ({x}^{2/3}+\frac{\sqrt{2}}{x})\,\text{d}x.$

- $\frac{3 x^{\frac{5}{3}} \ln{\left(x \right)}}{5} + \ln{\left(x \right)}+C$

- $\frac{7 x^{\frac{4}{3}}}{5} + 2 \ln|x|+C$

- $\frac{11 x^{\frac{11}{3}}}{5} + \sqrt{5} \ln|x|+C$

- $\frac{3 x^{\frac{5}{3}}}{5} + \sqrt{2} \ln|x|+C$ **correct**

- $\frac{9 x^{\frac{7}{3}}}{5} + \sqrt{3} \ln|x|+C$

First, we apply the sum rule and get

$$
\int ({x}^{2/3}+\frac{\sqrt{2}}{x})\,\text{d}x=\int {x}^{2/3}\,\text{d}x+\sqrt{2}\int \frac{1}{x}\,\text{d}x
$$

Now, using the power rule in the first term, and taking out the coefficient in the second term, we get

$$
\begin{aligned}\int {x}^{2/3}\,\text{d}x+\sqrt{2}\int \frac{1}{x}\,\text{d}x & =\frac{{x}^{2/3+1}}{\frac{2}{3}+1}+\sqrt{2}\ln|x|+C \\  & =\frac{3}{5}{x}^{5/3}+\sqrt{2}\ln|x|+C.\end{aligned}
$$

---

## q-29885 — easy

{"n": 1, "r": 2}

Calculate $\int ({x}^{1/3}+\frac{\sqrt{2}}{x})\,\text{d}x.$

- $\frac{3 x^{\frac{4}{3}} \ln{\left(x \right)}}{4} + \ln{\left(x \right)}+C$

- $\frac{3 x}{2} + 2 \ln|x|+C$

- $\frac{5 x^{\frac{10}{3}}}{2} + \sqrt{5} \ln|x|+C$

- $\frac{3 x^{\frac{4}{3}}}{4} + \sqrt{2} \ln|x|+C$ **correct**

- $2 x^{2} + \sqrt{3} \ln|x|+C$

First, we apply the sum rule and get

$$
\int ({x}^{1/3}+\frac{\sqrt{2}}{x})\,\text{d}x=\int {x}^{1/3}\,\text{d}x+\sqrt{2}\int \frac{1}{x}\,\text{d}x
$$

Now, using the power rule in the first term, and taking out the coefficient in the second term, we get

$$
\begin{aligned}\int {x}^{1/3}\,\text{d}x+\sqrt{2}\int \frac{1}{x}\,\text{d}x & =\frac{{x}^{1/3+1}}{\frac{1}{3}+1}+\sqrt{2}\ln|x|+C \\  & =\frac{3}{4}{x}^{4/3}+\sqrt{2}\ln|x|+C.\end{aligned}
$$

---

## q-29886 — easy

{"a": 2, "n": 7, "d": 3}

Find the integral of $2{x}^{7/3}-\frac{1}{3x}$ with respect to $x.$

- $\frac{7 x^{\frac{2}{3}}}{2} - \ln|x|+C$

- $\frac{5 x^{\frac{7}{3}}}{2} - 3 \ln|x|+C$

- $\frac{3 x^{\frac{10}{3}}}{5} - \frac{\ln|x|}{3}+C$ **correct**

- $\frac{7 x^{\frac{7}{3}}}{5} - 3 \ln|x|+C$

- $\frac{\sqrt[3]{x}}{5} - \frac{\ln|x|}{3}+C$

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (2{x}^{7/3}-\frac{1}{3x})\text{d}x & =\int 2{x}^{7/3}\,\text{d}x-\frac{1}{3}\int \frac{1}{x}\,\text{d}x \\  & =2\cdot \frac{{x}^{7/3+1}}{(\frac{7}{3}+1)}-\frac{1}{3}\ln|x|+C \\  & =\frac{3}{5}{x}^{10/3}-\frac{1}{3}\ln|x|+C.\end{aligned}
$$

---

## q-29886 — easy

{"a": 2, "n": 4, "d": 2}

Find the integral of $2{x}^{4/3}-\frac{1}{2x}$ with respect to $x.$

- $- \ln|x| + \frac{2}{\sqrt[3]{x}}+C$

- $x^{\frac{4}{3}} - 2 \ln|x|+C$

- $\frac{6 x^{\frac{7}{3}}}{7} - \frac{\ln|x|}{2}+C$ **correct**

- $2 x^{\frac{4}{3}} - 2 \ln|x|+C$

- $- \frac{\ln|x|}{2} + \frac{1}{2 x^{\frac{2}{3}}}+C$

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (2{x}^{4/3}-\frac{1}{2x})\text{d}x & =\int 2{x}^{4/3}\,\text{d}x-\frac{1}{2}\int \frac{1}{x}\,\text{d}x \\  & =2\cdot \frac{{x}^{4/3+1}}{(\frac{4}{3}+1)}-\frac{1}{2}\ln|x|+C \\  & =\frac{6}{7}{x}^{7/3}-\frac{1}{2}\ln|x|+C.\end{aligned}
$$

---

## q-29888 — easy

{"a": 3, "b": 3}

Find the integral of $\frac{3}{{x}^{-1}}+3{x}^{-1}$ with respect to $x.$

- $\frac{x^{2}}{2} + 3 \ln|x|+C$

- $\frac{4 x^{2}}{3} + 5 \ln|x|+C$

- $\frac{3 x^{2}}{2} + 3 \ln|x|+C$ **correct**

- $\frac{5 x^{2}}{2} + 4 \ln|x|+C$

- $\frac{2 x^{2}}{3} + 2 \ln|x|+C$

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (\frac{3}{{x}^{-1}}+3{x}^{-1})\text{d}x & =3\int x\,\text{d}x+3\int \frac{1}{x}\,\text{d}x \\  & =\frac{3}{2}{x}^{2}+3\ln|x|+C.\end{aligned}
$$

---

## q-29888 — easy

{"a": 3, "b": 2}

Find the integral of $\frac{3}{{x}^{-1}}+2{x}^{-1}$ with respect to $x.$

- $\frac{x^{2}}{2} + 2 \ln|x|+C$

- $2 x^{2} + 4 \ln|x|+C$

- $\frac{3 x^{2}}{2} + 2 \ln|x|+C$ **correct**

- $\frac{5 x^{2}}{2} + 3 \ln|x|+C$

- $x^{2} + \ln|x|+C$

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (\frac{3}{{x}^{-1}}+2{x}^{-1})\text{d}x & =3\int x\,\text{d}x+2\int \frac{1}{x}\,\text{d}x \\  & =\frac{3}{2}{x}^{2}+2\ln|x|+C.\end{aligned}
$$

---

## q-29836 — easy

{"a": 3, "d": 5, "b": 3}

Find the integral of $\frac{3}{5x} + 3x$ with respect to $x$.

- $\frac{5 x^{2}}{2} + \frac{7 \ln|x|}{5}+C$

- $\frac{3 x^{2}}{2} + \frac{3 \ln|x|}{5}+C$ **correct**

- $\frac{7 x^{2}}{2} + \ln{\left(x \right)}+C$

- $\frac{5 x^{2}}{2} + \frac{3 \ln{\left(x \right)}}{5}+C$

- $\frac{x^{2}}{2} + \frac{5 \ln|x|}{3}+C$

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (\frac{3}{5x}+3x)\,\text{d}x & =\int \frac{3}{5x}\,\text{d}x+3\int x\,\text{d}x \\  & =\frac{3}{5}\int \frac{1}{x}\,\text{d}x+3\int x\,\text{d}x \\  & =\frac{3}{5}\ln|x|+3\cdot\frac{x^{1+1}}{1+1}+C \\  & =\frac{3 x^{2}}{2} + \frac{3 \ln|x|}{5}+C.\end{aligned}
$$

---

## q-29836 — easy

{"a": 2, "d": 5, "b": 2}

Find the integral of $\frac{2}{5x} + 2x$ with respect to $x$.

- $\frac{5 x^{2}}{2} + \frac{6 \ln|x|}{5}+C$

- $x^{2} + \frac{2 \ln|x|}{5}+C$ **correct**

- $3 x^{2} + \ln{\left(x \right)}+C$

- $\frac{5 x^{2}}{2} + \frac{2 \ln{\left(x \right)}}{5}+C$

- $\frac{x^{2}}{2} + \frac{5 \ln|x|}{2}+C$

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (\frac{2}{5x}+2x)\,\text{d}x & =\int \frac{2}{5x}\,\text{d}x+2\int x\,\text{d}x \\  & =\frac{2}{5}\int \frac{1}{x}\,\text{d}x+2\int x\,\text{d}x \\  & =\frac{2}{5}\ln|x|+2\cdot\frac{x^{1+1}}{1+1}+C \\  & =x^{2} + \frac{2 \ln|x|}{5}+C.\end{aligned}
$$

---

## q-29857 — easy

{"a": 2, "b": 1}

Find the integral of $\frac{2}{x} - \frac{1}{\sqrt{x}}$ with respect to $x$.

- $- 2 \sqrt{x} + x+C$

- $- \sqrt{x} + \ln|x|+C$

- $2 \ln|x| - \frac{2}{x}+C$

- $2 \sqrt{x} + \ln|x|+C$

- $- 2 \sqrt{x} + 2 \ln|x|+C$ **correct**

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (2/x-1/\sqrt{x})\,\text{d}x & =2\int \frac{1}{x}\,\text{d}x-1\int x^{-1/2}\,\text{d}x \\  & =2\ln|x|-1\cdot\frac{x^{-1/2+1}}{-1/2+1}+C \\  & =- 2 \sqrt{x} + 2 \ln|x|+C.\end{aligned}
$$

---

## q-29857 — easy

{"a": 2, "b": 2}

Find the integral of $\frac{2}{x} - \frac{2}{\sqrt{x}}$ with respect to $x$.

- $- 4 \sqrt{x} + x+C$

- $- 2 \sqrt{x} + 2 \ln|x|+C$

- $2 \ln|x| - \frac{4}{x}+C$

- $4 \sqrt{x} + 2 \ln|x|+C$

- $- 4 \sqrt{x} + 2 \ln|x|+C$ **correct**

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (2/x-2/\sqrt{x})\,\text{d}x & =2\int \frac{1}{x}\,\text{d}x-2\int x^{-1/2}\,\text{d}x \\  & =2\ln|x|-2\cdot\frac{x^{-1/2+1}}{-1/2+1}+C \\  & =- 4 \sqrt{x} + 2 \ln|x|+C.\end{aligned}
$$

---

## q-49100 — moderate

{"a": 2, "c": 1}

Find the integral of ${(2-\frac{1}{x})}^{2}$ with respect to $x.$

- $2 x - \ln|x|+C$

- $\ln{\left(\left|{2 - \frac{1}{x}}\right| \right)}+C$

- $2 x \ln|x|+C$

- $\left(2 x - \ln|x|\right)^{2}+C$

- $4 x - 4 \ln|x| - \frac{1}{x}+C$ **correct**

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(2-\frac{1}{x})}^{2}\text{d}x & =\int (4-\frac{4}{x}+\frac{1}{{x}^{2}})\text{d}x \\  & =\int 4\,\text{d}x-\int \frac{4}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =4\int \text{d}x-4\int \frac{1}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =4x-4\ln|x|+\frac{{x}^{-2+1}}{-2+1}+C \\  & =4x-4\ln|x|-\frac{1}{x}+C.\end{aligned}
$$

---

## q-49100 — moderate

{"a": 2, "c": 3}

Find the integral of ${(2-\frac{3}{x})}^{2}$ with respect to $x.$

- $2 x - 3 \ln|x|+C$

- $\ln{\left(\left|{2 - \frac{3}{x}}\right| \right)}+C$

- $6 x \ln|x|+C$

- $\left(2 x - 3 \ln|x|\right)^{2}+C$

- $4 x - 12 \ln|x| - \frac{9}{x}+C$ **correct**

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(2-\frac{3}{x})}^{2}\text{d}x & =\int (4-\frac{12}{x}+\frac{9}{{x}^{2}})\text{d}x \\  & =\int 4\,\text{d}x-\int \frac{12}{x}\,\text{d}x+\int \frac{9}{{x}^{2}}\,\text{d}x \\  & =4\int \text{d}x-12\int \frac{1}{x}\,\text{d}x+9\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =4x-12\ln|x|+9\frac{{x}^{-2+1}}{-2+1}+C \\  & =4x-12\ln|x|-\frac{9}{x}+C.\end{aligned}
$$

---

## q-29915 — hard

{"m": 3, "a": 1, "b": 5}

Find the integral of $\frac{\sqrt{{x}^{3}}}{\sqrt{{x}^{5}}}-5{x}^{-1}$ with respect to $x.$

- $4 \ln|x|+C$

- $- 4 \ln|x|+C$ **correct**

- $- 5 \ln|x|+C$

- $5 x+C$

- $- 6 x+C$

Simplifying the exponents and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (\frac{\sqrt{{x}^{3}}}{\sqrt{{x}^{5}}}-5{x}^{-1})\text{d}x & =\int \frac{1}{{x}^{5/2-3/2}}\,\text{d}x-5\int \frac{1}{x}\,\text{d}x \\  & =\int \frac{1}{x}\,\text{d}x-5\int \frac{1}{x}\,\text{d}x \\  & =-4\int \frac{1}{x}\,\text{d}x \\  & =-4\ln|x|+C.\end{aligned}
$$

---

## q-29915 — hard

{"m": 1, "a": 1, "b": 2}

Find the integral of $\frac{\sqrt{{x}^{1}}}{\sqrt{{x}^{3}}}-2{x}^{-1}$ with respect to $x.$

- $\ln|x|+C$

- $- \ln|x|+C$ **correct**

- $- 2 \ln|x|+C$

- $2 x+C$

- $- 3 x+C$

Simplifying the exponents and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (\frac{\sqrt{{x}^{1}}}{\sqrt{{x}^{3}}}-2{x}^{-1})\text{d}x & =\int \frac{1}{{x}^{3/2-1/2}}\,\text{d}x-2\int \frac{1}{x}\,\text{d}x \\  & =\int \frac{1}{x}\,\text{d}x-2\int \frac{1}{x}\,\text{d}x \\  & =-1\int \frac{1}{x}\,\text{d}x \\  & =-1\ln|x|+C.\end{aligned}
$$
