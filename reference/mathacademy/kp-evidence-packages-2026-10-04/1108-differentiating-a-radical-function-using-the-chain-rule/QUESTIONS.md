# Differentiating a Radical Function Using the Chain Rule

Database content, including the canonical example. For blank fields, stored answer values are not displayed multiple-choice options.

## e-182 — canonical worked example

Source: existing database content

Difficulty: easy

### Problem

Given that $y = \sqrt{1-x^2}$, find $\dfrac{\textrm d y}{\textrm d x}$.

### Worked solution

We use the chain rule in the form

$$
\dfrac{\textrm d y}{\textrm d x} = \dfrac{\textrm d y}{\textrm d u}\cdot \dfrac{\textrm d u}{\textrm d x}
$$

Here, we've used $u$ instead of $g$ for the intermediate variable.

Let $u=1-x^2$. Then

$$
y = \sqrt u = u^{1/2}
$$

Differentiating, we have

$$
\dfrac{\textrm d y}{\textrm d u} = \dfrac{1}{2}u^{-1/2} = \dfrac{1}{2\sqrt u}
$$

and

$$
\dfrac{\textrm d u}{\textrm d x} = -2x
$$

Multiplying the two together gives

$$
\begin{aligned}
\frac{dy}{dx} &= \frac{1}{2\sqrt{u}} \cdot (-2x) \\
&=-\frac{2x}{2\sqrt{u}} \\
&=-\frac{x}{\sqrt{1 - x^{2}}}
\end{aligned}
$$


## q-107360

Source: existing database content

Difficulty: easy

### Problem

Find the slope of the tangent to the curve $y=\sqrt{1-4x}$ at the point where $x=-2.$

### Worked solution

To find the slope at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

We use the chain rule in the form

$$
\frac{\text{d}y}{\text{d}x}=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x}.
$$

Let $u=1-4x.$ Then $y=\sqrt{u}.$ Differentiating, we have

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2\sqrt{u}}
$$

and

$$
\frac{\text{d}u}{\text{d}x}=-4.
$$

Multiplying the two together gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{2\sqrt{u}}\cdot (-4) \\  & =-\frac{2}{\sqrt{1-4x}}.\end{aligned}
$$

Finally, substituting $x=-2,$ we get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=-2} & ={(-\frac{2}{\sqrt{1-4x}})|}_{x=-2} \\  & =-\frac{2}{\sqrt{1-4(-2)}} \\  & =-\frac{2}{3}\,.\end{aligned}
$$

### Answer field `selection` (radio)

1. $-\frac{5}{3}$

2. $-\frac{3}{4}$

3. $-\frac{2}{3}$ **[stored correct answer]**

4. $2$

5. $\frac{1}{3}$


## q-342802

Source: existing database content

Difficulty: easy

### Problem

The slope of the tangent to the curve $y=\frac{1}{\sqrt{3{x}^{2}+12x}}$ at the point where $x=2$ is{{field-1}}.

### Worked solution

To find the slope at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

We use the chain rule in the form

$$
\frac{\text{d}y}{\text{d}x}=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x}.
$$

Let $u=3{x}^{2}+12x.$ Then $y=\frac{1}{\sqrt{u}}={u}^{-1/2}.$ Differentiating, we have

$$
\frac{\text{d}y}{\text{d}u}=-\frac{1}{2}{u}^{-3/2}=-\frac{1}{2\sqrt{{u}^{3}}},
$$

and

$$
\frac{\text{d}u}{\text{d}x}=6x+12.
$$

Multiplying the two together gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{1}{2\sqrt{{u}^{3}}}\cdot (6x+12) \\  & =-\frac{6x+12}{2\sqrt{(3{x}^{2}+12x{)}^{3}}}.\end{aligned}
$$

Finally, substituting $x=2,$ we get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(-\frac{6x+12}{2\sqrt{(3{x}^{2}+12x{)}^{3}}})|}_{x=2} \\  & =-\frac{6(2)+12}{2\sqrt{(3(2{)}^{2}+12(2){)}^{3}}} \\  & =-\frac{24}{2\sqrt{{36}^{3}}} \\  & =-\frac{1}{18}.\end{aligned}
$$

### Answer field `field-1` (blank)

1. $\frac{1}{18}$

2. $-\frac{1}{18}$ **[stored correct answer]**


## q-48846

Source: existing database content

Difficulty: easy

### Problem

Given that $y = \sqrt{4x - 3}$, find $\frac{dy}{dx}$.

### Worked solution

Write $y=(4x-3)^{1/2}$. For $x>3/4$,
$$y'=\frac12(4x-3)^{-1/2}\cdot4=\frac2{\sqrt{4x-3}}.$$

### Answer field `selection` (radio)

1. $\frac{4}{\sqrt{4x - 3}}$

2. $\frac{2}{\sqrt{4x - 3}}$ **[stored correct answer]**

3. $\frac{1}{2\sqrt{4x + 3}}$

4. $\frac{2}{\sqrt{4x + 3}}$

5. $\frac{1}{2\sqrt{4x - 3}}$


## q-342680

Source: existing database content

Difficulty: hard

### Problem

Given that $y=\sqrt{{x}^{2}-6x}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

### Worked solution

We use the chain rule in the form

$$
\frac{\text{d}y}{\text{d}x}=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x}.
$$

Let $u={x}^{2}-6x.$ Then $y=\sqrt{u}.$ Differentiating, we have

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2\sqrt{u}},
$$

and

$$
\frac{\text{d}u}{\text{d}x}=2x-6.
$$

Multiplying the two together gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{2\sqrt{u}}\cdot (2x-6) \\  & =\frac{2(x-3)}{2\sqrt{{x}^{2}-6x}} \\  & =\frac{x-3}{\sqrt{{x}^{2}-6x}}.\end{aligned}
$$

### Answer field `field-1` (blank)

1. $\frac{x-3}{\sqrt{x^2-6x}}$ **[stored correct answer]**

2. $2x-6$


## q-342683

Source: existing database content

Difficulty: hard

### Problem

Given that $y=\sqrt{3x+6}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

### Worked solution

We use the chain rule in the form

$$
\frac{\text{d}y}{\text{d}x}=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x}.
$$

Let $u=3x+6.$ Then $y=\sqrt{u}.$ Differentiating, we have

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2\sqrt{u}},
$$

and

$$
\frac{\text{d}u}{\text{d}x}=3.
$$

Multiplying the two together gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{2\sqrt{u}}\cdot 3 \\  & =\frac{3}{2\sqrt{3x+6}}.\end{aligned}
$$

### Answer field `field-1` (blank)

1. $\frac{3}{2\sqrt{3x+6}}$ **[stored correct answer]**


## q-107291

Source: existing database content

Difficulty: moderate

### Problem

Given that $y=\sqrt{3-6x},$ find $\frac{\text{d}y}{\text{d}x}.$

### Worked solution

We use the chain rule in the form

$$
\frac{\text{d}y}{\text{d}x}=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x}.
$$

Let $u=3-6x.$ Then $y=\sqrt{u}={u}^{1/2}.$ Differentiating, we have

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2}{u}^{-1/2}=\frac{1}{2\sqrt{u}}
$$

and

$$
\frac{\text{d}u}{\text{d}x}=-6.
$$

Multiplying the two together gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{2\sqrt{u}}\cdot (-6) \\  & =-\frac{3}{\sqrt{3-6x}}.\end{aligned}
$$

### Answer field `selection` (radio)

1. $-\frac{3}{\sqrt{3-6x}}$ **[stored correct answer]**

2. $\frac{6}{\sqrt{3-6x}}$

3. $\frac{1}{12\sqrt{3-6x}}$

4. $-\frac{1}{2\sqrt{3-6x}}$

5. $-\frac{1}{\sqrt{3-6x}}$


## q-314194

Source: existing database content

Difficulty: moderate

### Problem

Find $\frac{\text{d}y}{\text{d}x}$ for $y=\frac{1}{\sqrt{2x+7}}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

### Worked solution

We use the chain rule in the form

$$
\frac{\text{d}y}{\text{d}x}=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x}.
$$

Let $u=2x+7.$ Then $y=\frac{1}{\sqrt{u}}={u}^{-1/2}.$ Differentiating, we have

$$
\frac{\text{d}y}{\text{d}u}=-\frac{1}{2}{u}^{-3/2}=-\frac{1}{2\sqrt{{u}^{3}}},
$$

and

$$
\frac{\text{d}u}{\text{d}x}=2.
$$

Multiplying the two together gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{1}{2\sqrt{{u}^{3}}}\cdot 2 \\  & =-\frac{1}{\sqrt{{u}^{3}}} \\  & =-\frac{1}{\sqrt{(2x+7{)}^{3}}}.\end{aligned}
$$

### Answer field `field-1` (blank)

1. $\frac{1}{\sqrt{(2x+7)^3}}$

2. $-\frac{1}{\sqrt{(2x+7)^3}}$ **[stored correct answer]**


## q-342764

Source: existing database content

Difficulty: moderate

### Problem

Find $\frac{\text{d}y}{\text{d}x}$ for $y=\frac{1}{\sqrt{5x+1}}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

### Worked solution

We use the chain rule in the form

$$
\frac{\text{d}y}{\text{d}x}=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x}.
$$

Let $u=5x+1.$ Then $y=\frac{1}{\sqrt{u}}={u}^{-1/2}.$ Differentiating, we have

$$
\frac{\text{d}y}{\text{d}u}=-\frac{1}{2}{u}^{-3/2}=-\frac{1}{2\sqrt{{u}^{3}}},
$$

and

$$
\frac{\text{d}u}{\text{d}x}=5.
$$

Multiplying the two together gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{1}{2\sqrt{{u}^{3}}}\cdot 5 \\  & =-\frac{5}{2\sqrt{{u}^{3}}} \\  & =-\frac{5}{2\sqrt{(5x+1)^{3}}}.\end{aligned}
$$

### Answer field `field-1` (blank)

1. $-\frac{5}{2(5x+1)\sqrt{5x+1}}$ **[stored correct answer]**


## q-48730

Source: existing database content

Difficulty: moderate

### Problem

Find $\frac{dy}{dx}$ for $y = \frac{1}{\sqrt{5x - 1}}$.

### Worked solution

Write $y=(5x-1)^{-1/2}$. For $x>1/5$, the chain rule gives
$$y'=-\frac12(5x-1)^{-3/2}\cdot5=-\frac5{2(5x-1)^{3/2}}.$$

### Answer field `selection` (radio)

1. $\frac{1}{2\sqrt{5x - 1}}$

2. $-\frac{5}{2\sqrt{5x - 1}}$

3. $-\frac{3}{5x - 1}$

4. $\frac1{2\sqrt{(5x-1)^3}}$

5. $-\frac5{2\sqrt{(5x-1)^3}}$ **[stored correct answer]**

