# Differentiating Trigonometric Functions

## Table of Contents

- [Introduction](#introduction)
- [Finding the Derivative of an Expression With Sine or Cosine Trigonometric Functions](#finding-the-derivative-of-an-expression-with-sine-or-cosine-trigonometric-functions)
- [Finding the Derivative of an Expression With the Tangent Trigonometric Function](#finding-the-derivative-of-an-expression-with-the-tangent-trigonometric-function)
- [Justifying the Formula for the Derivative of Sine](#justifying-the-formula-for-the-derivative-of-sine)
- [Justifying the Formula for the Derivative of Cosine](#justifying-the-formula-for-the-derivative-of-cosine)
- [Justifying the Formula for the Derivative of Tangent](#justifying-the-formula-for-the-derivative-of-tangent)

## Prerequisites

- [Finding Trigonometric Ratios of Special Angles Using the Unit Circle](../268/268.md)
- [Calculating the Equation of a Tangent Line Using Differentiation](../986/986.md)

---

<a id="introduction"></a>
## Introduction

The derivatives of sine, cosine, and tangent are shown in the table below:

| $f(x)$ | $f'(x)$ |
| --- | ---: |
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $\tan x$ | $\sec^2 x$ |

Now that we know the derivatives of the standard trigonometric functions, we can differentiate any combination of them by using the properties of differentiation.

For example, let's find the derivative of

$$
y = \cos x + \sin x
$$

Here, we can use the fact that the derivative of the sum is equal to the sum of the derivatives, and get

$$
\begin{aligned}
\frac{dy}{dx} &= \frac{d}{dx}(\cos x + \sin x) \\
&= \frac{d}{dx}(\cos x) + \frac{d}{dx}(\sin x) \\
&=-\sin x + \cos x
\end{aligned}
$$

**Note:** We'll derive the derivatives shown in the table at the end of this lesson.

---

<a id="finding-the-derivative-of-an-expression-with-sine-or-cosine-trigonometric-functions"></a>
## Finding the Derivative of an Expression With Sine or Cosine Trigonometric Functions

**Example:** Find the derivative of $y = 3\cos x + 4\sin x + 2x^3$.

**Explanation**

We know that

$$
\dfrac{\textrm{d}}{\textrm{d}x} (\sin x) = \cos x
$$

and that

$$
\dfrac{\textrm{d}}{\textrm{d}x} (\cos x) = -\sin x
$$

Applying these formulas, we have

$$
\begin{aligned}
\frac{dy}{dx} &= \frac{d}{dx}(3\cos x + 4\sin x + 2x^{3}) \\
&= 3\frac{d}{dx}(\cos x) + 4\frac{d}{dx}(\sin x) + 2\frac{d}{dx}(x^{3}) \\
&=-3\sin x + 4\cos x + 2(3)x^{2} \\
&=-3\sin x + 4\cos x + 6x^{2}
\end{aligned}
$$

---

**Question 1:**

```quiz
type: radio
id: ma-47908
# MA_ANSWER_MISSING: set exactly one options[].correct=true for radio, or all correct options for checkbox
content: |-
  Find the derivative of $y = \frac{\cos x}{8} - \frac{\sin x}{4}$.
options:
- id: a
  content: |-
    $-\frac{\sin x + 2\cos x}{8}$
- id: b
  content: |-
    $-\frac{2\sin x + \cos x}{8}$
- id: c
  content: |-
    $\frac{\sin x - 2\cos x}{8}$
- id: d
  content: |-
    $\frac{\sin x + 2\cos x}{8}$
- id: e
  content: |-
    $-\frac{\sin x + \cos x}{8}$
```

---

**Question 2:**

```quiz
type: radio
id: ma-47906
# MA_ANSWER_MISSING: set exactly one options[].correct=true for radio, or all correct options for checkbox
content: |-
  Find $\frac{d}{dx}(5\cos x - \sin x)$.
options:
- id: a
  content: |-
    $-\sin x - 5\cos x$
- id: b
  content: |-
    $-5\sin x - \cos x$
- id: c
  content: |-
    $-5\tan x - \cos x$
- id: d
  content: |-
    $-5\cos x - \sin x$
- id: e
  content: |-
    $-5\sin x + \cos x$
```

---

<a id="finding-the-derivative-of-an-expression-with-the-tangent-trigonometric-function"></a>
## Finding the Derivative of an Expression With the Tangent Trigonometric Function

**Example:** Find the slope of $y = 4\tan x + 5x$ at $x = 0$.

**Explanation**

The slope at $x=0$ is given by the value of the derivative $y'$ at $x=0$.

First, we compute the derivative, using the fact that

$$
\dfrac{\textrm{d}}{\textrm{d}x} (\tan x) = \sec^2 x
$$

We get

$$
\begin{aligned}
y^{′}(x) &= \frac{d}{dx}(4\tan x + 5x) \\
&= 4\sec^{2} x + 5
\end{aligned}
$$

Evaluating at $x=0$, we get

$$
\begin{aligned}
y^{′}(0) &= 4\sec^{2} 0 + 5 \\
&= 4 \cdot 1 + 5 \\
&= 9
\end{aligned}
$$

Therefore, the slope is $9$.

---

**Question 3:**

```quiz
type: radio
id: ma-47905
# MA_ANSWER_MISSING: set exactly one options[].correct=true for radio, or all correct options for checkbox
content: |-
  Find $f^{′}(x)$ for $f(x) = \tan x - 2\sin x$.
options:
- id: a
  content: |-
    $\sec x - 2\cos x$
- id: b
  content: |-
    $-\sec^{2} x + 2\cos x$
- id: c
  content: |-
    $\sec^{2} x + 2\cos x$
- id: d
  content: |-
    $\sec x + 2\cos x$
- id: e
  content: |-
    $\sec^{2} x - 2\cos x$
```

---

**Question 4:**

```quiz
type: radio
id: ma-30990
# MA_ANSWER_MISSING: set exactly one options[].correct=true for radio, or all correct options for checkbox
content: |-
  Find $\frac{df}{dx}$ for $f(x) = 8\tan x - 3x$.
options:
- id: a
  content: |-
    $8\sec^{2} x - 3$
- id: b
  content: |-
    $8\csc^{2} x + 3$
- id: c
  content: |-
    $-8\csc^{2} x - 3x$
- id: d
  content: |-
    $-8\sec^{2} x - 3x$
- id: e
  content: |-
    $8\csc x - 3$
```

---

<a id="justifying-the-formula-for-the-derivative-of-sine"></a>
## Justifying the Formula for the Derivative of Sine

To understand why the derivative of sine is cosine, we need to use the definition of the derivative:

$$
\dfrac {\textrm{d}} {\textrm{d}x} (\sin x) = \lim_{h\rightarrow 0}\dfrac{\sin(x+h) - \sin x}{h}
$$

Now, the so-called **addition formula for sine** states that

$$
\sin(x+h) = \sin(x)\cos(h)+\cos (x) \sin(h)
$$

By using the addition formula for sine, we can rewrite our expression for the derivative as follows:

$$
\begin{aligned}
\frac{d}{dx}(\sin x) &= lim_(h → 0)(\sin (x)\cos (h) + \sin (h)\cos (x) - \sin (x))/(h) \\
&= lim_(h → 0)(\sin (x)(\cos (h) - 1) + \cos (x)\sin (h))/(h) \\
&= lim_(h → 0)(\sin (x)((\cos (h) - 1))/(h) + \cos (x)(\sin (h))/(h)) \\
&= \sin (x)lim_(h → 0)((\cos (h) - 1))/(h)_(⏟)_(0) + \cos (x)lim_(h → 0)(\sin (h))/(h)_(⏟)_(1) \\
&= \cos (x)
\end{aligned}
$$

In the last step, we used two important results for trigonometric limits:

$$
\lim_{h\rightarrow 0} \dfrac{1 - \cos(h)}{h}=0 \qquad \text{and} \qquad \lim_{h\rightarrow 0} \dfrac{\sin(h)}{h}=1
$$

Deriving these results requires separate discussions, which we'll leave to future topics.

---

<a id="justifying-the-formula-for-the-derivative-of-cosine"></a>
## Justifying the Formula for the Derivative of Cosine

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

---

<a id="justifying-the-formula-for-the-derivative-of-tangent"></a>
## Justifying the Formula for the Derivative of Tangent

We can also prove that

$$
(\tan x)'= \sec^2 x
$$

using limits, though it's a bit cumbersome.

A faster way is to use a rule of differentiation known as the **quotient rule**.

You'll learn about the quotient rule very soon!
