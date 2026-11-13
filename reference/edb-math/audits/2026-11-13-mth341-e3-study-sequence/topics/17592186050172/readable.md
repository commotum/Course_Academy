# 17592186050172 Describing Properties of the Sine Function

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186173225 — Introduction

Let's recall the graph of $y=\sin{x}$ once again.

![](images/1d/1dfe4444da1a8f30db08c90de8efecbe1214125b1cfbf49c2ae8681edf3d10db.png)

The graph has infinitely many zeros, and there are an infinite number of points where the function reaches its maximum and minimum values. Let's see how to write down general expressions for these properties. 

We'll assume that $n$ represents any integer throughout this discussion. 

**The Zeros of the Function**

From the graph, we see that the zeros of the function are $x=0,\pm\pi, \pm 2\pi\dots.$ 

We can write down a general expression for the zeros as follows:

$$
x = n\pi.
$$

**The Maxima of the Function**

The function has a maximum when $x=\dfrac\pi 2$ and the function is periodic with period $2\pi.$ Therefore, a general expression for the values of $x$ that maximize sine is

$$
x = \dfrac{\pi}{2} + 2n\pi.
$$

**The Minima of the Function**

The function has a minimum when $x=-\dfrac\pi 2$ and the function is periodic with period $2\pi.$ Therefore, a general expression for the values of $x$ that minimize sine is

$$
x = -\dfrac{\pi}{2} + 2n\pi.
$$



### example 17592186171689 — Describing Properties of the Sine Function

Which of the following statements are true regarding the function $y=\sin{x}$? Assume that $n$ is an integer.

1. The zeros of the function are $x=2n\pi$.
2. The function has minimum values at $x=-\dfrac{\pi}{2}+2n\pi$.
3. The function has maximum values at $x=\dfrac{\pi}{2}+2n\pi$.

Let's plot the graph of $y=\sin{x}$.

![](images/1d/1dfe4444da1a8f30db08c90de8efecbe1214125b1cfbf49c2ae8681edf3d10db.png)

Let's go through each statement.

- Statement I is false. The zeros occur at $x=0, \pm \pi, \pm 2\pi,\ldots$, which can be written as $x=n\pi$.
- Statement II is true. The function has a minimum at $x=-\dfrac{\pi}{2}$, and the period is $2\pi$. Therefore, the minimum values occur at $-\dfrac{\pi}{2}+2n\pi$.
- Statement III is true. The function has a maximum at $x=\dfrac{\pi}{2}$, and the period is $2\pi$. Therefore, the maximum values occur at $\dfrac{\pi}{2}+2n\pi$.

### tutorial 17592186173226 — The Periodicity Property of the Sine Function

Let's recall the graph of the function $y=\sin x.$

![](images/1d/1dfe4444da1a8f30db08c90de8efecbe1214125b1cfbf49c2ae8681edf3d10db.png)

As we've already mentioned, the function $y=\sin x$ is periodic, which means it repeats itself. The period, or horizontal distance needed to complete one of the repeated cycles, is $2\pi.$ 

   

![](images/64/64f1ea47f976cc36869033c1571ef5cd7137a8d2ba822fe31f311021efbdc2a5.png)

   The periodicity of $y=\sin x$ means that $\sin\left( x+2n\pi\right) = \sin\left( x\right)$ for any number $x$ and $n$ is any integer.



### example 17592186171690 — Utilizing the Periodicity Property of the Sine Function

If $\sin x = \dfrac{1}2$, then what is $-2\sin(x+6\pi)-3$?

The period of $y = \sin x$ is $2\pi$. Therefore, for any integer $n$ we have

$$
\sin{x} = \sin{(x+2n\pi)}
$$

Substituting $n=3$ into the above gives

$$
\begin{aligned}
\sin x &= \sin (x + 2 \cdot 3 \cdot π) \\
&= \sin (x + 6π)
\end{aligned}
$$

Therefore, if

$$
\sin{x} = \dfrac{1}{2}
$$

then

$$
\sin{(x+6\pi)} = \dfrac{1}{2}
$$

Finally, then:

$$
\begin{aligned}
-2\sin (x + 6π) - 3 &= -2\left(\frac{1}{2}\right) - 3 \\
&=-1 - 3 \\
&=-4
\end{aligned}
$$

### tutorial 17592186173261 — The Oddness Property of the Sine Function

Recall that a function $f(x)$ is *odd* if it satisfies the property

$$
f(-x) = -f(x).
$$

As it turns out, sine is an odd function! So, for any value of $x,$ we have

$$
\sin(-x) = -\sin(x).
$$

Odd functions always have rotational symmetry of order $2$ about the origin. This is indeed true of the sine function, as we can see from the diagram below. 

![](images/3d/3db401dbceb6b294fb2129e0e9609ac53c97968f62e47eacfc3e78deb8b4777a.png)

We can use the oddness property of sine in conjunction with its periodicity property to simplify trigonometric expressions. Let's see an example.



### example 17592186171691 — Utilizing the Oddness Property of the Sine Function

If $\sin{x} = -\dfrac{4}{7}$, then what is the value of $\sin(-x + 16 \pi)$?

First, let's recall the graph of

$$
y = \sin{x}
$$

![](images/08/08d442eff9febe44bd39e6c15c998d76d56d17bbb7a676d2d511771479bb2f29.png)

From the graph, we note the following:

- The period of $\sin{x}$ is $2\pi$.
- Our graph has rotational symmetry of order $2$ about the origin. This means that $\sin{x}$ is an *odd* function, and we have
$\sin(-x) = -\sin{x}$.

Let's now evaluate our expression:

- Firstly, using the periodicity of $\sin{x}$, we have
$$
\begin{aligned}\operatorname{sin}(-x+16\pi ) & =\operatorname{sin}(-x+2\pi \cdot 8) \\  & =\operatorname{sin}(-x).\end{aligned}
$$
- Secondly, using the oddness of $\sin{x}$, we have
$$
\begin{aligned}\operatorname{sin}(-x) & =-\operatorname{sin}x \\  & =-\left(-\frac{4}{7}\right) \\  & =\frac{4}{7}.\end{aligned}
$$

Therefore,

$$
\sin(-x + 16\pi) = \dfrac{4}{7}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Describing Properties of the Sine Function (4 captured questions)

Question 17592186172547 — None

Which of the following statements are true regarding the function $y = \sin x$? Assume that $n$ is an integer.

1. The function has maximum values at $x = 0, ± π, ± 2π,..$.
2. The function has maximum values at $x = \frac{π}{2} + 2πn$.
3. The range of the function is $y ∈ [- 1, 1]$.

Solution: 

Question 17592186172548 — question.difficulty/moderate

Which of the following statements are true regarding the function $y = \sin x$? Assume that $n$ is an integer.

1. The function intersects the $x$-axis at $x = nπ$.
2. The function has minimum values at $x =-\frac{π}{2} + 2nπ$.
3. The range of the function is $y ∈ [- π, π]$.

Solution: 

Question 17592186580244 — question.difficulty/moderate

Which of the following statements are true regarding the function $y=\operatorname{sin}⁡x?$ Assume that $n$ is an integer. 

I. The function has zeros at $x=\frac{\pi }{2}+n\pi .$

II. The function has minimum values at $$
\displaystyle x=…-\frac{\pi }{2},\frac{3\pi }{2},\frac{7\pi }{2}...
$$

III. The range of the function is $y\in [-1,1].$

Solution: Let's plot the graph of $y=\operatorname{sin}⁡x.$

![](images/77/776d667a77d544cb8fef10ad1c0b3fc625afa75e97f3203d41aefea5ff0c08d0.png)

Let's go through each statement.

- Statement I is false. The zeros occur at $x=0,\pm \pi ,\pm 2\pi ,…,$ which can be written as $x=n\pi .$

- Statement II is true. The minimum values of the function occur at $-\frac{\pi }{2}+2n\pi .$

- Statement III is true. The minimum value is $-1,$ the maximum value is $1,$ and so the range is $y\in [-1,1].$

Answer selection: II and III only

### Utilizing the Periodicity Property of the Sine Function (6 captured questions)

Question 17592186172585 — None

If $\sin x = 1$, then $3\sin (x - 2π) + 1 =$

Solution: 

Question 17592186172586 — None

If $\sin x = \frac{1}{2}$, then $\sin (x + 12π) =$

Solution: 

Question 17592186580238 — question.difficulty/moderate

If $\operatorname{sin}⁡x=-\frac{\sqrt{6}}{3},$ then $6\operatorname{sin}⁡(x-12\pi )=$

Solution: The period of $y=\operatorname{sin}⁡x$ is $2\pi .$ Therefore, for integer $n$ we have

$$
\operatorname{sin}⁡x=\operatorname{sin}⁡(x+2n\pi ).
$$

Substituting $n=-6$ into the left-hand-side gives

$$
\begin{aligned}\operatorname{sin}⁡x &=\operatorname{sin}⁡(x-12\pi ).\end{aligned}
$$

Therefore, if $\operatorname{sin}⁡x=-\frac{\sqrt{6}}{3},$ then $\operatorname{sin}⁡(x-12\pi )=-\frac{\sqrt{6}}{3}.$

Finally, we get

$$
6\operatorname{sin}⁡(x-12\pi )=6\left(-\frac{\sqrt{6}}{3}\right)=-2\sqrt{6}.
$$

Answer selection: -2\sqrt{6}

### Utilizing the Oddness Property of the Sine Function (5 captured questions)

Question 17592186172315 — None

If $\sin x = \frac{1}{2}$, then $\sin (-x + 12π) =$

Solution: 

Question 17592186172316 — None

If $\sin a =-0.23$, then $\sin (-a) =$

Solution: 

Question 17592186580267 — question.difficulty/moderate

If $\operatorname{sin}⁡x=0.44,$ then $\operatorname{sin}⁡(-x-4\pi )=$

Solution: First, let's recall the graph of $y=\operatorname{sin}⁡x.$

![](images/08/08d442eff9febe44bd39e6c15c998d76d56d17bbb7a676d2d511771479bb2f29.png)

From the graph, we note the following:

- The period of $\operatorname{sin}⁡x$ is $2\pi .$

- Our graph has rotational symmetry of order $2$ about the origin. This means that $\operatorname{sin}⁡x$ is an *odd* function, and we have

$$
\operatorname{sin}⁡(-x)=-\operatorname{sin}⁡x.
$$

Let's now evaluate our expression:

- Firstly, using the periodicity of $\operatorname{sin}⁡x,$ we have

$$
\begin{aligned}\operatorname{sin}⁡(-x-4\pi ) & =\operatorname{sin}⁡(-x-2\pi \cdot 2) \\  & =\operatorname{sin}⁡(-x).\end{aligned}
$$

- Secondly, using the oddness of $\operatorname{sin}⁡x,$ we have

$$
\begin{aligned}\operatorname{sin}⁡(-x) & =-\operatorname{sin}⁡x \\  & =-0.44.\end{aligned}
$$

Therefore, $\operatorname{sin}⁡(-x-4\pi )=-0.44.$

Answer selection: -0.44
