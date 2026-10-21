We can follow the same method for the cosine and use the definition of the derivative to show that

$$
(\cos x)'=-\sin x
$$

First, we start with the definition of the derivative:

$$
\dfrac {\textrm{d}} {\textrm{d}x} (\cos x) = \lim_{h\rightarrow 0}\dfrac{\cos(x+h) - \cos x}{h}
$$

Now, the so-called **addition formula for cosine** states that

$$
\cos(x+h) = \cos(x)\cos(h)- \sin(x)\sin(h)
$$

Using the addition formula for cosine, we can rewrite our expression for the derivative as follows:

$$
\begin{aligned}
\frac{d}{dx}(\cos x) &= lim_(h → 0)(\cos (x)\cos (h) - \sin (x)\sin (h) - \cos (x))/(h) \\
&= lim_(h → 0)(\cos (x)(\cos (h) - 1) - \sin (x)\sin (h))/(h) \\
&= \cos (x)lim_(h → 0)(\cos (h) - 1)/(h)_(⏟)_(0) - \sin (x)lim_(h → 0)(\sin (h))/(h)_(⏟)_(1) \\
&=-\sin (x)
\end{aligned}
$$

Once again, in the last step, we used the special limits for sine and cosine.
