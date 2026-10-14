## Observed source replay (evidence only) | easy | q-96702 | observed_raw

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}-x={e}^{y}$
- **II.** $y\frac{\text{d}y}{\text{d}x}-2=\sqrt{y}$
- **III.** $4\frac{\text{d}y}{\text{d}x}-\frac{x}{y}=5y$

Author review: complete checkbox banks and correct lookup refs.

- I (checkbox): false [3895e729-4b80-55b7-b728-f7de84f1c7b4], true [fd142676-60c4-53bf-93ca-876ecefe996d]; correct=false; ref=[":answer/id", "3895e729-4b80-55b7-b728-f7de84f1c7b4"]
- II (checkbox): false [d7665952-8830-56bb-9fb3-f0a2abfb8595], true [ca730cba-f151-5d18-a266-5fdce78f213e]; correct=true; ref=[":answer/id", "ca730cba-f151-5d18-a266-5fdce78f213e"]
- III (checkbox): true [90b78f8e-41bb-5a86-8d23-8ee6c1ce8d4d], false [e38492cf-3257-541a-acba-1f16d6ec8417]; correct=false; ref=[":answer/id", "e38492cf-3257-541a-acba-1f16d6ec8417"]

Worked solution:

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{'}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-x & ={e}^{y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{y}+x \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)={e}^{y}+x.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}-2 & =\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =\frac{\sqrt{y}+2}{2} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{\sqrt{y}+2}{2}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}4\frac{\text{d}y}{\text{d}x}-\frac{x}{y} & =5y \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{4}(5y+\frac{x}{y}) \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{1}{4}(5y+\frac{x}{y}).$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "II only."

