# Originals and labeled generated variants

## original q-141096 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-2y.
$$

 Which of the following is a solution to this equation?

- $y=-2{e}^{-2x}$
- $y=-2{e}^{x}$
- $y=2{e}^{-x}+1$

* III only
* II only
* I only **(correct)**
* None
* I, II, and III

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-2{e}^{-2x},$ we get $\frac{\text{d}y}{\text{d}x}=4{e}^{-2x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2y \\ 4{e}^{-2x} & \overset{?}{=}-2(-2{e}^{-2x}) \\ 4{e}^{-2x} & =4{e}^{-2x}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-2{e}^{-2x}$ *is* a solution to our differential equation.

- Differentiating $y=-2{e}^{x},$ we get $\frac{\text{d}y}{\text{d}x}=-2{e}^{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2y \\ -2{e}^{x} & \overset{?}{=}-2(-2{e}^{x}) \\ -2{e}^{x} & \overset{?}{=}4{e}^{x} \\ 0 & \ne 6{e}^{x}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-2{e}^{x}$ is *not* a solution to our differential equation.

- Differentiating $y=2{e}^{-x}+1,$ we get $\frac{\text{d}y}{\text{d}x}=-2{e}^{-x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2y \\ -2{e}^{-x} & \overset{?}{=}-2(2{e}^{-x}+1) \\ -2{e}^{-x} & \overset{?}{=}-4{e}^{-x}-2 \\ 2{e}^{-x} & \ne -2.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2{e}^{-x}+1$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## generated source-mask q-141096 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(-2\left(\frac{y}{2}\right)\right).
$$

 Which of the following is a solution to this equation?

- $y=2\left(-2{e}^{-2x}\right)$
- $y=2\left(-2{e}^{x}\right)$
- $y=2\left(2{e}^{-x}+1\right)$

* II only
* I, II, and III
* III only
* I only **(correct)**
* None

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(-2{e}^{-2x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(4{e}^{-2x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-2\left(\frac{y}{2}\right) \right)\\2\left( 4{e}^{-2x} \right)& \overset{?}{=}2\left(-2(-2{e}^{-2x}) \right)\\2\left( 4{e}^{-2x} \right)& =2\left(4{e}^{-2x}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(-2{e}^{-2x}\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(-2{e}^{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-2{e}^{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-2\left(\frac{y}{2}\right) \right)\\2\left( -2{e}^{x} \right)& \overset{?}{=}2\left(-2(-2{e}^{x}) \right)\\2\left( -2{e}^{x} \right)& \overset{?}{=}2\left(4{e}^{x} \right)\\ 0 & \ne2\left( 6{e}^{x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(-2{e}^{x}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left(2{e}^{-x}+1\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-2{e}^{-x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-2\left(\frac{y}{2}\right) \right)\\2\left( -2{e}^{-x} \right)& \overset{?}{=}2\left(-2(2{e}^{-x}+1) \right)\\2\left( -2{e}^{-x} \right)& \overset{?}{=}2\left(-4{e}^{-x}-2 \right)\\2\left( 2{e}^{-x} \right)& \ne2\left( -2\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(2{e}^{-x}+1\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## generated source-mask q-141096 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(-2\left(\frac{y}{-3}\right)\right).
$$

 Which of the following is a solution to this equation?

- $y=-3\left(-2{e}^{-2x}\right)$
- $y=-3\left(-2{e}^{x}\right)$
- $y=-3\left(2{e}^{-x}+1\right)$

* II only
* I, II, and III
* III only
* I only **(correct)**
* None

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(-2{e}^{-2x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(4{e}^{-2x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-2\left(\frac{y}{-3}\right) \right)\\-3\left( 4{e}^{-2x} \right)& \overset{?}{=}-3\left(-2(-2{e}^{-2x}) \right)\\-3\left( 4{e}^{-2x} \right)& =-3\left(4{e}^{-2x}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(-2{e}^{-2x}\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(-2{e}^{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-2{e}^{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-2\left(\frac{y}{-3}\right) \right)\\-3\left( -2{e}^{x} \right)& \overset{?}{=}-3\left(-2(-2{e}^{x}) \right)\\-3\left( -2{e}^{x} \right)& \overset{?}{=}-3\left(4{e}^{x} \right)\\ 0 & \ne-3\left( 6{e}^{x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(-2{e}^{x}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left(2{e}^{-x}+1\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-2{e}^{-x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-2\left(\frac{y}{-3}\right) \right)\\-3\left( -2{e}^{-x} \right)& \overset{?}{=}-3\left(-2(2{e}^{-x}+1) \right)\\-3\left( -2{e}^{-x} \right)& \overset{?}{=}-3\left(-4{e}^{-x}-2 \right)\\-3\left( 2{e}^{-x} \right)& \ne-3\left( -2\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(2{e}^{-x}+1\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## original q-79335 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation 

$$
\frac{\text{d}y}{\text{d}x}=\frac{2y}{x}-2,\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=2x$
- $y={x}^{2}$
- $y={x}^{3}$

* I and III only
* II only
* I only **(correct)**
* II and III only
* I and II only

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2x,$ we get $\frac{\text{d}y}{\text{d}x}=2.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2y}{x}-2 \\ 2 & \overset{?}{=}\frac{2\cdot 2x}{x}-2 \\ 2 & \overset{?}{=}\frac{4x}{x}-2 \\ 2 & \overset{?}{=}4-2 \\ 2 & =2.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2x$ *is* a solution to our differential equation.

- Differentiating $y={x}^{2},$ we get $\frac{\text{d}y}{\text{d}x}=2x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2y}{x}-2 \\ 2x & \overset{?}{=}\frac{2\cdot {x}^{2}}{x}-2 \\ 2x & \overset{?}{=}\frac{2{x}^{2}}{x}-2 \\ 2x & \overset{?}{=}2x-2 \\ 0 & \ne -2.\,\times \end{aligned}
$$

This statement is *false*. Therefore, the function $y={x}^{2}$ is *not* a solution to our differential equation.

- Differentiating $y={x}^{3},$ we get $\frac{\text{d}y}{\text{d}x}=3{x}^{2}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2y}{x}-2 \\ 3{x}^{2} & \overset{?}{=}\frac{2\cdot {x}^{3}}{x}-2 \\ 3{x}^{2} & \overset{?}{=}\frac{2{x}^{3}}{x}-2 \\ 3{x}^{2} & \overset{?}{=}2{x}^{2}-2 \\ {x}^{2} & \ne -2\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y={x}^{3}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## generated source-mask q-79335 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation 

$$
\frac{\text{d}y}{\text{d}x}=2\left(\frac{2\left(\frac{y}{2}\right)}{x}-2\right),\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=2\left(2x\right)$
- $y=2\left({x}^{2}\right)$
- $y=2\left({x}^{3}\right)$

* II only
* I and II only
* I and III only
* I only **(correct)**
* II and III only

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(2x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(2\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{2\left(\frac{y}{2}\right)}{x}-2 \right)\\2\left( 2 \right)& \overset{?}{=}2\left(\frac{2\cdot 2x}{x}-2 \right)\\2\left( 2 \right)& \overset{?}{=}2\left(\frac{4x}{x}-2 \right)\\2\left( 2 \right)& \overset{?}{=}2\left(4-2 \right)\\2\left( 2 \right)& =2\left(2\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(2x\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left({x}^{2}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(2x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{2\left(\frac{y}{2}\right)}{x}-2 \right)\\2\left( 2x \right)& \overset{?}{=}2\left(\frac{2\cdot {x}^{2}}{x}-2 \right)\\2\left( 2x \right)& \overset{?}{=}2\left(\frac{2{x}^{2}}{x}-2 \right)\\2\left( 2x \right)& \overset{?}{=}2\left(2x-2 \right)\\ 0 & \ne2\left( -2\right).\,\times \end{aligned}
$$

This statement is *false*. Therefore, the function $y=2\left({x}^{2}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left({x}^{3}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(3{x}^{2}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{2\left(\frac{y}{2}\right)}{x}-2 \right)\\2\left( 3{x}^{2} \right)& \overset{?}{=}2\left(\frac{2\cdot {x}^{3}}{x}-2 \right)\\2\left( 3{x}^{2} \right)& \overset{?}{=}2\left(\frac{2{x}^{3}}{x}-2 \right)\\2\left( 3{x}^{2} \right)& \overset{?}{=}2\left(2{x}^{2}-2 \right)\\2\left( {x}^{2} \right)& \ne2\left( -2\right)\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left({x}^{3}\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## generated source-mask q-79335 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation 

$$
\frac{\text{d}y}{\text{d}x}=-3\left(\frac{2\left(\frac{y}{-3}\right)}{x}-2\right),\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=-3\left(2x\right)$
- $y=-3\left({x}^{2}\right)$
- $y=-3\left({x}^{3}\right)$

* II only
* I and II only
* I and III only
* I only **(correct)**
* II and III only

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(2x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(2\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{2\left(\frac{y}{-3}\right)}{x}-2 \right)\\-3\left( 2 \right)& \overset{?}{=}-3\left(\frac{2\cdot 2x}{x}-2 \right)\\-3\left( 2 \right)& \overset{?}{=}-3\left(\frac{4x}{x}-2 \right)\\-3\left( 2 \right)& \overset{?}{=}-3\left(4-2 \right)\\-3\left( 2 \right)& =-3\left(2\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(2x\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left({x}^{2}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(2x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{2\left(\frac{y}{-3}\right)}{x}-2 \right)\\-3\left( 2x \right)& \overset{?}{=}-3\left(\frac{2\cdot {x}^{2}}{x}-2 \right)\\-3\left( 2x \right)& \overset{?}{=}-3\left(\frac{2{x}^{2}}{x}-2 \right)\\-3\left( 2x \right)& \overset{?}{=}-3\left(2x-2 \right)\\ 0 & \ne-3\left( -2\right).\,\times \end{aligned}
$$

This statement is *false*. Therefore, the function $y=-3\left({x}^{2}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left({x}^{3}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(3{x}^{2}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{2\left(\frac{y}{-3}\right)}{x}-2 \right)\\-3\left( 3{x}^{2} \right)& \overset{?}{=}-3\left(\frac{2\cdot {x}^{3}}{x}-2 \right)\\-3\left( 3{x}^{2} \right)& \overset{?}{=}-3\left(\frac{2{x}^{3}}{x}-2 \right)\\-3\left( 3{x}^{2} \right)& \overset{?}{=}-3\left(2{x}^{2}-2 \right)\\-3\left( {x}^{2} \right)& \ne-3\left( -2\right)\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left({x}^{3}\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## original q-141091 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2y\operatorname{cot}⁡2x.
$$

 Which of the following is a solution to this equation?

- $y=\operatorname{sin}⁡2x$
- $y=\operatorname{sin}⁡2x+1$
- $y=-3\operatorname{sin}⁡2x$

* III only
* I and III only **(correct)**
* I only
* I and II only
* II only

**Correct answer:** I and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=\operatorname{sin}⁡2x,$ we get $\frac{\text{d}y}{\text{d}x}=2\operatorname{cos}⁡2x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2y\operatorname{cot}⁡2x \\ 2\operatorname{cos}⁡2x & \overset{?}{=}2\operatorname{sin}⁡2x\cdot \operatorname{cot}⁡2x \\ 2\operatorname{cos}⁡2x & =2\operatorname{cos}⁡2x.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=\operatorname{sin}⁡2x$ *is* a solution to our differential equation.

- Differentiating $y=\operatorname{sin}⁡2x+1,$ we get $\frac{\text{d}y}{\text{d}x}=2\operatorname{cos}⁡2x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2y\operatorname{cot}⁡2x \\ 2\operatorname{cos}⁡2x & \overset{?}{=}2(\operatorname{sin}⁡2x+1)\operatorname{cot}⁡2x \\ 2\operatorname{cos}⁡2x & \overset{?}{=}2\operatorname{cos}⁡2x+2\operatorname{cot}⁡2x \\ 0 & =2\operatorname{cot}⁡2x.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=\operatorname{sin}⁡2x+1$ is *not* a solution to our differential equation.

- Differentiating $y=-3\operatorname{sin}⁡2x,$ we get $\frac{\text{d}y}{\text{d}x}=-6\operatorname{cos}⁡2x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2y\operatorname{cot}⁡2x \\ -6\operatorname{cos}⁡2x & \overset{?}{=}2(-3\operatorname{sin}⁡2x)\cdot \operatorname{cot}⁡2x \\ -6\operatorname{cos}⁡2x & =-6\operatorname{cos}⁡2x.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\operatorname{sin}⁡2x$ *is* a solution to our differential equation.

Therefore, the correct answer is "I and III only."

## generated source-mask q-141091 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(2\left(\frac{y}{2}\right)\operatorname{cot}⁡2x\right).
$$

 Which of the following is a solution to this equation?

- $y=2\left(\operatorname{sin}⁡2x\right)$
- $y=2\left(\operatorname{sin}⁡2x+1\right)$
- $y=2\left(-3\operatorname{sin}⁡2x\right)$

* I and III only **(correct)**
* II only
* III only
* I only
* I and II only

**Correct answer:** I and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(\operatorname{sin}⁡2x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(2\operatorname{cos}⁡2x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(2\left(\frac{y}{2}\right)\operatorname{cot}⁡2x \right)\\2\left( 2\operatorname{cos}⁡2x \right)& \overset{?}{=}2\left(2\operatorname{sin}⁡2x\cdot \operatorname{cot}⁡2x \right)\\2\left( 2\operatorname{cos}⁡2x \right)& =2\left(2\operatorname{cos}⁡2x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(\operatorname{sin}⁡2x\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(\operatorname{sin}⁡2x+1\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(2\operatorname{cos}⁡2x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(2\left(\frac{y}{2}\right)\operatorname{cot}⁡2x \right)\\2\left( 2\operatorname{cos}⁡2x \right)& \overset{?}{=}2\left(2(\operatorname{sin}⁡2x+1)\operatorname{cot}⁡2x \right)\\2\left( 2\operatorname{cos}⁡2x \right)& \overset{?}{=}2\left(2\operatorname{cos}⁡2x+2\operatorname{cot}⁡2x \right)\\ 0 & =2\left(2\operatorname{cot}⁡2x\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(\operatorname{sin}⁡2x+1\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left(-3\operatorname{sin}⁡2x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-6\operatorname{cos}⁡2x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(2\left(\frac{y}{2}\right)\operatorname{cot}⁡2x \right)\\2\left( -6\operatorname{cos}⁡2x \right)& \overset{?}{=}2\left(2(-3\operatorname{sin}⁡2x)\cdot \operatorname{cot}⁡2x \right)\\2\left( -6\operatorname{cos}⁡2x \right)& =2\left(-6\operatorname{cos}⁡2x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(-3\operatorname{sin}⁡2x\right)$ *is* a solution to our differential equation.

Therefore, the correct answer is "I and III only."

## generated source-mask q-141091 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(2\left(\frac{y}{-3}\right)\operatorname{cot}⁡2x\right).
$$

 Which of the following is a solution to this equation?

- $y=-3\left(\operatorname{sin}⁡2x\right)$
- $y=-3\left(\operatorname{sin}⁡2x+1\right)$
- $y=-3\left(-3\operatorname{sin}⁡2x\right)$

* I and III only **(correct)**
* II only
* III only
* I only
* I and II only

**Correct answer:** I and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(\operatorname{sin}⁡2x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(2\operatorname{cos}⁡2x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(2\left(\frac{y}{-3}\right)\operatorname{cot}⁡2x \right)\\-3\left( 2\operatorname{cos}⁡2x \right)& \overset{?}{=}-3\left(2\operatorname{sin}⁡2x\cdot \operatorname{cot}⁡2x \right)\\-3\left( 2\operatorname{cos}⁡2x \right)& =-3\left(2\operatorname{cos}⁡2x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(\operatorname{sin}⁡2x\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(\operatorname{sin}⁡2x+1\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(2\operatorname{cos}⁡2x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(2\left(\frac{y}{-3}\right)\operatorname{cot}⁡2x \right)\\-3\left( 2\operatorname{cos}⁡2x \right)& \overset{?}{=}-3\left(2(\operatorname{sin}⁡2x+1)\operatorname{cot}⁡2x \right)\\-3\left( 2\operatorname{cos}⁡2x \right)& \overset{?}{=}-3\left(2\operatorname{cos}⁡2x+2\operatorname{cot}⁡2x \right)\\ 0 & =-3\left(2\operatorname{cot}⁡2x\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(\operatorname{sin}⁡2x+1\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left(-3\operatorname{sin}⁡2x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-6\operatorname{cos}⁡2x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(2\left(\frac{y}{-3}\right)\operatorname{cot}⁡2x \right)\\-3\left( -6\operatorname{cos}⁡2x \right)& \overset{?}{=}-3\left(2(-3\operatorname{sin}⁡2x)\cdot \operatorname{cot}⁡2x \right)\\-3\left( -6\operatorname{cos}⁡2x \right)& =-3\left(-6\operatorname{cos}⁡2x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(-3\operatorname{sin}⁡2x\right)$ *is* a solution to our differential equation.

Therefore, the correct answer is "I and III only."

## original q-141092 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-y\operatorname{tan}⁡x.
$$

 Which of the following is a solution to this equation?

- $y=\operatorname{cos}⁡x$
- $y=3\operatorname{cos}⁡x$
- $y=-2\operatorname{cos}⁡x$

* I only
* III only
* I, II, and III **(correct)**
* II only
* I and II only

**Correct answer:** I, II, and III

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=\operatorname{cos}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=-\operatorname{sin}⁡x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-y\operatorname{tan}⁡x \\ -\operatorname{sin}⁡x & \overset{?}{=}-\operatorname{cos}⁡x\cdot \operatorname{tan}⁡x \\ -\operatorname{sin}⁡x & =-\operatorname{sin}⁡x.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=\operatorname{cos}⁡x$ *is* a solution to our differential equation.

- Differentiating $y=3\operatorname{cos}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=-3\operatorname{sin}⁡x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-y\operatorname{tan}⁡x \\ -3\operatorname{sin}⁡x & \overset{?}{=}-3\operatorname{cos}⁡x\cdot \operatorname{tan}⁡x \\ -3\operatorname{sin}⁡x & =-3\operatorname{sin}⁡x.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=3\operatorname{cos}⁡x$ *is* a solution to our differential equation.

- Differentiating $y=-2\operatorname{cos}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=2\operatorname{sin}⁡x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-y\operatorname{tan}⁡x \\ 2\operatorname{sin}⁡x & \overset{?}{=}-(-2\operatorname{cos}⁡x)\cdot \operatorname{tan}⁡x \\ 2\operatorname{sin}⁡x & =2\operatorname{sin}⁡x.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-2\operatorname{cos}⁡x$ *is* a solution to our differential equation.

Therefore, the correct answer is "I, II, and III."

## generated source-mask q-141092 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(-\left(\frac{y}{2}\right)\operatorname{tan}⁡x\right).
$$

 Which of the following is a solution to this equation?

- $y=2\left(\operatorname{cos}⁡x\right)$
- $y=2\left(3\operatorname{cos}⁡x\right)$
- $y=2\left(-2\operatorname{cos}⁡x\right)$

* III only
* I and II only
* I only
* I, II, and III **(correct)**
* II only

**Correct answer:** I, II, and III

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(\operatorname{cos}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-\operatorname{sin}⁡x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\left(\frac{y}{2}\right)\operatorname{tan}⁡x \right)\\2\left( -\operatorname{sin}⁡x \right)& \overset{?}{=}2\left(-\operatorname{cos}⁡x\cdot \operatorname{tan}⁡x \right)\\2\left( -\operatorname{sin}⁡x \right)& =2\left(-\operatorname{sin}⁡x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(\operatorname{cos}⁡x\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(3\operatorname{cos}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-3\operatorname{sin}⁡x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\left(\frac{y}{2}\right)\operatorname{tan}⁡x \right)\\2\left( -3\operatorname{sin}⁡x \right)& \overset{?}{=}2\left(-3\operatorname{cos}⁡x\cdot \operatorname{tan}⁡x \right)\\2\left( -3\operatorname{sin}⁡x \right)& =2\left(-3\operatorname{sin}⁡x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(3\operatorname{cos}⁡x\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(-2\operatorname{cos}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(2\operatorname{sin}⁡x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\left(\frac{y}{2}\right)\operatorname{tan}⁡x \right)\\2\left( 2\operatorname{sin}⁡x \right)& \overset{?}{=}2\left(-(-2\operatorname{cos}⁡x)\cdot \operatorname{tan}⁡x \right)\\2\left( 2\operatorname{sin}⁡x \right)& =2\left(2\operatorname{sin}⁡x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(-2\operatorname{cos}⁡x\right)$ *is* a solution to our differential equation.

Therefore, the correct answer is "I, II, and III."

## generated source-mask q-141092 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(-\left(\frac{y}{-3}\right)\operatorname{tan}⁡x\right).
$$

 Which of the following is a solution to this equation?

- $y=-3\left(\operatorname{cos}⁡x\right)$
- $y=-3\left(3\operatorname{cos}⁡x\right)$
- $y=-3\left(-2\operatorname{cos}⁡x\right)$

* III only
* I and II only
* I only
* I, II, and III **(correct)**
* II only

**Correct answer:** I, II, and III

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(\operatorname{cos}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-\operatorname{sin}⁡x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\left(\frac{y}{-3}\right)\operatorname{tan}⁡x \right)\\-3\left( -\operatorname{sin}⁡x \right)& \overset{?}{=}-3\left(-\operatorname{cos}⁡x\cdot \operatorname{tan}⁡x \right)\\-3\left( -\operatorname{sin}⁡x \right)& =-3\left(-\operatorname{sin}⁡x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(\operatorname{cos}⁡x\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(3\operatorname{cos}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-3\operatorname{sin}⁡x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\left(\frac{y}{-3}\right)\operatorname{tan}⁡x \right)\\-3\left( -3\operatorname{sin}⁡x \right)& \overset{?}{=}-3\left(-3\operatorname{cos}⁡x\cdot \operatorname{tan}⁡x \right)\\-3\left( -3\operatorname{sin}⁡x \right)& =-3\left(-3\operatorname{sin}⁡x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(3\operatorname{cos}⁡x\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(-2\operatorname{cos}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(2\operatorname{sin}⁡x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\left(\frac{y}{-3}\right)\operatorname{tan}⁡x \right)\\-3\left( 2\operatorname{sin}⁡x \right)& \overset{?}{=}-3\left(-(-2\operatorname{cos}⁡x)\cdot \operatorname{tan}⁡x \right)\\-3\left( 2\operatorname{sin}⁡x \right)& =-3\left(2\operatorname{sin}⁡x\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(-2\operatorname{cos}⁡x\right)$ *is* a solution to our differential equation.

Therefore, the correct answer is "I, II, and III."

## original q-141093 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=\frac{2}{{e}^{y/2}}.
$$

 Which of the following is a solution to this equation?

- $y=\operatorname{ln}⁡x$
- $y=2\operatorname{ln}⁡x$
- $y=-\operatorname{ln}⁡x$

* III only
* I and III only
* II only **(correct)**
* I only
* II and III only

**Correct answer:** II only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=\operatorname{ln}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=\frac{1}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2}{{e}^{y/2}} \\ \frac{1}{x} & \overset{?}{=}\frac{2}{{e}^{(\operatorname{ln}⁡x)/2}} \\ \frac{1}{x} & \overset{?}{=}\frac{2}{{e}^{\operatorname{ln}⁡\sqrt{x}}} \\ \frac{1}{x} & =\frac{2}{\sqrt{x}} \\ 1 & =2\sqrt{x}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=\operatorname{ln}⁡x$ is *not* a solution to our differential equation.

- Differentiating $y=2\operatorname{ln}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=\frac{2}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2}{{e}^{y/2}} \\ \frac{2}{x} & \overset{?}{=}\frac{2}{{e}^{(2\operatorname{ln}⁡x)/2}} \\ \frac{2}{x} & \overset{?}{=}\frac{2}{{e}^{\operatorname{ln}⁡x}} \\ \frac{2}{x} & =\frac{2}{x}.\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=2\operatorname{ln}⁡x$ *is* a solution to our differential equation.

- Differentiating $y=-\operatorname{ln}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=-\frac{1}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2}{{e}^{y/2}} \\ -\frac{1}{x} & \overset{?}{=}\frac{2}{{e}^{(-\operatorname{ln}⁡x)/2}} \\ -\frac{1}{x} & \overset{?}{=}\frac{2}{{e}^{\operatorname{ln}⁡({x}^{-1/2})}} \\ -\frac{1}{x} & \overset{?}{=}\frac{2}{{x}^{-1/2}} \\ -\frac{1}{x} & =2\sqrt{x} \\ -1 & =2x\sqrt{x}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-\operatorname{ln}⁡x$ is *not* a solution to our differential equation.

Therefore, the correct answer is "II only."

## generated source-mask q-141093 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(\frac{2}{{e}^{\left(\frac{y}{2}\right)/2}}\right).
$$

 Which of the following is a solution to this equation?

- $y=2\left(\operatorname{ln}⁡x\right)$
- $y=2\left(2\operatorname{ln}⁡x\right)$
- $y=2\left(-\operatorname{ln}⁡x\right)$

* I and III only
* II and III only
* III only
* II only **(correct)**
* I only

**Correct answer:** II only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(\frac{1}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{2}{{e}^{\left(\frac{y}{2}\right)/2}} \right)\\2\left( \frac{1}{x} \right)& \overset{?}{=}2\left(\frac{2}{{e}^{(\operatorname{ln}⁡x)/2}} \right)\\2\left( \frac{1}{x} \right)& \overset{?}{=}2\left(\frac{2}{{e}^{\operatorname{ln}⁡\sqrt{x}}} \right)\\2\left( \frac{1}{x} \right)& =2\left(\frac{2}{\sqrt{x}} \right)\\2\left( 1 \right)& =2\left(2\sqrt{x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left(2\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(\frac{2}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{2}{{e}^{\left(\frac{y}{2}\right)/2}} \right)\\2\left( \frac{2}{x} \right)& \overset{?}{=}2\left(\frac{2}{{e}^{(2\operatorname{ln}⁡x)/2}} \right)\\2\left( \frac{2}{x} \right)& \overset{?}{=}2\left(\frac{2}{{e}^{\operatorname{ln}⁡x}} \right)\\2\left( \frac{2}{x} \right)& =2\left(\frac{2}{x}\right).\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=2\left(2\operatorname{ln}⁡x\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(-\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-\frac{1}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{2}{{e}^{\left(\frac{y}{2}\right)/2}} \right)\\2\left( -\frac{1}{x} \right)& \overset{?}{=}2\left(\frac{2}{{e}^{(-\operatorname{ln}⁡x)/2}} \right)\\2\left( -\frac{1}{x} \right)& \overset{?}{=}2\left(\frac{2}{{e}^{\operatorname{ln}⁡({x}^{-1/2})}} \right)\\2\left( -\frac{1}{x} \right)& \overset{?}{=}2\left(\frac{2}{{x}^{-1/2}} \right)\\2\left( -\frac{1}{x} \right)& =2\left(2\sqrt{x} \right)\\2\left( -1 \right)& =2\left(2x\sqrt{x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(-\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "II only."

## generated source-mask q-141093 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(\frac{2}{{e}^{\left(\frac{y}{-3}\right)/2}}\right).
$$

 Which of the following is a solution to this equation?

- $y=-3\left(\operatorname{ln}⁡x\right)$
- $y=-3\left(2\operatorname{ln}⁡x\right)$
- $y=-3\left(-\operatorname{ln}⁡x\right)$

* I and III only
* II and III only
* III only
* II only **(correct)**
* I only

**Correct answer:** II only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(\frac{1}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{2}{{e}^{\left(\frac{y}{-3}\right)/2}} \right)\\-3\left( \frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{2}{{e}^{(\operatorname{ln}⁡x)/2}} \right)\\-3\left( \frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{2}{{e}^{\operatorname{ln}⁡\sqrt{x}}} \right)\\-3\left( \frac{1}{x} \right)& =-3\left(\frac{2}{\sqrt{x}} \right)\\-3\left( 1 \right)& =-3\left(2\sqrt{x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left(2\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(\frac{2}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{2}{{e}^{\left(\frac{y}{-3}\right)/2}} \right)\\-3\left( \frac{2}{x} \right)& \overset{?}{=}-3\left(\frac{2}{{e}^{(2\operatorname{ln}⁡x)/2}} \right)\\-3\left( \frac{2}{x} \right)& \overset{?}{=}-3\left(\frac{2}{{e}^{\operatorname{ln}⁡x}} \right)\\-3\left( \frac{2}{x} \right)& =-3\left(\frac{2}{x}\right).\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=-3\left(2\operatorname{ln}⁡x\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(-\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-\frac{1}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{2}{{e}^{\left(\frac{y}{-3}\right)/2}} \right)\\-3\left( -\frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{2}{{e}^{(-\operatorname{ln}⁡x)/2}} \right)\\-3\left( -\frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{2}{{e}^{\operatorname{ln}⁡({x}^{-1/2})}} \right)\\-3\left( -\frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{2}{{x}^{-1/2}} \right)\\-3\left( -\frac{1}{x} \right)& =-3\left(2\sqrt{x} \right)\\-3\left( -1 \right)& =-3\left(2x\sqrt{x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(-\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "II only."

## original q-141098 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=\frac{4y}{x},\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=4x$
- $y=2{x}^{2}$
- $y={x}^{3}$

* I and II only
* III only
* I only
* II and III only
* None **(correct)**

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=4x,$ we get $\frac{\text{d}y}{\text{d}x}=4.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4y}{x} \\ 4 & \overset{?}{=}\frac{4(4x)}{x} \\ 4 & \ne 16.\,\times \end{aligned}
$$

This statement is *false*. Therefore, the function $y=4x$ is *not* a solution to our differential equation.

- Differentiating $y=2{x}^{2},$ we get $\frac{\text{d}y}{\text{d}x}=4x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4y}{x} \\ 4x & \overset{?}{=}\frac{4(2{x}^{2})}{x} \\ 4x & \overset{?}{=}8x \\ -4x & \ne 0.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2{x}^{2}$ is *not* a solution to our differential equation.

- Differentiating $y={x}^{3},$ we get $\frac{\text{d}y}{\text{d}x}=3{x}^{2}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4y}{x} \\ 3{x}^{2} & \overset{?}{=}\frac{4({x}^{3})}{x} \\ 3{x}^{2} & \ne 4{x}^{2} \\ 0 & \ne {x}^{2}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y={x}^{3}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## generated source-mask q-141098 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(\frac{4\left(\frac{y}{2}\right)}{x}\right),\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=2\left(4x\right)$
- $y=2\left(2{x}^{2}\right)$
- $y=2\left({x}^{3}\right)$

* III only
* None **(correct)**
* I and II only
* I only
* II and III only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(4x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(4\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{4\left(\frac{y}{2}\right)}{x} \right)\\2\left( 4 \right)& \overset{?}{=}2\left(\frac{4(4x)}{x} \right)\\2\left( 4 \right)& \ne2\left( 16\right).\,\times \end{aligned}
$$

This statement is *false*. Therefore, the function $y=2\left(4x\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left(2{x}^{2}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(4x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{4\left(\frac{y}{2}\right)}{x} \right)\\2\left( 4x \right)& \overset{?}{=}2\left(\frac{4(2{x}^{2})}{x} \right)\\2\left( 4x \right)& \overset{?}{=}2\left(8x \right)\\2\left( -4x \right)& \ne 0.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(2{x}^{2}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left({x}^{3}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(3{x}^{2}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{4\left(\frac{y}{2}\right)}{x} \right)\\2\left( 3{x}^{2} \right)& \overset{?}{=}2\left(\frac{4({x}^{3})}{x} \right)\\2\left( 3{x}^{2} \right)& \ne2\left( 4{x}^{2} \right)\\ 0 & \ne2\left( {x}^{2}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left({x}^{3}\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## generated source-mask q-141098 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(\frac{4\left(\frac{y}{-3}\right)}{x}\right),\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=-3\left(4x\right)$
- $y=-3\left(2{x}^{2}\right)$
- $y=-3\left({x}^{3}\right)$

* III only
* None **(correct)**
* I and II only
* I only
* II and III only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(4x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(4\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{4\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( 4 \right)& \overset{?}{=}-3\left(\frac{4(4x)}{x} \right)\\-3\left( 4 \right)& \ne-3\left( 16\right).\,\times \end{aligned}
$$

This statement is *false*. Therefore, the function $y=-3\left(4x\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left(2{x}^{2}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(4x\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{4\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( 4x \right)& \overset{?}{=}-3\left(\frac{4(2{x}^{2})}{x} \right)\\-3\left( 4x \right)& \overset{?}{=}-3\left(8x \right)\\-3\left( -4x \right)& \ne 0.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(2{x}^{2}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left({x}^{3}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(3{x}^{2}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{4\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( 3{x}^{2} \right)& \overset{?}{=}-3\left(\frac{4({x}^{3})}{x} \right)\\-3\left( 3{x}^{2} \right)& \ne-3\left( 4{x}^{2} \right)\\ 0 & \ne-3\left( {x}^{2}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left({x}^{3}\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## original q-141099 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-\frac{2y}{x},\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=-\frac{1}{x}$
- $y=-\frac{1}{{x}^{2}}$
- $y=\frac{4}{{x}^{2}}$

* II and III only **(correct)**
* I and II only
* I only
* III only
* II only

**Correct answer:** II and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-\frac{1}{x},$ we get $\frac{\text{d}y}{\text{d}x}=\frac{1}{{x}^{2}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{2y}{x} \\ \frac{1}{{x}^{2}} & \overset{?}{=}-\frac{2(-\frac{1}{x})}{x} \\ \frac{1}{{x}^{2}} & \overset{?}{=}\frac{2}{{x}^{2}} \\ 0 & \ne \frac{1}{{x}^{2}}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-\frac{1}{x}$ is *not* a solution to our differential equation.

- Differentiating $y=-\frac{1}{{x}^{2}},$ we get $\frac{\text{d}y}{\text{d}x}=\frac{2}{{x}^{3}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{2y}{x} \\ \frac{2}{{x}^{3}} & \overset{?}{=}-\frac{2(-\frac{1}{{x}^{2}})}{x} \\ \frac{2}{{x}^{3}} & =\frac{2}{{x}^{3}}.\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=-\frac{1}{{x}^{2}}$ *is* a solution to our differential equation.

- Differentiating $y=\frac{4}{{x}^{2}},$ we get $\frac{\text{d}y}{\text{d}x}=-\frac{8}{{x}^{3}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{2y}{x} \\ -\frac{8}{{x}^{3}} & \overset{?}{=}-\frac{2(\frac{4}{{x}^{2}})}{x} \\ -\frac{8}{{x}^{3}} & =-\frac{8}{{x}^{3}}.\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=\frac{4}{{x}^{2}}$ *is* a solution to our differential equation.

Therefore, the correct answer is "II and III only."

## generated source-mask q-141099 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(-\frac{2\left(\frac{y}{2}\right)}{x}\right),\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=2\left(-\frac{1}{x}\right)$
- $y=2\left(-\frac{1}{{x}^{2}}\right)$
- $y=2\left(\frac{4}{{x}^{2}}\right)$

* I and II only
* II only
* II and III only **(correct)**
* I only
* III only

**Correct answer:** II and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(-\frac{1}{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(\frac{1}{{x}^{2}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\frac{2\left(\frac{y}{2}\right)}{x} \right)\\2\left( \frac{1}{{x}^{2}} \right)& \overset{?}{=}2\left(-\frac{2(-\frac{1}{x})}{x} \right)\\2\left( \frac{1}{{x}^{2}} \right)& \overset{?}{=}2\left(\frac{2}{{x}^{2}} \right)\\ 0 & \ne2\left( \frac{1}{{x}^{2}}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(-\frac{1}{x}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left(-\frac{1}{{x}^{2}}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(\frac{2}{{x}^{3}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\frac{2\left(\frac{y}{2}\right)}{x} \right)\\2\left( \frac{2}{{x}^{3}} \right)& \overset{?}{=}2\left(-\frac{2(-\frac{1}{{x}^{2}})}{x} \right)\\2\left( \frac{2}{{x}^{3}} \right)& =2\left(\frac{2}{{x}^{3}}\right).\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=2\left(-\frac{1}{{x}^{2}}\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(\frac{4}{{x}^{2}}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-\frac{8}{{x}^{3}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\frac{2\left(\frac{y}{2}\right)}{x} \right)\\2\left( -\frac{8}{{x}^{3}} \right)& \overset{?}{=}2\left(-\frac{2(\frac{4}{{x}^{2}})}{x} \right)\\2\left( -\frac{8}{{x}^{3}} \right)& =2\left(-\frac{8}{{x}^{3}}\right).\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=2\left(\frac{4}{{x}^{2}}\right)$ *is* a solution to our differential equation.

Therefore, the correct answer is "II and III only."

## generated source-mask q-141099 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(-\frac{2\left(\frac{y}{-3}\right)}{x}\right),\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=-3\left(-\frac{1}{x}\right)$
- $y=-3\left(-\frac{1}{{x}^{2}}\right)$
- $y=-3\left(\frac{4}{{x}^{2}}\right)$

* I and II only
* II only
* II and III only **(correct)**
* I only
* III only

**Correct answer:** II and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(-\frac{1}{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(\frac{1}{{x}^{2}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\frac{2\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( \frac{1}{{x}^{2}} \right)& \overset{?}{=}-3\left(-\frac{2(-\frac{1}{x})}{x} \right)\\-3\left( \frac{1}{{x}^{2}} \right)& \overset{?}{=}-3\left(\frac{2}{{x}^{2}} \right)\\ 0 & \ne-3\left( \frac{1}{{x}^{2}}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(-\frac{1}{x}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left(-\frac{1}{{x}^{2}}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(\frac{2}{{x}^{3}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\frac{2\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( \frac{2}{{x}^{3}} \right)& \overset{?}{=}-3\left(-\frac{2(-\frac{1}{{x}^{2}})}{x} \right)\\-3\left( \frac{2}{{x}^{3}} \right)& =-3\left(\frac{2}{{x}^{3}}\right).\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=-3\left(-\frac{1}{{x}^{2}}\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(\frac{4}{{x}^{2}}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-\frac{8}{{x}^{3}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\frac{2\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( -\frac{8}{{x}^{3}} \right)& \overset{?}{=}-3\left(-\frac{2(\frac{4}{{x}^{2}})}{x} \right)\\-3\left( -\frac{8}{{x}^{3}} \right)& =-3\left(-\frac{8}{{x}^{3}}\right).\,✓\end{aligned}
$$

This statement is *true.* Therefore, the function $y=-3\left(\frac{4}{{x}^{2}}\right)$ *is* a solution to our differential equation.

Therefore, the correct answer is "II and III only."

## original q-141101 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=\frac{5y}{x},\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y={x}^{5}$
- $y={x}^{10}$
- $y=5{x}^{4}$

* III only
* II only
* None
* II and III only
* I only **(correct)**

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y={x}^{5},$ we get $\frac{\text{d}y}{\text{d}x}=5{x}^{4}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{5y}{x} \\ 5{x}^{4} & \overset{?}{=}\frac{5({x}^{5})}{x} \\ 5{x}^{4} & =5{x}^{4}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y={x}^{5}$ *is* a solution to our differential equation.

- Differentiating $y={x}^{10},$ we get $\frac{\text{d}y}{\text{d}x}=10{x}^{9}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{5y}{x} \\ 10{x}^{9} & \overset{?}{=}\frac{5({x}^{10})}{x} \\ 10{x}^{9} & \overset{?}{=}5{x}^{9} \\ 5{x}^{9} & \ne 0.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y={x}^{10}$ is *not* a solution to our differential equation.

- Differentiating $y=5{x}^{4},$ we get $\frac{\text{d}y}{\text{d}x}=20{x}^{3}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{5y}{x} \\ 20{x}^{3} & \overset{?}{=}\frac{5(5{x}^{4})}{x} \\ 20{x}^{3} & \overset{?}{=}25{x}^{3} \\ 0 & \ne 5{x}^{3}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=5{x}^{4}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## generated source-mask q-141101 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(\frac{5\left(\frac{y}{2}\right)}{x}\right),\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=2\left({x}^{5}\right)$
- $y=2\left({x}^{10}\right)$
- $y=2\left(5{x}^{4}\right)$

* II only
* I only **(correct)**
* III only
* None
* II and III only

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left({x}^{5}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(5{x}^{4}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{5\left(\frac{y}{2}\right)}{x} \right)\\2\left( 5{x}^{4} \right)& \overset{?}{=}2\left(\frac{5({x}^{5})}{x} \right)\\2\left( 5{x}^{4} \right)& =2\left(5{x}^{4}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left({x}^{5}\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left({x}^{10}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(10{x}^{9}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{5\left(\frac{y}{2}\right)}{x} \right)\\2\left( 10{x}^{9} \right)& \overset{?}{=}2\left(\frac{5({x}^{10})}{x} \right)\\2\left( 10{x}^{9} \right)& \overset{?}{=}2\left(5{x}^{9} \right)\\2\left( 5{x}^{9} \right)& \ne 0.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left({x}^{10}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left(5{x}^{4}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(20{x}^{3}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{5\left(\frac{y}{2}\right)}{x} \right)\\2\left( 20{x}^{3} \right)& \overset{?}{=}2\left(\frac{5(5{x}^{4})}{x} \right)\\2\left( 20{x}^{3} \right)& \overset{?}{=}2\left(25{x}^{3} \right)\\ 0 & \ne2\left( 5{x}^{3}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(5{x}^{4}\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## generated source-mask q-141101 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(\frac{5\left(\frac{y}{-3}\right)}{x}\right),\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=-3\left({x}^{5}\right)$
- $y=-3\left({x}^{10}\right)$
- $y=-3\left(5{x}^{4}\right)$

* II only
* I only **(correct)**
* III only
* None
* II and III only

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left({x}^{5}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(5{x}^{4}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{5\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( 5{x}^{4} \right)& \overset{?}{=}-3\left(\frac{5({x}^{5})}{x} \right)\\-3\left( 5{x}^{4} \right)& =-3\left(5{x}^{4}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left({x}^{5}\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left({x}^{10}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(10{x}^{9}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{5\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( 10{x}^{9} \right)& \overset{?}{=}-3\left(\frac{5({x}^{10})}{x} \right)\\-3\left( 10{x}^{9} \right)& \overset{?}{=}-3\left(5{x}^{9} \right)\\-3\left( 5{x}^{9} \right)& \ne 0.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left({x}^{10}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left(5{x}^{4}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(20{x}^{3}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{5\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( 20{x}^{3} \right)& \overset{?}{=}-3\left(\frac{5(5{x}^{4})}{x} \right)\\-3\left( 20{x}^{3} \right)& \overset{?}{=}-3\left(25{x}^{3} \right)\\ 0 & \ne-3\left( 5{x}^{3}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(5{x}^{4}\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## original q-141103 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=\frac{1}{{e}^{3y}}.
$$

 Which of the following is a solution to this equation?

- $y=\operatorname{ln}⁡x$
- $y=-\operatorname{ln}⁡x$
- $y=-2\operatorname{ln}⁡x$

* III only
* I and II only
* None **(correct)**
* II only
* I and III only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=\operatorname{ln}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=\frac{1}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{e}^{3y}} \\ \frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{3\operatorname{ln}⁡x}} \\ \frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{\operatorname{ln}⁡({x}^{3})}} \\ \frac{1}{x} & =\frac{1}{{x}^{3}} \\ {x}^{2} & =1.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=\operatorname{ln}⁡x$ is *not* a solution to our differential equation.

- Differentiating $y=-\operatorname{ln}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=-\frac{1}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{e}^{3y}} \\ -\frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{3(-\operatorname{ln}⁡x)}} \\ -\frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{-3\operatorname{ln}⁡x}} \\ -\frac{1}{x} & \overset{?}{=}\frac{1}{{e}^{\operatorname{ln}⁡({x}^{-3})}} \\ -\frac{1}{x} & \overset{?}{=}\frac{1}{{x}^{-3}} \\ -\frac{1}{x} & ={x}^{3} \\ -1 & ={x}^{4}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-\operatorname{ln}⁡x$ is *not* a solution to our differential equation.

- Differentiating $y=-2\operatorname{ln}⁡x,$ we get $\frac{\text{d}y}{\text{d}x}=-\frac{2}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{e}^{3y}} \\ -\frac{2}{x} & \overset{?}{=}\frac{1}{{e}^{3(-2\operatorname{ln}⁡x)}} \\ -\frac{2}{x} & \overset{?}{=}\frac{1}{{e}^{-6\operatorname{ln}⁡x}} \\ -\frac{2}{x} & \overset{?}{=}\frac{1}{{e}^{\operatorname{ln}⁡({x}^{-6})}} \\ -\frac{2}{x} & \overset{?}{=}\frac{1}{{x}^{-6}} \\ -\frac{2}{x} & ={x}^{6} \\ -2 & ={x}^{7}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-2\operatorname{ln}⁡x$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## generated source-mask q-141103 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(\frac{1}{{e}^{3\left(\frac{y}{2}\right)}}\right).
$$

 Which of the following is a solution to this equation?

- $y=2\left(\operatorname{ln}⁡x\right)$
- $y=2\left(-\operatorname{ln}⁡x\right)$
- $y=2\left(-2\operatorname{ln}⁡x\right)$

* I and II only
* I and III only
* III only
* None **(correct)**
* II only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(\frac{1}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{1}{{e}^{3\left(\frac{y}{2}\right)}} \right)\\2\left( \frac{1}{x} \right)& \overset{?}{=}2\left(\frac{1}{{e}^{3\operatorname{ln}⁡x}} \right)\\2\left( \frac{1}{x} \right)& \overset{?}{=}2\left(\frac{1}{{e}^{\operatorname{ln}⁡({x}^{3})}} \right)\\2\left( \frac{1}{x} \right)& =2\left(\frac{1}{{x}^{3}} \right)\\2\left( {x}^{2} \right)& =2\left(1\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left(-\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-\frac{1}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{1}{{e}^{3\left(\frac{y}{2}\right)}} \right)\\2\left( -\frac{1}{x} \right)& \overset{?}{=}2\left(\frac{1}{{e}^{3(-\operatorname{ln}⁡x)}} \right)\\2\left( -\frac{1}{x} \right)& \overset{?}{=}2\left(\frac{1}{{e}^{-3\operatorname{ln}⁡x}} \right)\\2\left( -\frac{1}{x} \right)& \overset{?}{=}2\left(\frac{1}{{e}^{\operatorname{ln}⁡({x}^{-3})}} \right)\\2\left( -\frac{1}{x} \right)& \overset{?}{=}2\left(\frac{1}{{x}^{-3}} \right)\\2\left( -\frac{1}{x} \right)& =2\left({x}^{3} \right)\\2\left( -1 \right)& =2\left({x}^{4}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(-\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left(-2\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-\frac{2}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(\frac{1}{{e}^{3\left(\frac{y}{2}\right)}} \right)\\2\left( -\frac{2}{x} \right)& \overset{?}{=}2\left(\frac{1}{{e}^{3(-2\operatorname{ln}⁡x)}} \right)\\2\left( -\frac{2}{x} \right)& \overset{?}{=}2\left(\frac{1}{{e}^{-6\operatorname{ln}⁡x}} \right)\\2\left( -\frac{2}{x} \right)& \overset{?}{=}2\left(\frac{1}{{e}^{\operatorname{ln}⁡({x}^{-6})}} \right)\\2\left( -\frac{2}{x} \right)& \overset{?}{=}2\left(\frac{1}{{x}^{-6}} \right)\\2\left( -\frac{2}{x} \right)& =2\left({x}^{6} \right)\\2\left( -2 \right)& =2\left({x}^{7}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(-2\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## generated source-mask q-141103 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(\frac{1}{{e}^{3\left(\frac{y}{-3}\right)}}\right).
$$

 Which of the following is a solution to this equation?

- $y=-3\left(\operatorname{ln}⁡x\right)$
- $y=-3\left(-\operatorname{ln}⁡x\right)$
- $y=-3\left(-2\operatorname{ln}⁡x\right)$

* I and II only
* I and III only
* III only
* None **(correct)**
* II only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(\frac{1}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{1}{{e}^{3\left(\frac{y}{-3}\right)}} \right)\\-3\left( \frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{e}^{3\operatorname{ln}⁡x}} \right)\\-3\left( \frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{e}^{\operatorname{ln}⁡({x}^{3})}} \right)\\-3\left( \frac{1}{x} \right)& =-3\left(\frac{1}{{x}^{3}} \right)\\-3\left( {x}^{2} \right)& =-3\left(1\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left(-\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-\frac{1}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{1}{{e}^{3\left(\frac{y}{-3}\right)}} \right)\\-3\left( -\frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{e}^{3(-\operatorname{ln}⁡x)}} \right)\\-3\left( -\frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{e}^{-3\operatorname{ln}⁡x}} \right)\\-3\left( -\frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{e}^{\operatorname{ln}⁡({x}^{-3})}} \right)\\-3\left( -\frac{1}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{x}^{-3}} \right)\\-3\left( -\frac{1}{x} \right)& =-3\left({x}^{3} \right)\\-3\left( -1 \right)& =-3\left({x}^{4}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(-\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left(-2\operatorname{ln}⁡x\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-\frac{2}{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(\frac{1}{{e}^{3\left(\frac{y}{-3}\right)}} \right)\\-3\left( -\frac{2}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{e}^{3(-2\operatorname{ln}⁡x)}} \right)\\-3\left( -\frac{2}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{e}^{-6\operatorname{ln}⁡x}} \right)\\-3\left( -\frac{2}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{e}^{\operatorname{ln}⁡({x}^{-6})}} \right)\\-3\left( -\frac{2}{x} \right)& \overset{?}{=}-3\left(\frac{1}{{x}^{-6}} \right)\\-3\left( -\frac{2}{x} \right)& =-3\left({x}^{6} \right)\\-3\left( -2 \right)& =-3\left({x}^{7}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(-2\operatorname{ln}⁡x\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## original q-79330 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=4y.
$$

 Which of the following is a solution to this equation?

- $y={e}^{-4x}$
- $y={e}^{4x}$
- $y=4{e}^{x}$

* I only
* II only **(correct)**
* III only
* I and III only
* II and III only

**Correct answer:** II only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y={e}^{-4x},$ we get $\frac{\text{d}y}{\text{d}x}=-4{e}^{-4x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4y \\ -4{e}^{-4x} & \overset{?}{=}4{e}^{-4x} \\ 0 & \ne 8{e}^{-4x}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y={e}^{-4x}$ is *not* a solution to our differential equation.

- Differentiating $y={e}^{4x},$ we get $\frac{\text{d}y}{\text{d}x}=4{e}^{4x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4y \\ 4{e}^{4x} & =4{e}^{4x}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y={e}^{4x}$ *is* a solution to our differential equation.

- Differentiating $y=4{e}^{x},$ we get $\frac{\text{d}y}{\text{d}x}=4{e}^{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4y \\ 4{e}^{x} & \overset{?}{=}4(4{e}^{x}) \\ 4{e}^{x} & \overset{?}{=}16{e}^{x} \\ 0 & \ne 12{e}^{x}.\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=4{e}^{x}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "II only."

## generated source-mask q-79330 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(4\left(\frac{y}{2}\right)\right).
$$

 Which of the following is a solution to this equation?

- $y=2\left({e}^{-4x}\right)$
- $y=2\left({e}^{4x}\right)$
- $y=2\left(4{e}^{x}\right)$

* II only **(correct)**
* II and III only
* I only
* III only
* I and III only

**Correct answer:** II only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left({e}^{-4x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-4{e}^{-4x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(4\left(\frac{y}{2}\right) \right)\\2\left( -4{e}^{-4x} \right)& \overset{?}{=}2\left(4{e}^{-4x} \right)\\ 0 & \ne2\left( 8{e}^{-4x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left({e}^{-4x}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=2\left({e}^{4x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(4{e}^{4x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(4\left(\frac{y}{2}\right) \right)\\2\left( 4{e}^{4x} \right)& =2\left(4{e}^{4x}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left({e}^{4x}\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(4{e}^{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(4{e}^{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(4\left(\frac{y}{2}\right) \right)\\2\left( 4{e}^{x} \right)& \overset{?}{=}2\left(4(4{e}^{x}) \right)\\2\left( 4{e}^{x} \right)& \overset{?}{=}2\left(16{e}^{x} \right)\\ 0 & \ne2\left( 12{e}^{x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2\left(4{e}^{x}\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "II only."

## generated source-mask q-79330 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(4\left(\frac{y}{-3}\right)\right).
$$

 Which of the following is a solution to this equation?

- $y=-3\left({e}^{-4x}\right)$
- $y=-3\left({e}^{4x}\right)$
- $y=-3\left(4{e}^{x}\right)$

* II only **(correct)**
* II and III only
* I only
* III only
* I and III only

**Correct answer:** II only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left({e}^{-4x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-4{e}^{-4x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(4\left(\frac{y}{-3}\right) \right)\\-3\left( -4{e}^{-4x} \right)& \overset{?}{=}-3\left(4{e}^{-4x} \right)\\ 0 & \ne-3\left( 8{e}^{-4x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left({e}^{-4x}\right)$ is *not* a solution to our differential equation.

- Differentiating $y=-3\left({e}^{4x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(4{e}^{4x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(4\left(\frac{y}{-3}\right) \right)\\-3\left( 4{e}^{4x} \right)& =-3\left(4{e}^{4x}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left({e}^{4x}\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(4{e}^{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(4{e}^{x}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(4\left(\frac{y}{-3}\right) \right)\\-3\left( 4{e}^{x} \right)& \overset{?}{=}-3\left(4(4{e}^{x}) \right)\\-3\left( 4{e}^{x} \right)& \overset{?}{=}-3\left(16{e}^{x} \right)\\ 0 & \ne-3\left( 12{e}^{x}\right).\,\times \end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-3\left(4{e}^{x}\right)$ is *not* a solution to our differential equation.

Therefore, the correct answer is "II only."

## original q-79333 | Moderate (M) | Observed original; evidence only

**Difficulty and origin:** Moderate (M) | Observed original; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-\frac{y}{x},\,x\ne 0.
$$

Which of the following is a solution to this equation?

- $y=\frac{7}{x}$
- $y=-\frac{1}{x}$
- $y=\frac{2}{x}$

* II only
* I and II only
* III only
* I and III only
* I, II, and III **(correct)**

**Correct answer:** I, II, and III

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=\frac{7}{x},$ we get $\frac{\text{d}y}{\text{d}x}=-\frac{7}{{x}^{2}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{y}{x} \\ -\frac{7}{{x}^{2}} & \overset{?}{=}-\frac{(\frac{7}{x})}{x} \\ -\frac{7}{{x}^{2}} & =-\frac{7}{{x}^{2}}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=\frac{7}{x}$ *is* a solution to our differential equation.

- Differentiating $y=-\frac{1}{x},$ we get $\frac{\text{d}y}{\text{d}x}=\frac{1}{{x}^{2}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{y}{x} \\ \frac{1}{{x}^{2}} & \overset{?}{=}-\frac{(-\frac{1}{x})}{x} \\ \frac{1}{{x}^{2}} & =\frac{1}{{x}^{2}}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-\frac{1}{x}$ *is* a solution to our differential equation.

- Differentiating $y=\frac{2}{x},$ we get $\frac{\text{d}y}{\text{d}x}=-\frac{2}{{x}^{2}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{y}{x} \\ -\frac{2}{{x}^{2}} & \overset{?}{=}-\frac{(\frac{2}{x})}{x} \\ -\frac{2}{{x}^{2}} & =-\frac{2}{{x}^{2}}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=\frac{2}{x}$ *is* a solution to our differential equation.

Therefore, the correct answer is "I, II, and III."

## generated source-mask q-79333 scale=2 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=2\left(-\frac{\left(\frac{y}{2}\right)}{x}\right),\,x\ne 0.
$$

Which of the following is a solution to this equation?

- $y=2\left(\frac{7}{x}\right)$
- $y=2\left(-\frac{1}{x}\right)$
- $y=2\left(\frac{2}{x}\right)$

* I and II only
* I, II, and III **(correct)**
* II only
* III only
* I and III only

**Correct answer:** I, II, and III

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2\left(\frac{7}{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-\frac{7}{{x}^{2}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\frac{\left(\frac{y}{2}\right)}{x} \right)\\2\left( -\frac{7}{{x}^{2}} \right)& \overset{?}{=}2\left(-\frac{(\frac{7}{x})}{x} \right)\\2\left( -\frac{7}{{x}^{2}} \right)& =2\left(-\frac{7}{{x}^{2}}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(\frac{7}{x}\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(-\frac{1}{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(\frac{1}{{x}^{2}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\frac{\left(\frac{y}{2}\right)}{x} \right)\\2\left( \frac{1}{{x}^{2}} \right)& \overset{?}{=}2\left(-\frac{(-\frac{1}{x})}{x} \right)\\2\left( \frac{1}{{x}^{2}} \right)& =2\left(\frac{1}{{x}^{2}}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(-\frac{1}{x}\right)$ *is* a solution to our differential equation.

- Differentiating $y=2\left(\frac{2}{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=2\left(-\frac{2}{{x}^{2}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2\left(-\frac{\left(\frac{y}{2}\right)}{x} \right)\\2\left( -\frac{2}{{x}^{2}} \right)& \overset{?}{=}2\left(-\frac{(\frac{2}{x})}{x} \right)\\2\left( -\frac{2}{{x}^{2}} \right)& =2\left(-\frac{2}{{x}^{2}}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2\left(\frac{2}{x}\right)$ *is* a solution to our differential equation.

Therefore, the correct answer is "I, II, and III."

## generated source-mask q-79333 scale=-3 | Moderate (M) | Observed source mask variant; evidence only

**Difficulty and origin:** Moderate (M) | Observed source mask variant; evidence only

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-3\left(-\frac{\left(\frac{y}{-3}\right)}{x}\right),\,x\ne 0.
$$

Which of the following is a solution to this equation?

- $y=-3\left(\frac{7}{x}\right)$
- $y=-3\left(-\frac{1}{x}\right)$
- $y=-3\left(\frac{2}{x}\right)$

* I and II only
* I, II, and III **(correct)**
* II only
* III only
* I and III only

**Correct answer:** I, II, and III

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-3\left(\frac{7}{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-\frac{7}{{x}^{2}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\frac{\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( -\frac{7}{{x}^{2}} \right)& \overset{?}{=}-3\left(-\frac{(\frac{7}{x})}{x} \right)\\-3\left( -\frac{7}{{x}^{2}} \right)& =-3\left(-\frac{7}{{x}^{2}}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(\frac{7}{x}\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(-\frac{1}{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(\frac{1}{{x}^{2}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\frac{\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( \frac{1}{{x}^{2}} \right)& \overset{?}{=}-3\left(-\frac{(-\frac{1}{x})}{x} \right)\\-3\left( \frac{1}{{x}^{2}} \right)& =-3\left(\frac{1}{{x}^{2}}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(-\frac{1}{x}\right)$ *is* a solution to our differential equation.

- Differentiating $y=-3\left(\frac{2}{x}\right),$ we get $\frac{\text{d}y}{\text{d}x}=-3\left(-\frac{2}{{x}^{2}}\right).$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-3\left(-\frac{\left(\frac{y}{-3}\right)}{x} \right)\\-3\left( -\frac{2}{{x}^{2}} \right)& \overset{?}{=}-3\left(-\frac{(\frac{2}{x})}{x} \right)\\-3\left( -\frac{2}{{x}^{2}} \right)& =-3\left(-\frac{2}{{x}^{2}}\right).\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=-3\left(\frac{2}{x}\right)$ *is* a solution to our differential equation.

Therefore, the correct answer is "I, II, and III."

## authored easy exp seed=0 | Easy (E) | Authored missing level extension

**Difficulty and origin:** Easy (E) | Authored missing level extension

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=y.
$$

 Which of the following is a solution to this equation?

- $y=e^{- x}$
- $y=2 e^{x}$
- $y=- e^{x}$

* II only
* II and III only **(correct)**
* I only
* I and III only
* III only

**Correct answer:** II and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=e^{- x},$ we get $\frac{\text{d}y}{\text{d}x}=- e^{- x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ - e^{- x} & \overset{?}{=}1\cdot \left(e^{- x}\right) \\ - e^{- x} & \overset{?}{=}e^{- x} \\ - 2 e^{- x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=e^{- x}$ is *not* a solution to our differential equation.

- Differentiating $y=2 e^{x},$ we get $\frac{\text{d}y}{\text{d}x}=2 e^{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ 2 e^{x} & \overset{?}{=}1\cdot \left(2 e^{x}\right) \\ 2 e^{x} & =2 e^{x}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2 e^{x}$ *is* a solution to our differential equation.

- Differentiating $y=- e^{x},$ we get $\frac{\text{d}y}{\text{d}x}=- e^{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ - e^{x} & \overset{?}{=}1\cdot \left(- e^{x}\right) \\ - e^{x} & =- e^{x}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=- e^{x}$ *is* a solution to our differential equation.

Therefore, the correct answer is "II and III only."

## authored easy exp seed=1 | Easy (E) | Authored missing level extension

**Difficulty and origin:** Easy (E) | Authored missing level extension

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=- y.
$$

 Which of the following is a solution to this equation?

- $y=2 e^{- x}$
- $y=2 - 3 e^{x}$
- $y=e^{x} + 1$

* I and III only
* None
* I only **(correct)**
* I, II, and III
* II and III only

**Correct answer:** I only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=2 e^{- x},$ we get $\frac{\text{d}y}{\text{d}x}=- 2 e^{- x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- y \\ - 2 e^{- x} & \overset{?}{=}-1\cdot \left(2 e^{- x}\right) \\ - 2 e^{- x} & =- 2 e^{- x}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=2 e^{- x}$ *is* a solution to our differential equation.

- Differentiating $y=2 - 3 e^{x},$ we get $\frac{\text{d}y}{\text{d}x}=- 3 e^{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- y \\ - 3 e^{x} & \overset{?}{=}-1\cdot \left(2 - 3 e^{x}\right) \\ - 3 e^{x} & \overset{?}{=}3 e^{x} - 2 \\ 2 - 6 e^{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2 - 3 e^{x}$ is *not* a solution to our differential equation.

- Differentiating $y=e^{x} + 1,$ we get $\frac{\text{d}y}{\text{d}x}=e^{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- y \\ e^{x} & \overset{?}{=}-1\cdot \left(e^{x} + 1\right) \\ e^{x} & \overset{?}{=}- e^{x} - 1 \\ 2 e^{x} + 1 & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=e^{x} + 1$ is *not* a solution to our differential equation.

Therefore, the correct answer is "I only."

## authored moderate exp seed=0 | Moderate (M) | Authored same method variant

**Difficulty and origin:** Moderate (M) | Authored same method variant

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=4 y.
$$

 Which of the following is a solution to this equation?

- $y=- 4 e^{5 x}$
- $y=3 e^{5 x} + 2$
- $y=4 e^{3 x}$

* III only
* None **(correct)**
* I and II only
* II and III only
* I, II, and III

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=- 4 e^{5 x},$ we get $\frac{\text{d}y}{\text{d}x}=- 20 e^{5 x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 y \\ - 20 e^{5 x} & \overset{?}{=}4\cdot \left(- 4 e^{5 x}\right) \\ - 20 e^{5 x} & \overset{?}{=}- 16 e^{5 x} \\ - 4 e^{5 x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=- 4 e^{5 x}$ is *not* a solution to our differential equation.

- Differentiating $y=3 e^{5 x} + 2,$ we get $\frac{\text{d}y}{\text{d}x}=15 e^{5 x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 y \\ 15 e^{5 x} & \overset{?}{=}4\cdot \left(3 e^{5 x} + 2\right) \\ 15 e^{5 x} & \overset{?}{=}12 e^{5 x} + 8 \\ 3 e^{5 x} - 8 & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=3 e^{5 x} + 2$ is *not* a solution to our differential equation.

- Differentiating $y=4 e^{3 x},$ we get $\frac{\text{d}y}{\text{d}x}=12 e^{3 x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 y \\ 12 e^{3 x} & \overset{?}{=}4\cdot \left(4 e^{3 x}\right) \\ 12 e^{3 x} & \overset{?}{=}16 e^{3 x} \\ - 4 e^{3 x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=4 e^{3 x}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## authored moderate exp seed=1 | Moderate (M) | Authored same method variant

**Difficulty and origin:** Moderate (M) | Authored same method variant

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=- 3 y.
$$

 Which of the following is a solution to this equation?

- $y=-2 + e^{- 3 x}$
- $y=4 e^{- 2 x}$
- $y=-2 - e^{- 2 x}$

* III only
* I, II, and III
* I only
* None **(correct)**
* I and III only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-2 + e^{- 3 x},$ we get $\frac{\text{d}y}{\text{d}x}=- 3 e^{- 3 x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 3 y \\ - 3 e^{- 3 x} & \overset{?}{=}-3\cdot \left(-2 + e^{- 3 x}\right) \\ - 3 e^{- 3 x} & \overset{?}{=}6 - 3 e^{- 3 x} \\ -6 & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-2 + e^{- 3 x}$ is *not* a solution to our differential equation.

- Differentiating $y=4 e^{- 2 x},$ we get $\frac{\text{d}y}{\text{d}x}=- 8 e^{- 2 x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 3 y \\ - 8 e^{- 2 x} & \overset{?}{=}-3\cdot \left(4 e^{- 2 x}\right) \\ - 8 e^{- 2 x} & \overset{?}{=}- 12 e^{- 2 x} \\ 4 e^{- 2 x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=4 e^{- 2 x}$ is *not* a solution to our differential equation.

- Differentiating $y=-2 - e^{- 2 x},$ we get $\frac{\text{d}y}{\text{d}x}=2 e^{- 2 x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 3 y \\ 2 e^{- 2 x} & \overset{?}{=}-3\cdot \left(-2 - e^{- 2 x}\right) \\ 2 e^{- 2 x} & \overset{?}{=}6 + 3 e^{- 2 x} \\ -6 - e^{- 2 x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-2 - e^{- 2 x}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## authored moderate power seed=0 | Moderate (M) | Authored same method variant

**Difficulty and origin:** Moderate (M) | Authored same method variant

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=\frac{4 y}{x},\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=- 4 x^{5}$
- $y=3 x^{5} + 2$
- $y=4 x^{3}$

* I, II, and III
* None **(correct)**
* I only
* III only
* II only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=- 4 x^{5},$ we get $\frac{\text{d}y}{\text{d}x}=- 20 x^{4}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4 y}{x} \\ - 20 x^{4} & \overset{?}{=}\frac{4\cdot \left(- 4 x^{5}\right)}{x} \\ - 20 x^{4} & \overset{?}{=}- 16 x^{4} \\ - 4 x^{4} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=- 4 x^{5}$ is *not* a solution to our differential equation.

- Differentiating $y=3 x^{5} + 2,$ we get $\frac{\text{d}y}{\text{d}x}=15 x^{4}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4 y}{x} \\ 15 x^{4} & \overset{?}{=}\frac{4\cdot \left(3 x^{5} + 2\right)}{x} \\ 15 x^{4} & \overset{?}{=}\frac{4 \left(3 x^{5} + 2\right)}{x} \\ \frac{3 x^{5} - 8}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=3 x^{5} + 2$ is *not* a solution to our differential equation.

- Differentiating $y=4 x^{3},$ we get $\frac{\text{d}y}{\text{d}x}=12 x^{2}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4 y}{x} \\ 12 x^{2} & \overset{?}{=}\frac{4\cdot \left(4 x^{3}\right)}{x} \\ 12 x^{2} & \overset{?}{=}16 x^{2} \\ - 4 x^{2} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=4 x^{3}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## authored moderate power seed=1 | Moderate (M) | Authored same method variant

**Difficulty and origin:** Moderate (M) | Authored same method variant

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=- \frac{3 y}{x},\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=-2 + \frac{1}{x^{3}}$
- $y=\frac{4}{x^{2}}$
- $y=-2 - \frac{1}{x^{2}}$

* II only
* I and II only
* I and III only
* None **(correct)**
* II and III only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=-2 + \frac{1}{x^{3}},$ we get $\frac{\text{d}y}{\text{d}x}=- \frac{3}{x^{4}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- \frac{3 y}{x} \\ - \frac{3}{x^{4}} & \overset{?}{=}\frac{-3\cdot \left(-2 + \frac{1}{x^{3}}\right)}{x} \\ - \frac{3}{x^{4}} & \overset{?}{=}\frac{6}{x} - \frac{3}{x^{4}} \\ - \frac{6}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-2 + \frac{1}{x^{3}}$ is *not* a solution to our differential equation.

- Differentiating $y=\frac{4}{x^{2}},$ we get $\frac{\text{d}y}{\text{d}x}=- \frac{8}{x^{3}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- \frac{3 y}{x} \\ - \frac{8}{x^{3}} & \overset{?}{=}\frac{-3\cdot \left(\frac{4}{x^{2}}\right)}{x} \\ - \frac{8}{x^{3}} & \overset{?}{=}- \frac{12}{x^{3}} \\ \frac{4}{x^{3}} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=\frac{4}{x^{2}}$ is *not* a solution to our differential equation.

- Differentiating $y=-2 - \frac{1}{x^{2}},$ we get $\frac{\text{d}y}{\text{d}x}=\frac{2}{x^{3}}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- \frac{3 y}{x} \\ \frac{2}{x^{3}} & \overset{?}{=}\frac{-3\cdot \left(-2 - \frac{1}{x^{2}}\right)}{x} \\ \frac{2}{x^{3}} & \overset{?}{=}\frac{6}{x} + \frac{3}{x^{3}} \\ - \frac{6}{x} - \frac{1}{x^{3}} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=-2 - \frac{1}{x^{2}}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## authored moderate sin seed=0 | Moderate (M) | Authored same method variant

**Difficulty and origin:** Moderate (M) | Authored same method variant

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=3 y \cot{\left(3 x \right)},\,\sin(3 x)\ne0.
$$

 Which of the following is a solution to this equation?

- $y=3 \sin{\left(3 x \right)} - 2$
- $y=\sin{\left(3 x \right)}$
- $y=4 \sin{\left(3 x \right)}$

* III only
* II and III only **(correct)**
* None
* II only
* I and III only

**Correct answer:** II and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=3 \sin{\left(3 x \right)} - 2,$ we get $\frac{\text{d}y}{\text{d}x}=9 \cos{\left(3 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3 y \cot{\left(3 x \right)} \\ 9 \cos{\left(3 x \right)} & \overset{?}{=}3\cdot \left(3 \sin{\left(3 x \right)} - 2\right)\cot\left(3 x\right) \\ 9 \cos{\left(3 x \right)} & \overset{?}{=}3 \left(3 \sin{\left(3 x \right)} - 2\right) \cot{\left(3 x \right)} \\ \frac{6}{\tan{\left(3 x \right)}} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=3 \sin{\left(3 x \right)} - 2$ is *not* a solution to our differential equation.

- Differentiating $y=\sin{\left(3 x \right)},$ we get $\frac{\text{d}y}{\text{d}x}=3 \cos{\left(3 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3 y \cot{\left(3 x \right)} \\ 3 \cos{\left(3 x \right)} & \overset{?}{=}3\cdot \left(\sin{\left(3 x \right)}\right)\cot\left(3 x\right) \\ 3 \cos{\left(3 x \right)} & =3 \cos{\left(3 x \right)}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=\sin{\left(3 x \right)}$ *is* a solution to our differential equation.

- Differentiating $y=4 \sin{\left(3 x \right)},$ we get $\frac{\text{d}y}{\text{d}x}=12 \cos{\left(3 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3 y \cot{\left(3 x \right)} \\ 12 \cos{\left(3 x \right)} & \overset{?}{=}3\cdot \left(4 \sin{\left(3 x \right)}\right)\cot\left(3 x\right) \\ 12 \cos{\left(3 x \right)} & =12 \cos{\left(3 x \right)}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=4 \sin{\left(3 x \right)}$ *is* a solution to our differential equation.

Therefore, the correct answer is "II and III only."

## authored moderate sin seed=1 | Moderate (M) | Authored same method variant

**Difficulty and origin:** Moderate (M) | Authored same method variant

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=4 y \cot{\left(4 x \right)},\,\sin(4 x)\ne0.
$$

 Which of the following is a solution to this equation?

- $y=3 \sin{\left(4 x \right)} + 2$
- $y=- \sin{\left(4 x \right)} - 2$
- $y=4 \sin{\left(4 x \right)} - 2$

* II only
* None **(correct)**
* III only
* I only
* I, II, and III

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=3 \sin{\left(4 x \right)} + 2,$ we get $\frac{\text{d}y}{\text{d}x}=12 \cos{\left(4 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 y \cot{\left(4 x \right)} \\ 12 \cos{\left(4 x \right)} & \overset{?}{=}4\cdot \left(3 \sin{\left(4 x \right)} + 2\right)\cot\left(4 x\right) \\ 12 \cos{\left(4 x \right)} & \overset{?}{=}4 \left(3 \sin{\left(4 x \right)} + 2\right) \cot{\left(4 x \right)} \\ - \frac{8}{\tan{\left(4 x \right)}} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=3 \sin{\left(4 x \right)} + 2$ is *not* a solution to our differential equation.

- Differentiating $y=- \sin{\left(4 x \right)} - 2,$ we get $\frac{\text{d}y}{\text{d}x}=- 4 \cos{\left(4 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 y \cot{\left(4 x \right)} \\ - 4 \cos{\left(4 x \right)} & \overset{?}{=}4\cdot \left(- \sin{\left(4 x \right)} - 2\right)\cot\left(4 x\right) \\ - 4 \cos{\left(4 x \right)} & \overset{?}{=}- 4 \left(\sin{\left(4 x \right)} + 2\right) \cot{\left(4 x \right)} \\ \frac{8}{\tan{\left(4 x \right)}} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=- \sin{\left(4 x \right)} - 2$ is *not* a solution to our differential equation.

- Differentiating $y=4 \sin{\left(4 x \right)} - 2,$ we get $\frac{\text{d}y}{\text{d}x}=16 \cos{\left(4 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 y \cot{\left(4 x \right)} \\ 16 \cos{\left(4 x \right)} & \overset{?}{=}4\cdot \left(4 \sin{\left(4 x \right)} - 2\right)\cot\left(4 x\right) \\ 16 \cos{\left(4 x \right)} & \overset{?}{=}8 \left(2 \sin{\left(4 x \right)} - 1\right) \cot{\left(4 x \right)} \\ \frac{8}{\tan{\left(4 x \right)}} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=4 \sin{\left(4 x \right)} - 2$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## authored moderate cos seed=0 | Moderate (M) | Authored same method variant

**Difficulty and origin:** Moderate (M) | Authored same method variant

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=- 3 y \tan{\left(3 x \right)},\,\cos(3 x)\ne0.
$$

 Which of the following is a solution to this equation?

- $y=3 \cos{\left(3 x \right)} - 2$
- $y=\cos{\left(3 x \right)}$
- $y=4 \cos{\left(3 x \right)}$

* I and III only
* II and III only **(correct)**
* III only
* II only
* I, II, and III

**Correct answer:** II and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=3 \cos{\left(3 x \right)} - 2,$ we get $\frac{\text{d}y}{\text{d}x}=- 9 \sin{\left(3 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 3 y \tan{\left(3 x \right)} \\ - 9 \sin{\left(3 x \right)} & \overset{?}{=}-3\cdot \left(3 \cos{\left(3 x \right)} - 2\right)\tan\left(3 x\right) \\ - 9 \sin{\left(3 x \right)} & \overset{?}{=}3 \left(2 - 3 \cos{\left(3 x \right)}\right) \tan{\left(3 x \right)} \\ - 6 \tan{\left(3 x \right)} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=3 \cos{\left(3 x \right)} - 2$ is *not* a solution to our differential equation.

- Differentiating $y=\cos{\left(3 x \right)},$ we get $\frac{\text{d}y}{\text{d}x}=- 3 \sin{\left(3 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 3 y \tan{\left(3 x \right)} \\ - 3 \sin{\left(3 x \right)} & \overset{?}{=}-3\cdot \left(\cos{\left(3 x \right)}\right)\tan\left(3 x\right) \\ - 3 \sin{\left(3 x \right)} & =- 3 \sin{\left(3 x \right)}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=\cos{\left(3 x \right)}$ *is* a solution to our differential equation.

- Differentiating $y=4 \cos{\left(3 x \right)},$ we get $\frac{\text{d}y}{\text{d}x}=- 12 \sin{\left(3 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 3 y \tan{\left(3 x \right)} \\ - 12 \sin{\left(3 x \right)} & \overset{?}{=}-3\cdot \left(4 \cos{\left(3 x \right)}\right)\tan\left(3 x\right) \\ - 12 \sin{\left(3 x \right)} & =- 12 \sin{\left(3 x \right)}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=4 \cos{\left(3 x \right)}$ *is* a solution to our differential equation.

Therefore, the correct answer is "II and III only."

## authored moderate cos seed=1 | Moderate (M) | Authored same method variant

**Difficulty and origin:** Moderate (M) | Authored same method variant

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=- 4 y \tan{\left(4 x \right)},\,\cos(4 x)\ne0.
$$

 Which of the following is a solution to this equation?

- $y=3 \cos{\left(4 x \right)} + 2$
- $y=- \cos{\left(4 x \right)} - 2$
- $y=4 \cos{\left(4 x \right)} - 2$

* II only
* None **(correct)**
* I and III only
* III only
* I only

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=3 \cos{\left(4 x \right)} + 2,$ we get $\frac{\text{d}y}{\text{d}x}=- 12 \sin{\left(4 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 4 y \tan{\left(4 x \right)} \\ - 12 \sin{\left(4 x \right)} & \overset{?}{=}-4\cdot \left(3 \cos{\left(4 x \right)} + 2\right)\tan\left(4 x\right) \\ - 12 \sin{\left(4 x \right)} & \overset{?}{=}- 4 \left(3 \cos{\left(4 x \right)} + 2\right) \tan{\left(4 x \right)} \\ 8 \tan{\left(4 x \right)} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=3 \cos{\left(4 x \right)} + 2$ is *not* a solution to our differential equation.

- Differentiating $y=- \cos{\left(4 x \right)} - 2,$ we get $\frac{\text{d}y}{\text{d}x}=4 \sin{\left(4 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 4 y \tan{\left(4 x \right)} \\ 4 \sin{\left(4 x \right)} & \overset{?}{=}-4\cdot \left(- \cos{\left(4 x \right)} - 2\right)\tan\left(4 x\right) \\ 4 \sin{\left(4 x \right)} & \overset{?}{=}4 \left(\cos{\left(4 x \right)} + 2\right) \tan{\left(4 x \right)} \\ - 8 \tan{\left(4 x \right)} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=- \cos{\left(4 x \right)} - 2$ is *not* a solution to our differential equation.

- Differentiating $y=4 \cos{\left(4 x \right)} - 2,$ we get $\frac{\text{d}y}{\text{d}x}=- 16 \sin{\left(4 x \right)}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =- 4 y \tan{\left(4 x \right)} \\ - 16 \sin{\left(4 x \right)} & \overset{?}{=}-4\cdot \left(4 \cos{\left(4 x \right)} - 2\right)\tan\left(4 x\right) \\ - 16 \sin{\left(4 x \right)} & \overset{?}{=}- 16 \sin{\left(4 x \right)} + 8 \tan{\left(4 x \right)} \\ - 8 \tan{\left(4 x \right)} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=4 \cos{\left(4 x \right)} - 2$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## authored hard log seed=0 | Hard (H) | Authored missing level extension

**Difficulty and origin:** Hard (H) | Authored missing level extension

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=3 e^{- \frac{y}{3}},\,x>0.
$$

 Which of the following is a solution to this equation?

- $y=- 3 \ln{\left(x \right)} - 1$
- $y=2 \ln{\left(x \right)} + 1$
- $y=- 3 \ln{\left(x \right)}$

* II only
* None **(correct)**
* III only
* I and II only
* I, II, and III

**Correct answer:** None

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=- 3 \ln{\left(x \right)} - 1,$ we get $\frac{\text{d}y}{\text{d}x}=- \frac{3}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3 e^{- \frac{y}{3}} \\ - \frac{3}{x} & \overset{?}{=}3e^{-\frac{1}{3}\cdot \left(- 3 \ln{\left(x \right)} - 1\right)} \\ - \frac{3}{x} & \overset{?}{=}3e^{\frac{1}{3}}\cdot e^{\ln\left(x\right)} \\ - \frac{3}{x} & \overset{?}{=}3 x e^{\frac{1}{3}} \\ - 3 x e^{\frac{1}{3}} - \frac{3}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=- 3 \ln{\left(x \right)} - 1$ is *not* a solution to our differential equation.

- Differentiating $y=2 \ln{\left(x \right)} + 1,$ we get $\frac{\text{d}y}{\text{d}x}=\frac{2}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3 e^{- \frac{y}{3}} \\ \frac{2}{x} & \overset{?}{=}3e^{-\frac{1}{3}\cdot \left(2 \ln{\left(x \right)} + 1\right)} \\ \frac{2}{x} & \overset{?}{=}3e^{- \frac{1}{3}}\cdot e^{\ln\left(\frac{1}{x^{\frac{2}{3}}}\right)} \\ \frac{2}{x} & \overset{?}{=}\frac{3}{x^{\frac{2}{3}} e^{\frac{1}{3}}} \\ \frac{2}{x} - \frac{3}{x^{\frac{2}{3}} e^{\frac{1}{3}}} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=2 \ln{\left(x \right)} + 1$ is *not* a solution to our differential equation.

- Differentiating $y=- 3 \ln{\left(x \right)},$ we get $\frac{\text{d}y}{\text{d}x}=- \frac{3}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3 e^{- \frac{y}{3}} \\ - \frac{3}{x} & \overset{?}{=}3e^{-\frac{1}{3}\cdot \left(- 3 \ln{\left(x \right)}\right)} \\ - \frac{3}{x} & \overset{?}{=}3e^{0}\cdot e^{\ln\left(x\right)} \\ - \frac{3}{x} & \overset{?}{=}3 x \\ - 3 x - \frac{3}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=- 3 \ln{\left(x \right)}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "None."

## authored hard log seed=1 | Hard (H) | Authored missing level extension

**Difficulty and origin:** Hard (H) | Authored missing level extension

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=4 e^{- \frac{y}{4}},\,x>0.
$$

 Which of the following is a solution to this equation?

- $y=4 \ln{\left(x \right)} + 1$
- $y=4 \ln{\left(x \right)}$
- $y=1 - 4 \ln{\left(x \right)}$

* I and III only
* I, II, and III
* II only **(correct)**
* III only
* II and III only

**Correct answer:** II only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=4 \ln{\left(x \right)} + 1,$ we get $\frac{\text{d}y}{\text{d}x}=\frac{4}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 e^{- \frac{y}{4}} \\ \frac{4}{x} & \overset{?}{=}4e^{-\frac{1}{4}\cdot \left(4 \ln{\left(x \right)} + 1\right)} \\ \frac{4}{x} & \overset{?}{=}4e^{- \frac{1}{4}}\cdot e^{\ln\left(\frac{1}{x}\right)} \\ \frac{4}{x} & \overset{?}{=}\frac{4}{x e^{\frac{1}{4}}} \\ - \frac{4}{x e^{\frac{1}{4}}} + \frac{4}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=4 \ln{\left(x \right)} + 1$ is *not* a solution to our differential equation.

- Differentiating $y=4 \ln{\left(x \right)},$ we get $\frac{\text{d}y}{\text{d}x}=\frac{4}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 e^{- \frac{y}{4}} \\ \frac{4}{x} & \overset{?}{=}4e^{-\frac{1}{4}\cdot \left(4 \ln{\left(x \right)}\right)} \\ \frac{4}{x} & \overset{?}{=}4e^{0}\cdot e^{\ln\left(\frac{1}{x}\right)} \\ \frac{4}{x} & =\frac{4}{x}.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=4 \ln{\left(x \right)}$ *is* a solution to our differential equation.

- Differentiating $y=1 - 4 \ln{\left(x \right)},$ we get $\frac{\text{d}y}{\text{d}x}=- \frac{4}{x}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4 e^{- \frac{y}{4}} \\ - \frac{4}{x} & \overset{?}{=}4e^{-\frac{1}{4}\cdot \left(1 - 4 \ln{\left(x \right)}\right)} \\ - \frac{4}{x} & \overset{?}{=}4e^{- \frac{1}{4}}\cdot e^{\ln\left(x\right)} \\ - \frac{4}{x} & \overset{?}{=}\frac{4 x}{e^{\frac{1}{4}}} \\ - \frac{4 x}{e^{\frac{1}{4}}} - \frac{4}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=1 - 4 \ln{\left(x \right)}$ is *not* a solution to our differential equation.

Therefore, the correct answer is "II only."

## authored hard affine seed=0 | Hard (H) | Authored missing level extension

**Difficulty and origin:** Hard (H) | Authored missing level extension

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-2 + \frac{3 y}{x},\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=- 3 x^{3} + x + 1$
- $y=x^{3} + x$
- $y=x^{3} + x + 1$

* I only
* II only **(correct)**
* III only
* None
* I and II only

**Correct answer:** II only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=- 3 x^{3} + x + 1,$ we get $\frac{\text{d}y}{\text{d}x}=1 - 9 x^{2}.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2 + \frac{3 y}{x} \\ 1 - 9 x^{2} & \overset{?}{=}\frac{3\cdot \left(- 3 x^{3} + x + 1\right)}{x}-2 \\ 1 - 9 x^{2} & \overset{?}{=}\frac{- 9 x^{3} + x + 3}{x} \\ - \frac{3}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=- 3 x^{3} + x + 1$ is *not* a solution to our differential equation.

- Differentiating $y=x^{3} + x,$ we get $\frac{\text{d}y}{\text{d}x}=3 x^{2} + 1.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2 + \frac{3 y}{x} \\ 3 x^{2} + 1 & \overset{?}{=}\frac{3\cdot \left(x^{3} + x\right)}{x}-2 \\ 3 x^{2} + 1 & =3 x^{2} + 1.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=x^{3} + x$ *is* a solution to our differential equation.

- Differentiating $y=x^{3} + x + 1,$ we get $\frac{\text{d}y}{\text{d}x}=3 x^{2} + 1.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2 + \frac{3 y}{x} \\ 3 x^{2} + 1 & \overset{?}{=}\frac{3\cdot \left(x^{3} + x + 1\right)}{x}-2 \\ 3 x^{2} + 1 & \overset{?}{=}\frac{3 x^{3} + x + 3}{x} \\ - \frac{3}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=x^{3} + x + 1$ is *not* a solution to our differential equation.

Therefore, the correct answer is "II only."

## authored hard affine seed=1 | Hard (H) | Authored missing level extension

**Difficulty and origin:** Hard (H) | Authored missing level extension

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}=-2 + \frac{2 y}{x},\,x\ne 0.
$$

 Which of the following is a solution to this equation?

- $y=- 3 x^{2} + 2 x - 1$
- $y=x^{2} + 2 x$
- $y=3 x^{2} + 2 x$

* III only
* I, II, and III
* I only
* II only
* II and III only **(correct)**

**Correct answer:** II and III only

For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the stated domain.

We check each proposed solution by differentiating and substituting it into the original equation. 

- Differentiating $y=- 3 x^{2} + 2 x - 1,$ we get $\frac{\text{d}y}{\text{d}x}=2 - 6 x.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2 + \frac{2 y}{x} \\ 2 - 6 x & \overset{?}{=}\frac{2\cdot \left(- 3 x^{2} + 2 x - 1\right)}{x}-2 \\ 2 - 6 x & \overset{?}{=}- 6 x + 2 - \frac{2}{x} \\ \frac{2}{x} & \not\equiv 0\end{aligned}
$$

This statement is *not true* for all $x.$ Therefore, the function $y=- 3 x^{2} + 2 x - 1$ is *not* a solution to our differential equation.

- Differentiating $y=x^{2} + 2 x,$ we get $\frac{\text{d}y}{\text{d}x}=2 x + 2.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2 + \frac{2 y}{x} \\ 2 x + 2 & \overset{?}{=}\frac{2\cdot \left(x^{2} + 2 x\right)}{x}-2 \\ 2 x + 2 & =2 x + 2.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=x^{2} + 2 x$ *is* a solution to our differential equation.

- Differentiating $y=3 x^{2} + 2 x,$ we get $\frac{\text{d}y}{\text{d}x}=6 x + 2.$ Substituting into the original equation, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-2 + \frac{2 y}{x} \\ 6 x + 2 & \overset{?}{=}\frac{2\cdot \left(3 x^{2} + 2 x\right)}{x}-2 \\ 6 x + 2 & =6 x + 2.\,✓\end{aligned}
$$

This statement is *true*. Therefore, the function $y=3 x^{2} + 2 x$ *is* a solution to our differential equation.

Therefore, the correct answer is "II and III only."
