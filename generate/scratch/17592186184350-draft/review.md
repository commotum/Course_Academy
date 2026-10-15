## q-31420 — observed original and changed-base evidence profile

Original exact evidence replay:

Calculate the integral $\int x{8}^{3{x}^{2}}\,\text{d}x.$

- \frac{{8}^{3{x}^{2}}}{3\operatorname{ln}⁡8}+C
- \frac{{8}^{3{x}^{2}}}{\operatorname{ln}⁡8}+C
- \frac{{8}^{3x}}{2\operatorname{ln}⁡8}+C
- \frac{{8}^{3{x}^{2}}}{6\operatorname{ln}⁡8}+C (correct)
- \frac{x{8}^{3{x}^{2}}}{6\operatorname{ln}⁡8}+C

Let's introduce the new variable $u=3{x}^{2}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=6x\,⟹\,\frac{1}{6}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{8}^{3{x}^{2}}\,\text{d}x & =\int {8}^{3{x}^{2}}\cdot x\,\text{d}x \\  & =\int {8}^{u}\cdot \frac{1}{6}\,\text{d}u \\  & =\frac{1}{6}\int {8}^{u}\,\text{d}u \\  & =\frac{1}{6}\frac{{8}^{u}}{\operatorname{ln}⁡8}+C \\  & =\frac{{8}^{3{x}^{2}}}{6\operatorname{ln}⁡8}+C.\end{aligned}
$$

Generated variant:

Calculate the integral $\int x{2}^{3{x}^{2}}\,\text{d}x.$

- \frac{{2}^{3{x}^{2}}}{3\operatorname{ln}⁡2}+C
- \frac{x{2}^{3{x}^{2}}}{6\operatorname{ln}⁡2}+C
- \frac{{2}^{3{x}^{2}}}{6\operatorname{ln}⁡2}+C (correct)
- \frac{{2}^{3x}}{2\operatorname{ln}⁡2}+C
- \frac{{2}^{3{x}^{2}}}{\operatorname{ln}⁡2}+C

Let's introduce the new variable $u=3{x}^{2}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=6x\,⟹\,\frac{1}{6}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{2}^{3{x}^{2}}\,\text{d}x & =\int {2}^{3{x}^{2}}\cdot x\,\text{d}x \\  & =\int {2}^{u}\cdot \frac{1}{6}\,\text{d}u \\  & =\frac{1}{6}\int {2}^{u}\,\text{d}u \\  & =\frac{1}{6}\frac{{2}^{u}}{\operatorname{ln}⁡2}+C \\  & =\frac{{2}^{3{x}^{2}}}{6\operatorname{ln}⁡2}+C.\end{aligned}
$$

## q-73800 — observed original and changed-base evidence profile

Original exact evidence replay:

Calculate the integral $\displaystyle \int3x^{2}3^{x^{3} - 5}dx$.

- \frac{3^{x^{3} - 5}}{2\ln 3} + C
- 3^{x^{3} - 5} + C
- \frac{3^{x^{3} - 5}}{2} + C
- 2 \cdot 3^{x^{3} - 5} + C
- \frac{3^{x^{3} - 5}}{\ln 3} + C

[Raw source has no worked solution or correct designation.]

Generated variant:

Calculate the integral $\displaystyle \int3x^{2}2^{x^{3} - 5}dx$.

- \frac{2^{x^{3} - 5}}{2\ln 2} + C
- \frac{2^{x^{3} - 5}}{\ln 2} + C
- 2 \cdot 2^{x^{3} - 5} + C
- \frac{2^{x^{3} - 5}}{2} + C
- 2^{x^{3} - 5} + C

[Raw source has no worked solution or correct designation.]

## q-211989 — observed original and changed-base evidence profile

Original exact evidence replay:

Calculate the integral $\int {x}^{2}{4}^{{x}^{3}/5}\,\text{d}x.$

- \frac{5\cdot {4}^{{x}^{3}}}{\operatorname{ln}⁡4}+C
- \frac{5\cdot {4}^{{x}^{3}/5}}{3\operatorname{ln}⁡4}+C (correct)
- \frac{3\cdot {4}^{{x}^{3}/5}}{5\operatorname{ln}⁡4}+C
- \frac{{4}^{{x}^{3}}}{\operatorname{ln}⁡4}+C
- \frac{{4}^{{x}^{3}/5}}{3}+C

Let's introduce the new variable $u=\frac{{x}^{3}}{5}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=\frac{3}{5}{x}^{2}\,⟹\,\frac{5}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int {x}^{2}{4}^{{x}^{3}/5}\,\text{d}x & =\int {4}^{{x}^{3}/5}\cdot {x}^{2}\,\text{d}x \\  & =\int {4}^{u}\cdot \frac{5}{3}\,\text{d}u \\  & =\frac{5}{3}\int {4}^{u}\,\text{d}u \\  & =\frac{5\cdot {4}^{u}}{3\operatorname{ln}⁡4}+C \\  & =\frac{5\cdot {4}^{{x}^{3}/5}}{3\operatorname{ln}⁡4}+C.\end{aligned}
$$

Generated variant:

Calculate the integral $\int {x}^{2}{2}^{{x}^{3}/5}\,\text{d}x.$

- \frac{5\cdot {2}^{{x}^{3}}}{\operatorname{ln}⁡2}+C
- \frac{{2}^{{x}^{3}/5}}{3}+C
- \frac{{2}^{{x}^{3}}}{\operatorname{ln}⁡2}+C
- \frac{3\cdot {2}^{{x}^{3}/5}}{5\operatorname{ln}⁡2}+C
- \frac{5\cdot {2}^{{x}^{3}/5}}{3\operatorname{ln}⁡2}+C (correct)

Let's introduce the new variable $u=\frac{{x}^{3}}{5}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=\frac{3}{5}{x}^{2}\,⟹\,\frac{5}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int {x}^{2}{2}^{{x}^{3}/5}\,\text{d}x & =\int {2}^{{x}^{3}/5}\cdot {x}^{2}\,\text{d}x \\  & =\int {2}^{u}\cdot \frac{5}{3}\,\text{d}u \\  & =\frac{5}{3}\int {2}^{u}\,\text{d}u \\  & =\frac{5\cdot {2}^{u}}{3\operatorname{ln}⁡2}+C \\  & =\frac{5\cdot {2}^{{x}^{3}/5}}{3\operatorname{ln}⁡2}+C.\end{aligned}
$$

## q-31419 — observed original and changed-base evidence profile

Original exact evidence replay:

Calculate the integral $\int x{4}^{{x}^{2}-7}\,\text{d}x.$

- \frac{{4}^{{x}^{2}-7}}{\operatorname{ln}⁡4}+C
- \frac{{4}^{x}}{2\operatorname{ln}⁡4}+C
- \frac{{4}^{x-7}}{\operatorname{ln}⁡4}+C
- \frac{{4}^{{x}^{2}-7}}{2}+C
- \frac{{4}^{{x}^{2}-7}}{2\operatorname{ln}⁡4}+C (correct)

Let's introduce the new variable $u={x}^{2}-7.$ Differentiating gives 

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{4}^{{x}^{2}-7}\,\text{d}x & =\int {4}^{{x}^{2}-7}\cdot x\,\text{d}x \\  & =\int {4}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {4}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{4}^{u}}{\operatorname{ln}⁡4}+C \\  & =\frac{{4}^{{x}^{2}-7}}{2\operatorname{ln}⁡4}+C.\end{aligned}
$$

Generated variant:

Calculate the integral $\int x{2}^{{x}^{2}-7}\,\text{d}x.$

- \frac{{2}^{{x}^{2}-7}}{\operatorname{ln}⁡2}+C
- \frac{{2}^{{x}^{2}-7}}{2\operatorname{ln}⁡2}+C (correct)
- \frac{{2}^{{x}^{2}-7}}{2}+C
- \frac{{2}^{x-7}}{\operatorname{ln}⁡2}+C
- \frac{{2}^{x}}{2\operatorname{ln}⁡2}+C

Let's introduce the new variable $u={x}^{2}-7.$ Differentiating gives 

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{2}^{{x}^{2}-7}\,\text{d}x & =\int {2}^{{x}^{2}-7}\cdot x\,\text{d}x \\  & =\int {2}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {2}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{2}^{u}}{\operatorname{ln}⁡2}+C \\  & =\frac{{2}^{{x}^{2}-7}}{2\operatorname{ln}⁡2}+C.\end{aligned}
$$

## q-31426 — observed original and changed-base evidence profile

Original exact evidence replay:

Calculate the integral $\int x{5}^{{x}^{2}/3}\,\text{d}x.$

- \frac{3\cdot {5}^{{x}^{2}/3}}{\operatorname{ln}⁡5}+C
- \frac{{5}^{{x}^{2}/3}}{2}+C
- \frac{3\cdot {5}^{{x}^{2}/3}}{2\operatorname{ln}⁡5}+C (correct)
- \frac{{5}^{x/3}}{\operatorname{ln}⁡5}+C
- \frac{{5}^{{x}^{2}/3}}{\operatorname{ln}⁡5}+C

Let's introduce the new variable $u=\frac{{x}^{2}}{3}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=\frac{2}{3}x\,⟹\,\frac{3}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{5}^{{x}^{2}/3}\,\text{d}x & =\int {5}^{{x}^{2}/3}\cdot x\,\text{d}x \\  & =\int {5}^{u}\cdot \frac{3}{2}\,\text{d}u \\  & =\frac{3}{2}\int {5}^{u}\,\text{d}u \\  & =\frac{3}{2}\frac{{5}^{u}}{\operatorname{ln}⁡5}+C \\  & =\frac{3\cdot {5}^{{x}^{2}/3}}{2\operatorname{ln}⁡5}+C.\end{aligned}
$$

Generated variant:

Calculate the integral $\int x{2}^{{x}^{2}/3}\,\text{d}x.$

- \frac{3\cdot {2}^{{x}^{2}/3}}{\operatorname{ln}⁡2}+C
- \frac{{2}^{{x}^{2}/3}}{\operatorname{ln}⁡2}+C
- \frac{{2}^{x/3}}{\operatorname{ln}⁡2}+C
- \frac{3\cdot {2}^{{x}^{2}/3}}{2\operatorname{ln}⁡2}+C (correct)
- \frac{{2}^{{x}^{2}/3}}{2}+C

Let's introduce the new variable $u=\frac{{x}^{2}}{3}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=\frac{2}{3}x\,⟹\,\frac{3}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{2}^{{x}^{2}/3}\,\text{d}x & =\int {2}^{{x}^{2}/3}\cdot x\,\text{d}x \\  & =\int {2}^{u}\cdot \frac{3}{2}\,\text{d}u \\  & =\frac{3}{2}\int {2}^{u}\,\text{d}u \\  & =\frac{3}{2}\frac{{2}^{u}}{\operatorname{ln}⁡2}+C \\  & =\frac{3\cdot {2}^{{x}^{2}/3}}{2\operatorname{ln}⁡2}+C.\end{aligned}
$$

## q-73665 — observed original and changed-base evidence profile

Original exact evidence replay:

Calculate the integral $\int 4x\,{4}^{4{x}^{2}-3}\,\text{d}x.$

- \frac{2\cdot {4}^{4{x}^{2}-3}}{\operatorname{ln}⁡4}+C
- {4}^{4{x}^{2}-3}+C
- {4}^{4{x}^{2}-3}\,\operatorname{ln}⁡4+C
- \frac{{4}^{4{x}^{2}-3}}{2\operatorname{ln}⁡4}+C (correct)
- \frac{{4}^{4{x}^{2}-3}}{4\operatorname{ln}⁡4}+C

Let's introduce the new variable $u=4{x}^{2}-3.$ Differentiating gives 

$$
\frac{\text{d}u}{\text{d}x}=8x\,⟹\,\frac{1}{8}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 4x\,{4}^{4{x}^{2}-3}\,\text{d}x & =4\int {4}^{4{x}^{2}-3}\cdot x\,\text{d}x \\  & =4\int {4}^{u}\cdot \frac{1}{8}\,\text{d}u \\  & =\frac{1}{2}\int {4}^{u}\,\text{d}u \\  & =\frac{{4}^{u}}{2\operatorname{ln}⁡4}+C \\  & =\frac{{4}^{4{x}^{2}-3}}{2\operatorname{ln}⁡4}+C.\end{aligned}
$$

Generated variant:

Calculate the integral $\int 4x\,{2}^{4{x}^{2}-3}\,\text{d}x.$

- \frac{2\cdot {2}^{4{x}^{2}-3}}{\operatorname{ln}⁡2}+C
- \frac{{2}^{4{x}^{2}-3}}{4\operatorname{ln}⁡2}+C
- \frac{{2}^{4{x}^{2}-3}}{2\operatorname{ln}⁡2}+C (correct)
- {2}^{4{x}^{2}-3}\,\operatorname{ln}⁡2+C
- {2}^{4{x}^{2}-3}+C

Let's introduce the new variable $u=4{x}^{2}-3.$ Differentiating gives 

$$
\frac{\text{d}u}{\text{d}x}=8x\,⟹\,\frac{1}{8}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 4x\,{2}^{4{x}^{2}-3}\,\text{d}x & =4\int {2}^{4{x}^{2}-3}\cdot x\,\text{d}x \\  & =4\int {2}^{u}\cdot \frac{1}{8}\,\text{d}u \\  & =\frac{1}{2}\int {2}^{u}\,\text{d}u \\  & =\frac{{2}^{u}}{2\operatorname{ln}⁡2}+C \\  & =\frac{{2}^{4{x}^{2}-3}}{2\operatorname{ln}⁡2}+C.\end{aligned}
$$

## q-73801 — observed original and changed-base evidence profile

Original exact evidence replay:

Calculate the integral $\int 2x{6}^{{x}^{2}+1}\,\text{d}x.$

- \frac{{6}^{{x}^{2}+1}\operatorname{ln}⁡6}{3}+C
- \frac{{6}^{{x}^{2}+1}}{\operatorname{ln}⁡6}+C (correct)
- \frac{{6}^{{x}^{2}+1}}{6}+C
- {6}^{{x}^{2}+1}\operatorname{ln}⁡3+C
- {6}^{{x}^{2}+1}+C

Let's introduce the new variable $u={x}^{2}+1.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\text{d}u=2x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 2x{6}^{{x}^{2}+1}\,\text{d}x & =\int {6}^{{x}^{2}+1}\cdot 2x\,\text{d}x \\  & =\int {6}^{u}\cdot \,\text{d}u \\  & =\frac{{6}^{u}}{\operatorname{ln}⁡6}+C \\  & =\frac{{6}^{{x}^{2}+1}}{\operatorname{ln}⁡6}+C.\end{aligned}
$$

Generated variant:

Calculate the integral $\int 2x{2}^{{x}^{2}+1}\,\text{d}x.$

- \frac{{2}^{{x}^{2}+1}\operatorname{ln}⁡2}{3}+C
- {2}^{{x}^{2}+1}+C
- {2}^{{x}^{2}+1}\operatorname{ln}⁡3+C
- \frac{{2}^{{x}^{2}+1}}{6}+C
- \frac{{2}^{{x}^{2}+1}}{\operatorname{ln}⁡2}+C (correct)

Let's introduce the new variable $u={x}^{2}+1.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\text{d}u=2x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 2x{2}^{{x}^{2}+1}\,\text{d}x & =\int {2}^{{x}^{2}+1}\cdot 2x\,\text{d}x \\  & =\int {2}^{u}\cdot \,\text{d}u \\  & =\frac{{2}^{u}}{\operatorname{ln}⁡2}+C \\  & =\frac{{2}^{{x}^{2}+1}}{\operatorname{ln}⁡2}+C.\end{aligned}
$$

## q-73802 — observed original and changed-base evidence profile

Original exact evidence replay:

Calculate the integral $\int x{7}^{{x}^{2}-7}\,\text{d}x.$

- \frac{{7}^{{x}^{2}-7}\operatorname{ln}⁡7}{2}+C
- \frac{{7}^{{x}^{2}-7}}{2\operatorname{ln}⁡7}+C (correct)
- \frac{2\cdot {7}^{{x}^{2}-7}}{\operatorname{ln}⁡7}+C
- {7}^{{x}^{2}-7}+C
- \frac{{7}^{{x}^{2}-7}}{2}+C

Let's introduce the new variable $u={x}^{2}-7.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{7}^{{x}^{2}-7}\,\text{d}x & =\int {7}^{{x}^{2}-7}\cdot x\,\text{d}x \\  & =\int {7}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {7}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{7}^{u}}{\operatorname{ln}⁡7}+C \\  & =\frac{{7}^{{x}^{2}-7}}{2\operatorname{ln}⁡7}+C.\end{aligned}
$$

Generated variant:

Calculate the integral $\int x{2}^{{x}^{2}-7}\,\text{d}x.$

- \frac{{2}^{{x}^{2}-7}\operatorname{ln}⁡2}{2}+C
- \frac{{2}^{{x}^{2}-7}}{2}+C
- {2}^{{x}^{2}-7}+C
- \frac{2\cdot {2}^{{x}^{2}-7}}{\operatorname{ln}⁡2}+C
- \frac{{2}^{{x}^{2}-7}}{2\operatorname{ln}⁡2}+C (correct)

Let's introduce the new variable $u={x}^{2}-7.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{2}^{{x}^{2}-7}\,\text{d}x & =\int {2}^{{x}^{2}-7}\cdot x\,\text{d}x \\  & =\int {2}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {2}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{2}^{u}}{\operatorname{ln}⁡2}+C \\  & =\frac{{2}^{{x}^{2}-7}}{2\operatorname{ln}⁡2}+C.\end{aligned}
$$

## q-31420 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int x{5}^{3{x}^{2}}\,\text{d}x.$

- \frac{5^{3 x^{2}}}{6}+C
- \frac{5^{3 x^{2}}}{6 \ln{\left(5 \right)}}+C (correct)
- \frac{5^{3 x^{2}}}{\ln{\left(5 \right)}}+C
- \frac{6 \cdot 5^{3 x^{2}}}{\ln{\left(5 \right)}}+C
- \frac{5^{3 x^{2}} \ln{\left(5 \right)}}{6}+C

Let's introduce the new variable $u=3{x}^{2}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=6x\,⟹\,\frac{1}{6}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{5}^{3{x}^{2}}\,\text{d}x & =\int {5}^{3{x}^{2}}\cdot x\,\text{d}x \\  & =\int {5}^{u}\cdot \frac{1}{6}\,\text{d}u \\  & =\frac{1}{6}\int {5}^{u}\,\text{d}u \\  & =\frac{1}{6}\frac{{5}^{u}}{\operatorname{ln}⁡5}+C \\  & =\frac{{5}^{3{x}^{2}}}{6\operatorname{ln}⁡5}+C.\end{aligned}
$$

## q-31420 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int x{12}^{5{x}^{2}}\,\text{d}x.$

- \frac{12^{5 x^{2}}}{10}+C
- \frac{10 \cdot 12^{5 x^{2}}}{\ln{\left(12 \right)}}+C
- \frac{12^{5 x^{2}}}{10 \ln{\left(12 \right)}}+C (correct)
- \frac{12^{5 x^{2}}}{\ln{\left(12 \right)}}+C
- \frac{12^{5 x^{2}} \ln{\left(12 \right)}}{10}+C

Let's introduce the new variable $u=5{x}^{2}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=10x\,⟹\,\frac{1}{10}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{12}^{5{x}^{2}}\,\text{d}x & =\int {12}^{5{x}^{2}}\cdot x\,\text{d}x \\  & =\int {12}^{u}\cdot \frac{1}{10}\,\text{d}u \\  & =\frac{1}{10}\int {12}^{u}\,\text{d}u \\  & =\frac{1}{10}\frac{{12}^{u}}{\operatorname{ln}⁡12}+C \\  & =\frac{{12}^{5{x}^{2}}}{10\operatorname{ln}⁡12}+C.\end{aligned}
$$

## q-31419 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int x{5}^{{x}^{2}-1}\,\text{d}x.$

- \frac{5^{x^{2} - 1}}{2 \ln{\left(5 \right)}}+C (correct)
- \frac{5^{x^{2} - 1}}{\ln{\left(5 \right)}}+C
- \frac{2 \cdot 5^{x^{2} - 1}}{\ln{\left(5 \right)}}+C
- \frac{5^{x^{2} - 1} \ln{\left(5 \right)}}{2}+C
- \frac{5^{x^{2} - 1}}{2}+C

Let's introduce the new variable $u={x}^{2}-1.$ Differentiating gives 

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{5}^{{x}^{2}-1}\,\text{d}x & =\int {5}^{{x}^{2}-1}\cdot x\,\text{d}x \\  & =\int {5}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {5}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{5}^{u}}{\operatorname{ln}⁡5}+C \\  & =\frac{{5}^{{x}^{2}-1}}{2\operatorname{ln}⁡5}+C.\end{aligned}
$$

## q-31419 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int x{12}^{{x}^{2}-2}\,\text{d}x.$

- \frac{12^{x^{2} - 2}}{2}+C
- \frac{2 \cdot 12^{x^{2} - 2}}{\ln{\left(12 \right)}}+C
- \frac{12^{x^{2} - 2}}{2 \ln{\left(12 \right)}}+C (correct)
- \frac{12^{x^{2} - 2}}{\ln{\left(12 \right)}}+C
- \frac{12^{x^{2} - 2} \ln{\left(12 \right)}}{2}+C

Let's introduce the new variable $u={x}^{2}-2.$ Differentiating gives 

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{12}^{{x}^{2}-2}\,\text{d}x & =\int {12}^{{x}^{2}-2}\cdot x\,\text{d}x \\  & =\int {12}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {12}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{12}^{u}}{\operatorname{ln}⁡12}+C \\  & =\frac{{12}^{{x}^{2}-2}}{2\operatorname{ln}⁡12}+C.\end{aligned}
$$

## q-31426 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int x{5}^{{x}^{2}/7}\,\text{d}x.$

- \frac{7 \cdot 5^{\frac{x^{2}}{7}}}{2 \ln{\left(5 \right)}}+C (correct)
- \frac{7 \cdot 5^{\frac{x^{2}}{7}} \ln{\left(5 \right)}}{2}+C
- \frac{2 \cdot 5^{\frac{x^{2}}{7}}}{7 \ln{\left(5 \right)}}+C
- \frac{7 \cdot 5^{\frac{x^{2}}{7}}}{2}+C
- \frac{5^{\frac{x^{2}}{7}}}{\ln{\left(5 \right)}}+C

Let's introduce the new variable $u=\frac{{x}^{2}}{7}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=\frac{2}{7}x\,⟹\,\frac{7}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{5}^{{x}^{2}/7}\,\text{d}x & =\int {5}^{{x}^{2}/7}\cdot x\,\text{d}x \\  & =\int {5}^{u}\cdot \frac{7}{2}\,\text{d}u \\  & =\frac{7}{2}\int {5}^{u}\,\text{d}u \\  & =\frac{7}{2}\frac{{5}^{u}}{\operatorname{ln}⁡5}+C \\  & =\frac{7\cdot {5}^{{x}^{2}/7}}{2\operatorname{ln}⁡5}+C.\end{aligned}
$$

## q-31426 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int x{12}^{{x}^{2}/6}\,\text{d}x.$

- 3 \cdot 12^{\frac{x^{2}}{6}}+C
- \frac{12^{\frac{x^{2}}{6}}}{3 \ln{\left(12 \right)}}+C
- \frac{3 \cdot 12^{\frac{x^{2}}{6}}}{\ln{\left(12 \right)}}+C (correct)
- \frac{12^{\frac{x^{2}}{6}}}{\ln{\left(12 \right)}}+C
- 3 \cdot 12^{\frac{x^{2}}{6}} \ln{\left(12 \right)}+C

Let's introduce the new variable $u=\frac{{x}^{2}}{6}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=\frac{2}{6}x\,⟹\,\frac{6}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{12}^{{x}^{2}/6}\,\text{d}x & =\int {12}^{{x}^{2}/6}\cdot x\,\text{d}x \\  & =\int {12}^{u}\cdot \frac{6}{2}\,\text{d}u \\  & =\frac{6}{2}\int {12}^{u}\,\text{d}u \\  & =\frac{6}{2}\frac{{12}^{u}}{\operatorname{ln}⁡12}+C \\  & =\frac{6\cdot {12}^{{x}^{2}/6}}{2\operatorname{ln}⁡12}+C.\end{aligned}
$$

## q-73665 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int 3x\,{5}^{3{x}^{2}-4}\,\text{d}x.$

- \frac{5^{3 x^{2} - 4}}{2}+C
- \frac{5^{3 x^{2} - 4}}{2 \ln{\left(5 \right)}}+C (correct)
- \frac{5^{3 x^{2} - 4} \ln{\left(5 \right)}}{2}+C
- \frac{2 \cdot 5^{3 x^{2} - 4}}{\ln{\left(5 \right)}}+C
- \frac{5^{3 x^{2} - 4}}{\ln{\left(5 \right)}}+C

Let's introduce the new variable $u=3{x}^{2}-4.$ Differentiating gives 

$$
\frac{\text{d}u}{\text{d}x}=6x\,⟹\,\frac{1}{6}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 3x\,{5}^{3{x}^{2}-4}\,\text{d}x & =3\int {5}^{3{x}^{2}-4}\cdot x\,\text{d}x \\  & =3\int {5}^{u}\cdot \frac{1}{6}\,\text{d}u \\  & =\frac{1}{2}\int {5}^{u}\,\text{d}u \\  & =\frac{{5}^{u}}{2\operatorname{ln}⁡5}+C \\  & =\frac{{5}^{3{x}^{2}-4}}{2\operatorname{ln}⁡5}+C.\end{aligned}
$$

## q-73665 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int 5x\,{12}^{5{x}^{2}-1}\,\text{d}x.$

- \frac{12^{5 x^{2} - 1}}{2}+C
- \frac{2 \cdot 12^{5 x^{2} - 1}}{\ln{\left(12 \right)}}+C
- \frac{12^{5 x^{2} - 1}}{2 \ln{\left(12 \right)}}+C (correct)
- \frac{12^{5 x^{2} - 1}}{\ln{\left(12 \right)}}+C
- \frac{12^{5 x^{2} - 1} \ln{\left(12 \right)}}{2}+C

Let's introduce the new variable $u=5{x}^{2}-1.$ Differentiating gives 

$$
\frac{\text{d}u}{\text{d}x}=10x\,⟹\,\frac{1}{10}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 5x\,{12}^{5{x}^{2}-1}\,\text{d}x & =5\int {12}^{5{x}^{2}-1}\cdot x\,\text{d}x \\  & =5\int {12}^{u}\cdot \frac{1}{10}\,\text{d}u \\  & =\frac{1}{2}\int {12}^{u}\,\text{d}u \\  & =\frac{{12}^{u}}{2\operatorname{ln}⁡12}+C \\  & =\frac{{12}^{5{x}^{2}-1}}{2\operatorname{ln}⁡12}+C.\end{aligned}
$$

## q-73801 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int 2x{5}^{{x}^{2}+9}\,\text{d}x.$

- \frac{5^{x^{2} + 9}}{\ln{\left(5 \right)}}+C (correct)
- \frac{2 \cdot 5^{x^{2} + 9}}{\ln{\left(5 \right)}}+C
- \frac{5^{x^{2} + 9}}{2 \ln{\left(5 \right)}}+C
- 5^{x^{2} + 9} \ln{\left(5 \right)}+C
- 5^{x^{2} + 9}+C

Let's introduce the new variable $u={x}^{2}+9.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\text{d}u=2x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 2x{5}^{{x}^{2}+9}\,\text{d}x & =\int {5}^{{x}^{2}+9}\cdot 2x\,\text{d}x \\  & =\int {5}^{u}\cdot \,\text{d}u \\  & =\frac{{5}^{u}}{\operatorname{ln}⁡5}+C \\  & =\frac{{5}^{{x}^{2}+9}}{\operatorname{ln}⁡5}+C.\end{aligned}
$$

## q-73801 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int 2x{12}^{{x}^{2}+8}\,\text{d}x.$

- 12^{x^{2} + 8}+C
- \frac{12^{x^{2} + 8}}{2 \ln{\left(12 \right)}}+C
- \frac{12^{x^{2} + 8}}{\ln{\left(12 \right)}}+C (correct)
- \frac{2 \cdot 12^{x^{2} + 8}}{\ln{\left(12 \right)}}+C
- 12^{x^{2} + 8} \ln{\left(12 \right)}+C

Let's introduce the new variable $u={x}^{2}+8.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\text{d}u=2x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 2x{12}^{{x}^{2}+8}\,\text{d}x & =\int {12}^{{x}^{2}+8}\cdot 2x\,\text{d}x \\  & =\int {12}^{u}\cdot \,\text{d}u \\  & =\frac{{12}^{u}}{\operatorname{ln}⁡12}+C \\  & =\frac{{12}^{{x}^{2}+8}}{\operatorname{ln}⁡12}+C.\end{aligned}
$$

## q-73802 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int x{5}^{{x}^{2}-1}\,\text{d}x.$

- \frac{5^{x^{2} - 1}}{2 \ln{\left(5 \right)}}+C (correct)
- \frac{5^{x^{2} - 1}}{\ln{\left(5 \right)}}+C
- \frac{2 \cdot 5^{x^{2} - 1}}{\ln{\left(5 \right)}}+C
- \frac{5^{x^{2} - 1} \ln{\left(5 \right)}}{2}+C
- \frac{5^{x^{2} - 1}}{2}+C

Let's introduce the new variable $u={x}^{2}-1.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{5}^{{x}^{2}-1}\,\text{d}x & =\int {5}^{{x}^{2}-1}\cdot x\,\text{d}x \\  & =\int {5}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {5}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{5}^{u}}{\operatorname{ln}⁡5}+C \\  & =\frac{{5}^{{x}^{2}-1}}{2\operatorname{ln}⁡5}+C.\end{aligned}
$$

## q-73802 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int x{12}^{{x}^{2}-2}\,\text{d}x.$

- \frac{12^{x^{2} - 2}}{2}+C
- \frac{2 \cdot 12^{x^{2} - 2}}{\ln{\left(12 \right)}}+C
- \frac{12^{x^{2} - 2}}{2 \ln{\left(12 \right)}}+C (correct)
- \frac{12^{x^{2} - 2}}{\ln{\left(12 \right)}}+C
- \frac{12^{x^{2} - 2} \ln{\left(12 \right)}}{2}+C

Let's introduce the new variable $u={x}^{2}-2.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x{12}^{{x}^{2}-2}\,\text{d}x & =\int {12}^{{x}^{2}-2}\cdot x\,\text{d}x \\  & =\int {12}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {12}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{12}^{u}}{\operatorname{ln}⁡12}+C \\  & =\frac{{12}^{{x}^{2}-2}}{2\operatorname{ln}⁡12}+C.\end{aligned}
$$

## q-211989 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int {x}^{2}{5}^{{x}^{3}/8}\,\text{d}x.$

- \frac{8 \cdot 5^{\frac{x^{3}}{8}}}{3 \ln{\left(5 \right)}}+C (correct)
- \frac{8 \cdot 5^{\frac{x^{3}}{8}} \ln{\left(5 \right)}}{3}+C
- \frac{3 \cdot 5^{\frac{x^{3}}{8}}}{8 \ln{\left(5 \right)}}+C
- \frac{8 \cdot 5^{\frac{x^{3}}{8}}}{3}+C
- \frac{5^{\frac{x^{3}}{8}}}{\ln{\left(5 \right)}}+C

Let's introduce the new variable $u=\frac{{x}^{3}}{8}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=\frac{3}{8}{x}^{2}\,⟹\,\frac{8}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int {x}^{2}{5}^{{x}^{3}/8}\,\text{d}x & =\int {5}^{{x}^{3}/8}\cdot {x}^{2}\,\text{d}x \\  & =\int {5}^{u}\cdot \frac{8}{3}\,\text{d}u \\  & =\frac{8}{3}\int {5}^{u}\,\text{d}u \\  & =\frac{8\cdot {5}^{u}}{3\operatorname{ln}⁡5}+C \\  & =\frac{8\cdot {5}^{{x}^{3}/8}}{3\operatorname{ln}⁡5}+C.\end{aligned}
$$

## q-211989 — normal authored bank; source-shaped solution

Generated variant:

Calculate the integral $\int {x}^{2}{12}^{{x}^{3}/7}\,\text{d}x.$

- \frac{7 \cdot 12^{\frac{x^{3}}{7}}}{3}+C
- \frac{3 \cdot 12^{\frac{x^{3}}{7}}}{7 \ln{\left(12 \right)}}+C
- \frac{7 \cdot 12^{\frac{x^{3}}{7}}}{3 \ln{\left(12 \right)}}+C (correct)
- \frac{12^{\frac{x^{3}}{7}}}{\ln{\left(12 \right)}}+C
- \frac{7 \cdot 12^{\frac{x^{3}}{7}} \ln{\left(12 \right)}}{3}+C

Let's introduce the new variable $u=\frac{{x}^{3}}{7}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=\frac{3}{7}{x}^{2}\,⟹\,\frac{7}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int {x}^{2}{12}^{{x}^{3}/7}\,\text{d}x & =\int {12}^{{x}^{3}/7}\cdot {x}^{2}\,\text{d}x \\  & =\int {12}^{u}\cdot \frac{7}{3}\,\text{d}u \\  & =\frac{7}{3}\int {12}^{u}\,\text{d}u \\  & =\frac{7\cdot {12}^{u}}{3\operatorname{ln}⁡12}+C \\  & =\frac{7\cdot {12}^{{x}^{3}/7}}{3\operatorname{ln}⁡12}+C.\end{aligned}
$$

## q-73800 — authored normal completion / missing-level extension

Generated variant:

Calculate the integral $\int 3 x^{2}\,{5}^{x^{3} - 1}\,\text{d}x.$

- \frac{5^{x^{3} - 1}}{\ln{\left(5 \right)}}+C (correct)
- \frac{3 \cdot 5^{x^{3} - 1}}{\ln{\left(5 \right)}}+C
- \frac{5^{x^{3} - 1}}{3 \ln{\left(5 \right)}}+C
- 5^{x^{3} - 1} \ln{\left(5 \right)}+C
- 5^{x^{3} - 1}+C

Let's introduce the new variable $u=x^{3} - 1.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=3 x^{2}\,⟹\,1\text{d}u=3 x^{2}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 3 x^{2}\,{5}^{x^{3} - 1}\,\text{d}x & =\int {5}^{x^{3} - 1}\cdot 3 x^{2}\,\text{d}x \\ & =\int {5}^{u}\cdot 1\,\text{d}u \\ & =1\cdot\frac{{5}^{u}}{\ln 5}+C \\ & =\frac{5^{x^{3} - 1}}{\ln{\left(5 \right)}}+C.\end{aligned}
$$

## q-73800 — authored normal completion / missing-level extension

Generated variant:

Calculate the integral $\int 3 x^{2}\,{12}^{x^{3} - 2}\,\text{d}x.$

- 12^{x^{3} - 2}+C
- \frac{12^{x^{3} - 2}}{3 \ln{\left(12 \right)}}+C
- \frac{12^{x^{3} - 2}}{\ln{\left(12 \right)}}+C (correct)
- \frac{3 \cdot 12^{x^{3} - 2}}{\ln{\left(12 \right)}}+C
- 12^{x^{3} - 2} \ln{\left(12 \right)}+C

Let's introduce the new variable $u=x^{3} - 2.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=3 x^{2}\,⟹\,1\text{d}u=3 x^{2}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int 3 x^{2}\,{12}^{x^{3} - 2}\,\text{d}x & =\int {12}^{x^{3} - 2}\cdot 3 x^{2}\,\text{d}x \\ & =\int {12}^{u}\cdot 1\,\text{d}u \\ & =1\cdot\frac{{12}^{u}}{\ln 12}+C \\ & =\frac{12^{x^{3} - 2}}{\ln{\left(12 \right)}}+C.\end{aligned}
$$

## negative-quartic — authored normal completion / missing-level extension

Generated variant:

Calculate the integral $\int x^{3}\,{5}^{4 - 3 x^{4}}\,\text{d}x.$

- - \frac{5^{4 - 3 x^{4}}}{12 \ln{\left(5 \right)}}+C (correct)
- \frac{5^{4 - 3 x^{4}}}{\ln{\left(5 \right)}}+C
- - \frac{12 \cdot 5^{4 - 3 x^{4}}}{\ln{\left(5 \right)}}+C
- - \frac{5^{4 - 3 x^{4}} \ln{\left(5 \right)}}{12}+C
- - \frac{5^{4 - 3 x^{4}}}{12}+C

Let's introduce the new variable $u=4 - 3 x^{4}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=- 12 x^{3}\,⟹\,\left(- \frac{1}{12}\right)\text{d}u=x^{3}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x^{3}\,{5}^{4 - 3 x^{4}}\,\text{d}x & =\int {5}^{4 - 3 x^{4}}\cdot x^{3}\,\text{d}x \\ & =\int {5}^{u}\cdot \left(- \frac{1}{12}\right)\,\text{d}u \\ & =\left(- \frac{1}{12}\right)\int {5}^{u}\,\text{d}u \\ & =\left(- \frac{1}{12}\right)\cdot\frac{{5}^{u}}{\ln 5}+C \\ & =- \frac{5^{4 - 3 x^{4}}}{12 \ln{\left(5 \right)}}+C.\end{aligned}
$$

## negative-quartic — authored normal completion / missing-level extension

Generated variant:

Calculate the integral $\int x^{3}\,{12}^{- 2 x^{4} - 1}\,\text{d}x.$

- - \frac{8 \cdot 12^{- 2 x^{4} - 1}}{\ln{\left(12 \right)}}+C
- \frac{12^{- 2 x^{4} - 1}}{\ln{\left(12 \right)}}+C
- - \frac{12^{- 2 x^{4} - 1}}{8 \ln{\left(12 \right)}}+C (correct)
- - \frac{12^{- 2 x^{4} - 1}}{8}+C
- - \frac{12^{- 2 x^{4} - 1} \ln{\left(12 \right)}}{8}+C

Let's introduce the new variable $u=- 2 x^{4} - 1.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=- 8 x^{3}\,⟹\,\left(- \frac{1}{8}\right)\text{d}u=x^{3}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int x^{3}\,{12}^{- 2 x^{4} - 1}\,\text{d}x & =\int {12}^{- 2 x^{4} - 1}\cdot x^{3}\,\text{d}x \\ & =\int {12}^{u}\cdot \left(- \frac{1}{8}\right)\,\text{d}u \\ & =\left(- \frac{1}{8}\right)\int {12}^{u}\,\text{d}u \\ & =\left(- \frac{1}{8}\right)\cdot\frac{{12}^{u}}{\ln 12}+C \\ & =- \frac{12^{- 2 x^{4} - 1}}{8 \ln{\left(12 \right)}}+C.\end{aligned}
$$
