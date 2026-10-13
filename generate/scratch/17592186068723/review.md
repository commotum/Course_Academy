# Source, replay and variant review

All complete banks match mathematically. Prompt TeX and final solution layouts are standardized; the substitution sequence and shared instructional prose are preserved. The incomplete unrated source is preserved and repaired only in generated instances.

## q-12494

Source

Calculate $\intx(x^{2} + 5)^{10}dx$.

['\\frac{1}{11}(x^{2} + 5)^{11} + C', '\\frac{1}{10}(x^{2} + 5)^{10} + C', '\\frac{1}{10}(x^{2} + 5)^{11} + C', '\\frac{1}{20}(x^{2} + 5)^{10} + C', '\\frac{1}{22}(x^{2} + 5)^{11} + C']

Missing source solution

Replay

Calculate $\int x\left(x^{2} + 5\right)^{10}\,\text{d}x.$

['\\frac{\\left(x^{2} + 5\\right)^{10}}{10}+C', '\\frac{\\left(x^{2} + 5\\right)^{10}}{20}+C', '\\frac{\\left(x^{2} + 5\\right)^{11}}{10}+C', '\\frac{\\left(x^{2} + 5\\right)^{11}}{22}+C', '\\frac{\\left(x^{2} + 5\\right)^{11}}{11}+C']

In this case, the $x$ outside the parentheses isn't quite the derivative of $(x^{2} + 5).$ But the derivative is $2 x,$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{2} + 5.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=2 x\quad\Longrightarrow\quad \frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x\left(x^{2} + 5\right)^{10}\,\text{d}x=\frac{1}{2}\int u^{10}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{2}\int u^{10}\,\text{d}u &=\frac{1}{2}\frac{u^{11}}{11}+C\\ &=\frac{1}{22}u^{11}+C\\ &=\frac{\left(x^{2} + 5\right)^{11}}{22}+C.\end{aligned}
$$

Variant

Calculate $\int x\left(x^{2} + 3\right)^{5}\,\text{d}x.$

['\\frac{\\left(x^{2} + 3\\right)^{6}}{6}+C', '\\frac{\\left(x^{2} + 3\\right)^{6}}{5}+C', '\\frac{\\left(x^{2} + 3\\right)^{6}}{12}+C', '\\frac{\\left(x^{2} + 3\\right)^{5}}{10}+C', '\\frac{\\left(x^{2} + 3\\right)^{5}}{5}+C']

In this case, the $x$ outside the parentheses isn't quite the derivative of $(x^{2} + 3).$ But the derivative is $2 x,$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{2} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=2 x\quad\Longrightarrow\quad \frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x\left(x^{2} + 3\right)^{5}\,\text{d}x=\frac{1}{2}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{2}\int u^{5}\,\text{d}u &=\frac{1}{2}\frac{u^{6}}{6}+C\\ &=\frac{1}{12}u^{6}+C\\ &=\frac{\left(x^{2} + 3\right)^{6}}{12}+C.\end{aligned}
$$

## q-12496

Source

Calculate $\int {x}^{3}{({x}^{4}+11)}^{9}\,\text{d}x.$

['\\frac{1}{44}{({x}^{4}+11)}^{10}+C', '\\frac{1}{40}{({x}^{4}+11)}^{10}+C', '\\frac{1}{9}{({x}^{4}+11)}^{9}+C', '\\frac{1}{36}{({x}^{4}+11)}^{9}+C', '\\frac{1}{10}{({x}^{4}+11)}^{10}+C']

In this case, the ${x}^{3}$ that's outside the parentheses isn't quite the derivative of $({x}^{4}+11).$ But the derivative is $4{x}^{3},$ so we're only out by a constant factor. 

So we make the substitution

$$
u={x}^{4}+11.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =4{x}^{3}\,⟹\,\frac{1}{4}\text{d}u={x}^{3}\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int {x}^{3}{({x}^{4}+11)}^{9}\,\text{d}x & =\int ({x}^{4}+11)^{9}\cdot {x}^{3}\,\text{d}x \\  & =\int {u}^{9}\cdot \frac{1}{4}\text{d}u \\  & =\frac{1}{4}\int {u}^{9}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{4}\int {u}^{9}\,\text{d}u & =\frac{1}{4}\cdot \frac{{u}^{10}}{10}+C \\  & =\frac{1}{40}{u}^{10}+C \\  & =\frac{1}{40}({x}^{4}+11)^{10}+C.\end{aligned}
$$

Replay

Calculate $\int x^{3}\left(x^{4} + 11\right)^{9}\,\text{d}x.$

['\\frac{\\left(x^{4} + 11\\right)^{10}}{40}+C', '\\frac{\\left(x^{4} + 11\\right)^{9}}{36}+C', '\\frac{\\left(x^{4} + 11\\right)^{9}}{9}+C', '\\frac{\\left(x^{4} + 11\\right)^{10}}{10}+C', '\\frac{\\left(x^{4} + 11\\right)^{10}}{44}+C']

In this case, the $x^{3}$ outside the parentheses isn't quite the derivative of $(x^{4} + 11).$ But the derivative is $4 x^{3},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{4} + 11.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=4 x^{3}\quad\Longrightarrow\quad \frac{1}{4}\,\text{d}u=x^{3}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x^{3}\left(x^{4} + 11\right)^{9}\,\text{d}x=\frac{1}{4}\int u^{9}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{4}\int u^{9}\,\text{d}u &=\frac{1}{4}\frac{u^{10}}{10}+C\\ &=\frac{1}{40}u^{10}+C\\ &=\frac{\left(x^{4} + 11\right)^{10}}{40}+C.\end{aligned}
$$

Variant

Calculate $\int x^{3}\left(x^{4} + 3\right)^{5}\,\text{d}x.$

['\\frac{\\left(x^{4} + 3\\right)^{6}}{12}+C', '\\frac{\\left(x^{4} + 3\\right)^{5}}{5}+C', '\\frac{\\left(x^{4} + 3\\right)^{6}}{6}+C', '\\frac{\\left(x^{4} + 3\\right)^{5}}{20}+C', '\\frac{\\left(x^{4} + 3\\right)^{6}}{24}+C']

In this case, the $x^{3}$ outside the parentheses isn't quite the derivative of $(x^{4} + 3).$ But the derivative is $4 x^{3},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{4} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=4 x^{3}\quad\Longrightarrow\quad \frac{1}{4}\,\text{d}u=x^{3}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x^{3}\left(x^{4} + 3\right)^{5}\,\text{d}x=\frac{1}{4}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{4}\int u^{5}\,\text{d}u &=\frac{1}{4}\frac{u^{6}}{6}+C\\ &=\frac{1}{24}u^{6}+C\\ &=\frac{\left(x^{4} + 3\right)^{6}}{24}+C.\end{aligned}
$$

## q-113710

Source

Calculate $\int 2{x}^{5}(4+{x}^{6})^{5}\,\text{d}x.$

['\\frac{(4+{x}^{6})^{6}}{6}+C', '\\frac{(4+{x}^{6})^{6}}{18}+C', '\\frac{(4+{x}^{6})^{6}}{3}+C', '\\frac{(4+{x}^{6})^{6}}{2}+C', '2(4+{x}^{6})^{6}+C']

In this case, the term $2{x}^{5}$ outside the parentheses isn't quite the derivative of $4+{x}^{6}.$ But the derivative is $6{x}^{5},$ so we're only out by a constant factor.
So we make the substitution

$$
u=4+{x}^{6}.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =6{x}^{5}\,⟹\,\frac{1}{3}\text{d}u=2{x}^{5}\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int 2{x}^{5}(4+{x}^{6})^{5}\,\text{d}x & =\int (4+{x}^{6})^{5}\cdot 2{x}^{5}\,\text{d}x \\  & =\int {u}^{5}\cdot \frac{1}{3}\text{d}u \\  & =\frac{1}{3}\int {u}^{5}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{3}\int {u}^{5}\,\text{d}u & =\frac{1}{3}\cdot \frac{{u}^{6}}{6}+C \\  & =\frac{1}{18}{u}^{6}+C \\  & =\frac{1}{18}(4+{x}^{6})^{6}+C \\  & =\frac{(4+{x}^{6})^{6}}{18}+C.\end{aligned}
$$

Replay

Calculate $\int 2 x^{5}\left(x^{6} + 4\right)^{5}\,\text{d}x.$

['\\frac{\\left(x^{6} + 4\\right)^{6}}{18}+C', '\\frac{\\left(x^{6} + 4\\right)^{6}}{2}+C', '\\frac{\\left(x^{6} + 4\\right)^{6}}{3}+C', '2 \\left(x^{6} + 4\\right)^{6}+C', '\\frac{\\left(x^{6} + 4\\right)^{6}}{6}+C']

In this case, the $2 x^{5}$ outside the parentheses isn't quite the derivative of $(x^{6} + 4).$ But the derivative is $6 x^{5},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{6} + 4.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=6 x^{5}\quad\Longrightarrow\quad \frac{1}{3}\,\text{d}u=2 x^{5}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int 2 x^{5}\left(x^{6} + 4\right)^{5}\,\text{d}x=\frac{1}{3}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{3}\int u^{5}\,\text{d}u &=\frac{1}{3}\frac{u^{6}}{6}+C\\ &=\frac{1}{18}u^{6}+C\\ &=\frac{\left(x^{6} + 4\right)^{6}}{18}+C.\end{aligned}
$$

Variant

Calculate $\int 2 x^{5}\left(x^{6} + 3\right)^{5}\,\text{d}x.$

['\\frac{\\left(x^{6} + 3\\right)^{6}}{6}+C', '\\frac{\\left(x^{6} + 3\\right)^{6}}{3}+C', '2 \\left(x^{6} + 3\\right)^{6}+C', '\\frac{\\left(x^{6} + 3\\right)^{6}}{2}+C', '\\frac{\\left(x^{6} + 3\\right)^{6}}{18}+C']

In this case, the $2 x^{5}$ outside the parentheses isn't quite the derivative of $(x^{6} + 3).$ But the derivative is $6 x^{5},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{6} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=6 x^{5}\quad\Longrightarrow\quad \frac{1}{3}\,\text{d}u=2 x^{5}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int 2 x^{5}\left(x^{6} + 3\right)^{5}\,\text{d}x=\frac{1}{3}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{3}\int u^{5}\,\text{d}u &=\frac{1}{3}\frac{u^{6}}{6}+C\\ &=\frac{1}{18}u^{6}+C\\ &=\frac{\left(x^{6} + 3\right)^{6}}{18}+C.\end{aligned}
$$

## q-113711

Source

Calculate $\int {x}^{6}(2+{x}^{7})^{2}\,\text{d}x.$

['\\frac{(2+{x}^{7})^{3}}{21}+C', '\\frac{7(2+{x}^{7})^{3}}{3}+C', '\\frac{(2+{x}^{7})^{3}}{3}+C', '\\frac{(2+{x}^{7})^{3}}{7}+C', '21(2+{x}^{7})^{3}+C']

In this case, the term ${x}^{6}$ outside the parentheses isn't quite the derivative of $2+{x}^{7}.$ But the derivative is $7{x}^{6},$ so we're only out by a constant factor.
So we make the substitution

$$
u=2+{x}^{7}.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =7{x}^{6}\,⟹\,\frac{1}{7}\text{d}u={x}^{6}\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int {x}^{6}(2+{x}^{7})^{2}\,\text{d}x & =\int (2+{x}^{7})^{2}\cdot {x}^{6}\,\text{d}x \\  & =\int {u}^{2}\cdot \frac{1}{7}\text{d}u \\  & =\frac{1}{7}\int {u}^{2}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{7}\int {u}^{2}\,\text{d}u & =\frac{1}{7}\cdot \frac{{u}^{3}}{3}+C \\  & =\frac{1}{21}{u}^{3}+C \\  & =\frac{1}{21}(2+{x}^{7})^{3}+C \\  & =\frac{(2+{x}^{7})^{3}}{21}+C.\end{aligned}
$$

Replay

Calculate $\int x^{6}\left(x^{7} + 2\right)^{2}\,\text{d}x.$

['\\frac{7 \\left(x^{7} + 2\\right)^{3}}{3}+C', '\\frac{\\left(x^{7} + 2\\right)^{3}}{7}+C', '\\frac{\\left(x^{7} + 2\\right)^{3}}{3}+C', '21 \\left(x^{7} + 2\\right)^{3}+C', '\\frac{\\left(x^{7} + 2\\right)^{3}}{21}+C']

In this case, the $x^{6}$ outside the parentheses isn't quite the derivative of $(x^{7} + 2).$ But the derivative is $7 x^{6},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{7} + 2.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=7 x^{6}\quad\Longrightarrow\quad \frac{1}{7}\,\text{d}u=x^{6}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x^{6}\left(x^{7} + 2\right)^{2}\,\text{d}x=\frac{1}{7}\int u^{2}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{7}\int u^{2}\,\text{d}u &=\frac{1}{7}\frac{u^{3}}{3}+C\\ &=\frac{1}{21}u^{3}+C\\ &=\frac{\left(x^{7} + 2\right)^{3}}{21}+C.\end{aligned}
$$

Variant

Calculate $\int x^{6}\left(x^{7} + 3\right)^{5}\,\text{d}x.$

['\\frac{\\left(x^{7} + 3\\right)^{6}}{42}+C', '\\frac{\\left(x^{7} + 3\\right)^{6}}{6}+C', '42 \\left(x^{7} + 3\\right)^{6}+C', '\\frac{\\left(x^{7} + 3\\right)^{6}}{7}+C', '\\frac{7 \\left(x^{7} + 3\\right)^{6}}{6}+C']

In this case, the $x^{6}$ outside the parentheses isn't quite the derivative of $(x^{7} + 3).$ But the derivative is $7 x^{6},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{7} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=7 x^{6}\quad\Longrightarrow\quad \frac{1}{7}\,\text{d}u=x^{6}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x^{6}\left(x^{7} + 3\right)^{5}\,\text{d}x=\frac{1}{7}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{7}\int u^{5}\,\text{d}u &=\frac{1}{7}\frac{u^{6}}{6}+C\\ &=\frac{1}{42}u^{6}+C\\ &=\frac{\left(x^{7} + 3\right)^{6}}{42}+C.\end{aligned}
$$

## q-113715

Source

Calculate $\int 2{x}^{2}\sqrt{{x}^{3}+10}\,\text{d}x.$

['\\frac{3\\sqrt{({x}^{3}+10)^{3}}}{2}+C', '\\frac{2\\sqrt{({x}^{3}+10)^{3}}}{3}+C', '\\frac{4\\sqrt{({x}^{3}+10)^{3}}}{9}+C', '\\frac{9\\sqrt{({x}^{3}+10)^{3}}}{4}+C', '\\sqrt{({x}^{3}+10)^{3}}+C']

In this case, the $2{x}^{2}$ that's outside the square root isn't quite the derivative of ${x}^{3}+10.$ But the derivative is $3{x}^{2},$ so we're only out by a constant factor.

So we make the substitution

$$
u={x}^{3}+10.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =3{x}^{2}\,⟹\,\frac{2}{3}\text{d}u=2{x}^{2}\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int 2{x}^{2}\sqrt{{x}^{3}+10}\,\text{d}x & =\int \sqrt{{x}^{3}+10}\cdot 2{x}^{2}\,\text{d}x \\  & =\int \sqrt{u}\cdot \frac{2}{3}\text{d}u \\  & =\frac{2}{3}\int {u}^{1/2}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{2}{3}\int {u}^{1/2}\,\text{d}u & =\frac{2}{3}\cdot \frac{{u}^{3/2}}{(\frac{3}{2})}+C \\  & =\frac{2}{3}\cdot \frac{2}{3}\cdot {u}^{3/2} \\  & =\frac{4}{9}{u}^{3/2}+C \\  & =\frac{4}{9}\sqrt{{u}^{3}}+C \\  & =\frac{4\sqrt{({x}^{3}+10)^{3}}}{9}+C.\end{aligned}
$$

Replay

Calculate $\int 2 x^{2}\sqrt{x^{3} + 10}\,\text{d}x.$

Work on an interval where $x^{3} + 10>0$.

['\\frac{2 \\left(x^{3} + 10\\right)^{\\frac{3}{2}}}{3}+C', '\\frac{9 \\left(x^{3} + 10\\right)^{\\frac{3}{2}}}{4}+C', '\\frac{4 \\left(x^{3} + 10\\right)^{\\frac{3}{2}}}{9}+C', '\\left(x^{3} + 10\\right)^{\\frac{3}{2}}+C', '\\frac{3 \\left(x^{3} + 10\\right)^{\\frac{3}{2}}}{2}+C']

In this case, the $2 x^{2}$ outside the parentheses isn't quite the derivative of $(x^{3} + 10).$ But the derivative is $3 x^{2},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{3} + 10.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=3 x^{2}\quad\Longrightarrow\quad \frac{2}{3}\,\text{d}u=2 x^{2}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int 2 x^{2}\sqrt{x^{3} + 10}\,\text{d}x=\frac{2}{3}\int u^{\frac{1}{2}}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{2}{3}\int u^{\frac{1}{2}}\,\text{d}u &=\frac{2}{3}\frac{u^{\frac{3}{2}}}{\frac{3}{2}}+C\\ &=\frac{4}{9}u^{\frac{3}{2}}+C\\ &=\frac{4 \left(x^{3} + 10\right)^{\frac{3}{2}}}{9}+C.\end{aligned}
$$

Variant

Calculate $\int 2 x^{2}\sqrt{x^{3} + 3}\,\text{d}x.$

Work on an interval where $x^{3} + 3>0$.

['\\frac{9 \\left(x^{3} + 3\\right)^{\\frac{3}{2}}}{4}+C', '\\frac{3 \\left(x^{3} + 3\\right)^{\\frac{3}{2}}}{2}+C', '\\frac{4 \\left(x^{3} + 3\\right)^{\\frac{3}{2}}}{9}+C', '\\frac{2 \\left(x^{3} + 3\\right)^{\\frac{3}{2}}}{3}+C', '\\left(x^{3} + 3\\right)^{\\frac{3}{2}}+C']

In this case, the $2 x^{2}$ outside the parentheses isn't quite the derivative of $(x^{3} + 3).$ But the derivative is $3 x^{2},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{3} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=3 x^{2}\quad\Longrightarrow\quad \frac{2}{3}\,\text{d}u=2 x^{2}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int 2 x^{2}\sqrt{x^{3} + 3}\,\text{d}x=\frac{2}{3}\int u^{\frac{1}{2}}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{2}{3}\int u^{\frac{1}{2}}\,\text{d}u &=\frac{2}{3}\frac{u^{\frac{3}{2}}}{\frac{3}{2}}+C\\ &=\frac{4}{9}u^{\frac{3}{2}}+C\\ &=\frac{4 \left(x^{3} + 3\right)^{\frac{3}{2}}}{9}+C.\end{aligned}
$$

## q-2379

Source

$\int x{(3-{x}^{2})}^{5}\,\text{d}x=$

['-\\frac{{(3-{x}^{2})}^{6}}{12}+C', '\\frac{{(3-{x}^{2})}^{6}}{6}+C', '-\\frac{{(3-{x}^{2})}^{5}}{5}+C', '\\frac{{(3-{x}^{2})}^{6}}{4}+C', '-\\frac{{(3-{x}^{2})}^{6}}{6}+C']

In this case, the $x$ that's outside the parentheses isn't quite the derivative of $(3-{x}^{2}).$ But the derivative is $-2x,$ so we're only out by a constant factor. 

So we make the substitution

$$
u=3-{x}^{2}.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =-2x\,⟹\,(-\frac{1}{2})\text{d}u=x\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int x{(3-{x}^{2})}^{5}\,\text{d}x & =\int {(3-{x}^{2})}^{5}\cdot x\,\text{d}x \\  & =\int {u}^{5}\cdot (-\frac{1}{2})\text{d}u \\  & =-\frac{1}{2}\int {u}^{5}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}-\frac{1}{2}\int {u}^{5}\,\text{d}u & =-\frac{1}{2}\cdot \frac{{u}^{6}}{6}+C \\  & =-\frac{1}{12}{u}^{6}+C \\  & =-\frac{1}{12}{(3-{x}^{2})}^{6}+C \\  & =-\frac{{(3-{x}^{2})}^{6}}{12}+C.\end{aligned}
$$

Replay

$\int x\left(- x^{2} + 3\right)^{5}\,\text{d}x=$

['\\frac{\\left(- x^{2} + 3\\right)^{6}}{6}+C', '\\frac{\\left(- x^{2} + 3\\right)^{6}}{4}+C', '- \\frac{\\left(- x^{2} + 3\\right)^{5}}{5}+C', '- \\frac{\\left(- x^{2} + 3\\right)^{6}}{6}+C', '- \\frac{\\left(- x^{2} + 3\\right)^{6}}{12}+C']

In this case, the $x$ outside the parentheses isn't quite the derivative of $(- x^{2} + 3).$ But the derivative is $- 2 x,$ so we're only out by a constant factor.

So we make the substitution

$$
u=- x^{2} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=- 2 x\quad\Longrightarrow\quad - \frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x\left(- x^{2} + 3\right)^{5}\,\text{d}x=- \frac{1}{2}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}- \frac{1}{2}\int u^{5}\,\text{d}u &=- \frac{1}{2}\frac{u^{6}}{6}+C\\ &=- \frac{1}{12}u^{6}+C\\ &=- \frac{\left(- x^{2} + 3\right)^{6}}{12}+C.\end{aligned}
$$

Variant

$\int x\left(- x^{2} + 3\right)^{5}\,\text{d}x=$

['- \\frac{\\left(- x^{2} + 3\\right)^{6}}{12}+C', '- \\frac{\\left(- x^{2} + 3\\right)^{5}}{5}+C', '- \\frac{\\left(- x^{2} + 3\\right)^{6}}{6}+C', '\\frac{\\left(- x^{2} + 3\\right)^{6}}{4}+C', '\\frac{\\left(- x^{2} + 3\\right)^{6}}{6}+C']

In this case, the $x$ outside the parentheses isn't quite the derivative of $(- x^{2} + 3).$ But the derivative is $- 2 x,$ so we're only out by a constant factor.

So we make the substitution

$$
u=- x^{2} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=- 2 x\quad\Longrightarrow\quad - \frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x\left(- x^{2} + 3\right)^{5}\,\text{d}x=- \frac{1}{2}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}- \frac{1}{2}\int u^{5}\,\text{d}u &=- \frac{1}{2}\frac{u^{6}}{6}+C\\ &=- \frac{1}{12}u^{6}+C\\ &=- \frac{\left(- x^{2} + 3\right)^{6}}{12}+C.\end{aligned}
$$

## q-2388

Source

Calculate $\int x({x}^{2}-1)^{3}\,\text{d}x.$

['\\frac{({x}^{2}-1)^{4}}{8}+C', '8({x}^{2}-1)^{4}+C', '\\frac{({x}^{2}-1)^{5}}{10}+C', '\\frac{({x}^{2}-1)^{3}}{6}+C', '3({x}^{2}-1)^{3}+C']

In this case, the $x$ that's outside the parentheses isn't quite the derivative of $({x}^{2}-1).$ But the derivative is $2x,$ so we're only out by a constant factor.
So we make the substitution

$$
u={x}^{2}-1.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int x({x}^{2}-1)^{3}\,\text{d}x & =\int ({x}^{2}-1)^{3}\cdot x\,\text{d}x \\  & =\int {u}^{3}\cdot \frac{1}{2}\text{d}u \\  & =\frac{1}{2}\int {u}^{3}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{2}\int {u}^{3}\,\text{d}u & =\frac{1}{2}\cdot \frac{{u}^{4}}{4}+C \\  & =\frac{1}{8}{u}^{4}+C \\  & =\frac{1}{8}({x}^{2}-1)^{4}+C \\  & =\frac{({x}^{2}-1)^{4}}{8}+C.\end{aligned}
$$

Replay

Calculate $\int x\left(x^{2} - 1\right)^{3}\,\text{d}x.$

['8 \\left(x^{2} - 1\\right)^{4}+C', '\\frac{\\left(x^{2} - 1\\right)^{3}}{6}+C', '\\frac{\\left(x^{2} - 1\\right)^{5}}{10}+C', '3 \\left(x^{2} - 1\\right)^{3}+C', '\\frac{\\left(x^{2} - 1\\right)^{4}}{8}+C']

In this case, the $x$ outside the parentheses isn't quite the derivative of $(x^{2} - 1).$ But the derivative is $2 x,$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{2} - 1.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=2 x\quad\Longrightarrow\quad \frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x\left(x^{2} - 1\right)^{3}\,\text{d}x=\frac{1}{2}\int u^{3}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{2}\int u^{3}\,\text{d}u &=\frac{1}{2}\frac{u^{4}}{4}+C\\ &=\frac{1}{8}u^{4}+C\\ &=\frac{\left(x^{2} - 1\right)^{4}}{8}+C.\end{aligned}
$$

Variant

Calculate $\int x\left(x^{2} - 3\right)^{5}\,\text{d}x.$

['\\frac{\\left(x^{2} - 3\\right)^{6}}{12}+C', '\\frac{\\left(x^{2} - 3\\right)^{7}}{14}+C', '5 \\left(x^{2} - 3\\right)^{5}+C', '\\frac{\\left(x^{2} - 3\\right)^{5}}{10}+C', '12 \\left(x^{2} - 3\\right)^{6}+C']

In this case, the $x$ outside the parentheses isn't quite the derivative of $(x^{2} - 3).$ But the derivative is $2 x,$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{2} - 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=2 x\quad\Longrightarrow\quad \frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x\left(x^{2} - 3\right)^{5}\,\text{d}x=\frac{1}{2}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{2}\int u^{5}\,\text{d}u &=\frac{1}{2}\frac{u^{6}}{6}+C\\ &=\frac{1}{12}u^{6}+C\\ &=\frac{\left(x^{2} - 3\right)^{6}}{12}+C.\end{aligned}
$$

## q-72385

Source

$\int {x}^{2}{(2{x}^{3}+1)}^{5}\,\text{d}x=$

['\\frac{1}{10}(2{x}^{3}+1)^{5}+C', '\\frac{1}{5}(2{x}^{3}+1)^{5}+C', '\\frac{1}{36}(2{x}^{3}+1)^{6}+C', '\\frac{1}{6}(2{x}^{3}+1)^{6}+C', '10(2{x}^{3}+1)^{5}+C']

In this case, the ${x}^{2}$ that's outside the parentheses isn't quite the derivative of $(2{x}^{3}+1).$ But the derivative is $6{x}^{2},$ so we're only out by a constant factor. 

So we make the substitution

$$
u=2{x}^{3}+1.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =6{x}^{2}\,⟹\,\frac{1}{6}\text{d}u={x}^{2}\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int {x}^{2}{(2{x}^{3}+1)}^{5}\,\text{d}x & =\int (2{x}^{3}+1)^{5}\cdot {x}^{2}\,\text{d}x \\  & =\int {u}^{5}\cdot \frac{1}{6}\text{d}u \\  & =\frac{1}{6}\int {u}^{5}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{6}\int {u}^{5}\,\text{d}u & =\frac{1}{6}\cdot \frac{{u}^{6}}{6}+C \\  & =\frac{1}{36}{u}^{6}+C \\  & =\frac{1}{36}(2{x}^{3}+1)^{6}+C.\end{aligned}
$$

Replay

$\int x^{2}\left(2 x^{3} + 1\right)^{5}\,\text{d}x=$

['\\frac{\\left(2 x^{3} + 1\\right)^{5}}{5}+C', '\\frac{\\left(2 x^{3} + 1\\right)^{6}}{6}+C', '\\frac{\\left(2 x^{3} + 1\\right)^{6}}{36}+C', '10 \\left(2 x^{3} + 1\\right)^{5}+C', '\\frac{\\left(2 x^{3} + 1\\right)^{5}}{10}+C']

In this case, the $x^{2}$ outside the parentheses isn't quite the derivative of $(2 x^{3} + 1).$ But the derivative is $6 x^{2},$ so we're only out by a constant factor.

So we make the substitution

$$
u=2 x^{3} + 1.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=6 x^{2}\quad\Longrightarrow\quad \frac{1}{6}\,\text{d}u=x^{2}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x^{2}\left(2 x^{3} + 1\right)^{5}\,\text{d}x=\frac{1}{6}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{6}\int u^{5}\,\text{d}u &=\frac{1}{6}\frac{u^{6}}{6}+C\\ &=\frac{1}{36}u^{6}+C\\ &=\frac{\left(2 x^{3} + 1\right)^{6}}{36}+C.\end{aligned}
$$

Variant

$\int x^{2}\left(2 x^{3} + 3\right)^{5}\,\text{d}x=$

['\\frac{\\left(2 x^{3} + 3\\right)^{5}}{10}+C', '\\frac{\\left(2 x^{3} + 3\\right)^{6}}{36}+C', '10 \\left(2 x^{3} + 3\\right)^{5}+C', '\\frac{\\left(2 x^{3} + 3\\right)^{6}}{6}+C', '\\frac{\\left(2 x^{3} + 3\\right)^{5}}{5}+C']

In this case, the $x^{2}$ outside the parentheses isn't quite the derivative of $(2 x^{3} + 3).$ But the derivative is $6 x^{2},$ so we're only out by a constant factor.

So we make the substitution

$$
u=2 x^{3} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=6 x^{2}\quad\Longrightarrow\quad \frac{1}{6}\,\text{d}u=x^{2}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x^{2}\left(2 x^{3} + 3\right)^{5}\,\text{d}x=\frac{1}{6}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{6}\int u^{5}\,\text{d}u &=\frac{1}{6}\frac{u^{6}}{6}+C\\ &=\frac{1}{36}u^{6}+C\\ &=\frac{\left(2 x^{3} + 3\right)^{6}}{36}+C.\end{aligned}
$$

## q-72386

Source

$\int 2{x}^{7}{(1+{x}^{8})}^{7}\,\text{d}x=$

['\\frac{1}{32}{(1+{x}^{8})}^{8}+C', '8{(1+{x}^{8})}^{8}+C', '7{(1+{x}^{8})}^{7}+C', '\\frac{1}{8}{(1+{x}^{8})}^{8}+C', '\\frac{1}{56}{(1+{x}^{8})}^{7}+C']

In this case, the $2{x}^{7}$ that's outside the parentheses isn't quite the derivative of $(1+{x}^{8}).$ But the derivative is $8{x}^{7},$ so we're only out by a constant factor. 

So we make the substitution

$$
u=1+{x}^{8}.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =8{x}^{7}\,⟹\,\frac{1}{8}\text{d}u={x}^{7}\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int 2{x}^{7}{(1+{x}^{8})}^{7}\,\text{d}x & =\int 2{(1+{x}^{8})}^{7}\cdot {x}^{7}\,\text{d}x \\  & =\int 2{u}^{7}\cdot \frac{1}{8}\text{d}u \\  & =\frac{1}{4}\int {u}^{7}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{4}\int {u}^{7}\,\text{d}u & =\frac{1}{4}\cdot \frac{{u}^{8}}{8}+C \\  & =\frac{1}{32}{u}^{8}+C \\  & =\frac{1}{32}{(1+{x}^{8})}^{8}+C.\end{aligned}
$$

Replay

$\int 2 x^{7}\left(x^{8} + 1\right)^{7}\,\text{d}x=$

['8 \\left(x^{8} + 1\\right)^{8}+C', '\\frac{\\left(x^{8} + 1\\right)^{8}}{8}+C', '7 \\left(x^{8} + 1\\right)^{7}+C', '\\frac{\\left(x^{8} + 1\\right)^{7}}{56}+C', '\\frac{\\left(x^{8} + 1\\right)^{8}}{32}+C']

In this case, the $2 x^{7}$ outside the parentheses isn't quite the derivative of $(x^{8} + 1).$ But the derivative is $8 x^{7},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{8} + 1.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=8 x^{7}\quad\Longrightarrow\quad \frac{1}{4}\,\text{d}u=2 x^{7}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int 2 x^{7}\left(x^{8} + 1\right)^{7}\,\text{d}x=\frac{1}{4}\int u^{7}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{4}\int u^{7}\,\text{d}u &=\frac{1}{4}\frac{u^{8}}{8}+C\\ &=\frac{1}{32}u^{8}+C\\ &=\frac{\left(x^{8} + 1\right)^{8}}{32}+C.\end{aligned}
$$

Variant

$\int 2 x^{7}\left(x^{8} + 3\right)^{5}\,\text{d}x=$

['\\frac{\\left(x^{8} + 3\\right)^{6}}{24}+C', '5 \\left(x^{8} + 3\\right)^{5}+C', '\\frac{\\left(x^{8} + 3\\right)^{5}}{40}+C', '\\frac{\\left(x^{8} + 3\\right)^{6}}{6}+C', '6 \\left(x^{8} + 3\\right)^{6}+C']

In this case, the $2 x^{7}$ outside the parentheses isn't quite the derivative of $(x^{8} + 3).$ But the derivative is $8 x^{7},$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{8} + 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=8 x^{7}\quad\Longrightarrow\quad \frac{1}{4}\,\text{d}u=2 x^{7}\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int 2 x^{7}\left(x^{8} + 3\right)^{5}\,\text{d}x=\frac{1}{4}\int u^{5}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{4}\int u^{5}\,\text{d}u &=\frac{1}{4}\frac{u^{6}}{6}+C\\ &=\frac{1}{24}u^{6}+C\\ &=\frac{\left(x^{8} + 3\right)^{6}}{24}+C.\end{aligned}
$$

## q-72467

Source

Calculate $\int x\sqrt{{x}^{2}-5}\,\text{d}x.$

['2\\sqrt{({x}^{2}-5)^{3}}+C', '3\\sqrt{({x}^{2}-5)^{3}}+C', '\\sqrt{({x}^{2}-5)^{3}}+C', '\\frac{1}{3}\\sqrt{({x}^{2}-5)^{3}}+C', '\\frac{1}{2}\\sqrt{({x}^{2}-5)^{3}}+C']

In this case, the $x$ that's outside the square root isn't quite the derivative of $({x}^{2}-5).$ But the derivative is $2x,$ so we're only out by a constant factor.

So we make the substitution

$$
u={x}^{2}-5.
$$

Its derivative is given by

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x} & =2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x,\end{aligned}
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\begin{aligned}\int x\sqrt{{x}^{2}-5}\,\text{d}x & =\int \sqrt{{x}^{2}-5}\cdot x\,\text{d}x \\  & =\int \sqrt{u}\cdot \frac{1}{2}\text{d}u \\  & =\frac{1}{2}\int {u}^{1/2}\,\text{d}u\end{aligned}
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{2}\int {u}^{1/2}\,\text{d}u & =\frac{1}{2}\cdot \frac{{u}^{3/2}}{(\frac{3}{2})}+C \\  & =\frac{1}{2}\cdot \frac{2}{3}\cdot {u}^{3/2}+C \\  & =\frac{1}{3}{u}^{3/2}+C \\  & =\frac{1}{3}\sqrt{{u}^{3}}+C \\  & =\frac{1}{3}\sqrt{({x}^{2}-5)^{3}}+C.\end{aligned}
$$

Replay

Calculate $\int x\sqrt{x^{2} - 5}\,\text{d}x.$

Work on an interval where $x^{2} - 5>0$.

['3 \\left(x^{2} - 5\\right)^{\\frac{3}{2}}+C', '\\frac{\\left(x^{2} - 5\\right)^{\\frac{3}{2}}}{3}+C', '\\left(x^{2} - 5\\right)^{\\frac{3}{2}}+C', '\\frac{\\left(x^{2} - 5\\right)^{\\frac{3}{2}}}{2}+C', '2 \\left(x^{2} - 5\\right)^{\\frac{3}{2}}+C']

In this case, the $x$ outside the parentheses isn't quite the derivative of $(x^{2} - 5).$ But the derivative is $2 x,$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{2} - 5.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=2 x\quad\Longrightarrow\quad \frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x\sqrt{x^{2} - 5}\,\text{d}x=\frac{1}{2}\int u^{\frac{1}{2}}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{2}\int u^{\frac{1}{2}}\,\text{d}u &=\frac{1}{2}\frac{u^{\frac{3}{2}}}{\frac{3}{2}}+C\\ &=\frac{1}{3}u^{\frac{3}{2}}+C\\ &=\frac{\left(x^{2} - 5\right)^{\frac{3}{2}}}{3}+C.\end{aligned}
$$

Variant

Calculate $\int x\sqrt{x^{2} - 3}\,\text{d}x.$

Work on an interval where $x^{2} - 3>0$.

['\\frac{\\left(x^{2} - 3\\right)^{\\frac{3}{2}}}{3}+C', '2 \\left(x^{2} - 3\\right)^{\\frac{3}{2}}+C', '\\left(x^{2} - 3\\right)^{\\frac{3}{2}}+C', '3 \\left(x^{2} - 3\\right)^{\\frac{3}{2}}+C', '\\frac{\\left(x^{2} - 3\\right)^{\\frac{3}{2}}}{2}+C']

In this case, the $x$ outside the parentheses isn't quite the derivative of $(x^{2} - 3).$ But the derivative is $2 x,$ so we're only out by a constant factor.

So we make the substitution

$$
u=x^{2} - 3.
$$

Its derivative is given by

$$
\frac{\text{d}u}{\text{d}x}=2 x\quad\Longrightarrow\quad \frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

and we can now write our integral in terms of $u,$ as follows:

$$
\int x\sqrt{x^{2} - 3}\,\text{d}x=\frac{1}{2}\int u^{\frac{1}{2}}\,\text{d}u.
$$

Finally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get

$$
\begin{aligned}\frac{1}{2}\int u^{\frac{1}{2}}\,\text{d}u &=\frac{1}{2}\frac{u^{\frac{3}{2}}}{\frac{3}{2}}+C\\ &=\frac{1}{3}u^{\frac{3}{2}}+C\\ &=\frac{\left(x^{2} - 3\right)^{\frac{3}{2}}}{3}+C.\end{aligned}
$$