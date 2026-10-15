# Originals and changed cases

All full banks and concrete observed/shared-prose solutions appear below. The source wrapper remains immutable; repairs and authored completion are recorded separately.



## q-13802 — original

Calculate the integral $\int \frac{2}{x\operatorname{ln}⁡(2x)}\,\text{d}x.$

- $\operatorname{ln}⁡|\operatorname{ln}⁡(2x)|+C$
- $2\operatorname{ln}⁡|\operatorname{ln}⁡x|+C$
- $\operatorname{ln}⁡|\operatorname{ln}⁡x|+C$
- **Correct:** $2\operatorname{ln}⁡|\operatorname{ln}⁡(2x)|+C$
- $2\operatorname{ln}⁡|\operatorname{ln}⁡(2x)|$

Let's set $u=\operatorname{ln}⁡(2x).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{2x}\cdot 2=\frac{1}{x}\,⟹\,\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{2}{x\operatorname{ln}⁡(2x)}\,\text{d}x & =2\int \frac{1}{\operatorname{ln}⁡(2x)}\cdot \frac{\text{d}x}{x} \\  & =2\int \frac{1}{u}\cdot \text{d}u \\  & =2\operatorname{ln}⁡|u|+C \\  & =2\operatorname{ln}⁡|\operatorname{ln}⁡(2x)|+C\end{aligned}
$$


## q-13802 — changed {'k': 7, 'a': 5, 'n': 1, 'p_num': -1, 'p_den': 1}

Calculate the integral $\int \frac{7}{x\log{\left(5 x \right)}}\,\text{d}x.$

- **Correct:** $C + 7 \log{\left(\left|{\log{\left(5 x \right)}}\right| \right)}$
- $C + 7 \log{\left(\left|{\log{\left(x \right)}}\right| \right)}$
- $7 \log{\left(\left|{\log{\left(5 x \right)}}\right| \right)}$
- $C + \log{\left(\left|{\log{\left(5 x \right)}}\right| \right)}$
- $C + \log{\left(\left|{\log{\left(x \right)}}\right| \right)}$

Let's set $u=\log{\left(5 x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{5 x}\cdot 5=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{7}{x\log{\left(5 x \right)}}\,\text{d}x & =7\int \frac{1}{\log{\left(5 x \right)}}\cdot \frac{1}{x}\,\text{d}x \\  & =7\int \frac{1}{u}\,\text{d}u \\  & =7\ln|u|+C \\  & =7\ln|\log{\left(5 x \right)}|+C\end{aligned}
$$


## q-13814 — original

Calculate the integral $\int \frac{5}{x{ln}^{2}⁡(3x)}\,\text{d}x.$

- **Correct:** $-\frac{5}{\operatorname{ln}⁡(3x)}+C$
- $\frac{5}{{ln}^{2}⁡(3x)}+C$
- $-\frac{15}{{ln}^{3}⁡(3x)}$
- $-\frac{1}{\operatorname{ln}⁡(3x)}+C$
- $\frac{15}{\operatorname{ln}⁡(3x)}+C$

Let's set $u=\operatorname{ln}⁡(3x).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3x}\cdot 3=\frac{1}{x}\,⟹\,\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{5}{x{ln}^{2}⁡(3x)}\,\text{d}x & =5\int \frac{1}{(\operatorname{ln}⁡(3x))^{2}}\cdot \frac{\text{d}x}{x} \\  & =5\int \frac{1}{{u}^{2}}\cdot \text{d}u \\  & =-5\cdot {u}^{-1}+C \\  & =-\frac{5}{u}+C \\  & =-\frac{5}{\operatorname{ln}⁡(3x)}+C\end{aligned}
$$


## q-13814 — changed {'k': 7, 'a': 5, 'n': 1, 'p_num': -2, 'p_den': 1}

Calculate the integral $\int \frac{7}{x\log{\left(5 x \right)}^{2}}\,\text{d}x.$

- $C - \frac{1}{\log{\left(5 x \right)}}$
- $C + \frac{7}{\log{\left(5 x \right)}^{2}}$
- $C + \frac{35}{\log{\left(5 x \right)}}$
- **Correct:** $C - \frac{7}{\log{\left(5 x \right)}}$
- $- \frac{35}{\log{\left(5 x \right)}^{3}}$

Let's set $u=\log{\left(5 x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{5 x}\cdot 5=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{7}{x\log{\left(5 x \right)}^{2}}\,\text{d}x & =7\int \frac{1}{\log{\left(5 x \right)}^{2}}\cdot \frac{1}{x}\,\text{d}x \\  & =7\int \frac{1}{u^{2}}\,\text{d}u \\  & =7\cdot \frac{u^{-1}}{-1}+C \\  & =- \frac{7}{u}+C \\  & =- \frac{7}{\log{\left(5 x \right)}}+C\end{aligned}
$$


## q-2202 — original

Calculate the integral $\displaystyle \int\frac{4\ln x}{x}dx$.

- $-\ln^{2} x + C$
- $\ln^{2} x + C$
- **Correct:** $2\ln^{2} x + C$
- $2\ln x + C$
- $\frac{\ln^{2} x}{2} + C$

Let's set $u=\log{\left(x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{4 \log{\left(x \right)}}{x}\,\text{d}x & =4\int \log{\left(x \right)}\cdot \frac{1}{x}\,\text{d}x \\  & =4\int u\,\text{d}u \\  & =4\cdot \frac{u^{2}}{2}+C \\  & =2 u^{2}+C \\  & =2 \log{\left(x \right)}^{2}+C\end{aligned}
$$


## q-2202 — changed {'k': 7, 'a': 1, 'n': 1, 'p_num': 2, 'p_den': 1}

Calculate the integral $\int \frac{7 \log{\left(x \right)}^{2}}{x}\,\text{d}x.$

- $C + \frac{7 \log{\left(x \right)}^{2}}{3}$
- $C + \frac{7 \log{\left(x \right)}^{3}}{6}$
- $C + \frac{7 \log{\left(x \right)}^{3}}{12}$
- $C - \frac{7 \log{\left(x \right)}^{3}}{6}$
- **Correct:** $C + \frac{7 \log{\left(x \right)}^{3}}{3}$

Let's set $u=\log{\left(x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{7 \log{\left(x \right)}^{2}}{x}\,\text{d}x & =7\int \log{\left(x \right)}^{2}\cdot \frac{1}{x}\,\text{d}x \\  & =7\int u^{2}\,\text{d}u \\  & =7\cdot \frac{u^{3}}{3}+C \\  & =\frac{7 u^{3}}{3}+C \\  & =\frac{7 \log{\left(x \right)}^{3}}{3}+C\end{aligned}
$$


## q-13803 — original

Calculate the integral $\int \frac{\operatorname{ln}⁡x}{2x}\,\text{d}x.$

- ${ln}^{2}⁡x+C$
- $\frac{1}{4}\operatorname{ln}⁡x+C$
- $\frac{1}{2}{ln}^{2}⁡x+C$
- **Correct:** $\frac{1}{4}{ln}^{2}⁡x+C$
- $\frac{1}{2}\operatorname{ln}⁡x+C$

Let's set $u=\operatorname{ln}⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\,⟹\,\text{d}u=\frac{1}{x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\operatorname{ln}⁡x}{2x}\,\text{d}x & =\frac{1}{2}\int \operatorname{ln}⁡x\cdot \frac{\text{d}x}{x} \\  & =\frac{1}{2}\int u\,\text{d}u \\  & =\frac{1}{2}\cdot \frac{{u}^{2}}{2}+C \\  & =\frac{1}{4}{u}^{2}+C \\  & =\frac{1}{4}{ln}^{2}⁡x+C\end{aligned}
$$


## q-13803 — changed {'k': 7, 'a': 1, 'n': 1, 'p_num': 2, 'p_den': 1}

Calculate the integral $\int \frac{\log{\left(x \right)}^{2}}{7 x}\,\text{d}x.$

- **Correct:** $C + \frac{\log{\left(x \right)}^{3}}{21}$
- $C + \frac{\log{\left(x \right)}^{2}}{21}$
- $C + \frac{\log{\left(x \right)}^{2}}{7}$
- $C + \log{\left(x \right)}^{3}$
- $C + \frac{\log{\left(x \right)}^{3}}{7}$

Let's set $u=\log{\left(x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\log{\left(x \right)}^{2}}{7 x}\,\text{d}x & =\frac{1}{7}\int \log{\left(x \right)}^{2}\cdot \frac{1}{x}\,\text{d}x \\  & =\frac{1}{7}\int u^{2}\,\text{d}u \\  & =\frac{1}{7}\cdot \frac{u^{3}}{3}+C \\  & =\frac{u^{3}}{21}+C \\  & =\frac{\log{\left(x \right)}^{3}}{21}+C\end{aligned}
$$


## q-13807 — original

Calculate the integral $\int \frac{\operatorname{ln}⁡({x}^{2})}{3x}\,\text{d}x.$

- **Correct:** $\frac{1}{12}{ln}^{2}⁡({x}^{2})+C$
- $\frac{1}{12}{ln}^{2}⁡|x|+C$
- $\frac{1}{6}{ln}^{2}⁡({x}^{2})+C$
- $\frac{1}{12}\operatorname{ln}⁡({x}^{2})+C$
- $\frac{1}{2}{ln}^{2}⁡({x}^{2})+C$

Let's set $u=\operatorname{ln}⁡({x}^{2}).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{{x}^{2}}\cdot 2x=\frac{2}{x}\,⟹\,\frac{1}{2}\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\operatorname{ln}⁡({x}^{2})}{3x}\,\text{d}x & =\frac{1}{3}\int \operatorname{ln}⁡({x}^{2})\cdot \frac{\text{d}x}{x} \\  & =\frac{1}{3}\int u\cdot (\frac{1}{2}\text{d}u) \\  & =\frac{1}{6}\int u\,\text{d}u \\  & =\frac{1}{6}\cdot \frac{{u}^{2}}{2}+C \\  & =\frac{1}{12}{u}^{2}+C \\  & =\frac{1}{12}{ln}^{2}⁡({x}^{2})+C\end{aligned}
$$


## q-13807 — changed {'k': 7, 'a': 1, 'n': 3, 'p_num': 1, 'p_den': 1}

Calculate the integral $\int \frac{\log{\left(x^{3} \right)}}{7 x}\,\text{d}x.$

- $C + \frac{\log{\left(x^{3} \right)}}{42}$
- $C + \frac{\log{\left(\left|{x}\right| \right)}^{2}}{42}$
- $C + \frac{\log{\left(x^{3} \right)}^{2}}{3}$
- **Correct:** $C + \frac{\log{\left(x^{3} \right)}^{2}}{42}$
- $C + \frac{\log{\left(x^{3} \right)}^{2}}{21}$

Let's set $u=\log{\left(x^{3} \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x^{3}}\cdot 3 x^{2}=\frac{3}{x}\quad\Longrightarrow\quad \frac{1}{3}\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\log{\left(x^{3} \right)}}{7 x}\,\text{d}x & =\frac{1}{7}\int \log{\left(x^{3} \right)}\cdot \frac{1}{x}\,\text{d}x \\  & =\frac{1}{7}\int u\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{1}{21}\int u\,\text{d}u \\  & =\frac{1}{21}\cdot \frac{u^{2}}{2}+C \\  & =\frac{u^{2}}{42}+C \\  & =\frac{\log{\left(x^{3} \right)}^{2}}{42}+C\end{aligned}
$$


## q-13808 — original

Calculate the integral $\int \frac{5}{x\operatorname{ln}⁡({x}^{2})}\,\text{d}x.$

- $5\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C$
- $\frac{1}{2}x\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C$
- $\frac{1}{2}\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C$
- $\frac{5}{2}x\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C$
- **Correct:** $\frac{5}{2}\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C$

Let's set $u=\operatorname{ln}⁡({x}^{2}).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{{x}^{2}}\cdot 2x=\frac{2}{x}\,⟹\,\frac{1}{2}\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{5}{x\operatorname{ln}⁡({x}^{2})}\,\text{d}x & =5\int \frac{1}{\operatorname{ln}⁡({x}^{2})}\cdot \frac{\text{d}x}{x} \\  & =5\int \frac{1}{u}\cdot (\frac{1}{2}\text{d}u) \\  & =\frac{5}{2}\int \frac{1}{u}\cdot \text{d}u \\  & =\frac{5}{2}\operatorname{ln}⁡|u|+C \\  & =\frac{5}{2}\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C\end{aligned}
$$


## q-13808 — changed {'k': 7, 'a': 1, 'n': 3, 'p_num': -1, 'p_den': 1}

Calculate the integral $\int \frac{7}{x\log{\left(x^{3} \right)}}\,\text{d}x.$

- $C + \frac{7 x \log{\left(\left|{\log{\left(x^{3} \right)}}\right| \right)}}{3}$
- $C + \frac{x \log{\left(\left|{\log{\left(x^{3} \right)}}\right| \right)}}{3}$
- **Correct:** $C + \frac{7 \log{\left(\left|{\log{\left(x^{3} \right)}}\right| \right)}}{3}$
- $C + 7 \log{\left(\left|{\log{\left(x^{3} \right)}}\right| \right)}$
- $C + \frac{\log{\left(\left|{\log{\left(x^{3} \right)}}\right| \right)}}{3}$

Let's set $u=\log{\left(x^{3} \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x^{3}}\cdot 3 x^{2}=\frac{3}{x}\quad\Longrightarrow\quad \frac{1}{3}\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{7}{x\log{\left(x^{3} \right)}}\,\text{d}x & =7\int \frac{1}{\log{\left(x^{3} \right)}}\cdot \frac{1}{x}\,\text{d}x \\  & =7\int \frac{1}{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{7}{3}\int \frac{1}{u}\,\text{d}u \\  & =\frac{7}{3}\ln|u|+C \\  & =\frac{7}{3}\ln|\log{\left(x^{3} \right)}|+C\end{aligned}
$$


## q-13809 — original

Calculate the integral $\int \frac{{ln}^{2}⁡x}{4x}\,\text{d}x.$

- $\frac{1}{4}{ln}^{2}⁡x+C$
- **Correct:** $\frac{1}{12}{ln}^{3}⁡x+C$
- $\frac{1}{12}{ln}^{2}⁡x+C$
- $\frac{1}{4}{ln}^{3}⁡x+C$
- $\frac{1}{3}{ln}^{3}⁡x+C$

Let's set $u=\operatorname{ln}⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\,⟹\,\text{d}u=\frac{1}{x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{{ln}^{2}⁡x}{4x}\,\text{d}x & =\frac{1}{4}\int (\operatorname{ln}⁡x)^{2}\cdot \frac{\text{d}x}{x} \\  & =\frac{1}{4}\int {u}^{2}\,\text{d}u \\  & =\frac{1}{4}\cdot \frac{{u}^{3}}{3}+C \\  & =\frac{1}{12}{u}^{3}+C \\  & =\frac{1}{12}{ln}^{3}⁡x+C\end{aligned}
$$


## q-13809 — changed {'k': 7, 'a': 1, 'n': 1, 'p_num': 2, 'p_den': 1}

Calculate the integral $\int \frac{\log{\left(x \right)}^{2}}{7 x}\,\text{d}x.$

- $C + \frac{\log{\left(x \right)}^{3}}{7}$
- **Correct:** $C + \frac{\log{\left(x \right)}^{3}}{21}$
- $C + \frac{\log{\left(x \right)}^{3}}{3}$
- $C + \frac{\log{\left(x \right)}^{2}}{7}$
- $C + \frac{\log{\left(x \right)}^{2}}{21}$

Let's set $u=\log{\left(x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\log{\left(x \right)}^{2}}{7 x}\,\text{d}x & =\frac{1}{7}\int \log{\left(x \right)}^{2}\cdot \frac{1}{x}\,\text{d}x \\  & =\frac{1}{7}\int u^{2}\,\text{d}u \\  & =\frac{1}{7}\cdot \frac{u^{3}}{3}+C \\  & =\frac{u^{3}}{21}+C \\  & =\frac{\log{\left(x \right)}^{3}}{21}+C\end{aligned}
$$


## q-210742 — original

Calculate the integral $\int \frac{6\operatorname{ln}⁡({x}^{3})}{x}\,\text{d}x.$

- $2{ln}^{3}⁡({x}^{3})+C$
- $\frac{1}{3}{ln}^{2}⁡({x}^{3})+C$
- $\frac{1}{2}{ln}^{2}⁡({x}^{3})+C$
- $3{ln}^{3}⁡({x}^{2})+C$
- **Correct:** ${ln}^{2}⁡({x}^{3})+C$

Let's set $u=\operatorname{ln}⁡({x}^{3}).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{{x}^{3}}\cdot 3{x}^{2}=\frac{3}{x}\,⟹\,\frac{1}{3}\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{6\operatorname{ln}⁡({x}^{3})}{x}\,\text{d}x & =6\int \operatorname{ln}⁡({x}^{3})\cdot \frac{\text{d}x}{x} \\  & =6\int u\cdot (\frac{1}{3}\text{d}u) \\  & =\frac{6}{3}\int u\,\text{d}u \\  & =2\cdot \frac{{u}^{2}}{2}+C \\  & ={u}^{2}+C \\  & ={ln}^{2}⁡({x}^{3})+C\end{aligned}
$$


## q-210742 — changed {'k': 7, 'a': 1, 'n': 3, 'p_num': 1, 'p_den': 1}

Calculate the integral $\int \frac{7 \log{\left(x^{3} \right)}}{x}\,\text{d}x.$

- $C + \frac{7 \log{\left(x^{2} \right)}^{3}}{2}$
- $C + \frac{\log{\left(x^{3} \right)}^{2}}{3}$
- **Correct:** $C + \frac{7 \log{\left(x^{3} \right)}^{2}}{6}$
- $C + \frac{7 \log{\left(x^{3} \right)}^{3}}{3}$
- $C + \frac{\log{\left(x^{3} \right)}^{2}}{2}$

Let's set $u=\log{\left(x^{3} \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x^{3}}\cdot 3 x^{2}=\frac{3}{x}\quad\Longrightarrow\quad \frac{1}{3}\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{7 \log{\left(x^{3} \right)}}{x}\,\text{d}x & =7\int \log{\left(x^{3} \right)}\cdot \frac{1}{x}\,\text{d}x \\  & =7\int u\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{7}{3}\int u\,\text{d}u \\  & =\frac{7}{3}\cdot \frac{u^{2}}{2}+C \\  & =\frac{7 u^{2}}{6}+C \\  & =\frac{7 \log{\left(x^{3} \right)}^{2}}{6}+C\end{aligned}
$$


## q-210746 — original

Calculate the integral $\int \frac{2}{x\operatorname{ln}⁡(4x)}\,\text{d}x.$

- $\operatorname{ln}⁡|\operatorname{ln}⁡(2x)|+C$
- **Correct:** $2\operatorname{ln}⁡|\operatorname{ln}⁡(4x)|+C$
- $\frac{1}{4}\operatorname{ln}⁡|\operatorname{ln}⁡(2x)|+C$
- $\frac{1}{2}\operatorname{ln}⁡|\operatorname{ln}⁡(4x)|+C$
- $4\operatorname{ln}⁡|\operatorname{ln}⁡x|+C$

Let's set $u=\operatorname{ln}⁡(4x).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{4x}\cdot 4\,⟹\,\text{d}u=\frac{1}{x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{2}{x\operatorname{ln}⁡(4x)}\,\text{d}x & =2\int \frac{1}{\operatorname{ln}⁡(4x)}\cdot \frac{\text{d}x}{x} \\  & =2\int \frac{1}{u}\cdot \text{d}u \\  & =2\operatorname{ln}⁡|u|+C \\  & =2\operatorname{ln}⁡|\operatorname{ln}⁡(4x)|+C\end{aligned}
$$


## q-210746 — changed {'k': 7, 'a': 5, 'n': 1, 'p_num': -1, 'p_den': 1}

Calculate the integral $\int \frac{7}{x\log{\left(5 x \right)}}\,\text{d}x.$

- $C + \frac{\log{\left(\left|{\log{\left(5 x \right)}}\right| \right)}}{7}$
- **Correct:** $C + 7 \log{\left(\left|{\log{\left(5 x \right)}}\right| \right)}$
- $C + 5 \log{\left(\left|{\log{\left(x \right)}}\right| \right)}$
- $C + \log{\left(\left|{\log{\left(\frac{5 x}{2} \right)}}\right| \right)}$
- $C + \frac{\log{\left(\left|{\log{\left(\frac{5 x}{2} \right)}}\right| \right)}}{5}$

Let's set $u=\log{\left(5 x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{5 x}\cdot 5\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{7}{x\log{\left(5 x \right)}}\,\text{d}x & =7\int \frac{1}{\log{\left(5 x \right)}}\cdot \frac{1}{x}\,\text{d}x \\  & =7\int \frac{1}{u}\,\text{d}u \\  & =7\ln|u|+C \\  & =7\ln|\log{\left(5 x \right)}|+C\end{aligned}
$$


## q-2380 — original

Calculate the integral $\int \frac{1}{x\sqrt{\operatorname{ln}⁡x}}\,\text{d}x.$

- $\frac{1}{\operatorname{ln}⁡(\operatorname{ln}⁡x)}+C$
- $\frac{\operatorname{ln}⁡x}{x}+C$
- **Correct:** $2\sqrt{\operatorname{ln}⁡x}+C$
- $\frac{\sqrt{\operatorname{ln}⁡(\operatorname{ln}⁡x)}}{x}+C$
- $\operatorname{ln}⁡x+C$

Let's set $u=\operatorname{ln}⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\,⟹\,\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{1}{x\sqrt{\operatorname{ln}⁡x}}\,\text{d}x & =\int \frac{1}{\sqrt{\operatorname{ln}⁡x}}\cdot \frac{\text{d}x}{x} \\  & =\int \frac{1}{\sqrt{u}}\cdot \text{d}u \\  & =\int {u}^{-1/2}\,\text{d}u \\  & =2{u}^{1/2}+C \\  & =2\sqrt{\operatorname{ln}⁡x}+C\end{aligned}
$$


## q-2380 — changed {'k': 7, 'a': 1, 'n': 1, 'p_num': -1, 'p_den': 2}

Calculate the integral $\int \frac{7}{x\sqrt{\log{\left(x \right)}}}\,\text{d}x.$

- $C + \frac{7 \sqrt{\log{\left(\log{\left(x \right)} \right)}}}{x}$
- $C + \frac{7}{\log{\left(\log{\left(x \right)} \right)}}$
- $C + \frac{7 \log{\left(x \right)}}{x}$
- **Correct:** $C + 14 \sqrt{\log{\left(x \right)}}$
- $C + 7 \log{\left(x \right)}$

Let's set $u=\log{\left(x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{7}{x\sqrt{\log{\left(x \right)}}}\,\text{d}x & =7\int \frac{1}{\sqrt{\log{\left(x \right)}}}\cdot \frac{1}{x}\,\text{d}x \\  & =7\int \frac{1}{\sqrt{u}}\,\text{d}u \\  & =7\int u^{- \frac{1}{2}}\,\text{d}u \\  & =7\cdot \frac{u^{\frac{1}{2}}}{\frac{1}{2}}+C \\  & =14 \sqrt{\log{\left(x \right)}}+C\end{aligned}
$$


## q-31398 — original

Calculate the integral $\int \frac{\sqrt{\operatorname{ln}⁡x}}{3x}\,\text{d}x.$

- $\frac{2}{9}\sqrt{\operatorname{ln}⁡x}+C$
- **Correct:** $\frac{2}{9}\sqrt{{ln}^{3}⁡x}+C$
- $\frac{1}{9}{ln}^{2}⁡x+C$
- $\frac{9}{2}\sqrt{{ln}^{3}⁡x}+C$
- $\frac{2}{9}{ln}^{3}⁡x+C$

Let's set $u=\operatorname{ln}⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\,⟹\,\text{d}u=\frac{1}{x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\sqrt{\operatorname{ln}⁡x}}{3x}\,\text{d}x & =\frac{1}{3}\int \sqrt{\operatorname{ln}⁡x}\cdot \frac{\text{d}x}{x} \\  & =\frac{1}{3}\int \sqrt{u}\,\text{d}u \\  & =\frac{1}{3}\int {u}^{1/2}\,\text{d}u \\  & =\frac{1}{3}\cdot \frac{2{u}^{3/2}}{3}+C \\  & =\frac{2}{9}{u}^{3/2}+C \\  & =\frac{2}{9}\sqrt{{ln}^{3}⁡x}+C\end{aligned}
$$


## q-31398 — changed {'k': 7, 'a': 1, 'n': 1, 'p_num': 1, 'p_den': 2}

Calculate the integral $\int \frac{\sqrt{\log{\left(x \right)}}}{7 x}\,\text{d}x.$

- $C + \frac{21 \sqrt{\log{\left(x \right)}^{3}}}{2}$
- $C + \frac{2 \sqrt{\log{\left(x \right)}}}{21}$
- **Correct:** $C + \frac{2 \sqrt{\log{\left(x \right)}^{3}}}{21}$
- $C + \frac{\log{\left(x \right)}^{2}}{21}$
- $C + \frac{2 \log{\left(x \right)}^{3}}{21}$

Let's set $u=\log{\left(x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\sqrt{\log{\left(x \right)}}}{7 x}\,\text{d}x & =\frac{1}{7}\int \sqrt{\log{\left(x \right)}}\cdot \frac{1}{x}\,\text{d}x \\  & =\frac{1}{7}\int \sqrt{u}\,\text{d}u \\  & =\frac{1}{7}\int u^{\frac{1}{2}}\,\text{d}u \\  & =\frac{1}{7}\cdot \frac{u^{\frac{3}{2}}}{\frac{3}{2}}+C \\  & =\frac{2 u^{\frac{3}{2}}}{21}+C \\  & =\frac{2 \sqrt{\log{\left(x \right)}^{3}}}{21}+C\end{aligned}
$$


## q-210743 — original

Calculate the integral $\int \frac{9\sqrt{\operatorname{ln}⁡(3x)}}{x}\,\text{d}x.$

- $\sqrt{{ln}^{3}⁡(9x)}+C$
- $6\sqrt{{ln}^{2}⁡(3{x}^{2})}+C$
- $6\sqrt{\operatorname{ln}⁡(9x)}+C$
- $\frac{1}{6}\sqrt{\operatorname{ln}⁡(3x)}+C$
- **Correct:** $6\sqrt{{ln}^{3}⁡(3x)}+C$

Let's set $u=\operatorname{ln}⁡(3x).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3x}\cdot 3\,⟹\,\text{d}u=\frac{1}{x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{9\sqrt{\operatorname{ln}⁡(3x)}}{x}\,\text{d}x & =9\int \sqrt{\operatorname{ln}⁡(3x)}\cdot \frac{\text{d}x}{x} \\  & =9\int \sqrt{u}\,\text{d}u \\  & =9\int {u}^{1/2}\,\text{d}u \\  & =9\cdot \frac{2{u}^{3/2}}{3}+C \\  & =6{u}^{3/2}+C \\  & =6\sqrt{{ln}^{3}⁡(3x)}+C\end{aligned}
$$


## q-210743 — changed {'k': 7, 'a': 5, 'n': 1, 'p_num': 1, 'p_den': 2}

Calculate the integral $\int \frac{7 \sqrt{\log{\left(5 x \right)}}}{x}\,\text{d}x.$

- $C + \frac{3 \sqrt{\log{\left(5 x \right)}}}{14}$
- $C + \frac{14 \sqrt{\log{\left(5 x^{2} \right)}^{2}}}{3}$
- **Correct:** $C + \frac{14 \sqrt{\log{\left(5 x \right)}^{3}}}{3}$
- $C + \sqrt{\log{\left(25 x \right)}^{3}}$
- $C + \frac{14 \sqrt{\log{\left(25 x \right)}}}{3}$

Let's set $u=\log{\left(5 x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{5 x}\cdot 5\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{7 \sqrt{\log{\left(5 x \right)}}}{x}\,\text{d}x & =7\int \sqrt{\log{\left(5 x \right)}}\cdot \frac{1}{x}\,\text{d}x \\  & =7\int \sqrt{u}\,\text{d}u \\  & =7\int u^{\frac{1}{2}}\,\text{d}u \\  & =7\cdot \frac{u^{\frac{3}{2}}}{\frac{3}{2}}+C \\  & =\frac{14 u^{\frac{3}{2}}}{3}+C \\  & =\frac{14 \sqrt{\log{\left(5 x \right)}^{3}}}{3}+C\end{aligned}
$$


## q-2194 — original

Calculate the integral $\int \frac{\sqrt{2}}{x\operatorname{ln}⁡x}\,\text{d}x.$

- $x\operatorname{ln}⁡(\operatorname{ln}⁡\sqrt{2})+C$
- $\operatorname{ln}⁡|\operatorname{ln}⁡x|+C$
- $\frac{1}{\operatorname{ln}⁡|\operatorname{ln}⁡x|}+C$
- $\frac{\sqrt{2}}{\operatorname{ln}⁡|\operatorname{ln}⁡x|}+C$
- **Correct:** $\sqrt{2}\operatorname{ln}⁡|\operatorname{ln}⁡x|+C$

Let's set $u=\operatorname{ln}⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\,⟹\,\text{d}u=\frac{1}{x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{\sqrt{2}}{x\operatorname{ln}⁡x}\,\text{d}x & =\sqrt{2}\int \frac{1}{\operatorname{ln}⁡x}\cdot \frac{\text{d}x}{x} \\  & =\sqrt{2}\int \frac{1}{u}\cdot \text{d}u \\  & =\sqrt{2}\operatorname{ln}⁡|u|+C \\  & =\sqrt{2}\operatorname{ln}⁡|\operatorname{ln}⁡x|+C\end{aligned}\end{aligned}
$$


## q-2194 — changed {'k': 11, 'a': 1, 'n': 1, 'p_num': -1, 'p_den': 1}

Calculate the integral $\int \frac{\sqrt{11}}{x\log{\left(x \right)}}\,\text{d}x.$

- $C + x \log{\left(\log{\left(\sqrt{11} \right)} \right)}$
- $C + \log{\left(\left|{\log{\left(x \right)}}\right| \right)}$
- $C + \frac{1}{\log{\left(\left|{\log{\left(x \right)}}\right| \right)}}$
- $C + \frac{\sqrt{11}}{\log{\left(\left|{\log{\left(x \right)}}\right| \right)}}$
- **Correct:** $C + \sqrt{11} \log{\left(\left|{\log{\left(x \right)}}\right| \right)}$

Let's set $u=\log{\left(x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\sqrt{11}}{x\log{\left(x \right)}}\,\text{d}x & =\sqrt{11}\int \frac{1}{\log{\left(x \right)}}\cdot \frac{1}{x}\,\text{d}x \\  & =\sqrt{11}\int \frac{1}{u}\,\text{d}u \\  & =\sqrt{11}\ln|u|+C \\  & =\sqrt{11}\ln|\log{\left(x \right)}|+C\end{aligned}
$$


## q-210748 — original

Calculate the integral $\int \frac{\sqrt{3}}{x\operatorname{ln}⁡({x}^{2})}\,\text{d}x.$

- $\frac{1}{2}\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C$
- $2\operatorname{ln}⁡|\sqrt{3}\operatorname{ln}⁡x|+C$
- $\frac{3}{2}\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C$
- $\sqrt{3}\operatorname{ln}⁡|\operatorname{ln}⁡x|+C$
- **Correct:** $\frac{\sqrt{3}}{2}\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C$

Let's set $u=\operatorname{ln}⁡({x}^{2}).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{{x}^{2}}\cdot 2x=\frac{2}{x}\,⟹\,\frac{1}{2}\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\sqrt{3}}{x\operatorname{ln}⁡({x}^{2})}\,\text{d}x & =\sqrt{3}\int \frac{1}{\operatorname{ln}⁡({x}^{2})}\cdot \frac{\text{d}x}{x} \\  & =\sqrt{3}\int \frac{1}{u}\cdot (\frac{1}{2}\text{d}u) \\  & =\frac{\sqrt{3}}{2}\int \frac{\text{d}u}{u} \\  & =\frac{\sqrt{3}}{2}\operatorname{ln}⁡|u|+C \\  & =\frac{\sqrt{3}}{2}\operatorname{ln}⁡|\operatorname{ln}⁡({x}^{2})|+C\end{aligned}
$$


## q-210748 — changed {'k': 11, 'a': 1, 'n': 3, 'p_num': -1, 'p_den': 1}

Calculate the integral $\int \frac{\sqrt{11}}{x\log{\left(x^{3} \right)}}\,\text{d}x.$

- $C + \sqrt{11} \log{\left(\left|{\log{\left(x \right)}}\right| \right)}$
- $C + \frac{\log{\left(\left|{\log{\left(x^{3} \right)}}\right| \right)}}{3}$
- $C + 3 \log{\left(\sqrt{11} \left|{\log{\left(x \right)}}\right| \right)}$
- $C + \frac{11 \log{\left(\left|{\log{\left(x^{3} \right)}}\right| \right)}}{3}$
- **Correct:** $C + \frac{\sqrt{11} \log{\left(\left|{\log{\left(x^{3} \right)}}\right| \right)}}{3}$

Let's set $u=\log{\left(x^{3} \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x^{3}}\cdot 3 x^{2}=\frac{3}{x}\quad\Longrightarrow\quad \frac{1}{3}\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\sqrt{11}}{x\log{\left(x^{3} \right)}}\,\text{d}x & =\sqrt{11}\int \frac{1}{\log{\left(x^{3} \right)}}\cdot \frac{1}{x}\,\text{d}x \\  & =\sqrt{11}\int \frac{1}{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{\sqrt{11}}{3}\int \frac{1}{u}\,\text{d}u \\  & =\frac{\sqrt{11}}{3}\ln|u|+C \\  & =\frac{\sqrt{11}}{3}\ln|\log{\left(x^{3} \right)}|+C\end{aligned}
$$


## q-13822 — original

Calculate the integral $\int \frac{1}{3x\operatorname{ln}⁡(3x)}\,\text{d}x.$

- $\operatorname{ln}⁡(3x)+C$
- $\frac{3}{2}\operatorname{ln}⁡|\operatorname{ln}⁡(3x)|+C$
- $\frac{1}{3}\operatorname{ln}⁡|\operatorname{ln}⁡(x)|+C$
- $\operatorname{ln}⁡|\operatorname{ln}⁡(3x)|+C$
- **Correct:** $\frac{1}{3}\operatorname{ln}⁡|\operatorname{ln}⁡(3x)|+C$

Let's set $u=\operatorname{ln}⁡(3x).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3x}\cdot 3=\frac{1}{x}\,⟹\,\text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{1}{3x\operatorname{ln}⁡(3x)}\,\text{d}x & =\frac{1}{3}\int \frac{1}{\operatorname{ln}⁡(3x)}\cdot \frac{\text{d}x}{x} \\  & =\frac{1}{3}\int \frac{1}{u}\cdot \text{d}u \\  & =\frac{1}{3}\int \frac{1}{u}\cdot \text{d}u \\  & =\frac{1}{3}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{3}\operatorname{ln}⁡|\operatorname{ln}⁡(3x)|+C\end{aligned}
$$


## q-13822 — changed {'k': 7, 'a': 5, 'n': 1, 'p_num': -1, 'p_den': 1}

Calculate the integral $\int \frac{1}{7 x\log{\left(5 x \right)}}\,\text{d}x.$

- $C + \log{\left(\left|{\log{\left(5 x \right)}}\right| \right)}$
- $C + \frac{5 \log{\left(\left|{\log{\left(5 x \right)}}\right| \right)}}{2}$
- **Correct:** $C + \frac{\log{\left(\left|{\log{\left(5 x \right)}}\right| \right)}}{7}$
- $C + \log{\left(5 x \right)}$
- $C + \frac{\log{\left(\left|{\log{\left(x \right)}}\right| \right)}}{7}$

Let's set $u=\log{\left(5 x \right)}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{5 x}\cdot 5=\frac{1}{x}\quad\Longrightarrow\quad \text{d}u=\frac{\text{d}x}{x}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{1}{7 x\log{\left(5 x \right)}}\,\text{d}x & =\frac{1}{7}\int \frac{1}{\log{\left(5 x \right)}}\cdot \frac{1}{x}\,\text{d}x \\  & =\frac{1}{7}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{7}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{7}\ln|u|+C \\  & =\frac{1}{7}\ln|\log{\left(5 x \right)}|+C\end{aligned}
$$
