# Cartesian-equation rebuild review

KP `17592186100890`; source basis `1356`; draft version `trig-cartesian-guide-draft-4`.

All 20 source questions are shown, each with two generated variants using the same complete bank profile or blank template. All 14 observed radio bank profiles are represented. Moderate source replay retains their banks; normal moderate generation uses four authored variation banks, positive coefficients, and single-quadrant intervals. These are variations at one difficulty with no instructional sequence. Domain restrictions are author metadata. Source mathematical content is retained; choice escaping is normalized for display.

# ellipse_sin_radio / sin_shift_exchange

## Original source — Easy — q-15751

Find the Cartesian equation of the curve defined parametrically as 

$$
x=2\operatorname{sin}⁡t-1,\,\,\,y=5\operatorname{cos}⁡t+4,\,t\in [0,2\pi ).
$$

- **A.** ${(\frac{x+1}{2})}^{2}+{(\frac{y-4}{5})}^{2}=1$
- **B.** ${(\frac{x-1}{2})}^{2}+{(\frac{y+4}{5})}^{2}=1$
- **C.** ${(\frac{x+4}{5})}^{2}+{(\frac{y-1}{2})}^{2}=1$
- **D.** ${(\frac{x+4}{5})}^{2}+{(\frac{y+1}{2})}^{2}=1$
- **E.** ${(\frac{x-1}{2})}^{2}+{(\frac{y-4}{5})}^{2}=1$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=2\operatorname{sin}⁡t-1\, & ⇒\,\operatorname{sin}⁡t=\frac{x+1}{2} \\ y=5\operatorname{cos}⁡t+4\, & ⇒\,\operatorname{cos}⁡t=\frac{y-4}{5}.\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$, we get

$$
\begin{aligned}{(\frac{x+1}{2})}^{2}+{(\frac{y-4}{5})}^{2}=1.\end{aligned}
$$

So the Cartesian equation of the given curve is ${(\frac{x+1}{2})}^{2}+{(\frac{y-4}{5})}^{2}=1.$

## Generated — Easy
Template: `ellipse_sin_radio`; seed: `17`.

Bank profile: `sin_shift_exchange`; source: `q-15751`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=5\sin t-1,\qquad y=4\cos t+1,\qquad t\in[0,2\pi).
$$

- **A.** $\left(\frac{x + 1}{5}\right)^2+\left(\frac{y - 1}{4}\right)^2=1$
- **B.** $\left(\frac{x + 1}{4}\right)^2+\left(\frac{y - 1}{5}\right)^2=1$
- **C.** $\left(\frac{x - 1}{5}\right)^2+\left(\frac{y + 1}{4}\right)^2=1$
- **D.** $\left(\frac{x + 1}{4}\right)^2+\left(\frac{y + 1}{5}\right)^2=1$
- **E.** $\left(\frac{x - 1}{5}\right)^2+\left(\frac{y - 1}{4}\right)^2=1$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=5\sin t-1 & \Rightarrow\quad \sin t=\frac{x + 1}{5} \\
y=4\cos t+1 & \Rightarrow\quad \cos t=\frac{y - 1}{4}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(\frac{x + 1}{5}\right)^2+\left(\frac{y - 1}{4}\right)^2=1.
$$

So the Cartesian equation of the given curve is $\left(\frac{x + 1}{5}\right)^2+\left(\frac{y - 1}{4}\right)^2=1.$

**Author metadata — curve restrictions:** $-6\le x\le 4,\quad -3\le y\le 5$.

## Generated — Easy
Template: `ellipse_sin_radio`; seed: `29`.

Bank profile: `sin_shift_exchange`; source: `q-15751`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=5\sin t+1,\qquad y=\cos t+5,\qquad t\in[0,2\pi).
$$

- **A.** $\left(x + 5\right)^2+\left(\frac{y - 1}{5}\right)^2=1$
- **B.** $\left(x + 5\right)^2+\left(\frac{y + 1}{5}\right)^2=1$
- **C.** $\left(\frac{x + 1}{5}\right)^2+\left(y + 5\right)^2=1$
- **D.** $\left(\frac{x - 1}{5}\right)^2+\left(y - 5\right)^2=1$
- **E.** $\left(\frac{x + 1}{5}\right)^2+\left(y - 5\right)^2=1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=5\sin t+1 & \Rightarrow\quad \sin t=\frac{x - 1}{5} \\
y=\cos t+5 & \Rightarrow\quad \cos t=y - 5
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(\frac{x - 1}{5}\right)^2+\left(y - 5\right)^2=1.
$$

So the Cartesian equation of the given curve is $\left(\frac{x - 1}{5}\right)^2+\left(y - 5\right)^2=1.$

**Author metadata — curve restrictions:** $-4\le x\le 6,\quad 4\le y\le 6$.

---

# ellipse_sin_radio / sin_unit_y_shift

## Original source — Easy — q-102680

Find the Cartesian equation of the curve defined parametrically as

$$
x=\operatorname{sin}⁡t,\,\,\,y=\operatorname{cos}⁡t-5,\,t\in [0,2\pi ).
$$

- **A.** $(x+5)^{2}+(y+5)^{2}=1$
- **B.** $(x-5)^{2}+{y}^{2}=1$
- **C.** ${x}^{2}+(y-5)^{2}=1$
- **D.** ${x}^{2}+(y+5)^{2}=1$
- **E.** ${x}^{2}+5{y}^{2}=1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=\operatorname{sin}⁡t\, & ⇒\,\operatorname{sin}⁡t=x \\ y=\operatorname{cos}⁡t-5\, & ⇒\,\operatorname{cos}⁡t=y+5\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$, we get

$$
{x}^{2}+(y+5)^{2}=1.
$$

So the Cartesian equation of the given curve is ${x}^{2}+(y+5)^{2}=1.$

## Generated — Easy
Template: `ellipse_sin_radio`; seed: `17`.

Bank profile: `sin_unit_y_shift`; source: `q-102680`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=\sin t,\qquad y=\cos t-1,\qquad t\in[0,2\pi).
$$

- **A.** $x^2+\left(y + 1\right)^2=1$
- **B.** $\left(x - 1\right)^2+y^2=1$
- **C.** $\left(x + 1\right)^2+\left(y + 1\right)^2=1$
- **D.** $x^2+\left(y - 1\right)^2=1$
- **E.** $x^2+y^2=1$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=\sin t & \Rightarrow\quad \sin t=x \\
y=\cos t-1 & \Rightarrow\quad \cos t=y + 1
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
x^2+\left(y + 1\right)^2=1.
$$

So the Cartesian equation of the given curve is $x^2+\left(y + 1\right)^2=1.$

**Author metadata — curve restrictions:** $-1\le x\le 1,\quad -2\le y\le 0$.

## Generated — Easy
Template: `ellipse_sin_radio`; seed: `36`.

Bank profile: `sin_unit_y_shift`; source: `q-102680`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=\sin t,\qquad y=\cos t-3,\qquad t\in[0,2\pi).
$$

- **A.** $x^2+3y^2=1$
- **B.** $\left(x + 3\right)^2+\left(y + 3\right)^2=1$
- **C.** $x^2+\left(y - 3\right)^2=1$
- **D.** $x^2+\left(y + 3\right)^2=1$
- **E.** $\left(x - 3\right)^2+y^2=1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=\sin t & \Rightarrow\quad \sin t=x \\
y=\cos t-3 & \Rightarrow\quad \cos t=y + 3
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
x^2+\left(y + 3\right)^2=1.
$$

So the Cartesian equation of the given curve is $x^2+\left(y + 3\right)^2=1.$

**Author metadata — curve restrictions:** $-1\le x\le 1,\quad -4\le y\le -2$.

---

# ellipse_sin_radio / sin_compound_scale_offset

## Original source — Easy — q-102682

Find the Cartesian equation of the curve defined parametrically as 

$$
x=5\operatorname{sin}⁡t+3,\,\,\,y=3\operatorname{cos}⁡t-2,\,t\in [0,2\pi ).
$$

- **A.** ${(\frac{x-3}{2})}^{2}+{(\frac{y+5}{3})}^{2}=1$
- **B.** ${(\frac{x+2}{5})}^{2}+{(\frac{y-3}{3})}^{2}=1$
- **C.** ${(\frac{x-3}{5})}^{2}+{(\frac{y+2}{3})}^{2}=1$
- **D.** ${(\frac{x-3}{2})}^{2}+{(\frac{y+2}{5})}^{2}=1$
- **E.** ${(\frac{x-5}{3})}^{2}+{(\frac{y+3}{2})}^{2}=1$

**Correct: C**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=5\operatorname{sin}⁡t+3\, & ⇒\,\operatorname{sin}⁡t=\frac{x-3}{5} \\ y=3\operatorname{cos}⁡t-2\, & ⇒\,\operatorname{cos}⁡t=\frac{y+2}{3}\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$, we get

$$
\begin{aligned}{(\frac{x-3}{5})}^{2}+{(\frac{y+2}{3})}^{2}=1.\end{aligned}
$$

So the Cartesian equation of the given curve is ${(\frac{x-3}{5})}^{2}+{(\frac{y+2}{3})}^{2}=1.$

## Generated — Easy
Template: `ellipse_sin_radio`; seed: `18`.

Bank profile: `sin_compound_scale_offset`; source: `q-102682`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t+3,\qquad y=\cos t+1,\qquad t\in[0,2\pi).
$$

- **A.** $\left(-\frac{x - 3}{1}\right)^2+\left(\frac{y - 1}{2}\right)^2=1$
- **B.** $\left(\frac{x - 2}{3}\right)^2+\left(-\frac{y + 3}{1}\right)^2=1$
- **C.** $\left(\frac{x - 1}{2}\right)^2+\left(y - 3\right)^2=1$
- **D.** $\left(\frac{x - 3}{2}\right)^2+\left(y - 1\right)^2=1$
- **E.** $\left(-\frac{x - 3}{1}\right)^2+\left(y + 2\right)^2=1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t+3 & \Rightarrow\quad \sin t=\frac{x - 3}{2} \\
y=\cos t+1 & \Rightarrow\quad \cos t=y - 1
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(\frac{x - 3}{2}\right)^2+\left(y - 1\right)^2=1.
$$

So the Cartesian equation of the given curve is $\left(\frac{x - 3}{2}\right)^2+\left(y - 1\right)^2=1.$

**Author metadata — curve restrictions:** $1\le x\le 5,\quad 0\le y\le 2$.

## Generated — Easy
Template: `ellipse_sin_radio`; seed: `30`.

Bank profile: `sin_compound_scale_offset`; source: `q-102682`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=4\sin t+4,\qquad y=\cos t-2,\qquad t\in[0,2\pi).
$$

- **A.** $\left(\frac{x - 4}{2}\right)^2+\left(y + 4\right)^2=1$
- **B.** $\left(\frac{x - 4}{4}\right)^2+\left(y + 2\right)^2=1$
- **C.** $\left(\frac{x - 4}{2}\right)^2+\left(\frac{y + 2}{4}\right)^2=1$
- **D.** $\left(\frac{x + 2}{4}\right)^2+\left(y - 4\right)^2=1$
- **E.** $\left(\frac{x - 4}{4}\right)^2+\left(\frac{y + 4}{2}\right)^2=1$

**Correct: B**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=4\sin t+4 & \Rightarrow\quad \sin t=\frac{x - 4}{4} \\
y=\cos t-2 & \Rightarrow\quad \cos t=y + 2
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(\frac{x - 4}{4}\right)^2+\left(y + 2\right)^2=1.
$$

So the Cartesian equation of the given curve is $\left(\frac{x - 4}{4}\right)^2+\left(y + 2\right)^2=1.$

**Author metadata — curve restrictions:** $0\le x\le 8,\quad -3\le y\le -1$.

---

# ellipse_sin_radio / sin_unit_x_shift_identity

## Original source — Easy — q-15657

Find the Cartesian equation of the curve defined parametrically as

$$
x=\operatorname{sin}⁡t-3,\,\,\,y=\operatorname{cos}⁡t,\,t\in [0,2\pi ).
$$

- **A.** $(x+3)^{2}+{y}^{2}=1$
- **B.** ${x}^{2}+(y-3)^{2}=1$
- **C.** $3{x}^{2}+{y}^{2}=1$
- **D.** ${x}^{2}+{y}^{2}=3$
- **E.** $(x-3)^{2}+(y-3)^{2}=3$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=\operatorname{sin}⁡t-3\, & ⇒\,\operatorname{sin}⁡t=x+3 \\ y=\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=y.\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$, we get

$$
(x+3)^{2}+{y}^{2}=1.
$$

So the Cartesian equation of the given curve is $(x+3)^{2}+{y}^{2}=1.$

## Generated — Easy
Template: `ellipse_sin_radio`; seed: `17`.

Bank profile: `sin_unit_x_shift_identity`; source: `q-15657`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=\sin t-2,\qquad y=\cos t,\qquad t\in[0,2\pi).
$$

- **A.** $\left(x + 2\right)^2+y^2=1$
- **B.** $2x^2+y^2=1$
- **C.** $x^2+\left(y - 2\right)^2=1$
- **D.** $x^2+y^2=2$
- **E.** $\left(x - 2\right)^2+\left(y - 2\right)^2=2$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=\sin t-2 & \Rightarrow\quad \sin t=x + 2 \\
y=\cos t & \Rightarrow\quad \cos t=y
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(x + 2\right)^2+y^2=1.
$$

So the Cartesian equation of the given curve is $\left(x + 2\right)^2+y^2=1.$

**Author metadata — curve restrictions:** $-3\le x\le -1,\quad -1\le y\le 1$.

## Generated — Easy
Template: `ellipse_sin_radio`; seed: `29`.

Bank profile: `sin_unit_x_shift_identity`; source: `q-15657`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=\sin t-5,\qquad y=\cos t,\qquad t\in[0,2\pi).
$$

- **A.** $x^2+y^2=5$
- **B.** $5x^2+y^2=1$
- **C.** $x^2+\left(y - 5\right)^2=1$
- **D.** $\left(x + 5\right)^2+y^2=1$
- **E.** $\left(x - 5\right)^2+\left(y - 5\right)^2=5$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=\sin t-5 & \Rightarrow\quad \sin t=x + 5 \\
y=\cos t & \Rightarrow\quad \cos t=y
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(x + 5\right)^2+y^2=1.
$$

So the Cartesian equation of the given curve is $\left(x + 5\right)^2+y^2=1.$

**Author metadata — curve restrictions:** $-6\le x\le -4,\quad -1\le y\le 1$.

---

# ellipse_cos_radio / cos_identity_scale

## Original source — Easy — q-15752

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\operatorname{cos}⁡t,\,\,\,y=3\operatorname{sin}⁡t,\,t\in [0,2\pi ).
$$

- **A.** ${(\frac{y}{2})}^{2}-{(\frac{x}{3})}^{2}=2\pi $
- **B.** $-{(\frac{y}{3})}^{2}+{(\frac{x}{2})}^{2}=1$
- **C.** ${x}^{2}+{y}^{2}=6$
- **D.** ${(\frac{y}{3})}^{2}+{(\frac{x}{2})}^{2}=1$
- **E.** ${(\frac{y}{2})}^{2}-{(\frac{x}{3})}^{2}=1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=2\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=\frac{x}{2} \\ y=3\operatorname{sin}⁡t\, & ⇒\,\operatorname{sin}⁡t=\frac{y}{3}.\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1,$ we get

$$
\begin{aligned}{(\frac{y}{3})}^{2}+{(\frac{x}{2})}^{2}=1.\end{aligned}
$$

So the Cartesian equation of the given curve is ${(\frac{y}{3})}^{2}+{(\frac{x}{2})}^{2}=1.$

## Generated — Easy
Template: `ellipse_cos_radio`; seed: `17`.

Bank profile: `cos_identity_scale`; source: `q-15752`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=5\cos t-1,\qquad y=4\sin t,\qquad t\in[0,2\pi).
$$

- **A.** $\left(\frac{y}{4}\right)^2+\left(\frac{x + 1}{5}\right)^2=1$
- **B.** $-\left(\frac{y}{4}\right)^2+\left(\frac{x + 1}{5}\right)^2=1$
- **C.** $\left(\frac{y}{5}\right)^2-\left(\frac{x + 1}{4}\right)^2=2 \pi$
- **D.** $\left(x + 1\right)^2+y^2=20$
- **E.** $\left(\frac{y}{5}\right)^2-\left(\frac{x + 1}{4}\right)^2=1$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=5\cos t-1 & \Rightarrow\quad \cos t=\frac{x + 1}{5} \\
y=4\sin t & \Rightarrow\quad \sin t=\frac{y}{4}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(\frac{y}{4}\right)^2+\left(\frac{x + 1}{5}\right)^2=1.
$$

So the Cartesian equation of the given curve is $\left(\frac{y}{4}\right)^2+\left(\frac{x + 1}{5}\right)^2=1.$

**Author metadata — curve restrictions:** $-6\le x\le 4,\quad -4\le y\le 4$.

## Generated — Easy
Template: `ellipse_cos_radio`; seed: `29`.

Bank profile: `cos_identity_scale`; source: `q-15752`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=5\cos t,\qquad y=\sin t+4,\qquad t\in[0,2\pi).
$$

- **A.** $x^2+\left(y - 4\right)^2=5$
- **B.** $-\left(y - 4\right)^2+\left(\frac{x}{5}\right)^2=1$
- **C.** $\left(\frac{y - 4}{5}\right)^2-x^2=2 \pi$
- **D.** $\left(y - 4\right)^2+\left(\frac{x}{5}\right)^2=1$
- **E.** $\left(\frac{y - 4}{5}\right)^2-x^2=1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=5\cos t & \Rightarrow\quad \cos t=\frac{x}{5} \\
y=\sin t+4 & \Rightarrow\quad \sin t=y - 4
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(y - 4\right)^2+\left(\frac{x}{5}\right)^2=1.
$$

So the Cartesian equation of the given curve is $\left(y - 4\right)^2+\left(\frac{x}{5}\right)^2=1.$

**Author metadata — curve restrictions:** $-5\le x\le 5,\quad 3\le y\le 5$.

---

# ellipse_cos_radio / cos_unit_shift_identity

## Original source — Easy — q-15679

Find the Cartesian equation of the curve defined parametrically as

$$
x=\operatorname{cos}⁡t-2,\,\,\,y=\operatorname{sin}⁡t+3,\,t\in [0,2\pi ).
$$

- **A.** $(y-3)^{2}+{x}^{2}=1$
- **B.** $(y-2)^{2}+(x-3)^{2}=1$
- **C.** $(y-3)^{2}+(x+2)^{2}=1$
- **D.** $(y+3)^{2}+(x+2)^{2}=3$
- **E.** ${y}^{2}+(x+3)^{2}=3$

**Correct: C**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=\operatorname{cos}⁡t-2\, & ⇒\,\operatorname{cos}⁡t=x+2 \\ y=\operatorname{sin}⁡t+3\, & ⇒\,\operatorname{sin}⁡t=y-3.\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1,$ we get

$$
(y-3)^{2}+(x+2)^{2}=1.
$$

So the Cartesian equation of the given curve is $(y-3)^{2}+(x+2)^{2}=1.$

## Generated — Easy
Template: `ellipse_cos_radio`; seed: `17`.

Bank profile: `cos_unit_shift_identity`; source: `q-15679`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=\cos t-1,\qquad y=\sin t+5,\qquad t\in[0,2\pi).
$$

- **A.** $\left(y - 5\right)^2+\left(x + 1\right)^2=1$
- **B.** $\left(y - 1\right)^2+\left(x - 5\right)^2=1$
- **C.** $\left(y - 5\right)^2+x^2=1$
- **D.** $\left(y + 5\right)^2+\left(x + 1\right)^2=5$
- **E.** $y^2+\left(x + 5\right)^2=5$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=\cos t-1 & \Rightarrow\quad \cos t=x + 1 \\
y=\sin t+5 & \Rightarrow\quad \sin t=y - 5
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(y - 5\right)^2+\left(x + 1\right)^2=1.
$$

So the Cartesian equation of the given curve is $\left(y - 5\right)^2+\left(x + 1\right)^2=1.$

**Author metadata — curve restrictions:** $-2\le x\le 0,\quad 4\le y\le 6$.

## Generated — Easy
Template: `ellipse_cos_radio`; seed: `29`.

Bank profile: `cos_unit_shift_identity`; source: `q-15679`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=\cos t-1,\qquad y=\sin t+2,\qquad t\in[0,2\pi).
$$

- **A.** $\left(y + 2\right)^2+\left(x + 1\right)^2=2$
- **B.** $\left(y - 1\right)^2+\left(x - 2\right)^2=1$
- **C.** $\left(y - 2\right)^2+x^2=1$
- **D.** $\left(y - 2\right)^2+\left(x + 1\right)^2=1$
- **E.** $y^2+\left(x + 2\right)^2=2$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=\cos t-1 & \Rightarrow\quad \cos t=x + 1 \\
y=\sin t+2 & \Rightarrow\quad \sin t=y - 2
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\left(y - 2\right)^2+\left(x + 1\right)^2=1.
$$

So the Cartesian equation of the given curve is $\left(y - 2\right)^2+\left(x + 1\right)^2=1.$

**Author metadata — curve restrictions:** $-2\le x\le 0,\quad 1\le y\le 3$.

---

# ellipse_sin_blank

## Original source — Easy — q-320946

Consider the curve defined parametrically as

$$
x=3\operatorname{sin}⁡t,\,\,\,y=\operatorname{cos}⁡t-2,\,t\in [0,2\pi ).
$$

The Cartesian equation of this curve is

{{field-1}}$=1.$

**Correct blank entry:** $\frac{1}{9}{x}^{2}+(y+2)^{2}$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=3\operatorname{sin}⁡t\, & ⇒\,\operatorname{sin}⁡t=\frac{x}{3} \\ y=\operatorname{cos}⁡t-2\, & ⇒\,\operatorname{cos}⁡t=y+2\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$, we get

$$
\begin{aligned}{(\frac{x}{3})}^{2}+(y+2)^{2} & =1 \\ \frac{1}{9}{x}^{2}+(y+2)^{2} & =1.\end{aligned}
$$

## Generated — Easy
Template: `ellipse_sin_blank`; seed: `17`.

Consider the curve defined parametrically as

$$
x=6\sin t,\qquad y=\cos t+2,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

{{field-1}}$=1.$

**Correct blank entry:** $\frac{1}{36}x^2+\left(y - 2\right)^2$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\sin t & \Rightarrow\quad \sin t=\frac{x}{6} \\
y=\cos t+2 & \Rightarrow\quad \cos t=y - 2
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\left(\frac{x}{6}\right)^2+\left(y - 2\right)^2 & =1 \\
\frac{1}{36}x^2+\left(y - 2\right)^2 & =1.
\end{aligned}
$$

**Author metadata — curve restrictions:** $-6\le x\le 6,\quad 1\le y\le 3$.

## Generated — Easy
Template: `ellipse_sin_blank`; seed: `29`.

Consider the curve defined parametrically as

$$
x=6\sin t,\qquad y=\cos t-4,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

{{field-1}}$=1.$

**Correct blank entry:** $\frac{1}{36}x^2+\left(y + 4\right)^2$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\sin t & \Rightarrow\quad \sin t=\frac{x}{6} \\
y=\cos t-4 & \Rightarrow\quad \cos t=y + 4
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\left(\frac{x}{6}\right)^2+\left(y + 4\right)^2 & =1 \\
\frac{1}{36}x^2+\left(y + 4\right)^2 & =1.
\end{aligned}
$$

**Author metadata — curve restrictions:** $-6\le x\le 6,\quad -5\le y\le -3$.

---

# ellipse_cos_blank

## Original source — Easy — q-319828

Consider the curve defined parametrically as

$$
x=2\operatorname{cos}⁡t,\,\,\,y=\operatorname{sin}⁡t+4,\,t\in [0,2\pi ).
$$

The Cartesian equation of this curve is

{{field-1}}$=1.$

**Correct blank entry:** $\frac{1}{4}{x}^{2}+(y-4)^{2}$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=2\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=\frac{x}{2} \\ y=\operatorname{sin}⁡t+4\, & ⇒\,\operatorname{sin}⁡t=y-4\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$, we get

$$
\begin{aligned}(y-4)^{2}+{(\frac{x}{2})}^{2} & =1 \\ \frac{1}{4}{x}^{2}+(y-4)^{2} & =1.\end{aligned}
$$

## Generated — Easy
Template: `ellipse_cos_blank`; seed: `17`.

Consider the curve defined parametrically as

$$
x=6\cos t,\qquad y=\sin t+2,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

{{field-1}}$=1.$

**Correct blank entry:** $\frac{1}{36}x^2+\left(y - 2\right)^2$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\cos t & \Rightarrow\quad \cos t=\frac{x}{6} \\
y=\sin t+2 & \Rightarrow\quad \sin t=y - 2
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\left(y - 2\right)^2+\left(\frac{x}{6}\right)^2 & =1 \\
\frac{1}{36}x^2+\left(y - 2\right)^2 & =1.
\end{aligned}
$$

**Author metadata — curve restrictions:** $-6\le x\le 6,\quad 1\le y\le 3$.

## Generated — Easy
Template: `ellipse_cos_blank`; seed: `29`.

Consider the curve defined parametrically as

$$
x=6\cos t,\qquad y=\sin t-4,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

{{field-1}}$=1.$

**Correct blank entry:** $\frac{1}{36}x^2+\left(y + 4\right)^2$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\cos t & \Rightarrow\quad \cos t=\frac{x}{6} \\
y=\sin t-4 & \Rightarrow\quad \sin t=y + 4
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\left(y + 4\right)^2+\left(\frac{x}{6}\right)^2 & =1 \\
\frac{1}{36}x^2+\left(y + 4\right)^2 & =1.
\end{aligned}
$$

**Author metadata — curve restrictions:** $-6\le x\le 6,\quad -5\le y\le -3$.

---

# tan_sec_radio / tan_sec_source

## Original source — Easy — q-102677

Find the Cartesian equation of the curve defined parametrically as 

$$
x=2\operatorname{tan}⁡t,\,\,\,y=\operatorname{sec}⁡t,\,t\in (0,\frac{\pi }{2}).
$$

- **A.** ${y}^{2}={(\frac{x}{2})}^{2}-1$
- **B.** ${y}^{2}={(\frac{2}{x})}^{2}+1$
- **C.** ${y}^{2}={(\frac{x}{2})}^{2}+1$
- **D.** ${y}^{2}={x}^{2}+2$
- **E.** ${y}^{2}=1-{(\frac{x}{2})}^{2}$

**Correct: C**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=2\operatorname{tan}⁡t\, & ⇒\,\operatorname{tan}⁡t=\frac{x}{2} \\ y=\operatorname{sec}⁡t\, & ⇒\,\operatorname{sec}⁡t=y\end{aligned}
$$

Dividing the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$ by ${cos}^{2}⁡t$, we get

$$
\begin{aligned}\frac{{sin}^{2}⁡t}{{cos}^{2}⁡t}+\frac{{cos}^{2}⁡t}{{cos}^{2}⁡t} & =\frac{1}{{cos}^{2}⁡t} \\ {(\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t})}^{2}+1 & ={(\frac{1}{\operatorname{cos}⁡t})}^{2} \\ {tan}^{2}⁡t+1 & ={sec}^{2}⁡t.\end{aligned}
$$

Substituting $\operatorname{tan}⁡t=\frac{x}{2}$ and $\operatorname{sec}⁡t=y$ into this formula, we get

$$
\begin{aligned}{(\frac{x}{2})}^{2}+1={y}^{2}.\end{aligned}
$$

So the Cartesian equation of the given curve is ${y}^{2}={(\frac{x}{2})}^{2}+1.$

## Generated — Easy
Template: `tan_sec_radio`; seed: `17`.

Bank profile: `tan_sec_source`; source: `q-102677`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=6\tan t,\qquad y=\sec t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y^2=\left(\frac{x}{6}\right)^2+1$
- **B.** $y^{2}=\left(\frac{6}{x}\right)^2+1$
- **C.** $y^{2}=\left(\frac{x}{6}\right)^2-1$
- **D.** $y^{2}=x^2+6$
- **E.** $y^{2}=1-\left(\frac{x}{6}\right)^2$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\tan t & \Rightarrow\quad \tan t=\frac{x}{6} \\
y=\sec t & \Rightarrow\quad \sec t=y
\end{aligned}
$$

Dividing the Pythagorean identity $\sin^2 t+\cos^2 t=1$ by $\cos^2 t$, we get

$$
\begin{aligned}
\frac{\sin^2 t}{\cos^2 t}+\frac{\cos^2 t}{\cos^2 t} & =\frac{1}{\cos^2 t} \\
\left(\frac{\sin t}{\cos t}\right)^2+1 & =\left(\frac{1}{\cos t}\right)^2 \\
\tan^2 t+1 & =\sec^2 t.
\end{aligned}
$$

Substituting $\tan t=\frac{x}{6}$ and $\sec t=y$ into this formula, we get

$$
\left(\frac{x}{6}\right)^2+1=y^2.
$$

So the Cartesian equation of the given curve is $y^2=\left(\frac{x}{6}\right)^2+1.$

**Author metadata — curve restrictions:** $x>0,\quad y>1$.

## Generated — Easy
Template: `tan_sec_radio`; seed: `36`.

Bank profile: `tan_sec_source`; source: `q-102677`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=4\tan t,\qquad y=\sec t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y^{2}=1-\left(\frac{x}{4}\right)^2$
- **B.** $y^{2}=\left(\frac{x}{4}\right)^2-1$
- **C.** $y^{2}=x^2+4$
- **D.** $y^2=\left(\frac{x}{4}\right)^2+1$
- **E.** $y^{2}=\left(\frac{4}{x}\right)^2+1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=4\tan t & \Rightarrow\quad \tan t=\frac{x}{4} \\
y=\sec t & \Rightarrow\quad \sec t=y
\end{aligned}
$$

Dividing the Pythagorean identity $\sin^2 t+\cos^2 t=1$ by $\cos^2 t$, we get

$$
\begin{aligned}
\frac{\sin^2 t}{\cos^2 t}+\frac{\cos^2 t}{\cos^2 t} & =\frac{1}{\cos^2 t} \\
\left(\frac{\sin t}{\cos t}\right)^2+1 & =\left(\frac{1}{\cos t}\right)^2 \\
\tan^2 t+1 & =\sec^2 t.
\end{aligned}
$$

Substituting $\tan t=\frac{x}{4}$ and $\sec t=y$ into this formula, we get

$$
\left(\frac{x}{4}\right)^2+1=y^2.
$$

So the Cartesian equation of the given curve is $y^2=\left(\frac{x}{4}\right)^2+1.$

**Author metadata — curve restrictions:** $x>0,\quad y>1$.

---

# cot_csc_radio / cot_csc_source

## Original source — Easy — q-15761

Find the Cartesian equation of the curve defined parametrically as 

$$
x=3\operatorname{cot}⁡t,\,\,\,y=\operatorname{csc}⁡t,\,t\in (0,\frac{\pi }{2}).
$$

- **A.** ${y}^{2}=1+{x}^{2}$
- **B.** ${y}^{2}=1-{(\frac{x}{3})}^{2}$
- **C.** ${y}^{2}=1-3{x}^{2}$
- **D.** ${y}^{2}=1+{(\frac{x}{3})}^{2}$
- **E.** ${y}^{2}=1+{(\frac{x}{2})}^{2}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=3\operatorname{cot}⁡t\, & ⇒\,\operatorname{cot}⁡t=\frac{x}{3} \\ y=\operatorname{csc}⁡t\, & ⇒\,\operatorname{csc}⁡t=y.\end{aligned}
$$

Dividing the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$ by ${sin}^{2}⁡t$, we get

$$
\begin{aligned}\frac{{sin}^{2}⁡t}{{sin}^{2}⁡t}+\frac{{cos}^{2}⁡t}{{sin}^{2}⁡t} & =\frac{1}{{sin}^{2}⁡t} \\ 1+{(\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t})}^{2} & ={(\frac{1}{\operatorname{sin}⁡t})}^{2} \\ 1+{cot}^{2}⁡t & ={csc}^{2}⁡t.\end{aligned}
$$

Substituting $\operatorname{cot}⁡t=\frac{x}{3}$ and $\operatorname{csc}⁡t=y$ into this formula, we get

$$
\begin{aligned}1+{(\frac{x}{3})}^{2}={y}^{2}.\end{aligned}
$$

So the Cartesian equation of the given curve is ${y}^{2}=1+{(\frac{x}{3})}^{2}.$

## Generated — Easy
Template: `cot_csc_radio`; seed: `17`.

Bank profile: `cot_csc_source`; source: `q-15761`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=6\cot t,\qquad y=\csc t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y^2=1+\left(\frac{x}{6}\right)^2$
- **B.** $y^{2}=1-\left(\frac{x}{6}\right)^2$
- **C.** $y^{2}=1+x^2$
- **D.** $y^{2}=1-6x^2$
- **E.** $y^{2}=1+\left(\frac{x}{5}\right)^2$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\cot t & \Rightarrow\quad \cot t=\frac{x}{6} \\
y=\csc t & \Rightarrow\quad \csc t=y
\end{aligned}
$$

Dividing the Pythagorean identity $\sin^2 t+\cos^2 t=1$ by $\sin^2 t$, we get

$$
\begin{aligned}
\frac{\sin^2 t}{\sin^2 t}+\frac{\cos^2 t}{\sin^2 t} & =\frac{1}{\sin^2 t} \\
1+\left(\frac{\cos t}{\sin t}\right)^2 & =\left(\frac{1}{\sin t}\right)^2 \\
1+\cot^2 t & =\csc^2 t.
\end{aligned}
$$

Substituting $\cot t=\frac{x}{6}$ and $\csc t=y$ into this formula, we get

$$
1+\left(\frac{x}{6}\right)^2=y^2.
$$

So the Cartesian equation of the given curve is $y^2=1+\left(\frac{x}{6}\right)^2.$

**Author metadata — curve restrictions:** $x>0,\quad y>1$.

## Generated — Easy
Template: `cot_csc_radio`; seed: `30`.

Bank profile: `cot_csc_source`; source: `q-15761`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=5\cot t,\qquad y=\csc t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y^{2}=1+x^2$
- **B.** $y^2=1+\left(\frac{x}{5}\right)^2$
- **C.** $y^{2}=1-5x^2$
- **D.** $y^{2}=1-\left(\frac{x}{5}\right)^2$
- **E.** $y^{2}=1+\left(\frac{x}{4}\right)^2$

**Correct: B**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=5\cot t & \Rightarrow\quad \cot t=\frac{x}{5} \\
y=\csc t & \Rightarrow\quad \csc t=y
\end{aligned}
$$

Dividing the Pythagorean identity $\sin^2 t+\cos^2 t=1$ by $\sin^2 t$, we get

$$
\begin{aligned}
\frac{\sin^2 t}{\sin^2 t}+\frac{\cos^2 t}{\sin^2 t} & =\frac{1}{\sin^2 t} \\
1+\left(\frac{\cos t}{\sin t}\right)^2 & =\left(\frac{1}{\sin t}\right)^2 \\
1+\cot^2 t & =\csc^2 t.
\end{aligned}
$$

Substituting $\cot t=\frac{x}{5}$ and $\csc t=y$ into this formula, we get

$$
1+\left(\frac{x}{5}\right)^2=y^2.
$$

So the Cartesian equation of the given curve is $y^2=1+\left(\frac{x}{5}\right)^2.$

**Author metadata — curve restrictions:** $x>0,\quad y>1$.

---

# cot_csc_blank

## Original source — Easy — q-321400

Consider the curve defined parametrically as

$$
x=3\operatorname{cot}⁡t,\,\,\,y=2\operatorname{csc}⁡t,\,0<t<\frac{\pi }{2}.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $2\sqrt{1+\frac{{x}^{2}}{9}}$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=3\operatorname{cot}⁡t\, & ⇒\,\operatorname{cot}⁡t=\frac{x}{3} \\ y=2\operatorname{csc}⁡t\, & ⇒\,\operatorname{csc}⁡t=\frac{y}{2}\end{aligned}
$$

Using the Pythagorean identity ${csc}^{2}⁡t=1+{cot}^{2}⁡t$, we get

$$
\begin{aligned}{csc}^{2}⁡t & =1+{cot}^{2}⁡t \\ \frac{{y}^{2}}{4} & =1+\frac{{x}^{2}}{9}.\end{aligned}
$$

We used here that $\operatorname{csc}⁡t>0$ and $\operatorname{cot}⁡t>0$ in the range $0<t<\frac{\pi }{2}.$

Now, solving for $y$, we obtain

$$
y=2\sqrt{\,1+\frac{{x}^{2}}{9}\,}.
$$

So, the Cartesian equation of the given curve is 
$y=2\sqrt{\,1+\frac{{x}^{2}}{9}\,}.$

## Generated — Easy
Template: `cot_csc_blank`; seed: `17`.

Consider the curve defined parametrically as

$$
x=6\cot t,\qquad y=5\csc t,\qquad 0<t<\frac{\pi}{2}.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $5\sqrt{1+\frac{x^2}{36}}$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\cot t & \Rightarrow\quad \cot t=\frac{x}{6} \\
y=5\csc t & \Rightarrow\quad \csc t=\frac{y}{5}
\end{aligned}
$$

Using the Pythagorean identity $\csc^2 t=1+\cot^2 t$, we get

$$
\begin{aligned}
\csc^2 t & =1+\cot^2 t \\
\frac{y^2}{25} & =1+\frac{x^2}{36}.
\end{aligned}
$$

We used here that $\csc t>0$ and $\cot t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, solving for $y$, we obtain

$$
y=5\sqrt{1+\frac{x^2}{36}}.
$$

So, the Cartesian equation of the given curve is $y=5\sqrt{1+\frac{x^2}{36}}.$

**Author metadata — curve restrictions:** $x>0,\quad y>5$.

## Generated — Easy
Template: `cot_csc_blank`; seed: `29`.

Consider the curve defined parametrically as

$$
x=6\cot t,\qquad y=2\csc t,\qquad 0<t<\frac{\pi}{2}.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $2\sqrt{1+\frac{x^2}{36}}$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\cot t & \Rightarrow\quad \cot t=\frac{x}{6} \\
y=2\csc t & \Rightarrow\quad \csc t=\frac{y}{2}
\end{aligned}
$$

Using the Pythagorean identity $\csc^2 t=1+\cot^2 t$, we get

$$
\begin{aligned}
\csc^2 t & =1+\cot^2 t \\
\frac{y^2}{4} & =1+\frac{x^2}{36}.
\end{aligned}
$$

We used here that $\csc t>0$ and $\cot t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, solving for $y$, we obtain

$$
y=2\sqrt{1+\frac{x^2}{36}}.
$$

So, the Cartesian equation of the given curve is $y=2\sqrt{1+\frac{x^2}{36}}.$

**Author metadata — curve restrictions:** $x>0,\quad y>2$.

---

# cos_tan_radio / cos_tan_source

## Original source — Moderate — q-102687

Find the Cartesian equation of the curve defined parametrically as

$$
x=\operatorname{cos}⁡t,\,\,\,y=\operatorname{tan}⁡t,\,0<t<\frac{\pi }{2}.
$$

- **A.** $y=\frac{\sqrt{1-{x}^{2}}}{2x}$
- **B.** $y=\frac{\sqrt{1-{x}^{2}}}{x}$
- **C.** $y=\frac{1-{x}^{2}}{2x}$
- **D.** $y=\sqrt{1-{x}^{2}}$
- **E.** $y=\frac{1-{x}^{2}}{x}$

**Correct: B**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=x \\ y=\operatorname{tan}⁡t\, & ⇒\,\operatorname{tan}⁡t=y\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$, we get

$$
\begin{aligned}{sin}^{2}⁡t+{cos}^{2}⁡t & =1 \\ {sin}^{2}⁡t & =1-{cos}^{2}⁡t \\ \operatorname{sin}⁡t & =\sqrt{1-{cos}^{2}⁡t}.\end{aligned}
$$

We used here that $\operatorname{sin}⁡t>0$ in the range $0<t<\frac{\pi }{2}.$

Now, using the definition of a tangent, we obtain

$$
\operatorname{tan}⁡t=\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}=\frac{\sqrt{1-{cos}^{2}⁡t}}{\operatorname{cos}⁡t}.
$$

Substituting $\operatorname{cos}⁡t=x$ and $\operatorname{tan}⁡t=y$ into this formula, we get

$$
y=\frac{\sqrt{1-{x}^{2}}}{x}.
$$

So the Cartesian equation of the given curve is $y=\frac{\sqrt{1-{x}^{2}}}{x}.$

## Generated — Moderate
Template: `cos_tan_radio`; seed: `17`.

Bank profile: `cos_tan_source`; source: `q-102687`.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=4\cos t,\qquad y=3\tan t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y=\frac{3 \sqrt{- x^{2} + 16}}{x}$
- **B.** $y=\frac{6 \left(- \frac{x^{2}}{16} + 1\right)}{x}$
- **C.** $y=\frac{3 \sqrt{- x^{2} + 16}}{2 x}$
- **D.** $y=3 \sqrt{- \frac{x^{2}}{16} + 1}$
- **E.** $y=\frac{12 \left(- \frac{x^{2}}{16} + 1\right)}{x}$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=4\cos t & \Rightarrow\quad \cos t=\frac{x}{4} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sqrt{1-\cos^2 t}}{\cos t}.
$$

Substituting $\cos t=\frac{x}{4}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\sqrt{1-\left(\frac{x}{4}\right)^2}}{\frac{x}{4}} \\
y & =\frac{3 \sqrt{- x^{2} + 16}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 \sqrt{- x^{2} + 16}}{x}.$

**Author metadata — curve restrictions:** $0<x<4\quad y>0$.

## Generated — Moderate
Template: `cos_tan_radio`; seed: `29`.

Bank profile: `cos_tan_source`; source: `q-102687`.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=\cos t,\qquad y=3\tan t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y=3 \sqrt{- x^{2} + 1}$
- **B.** $y=\frac{3 \left(- x^{2} + 1\right)}{2 x}$
- **C.** $y=\frac{3 \sqrt{- x^{2} + 1}}{2 x}$
- **D.** $y=\frac{3 \sqrt{- x^{2} + 1}}{x}$
- **E.** $y=\frac{3 \left(- x^{2} + 1\right)}{x}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=\cos t & \Rightarrow\quad \cos t=x \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sqrt{1-\cos^2 t}}{\cos t}.
$$

Substituting $\cos t=x$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\sqrt{1-x^2}}{x} \\
y & =\frac{3 \sqrt{- x^{2} + 1}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 \sqrt{- x^{2} + 1}}{x}.$

**Author metadata — curve restrictions:** $0<x<1\quad y>0$.

---

# sin_tan_radio / sin_tan_source

## Original source — Moderate — q-15759

Find the Cartesian equation of the curve defined parametrically as

$$
x=\operatorname{sin}⁡t,\,\,\,y=\operatorname{tan}⁡t,\,0<t<\frac{\pi }{2}.
$$

- **A.** $y=\frac{4x}{\sqrt{1+{x}^{2}}}$
- **B.** $y=\frac{x}{\sqrt{{x}^{2}-4}}$
- **C.** $y=\frac{2x}{\sqrt{2+{x}^{2}}}$
- **D.** $y=\frac{x}{\sqrt{1-{x}^{2}}}$
- **E.** $y=\frac{2x}{\sqrt{{x}^{2}-1}}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=\operatorname{sin}⁡t\, & ⇒\,\operatorname{sin}⁡t=x \\ y=\operatorname{tan}⁡t\, & ⇒\,\operatorname{tan}⁡t=y\end{aligned}
$$

Using the Pythagorean identity ${sin}^{2}⁡t+{cos}^{2}⁡t=1$, we get

$$
\begin{aligned}{sin}^{2}⁡t+{cos}^{2}⁡t & =1 \\ {cos}^{2}⁡t & =1-{sin}^{2}⁡t \\ \operatorname{cos}⁡t & =\sqrt{1-{sin}^{2}⁡t}.\end{aligned}
$$

We used here that $\operatorname{cos}⁡t>0$ in the range $0<t<\frac{\pi }{2}.$

Now, using the definition of a tangent, we obtain

$$
\operatorname{tan}⁡t=\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}=\frac{\operatorname{sin}⁡t}{\sqrt{1-{sin}^{2}⁡t}}.
$$

Substituting $\operatorname{sin}⁡t=x$ and $\operatorname{tan}⁡t=y$ into this formula, we get

$$
y=\frac{x}{\sqrt{1-{x}^{2}}}.
$$

So the Cartesian equation of the given curve is $y=\frac{x}{\sqrt{1-{x}^{2}}}.$

## Generated — Moderate
Template: `sin_tan_radio`; seed: `17`.

Bank profile: `sin_tan_source`; source: `q-15759`.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=4\sin t,\qquad y=3\tan t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y=\frac{3 x}{\sqrt{- x^{2} + 16}}$
- **B.** $y=\frac{3 x}{\sqrt{x^{2} - 64}}$
- **C.** $y=\frac{12 x}{\sqrt{x^{2} + 16}}$
- **D.** $y=\frac{6 x}{\sqrt{x^{2} + 32}}$
- **E.** $y=\frac{6 x}{\sqrt{x^{2} - 16}}$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=4\sin t & \Rightarrow\quad \sin t=\frac{x}{4} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sin t}{\sqrt{1-\sin^2 t}}.
$$

Substituting $\sin t=\frac{x}{4}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{4}}{\sqrt{1-\left(\frac{x}{4}\right)^2}} \\
y & =\frac{3 x}{\sqrt{- x^{2} + 16}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 x}{\sqrt{- x^{2} + 16}}.$

**Author metadata — curve restrictions:** $0<x<4\quad y>0$.

## Generated — Moderate
Template: `sin_tan_radio`; seed: `29`.

Bank profile: `sin_tan_source`; source: `q-15759`.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=\sin t,\qquad y=3\tan t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y=\frac{6 x}{\sqrt{x^{2} + 2}}$
- **B.** $y=\frac{3 x}{\sqrt{x^{2} - 4}}$
- **C.** $y=\frac{12 x}{\sqrt{x^{2} + 1}}$
- **D.** $y=\frac{3 x}{\sqrt{- x^{2} + 1}}$
- **E.** $y=\frac{6 x}{\sqrt{x^{2} - 1}}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=\sin t & \Rightarrow\quad \sin t=x \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sin t}{\sqrt{1-\sin^2 t}}.
$$

Substituting $\sin t=x$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{x}{\sqrt{1-x^2}} \\
y & =\frac{3 x}{\sqrt{- x^{2} + 1}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 x}{\sqrt{- x^{2} + 1}}.$

**Author metadata — curve restrictions:** $0<x<1\quad y>0$.

---

# sin_double_factored_radio / sin_double_factored_source

## Original source — Hard — q-24378

Find the Cartesian equation of the curve defined parametrically as 

$$
x=2\operatorname{sin}⁡t,\,\,\,y=3\operatorname{cos}⁡2t,\,t\in [0,2\pi ).
$$

- **A.** $y=1-\frac{{x}^{2}}{4}$
- **B.** $y=3(1-\frac{{x}^{2}}{2})$
- **C.** $y=3(1+\frac{{x}^{2}}{4})$
- **D.** $y=2(1+\frac{{x}^{2}}{4})$
- **E.** $y=1-\frac{{x}^{2}}{2}$

**Correct: B**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=2\operatorname{sin}⁡t\, & ⇒\,\operatorname{sin}⁡t=\frac{x}{2} \\ y=3\operatorname{cos}⁡2t\, & ⇒\,\operatorname{cos}⁡2t=\frac{y}{3}.\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}\operatorname{cos}⁡2t & ={cos}^{2}⁡t-{sin}^{2}⁡t \\  & =(1-{sin}^{2}⁡t)-{sin}^{2}⁡t \\  & =1-2{sin}^{2}⁡t.\end{aligned}
$$

Substituting $\operatorname{sin}⁡t=\frac{x}{2}$ and $\operatorname{cos}⁡2t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}\frac{y}{3} & =1-2{(\frac{x}{2})}^{2} \\ \frac{y}{3} & =1-2(\frac{{x}^{2}}{4}) \\ \frac{y}{3} & =1-\frac{{x}^{2}}{2} \\ y & =3(1-\frac{{x}^{2}}{2}).\end{aligned}
$$

So the Cartesian equation of the given curve is $y=3(1-\frac{{x}^{2}}{2}).$

## Generated — Hard
Template: `sin_double_factored_radio`; seed: `17`.

Bank profile: `sin_double_factored_source`; source: `q-24378`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=6\sin t,\qquad y=5\cos 2t,\qquad t\in[0,2\pi).
$$

- **A.** $y=5\left(1-\frac{1}{18}x^2\right)$
- **B.** $y=5\left(\frac{x^{2}}{36} + 1\right)$
- **C.** $y=- \frac{x^{2}}{36} + 1$
- **D.** $y=4\left(\frac{x^{2}}{36} + 1\right)$
- **E.** $y=- \frac{x^{2}}{18} + 1$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\sin t & \Rightarrow\quad \sin t=\frac{x}{6} \\
y=5\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{5}
\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =(1-\sin^2 t)-\sin^2 t \\
 & =1-2\sin^2 t.
\end{aligned}
$$

Substituting $\sin t=\frac{x}{6}$ and $\cos 2t=\frac{y}{5}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{5} & =1-2\left(\frac{x}{6}\right)^2 \\
\frac{y}{5} & =1-2\left(\frac{x^2}{36}\right) \\
\frac{y}{5} & =1-\frac{1}{18}x^2 \\
y & =5\left(1-\frac{1}{18}x^2\right)
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=5\left(1-\frac{1}{18}x^2\right).$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

## Generated — Hard
Template: `sin_double_factored_radio`; seed: `29`.

Bank profile: `sin_double_factored_source`; source: `q-24378`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=6\sin t,\qquad y=2\cos 2t,\qquad t\in[0,2\pi).
$$

- **A.** $y=1\left(\frac{x^{2}}{36} + 1\right)$
- **B.** $y=2\left(\frac{x^{2}}{36} + 1\right)$
- **C.** $y=- \frac{x^{2}}{36} + 1$
- **D.** $y=2\left(1-\frac{1}{18}x^2\right)$
- **E.** $y=- \frac{x^{2}}{18} + 1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\sin t & \Rightarrow\quad \sin t=\frac{x}{6} \\
y=2\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{2}
\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =(1-\sin^2 t)-\sin^2 t \\
 & =1-2\sin^2 t.
\end{aligned}
$$

Substituting $\sin t=\frac{x}{6}$ and $\cos 2t=\frac{y}{2}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{2} & =1-2\left(\frac{x}{6}\right)^2 \\
\frac{y}{2} & =1-2\left(\frac{x^2}{36}\right) \\
\frac{y}{2} & =1-\frac{1}{18}x^2 \\
y & =2\left(1-\frac{1}{18}x^2\right)
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=2\left(1-\frac{1}{18}x^2\right).$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

---

# sin_double_expanded_radio / sin_double_expanded_source

## Original source — Hard — q-24576

Find the Cartesian equation of the curve defined parametrically as 

$$
x=6\operatorname{sin}⁡t,\,\,\,y=-5\operatorname{cos}⁡2t,\,t\in [0,2\pi ).
$$

- **A.** $y=-5+\frac{5{x}^{2}}{18}$
- **B.** $y=1+\frac{5{x}^{2}}{6}$
- **C.** $y=5+{x}^{2}$
- **D.** $y=-18+\frac{{x}^{2}}{5}$
- **E.** $y=\frac{1}{5}-{x}^{2}$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=6\operatorname{sin}⁡t\, & ⇒\,\operatorname{sin}⁡t=\frac{x}{6} \\ y=-5\operatorname{cos}⁡2t\, & ⇒\,\operatorname{cos}⁡2t=-\frac{y}{5}.\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}\operatorname{cos}⁡2t & ={cos}^{2}⁡t-{sin}^{2}⁡t \\  & =(1-{sin}^{2}⁡t)-{sin}^{2}⁡t \\  & =1-2{sin}^{2}⁡t.\end{aligned}
$$

Substituting $\operatorname{sin}⁡t=\frac{x}{6}$ and $\operatorname{cos}⁡2t=-\frac{y}{5}$ into this formula, we get

$$
\begin{aligned}-\frac{y}{5} & =1-2{(\frac{x}{6})}^{2} \\ -\frac{y}{5} & =1-2(\frac{{x}^{2}}{36}) \\ -\frac{y}{5} & =1-\frac{{x}^{2}}{18} \\ y & =-5+\frac{5{x}^{2}}{18}.\end{aligned}
$$

So the Cartesian equation of the given curve is $y=-5+\frac{5{x}^{2}}{18}.$

## Generated — Hard
Template: `sin_double_expanded_radio`; seed: `18`.

Bank profile: `sin_double_expanded_source`; source: `q-24576`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=3\sin t,\qquad y=-2\cos 2t,\qquad t\in[0,2\pi).
$$

- **A.** $y=\frac{x^{2}}{2} - \frac{9}{2}$
- **B.** $y=- x^{2} + \frac{1}{2}$
- **C.** $y=x^{2} + 2$
- **D.** $y=-2+\frac{4}{9}x^2$
- **E.** $y=\frac{2 x^{2}}{3} + 1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=3\sin t & \Rightarrow\quad \sin t=\frac{x}{3} \\
y=-2\cos 2t & \Rightarrow\quad \cos 2t=-\frac{y}{2}
\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =(1-\sin^2 t)-\sin^2 t \\
 & =1-2\sin^2 t.
\end{aligned}
$$

Substituting $\sin t=\frac{x}{3}$ and $\cos 2t=-\frac{y}{2}$ into this formula, we get

$$
\begin{aligned}
-\frac{y}{2} & =1-2\left(\frac{x}{3}\right)^2 \\
-\frac{y}{2} & =1-2\left(\frac{x^2}{9}\right) \\
-\frac{y}{2} & =1-\frac{2}{9}x^2 \\
y & =-2+\frac{4}{9}x^2
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=-2+\frac{4}{9}x^2.$

**Author metadata — curve restrictions:** $-3\le x\le 3$.

## Generated — Hard
Template: `sin_double_expanded_radio`; seed: `29`.

Bank profile: `sin_double_expanded_source`; source: `q-24576`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=6\sin t,\qquad y=-2\cos 2t,\qquad t\in[0,2\pi).
$$

- **A.** $y=\frac{x^{2}}{2} - 18$
- **B.** $y=x^{2} + 2$
- **C.** $y=\frac{x^{2}}{3} + 1$
- **D.** $y=-2+\frac{1}{9}x^2$
- **E.** $y=- x^{2} + \frac{1}{2}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\sin t & \Rightarrow\quad \sin t=\frac{x}{6} \\
y=-2\cos 2t & \Rightarrow\quad \cos 2t=-\frac{y}{2}
\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =(1-\sin^2 t)-\sin^2 t \\
 & =1-2\sin^2 t.
\end{aligned}
$$

Substituting $\sin t=\frac{x}{6}$ and $\cos 2t=-\frac{y}{2}$ into this formula, we get

$$
\begin{aligned}
-\frac{y}{2} & =1-2\left(\frac{x}{6}\right)^2 \\
-\frac{y}{2} & =1-2\left(\frac{x^2}{36}\right) \\
-\frac{y}{2} & =1-\frac{1}{18}x^2 \\
y & =-2+\frac{1}{9}x^2
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=-2+\frac{1}{9}x^2.$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

---

# cos_double_radio / cos_double_positive_source

## Original source — Hard — q-24574

Find the Cartesian equation of the curve defined parametrically as 

$$
x=4\operatorname{cos}⁡t,\,\,\,y=2\operatorname{cos}⁡2t,\,t\in [0,2\pi ).
$$

- **A.** $y=2(\frac{{x}^{2}}{8}-1)$
- **B.** $y=3(\frac{{x}^{2}}{5}-1)$
- **C.** $y=\frac{{x}^{2}}{4}+1$
- **D.** $y=3{x}^{2}+8$
- **E.** $y=1-\frac{{x}^{2}}{8}$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=4\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=\frac{x}{4} \\ y=2\operatorname{cos}⁡2t\, & ⇒\,\operatorname{cos}⁡2t=\frac{y}{2}.\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}\operatorname{cos}⁡2t & ={cos}^{2}⁡t-{sin}^{2}⁡t \\  & ={cos}^{2}⁡t-(1-{cos}^{2}⁡t) \\  & =2{cos}^{2}⁡t-1.\end{aligned}
$$

Substituting $\operatorname{cos}⁡t=\frac{x}{4}$ and $\operatorname{cos}⁡2t=\frac{y}{2}$ into this formula, we get

$$
\begin{aligned}\frac{y}{2} & =2{(\frac{x}{4})}^{2}-1 \\ \frac{y}{2} & =2(\frac{{x}^{2}}{16})-1 \\ \frac{y}{2} & =\frac{{x}^{2}}{8}-1 \\ y & =2(\frac{{x}^{2}}{8}-1).\end{aligned}
$$

So the Cartesian equation of the given curve is $y=2(\frac{{x}^{2}}{8}-1).$

## Generated — Hard
Template: `cos_double_radio`; seed: `17`.

Bank profile: `cos_double_positive_source`; source: `q-24574`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=6\cos t,\qquad y=5\cos 2t,\qquad t\in[0,2\pi).
$$

- **A.** $y=5\left(\frac{1}{18}x^2-1\right)$
- **B.** $y=\frac{x^{2}}{6} + 1$
- **C.** $y=6\left(\frac{x^{2}}{7} - 1\right)$
- **D.** $y=6 x^{2} + 30$
- **E.** $y=- \frac{x^{2}}{18} + 1$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\cos t & \Rightarrow\quad \cos t=\frac{x}{6} \\
y=5\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{5}
\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=\frac{x}{6}$ and $\cos 2t=\frac{y}{5}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{5} & =2\left(\frac{x}{6}\right)^2-1 \\
\frac{y}{5} & =2\left(\frac{x^2}{36}\right)-1 \\
\frac{y}{5} & =\frac{1}{18}x^2-1 \\
y & =5\left(\frac{1}{18}x^2-1\right)
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=5\left(\frac{1}{18}x^2-1\right).$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

## Generated — Hard
Template: `cos_double_radio`; seed: `29`.

Bank profile: `cos_double_positive_source`; source: `q-24574`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=6\cos t,\qquad y=2\cos 2t,\qquad t\in[0,2\pi).
$$

- **A.** $y=3 x^{2} + 12$
- **B.** $y=\frac{x^{2}}{6} + 1$
- **C.** $y=3\left(\frac{x^{2}}{7} - 1\right)$
- **D.** $y=2\left(\frac{1}{18}x^2-1\right)$
- **E.** $y=- \frac{x^{2}}{18} + 1$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\cos t & \Rightarrow\quad \cos t=\frac{x}{6} \\
y=2\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{2}
\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=\frac{x}{6}$ and $\cos 2t=\frac{y}{2}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{2} & =2\left(\frac{x}{6}\right)^2-1 \\
\frac{y}{2} & =2\left(\frac{x^2}{36}\right)-1 \\
\frac{y}{2} & =\frac{1}{18}x^2-1 \\
y & =2\left(\frac{1}{18}x^2-1\right)
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=2\left(\frac{1}{18}x^2-1\right).$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

---

# cos_double_radio / cos_double_negative_source

## Original source — Hard — q-24575

Find the Cartesian equation of the curve defined parametrically as 

$$
x=-3\operatorname{cos}⁡t,\,\,\,y=4\operatorname{cos}⁡2t,\,t\in [0,2\pi ).
$$

- **A.** $y=\frac{{x}^{2}}{9}-1$
- **B.** $y=1+\frac{{x}^{2}}{6}$
- **C.** $y=1-\frac{{x}^{2}}{9}$
- **D.** $y=7(\frac{{x}^{2}}{9}+1)$
- **E.** $y=4(\frac{2{x}^{2}}{9}-1)$

**Correct: E**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=-3\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=-\frac{x}{3} \\ y=4\operatorname{cos}⁡2t\, & ⇒\,\operatorname{cos}⁡2t=\frac{y}{4}.\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}\operatorname{cos}⁡2t & ={cos}^{2}⁡t-{sin}^{2}⁡t \\  & ={cos}^{2}⁡t-(1-{cos}^{2}⁡t) \\  & =2{cos}^{2}⁡t-1.\end{aligned}
$$

Substituting $\operatorname{cos}⁡t=-\frac{x}{3}$ and $\operatorname{cos}⁡2t=\frac{y}{4}$ into this formula, we get

$$
\begin{aligned}\frac{y}{4} & =2{(-\frac{x}{3})}^{2}-1 \\ \frac{y}{4} & =\frac{2{x}^{2}}{9}-1 \\ y & =4(\frac{2{x}^{2}}{9}-1).\end{aligned}
$$

So the Cartesian equation of the given curve is $y=4(\frac{2{x}^{2}}{9}-1).$

## Generated — Hard
Template: `cos_double_radio`; seed: `17`.

Bank profile: `cos_double_negative_source`; source: `q-24575`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=-6\cos t,\qquad y=5\cos 2t,\qquad t\in[0,2\pi).
$$

- **A.** $y=5\left(\frac{1}{18}x^2-1\right)$
- **B.** $y=\frac{x^{2}}{12} + 1$
- **C.** $y=\frac{x^{2}}{36} - 1$
- **D.** $y=- \frac{x^{2}}{36} + 1$
- **E.** $y=11\left(\frac{x^{2}}{36} + 1\right)$

**Correct: A**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=-6\cos t & \Rightarrow\quad \cos t=-\frac{x}{6} \\
y=5\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{5}
\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=-\frac{x}{6}$ and $\cos 2t=\frac{y}{5}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{5} & =2\left(-\frac{x}{6}\right)^2-1 \\
\frac{y}{5} & =\frac{1}{18}x^2-1 \\
y & =5\left(\frac{1}{18}x^2-1\right)
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=5\left(\frac{1}{18}x^2-1\right).$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

## Generated — Hard
Template: `cos_double_radio`; seed: `29`.

Bank profile: `cos_double_negative_source`; source: `q-24575`.

Find the Cartesian equation of the curve defined parametrically as

$$
x=-6\cos t,\qquad y=2\cos 2t,\qquad t\in[0,2\pi).
$$

- **A.** $y=- \frac{x^{2}}{36} + 1$
- **B.** $y=\frac{x^{2}}{12} + 1$
- **C.** $y=\frac{x^{2}}{36} - 1$
- **D.** $y=2\left(\frac{1}{18}x^2-1\right)$
- **E.** $y=8\left(\frac{x^{2}}{36} + 1\right)$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=-6\cos t & \Rightarrow\quad \cos t=-\frac{x}{6} \\
y=2\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{2}
\end{aligned}
$$

Now, using double angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=-\frac{x}{6}$ and $\cos 2t=\frac{y}{2}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{2} & =2\left(-\frac{x}{6}\right)^2-1 \\
\frac{y}{2} & =\frac{1}{18}x^2-1 \\
y & =2\left(\frac{1}{18}x^2-1\right)
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=2\left(\frac{1}{18}x^2-1\right).$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

---

# cos_double_blank

## Original source — Hard — q-321314

Consider the curve defined parametrically as

$$
x=5\operatorname{cos}⁡t,\,\,\,y=-6\operatorname{cos}⁡2t,\,t\in [0,2\pi ).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $-\frac{12{x}^{2}}{25}+6$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=5\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=\frac{x}{5} \\ y=-6\operatorname{cos}⁡2t\, & ⇒\,\operatorname{cos}⁡2t=-\frac{y}{6}.\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}\operatorname{cos}⁡2t & ={cos}^{2}⁡t-{sin}^{2}⁡t \\  & ={cos}^{2}⁡t-(1-{cos}^{2}⁡t) \\  & =2{cos}^{2}⁡t-1.\end{aligned}
$$

Substituting $\operatorname{cos}⁡t=\frac{x}{5}$ and $\operatorname{cos}⁡2t=-\frac{y}{6}$ into this formula, we get

$$
\begin{aligned}-\frac{y}{6} & =2{(\frac{x}{5})}^{2}-1 \\ -\frac{y}{6} & =\frac{2{x}^{2}}{25}-1 \\ y & =-6(\frac{2{x}^{2}}{25}-1) \\ y & =-\frac{12{x}^{2}}{25}+6.\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=-\frac{12{x}^{2}}{25}+6.$

## Generated — Hard
Template: `cos_double_blank`; seed: `18`.

Consider the curve defined parametrically as

$$
x=3\cos t,\qquad y=2\cos 2t,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $\frac{4 x^{2}}{9} - 2$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=3\cos t & \Rightarrow\quad \cos t=\frac{x}{3} \\
y=2\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{2}
\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=\frac{x}{3}$ and $\cos 2t=\frac{y}{2}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{2} & =2\left(\frac{x}{3}\right)^2-1 \\
\frac{y}{2} & =2\left(\frac{x^2}{9}\right)-1 \\
\frac{y}{2} & =\frac{2}{9}x^2-1 \\
y & =2\left(\frac{2}{9}x^2-1\right) \\
y & =\frac{4 x^{2}}{9} - 2.
\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{4 x^{2}}{9} - 2.$

**Author metadata — curve restrictions:** $-3\le x\le 3$.

## Generated — Hard
Template: `cos_double_blank`; seed: `29`.

Consider the curve defined parametrically as

$$
x=6\cos t,\qquad y=2\cos 2t,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $\frac{x^{2}}{9} - 2$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=6\cos t & \Rightarrow\quad \cos t=\frac{x}{6} \\
y=2\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{2}
\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=\frac{x}{6}$ and $\cos 2t=\frac{y}{2}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{2} & =2\left(\frac{x}{6}\right)^2-1 \\
\frac{y}{2} & =2\left(\frac{x^2}{36}\right)-1 \\
\frac{y}{2} & =\frac{1}{18}x^2-1 \\
y & =2\left(\frac{1}{18}x^2-1\right) \\
y & =\frac{x^{2}}{9} - 2.
\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{x^{2}}{9} - 2.$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

---

# cos_double_blank

## Original source — Hard — q-321315

Consider the curve defined parametrically as

$$
x=-4\operatorname{cos}⁡t,\,\,\,y=3\operatorname{cos}⁡2t,\,t\in [0,2\pi ).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $\frac{3{x}^{2}}{8}-3$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=-4\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=-\frac{x}{4} \\ y=3\operatorname{cos}⁡2t\, & ⇒\,\operatorname{cos}⁡2t=\frac{y}{3}.\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}\operatorname{cos}⁡2t & ={cos}^{2}⁡t-{sin}^{2}⁡t \\  & ={cos}^{2}⁡t-(1-{cos}^{2}⁡t) \\  & =2{cos}^{2}⁡t-1.\end{aligned}
$$

Substituting $\operatorname{cos}⁡t=-\frac{x}{4}$ and $\operatorname{cos}⁡2t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}\frac{y}{3} & =2{(-\frac{x}{4})}^{2}-1 \\ \frac{y}{3} & =\frac{2{x}^{2}}{16}-1 \\ y & =3(\frac{{x}^{2}}{8}-1) \\ y & =\frac{3{x}^{2}}{8}-3\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{3{x}^{2}}{8}-3.$

## Generated — Hard
Template: `cos_double_blank`; seed: `19`.

Consider the curve defined parametrically as

$$
x=-2\cos t,\qquad y=-6\cos 2t,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $- 3 x^{2} + 6$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=-2\cos t & \Rightarrow\quad \cos t=-\frac{x}{2} \\
y=-6\cos 2t & \Rightarrow\quad \cos 2t=-\frac{y}{6}
\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=-\frac{x}{2}$ and $\cos 2t=-\frac{y}{6}$ into this formula, we get

$$
\begin{aligned}
-\frac{y}{6} & =2\left(-\frac{x}{2}\right)^2-1 \\
-\frac{y}{6} & =\frac{1}{2}x^2-1 \\
y & =-6\left(\frac{1}{2}x^2-1\right) \\
y & =- 3 x^{2} + 6.
\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=- 3 x^{2} + 6.$

**Author metadata — curve restrictions:** $-2\le x\le 2$.

## Generated — Hard
Template: `cos_double_blank`; seed: `30`.

Consider the curve defined parametrically as

$$
x=-6\cos t,\qquad y=-4\cos 2t,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $- \frac{2 x^{2}}{9} + 4$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=-6\cos t & \Rightarrow\quad \cos t=-\frac{x}{6} \\
y=-4\cos 2t & \Rightarrow\quad \cos 2t=-\frac{y}{4}
\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=-\frac{x}{6}$ and $\cos 2t=-\frac{y}{4}$ into this formula, we get

$$
\begin{aligned}
-\frac{y}{4} & =2\left(-\frac{x}{6}\right)^2-1 \\
-\frac{y}{4} & =\frac{1}{18}x^2-1 \\
y & =-4\left(\frac{1}{18}x^2-1\right) \\
y & =- \frac{2 x^{2}}{9} + 4.
\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=- \frac{2 x^{2}}{9} + 4.$

**Author metadata — curve restrictions:** $-6\le x\le 6$.

---

# cos_double_blank

## Original source — Hard — q-321318

Consider the curve defined parametrically as

$$
x=6\operatorname{cos}⁡t,\,\,\,y=5\operatorname{cos}⁡2t,\,t\in [0,2\pi ).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $\frac{5{x}^{2}}{18}-5$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}x=6\operatorname{cos}⁡t\, & ⇒\,\operatorname{cos}⁡t=\frac{x}{6} \\ y=5\operatorname{cos}⁡2t\, & ⇒\,\operatorname{cos}⁡2t=\frac{y}{5}.\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}\operatorname{cos}⁡2t & ={cos}^{2}⁡t-{sin}^{2}⁡t \\  & ={cos}^{2}⁡t-(1-{cos}^{2}⁡t) \\  & =2{cos}^{2}⁡t-1.\end{aligned}
$$

Substituting $\operatorname{cos}⁡t=\frac{x}{6}$ and $\operatorname{cos}⁡2t=\frac{y}{5}$ into this formula, we get

$$
\begin{aligned}\frac{y}{5} & =2{(\frac{x}{6})}^{2}-1 \\ \frac{y}{5} & =2(\frac{{x}^{2}}{36})-1 \\ \frac{y}{5} & =\frac{2{x}^{2}}{36}-1 \\ y & =5(\frac{{x}^{2}}{18}-1) \\ y & =\frac{5{x}^{2}}{18}-5\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{5{x}^{2}}{18}-5.$

## Generated — Hard
Template: `cos_double_blank`; seed: `20`.

Consider the curve defined parametrically as

$$
x=-3\cos t,\qquad y=4\cos 2t,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $\frac{8 x^{2}}{9} - 4$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=-3\cos t & \Rightarrow\quad \cos t=-\frac{x}{3} \\
y=4\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{4}
\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=-\frac{x}{3}$ and $\cos 2t=\frac{y}{4}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{4} & =2\left(-\frac{x}{3}\right)^2-1 \\
\frac{y}{4} & =\frac{2}{9}x^2-1 \\
y & =4\left(\frac{2}{9}x^2-1\right) \\
y & =\frac{8 x^{2}}{9} - 4.
\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{8 x^{2}}{9} - 4.$

**Author metadata — curve restrictions:** $-3\le x\le 3$.

## Generated — Hard
Template: `cos_double_blank`; seed: `31`.

Consider the curve defined parametrically as

$$
x=-2\cos t,\qquad y=5\cos 2t,\qquad t\in[0,2\pi).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

**Correct blank entry:** $\frac{5 x^{2}}{2} - 5$

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=-2\cos t & \Rightarrow\quad \cos t=-\frac{x}{2} \\
y=5\cos 2t & \Rightarrow\quad \cos 2t=\frac{y}{5}
\end{aligned}
$$

Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain

$$
\begin{aligned}
\cos 2t & =\cos^2 t-\sin^2 t \\
 & =\cos^2 t-(1-\cos^2 t) \\
 & =2\cos^2 t-1.
\end{aligned}
$$

Substituting $\cos t=-\frac{x}{2}$ and $\cos 2t=\frac{y}{5}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{5} & =2\left(-\frac{x}{2}\right)^2-1 \\
\frac{y}{5} & =\frac{1}{2}x^2-1 \\
y & =5\left(\frac{1}{2}x^2-1\right) \\
y & =\frac{5 x^{2}}{2} - 5.
\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{5 x^{2}}{2} - 5.$

**Author metadata — curve restrictions:** $-2\le x\le 2$.

---

# Authored moderate variations

All examples below are moderate multiple-choice questions with the same solution process; their display order is not an instructional sequence. The banks, cotangent counterparts, and quadrant variations are authored extensions. The two captured moderate originals and their faithful bank variants remain in [review.md](review.md).

## Generated — Moderate
Template: `sin_tan_radio`; seed: `71`.

Bank profile: `sin_tan_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t,\qquad y=3\tan t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y=\frac{x}{\sqrt{- x^{2} + 4}}$
- **B.** $y=\frac{6 x}{- x^{2} + 4}$
- **C.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **D.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **E.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t & \Rightarrow\quad \sin t=\frac{x}{2} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sin t}{\sqrt{1-\sin^2 t}}.
$$

Substituting $\sin t=\frac{x}{2}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{2}}{\sqrt{1-\left(\frac{x}{2}\right)^2}} \\
y & =\frac{3 x}{\sqrt{- x^{2} + 4}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 x}{\sqrt{- x^{2} + 4}}.$

**Author metadata — curve restrictions:** $0<x<2\quad y>0$.

---

## Generated — Moderate
Template: `sin_tan_radio`; seed: `72`.

Bank profile: `sin_tan_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t,\qquad y=3\tan t,\qquad \frac{\pi}{2}<t<\pi.
$$

- **A.** $y=- \frac{x}{\sqrt{- x^{2} + 4}}$
- **B.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **C.** $y=- \frac{6 x}{- x^{2} + 4}$
- **D.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **E.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$

**Correct: E**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t & \Rightarrow\quad \sin t=\frac{x}{2} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =-\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t<0$ in the range $\frac{\pi}{2}<t<\pi.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sin t}{-\sqrt{1-\sin^2 t}}.
$$

Substituting $\sin t=\frac{x}{2}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{2}}{-\sqrt{1-\left(\frac{x}{2}\right)^2}} \\
y & =- \frac{3 x}{\sqrt{- x^{2} + 4}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}.$

**Author metadata — curve restrictions:** $0<x<2\quad y<0$.

---

## Generated — Moderate
Template: `sin_tan_radio`; seed: `73`.

Bank profile: `sin_tan_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t,\qquad y=3\tan t,\qquad \pi<t<\frac{3\pi}{2}.
$$

- **A.** $y=- \frac{6 x}{- x^{2} + 4}$
- **B.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **C.** $y=- \frac{x}{\sqrt{- x^{2} + 4}}$
- **D.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **E.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t & \Rightarrow\quad \sin t=\frac{x}{2} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =-\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t<0$ in the range $\pi<t<\frac{3\pi}{2}.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sin t}{-\sqrt{1-\sin^2 t}}.
$$

Substituting $\sin t=\frac{x}{2}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{2}}{-\sqrt{1-\left(\frac{x}{2}\right)^2}} \\
y & =- \frac{3 x}{\sqrt{- x^{2} + 4}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}.$

**Author metadata — curve restrictions:** $-2<x<0\quad y>0$.

---

## Generated — Moderate
Template: `sin_tan_radio`; seed: `74`.

Bank profile: `sin_tan_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t,\qquad y=3\tan t,\qquad \frac{3\pi}{2}<t<2\pi.
$$

- **A.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **B.** $y=\frac{6 x}{- x^{2} + 4}$
- **C.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **D.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **E.** $y=\frac{x}{\sqrt{- x^{2} + 4}}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t & \Rightarrow\quad \sin t=\frac{x}{2} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t>0$ in the range $\frac{3\pi}{2}<t<2\pi.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sin t}{\sqrt{1-\sin^2 t}}.
$$

Substituting $\sin t=\frac{x}{2}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{2}}{\sqrt{1-\left(\frac{x}{2}\right)^2}} \\
y & =\frac{3 x}{\sqrt{- x^{2} + 4}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 x}{\sqrt{- x^{2} + 4}}.$

**Author metadata — curve restrictions:** $-2<x<0\quad y<0$.

---

## Generated — Moderate
Template: `cos_tan_radio`; seed: `71`.

Bank profile: `cos_tan_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\cos t,\qquad y=3\tan t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y=\frac{\sqrt{- x^{2} + 4}}{x}$
- **B.** $y=\frac{3 \left(- x^{2} + 4\right)}{2 x}$
- **C.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **D.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **E.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\cos t & \Rightarrow\quad \cos t=\frac{x}{2} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sqrt{1-\cos^2 t}}{\cos t}.
$$

Substituting $\cos t=\frac{x}{2}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\sqrt{1-\left(\frac{x}{2}\right)^2}}{\frac{x}{2}} \\
y & =\frac{3 \sqrt{- x^{2} + 4}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 \sqrt{- x^{2} + 4}}{x}.$

**Author metadata — curve restrictions:** $0<x<2\quad y>0$.

---

## Generated — Moderate
Template: `cos_tan_radio`; seed: `72`.

Bank profile: `cos_tan_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\cos t,\qquad y=3\tan t,\qquad \frac{\pi}{2}<t<\pi.
$$

- **A.** $y=\frac{\sqrt{- x^{2} + 4}}{x}$
- **B.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **C.** $y=\frac{3 \left(- x^{2} + 4\right)}{2 x}$
- **D.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **E.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$

**Correct: E**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\cos t & \Rightarrow\quad \cos t=\frac{x}{2} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t>0$ in the range $\frac{\pi}{2}<t<\pi.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{\sqrt{1-\cos^2 t}}{\cos t}.
$$

Substituting $\cos t=\frac{x}{2}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\sqrt{1-\left(\frac{x}{2}\right)^2}}{\frac{x}{2}} \\
y & =\frac{3 \sqrt{- x^{2} + 4}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 \sqrt{- x^{2} + 4}}{x}.$

**Author metadata — curve restrictions:** $-2<x<0\quad y<0$.

---

## Generated — Moderate
Template: `cos_tan_radio`; seed: `73`.

Bank profile: `cos_tan_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\cos t,\qquad y=3\tan t,\qquad \pi<t<\frac{3\pi}{2}.
$$

- **A.** $y=- \frac{3 \left(- x^{2} + 4\right)}{2 x}$
- **B.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **C.** $y=- \frac{\sqrt{- x^{2} + 4}}{x}$
- **D.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **E.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\cos t & \Rightarrow\quad \cos t=\frac{x}{2} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =-\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t<0$ in the range $\pi<t<\frac{3\pi}{2}.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{-\sqrt{1-\cos^2 t}}{\cos t}.
$$

Substituting $\cos t=\frac{x}{2}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{-\sqrt{1-\left(\frac{x}{2}\right)^2}}{\frac{x}{2}} \\
y & =- \frac{3 \sqrt{- x^{2} + 4}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}.$

**Author metadata — curve restrictions:** $-2<x<0\quad y>0$.

---

## Generated — Moderate
Template: `cos_tan_radio`; seed: `74`.

Bank profile: `cos_tan_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\cos t,\qquad y=3\tan t,\qquad \frac{3\pi}{2}<t<2\pi.
$$

- **A.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **B.** $y=- \frac{3 \left(- x^{2} + 4\right)}{2 x}$
- **C.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **D.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **E.** $y=- \frac{\sqrt{- x^{2} + 4}}{x}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\cos t & \Rightarrow\quad \cos t=\frac{x}{2} \\
y=3\tan t & \Rightarrow\quad \tan t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =-\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t<0$ in the range $\frac{3\pi}{2}<t<2\pi.$

Now, using the definition of a tangent, we obtain

$$
\tan t=\frac{\sin t}{\cos t}=\frac{-\sqrt{1-\cos^2 t}}{\cos t}.
$$

Substituting $\cos t=\frac{x}{2}$ and $\tan t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{-\sqrt{1-\left(\frac{x}{2}\right)^2}}{\frac{x}{2}} \\
y & =- \frac{3 \sqrt{- x^{2} + 4}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}.$

**Author metadata — curve restrictions:** $0<x<2\quad y<0$.

---

## Generated — Moderate
Template: `sin_cot_radio`; seed: `71`.

Bank profile: `sin_cot_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t,\qquad y=3\cot t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y=\frac{\sqrt{- x^{2} + 4}}{x}$
- **B.** $y=\frac{3 \left(- x^{2} + 4\right)}{2 x}$
- **C.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **D.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **E.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t & \Rightarrow\quad \sin t=\frac{x}{2} \\
y=3\cot t & \Rightarrow\quad \cot t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, using the definition of a cotangent, we obtain

$$
\cot t=\frac{\cos t}{\sin t}=\frac{\sqrt{1-\sin^2 t}}{\sin t}.
$$

Substituting $\sin t=\frac{x}{2}$ and $\cot t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\sqrt{1-\left(\frac{x}{2}\right)^2}}{\frac{x}{2}} \\
y & =\frac{3 \sqrt{- x^{2} + 4}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 \sqrt{- x^{2} + 4}}{x}.$

**Author metadata — curve restrictions:** $0<x<2\quad y>0$.

---

## Generated — Moderate
Template: `sin_cot_radio`; seed: `72`.

Bank profile: `sin_cot_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t,\qquad y=3\cot t,\qquad \frac{\pi}{2}<t<\pi.
$$

- **A.** $y=- \frac{\sqrt{- x^{2} + 4}}{x}$
- **B.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **C.** $y=- \frac{3 \left(- x^{2} + 4\right)}{2 x}$
- **D.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **E.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$

**Correct: E**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t & \Rightarrow\quad \sin t=\frac{x}{2} \\
y=3\cot t & \Rightarrow\quad \cot t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =-\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t<0$ in the range $\frac{\pi}{2}<t<\pi.$

Now, using the definition of a cotangent, we obtain

$$
\cot t=\frac{\cos t}{\sin t}=\frac{-\sqrt{1-\sin^2 t}}{\sin t}.
$$

Substituting $\sin t=\frac{x}{2}$ and $\cot t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{-\sqrt{1-\left(\frac{x}{2}\right)^2}}{\frac{x}{2}} \\
y & =- \frac{3 \sqrt{- x^{2} + 4}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}.$

**Author metadata — curve restrictions:** $0<x<2\quad y<0$.

---

## Generated — Moderate
Template: `sin_cot_radio`; seed: `73`.

Bank profile: `sin_cot_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t,\qquad y=3\cot t,\qquad \pi<t<\frac{3\pi}{2}.
$$

- **A.** $y=- \frac{3 \left(- x^{2} + 4\right)}{2 x}$
- **B.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **C.** $y=- \frac{\sqrt{- x^{2} + 4}}{x}$
- **D.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **E.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t & \Rightarrow\quad \sin t=\frac{x}{2} \\
y=3\cot t & \Rightarrow\quad \cot t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =-\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t<0$ in the range $\pi<t<\frac{3\pi}{2}.$

Now, using the definition of a cotangent, we obtain

$$
\cot t=\frac{\cos t}{\sin t}=\frac{-\sqrt{1-\sin^2 t}}{\sin t}.
$$

Substituting $\sin t=\frac{x}{2}$ and $\cot t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{-\sqrt{1-\left(\frac{x}{2}\right)^2}}{\frac{x}{2}} \\
y & =- \frac{3 \sqrt{- x^{2} + 4}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}.$

**Author metadata — curve restrictions:** $-2<x<0\quad y>0$.

---

## Generated — Moderate
Template: `sin_cot_radio`; seed: `74`.

Bank profile: `sin_cot_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\sin t,\qquad y=3\cot t,\qquad \frac{3\pi}{2}<t<2\pi.
$$

- **A.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **B.** $y=\frac{3 \left(- x^{2} + 4\right)}{2 x}$
- **C.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **D.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **E.** $y=\frac{\sqrt{- x^{2} + 4}}{x}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\sin t & \Rightarrow\quad \sin t=\frac{x}{2} \\
y=3\cot t & \Rightarrow\quad \cot t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\cos^2 t & =1-\sin^2 t \\
\cos t & =\sqrt{1-\sin^2 t}.
\end{aligned}
$$

We used here that $\cos t>0$ in the range $\frac{3\pi}{2}<t<2\pi.$

Now, using the definition of a cotangent, we obtain

$$
\cot t=\frac{\cos t}{\sin t}=\frac{\sqrt{1-\sin^2 t}}{\sin t}.
$$

Substituting $\sin t=\frac{x}{2}$ and $\cot t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\sqrt{1-\left(\frac{x}{2}\right)^2}}{\frac{x}{2}} \\
y & =\frac{3 \sqrt{- x^{2} + 4}}{x}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 \sqrt{- x^{2} + 4}}{x}.$

**Author metadata — curve restrictions:** $-2<x<0\quad y<0$.

---

## Generated — Moderate
Template: `cos_cot_radio`; seed: `71`.

Bank profile: `cos_cot_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\cos t,\qquad y=3\cot t,\qquad 0<t<\frac{\pi}{2}.
$$

- **A.** $y=\frac{x}{\sqrt{- x^{2} + 4}}$
- **B.** $y=\frac{6 x}{- x^{2} + 4}$
- **C.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **D.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **E.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\cos t & \Rightarrow\quad \cos t=\frac{x}{2} \\
y=3\cot t & \Rightarrow\quad \cot t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t>0$ in the range $0<t<\frac{\pi}{2}.$

Now, using the definition of a cotangent, we obtain

$$
\cot t=\frac{\cos t}{\sin t}=\frac{\cos t}{\sqrt{1-\cos^2 t}}.
$$

Substituting $\cos t=\frac{x}{2}$ and $\cot t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{2}}{\sqrt{1-\left(\frac{x}{2}\right)^2}} \\
y & =\frac{3 x}{\sqrt{- x^{2} + 4}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 x}{\sqrt{- x^{2} + 4}}.$

**Author metadata — curve restrictions:** $0<x<2\quad y>0$.

---

## Generated — Moderate
Template: `cos_cot_radio`; seed: `72`.

Bank profile: `cos_cot_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\cos t,\qquad y=3\cot t,\qquad \frac{\pi}{2}<t<\pi.
$$

- **A.** $y=\frac{x}{\sqrt{- x^{2} + 4}}$
- **B.** $y=\frac{3 \sqrt{- x^{2} + 4}}{x}$
- **C.** $y=\frac{6 x}{- x^{2} + 4}$
- **D.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **E.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$

**Correct: E**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\cos t & \Rightarrow\quad \cos t=\frac{x}{2} \\
y=3\cot t & \Rightarrow\quad \cot t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t>0$ in the range $\frac{\pi}{2}<t<\pi.$

Now, using the definition of a cotangent, we obtain

$$
\cot t=\frac{\cos t}{\sin t}=\frac{\cos t}{\sqrt{1-\cos^2 t}}.
$$

Substituting $\cos t=\frac{x}{2}$ and $\cot t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{2}}{\sqrt{1-\left(\frac{x}{2}\right)^2}} \\
y & =\frac{3 x}{\sqrt{- x^{2} + 4}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{3 x}{\sqrt{- x^{2} + 4}}.$

**Author metadata — curve restrictions:** $-2<x<0\quad y<0$.

---

## Generated — Moderate
Template: `cos_cot_radio`; seed: `73`.

Bank profile: `cos_cot_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\cos t,\qquad y=3\cot t,\qquad \pi<t<\frac{3\pi}{2}.
$$

- **A.** $y=- \frac{6 x}{- x^{2} + 4}$
- **B.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **C.** $y=- \frac{x}{\sqrt{- x^{2} + 4}}$
- **D.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **E.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\cos t & \Rightarrow\quad \cos t=\frac{x}{2} \\
y=3\cot t & \Rightarrow\quad \cot t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =-\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t<0$ in the range $\pi<t<\frac{3\pi}{2}.$

Now, using the definition of a cotangent, we obtain

$$
\cot t=\frac{\cos t}{\sin t}=\frac{\cos t}{-\sqrt{1-\cos^2 t}}.
$$

Substituting $\cos t=\frac{x}{2}$ and $\cot t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{2}}{-\sqrt{1-\left(\frac{x}{2}\right)^2}} \\
y & =- \frac{3 x}{\sqrt{- x^{2} + 4}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}.$

**Author metadata — curve restrictions:** $-2<x<0\quad y>0$.

---

## Generated — Moderate
Template: `cos_cot_radio`; seed: `74`.

Bank profile: `cos_cot_variation`; authored variation; method adapted from the two moderate sources.

*Coefficients vary from the unit-coefficient moderate sources.*

Find the Cartesian equation of the curve defined parametrically as

$$
x=2\cos t,\qquad y=3\cot t,\qquad \frac{3\pi}{2}<t<2\pi.
$$

- **A.** $y=- \frac{3 \sqrt{- x^{2} + 4}}{x}$
- **B.** $y=- \frac{6 x}{- x^{2} + 4}$
- **C.** $y=\frac{3 x}{\sqrt{- x^{2} + 4}}$
- **D.** $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}$
- **E.** $y=- \frac{x}{\sqrt{- x^{2} + 4}}$

**Correct: D**

**Worked solution**

First, let's make the trigonometric functions the subject of each equation:

$$
\begin{aligned}
x=2\cos t & \Rightarrow\quad \cos t=\frac{x}{2} \\
y=3\cot t & \Rightarrow\quad \cot t=\frac{y}{3}
\end{aligned}
$$

Using the Pythagorean identity $\sin^2 t+\cos^2 t=1$, we get

$$
\begin{aligned}
\sin^2 t+\cos^2 t & =1 \\
\sin^2 t & =1-\cos^2 t \\
\sin t & =-\sqrt{1-\cos^2 t}.
\end{aligned}
$$

We used here that $\sin t<0$ in the range $\frac{3\pi}{2}<t<2\pi.$

Now, using the definition of a cotangent, we obtain

$$
\cot t=\frac{\cos t}{\sin t}=\frac{\cos t}{-\sqrt{1-\cos^2 t}}.
$$

Substituting $\cos t=\frac{x}{2}$ and $\cot t=\frac{y}{3}$ into this formula, we get

$$
\begin{aligned}
\frac{y}{3} & =\frac{\frac{x}{2}}{-\sqrt{1-\left(\frac{x}{2}\right)^2}} \\
y & =- \frac{3 x}{\sqrt{- x^{2} + 4}}.
\end{aligned}
$$

So the Cartesian equation of the given curve is $y=- \frac{3 x}{\sqrt{- x^{2} + 4}}.$

**Author metadata — curve restrictions:** $0<x<2\quad y<0$.

---

