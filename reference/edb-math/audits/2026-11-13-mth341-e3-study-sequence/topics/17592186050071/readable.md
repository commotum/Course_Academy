# 17592186050071 Evaluating Expressions Containing Inverse Trigonometric Functions

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186060956 — Introduction

Let's recall the ranges of the inverse trigonometric functions:

- The range of $\theta = \arcsin x$ is given by

$$
-\dfrac{\pi}{2} \leq \theta \leq \dfrac{\pi}{2}.
$$

- The range of $\theta = \arccos x$ is given by

$$
0 \leq \theta \leq \pi.
$$

- The range of $\theta = \arctan x$ is given by

$$
-\dfrac{\pi}{2} \lt \theta \lt \dfrac{\pi}{2}.
$$

When working with inverse trigonometric functions, it's essential to check that any answers we get lie within the permitted range.



### tutorial 17592186060961 — Computing the Value of an Inverse Trigonometric Function

Let's use our knowledge of inverse trigonometric functions to go through the steps of how to compute $\arcsin \left(\dfrac {\sqrt 3} 2\right).$ 

First, note that if $\theta = \arcsin \left(\dfrac{\sqrt3}{2}\right),$ then we must have that $\sin \theta = \dfrac{\sqrt3}{2}.$

Since the range of $\arcsin x$ is $$
\displaystyle \left[-\dfrac{\pi}{2}, \dfrac{\pi}{2}\right],
$$ we need to find an angle $$
\displaystyle \theta \in \left[-\dfrac{\pi}{2}, \dfrac{\pi}{2}\right]
$$ (i.e., in either the first or fourth quadrants) such that $\sin \theta = \dfrac{\sqrt3}{2}.$

Since $\dfrac{\sqrt3}{2}$ is positive, our answer is an angle that lies in the first quadrant, where sine is positive.

Now, let's take a look at the unit circle to find our angle.

![](images/db/dbf36192ac332dc49ed75278838e989a37ac7d888311be1b8b059a7b59667aa6.png)

From the values in the first quadrant, we see that

$$
\sin\left(\dfrac{\pi}{3}\right) = \dfrac{\sqrt3}{2}.
$$

Therefore,

$$
\arcsin\left(\dfrac{\sqrt3}{2}\right) = \dfrac{\pi}{3}.
$$



### example 17592186059609 — Evaluating Arcsine or Arccosine

Find the value of $\arccos\left(-\dfrac{1}{2}\right).$

The range of $\theta = \arccos x$ is given by

$$
0 \le \theta  \le \pi.
$$

Note that the angle $\theta$ spans the first and second quadrants.

Since $-\dfrac{1}{2}$ is negative, our answer is an angle that lies in the second quadrant, where cosine is negative.

![](images/db/dbf36192ac332dc49ed75278838e989a37ac7d888311be1b8b059a7b59667aa6.png)

From the values in the second quadrant, we see that

$$
\cos\left( \dfrac{2\pi}{3}\right) = -\dfrac{1}{2}.
$$

Therefore,

$$
\arccos\left(  -\dfrac{1}{2} \right) =\dfrac{2\pi}{3}.
$$

### example 17592186059620 — Evaluating Arcsine When a Coterminal Angle is Required

Find the value of $\arcsin \left(-\dfrac{\sqrt{3}} 2 \right).$

First, note that the range of $\theta = \arcsin x$ is given by

$$
-\dfrac\pi 2 \le \theta \le \dfrac\pi 2.
$$

Now, let's take a look at the unit circle.

![](images/db/dbf36192ac332dc49ed75278838e989a37ac7d888311be1b8b059a7b59667aa6.png)

From the values in the unit circle, we see that

$$
\sin\left( \dfrac{5\pi}{3}\right) = -\dfrac {\sqrt{3}} 2.
$$

However, $\dfrac{5\pi}{3}$ does not lie within the range of $\theta.$ To get an angle that's coterminal with $\dfrac{5\pi}{3}$ and lies within the range of $\theta,$ we subtract $2\pi{:}$

$$
\dfrac{5\pi}{3} - 2\pi = -\dfrac{\pi}{3}
$$

Therefore,

$$
\arcsin \left(-\dfrac {\sqrt{3}} 2\right) = -\dfrac{\pi}{3}.
$$

### example 17592186059610 — Evaluating Arctangent

Find, in radians, the value of $\arctan(-\sqrt 3).$

First, note that the range of $\theta = \arctan x$ is given by

$$
-\dfrac\pi 2 \lt \theta \lt \dfrac\pi 2.
$$

Note that the angle $\theta$ spans the first and fourth quadrants.

Since $-\sqrt 3$ is negative, our answer is an angle that lies in the fourth quadrant, where the tangent is negative.

From the special values of the trigonometric functions and the oddness of the tangent function, we know that 

$$
\tan \left(-\dfrac{\pi}{3}\right) = -\tan\left(\dfrac{\pi}{3}\right) = -\sqrt 3.
$$

Since $-\dfrac{\pi}{3}$ is an angle in the fourth quadrant that lies within the range of $\arctan,$ we conclude that

$$
\arctan \left(-\sqrt 3\right) = -\dfrac{\pi}{3}.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Evaluating Arcsine or Arccosine (17 captured questions)

Question 17592186060250 — question.difficulty/moderate

$\operatorname{arccos}⁡\left(-\frac{\sqrt{2}}{2}\right)=$

Solution: The range of $\theta =\operatorname{arccos}⁡x$ is given by

$$
0\le \theta \le \pi .
$$

Note that the angle $\theta $ spans the first and second quadrants.

Since $-\frac{\sqrt{2}}{2}$ is negative, our answer is an angle that lies in the second quadrant, where cosine is negative.

![](images/db/dbf36192ac332dc49ed75278838e989a37ac7d888311be1b8b059a7b59667aa6.png)

From the values in the second quadrant, we see that

$$
\operatorname{cos}⁡\left(\frac{3\pi }{4}\right)=-\frac{\sqrt{2}}{2}.
$$

Therefore,

$$
\operatorname{arccos}⁡\left(-\frac{\sqrt{2}}{2}\right)=\frac{3\pi }{4}.
$$

Answer selection: \frac{3\pi }{4}

Question 17592186060435 — None

What is $\arccos \left(\frac{\sqrt{3}}{2}\right)$?

Solution: 

Question 17592186233244 — question.difficulty/easy

$\operatorname{arcsin}\left(\frac{1}{2}\right)=$

Solution: First, note that the range of $\theta =\operatorname{arcsin}x$ is given by

$$
-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}.
$$

Note that the angle $\theta $ spans the first and fourth quadrants.

Since $\frac{1}{2}$ is positive, our answer is an angle that lies in the first quadrant, where sine is positive.

Now, let's take a look at the unit circle.

![](images/a3/a33ea7c6d1aa7cd7e54376aefb2af4347da59a61ecaabdbf4964d41b9661870a.png)

From the values in the first quadrant, we see that

$$
\operatorname{sin}\left(\frac{\pi }{6}\right)=\frac{1}{2}.
$$

Therefore,

$$
\operatorname{arcsin}\left(\frac{1}{2}\right)=\frac{\pi }{6}.
$$

### Evaluating Arcsine When a Coterminal Angle is Required (17 captured questions)

Question 17592186060246 — question.difficulty/moderate

$\operatorname{arcsin}⁡(-1)=$

Solution: First, note that the range of $\theta =\operatorname{arcsin}⁡x$ is given by

$$
-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}.
$$

Now, let's take a look at the unit circle.

![](images/db/dbf36192ac332dc49ed75278838e989a37ac7d888311be1b8b059a7b59667aa6.png)

From the values on the unit circle, we see that

$$
\operatorname{sin}⁡\left(\frac{3\pi }{2}\right)=-1.
$$

However, $\frac{3\pi }{2}$ does not lie within the range of $\theta .$ To get an angle that's coterminal with $\frac{3\pi }{2}$ that lies within the range of $\theta ,$ we subtract $2\pi .$

$$
\frac{3\pi }{2}-2\pi =-\frac{\pi }{2}
$$

Hence,

$$
\operatorname{arcsin}⁡(-1)=-\frac{\pi }{2}.
$$

Answer selection: -\frac{\pi }{2}

Question 17592186060247 — question.difficulty/moderate

$\operatorname{arcsin}⁡\left(-\frac{1}{2}\right)=$

Solution: First, note that the range of $\theta =\operatorname{arcsin}⁡x$ is given by

$$
-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}.
$$

Now, let's take a look at the unit circle.

![](images/db/dbf36192ac332dc49ed75278838e989a37ac7d888311be1b8b059a7b59667aa6.png)

From the values in the unit circle, we see that

$$
\operatorname{sin}⁡\left(\frac{11\pi }{6}\right)=-\frac{1}{2}.
$$

However, $\frac{11\pi }{6}$ does not lie within the range of $\theta .$ To get an angle that's coterminal with $\frac{11\pi }{6}$ that lies within the range of $\theta ,$ we subtract $2\pi .$

$$
\frac{11\pi }{6}-2\pi =-\frac{\pi }{6}
$$

Hence,

$$
\operatorname{arcsin}⁡\left(-\frac{1}{2}\right)=-\frac{\pi }{6}.
$$

Answer selection: -\frac{\pi }{6}

Question 17592186233674 — question.difficulty/moderate

$\operatorname{arcsin}\left(-\frac{\sqrt{2}}{2}\right)=$

Solution: First, note that the range of $\theta =\operatorname{arcsin}x$ is given by

$$
-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}.
$$

Now, let's take a look at the unit circle.

![](images/db/dbf36192ac332dc49ed75278838e989a37ac7d888311be1b8b059a7b59667aa6.png)

From the values in the unit circle, we see that

$$
\operatorname{sin}\left(\frac{7\pi }{4}\right)=-\frac{\sqrt{2}}{2}.
$$

However, $\frac{7\pi }{4}$ does not lie within the range of $\theta .$ To get an angle that's coterminal with $\frac{7\pi }{4}$ that lies within the range of $\theta ,$ we subtract $2\pi .$

$$
\frac{7\pi }{4}-2\pi =-\frac{\pi }{4}.
$$

Hence,

$$
\operatorname{arcsin}\left(-\frac{\sqrt{2}}{2}\right)=-\frac{\pi }{4}.
$$

### Evaluating Arctangent (19 captured questions)

Question 17592186060245 — question.difficulty/easy

$\operatorname{arctan}⁡(\sqrt{3})=$

Solution: The range of $\theta =\operatorname{arctan}⁡x$ is given by:

$$
-{90}^{∘}<\theta <{90}^{∘}
$$

Note that the angle $\theta $ spans the first and fourth quadrants.

Since $\sqrt{3}$ is positive, our answer is an angle that lies in the first quadrant, where the tangent is positive.

From the special values of the trigonometric functions, we know that 

$$
\operatorname{tan}⁡{60}^{∘}=\sqrt{3}.
$$

Since ${60}^{∘}$ is an angle in the first quadrant that lies within the range of $arctan,$ we conclude that

$$
\operatorname{arctan}⁡(\sqrt{3})={60}^{∘}.
$$

Answer selection: {60}^{∘}

Question 17592186060248 — None

What is $\arctan (-1)$?

Solution: 

Question 17592186233822 — question.difficulty/easy

Expressed in radians, $\operatorname{arctan}(\sqrt{3})=${{field-1}}.

Solution: The range of $\theta =\operatorname{arctan}x$ is given by:

$$
-\frac{\pi }{2}<\theta <\frac{\pi }{2}
$$

Note that the angle $\theta $ spans the first and fourth quadrants.

Since $\sqrt{3}$ is positive, our answer is an angle that lies in the first quadrant, where the tangent is positive.

From the special values of the trigonometric functions, we know that 

$$
\operatorname{tan}\left(\frac{\pi }{3}\right)=\sqrt{3}.
$$

Since $\frac{\pi }{3}$ is an angle in the first quadrant that lies within the range of $arctan,$ we conclude that

$$
\operatorname{arctan}(\sqrt{3})=\frac{\pi }{3}.
$$

Answer field-1: \frac{\pi }{3}
