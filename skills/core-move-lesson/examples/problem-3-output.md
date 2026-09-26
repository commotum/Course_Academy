# Finding the Units of a Coefficient in Angular Acceleration

## Table of Contents

- [Introduction](#introduction)
- [Matching Units in a Sum](#matching-units-in-a-sum)
- [Dividing Out a Time Power](#dividing-out-a-time-power)
- [Distinguishing the Coefficient From the Constant Term](#distinguishing-the-coefficient-from-the-constant-term)

## Prerequisites

- SI units for angular acceleration
- Powers of time units, such as $[t^2]=\mathrm{s}^2$
- Matching units across terms that are added

---

<a id="introduction"></a>
## Introduction

Suppose the $z$-component of angular acceleration is

$$
\alpha_z(t)=Bt^2+C.
$$

The core move is to match the units of each term on the right to the units of $\alpha_z(t)$, then divide out the units contributed by $t^2$.

---

<a id="matching-units-in-a-sum"></a>
## Matching Units in a Sum

**Example:** Suppose $a(t)=Kt+a_0$, where $a(t)$ has units $\mathrm{m}/\mathrm{s}^2$. What are the units of $K$?

**Explanation**

Since $Kt$ is added to make $a(t)$, it must have units $\mathrm{m}/\mathrm{s}^2$. Because $[t]=\mathrm{s}$,

$$
[K]\mathrm{s}=\frac{\mathrm{m}}{\mathrm{s}^2},
$$

so

$$
[K]=\frac{\mathrm{m}}{\mathrm{s}^3}.
$$

```quiz
type: radio
id: q-1
content: |-
  If $v(t)=At+v_0$ and $v(t)$ has units $\mathrm{m}/\mathrm{s}$, what are the units of $A$?
options:
- id: a
  content: |-
    $\mathrm{m}$
  feedback: |-
    Choosing $\mathrm{m}$ ignores the time multiplying $A$: it would give $[At]=\mathrm{m}\cdot\mathrm{s}$, not velocity. Because $At$ must have units $\mathrm{m}/\mathrm{s}$, divide by $[t]=\mathrm{s}$ to get $[A]=\mathrm{m}/\mathrm{s}^2$.
- id: b
  content: |-
    $\mathrm{m}/\mathrm{s}$
  feedback: |-
    This assigns $A$ the units of $v$ even though $At$, not $A$, is the term added to $v_0$. It would give $[At]=\mathrm{m}$; dividing the required velocity units by $\mathrm{s}$ gives $[A]=\mathrm{m}/\mathrm{s}^2$.
- id: c
  content: |-
    $\mathrm{m}/\mathrm{s}^2$
  correct: true
  feedback: |-
    Added terms must share units, so $At$ must have the velocity units $\mathrm{m}/\mathrm{s}$. With $[t]=\mathrm{s}$, $[A]=(\mathrm{m}/\mathrm{s})/\mathrm{s}=\mathrm{m}/\mathrm{s}^2$.
- id: d
  content: |-
    $\mathrm{m}/\mathrm{s}^3$
  feedback: |-
    This divides by one extra second. It makes $At$ have units $\mathrm{m}/\mathrm{s}^2$ (acceleration) instead of $\mathrm{m}/\mathrm{s}$ (velocity); because the term contains $t^1$, $[A]=(\mathrm{m}/\mathrm{s})/\mathrm{s}=\mathrm{m}/\mathrm{s}^2$.
- id: e
  content: |-
    $\mathrm{s}/\mathrm{m}$
  feedback: |-
    This reverses the required quotient. From $[A][t]=[v]$, $[A]=[v]/[t]=(\mathrm{m}/\mathrm{s})/\mathrm{s}=\mathrm{m}/\mathrm{s}^2$; $\mathrm{s}/\mathrm{m}$ would instead make $At$ have units $\mathrm{s}^2/\mathrm{m}$.
```

---

<a id="dividing-out-a-time-power"></a>
## Dividing Out a Time Power

**Example:** Suppose $\omega(t)=Dt^3+\omega_0$, where $\omega(t)$ has units $\mathrm{rad}/\mathrm{s}$. What are the units of $D$?

**Explanation**

The product $Dt^3$ must have units $\mathrm{rad}/\mathrm{s}$. Since $[t^3]=\mathrm{s}^3$,

$$
[D]\mathrm{s}^3=\frac{\mathrm{rad}}{\mathrm{s}},
$$

so

$$
[D]=\frac{\mathrm{rad}}{\mathrm{s}^4}.
$$

```quiz
type: radio
id: q-2
content: |-
  If $\theta(t)=Et^2+\theta_0$ and $\theta(t)$ has units $\mathrm{rad}$, what are the units of $E$?
options:
- id: a
  content: |-
    $\mathrm{rad}$
  feedback: |-
    This assigns $E$ the angle units and ignores $t^2$, making $Et^2$ have $\mathrm{rad}\cdot\mathrm{s}^2$ rather than $\mathrm{rad}$. Since $Et^2$ must match $\theta$, $[E]=\mathrm{rad}/\mathrm{s}^2$.
- id: b
  content: |-
    $\mathrm{rad}/\mathrm{s}$
  feedback: |-
    This divides out only one time factor, as though the term were $Et$. For $Et^2$, it gives $\mathrm{rad}\cdot\mathrm{s}$ rather than $\mathrm{rad}$; dividing by the full $\mathrm{s}^2$ gives $[E]=\mathrm{rad}/\mathrm{s}^2$.
- id: c
  content: |-
    $\mathrm{rad}/\mathrm{s}^2$
  correct: true
  feedback: |-
    Added terms must share units, so $Et^2$ must match $\theta$ in radians. With $[t^2]=\mathrm{s}^2$, $[E]=\mathrm{rad}/\mathrm{s}^2$.
- id: d
  content: |-
    $\mathrm{rad}/\mathrm{s}^3$
  feedback: |-
    This divides by one extra second, making $Et^2$ have $\mathrm{rad}/\mathrm{s}$ (angular velocity) instead of $\mathrm{rad}$ (angle). Canceling exactly the $t^2$ factor gives $[E]=\mathrm{rad}/\mathrm{s}^2$.
- id: e
  content: |-
    $\mathrm{rad}\cdot\mathrm{s}^2$
  feedback: |-
    This multiplies by $\mathrm{s}^2$ instead of canceling the time factor, so $Et^2$ would have $\mathrm{rad}\cdot\mathrm{s}^4$. Because $Et^2$ must match the angle $\theta$, $[E]=\mathrm{rad}/\mathrm{s}^2$.
```

---

<a id="distinguishing-the-coefficient-from-the-constant-term"></a>
## Distinguishing the Coefficient From the Constant Term

**Example:** In $\alpha_z(t)=Bt^2+C$, find the units of $B$.

**Explanation**

Angular acceleration has units $\mathrm{rad}/\mathrm{s}^2$. The whole product $Bt^2$ must have those units:

$$
[B]\mathrm{s}^2=\frac{\mathrm{rad}}{\mathrm{s}^2}.
$$

Therefore,

$$
[B]=\frac{\mathrm{rad}}{\mathrm{s}^4}.
$$

```quiz
type: radio
id: q-3
content: |-
  The $z$-component of angular acceleration is $\alpha_z(t)=Bt^2+C$. What SI units is $B$ measured in?
options:
- id: a
  content: |-
    $\mathrm{m}/\mathrm{s}^2$
  feedback: |-
    This treats $B$ as a linear acceleration and ignores $t^2$, making $Bt^2$ a length in meters. Because $Bt^2$ must be angular acceleration, $[B]=(\mathrm{rad}/\mathrm{s}^2)/\mathrm{s}^2=\mathrm{rad}/\mathrm{s}^4$.
- id: b
  content: |-
    $\mathrm{m}/\mathrm{s}^3$
  feedback: |-
    This mixes a linear numerator with only one additional inverse second, so $Bt^2$ would have $\mathrm{m}/\mathrm{s}$ (linear speed). The term must be angular acceleration, so $[B]=(\mathrm{rad}/\mathrm{s}^2)/\mathrm{s}^2=\mathrm{rad}/\mathrm{s}^4$.
- id: c
  content: |-
    $\mathrm{m}/\mathrm{s}^4$
  feedback: |-
    The time exponent is correct, but meters make $Bt^2$ a linear acceleration in $\mathrm{m}/\mathrm{s}^2$. The prompt requires angular acceleration, so the numerator must be radians: $[B]=\mathrm{rad}/\mathrm{s}^4$.
- id: d
  content: |-
    $\mathrm{rad}/\mathrm{s}^2$
  feedback: |-
    This gives $B$ the units of $\alpha_z$ or $C$ and ignores $t^2$, so $Bt^2$ would have $\mathrm{rad}$ (angle). Dividing the angular-acceleration units by $\mathrm{s}^2$ gives $[B]=\mathrm{rad}/\mathrm{s}^4$.
- id: e
  content: |-
    $\mathrm{rad}/\mathrm{s}^3$
  feedback: |-
    This removes only one of the two seconds contributed by $t^2$, so $Bt^2$ would have $\mathrm{rad}/\mathrm{s}$ (angular velocity). Dividing by the full $\mathrm{s}^2$ gives $[B]=\mathrm{rad}/\mathrm{s}^4$.
- id: f
  content: |-
    $\mathrm{rad}/\mathrm{s}^4$
  correct: true
  feedback: |-
    Added terms must share units, so $Bt^2$ must match $\alpha_z$ in $\mathrm{rad}/\mathrm{s}^2$. With $[t^2]=\mathrm{s}^2$, $[B]=(\mathrm{rad}/\mathrm{s}^2)/\mathrm{s}^2=\mathrm{rad}/\mathrm{s}^4$.
```

## Summary

When terms are added, their units must match. For $\alpha_z(t)=Bt^2+C$, the product $Bt^2$ has units $\mathrm{rad}/\mathrm{s}^2$, so $B$ must have units $\mathrm{rad}/\mathrm{s}^4$.
