# Template extraction

Fidelity and source-error handling: `raw-source-replay.json` reproduces every MA attribute exactly, including raw TeX, absent data, original bank ordering, correct markers and source difficulty. Raw records are evidence-only and never serving eligible. Seven complete cases serve normalized prose/math at original parameters with the full observed bank and exact ordered source solution; `source-replay.json` compares complete equations up to nonzero scalar multiplication. Two incomplete cases have separately authored solutions/keys, and q-214033 an authored blank answer. No completion is represented as captured evidence. All source and complete authored solutions appear side-by-side in `review.md`; `sourcecases.json` includes original+two variants for each of the nine families, plus three examples for each hard family.

Backbone: extract the supplied reference slope (standard form, or the slope formula on two integer points), take its negative reciprocal, use the actual supplied target point in point-slope form, expand and isolate y, and finish standard form only where the source does. Real coordinate plane. Source slopes are finite and nonzero; A,B are both nonzero because horizontal/vertical lines require a different solution branch absent from these sources and introduction. This scope restriction is independent of grading; the complete-equation comparator itself supports both axes. Target coordinates and answer intercepts can be zero or one. No arbitrary exclusions for valid 0/1 answers.

Declared variable slots: reference standard coefficients A,B independently chosen nonzero integers [-7,7], C integers [-12,12]; target px,py independently [-9,9]. For the two-point family reference point 1 is independently in [-5,5]^2 and dx,dy independently nonzero integers [-7,7]; point 2=point 1+(dx,dy), A=dy, B=-dx, C=A*x1+B*y1. Parameters passed explicitly use integers of absolute magnitude at most 100 for A,B,C,px,py and must preserve all structural relations. All references, slopes, banks and worked equations are derived from the same slots. Reference orientations and both point coordinates vary; translation alone is insufficient novelty. Within each source-template family, all variations keep the same reasoning stages/workload. Arithmetic formatting may repeat an equal stage, preserving the source's explicit stages rather than deleting a source row as redundant.

Every bank is chosen as one complete source profile BEFORE sampling. One profile per radio source (four total, including incomplete q-23633); no pooled recipes or first-valid subsets. Define old perpendicular normal (a0,b0)=(-B0,A0), new (a,b)=(-B,A). For each complete observed option (oa,ob,oc), derive na=oa*a/a0, nb=ob*b/b0, residual=oc-oa*px0-ob*py0, nc=na*px+nb*py+residual. Clear all coefficient denominators by their positive LCM and render the entire equivalent integer standard equation na*x+nb*y=nc. This exact incidence-residual transport is an authored, conservative algebraic extension of observed coefficient patterns. Its psychological interpretation is unresolved; it is NOT claimed to identify particular learner misconceptions. Full-bank collisions/extra-correct choices reject the entire instance. Source replay retains the original notation; variants use normalized exact coefficients. Blank profiles have no distractors, and retain RHS-only y= contract.

Per-source complete mappings below give original point/reference, prompt, each full equation, exact na/a and nb/b multipliers, and constant residual. These are complete recipes, not qualitative labels. Raw worked prose and all ordered equations remain in source.json and the review, not replaced by the recipe summary.

## q-214033

What is the equation of the line that passes through the point $(1,-5)$ and is perpendicular to $x + 3y = 12$?$y =$
{{field-1}}

Parameters: `{"A": 1, "B": 3, "C": 12, "px": 1, "py": -5}`. Field field-1 / :answer-field.type/blank.

Observed RHS: missing (authored completion `3x-8`).

Ordered source solution (missing remains missing here):

**Missing: authored completion is separate.**

## q-23633

Find the equation of the line that passes through the point $(-3,-2)$ and is perpendicular to the line passing through the points $(2, 6)$ and $(-3, 1)$.

Parameters: `{"A": -5, "B": 5, "C": 20, "px": -3, "py": -2, "points": [[2, 6], [-3, 1]]}`. Field selection / :answer-field.type/radio.

| Observed full option | na/a | nb/b | residual | Captured key |
|---|---|---|---|---|
|`x + y =-5`|-1/5|-1/5|0|False|
|`2x - y =-4`|-2/5|1/5|0|False|
|`2x + 3y = 0`|-2/5|-3/5|12|False|
|`x + y =-1`|-1/5|-1/5|4|False|
|`x - y =-1`|-1/5|1/5|0|False|

Ordered source solution (missing remains missing here):

**Missing: authored completion is separate.**

## q-103449

Find the equation of the line that passes through the point $(-2,2)$ and is perpendicular to the line passing through the points $(1,-1)$ and $(4,1).$

Parameters: `{"A": 2, "B": -3, "C": 5, "px": -2, "py": 2, "points": [[1, -1], [4, 1]]}`. Field selection / :answer-field.type/radio.

| Observed full option | na/a | nb/b | residual | Captured key |
|---|---|---|---|---|
|`3x+y=-4`|1|1/2|0|False|
|`3x-2y=-10`|1|-1|0|False|
|`x+2y=2`|1/3|1|0|False|
|`x-2y=-6`|1/3|-1|0|False|
|`3x+2y=-2`|1|1|0|True|

Ordered source solution (missing remains missing here):

Perpendicular lines have slopes which are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(1,-1)$ and $(4,1):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{1-(-1)}{4-1} \\  & =\frac{1+1}{4-1} \\  & =\frac{2}{3}\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (\frac{2}{3})=-1\,⇒\,m=-\frac{3}{2}.
$$

We know that the line passes through the point $(-2,2).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-2 & =-\frac{3}{2}(x-(-2)) \\ y-2 & =-\frac{3}{2}(x+2) \\ y-2 & =-\frac{3}{2}x-3 \\ y & =-\frac{3}{2}x-1\end{aligned}
$$

However, we want to write the equation in standard form. So, we will bring the $x$ term to the left-hand side and multiply both sides of the equation by $2:$

$$
\begin{aligned}y & =-\frac{3}{2}x-1 \\ \frac{3}{2}x+y & =-1 \\ 2\cdot (\frac{3}{2}x+y) & =2\cdot (-1) \\ 3x+2y & =-2\end{aligned}
$$

## q-23631

Find the equation of the line containing the point $(-1,1)$ that is perpendicular to $2x-3y=-5.$

Parameters: `{"A": 2, "B": -3, "C": -5, "px": -1, "py": 1}`. Field selection / :answer-field.type/radio.

| Observed full option | na/a | nb/b | residual | Captured key |
|---|---|---|---|---|
|`3x-2y=-5`|1|-1|0|False|
|`x+y=0`|1/3|1/2|0|False|
|`2x+3y=1`|2/3|3/2|0|False|
|`2x-3y=-5`|2/3|-3/2|0|False|
|`3x+2y=-1`|1|1|0|True|

Ordered source solution (missing remains missing here):

First, we write the equation $2x-3y=-5$ in its slope-intercept form, as follows:

$$
\begin{aligned}2x-3y & =-5 \\ -3y & =-2x-5 \\ y & =\frac{2}{3}x+\frac{5}{3}\end{aligned}
$$

Since perpendicular lines have slopes that are negative reciprocals of each other, the slope of the new line should be the negative reciprocal of the slope of the given line $y=\frac{2}{3}x+\frac{5}{3}.$ The given line has a slope of $\frac{2}{3},$ so our perpendicular line must have a slope of $-\frac{3}{2}.$

Our perpendicular line must have the slope $m=-\frac{3}{2}$ and pass through the point $({x}_{1},{y}_{1})=(-1,1).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-1 & =-\frac{3}{2}(x-(-1)) \\ y-1 & =-\frac{3}{2}(x+1) \\ y-1 & =-\frac{3}{2}x-\frac{3}{2} \\ y & =-\frac{3}{2}x-\frac{1}{2} \\ 2y & =-3x-1 \\ 3x+2y & =-1\end{aligned}
$$

## q-237230

What is the equation of the line that passes through the point $(-4,3)$ and is perpendicular to $5x+y=2?$

$y=$
{{field-1}}

Parameters: `{"A": 5, "B": 1, "C": 2, "px": -4, "py": 3}`. Field field-1 / :answer-field.type/blank.

Observed RHS: `\frac{1}{5}x+\frac{19}{5}`.

Ordered source solution (missing remains missing here):

First, we write the equation $5x+y=2$ in its slope-intercept form as follows:

$$
\begin{aligned}5x+y & =2 \\ y & =-5x+2\end{aligned}
$$

Since perpendicular lines have slopes that are negative reciprocals of each other, the slope of the new line should be the negative reciprocal of the slope of the given line $y=-5x+2.$ The given line has a slope of $-5,$ so our perpendicular line must have a slope of $\frac{1}{5}.$

Our perpendicular line must have the slope $m=\frac{1}{5}$ and pass through the point $({x}_{1},{y}_{1})=(-4,3).$ Using point-slope form and simplifying, we obtain the equation of the line in slope-intercept form:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-3 & =\frac{1}{5}(x-(-4)) \\ y-3 & =\frac{1}{5}(x+4) \\ y-3 & =\frac{1}{5}x+\frac{4}{5} \\ y & =\frac{1}{5}x+\frac{19}{5}\end{aligned}
$$

## q-237231

What is the equation of the line that passes through the point $(-7,0)$ and is perpendicular to $x-6y=-3?$

$y=$
{{field-1}}

Parameters: `{"A": 1, "B": -6, "C": -3, "px": -7, "py": 0}`. Field field-1 / :answer-field.type/blank.

Observed RHS: `-6x-42`.

Ordered source solution (missing remains missing here):

First, we write the equation $x-6y=-3$ in its slope-intercept form as follows:

$$
\begin{aligned}x-6y & =-3 \\ -6y & =-x-3 \\ y & =\frac{1}{6}x+\frac{1}{2}\end{aligned}
$$

Since perpendicular lines have slopes that are negative reciprocals of each other, the slope of the new line should be the negative reciprocal of the slope of the given line $y=\frac{1}{6}x+\frac{1}{2}.$ The given line has a slope of $\frac{1}{6},$ so our perpendicular line must have a slope of $-6.$

Our perpendicular line must have the slope $m=-6$ and pass through the point $({x}_{1},{y}_{1})=(-7,0).$ Using point-slope form and simplifying, we obtain the equation of the line in slope-intercept form:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-0 & =-6(x-(-7)) \\ y & =-6(x+7) \\ y & =-6x-42\end{aligned}
$$

## q-237232

What is the equation of the line that passes through the point $(1,1)$ and is perpendicular to $4x-3y=7?$

$y=$
{{field-1}}

Parameters: `{"A": 4, "B": -3, "C": 7, "px": 1, "py": 1}`. Field field-1 / :answer-field.type/blank.

Observed RHS: `-\frac{3}{4}x+\frac{7}{4}`.

Ordered source solution (missing remains missing here):

First, we write the equation $4x-3y=7$ in its slope-intercept form as follows:

$$
\begin{aligned}4x-3y & =7 \\ -3y & =-4x+7 \\ y & =\frac{4}{3}x-\frac{7}{3}\end{aligned}
$$

Since perpendicular lines have slopes that are negative reciprocals of each other, the slope of the new line should be the negative reciprocal of the slope of the given line $y=\frac{4}{3}x-\frac{7}{3}.$ The given line has a slope of $\frac{4}{3},$ so our perpendicular line must have a slope of $-\frac{3}{4}.$

Our perpendicular line must have the slope $m=-\frac{3}{4}$ and pass through the point $({x}_{1},{y}_{1})=(1,1).$ Using point-slope form and simplifying, we obtain the equation of the line in slope-intercept form:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-1 & =-\frac{3}{4}(x-1) \\ y-1 & =-\frac{3}{4}x+\frac{3}{4} \\ y & =-\frac{3}{4}x+\frac{7}{4}\end{aligned}
$$

## q-252524

Find the equation of the line that passes through the point $(3,4)$ and is perpendicular to the line passing through the points $(2,2)$ and $(5,8).$

Parameters: `{"A": 6, "B": -3, "C": 6, "px": 3, "py": 4, "points": [[2, 2], [5, 8]]}`. Field selection / :answer-field.type/radio.

| Observed full option | na/a | nb/b | residual | Captured key |
|---|---|---|---|---|
|`2x-y=2`|2/3|-1/6|0|False|
|`2x+5y=26`|2/3|5/6|0|False|
|`2x+y=10`|2/3|1/6|0|False|
|`x+2y=11`|1/3|1/3|0|True|
|`x+4y=19`|1/3|2/3|0|False|

Ordered source solution (missing remains missing here):

Perpendicular lines have slopes, which are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(2,2)$ and $(5,8):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{8-2}{5-2} \\  & =\frac{6}{3} \\  & =2\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (2)=-1\,⇒\,m=-\frac{1}{2}.
$$

We know that the line passes through the point $(3,4).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-4 & =-\frac{1}{2}(x-3) \\ 2(y-4) & =-(x-3) \\ 2y-8 & =-x+3 \\ 2y & =-x+11 \\ y & =-\frac{1}{2}x+\frac{11}{2}\end{aligned}
$$

However, we want to write the equation in standard form. So, we will bring the $x$ term to the left-hand side and multiply both sides of the equation by $2:$

$$
\begin{aligned}y & =-\frac{1}{2}x+\frac{11}{2} \\ \frac{1}{2}x+y & =\frac{11}{2} \\ 2\cdot (\frac{1}{2}x+y) & =2\cdot \frac{11}{2} \\ x+2y & =11\end{aligned}
$$

## q-72571

Find the equation of the line that passes through the point $(5,1)$ and is perpendicular to the line passing through the points $(1,5)$ and $(-3,-1).$

Parameters: `{"A": -6, "B": 4, "C": 14, "px": 5, "py": 1, "points": [[1, 5], [-3, -1]]}`. Field selection / :answer-field.type/radio.

| Observed full option | na/a | nb/b | residual | Captured key |
|---|---|---|---|---|
|`2x-3y=7`|-1/2|1/2|0|False|
|`x+y=6`|-1/4|-1/6|0|False|
|`2x-3y=5`|-1/2|1/2|-2|False|
|`2x+3y=13`|-1/2|-1/2|0|True|
|`2x+3y=7`|-1/2|-1/2|-6|False|

Ordered source solution (missing remains missing here):

Perpendicular lines have slopes which are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(1,5)$ and $(-3,-1):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{-1-5}{-3-1} \\  & =\frac{-6}{-4} \\  & =\frac{3}{2}\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (\frac{3}{2})=-1\,⇒\,m=-\frac{2}{3}.
$$

We know that the line passes through the point $(5,1).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-1 & =-\frac{2}{3}(x-5) \\ y-1 & =-\frac{2}{3}x+\frac{10}{3} \\ y & =-\frac{2}{3}x+\frac{13}{3}\end{aligned}
$$

However, we want to write the equation in standard form. So, we will bring the $x$ term to the left-hand side and multiply both sides of the equation by $3:$

$$
\begin{aligned}y & =-\frac{2}{3}x+\frac{13}{3} \\ \frac{2}{3}x+y & =\frac{13}{3} \\ 3\cdot (\frac{2}{3}x+y) & =3\cdot \frac{13}{3} \\ 2x+3y & =13\end{aligned}
$$

