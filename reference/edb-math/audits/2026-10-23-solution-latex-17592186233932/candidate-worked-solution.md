First, the slope of $y = f(x)$ at $x = \dfrac{1}{2}$ is given by $f'\left( \dfrac{1}{2} \right).$

We will calculate $f'(x)$ using the chain rule. We express $f(x)$ as the composite function
\[
f = \sec{u}, \qquad u = \pi x^{2}.
\]

Differentiating gives
\[
\dfrac{\textrm d f}{\textrm d u} = \sec{u}\tan{u}, \qquad\dfrac{\textrm d u}{\textrm d x} = 2\pi x.
\]

We now apply the chain rule, and get
$$
\begin{aligned}
\dfrac{\textrm d f}{\textrm d x} & = \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&= \sec{u}\tan{u} \cdot 2\pi x \\[5pt]
&= 2\pi x \sec{\left(\pi x^{2}\right)}\tan{\left(\pi x^{2}\right)}.
\end{aligned}
$$

Evaluating at $x=\dfrac{1}{2}$, we find 
$$
\begin{aligned}
f'\left( \dfrac{1}{2} \right) &= 2\pi \cdot \dfrac{1}{2}\cdot \sec{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]}\tan{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]} \\[5pt]
&= \pi \sec{\left(\dfrac{\pi}{4}\right)} \tan{\left(\dfrac{\pi}{4}\right)} \\[5pt]
&= \pi \cdot \sqrt{2}\cdot 1 \\[5pt]
&= \pi\sqrt{2}.
\end{aligned}
$$

Therefore, the slope of $y = f(x)$ at $x=\dfrac{1}{2}$ is $\bbox[4pt, border: 1px solid lightgray]{\pi\sqrt{2}}.$
