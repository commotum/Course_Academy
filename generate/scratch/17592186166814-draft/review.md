# Review

All original records retain captured wording. Raw evidence is ineligible for learner use. One source error is listed in template-extraction.md. Generated labels identify authored versus source-mask variants.

## observed original q-95984

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}={e}^{y}$
- **II.** $\frac{\text{d}y}{\text{d}x}-3y=0$
- **III.** $2\frac{\text{d}y}{\text{d}x}-xy=\sqrt{x}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)={e}^{y}.$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-3y & =0 \\ \frac{\text{d}y}{\text{d}x} & =3y \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=3y.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}2\frac{\text{d}y}{\text{d}x}-xy & =\sqrt{x} \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}(xy+\sqrt{x}) \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{1}{2}(xy+\sqrt{x}).$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "I and II only."

## generated source-template variant q-95984

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}={e}^{y}$
- **II.** $\frac{\text{d}y}{\text{d}x}-2y=0$
- **III.** $3\frac{\text{d}y}{\text{d}x}-xy=\sqrt{x}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)={e}^{y}.$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-2y & =0 \\ \frac{\text{d}y}{\text{d}x} & =2y \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=2y.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}3\frac{\text{d}y}{\text{d}x}-xy & =\sqrt{x} \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{3}(xy+\sqrt{x}) \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{1}{3}(xy+\sqrt{x}).$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "I and II only."

## observed original q-96387

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}={e}^{x}$
- **II.** ${y}^{′}-\frac{3}{y}=0$
- **III.** $\frac{1}{2}{y}^{′}-xy={e}^{x}$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}-\frac{3}{y} & =0 \\ {y}^{′} & =\frac{3}{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3}{y}.$

- Equation III is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{1}{2}{y}^{′}-xy & ={e}^{x} \\ \frac{1}{2}{y}^{′} & =xy+{e}^{x} \\ {y}^{′} & =2(xy+{e}^{x}) \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)=2(xy+{e}^{x}).$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

Therefore, the correct answer is "I and III only."

## generated source-template variant q-96387

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}={e}^{x}$
- **II.** ${y}^{′}-\frac{2}{y}=0$
- **III.** $\frac{1}{3}{y}^{′}-xy={e}^{x}$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}-\frac{2}{y} & =0 \\ {y}^{′} & =\frac{2}{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=\frac{2}{y}.$

- Equation III is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{1}{3}{y}^{′}-xy & ={e}^{x} \\ \frac{1}{3}{y}^{′} & =xy+{e}^{x} \\ {y}^{′} & =3(xy+{e}^{x}) \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)=3(xy+{e}^{x}).$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

Therefore, the correct answer is "I and III only."

## observed original q-118863

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{'}-8{e}^{y}=2$
- **II.** $y{y}^{'}+3=\operatorname{cos}y$
- **III.** $x{y}^{'}-8={e}^{y}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{'}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}{y}^{'}-8{e}^{y} & =2 \\ {y}^{'} & =8{e}^{y}+2 \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=8{e}^{y}+2.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}y{y}^{'}+3 & =\operatorname{cos}y \\ {y}^{'} & =\frac{\operatorname{cos}y-3}{y} \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\frac{\operatorname{cos}y-3}{y}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}x{y}^{'}-8 & ={e}^{y} \\ {y}^{'} & =\frac{{e}^{y}+8}{x} \\ {y}^{'} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{{e}^{y}+8}{x}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

Therefore, the correct answer is "I and II only."

## generated source-template variant q-118863

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{'}-2{e}^{y}=3$
- **II.** $y{y}^{'}+2=\operatorname{cos}y$
- **III.** $x{y}^{'}-2={e}^{y}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{'}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}{y}^{'}-2{e}^{y} & =3 \\ {y}^{'} & =2{e}^{y}+3 \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=2{e}^{y}+3.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}y{y}^{'}+2 & =\operatorname{cos}y \\ {y}^{'} & =\frac{\operatorname{cos}y-2}{y} \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\frac{\operatorname{cos}y-2}{y}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}x{y}^{'}-2 & ={e}^{y} \\ {y}^{'} & =\frac{{e}^{y}+2}{x} \\ {y}^{'} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{{e}^{y}+2}{x}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

Therefore, the correct answer is "I and II only."

## observed original q-96702

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}-x={e}^{y}$
- **II.** $y\frac{\text{d}y}{\text{d}x}-2=\sqrt{y}$
- **III.** $4\frac{\text{d}y}{\text{d}x}-\frac{x}{y}=5y$

Correct checkbox values: I=false, II=true, III=false

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

## generated source-template variant q-96702

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}-x={e}^{y}$
- **II.** $y\frac{\text{d}y}{\text{d}x}-3=\sqrt{y}$
- **III.** $2\frac{\text{d}y}{\text{d}x}-\frac{x}{y}=2y$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{'}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-x & ={e}^{y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{y}+x \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)={e}^{y}+x.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}-3 & =\sqrt{y} \\ \frac{\text{d}y}{\text{d}x} & =\frac{\sqrt{y}+3}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{\sqrt{y}+3}{y}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}2\frac{\text{d}y}{\text{d}x}-\frac{x}{y} & =2y \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}(2y+\frac{x}{y}) \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{1}{2}(2y+\frac{x}{y}).$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "II only."

## observed original q-96703

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $x\frac{\text{d}y}{\text{d}x}-3{y}^{3}=2$
- **II.** $\frac{\text{d}y}{\text{d}x}-7{y}^{2}=\frac{1}{y}$
- **III.** $\frac{\text{d}y}{\text{d}x}=\operatorname{ln}y$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{'}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}-3{y}^{3} & =2 \\ \frac{\text{d}y}{\text{d}x} & =\frac{2+3{y}^{3}}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{2+3{y}^{3}}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-7{y}^{2} & =\frac{1}{y} \\ \frac{\text{d}y}{\text{d}x} & =7{y}^{2}+\frac{1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=7{y}^{2}+\frac{1}{y}.$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=\operatorname{ln}y.$

Therefore, the correct answer is "II and III only."

## generated source-template variant q-96703

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $x\frac{\text{d}y}{\text{d}x}-2{y}^{2}=3$
- **II.** $\frac{\text{d}y}{\text{d}x}-2{y}^{3}=\frac{1}{y}$
- **III.** $\frac{\text{d}y}{\text{d}x}=\operatorname{ln}y$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{'}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}-2{y}^{2} & =3 \\ \frac{\text{d}y}{\text{d}x} & =\frac{3+2{y}^{2}}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3+2{y}^{2}}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-2{y}^{3} & =\frac{1}{y} \\ \frac{\text{d}y}{\text{d}x} & =2{y}^{3}+\frac{1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=2{y}^{3}+\frac{1}{y}.$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=\operatorname{ln}y.$

Therefore, the correct answer is "II and III only."

## observed original q-96705

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{y}\frac{\text{d}y}{\text{d}x}-3{y}^{3}=0$
- **II.** $\frac{\text{d}y}{\text{d}x}-2x=\operatorname{ln}⁡y$
- **III.** $5x\frac{\text{d}y}{\text{d}x}-\frac{y}{x}=0$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}{e}^{y}\frac{\text{d}y}{\text{d}x}-3{y}^{3} & =0 \\ \frac{\text{d}y}{\text{d}x} & =3{y}^{3}{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=3{y}^{3}{e}^{-y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-2x & =\operatorname{ln}⁡y \\ \frac{\text{d}y}{\text{d}x} & =\operatorname{ln}⁡y+2x \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\operatorname{ln}⁡y+2x.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}5x\frac{\text{d}y}{\text{d}x}-\frac{y}{x} & =0 \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{5{x}^{2}} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{y}{5{x}^{2}}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "I only."

## generated source-template variant q-96705

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{y}\frac{\text{d}y}{\text{d}x}-2{y}^{2}=0$
- **II.** $\frac{\text{d}y}{\text{d}x}-3x=\operatorname{ln}⁡y$
- **III.** $2x\frac{\text{d}y}{\text{d}x}-\frac{y}{x}=0$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}{e}^{y}\frac{\text{d}y}{\text{d}x}-2{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =2{y}^{2}{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=2{y}^{2}{e}^{-y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-3x & =\operatorname{ln}⁡y \\ \frac{\text{d}y}{\text{d}x} & =\operatorname{ln}⁡y+3x \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\operatorname{ln}⁡y+3x.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}2x\frac{\text{d}y}{\text{d}x}-\frac{y}{x} & =0 \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{2{x}^{2}} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{y}{2{x}^{2}}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "I only."

## observed original q-96712

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{'}=1-\sqrt{y}$
- **II.** ${y}^{'}-\operatorname{tan}y={e}^{2}$
- **III.** $x{y}^{'}-\frac{1}{y}=4$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{'}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. It is of the form ${y}^{'}=f(y),$ where $f(y)=1-\sqrt{y}.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}{y}^{'}-\operatorname{tan}y & ={e}^{2} \\ {y}^{'} & =\operatorname{tan}y+{e}^{2} \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\operatorname{tan}y+{e}^{2}.$

- Equation III is *not* an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x{y}^{'}-\frac{1}{y} & =4 \\ {y}^{'} & =\frac{4y+1}{xy} \\ {y}^{'} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{4y+1}{xy}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

Therefore, the correct answer is "III only."

## generated source-template variant q-96712

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{'}=1-\sqrt{y}$
- **II.** ${y}^{'}-\operatorname{tan}y={e}^{3}$
- **III.** $x{y}^{'}-\frac{1}{y}=2$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{'}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. It is of the form ${y}^{'}=f(y),$ where $f(y)=1-\sqrt{y}.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}{y}^{'}-\operatorname{tan}y & ={e}^{3} \\ {y}^{'} & =\operatorname{tan}y+{e}^{3} \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\operatorname{tan}y+{e}^{3}.$

- Equation III is *not* an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x{y}^{'}-\frac{1}{y} & =2 \\ {y}^{'} & =\frac{2y+1}{xy} \\ {y}^{'} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{2y+1}{xy}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

Therefore, the correct answer is "III only."

## observed original q-118858

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{2y}{y}^{′}+1=0$
- **II.** ${y}^{′}+\sqrt{xy}=2$
- **III.** ${y}^{′}=\operatorname{ln}⁡y$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{e}^{2y}{y}^{′}+1 & =0 \\ {y}^{′} & =-{e}^{-2y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=-{e}^{-2y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{y}^{′}+\sqrt{xy} & =2 \\ {y}^{′} & =2-\sqrt{xy} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)=2-\sqrt{xy}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form ${y}^{′}=f(y),$ where $f(y)=\operatorname{ln}⁡y.$

Therefore, the correct answer is "I and III only."

## generated source-template variant q-118858

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{3y}{y}^{′}+1=0$
- **II.** ${y}^{′}+\sqrt{xy}=3$
- **III.** ${y}^{′}=\operatorname{ln}⁡y$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{e}^{3y}{y}^{′}+1 & =0 \\ {y}^{′} & =-{e}^{-3y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=-{e}^{-3y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{y}^{′}+\sqrt{xy} & =3 \\ {y}^{′} & =3-\sqrt{xy} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)=3-\sqrt{xy}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form ${y}^{′}=f(y),$ where $f(y)=\operatorname{ln}⁡y.$

Therefore, the correct answer is "I and III only."

## observed original q-118859

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}-3{x}^{2}=1$
- **II.** ${y}^{′}+6y={e}^{3y}$
- **III.** ${y}^{′}=\operatorname{ln}⁡(2{x}^{2}+1)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}{y}^{′}-3{x}^{2} & =1 \\ {y}^{′} & =3{x}^{2}+1 \\ {y}^{′} & =f(x)\end{aligned}
$$

where $f(x)=3{x}^{2}+1.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}+6y & ={e}^{3y} \\ {y}^{′} & ={e}^{3y}-6y \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)={e}^{3y}-6y.$

- Equation III is not an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

Therefore, the correct answer is "II only."

## generated source-template variant q-118859

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}-2{x}^{3}=1$
- **II.** ${y}^{′}+2y={e}^{2y}$
- **III.** ${y}^{′}=\operatorname{ln}⁡(3{x}^{3}+1)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}{y}^{′}-2{x}^{3} & =1 \\ {y}^{′} & =2{x}^{3}+1 \\ {y}^{′} & =f(x)\end{aligned}
$$

where $f(x)=2{x}^{3}+1.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}+2y & ={e}^{2y} \\ {y}^{′} & ={e}^{2y}-2y \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)={e}^{2y}-2y.$

- Equation III is not an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

Therefore, the correct answer is "II only."

## observed original q-118868

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${x}^{2}{y}^{′}+6x{y}^{2}=8$
- **II.** ${y}^{′}+\frac{1}{x}=3{y}^{2}$
- **III.** ${y}^{′}=\operatorname{arctan}⁡({y}^{2}+2)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{x}^{2}{y}^{′}+6x{y}^{2} & =8 \\ {y}^{′} & =\frac{8-6x{y}^{2}}{{x}^{2}} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{8-6x{y}^{2}}{{x}^{2}}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{y}^{′}+\frac{1}{x} & =3{y}^{2} \\ {y}^{′} & =3{y}^{2}-\frac{1}{x} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)=3{y}^{2}-\frac{1}{x}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form ${y}^{′}=f(y),$ where $f(y)=\operatorname{arctan}⁡({y}^{2}+2).$

Therefore, the correct answer is "III only."

## generated source-template variant q-118868

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${x}^{3}{y}^{′}+2x{y}^{3}=2$
- **II.** ${y}^{′}+\frac{1}{x}=2{y}^{3}$
- **III.** ${y}^{′}=\operatorname{arctan}⁡({y}^{3}+3)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{x}^{3}{y}^{′}+2x{y}^{3} & =2 \\ {y}^{′} & =\frac{2-2x{y}^{3}}{{x}^{3}} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{2-2x{y}^{3}}{{x}^{3}}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{y}^{′}+\frac{1}{x} & =2{y}^{3} \\ {y}^{′} & =2{y}^{3}-\frac{1}{x} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)=2{y}^{3}-\frac{1}{x}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form ${y}^{′}=f(y),$ where $f(y)=\operatorname{arctan}⁡({y}^{3}+3).$

Therefore, the correct answer is "III only."

## observed original q-118869

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{{y}^{′}}{y}+\frac{1}{\operatorname{arctan}⁡y+2\pi }=0$
- **II.** ${y}^{′}+{y}^{2}={x}^{2}$
- **III.** ${y}^{′}=\operatorname{sin}⁡x$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}\frac{{y}^{′}}{y}+\frac{1}{\operatorname{arctan}⁡y+2\pi } & =0 \\ {y}^{′} & =-\frac{y}{\operatorname{arctan}⁡y+2\pi } \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=-\frac{y}{\operatorname{arctan}⁡y+2\pi }.$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{y}^{′}+{y}^{2} & ={x}^{2} \\ {y}^{′} & ={x}^{2}-{y}^{2} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)={x}^{2}-{y}^{2}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

Therefore, the correct answer is "II and III only."

## generated source-template variant q-118869

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{{y}^{′}}{y}+\frac{1}{\operatorname{arctan}⁡y+3\pi }=0$
- **II.** ${y}^{′}+{y}^{3}={x}^{3}$
- **III.** ${y}^{′}=\operatorname{sin}⁡x$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}\frac{{y}^{′}}{y}+\frac{1}{\operatorname{arctan}⁡y+3\pi } & =0 \\ {y}^{′} & =-\frac{y}{\operatorname{arctan}⁡y+3\pi } \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=-\frac{y}{\operatorname{arctan}⁡y+3\pi }.$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{y}^{′}+{y}^{3} & ={x}^{3} \\ {y}^{′} & ={x}^{3}-{y}^{3} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)={x}^{3}-{y}^{3}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

Therefore, the correct answer is "II and III only."

## observed original q-118870

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}={e}^{3-y}-2$
- **II.** $y{y}^{′}+\operatorname{cos}⁡y=1$
- **III.** ${y}^{′}=\operatorname{tan}⁡(x+y)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. It is of the form ${y}^{′}=f(y),$ where $f(y)={e}^{3-y}-2.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}y{y}^{′}+\operatorname{cos}⁡y & =1 \\ {y}^{′} & =\frac{1-\operatorname{cos}⁡y}{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=\frac{1-\operatorname{cos}⁡y}{y}.$

- Equation III is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

Therefore, the correct answer is "III only."

## generated source-template variant q-118870

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}={e}^{2-y}-3$
- **II.** $y{y}^{′}+\operatorname{cos}⁡y=1$
- **III.** ${y}^{′}=\operatorname{tan}⁡(x+y)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. It is of the form ${y}^{′}=f(y),$ where $f(y)={e}^{2-y}-3.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}y{y}^{′}+\operatorname{cos}⁡y & =1 \\ {y}^{′} & =\frac{1-\operatorname{cos}⁡y}{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=\frac{1-\operatorname{cos}⁡y}{y}.$

- Equation III is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

Therefore, the correct answer is "III only."

## observed original q-96711

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}=\operatorname{sin}⁡(\frac{y}{x})$
- **II.** ${y}^{′}-{x}^{2}y={e}^{x}$
- **III.** ${y}^{′}-\frac{3}{{y}^{2}}=1$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{y}^{′}-{x}^{2}y & ={e}^{x} \\ {y}^{′} & ={x}^{2}y+{e}^{x} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)={x}^{2}y+{e}^{x}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}-\frac{3}{{y}^{2}} & =1 \\ {y}^{′} & =\frac{3}{{y}^{2}}+1 \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3}{{y}^{2}}+1.$

Therefore, the correct answer is "I and II only."

## generated source-template variant q-96711

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}=\operatorname{sin}⁡(\frac{y}{x})$
- **II.** ${y}^{′}-{x}^{3}y={e}^{x}$
- **III.** ${y}^{′}-\frac{2}{{y}^{3}}=1$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{y}^{′}-{x}^{3}y & ={e}^{x} \\ {y}^{′} & ={x}^{3}y+{e}^{x} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)={x}^{3}y+{e}^{x}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}-\frac{2}{{y}^{3}} & =1 \\ {y}^{′} & =\frac{2}{{y}^{3}}+1 \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=\frac{2}{{y}^{3}}+1.$

Therefore, the correct answer is "I and II only."

## observed original q-96713

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{-y}{y}^{′}=-\sqrt{y}$
- **II.** ${y}^{′}-{y}^{3}=2{e}^{x}$
- **III.** ${y}^{′}-\frac{2}{{y}^{3}}=3\sqrt{y}$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{e}^{-y}{y}^{′} & =-\sqrt{y} \\ {y}^{′} & =-\sqrt{y}{e}^{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=-\sqrt{y}{e}^{y}.$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}{y}^{′}-{y}^{3} & =2{e}^{x} \\ {y}^{′} & ={y}^{3}+2{e}^{x} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)={y}^{3}+2{e}^{x}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}-\frac{2}{{y}^{3}} & =3\sqrt{y} \\ {y}^{′} & =\frac{2}{{y}^{3}}+3\sqrt{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=\frac{2}{{y}^{3}}+3\sqrt{y}.$

Therefore, the correct answer is "II only."

## generated source-template variant q-96713

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{-y}{y}^{′}=-\sqrt{y}$
- **II.** ${y}^{′}-{y}^{2}=3{e}^{x}$
- **III.** ${y}^{′}-\frac{3}{{y}^{2}}=2\sqrt{y}$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{e}^{-y}{y}^{′} & =-\sqrt{y} \\ {y}^{′} & =-\sqrt{y}{e}^{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=-\sqrt{y}{e}^{y}.$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}{y}^{′}-{y}^{2} & =3{e}^{x} \\ {y}^{′} & ={y}^{2}+3{e}^{x} \\ {y}^{′} & =f(x,y)\end{aligned}
$$

where $f(x,y)={y}^{2}+3{e}^{x}.$ So, it is not possible to write the equation in the form ${y}^{′}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}-\frac{3}{{y}^{2}} & =2\sqrt{y} \\ {y}^{′} & =\frac{3}{{y}^{2}}+2\sqrt{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3}{{y}^{2}}+2\sqrt{y}.$

Therefore, the correct answer is "II only."

## observed original q-96715

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}=\sqrt{{x}^{2}+\operatorname{sin}⁡y}$
- **II.** ${y}^{′}=\operatorname{sec}⁡\sqrt{2y}$
- **III.** ${y}^{′}-{y}^{3}=3\sqrt{y}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

- Equation II is an autonomous differential equation. It is of the form ${y}^{′}=f(y),$ where $f(y)=\operatorname{sec}⁡\sqrt{2y}.$

- Equation III is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}-{y}^{3} & =3\sqrt{y} \\ {y}^{′} & ={y}^{3}+3\sqrt{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)={y}^{3}+3\sqrt{y}.$

Therefore, the correct answer is "I only."

## generated source-template variant q-96715

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}=\sqrt{{x}^{3}+\operatorname{sin}⁡y}$
- **II.** ${y}^{′}=\operatorname{sec}⁡\sqrt{3y}$
- **III.** ${y}^{′}-{y}^{2}=2\sqrt{y}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${y}^{′}=f(y).$

- Equation II is an autonomous differential equation. It is of the form ${y}^{′}=f(y),$ where $f(y)=\operatorname{sec}⁡\sqrt{3y}.$

- Equation III is an autonomous differential equation. Writing the equation in the form ${y}^{′}=f(y),$ we get

$$
\begin{aligned}{y}^{′}-{y}^{2} & =2\sqrt{y} \\ {y}^{′} & ={y}^{2}+2\sqrt{y} \\ {y}^{′} & =f(y)\end{aligned}
$$

where $f(y)={y}^{2}+2\sqrt{y}.$

Therefore, the correct answer is "I only."

## generated source binding variant q-95984 prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}={e}^{u}$
- **II.** ${u}^{'}-3u=0$
- **III.** $2{u}^{'}-tu=\sqrt{t}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form ${u}^{'}=f(u),$ where $f(u)={e}^{u}.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}-3u & =0 \\ {u}^{'} & =3u \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=3u.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}2{u}^{'}-tu & =\sqrt{t} \\ {u}^{'} & =\frac{1}{2}(tu+\sqrt{t}) \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{1}{2}(tu+\sqrt{t}).$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

Therefore, the correct answer is "I and II only."

## generated source binding variant q-95984 leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}={e}^{v}$
- **II.** $\frac{\text{d}v}{\text{d}s}-3v=0$
- **III.** $2\frac{\text{d}v}{\text{d}s}-sv=\sqrt{s}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)={e}^{v}.$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-3v & =0 \\ \frac{\text{d}v}{\text{d}s} & =3v \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=3v.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}2\frac{\text{d}v}{\text{d}s}-sv & =\sqrt{s} \\ \frac{\text{d}v}{\text{d}s} & =\frac{1}{2}(sv+\sqrt{s}) \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{1}{2}(sv+\sqrt{s}).$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "I and II only."

## generated source binding variant q-96387 prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}={e}^{t}$
- **II.** ${u}^{'}-\frac{3}{u}=0$
- **III.** $\frac{1}{2}{u}^{'}-tu={e}^{t}$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${u}^{'}=f(u).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}-\frac{3}{u} & =0 \\ {u}^{'} & =\frac{3}{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\frac{3}{u}.$

- Equation III is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{1}{2}{u}^{'}-tu & ={e}^{t} \\ \frac{1}{2}{u}^{'} & =tu+{e}^{t} \\ {u}^{'} & =2(tu+{e}^{t}) \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=2(tu+{e}^{t}).$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

Therefore, the correct answer is "I and III only."

## generated source binding variant q-96387 leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}={e}^{s}$
- **II.** $\frac{\text{d}v}{\text{d}s}-\frac{3}{v}=0$
- **III.** $\frac{1}{2}\frac{\text{d}v}{\text{d}s}-sv={e}^{s}$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-\frac{3}{v} & =0 \\ \frac{\text{d}v}{\text{d}s} & =\frac{3}{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\frac{3}{v}.$

- Equation III is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{1}{2}\frac{\text{d}v}{\text{d}s}-sv & ={e}^{s} \\ \frac{1}{2}\frac{\text{d}v}{\text{d}s} & =sv+{e}^{s} \\ \frac{\text{d}v}{\text{d}s} & =2(sv+{e}^{s}) \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=2(sv+{e}^{s}).$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "I and III only."

## generated source binding variant q-118863 prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}-8{e}^{u}=2$
- **II.** $u{u}^{'}+3=\operatorname{cos}u$
- **III.** $t{u}^{'}-8={e}^{u}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{'}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}-8{e}^{u} & =2 \\ {u}^{'} & =8{e}^{u}+2 \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=8{e}^{u}+2.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}u{u}^{'}+3 & =\operatorname{cos}u \\ {u}^{'} & =\frac{\operatorname{cos}u-3}{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\frac{\operatorname{cos}u-3}{u}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}t{u}^{'}-8 & ={e}^{u} \\ {u}^{'} & =\frac{{e}^{u}+8}{t} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{{e}^{u}+8}{t}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

Therefore, the correct answer is "I and II only."

## generated source binding variant q-118863 leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}-8{e}^{v}=2$
- **II.** $v\frac{\text{d}v}{\text{d}s}+3=\operatorname{cos}v$
- **III.** $s\frac{\text{d}v}{\text{d}s}-8={e}^{v}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{'}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-8{e}^{v} & =2 \\ \frac{\text{d}v}{\text{d}s} & =8{e}^{v}+2 \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=8{e}^{v}+2.$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}v\frac{\text{d}v}{\text{d}s}+3 & =\operatorname{cos}v \\ \frac{\text{d}v}{\text{d}s} & =\frac{\operatorname{cos}v-3}{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\frac{\operatorname{cos}v-3}{v}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}s\frac{\text{d}v}{\text{d}s}-8 & ={e}^{v} \\ \frac{\text{d}v}{\text{d}s} & =\frac{{e}^{v}+8}{s} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{{e}^{v}+8}{s}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "I and II only."

## generated source binding variant q-96702 prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}-t={e}^{u}$
- **II.** $u{u}^{'}-2=\sqrt{u}$
- **III.** $4{u}^{'}-\frac{t}{u}=5u$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{'}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{u}^{'}-t & ={e}^{u} \\ {u}^{'} & ={e}^{u}+t \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)={e}^{u}+t.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}u{u}^{'}-2 & =\sqrt{u} \\ {u}^{'} & =\frac{\sqrt{u}+2}{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\frac{\sqrt{u}+2}{u}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}4{u}^{'}-\frac{t}{u} & =5u \\ {u}^{'} & =\frac{1}{4}(5u+\frac{t}{u}) \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{1}{4}(5u+\frac{t}{u}).$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

Therefore, the correct answer is "II only."

## generated source binding variant q-96702 leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}-s={e}^{v}$
- **II.** $v\frac{\text{d}v}{\text{d}s}-2=\sqrt{v}$
- **III.** $4\frac{\text{d}v}{\text{d}s}-\frac{s}{v}=5v$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{'}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-s & ={e}^{v} \\ \frac{\text{d}v}{\text{d}s} & ={e}^{v}+s \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)={e}^{v}+s.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}v\frac{\text{d}v}{\text{d}s}-2 & =\sqrt{v} \\ \frac{\text{d}v}{\text{d}s} & =\frac{\sqrt{v}+2}{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\frac{\sqrt{v}+2}{v}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}4\frac{\text{d}v}{\text{d}s}-\frac{s}{v} & =5v \\ \frac{\text{d}v}{\text{d}s} & =\frac{1}{4}(5v+\frac{s}{v}) \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{1}{4}(5v+\frac{s}{v}).$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "II only."

## generated source binding variant q-96703 prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $t{u}^{'}-3{u}^{3}=2$
- **II.** ${u}^{'}-7{u}^{2}=\frac{1}{u}$
- **III.** ${u}^{'}=\operatorname{ln}u$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{'}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}t{u}^{'}-3{u}^{3} & =2 \\ {u}^{'} & =\frac{2+3{u}^{3}}{t} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{2+3{u}^{3}}{t}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}-7{u}^{2} & =\frac{1}{u} \\ {u}^{'} & =7{u}^{2}+\frac{1}{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=7{u}^{2}+\frac{1}{u}.$

- Equation III is an autonomous differential equation. We see that it is of the form ${u}^{'}=f(u),$ where $f(u)=\operatorname{ln}u.$

Therefore, the correct answer is "II and III only."

## generated source binding variant q-96703 leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $s\frac{\text{d}v}{\text{d}s}-3{v}^{3}=2$
- **II.** $\frac{\text{d}v}{\text{d}s}-7{v}^{2}=\frac{1}{v}$
- **III.** $\frac{\text{d}v}{\text{d}s}=\operatorname{ln}v$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{'}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}s\frac{\text{d}v}{\text{d}s}-3{v}^{3} & =2 \\ \frac{\text{d}v}{\text{d}s} & =\frac{2+3{v}^{3}}{s} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{2+3{v}^{3}}{s}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-7{v}^{2} & =\frac{1}{v} \\ \frac{\text{d}v}{\text{d}s} & =7{v}^{2}+\frac{1}{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=7{v}^{2}+\frac{1}{v}.$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)=\operatorname{ln}v.$

Therefore, the correct answer is "II and III only."

## generated source binding variant q-96705 prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{u}{u}^{'}-3{u}^{3}=0$
- **II.** ${u}^{'}-2t=\operatorname{ln}⁡u$
- **III.** $5t{u}^{'}-\frac{u}{t}=0$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{e}^{u}{u}^{'}-3{u}^{3} & =0 \\ {u}^{'} & =3{u}^{3}{e}^{-u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=3{u}^{3}{e}^{-u}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{u}^{'}-2t & =\operatorname{ln}⁡u \\ {u}^{'} & =\operatorname{ln}⁡u+2t \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\operatorname{ln}⁡u+2t.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}5t{u}^{'}-\frac{u}{t} & =0 \\ {u}^{'} & =\frac{u}{5{t}^{2}} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{u}{5{t}^{2}}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

Therefore, the correct answer is "I only."

## generated source binding variant q-96705 leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{v}\frac{\text{d}v}{\text{d}s}-3{v}^{3}=0$
- **II.** $\frac{\text{d}v}{\text{d}s}-2s=\operatorname{ln}⁡v$
- **III.** $5s\frac{\text{d}v}{\text{d}s}-\frac{v}{s}=0$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}{e}^{v}\frac{\text{d}v}{\text{d}s}-3{v}^{3} & =0 \\ \frac{\text{d}v}{\text{d}s} & =3{v}^{3}{e}^{-v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=3{v}^{3}{e}^{-v}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-2s & =\operatorname{ln}⁡v \\ \frac{\text{d}v}{\text{d}s} & =\operatorname{ln}⁡v+2s \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\operatorname{ln}⁡v+2s.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}5s\frac{\text{d}v}{\text{d}s}-\frac{v}{s} & =0 \\ \frac{\text{d}v}{\text{d}s} & =\frac{v}{5{s}^{2}} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{v}{5{s}^{2}}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "I only."

## generated source binding variant q-96712 prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}=1-\sqrt{u}$
- **II.** ${u}^{'}-\operatorname{tan}u={e}^{2}$
- **III.** $t{u}^{'}-\frac{1}{u}=4$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{'}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. It is of the form ${u}^{'}=f(u),$ where $f(u)=1-\sqrt{u}.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}-\operatorname{tan}u & ={e}^{2} \\ {u}^{'} & =\operatorname{tan}u+{e}^{2} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\operatorname{tan}u+{e}^{2}.$

- Equation III is *not* an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t{u}^{'}-\frac{1}{u} & =4 \\ {u}^{'} & =\frac{4u+1}{tu} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{4u+1}{tu}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

Therefore, the correct answer is "III only."

## generated source binding variant q-96712 leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}=1-\sqrt{v}$
- **II.** $\frac{\text{d}v}{\text{d}s}-\operatorname{tan}v={e}^{2}$
- **III.** $s\frac{\text{d}v}{\text{d}s}-\frac{1}{v}=4$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{'}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. It is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)=1-\sqrt{v}.$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-\operatorname{tan}v & ={e}^{2} \\ \frac{\text{d}v}{\text{d}s} & =\operatorname{tan}v+{e}^{2} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\operatorname{tan}v+{e}^{2}.$

- Equation III is *not* an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}s\frac{\text{d}v}{\text{d}s}-\frac{1}{v} & =4 \\ \frac{\text{d}v}{\text{d}s} & =\frac{4v+1}{sv} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{4v+1}{sv}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "III only."

## generated source binding variant q-118858 prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{2u}{u}^{'}+1=0$
- **II.** ${u}^{'}+\sqrt{tu}=2$
- **III.** ${u}^{'}=\operatorname{ln}⁡u$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{e}^{2u}{u}^{'}+1 & =0 \\ {u}^{'} & =-{e}^{-2u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=-{e}^{-2u}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{u}^{'}+\sqrt{tu} & =2 \\ {u}^{'} & =2-\sqrt{tu} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=2-\sqrt{tu}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation III is an autonomous differential equation. We see that it is of the form ${u}^{'}=f(u),$ where $f(u)=\operatorname{ln}⁡u.$

Therefore, the correct answer is "I and III only."

## generated source binding variant q-118858 leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{2v}\frac{\text{d}v}{\text{d}s}+1=0$
- **II.** $\frac{\text{d}v}{\text{d}s}+\sqrt{sv}=2$
- **III.** $\frac{\text{d}v}{\text{d}s}=\operatorname{ln}⁡v$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}{e}^{2v}\frac{\text{d}v}{\text{d}s}+1 & =0 \\ \frac{\text{d}v}{\text{d}s} & =-{e}^{-2v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=-{e}^{-2v}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}+\sqrt{sv} & =2 \\ \frac{\text{d}v}{\text{d}s} & =2-\sqrt{sv} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=2-\sqrt{sv}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)=\operatorname{ln}⁡v.$

Therefore, the correct answer is "I and III only."

## generated source binding variant q-118859 prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}-3{t}^{2}=1$
- **II.** ${u}^{'}+6u={e}^{3u}$
- **III.** ${u}^{'}=\operatorname{ln}⁡(2{t}^{2}+1)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}{u}^{'}-3{t}^{2} & =1 \\ {u}^{'} & =3{t}^{2}+1 \\ {u}^{'} & =f(t)\end{aligned}
$$

where $f(t)=3{t}^{2}+1.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}+6u & ={e}^{3u} \\ {u}^{'} & ={e}^{3u}-6u \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)={e}^{3u}-6u.$

- Equation III is not an autonomous differential equation. It is not of the form ${u}^{'}=f(u).$

Therefore, the correct answer is "II only."

## generated source binding variant q-118859 leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}-3{s}^{2}=1$
- **II.** $\frac{\text{d}v}{\text{d}s}+6v={e}^{3v}$
- **III.** $\frac{\text{d}v}{\text{d}s}=\operatorname{ln}⁡(2{s}^{2}+1)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-3{s}^{2} & =1 \\ \frac{\text{d}v}{\text{d}s} & =3{s}^{2}+1 \\ \frac{\text{d}v}{\text{d}s} & =f(s)\end{aligned}
$$

where $f(s)=3{s}^{2}+1.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}+6v & ={e}^{3v} \\ \frac{\text{d}v}{\text{d}s} & ={e}^{3v}-6v \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)={e}^{3v}-6v.$

- Equation III is not an autonomous differential equation. It is not of the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "II only."

## generated source binding variant q-118868 prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${t}^{2}{u}^{'}+6t{u}^{2}=8$
- **II.** ${u}^{'}+\frac{1}{t}=3{u}^{2}$
- **III.** ${u}^{'}=\operatorname{arctan}⁡({u}^{2}+2)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{t}^{2}{u}^{'}+6t{u}^{2} & =8 \\ {u}^{'} & =\frac{8-6t{u}^{2}}{{t}^{2}} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{8-6t{u}^{2}}{{t}^{2}}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{u}^{'}+\frac{1}{t} & =3{u}^{2} \\ {u}^{'} & =3{u}^{2}-\frac{1}{t} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=3{u}^{2}-\frac{1}{t}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation III is an autonomous differential equation. We see that it is of the form ${u}^{'}=f(u),$ where $f(u)=\operatorname{arctan}⁡({u}^{2}+2).$

Therefore, the correct answer is "III only."

## generated source binding variant q-118868 leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${s}^{2}\frac{\text{d}v}{\text{d}s}+6s{v}^{2}=8$
- **II.** $\frac{\text{d}v}{\text{d}s}+\frac{1}{s}=3{v}^{2}$
- **III.** $\frac{\text{d}v}{\text{d}s}=\operatorname{arctan}⁡({v}^{2}+2)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{s}^{2}\frac{\text{d}v}{\text{d}s}+6s{v}^{2} & =8 \\ \frac{\text{d}v}{\text{d}s} & =\frac{8-6s{v}^{2}}{{s}^{2}} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{8-6s{v}^{2}}{{s}^{2}}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}+\frac{1}{s} & =3{v}^{2} \\ \frac{\text{d}v}{\text{d}s} & =3{v}^{2}-\frac{1}{s} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=3{v}^{2}-\frac{1}{s}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)=\operatorname{arctan}⁡({v}^{2}+2).$

Therefore, the correct answer is "III only."

## generated source binding variant q-118869 prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{{u}^{'}}{u}+\frac{1}{\operatorname{arctan}⁡u+2\pi }=0$
- **II.** ${u}^{'}+{u}^{2}={t}^{2}$
- **III.** ${u}^{'}=\operatorname{sin}⁡t$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}\frac{{u}^{'}}{u}+\frac{1}{\operatorname{arctan}⁡u+2\pi } & =0 \\ {u}^{'} & =-\frac{u}{\operatorname{arctan}⁡u+2\pi } \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=-\frac{u}{\operatorname{arctan}⁡u+2\pi }.$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{u}^{'}+{u}^{2} & ={t}^{2} \\ {u}^{'} & ={t}^{2}-{u}^{2} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)={t}^{2}-{u}^{2}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation III is *not* an autonomous differential equation. It is not of the form ${u}^{'}=f(u).$

Therefore, the correct answer is "II and III only."

## generated source binding variant q-118869 leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\frac{\text{d}v}{\text{d}s}}{v}+\frac{1}{\operatorname{arctan}⁡v+2\pi }=0$
- **II.** $\frac{\text{d}v}{\text{d}s}+{v}^{2}={s}^{2}$
- **III.** $\frac{\text{d}v}{\text{d}s}=\operatorname{sin}⁡s$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\frac{\text{d}v}{\text{d}s}}{v}+\frac{1}{\operatorname{arctan}⁡v+2\pi } & =0 \\ \frac{\text{d}v}{\text{d}s} & =-\frac{v}{\operatorname{arctan}⁡v+2\pi } \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=-\frac{v}{\operatorname{arctan}⁡v+2\pi }.$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}+{v}^{2} & ={s}^{2} \\ \frac{\text{d}v}{\text{d}s} & ={s}^{2}-{v}^{2} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)={s}^{2}-{v}^{2}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation III is *not* an autonomous differential equation. It is not of the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "II and III only."

## generated source binding variant q-118870 prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}={e}^{3-u}-2$
- **II.** $u{u}^{'}+\operatorname{cos}⁡u=1$
- **III.** ${u}^{'}=\operatorname{tan}⁡(t+u)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. It is of the form ${u}^{'}=f(u),$ where $f(u)={e}^{3-u}-2.$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}u{u}^{'}+\operatorname{cos}⁡u & =1 \\ {u}^{'} & =\frac{1-\operatorname{cos}⁡u}{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\frac{1-\operatorname{cos}⁡u}{u}.$

- Equation III is *not* an autonomous differential equation. It is not of the form ${u}^{'}=f(u).$

Therefore, the correct answer is "III only."

## generated source binding variant q-118870 leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}={e}^{3-v}-2$
- **II.** $v\frac{\text{d}v}{\text{d}s}+\operatorname{cos}⁡v=1$
- **III.** $\frac{\text{d}v}{\text{d}s}=\operatorname{tan}⁡(s+v)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. It is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)={e}^{3-v}-2.$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}v\frac{\text{d}v}{\text{d}s}+\operatorname{cos}⁡v & =1 \\ \frac{\text{d}v}{\text{d}s} & =\frac{1-\operatorname{cos}⁡v}{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\frac{1-\operatorname{cos}⁡v}{v}.$

- Equation III is *not* an autonomous differential equation. It is not of the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "III only."

## generated source binding variant q-96711 prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}=\operatorname{sin}⁡(\frac{u}{t})$
- **II.** ${u}^{'}-{t}^{2}u={e}^{t}$
- **III.** ${u}^{'}-\frac{3}{{u}^{2}}=1$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${u}^{'}=f(u).$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}{u}^{'}-{t}^{2}u & ={e}^{t} \\ {u}^{'} & ={t}^{2}u+{e}^{t} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)={t}^{2}u+{e}^{t}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation III is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}-\frac{3}{{u}^{2}} & =1 \\ {u}^{'} & =\frac{3}{{u}^{2}}+1 \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\frac{3}{{u}^{2}}+1.$

Therefore, the correct answer is "I and II only."

## generated source binding variant q-96711 leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}=\operatorname{sin}⁡(\frac{v}{s})$
- **II.** $\frac{\text{d}v}{\text{d}s}-{s}^{2}v={e}^{s}$
- **III.** $\frac{\text{d}v}{\text{d}s}-\frac{3}{{v}^{2}}=1$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get 

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-{s}^{2}v & ={e}^{s} \\ \frac{\text{d}v}{\text{d}s} & ={s}^{2}v+{e}^{s} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)={s}^{2}v+{e}^{s}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-\frac{3}{{v}^{2}} & =1 \\ \frac{\text{d}v}{\text{d}s} & =\frac{3}{{v}^{2}}+1 \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\frac{3}{{v}^{2}}+1.$

Therefore, the correct answer is "I and II only."

## generated source binding variant q-96713 prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{-u}{u}^{'}=-\sqrt{u}$
- **II.** ${u}^{'}-{u}^{3}=2{e}^{t}$
- **III.** ${u}^{'}-\frac{2}{{u}^{3}}=3\sqrt{u}$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{e}^{-u}{u}^{'} & =-\sqrt{u} \\ {u}^{'} & =-\sqrt{u}{e}^{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=-\sqrt{u}{e}^{u}.$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}{u}^{'}-{u}^{3} & =2{e}^{t} \\ {u}^{'} & ={u}^{3}+2{e}^{t} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)={u}^{3}+2{e}^{t}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation III is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}-\frac{2}{{u}^{3}} & =3\sqrt{u} \\ {u}^{'} & =\frac{2}{{u}^{3}}+3\sqrt{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\frac{2}{{u}^{3}}+3\sqrt{u}.$

Therefore, the correct answer is "II only."

## generated source binding variant q-96713 leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{-v}\frac{\text{d}v}{\text{d}s}=-\sqrt{v}$
- **II.** $\frac{\text{d}v}{\text{d}s}-{v}^{3}=2{e}^{s}$
- **III.** $\frac{\text{d}v}{\text{d}s}-\frac{2}{{v}^{3}}=3\sqrt{v}$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}{e}^{-v}\frac{\text{d}v}{\text{d}s} & =-\sqrt{v} \\ \frac{\text{d}v}{\text{d}s} & =-\sqrt{v}{e}^{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=-\sqrt{v}{e}^{v}.$

- Equation II is *not* an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-{v}^{3} & =2{e}^{s} \\ \frac{\text{d}v}{\text{d}s} & ={v}^{3}+2{e}^{s} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)={v}^{3}+2{e}^{s}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-\frac{2}{{v}^{3}} & =3\sqrt{v} \\ \frac{\text{d}v}{\text{d}s} & =\frac{2}{{v}^{3}}+3\sqrt{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\frac{2}{{v}^{3}}+3\sqrt{v}.$

Therefore, the correct answer is "II only."

## generated source binding variant q-96715 prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}=\sqrt{{t}^{2}+\operatorname{sin}⁡u}$
- **II.** ${u}^{'}=\operatorname{sec}⁡\sqrt{2u}$
- **III.** ${u}^{'}-{u}^{3}=3\sqrt{u}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form ${u}^{'}=f(u).$

- Equation II is an autonomous differential equation. It is of the form ${u}^{'}=f(u),$ where $f(u)=\operatorname{sec}⁡\sqrt{2u}.$

- Equation III is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}{u}^{'}-{u}^{3} & =3\sqrt{u} \\ {u}^{'} & ={u}^{3}+3\sqrt{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)={u}^{3}+3\sqrt{u}.$

Therefore, the correct answer is "I only."

## generated source binding variant q-96715 leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}=\sqrt{{s}^{2}+\operatorname{sin}⁡v}$
- **II.** $\frac{\text{d}v}{\text{d}s}=\operatorname{sec}⁡\sqrt{2v}$
- **III.** $\frac{\text{d}v}{\text{d}s}-{v}^{3}=3\sqrt{v}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is *not* an autonomous differential equation. It is not of the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is an autonomous differential equation. It is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)=\operatorname{sec}⁡\sqrt{2v}.$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\frac{\text{d}v}{\text{d}s}-{v}^{3} & =3\sqrt{v} \\ \frac{\text{d}v}{\text{d}s} & ={v}^{3}+3\sqrt{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)={v}^{3}+3\sqrt{v}.$

Therefore, the correct answer is "I only."

## generated authored easy 0 criterion False

Let $y=y(x)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=e^{y}$
- **II.** $\frac{\text{d}y}{\text{d}x}=x^{2}$
- **III.** $\frac{\text{d}y}{\text{d}x}=y^{2}$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=e^{y}.$

- Equation II is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=y^{2}.$

Therefore, the correct answer is "I and III only."

## generated authored easy 0 criterion True

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=e^{y}$
- **II.** $\frac{\text{d}y}{\text{d}x}=x^{2}$
- **III.** $\frac{\text{d}y}{\text{d}x}=y^{2}$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=e^{y}.$

- Equation II is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=y^{2}.$

Therefore, the correct answer is "II only."

## generated authored easy 1 criterion False

Let $y=y(x)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=e^{x}$
- **II.** $\frac{\text{d}y}{\text{d}x}=x^{3}$
- **III.** $\frac{\text{d}y}{\text{d}x}=y^{3}$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=y^{3}.$

Therefore, the correct answer is "III only."

## generated authored easy 1 criterion True

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=e^{x}$
- **II.** $\frac{\text{d}y}{\text{d}x}=x^{3}$
- **III.** $\frac{\text{d}y}{\text{d}x}=y^{3}$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=y^{3}.$

Therefore, the correct answer is "I and II only."

## generated authored moderate 0 criterion False

Let $y=y(x)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $y\frac{\text{d}y}{\text{d}x}+1=2\left(e^{y}\right)$
- **II.** $x\frac{\text{d}y}{\text{d}x}+1=2\left(x^{2}\right)$
- **III.** $y\frac{\text{d}y}{\text{d}x}+1=2\left(y^{2}\right)$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+1 & =2\left(e^{y}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(e^{y}\right)-1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{2 e^{y} - 1}{y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+1 & =2\left(x^{2}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(x^{2}\right)-1}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=2 x - \frac{1}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+1 & =2\left(y^{2}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(y^{2}\right)-1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=2 y - \frac{1}{y}.$

Therefore, the correct answer is "I and III only."

## generated authored moderate 0 criterion True

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $y\frac{\text{d}y}{\text{d}x}+1=2\left(e^{y}\right)$
- **II.** $x\frac{\text{d}y}{\text{d}x}+1=2\left(x^{2}\right)$
- **III.** $y\frac{\text{d}y}{\text{d}x}+1=2\left(y^{2}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+1 & =2\left(e^{y}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(e^{y}\right)-1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{2 e^{y} - 1}{y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+1 & =2\left(x^{2}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(x^{2}\right)-1}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=2 x - \frac{1}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+1 & =2\left(y^{2}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(y^{2}\right)-1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=2 y - \frac{1}{y}.$

Therefore, the correct answer is "II only."

## generated authored moderate 1 criterion False

Let $y=y(x)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(e^{x}\right)$
- **II.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(x^{3}\right)$
- **III.** $y\frac{\text{d}y}{\text{d}x}+2=3\left(y^{3}\right)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(e^{x}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(e^{x}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 e^{x} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(x^{3}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(x^{3}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 x^{3} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+2 & =3\left(y^{3}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(y^{3}\right)-2}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3 y^{3} - 2}{y}.$

Therefore, the correct answer is "III only."

## generated authored moderate 1 criterion True

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(e^{x}\right)$
- **II.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(x^{3}\right)$
- **III.** $y\frac{\text{d}y}{\text{d}x}+2=3\left(y^{3}\right)$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(e^{x}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(e^{x}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 e^{x} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(x^{3}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(x^{3}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 x^{3} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+2 & =3\left(y^{3}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(y^{3}\right)-2}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3 y^{3} - 2}{y}.$

Therefore, the correct answer is "I and II only."

## generated authored hard 0 criterion False

Let $y=y(x)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+2\right)\left(e^{y}+1\right)$
- **II.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+5\right)\left(y^{2}+1\right)$
- **III.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+2\right)\left(y^{2}+1\right)$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+2\right)\left(e^{y}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+2\right)\left(e^{y}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =e^{y} + 1 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=e^{y} + 1.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+5\right)\left(y^{2}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+5\right)\left(y^{2}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 5\right) \left(y^{2} + 1\right)}{x + 2}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+2\right)\left(y^{2}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+2\right)\left(y^{2}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =y^{2} + 1 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=y^{2} + 1.$

Therefore, the correct answer is "I and III only."

## generated authored hard 0 criterion True

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+2\right)\left(e^{y}+1\right)$
- **II.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+5\right)\left(y^{2}+1\right)$
- **III.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+2\right)\left(y^{2}+1\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+2\right)\left(e^{y}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+2\right)\left(e^{y}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =e^{y} + 1 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=e^{y} + 1.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+5\right)\left(y^{2}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+5\right)\left(y^{2}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 5\right) \left(y^{2} + 1\right)}{x + 2}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+2\right)\left(y^{2}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+2\right)\left(y^{2}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =y^{2} + 1 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=y^{2} + 1.$

Therefore, the correct answer is "II only."

## generated authored hard 1 criterion False

Let $y=y(x)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+6\right)\left(e^{y}+2\right)$
- **II.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+6\right)\left(y^{3}+2\right)$
- **III.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+3\right)\left(y^{3}+2\right)$

Correct checkbox values: I=false, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+6\right)\left(e^{y}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+6\right)\left(e^{y}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 6\right) \left(e^{y} + 2\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+6\right)\left(y^{3}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+6\right)\left(y^{3}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 6\right) \left(y^{3} + 2\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+3\right)\left(y^{3}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+3\right)\left(y^{3}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =y^{3} + 2 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=y^{3} + 2.$

Therefore, the correct answer is "III only."

## generated authored hard 1 criterion True

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+6\right)\left(e^{y}+2\right)$
- **II.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+6\right)\left(y^{3}+2\right)$
- **III.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+3\right)\left(y^{3}+2\right)$

Correct checkbox values: I=true, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+6\right)\left(e^{y}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+6\right)\left(e^{y}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 6\right) \left(e^{y} + 2\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+6\right)\left(y^{3}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+6\right)\left(y^{3}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 6\right) \left(y^{3} + 2\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+3\right)\left(y^{3}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+3\right)\left(y^{3}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =y^{3} + 2 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=y^{3} + 2.$

Therefore, the correct answer is "I and II only."

## generated authored binding easy xy leibniz

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=\ln{\left(x \right)}$
- **II.** $\frac{\text{d}y}{\text{d}x}=\ln{\left(y \right)}$
- **III.** $\frac{\text{d}y}{\text{d}x}=\sqrt{y}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=\ln{\left(y \right)}.$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=\sqrt{y}.$

Therefore, the correct answer is "I only."

## generated authored binding easy xy prime

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{'}=\ln{\left(x \right)}$
- **II.** ${y}^{'}=\ln{\left(y \right)}$
- **III.** ${y}^{'}=\sqrt{y}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form ${y}^{'}=f(y).$

- Equation II is an autonomous differential equation. We see that it is of the form ${y}^{'}=f(y),$ where $f(y)=\ln{\left(y \right)}.$

- Equation III is an autonomous differential equation. We see that it is of the form ${y}^{'}=f(y),$ where $f(y)=\sqrt{y}.$

Therefore, the correct answer is "I only."

## generated authored binding easy tu leibniz

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}u}{\text{d}t}=\ln{\left(t \right)}$
- **II.** $\frac{\text{d}u}{\text{d}t}=\ln{\left(u \right)}$
- **III.** $\frac{\text{d}u}{\text{d}t}=\sqrt{u}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form $\frac{\text{d}u}{\text{d}t}=f(u).$

- Equation II is an autonomous differential equation. We see that it is of the form $\frac{\text{d}u}{\text{d}t}=f(u),$ where $f(u)=\ln{\left(u \right)}.$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}u}{\text{d}t}=f(u),$ where $f(u)=\sqrt{u}.$

Therefore, the correct answer is "I only."

## generated authored binding easy tu prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${u}^{'}=\ln{\left(t \right)}$
- **II.** ${u}^{'}=\ln{\left(u \right)}$
- **III.** ${u}^{'}=\sqrt{u}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form ${u}^{'}=f(u).$

- Equation II is an autonomous differential equation. We see that it is of the form ${u}^{'}=f(u),$ where $f(u)=\ln{\left(u \right)}.$

- Equation III is an autonomous differential equation. We see that it is of the form ${u}^{'}=f(u),$ where $f(u)=\sqrt{u}.$

Therefore, the correct answer is "I only."

## generated authored binding easy sv leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}v}{\text{d}s}=\ln{\left(s \right)}$
- **II.** $\frac{\text{d}v}{\text{d}s}=\ln{\left(v \right)}$
- **III.** $\frac{\text{d}v}{\text{d}s}=\sqrt{v}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is an autonomous differential equation. We see that it is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)=\ln{\left(v \right)}.$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}v}{\text{d}s}=f(v),$ where $f(v)=\sqrt{v}.$

Therefore, the correct answer is "I only."

## generated authored binding easy sv prime

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${v}^{'}=\ln{\left(s \right)}$
- **II.** ${v}^{'}=\ln{\left(v \right)}$
- **III.** ${v}^{'}=\sqrt{v}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form ${v}^{'}=f(v).$

- Equation II is an autonomous differential equation. We see that it is of the form ${v}^{'}=f(v),$ where $f(v)=\ln{\left(v \right)}.$

- Equation III is an autonomous differential equation. We see that it is of the form ${v}^{'}=f(v),$ where $f(v)=\sqrt{v}.$

Therefore, the correct answer is "I only."

## generated authored binding easy ty leibniz

Let $y=y(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}t}=\ln{\left(t \right)}$
- **II.** $\frac{\text{d}y}{\text{d}t}=\ln{\left(y \right)}$
- **III.** $\frac{\text{d}y}{\text{d}t}=\sqrt{y}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}t}=f(y).$

- Equation II is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}t}=f(y),$ where $f(y)=\ln{\left(y \right)}.$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}t}=f(y),$ where $f(y)=\sqrt{y}.$

Therefore, the correct answer is "I only."

## generated authored binding easy ty prime

Let $y=y(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{'}=\ln{\left(t \right)}$
- **II.** ${y}^{'}=\ln{\left(y \right)}$
- **III.** ${y}^{'}=\sqrt{y}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. It is not of the form ${y}^{'}=f(y).$

- Equation II is an autonomous differential equation. We see that it is of the form ${y}^{'}=f(y),$ where $f(y)=\ln{\left(y \right)}.$

- Equation III is an autonomous differential equation. We see that it is of the form ${y}^{'}=f(y),$ where $f(y)=\sqrt{y}.$

Therefore, the correct answer is "I only."

## generated authored binding moderate xy leibniz

Let $y=y(x)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(\cos{\left(x \right)}\right)$
- **II.** $y\frac{\text{d}y}{\text{d}x}+2=3\left(\cos{\left(y \right)}\right)$
- **III.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(\sin{\left(x \right)}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(\cos{\left(x \right)}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(\cos{\left(x \right)}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 \cos{\left(x \right)} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+2 & =3\left(\cos{\left(y \right)}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(\cos{\left(y \right)}\right)-2}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3 \cos{\left(y \right)} - 2}{y}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(\sin{\left(x \right)}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(\sin{\left(x \right)}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 \sin{\left(x \right)} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "II only."

## generated authored binding moderate xy prime

Let $y=y(x)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $x{y}^{'}+2=3\left(\cos{\left(x \right)}\right)$
- **II.** $y{y}^{'}+2=3\left(\cos{\left(y \right)}\right)$
- **III.** $x{y}^{'}+2=3\left(\sin{\left(x \right)}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x{y}^{'}+2 & =3\left(\cos{\left(x \right)}\right) \\ {y}^{'} & =\frac{3\left(\cos{\left(x \right)}\right)-2}{x} \\ {y}^{'} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 \cos{\left(x \right)} - 2}{x}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}y{y}^{'}+2 & =3\left(\cos{\left(y \right)}\right) \\ {y}^{'} & =\frac{3\left(\cos{\left(y \right)}\right)-2}{y} \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3 \cos{\left(y \right)} - 2}{y}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x{y}^{'}+2 & =3\left(\sin{\left(x \right)}\right) \\ {y}^{'} & =\frac{3\left(\sin{\left(x \right)}\right)-2}{x} \\ {y}^{'} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 \sin{\left(x \right)} - 2}{x}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

Therefore, the correct answer is "II only."

## generated authored binding moderate tu leibniz

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $t\frac{\text{d}u}{\text{d}t}+2=3\left(\cos{\left(t \right)}\right)$
- **II.** $u\frac{\text{d}u}{\text{d}t}+2=3\left(\cos{\left(u \right)}\right)$
- **III.** $t\frac{\text{d}u}{\text{d}t}+2=3\left(\sin{\left(t \right)}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t\frac{\text{d}u}{\text{d}t}+2 & =3\left(\cos{\left(t \right)}\right) \\ \frac{\text{d}u}{\text{d}t} & =\frac{3\left(\cos{\left(t \right)}\right)-2}{t} \\ \frac{\text{d}u}{\text{d}t} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{3 \cos{\left(t \right)} - 2}{t}.$ So, it is not possible to write the equation in the form $\frac{\text{d}u}{\text{d}t}=f(u).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ we get

$$
\begin{aligned}u\frac{\text{d}u}{\text{d}t}+2 & =3\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}u}{\text{d}t} & =\frac{3\left(\cos{\left(u \right)}\right)-2}{u} \\ \frac{\text{d}u}{\text{d}t} & =f(u)\end{aligned}
$$

where $f(u)=\frac{3 \cos{\left(u \right)} - 2}{u}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t\frac{\text{d}u}{\text{d}t}+2 & =3\left(\sin{\left(t \right)}\right) \\ \frac{\text{d}u}{\text{d}t} & =\frac{3\left(\sin{\left(t \right)}\right)-2}{t} \\ \frac{\text{d}u}{\text{d}t} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{3 \sin{\left(t \right)} - 2}{t}.$ So, it is not possible to write the equation in the form $\frac{\text{d}u}{\text{d}t}=f(u).$

Therefore, the correct answer is "II only."

## generated authored binding moderate tu prime

Let $u=u(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $t{u}^{'}+2=3\left(\cos{\left(t \right)}\right)$
- **II.** $u{u}^{'}+2=3\left(\cos{\left(u \right)}\right)$
- **III.** $t{u}^{'}+2=3\left(\sin{\left(t \right)}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t{u}^{'}+2 & =3\left(\cos{\left(t \right)}\right) \\ {u}^{'} & =\frac{3\left(\cos{\left(t \right)}\right)-2}{t} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{3 \cos{\left(t \right)} - 2}{t}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}u{u}^{'}+2 & =3\left(\cos{\left(u \right)}\right) \\ {u}^{'} & =\frac{3\left(\cos{\left(u \right)}\right)-2}{u} \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\frac{3 \cos{\left(u \right)} - 2}{u}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t{u}^{'}+2 & =3\left(\sin{\left(t \right)}\right) \\ {u}^{'} & =\frac{3\left(\sin{\left(t \right)}\right)-2}{t} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{3 \sin{\left(t \right)} - 2}{t}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

Therefore, the correct answer is "II only."

## generated authored binding moderate sv leibniz

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $s\frac{\text{d}v}{\text{d}s}+2=3\left(\cos{\left(s \right)}\right)$
- **II.** $v\frac{\text{d}v}{\text{d}s}+2=3\left(\cos{\left(v \right)}\right)$
- **III.** $s\frac{\text{d}v}{\text{d}s}+2=3\left(\sin{\left(s \right)}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}s\frac{\text{d}v}{\text{d}s}+2 & =3\left(\cos{\left(s \right)}\right) \\ \frac{\text{d}v}{\text{d}s} & =\frac{3\left(\cos{\left(s \right)}\right)-2}{s} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{3 \cos{\left(s \right)} - 2}{s}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}v\frac{\text{d}v}{\text{d}s}+2 & =3\left(\cos{\left(v \right)}\right) \\ \frac{\text{d}v}{\text{d}s} & =\frac{3\left(\cos{\left(v \right)}\right)-2}{v} \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\frac{3 \cos{\left(v \right)} - 2}{v}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}s\frac{\text{d}v}{\text{d}s}+2 & =3\left(\sin{\left(s \right)}\right) \\ \frac{\text{d}v}{\text{d}s} & =\frac{3\left(\sin{\left(s \right)}\right)-2}{s} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{3 \sin{\left(s \right)} - 2}{s}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

Therefore, the correct answer is "II only."

## generated authored binding moderate sv prime

Let $v=v(s)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $s{v}^{'}+2=3\left(\cos{\left(s \right)}\right)$
- **II.** $v{v}^{'}+2=3\left(\cos{\left(v \right)}\right)$
- **III.** $s{v}^{'}+2=3\left(\sin{\left(s \right)}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}s{v}^{'}+2 & =3\left(\cos{\left(s \right)}\right) \\ {v}^{'} & =\frac{3\left(\cos{\left(s \right)}\right)-2}{s} \\ {v}^{'} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{3 \cos{\left(s \right)} - 2}{s}.$ So, it is not possible to write the equation in the form ${v}^{'}=f(v).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${v}^{'}=f(v),$ we get

$$
\begin{aligned}v{v}^{'}+2 & =3\left(\cos{\left(v \right)}\right) \\ {v}^{'} & =\frac{3\left(\cos{\left(v \right)}\right)-2}{v} \\ {v}^{'} & =f(v)\end{aligned}
$$

where $f(v)=\frac{3 \cos{\left(v \right)} - 2}{v}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}s{v}^{'}+2 & =3\left(\sin{\left(s \right)}\right) \\ {v}^{'} & =\frac{3\left(\sin{\left(s \right)}\right)-2}{s} \\ {v}^{'} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{3 \sin{\left(s \right)} - 2}{s}.$ So, it is not possible to write the equation in the form ${v}^{'}=f(v).$

Therefore, the correct answer is "II only."

## generated authored binding moderate ty leibniz

Let $y=y(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $t\frac{\text{d}y}{\text{d}t}+2=3\left(\cos{\left(t \right)}\right)$
- **II.** $y\frac{\text{d}y}{\text{d}t}+2=3\left(\cos{\left(y \right)}\right)$
- **III.** $t\frac{\text{d}y}{\text{d}t}+2=3\left(\sin{\left(t \right)}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t\frac{\text{d}y}{\text{d}t}+2 & =3\left(\cos{\left(t \right)}\right) \\ \frac{\text{d}y}{\text{d}t} & =\frac{3\left(\cos{\left(t \right)}\right)-2}{t} \\ \frac{\text{d}y}{\text{d}t} & =f(t,y)\end{aligned}
$$

where $f(t,y)=\frac{3 \cos{\left(t \right)} - 2}{t}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}t}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}t}+2 & =3\left(\cos{\left(y \right)}\right) \\ \frac{\text{d}y}{\text{d}t} & =\frac{3\left(\cos{\left(y \right)}\right)-2}{y} \\ \frac{\text{d}y}{\text{d}t} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3 \cos{\left(y \right)} - 2}{y}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t\frac{\text{d}y}{\text{d}t}+2 & =3\left(\sin{\left(t \right)}\right) \\ \frac{\text{d}y}{\text{d}t} & =\frac{3\left(\sin{\left(t \right)}\right)-2}{t} \\ \frac{\text{d}y}{\text{d}t} & =f(t,y)\end{aligned}
$$

where $f(t,y)=\frac{3 \sin{\left(t \right)} - 2}{t}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}t}=f(y).$

Therefore, the correct answer is "II only."

## generated authored binding moderate ty prime

Let $y=y(t)$.

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $t{y}^{'}+2=3\left(\cos{\left(t \right)}\right)$
- **II.** $y{y}^{'}+2=3\left(\cos{\left(y \right)}\right)$
- **III.** $t{y}^{'}+2=3\left(\sin{\left(t \right)}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t{y}^{'}+2 & =3\left(\cos{\left(t \right)}\right) \\ {y}^{'} & =\frac{3\left(\cos{\left(t \right)}\right)-2}{t} \\ {y}^{'} & =f(t,y)\end{aligned}
$$

where $f(t,y)=\frac{3 \cos{\left(t \right)} - 2}{t}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}y{y}^{'}+2 & =3\left(\cos{\left(y \right)}\right) \\ {y}^{'} & =\frac{3\left(\cos{\left(y \right)}\right)-2}{y} \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3 \cos{\left(y \right)} - 2}{y}.$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}t{y}^{'}+2 & =3\left(\sin{\left(t \right)}\right) \\ {y}^{'} & =\frac{3\left(\sin{\left(t \right)}\right)-2}{t} \\ {y}^{'} & =f(t,y)\end{aligned}
$$

where $f(t,y)=\frac{3 \sin{\left(t \right)} - 2}{t}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

Therefore, the correct answer is "II only."

## generated authored binding hard xy leibniz

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+5\right)\left(\sin{\left(y \right)}+4\right)$
- **II.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+3\right)\left(\sin{\left(y \right)}+4\right)$
- **III.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+3\right)\left(\sqrt{y}+4\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+5\right)\left(\sin{\left(y \right)}+4\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+5\right)\left(\sin{\left(y \right)}+4\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 5\right) \left(\sin{\left(y \right)} + 4\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+3\right)\left(\sin{\left(y \right)}+4\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+3\right)\left(\sin{\left(y \right)}+4\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =\sin{\left(y \right)} + 4 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\sin{\left(y \right)} + 4.$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+3\right)\left(\sqrt{y}+4\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+3\right)\left(\sqrt{y}+4\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =\sqrt{y} + 4 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\sqrt{y} + 4.$

Therefore, the correct answer is "I only."

## generated authored binding hard xy prime

Let $y=y(x)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+3\right){y}^{'}=\left(x+5\right)\left(\sin{\left(y \right)}+4\right)$
- **II.** $\left(x+3\right){y}^{'}=\left(x+3\right)\left(\sin{\left(y \right)}+4\right)$
- **III.** $\left(x+3\right){y}^{'}=\left(x+3\right)\left(\sqrt{y}+4\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right){y}^{'} & =\left(x+5\right)\left(\sin{\left(y \right)}+4\right) \\ {y}^{'} & =\frac{\left(x+5\right)\left(\sin{\left(y \right)}+4\right)}{\left(x+3\right)} \\ {y}^{'} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 5\right) \left(\sin{\left(y \right)} + 4\right)}{x + 3}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}\left(x+3\right){y}^{'} & =\left(x+3\right)\left(\sin{\left(y \right)}+4\right) \\ {y}^{'} & =\frac{\left(x+3\right)\left(\sin{\left(y \right)}+4\right)}{\left(x+3\right)} \\ {y}^{'} & =\sin{\left(y \right)} + 4 \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\sin{\left(y \right)} + 4.$

- Equation III is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}\left(x+3\right){y}^{'} & =\left(x+3\right)\left(\sqrt{y}+4\right) \\ {y}^{'} & =\frac{\left(x+3\right)\left(\sqrt{y}+4\right)}{\left(x+3\right)} \\ {y}^{'} & =\sqrt{y} + 4 \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\sqrt{y} + 4.$

Therefore, the correct answer is "I only."

## generated authored binding hard tu leibniz

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(t+3\right)\frac{\text{d}u}{\text{d}t}=\left(t+5\right)\left(\sin{\left(u \right)}+4\right)$
- **II.** $\left(t+3\right)\frac{\text{d}u}{\text{d}t}=\left(t+3\right)\left(\sin{\left(u \right)}+4\right)$
- **III.** $\left(t+3\right)\frac{\text{d}u}{\text{d}t}=\left(t+3\right)\left(\sqrt{u}+4\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(t+3\right)\frac{\text{d}u}{\text{d}t} & =\left(t+5\right)\left(\sin{\left(u \right)}+4\right) \\ \frac{\text{d}u}{\text{d}t} & =\frac{\left(t+5\right)\left(\sin{\left(u \right)}+4\right)}{\left(t+3\right)} \\ \frac{\text{d}u}{\text{d}t} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{\left(t + 5\right) \left(\sin{\left(u \right)} + 4\right)}{t + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}u}{\text{d}t}=f(u).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ we get

$$
\begin{aligned}\left(t+3\right)\frac{\text{d}u}{\text{d}t} & =\left(t+3\right)\left(\sin{\left(u \right)}+4\right) \\ \frac{\text{d}u}{\text{d}t} & =\frac{\left(t+3\right)\left(\sin{\left(u \right)}+4\right)}{\left(t+3\right)} \\ \frac{\text{d}u}{\text{d}t} & =\sin{\left(u \right)} + 4 \\ \frac{\text{d}u}{\text{d}t} & =f(u)\end{aligned}
$$

where $f(u)=\sin{\left(u \right)} + 4.$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ we get

$$
\begin{aligned}\left(t+3\right)\frac{\text{d}u}{\text{d}t} & =\left(t+3\right)\left(\sqrt{u}+4\right) \\ \frac{\text{d}u}{\text{d}t} & =\frac{\left(t+3\right)\left(\sqrt{u}+4\right)}{\left(t+3\right)} \\ \frac{\text{d}u}{\text{d}t} & =\sqrt{u} + 4 \\ \frac{\text{d}u}{\text{d}t} & =f(u)\end{aligned}
$$

where $f(u)=\sqrt{u} + 4.$

Therefore, the correct answer is "I only."

## generated authored binding hard tu prime

Let $u=u(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(t+3\right){u}^{'}=\left(t+5\right)\left(\sin{\left(u \right)}+4\right)$
- **II.** $\left(t+3\right){u}^{'}=\left(t+3\right)\left(\sin{\left(u \right)}+4\right)$
- **III.** $\left(t+3\right){u}^{'}=\left(t+3\right)\left(\sqrt{u}+4\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $u$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}u}{\text{d}t}=f(u),$ or equivalently, ${u}^{′}=f(u).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(t+3\right){u}^{'} & =\left(t+5\right)\left(\sin{\left(u \right)}+4\right) \\ {u}^{'} & =\frac{\left(t+5\right)\left(\sin{\left(u \right)}+4\right)}{\left(t+3\right)} \\ {u}^{'} & =f(t,u)\end{aligned}
$$

where $f(t,u)=\frac{\left(t + 5\right) \left(\sin{\left(u \right)} + 4\right)}{t + 3}.$ So, it is not possible to write the equation in the form ${u}^{'}=f(u).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}\left(t+3\right){u}^{'} & =\left(t+3\right)\left(\sin{\left(u \right)}+4\right) \\ {u}^{'} & =\frac{\left(t+3\right)\left(\sin{\left(u \right)}+4\right)}{\left(t+3\right)} \\ {u}^{'} & =\sin{\left(u \right)} + 4 \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\sin{\left(u \right)} + 4.$

- Equation III is an autonomous differential equation. Writing the equation in the form ${u}^{'}=f(u),$ we get

$$
\begin{aligned}\left(t+3\right){u}^{'} & =\left(t+3\right)\left(\sqrt{u}+4\right) \\ {u}^{'} & =\frac{\left(t+3\right)\left(\sqrt{u}+4\right)}{\left(t+3\right)} \\ {u}^{'} & =\sqrt{u} + 4 \\ {u}^{'} & =f(u)\end{aligned}
$$

where $f(u)=\sqrt{u} + 4.$

Therefore, the correct answer is "I only."

## generated authored binding hard sv leibniz

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(s+3\right)\frac{\text{d}v}{\text{d}s}=\left(s+5\right)\left(\sin{\left(v \right)}+4\right)$
- **II.** $\left(s+3\right)\frac{\text{d}v}{\text{d}s}=\left(s+3\right)\left(\sin{\left(v \right)}+4\right)$
- **III.** $\left(s+3\right)\frac{\text{d}v}{\text{d}s}=\left(s+3\right)\left(\sqrt{v}+4\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(s+3\right)\frac{\text{d}v}{\text{d}s} & =\left(s+5\right)\left(\sin{\left(v \right)}+4\right) \\ \frac{\text{d}v}{\text{d}s} & =\frac{\left(s+5\right)\left(\sin{\left(v \right)}+4\right)}{\left(s+3\right)} \\ \frac{\text{d}v}{\text{d}s} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{\left(s + 5\right) \left(\sin{\left(v \right)} + 4\right)}{s + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\left(s+3\right)\frac{\text{d}v}{\text{d}s} & =\left(s+3\right)\left(\sin{\left(v \right)}+4\right) \\ \frac{\text{d}v}{\text{d}s} & =\frac{\left(s+3\right)\left(\sin{\left(v \right)}+4\right)}{\left(s+3\right)} \\ \frac{\text{d}v}{\text{d}s} & =\sin{\left(v \right)} + 4 \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\sin{\left(v \right)} + 4.$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ we get

$$
\begin{aligned}\left(s+3\right)\frac{\text{d}v}{\text{d}s} & =\left(s+3\right)\left(\sqrt{v}+4\right) \\ \frac{\text{d}v}{\text{d}s} & =\frac{\left(s+3\right)\left(\sqrt{v}+4\right)}{\left(s+3\right)} \\ \frac{\text{d}v}{\text{d}s} & =\sqrt{v} + 4 \\ \frac{\text{d}v}{\text{d}s} & =f(v)\end{aligned}
$$

where $f(v)=\sqrt{v} + 4.$

Therefore, the correct answer is "I only."

## generated authored binding hard sv prime

Let $v=v(s)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(s+3\right){v}^{'}=\left(s+5\right)\left(\sin{\left(v \right)}+4\right)$
- **II.** $\left(s+3\right){v}^{'}=\left(s+3\right)\left(\sin{\left(v \right)}+4\right)$
- **III.** $\left(s+3\right){v}^{'}=\left(s+3\right)\left(\sqrt{v}+4\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $v$ and independent variable $s$ is said to be autonomous if it can be written in the form $\frac{\text{d}v}{\text{d}s}=f(v),$ or equivalently, ${v}^{′}=f(v).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(s+3\right){v}^{'} & =\left(s+5\right)\left(\sin{\left(v \right)}+4\right) \\ {v}^{'} & =\frac{\left(s+5\right)\left(\sin{\left(v \right)}+4\right)}{\left(s+3\right)} \\ {v}^{'} & =f(s,v)\end{aligned}
$$

where $f(s,v)=\frac{\left(s + 5\right) \left(\sin{\left(v \right)} + 4\right)}{s + 3}.$ So, it is not possible to write the equation in the form ${v}^{'}=f(v).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${v}^{'}=f(v),$ we get

$$
\begin{aligned}\left(s+3\right){v}^{'} & =\left(s+3\right)\left(\sin{\left(v \right)}+4\right) \\ {v}^{'} & =\frac{\left(s+3\right)\left(\sin{\left(v \right)}+4\right)}{\left(s+3\right)} \\ {v}^{'} & =\sin{\left(v \right)} + 4 \\ {v}^{'} & =f(v)\end{aligned}
$$

where $f(v)=\sin{\left(v \right)} + 4.$

- Equation III is an autonomous differential equation. Writing the equation in the form ${v}^{'}=f(v),$ we get

$$
\begin{aligned}\left(s+3\right){v}^{'} & =\left(s+3\right)\left(\sqrt{v}+4\right) \\ {v}^{'} & =\frac{\left(s+3\right)\left(\sqrt{v}+4\right)}{\left(s+3\right)} \\ {v}^{'} & =\sqrt{v} + 4 \\ {v}^{'} & =f(v)\end{aligned}
$$

where $f(v)=\sqrt{v} + 4.$

Therefore, the correct answer is "I only."

## generated authored binding hard ty leibniz

Let $y=y(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(t+3\right)\frac{\text{d}y}{\text{d}t}=\left(t+5\right)\left(\sin{\left(y \right)}+4\right)$
- **II.** $\left(t+3\right)\frac{\text{d}y}{\text{d}t}=\left(t+3\right)\left(\sin{\left(y \right)}+4\right)$
- **III.** $\left(t+3\right)\frac{\text{d}y}{\text{d}t}=\left(t+3\right)\left(\sqrt{y}+4\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(t+3\right)\frac{\text{d}y}{\text{d}t} & =\left(t+5\right)\left(\sin{\left(y \right)}+4\right) \\ \frac{\text{d}y}{\text{d}t} & =\frac{\left(t+5\right)\left(\sin{\left(y \right)}+4\right)}{\left(t+3\right)} \\ \frac{\text{d}y}{\text{d}t} & =f(t,y)\end{aligned}
$$

where $f(t,y)=\frac{\left(t + 5\right) \left(\sin{\left(y \right)} + 4\right)}{t + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}t}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ we get

$$
\begin{aligned}\left(t+3\right)\frac{\text{d}y}{\text{d}t} & =\left(t+3\right)\left(\sin{\left(y \right)}+4\right) \\ \frac{\text{d}y}{\text{d}t} & =\frac{\left(t+3\right)\left(\sin{\left(y \right)}+4\right)}{\left(t+3\right)} \\ \frac{\text{d}y}{\text{d}t} & =\sin{\left(y \right)} + 4 \\ \frac{\text{d}y}{\text{d}t} & =f(y)\end{aligned}
$$

where $f(y)=\sin{\left(y \right)} + 4.$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ we get

$$
\begin{aligned}\left(t+3\right)\frac{\text{d}y}{\text{d}t} & =\left(t+3\right)\left(\sqrt{y}+4\right) \\ \frac{\text{d}y}{\text{d}t} & =\frac{\left(t+3\right)\left(\sqrt{y}+4\right)}{\left(t+3\right)} \\ \frac{\text{d}y}{\text{d}t} & =\sqrt{y} + 4 \\ \frac{\text{d}y}{\text{d}t} & =f(y)\end{aligned}
$$

where $f(y)=\sqrt{y} + 4.$

Therefore, the correct answer is "I only."

## generated authored binding hard ty prime

Let $y=y(t)$.

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(t+3\right){y}^{'}=\left(t+5\right)\left(\sin{\left(y \right)}+4\right)$
- **II.** $\left(t+3\right){y}^{'}=\left(t+3\right)\left(\sin{\left(y \right)}+4\right)$
- **III.** $\left(t+3\right){y}^{'}=\left(t+3\right)\left(\sqrt{y}+4\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $t$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}t}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(t+3\right){y}^{'} & =\left(t+5\right)\left(\sin{\left(y \right)}+4\right) \\ {y}^{'} & =\frac{\left(t+5\right)\left(\sin{\left(y \right)}+4\right)}{\left(t+3\right)} \\ {y}^{'} & =f(t,y)\end{aligned}
$$

where $f(t,y)=\frac{\left(t + 5\right) \left(\sin{\left(y \right)} + 4\right)}{t + 3}.$ So, it is not possible to write the equation in the form ${y}^{'}=f(y).$

- Equation II is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}\left(t+3\right){y}^{'} & =\left(t+3\right)\left(\sin{\left(y \right)}+4\right) \\ {y}^{'} & =\frac{\left(t+3\right)\left(\sin{\left(y \right)}+4\right)}{\left(t+3\right)} \\ {y}^{'} & =\sin{\left(y \right)} + 4 \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\sin{\left(y \right)} + 4.$

- Equation III is an autonomous differential equation. Writing the equation in the form ${y}^{'}=f(y),$ we get

$$
\begin{aligned}\left(t+3\right){y}^{'} & =\left(t+3\right)\left(\sqrt{y}+4\right) \\ {y}^{'} & =\frac{\left(t+3\right)\left(\sqrt{y}+4\right)}{\left(t+3\right)} \\ {y}^{'} & =\sqrt{y} + 4 \\ {y}^{'} & =f(y)\end{aligned}
$$

where $f(y)=\sqrt{y} + 4.$

Therefore, the correct answer is "I only."
