## Observed source replay (evidence only) | easy | q-96702 | observed_raw

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}-x={e}^{y}$
- **II.** $y\frac{\text{d}y}{\text{d}x}-2=\sqrt{y}$
- **III.** $4\frac{\text{d}y}{\text{d}x}-\frac{x}{y}=5y$

Author review: complete checkbox banks and correct lookup refs.

- I (checkbox): false [3cfe98d0-c506-5dc0-a2a7-e1514035eb93], true [7050528c-e8b1-5bee-b4eb-cc22edf3ea9f]; correct=false; ref=[":answer/id", "3cfe98d0-c506-5dc0-a2a7-e1514035eb93"]
- II (checkbox): false [8d90a213-2ee9-5f3e-afed-82d1b10872d3], true [6409af29-fa77-5e96-951f-72d66770c563]; correct=true; ref=[":answer/id", "6409af29-fa77-5e96-951f-72d66770c563"]
- III (checkbox): true [86da9440-60c3-58ad-baf9-7828eb92775f], false [7a0b9cf0-1bce-5db3-a701-cc345f386760]; correct=false; ref=[":answer/id", "7a0b9cf0-1bce-5db3-a701-cc345f386760"]

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

