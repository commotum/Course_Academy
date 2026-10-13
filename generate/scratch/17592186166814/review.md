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

## generated authored easy 0 criterion False

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=y^{2}$
- **II.** $\frac{\text{d}y}{\text{d}x}=x^{2}$
- **III.** $\frac{\text{d}y}{\text{d}x}=e^{y}$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=y^{2}.$

- Equation II is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=e^{y}.$

Therefore, the correct answer is "I and III only."

## generated authored easy 0 criterion True

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=y^{2}$
- **II.** $\frac{\text{d}y}{\text{d}x}=x^{2}$
- **III.** $\frac{\text{d}y}{\text{d}x}=e^{y}$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=y^{2}.$

- Equation II is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=e^{y}.$

Therefore, the correct answer is "II only."

## generated authored easy 1 criterion False

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=y^{3}$
- **II.** $\frac{\text{d}y}{\text{d}x}=x^{3}$
- **III.** $\frac{\text{d}y}{\text{d}x}=e^{x}$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=y^{3}.$

- Equation II is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "I only."

## generated authored easy 1 criterion True

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}=y^{3}$
- **II.** $\frac{\text{d}y}{\text{d}x}=x^{3}$
- **III.** $\frac{\text{d}y}{\text{d}x}=e^{x}$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. We see that it is of the form $\frac{\text{d}y}{\text{d}x}=f(y),$ where $f(y)=y^{3}.$

- Equation II is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is not an autonomous differential equation. It is not of the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "II and III only."

## generated authored moderate 0 criterion False

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $y\frac{\text{d}y}{\text{d}x}+1=2\left(y^{2}\right)$
- **II.** $x\frac{\text{d}y}{\text{d}x}+1=2\left(x^{2}\right)$
- **III.** $y\frac{\text{d}y}{\text{d}x}+1=2\left(e^{y}\right)$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+1 & =2\left(y^{2}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(y^{2}\right)-1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=2 y - \frac{1}{y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+1 & =2\left(x^{2}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(x^{2}\right)-1}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=2 x - \frac{1}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+1 & =2\left(e^{y}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(e^{y}\right)-1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{2 e^{y} - 1}{y}.$

Therefore, the correct answer is "I and III only."

## generated authored moderate 0 criterion True

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $y\frac{\text{d}y}{\text{d}x}+1=2\left(y^{2}\right)$
- **II.** $x\frac{\text{d}y}{\text{d}x}+1=2\left(x^{2}\right)$
- **III.** $y\frac{\text{d}y}{\text{d}x}+1=2\left(e^{y}\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+1 & =2\left(y^{2}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(y^{2}\right)-1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=2 y - \frac{1}{y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+1 & =2\left(x^{2}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(x^{2}\right)-1}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=2 x - \frac{1}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+1 & =2\left(e^{y}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{2\left(e^{y}\right)-1}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{2 e^{y} - 1}{y}.$

Therefore, the correct answer is "II only."

## generated authored moderate 1 criterion False

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $y\frac{\text{d}y}{\text{d}x}+2=3\left(y^{3}\right)$
- **II.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(x^{3}\right)$
- **III.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(e^{x}\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+2 & =3\left(y^{3}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(y^{3}\right)-2}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3 y^{3} - 2}{y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(x^{3}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(x^{3}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 x^{3} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(e^{x}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(e^{x}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 e^{x} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "I only."

## generated authored moderate 1 criterion True

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $y\frac{\text{d}y}{\text{d}x}+2=3\left(y^{3}\right)$
- **II.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(x^{3}\right)$
- **III.** $x\frac{\text{d}y}{\text{d}x}+2=3\left(e^{x}\right)$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+2 & =3\left(y^{3}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(y^{3}\right)-2}{y} \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=\frac{3 y^{3} - 2}{y}.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(x^{3}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(x^{3}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 x^{3} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}x\frac{\text{d}y}{\text{d}x}+2 & =3\left(e^{x}\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{3\left(e^{x}\right)-2}{x} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{3 e^{x} - 2}{x}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "II and III only."

## generated authored hard 0 criterion False

Which of the following are autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+2\right)\left(y^{2}+1\right)$
- **II.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+5\right)\left(y^{2}+1\right)$
- **III.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+2\right)\left(e^{y}+1\right)$

Correct checkbox values: I=true, II=false, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+2\right)\left(y^{2}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+2\right)\left(y^{2}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =y^{2} + 1 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=y^{2} + 1.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+5\right)\left(y^{2}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+5\right)\left(y^{2}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 5\right) \left(y^{2} + 1\right)}{x + 2}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+2\right)\left(e^{y}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+2\right)\left(e^{y}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =e^{y} + 1 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=e^{y} + 1.$

Therefore, the correct answer is "I and III only."

## generated authored hard 0 criterion True

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+2\right)\left(y^{2}+1\right)$
- **II.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+5\right)\left(y^{2}+1\right)$
- **III.** $\left(x+2\right)\frac{\text{d}y}{\text{d}x}=\left(x+2\right)\left(e^{y}+1\right)$

Correct checkbox values: I=false, II=true, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+2\right)\left(y^{2}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+2\right)\left(y^{2}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =y^{2} + 1 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=y^{2} + 1.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+5\right)\left(y^{2}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+5\right)\left(y^{2}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 5\right) \left(y^{2} + 1\right)}{x + 2}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+2\right)\frac{\text{d}y}{\text{d}x} & =\left(x+2\right)\left(e^{y}+1\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+2\right)\left(e^{y}+1\right)}{\left(x+2\right)} \\ \frac{\text{d}y}{\text{d}x} & =e^{y} + 1 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=e^{y} + 1.$

Therefore, the correct answer is "II only."

## generated authored hard 1 criterion False

Which of the following are autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+3\right)\left(y^{3}+2\right)$
- **II.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+6\right)\left(y^{3}+2\right)$
- **III.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+6\right)\left(e^{y}+2\right)$

Correct checkbox values: I=true, II=false, III=false

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+3\right)\left(y^{3}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+3\right)\left(y^{3}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =y^{3} + 2 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=y^{3} + 2.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+6\right)\left(y^{3}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+6\right)\left(y^{3}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 6\right) \left(y^{3} + 2\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+6\right)\left(e^{y}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+6\right)\left(e^{y}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 6\right) \left(e^{y} + 2\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "I only."

## generated authored hard 1 criterion True

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

Consider intervals where the coefficients of the derivative are nonzero.

- **I.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+3\right)\left(y^{3}+2\right)$
- **II.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+6\right)\left(y^{3}+2\right)$
- **III.** $\left(x+3\right)\frac{\text{d}y}{\text{d}x}=\left(x+6\right)\left(e^{y}+2\right)$

Correct checkbox values: I=false, II=true, III=true

An ordinary differential equation with dependent variable $y$ and independent variable $x$ is said to be autonomous if it can be written in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ or equivalently, ${y}^{′}=f(y).$

With that in mind, let's check each of the differential equations:

- Equation I is an autonomous differential equation. Writing the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y),$ we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+3\right)\left(y^{3}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+3\right)\left(y^{3}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =y^{3} + 2 \\ \frac{\text{d}y}{\text{d}x} & =f(y)\end{aligned}
$$

where $f(y)=y^{3} + 2.$

- Equation II is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+6\right)\left(y^{3}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+6\right)\left(y^{3}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 6\right) \left(y^{3} + 2\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

- Equation III is not an autonomous differential equation. If we isolate the derivative term, we get

$$
\begin{aligned}\left(x+3\right)\frac{\text{d}y}{\text{d}x} & =\left(x+6\right)\left(e^{y}+2\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\left(x+6\right)\left(e^{y}+2\right)}{\left(x+3\right)} \\ \frac{\text{d}y}{\text{d}x} & =f(x,y)\end{aligned}
$$

where $f(x,y)=\frac{\left(x + 6\right) \left(e^{y} + 2\right)}{x + 3}.$ So, it is not possible to write the equation in the form $\frac{\text{d}y}{\text{d}x}=f(y).$

Therefore, the correct answer is "II and III only."
