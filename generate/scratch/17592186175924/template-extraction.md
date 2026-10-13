# Template extraction

General pattern: derive reference slope, take the negative reciprocal, use target point in point-slope form, expand, and return an RHS blank or standard-form radio line. All variables real; reference slope nonzero and finite. No horizontal/vertical branch extensions.

One template per original source layout and worked-solution sequence. Fixed: reference equation or two defining points, target x, prose, field key/type, source bank profile. Variable: target y becomes v+t for integer t in [-8,8]. Observed signed values and all source parameters appear at t=0. The bounded sampling policy is narrower than all possible lines, explicitly limiting to observed directions and vertical target translations.

Every radio choice a*x+b*y=c becomes a*x+b*y=c+b*t. This transforms the complete mathematical line and reproduces every original option at t=0, up to nonzero scale. It translates the correct line and all distractors together; mistake interpretation unresolved. No invented mistake labels or pooled recipes. Blanks return m*x+(v+t-m*u), m=-1/reference_slope, without equation or delimiters. Reject inequivalent-bank collisions and ambiguous keys.

Every source field and choice is mapped below, including observed values and exact transformation. Every source is replayed, including missing keys/solutions as explicitly authored additions. Source supplied solutions remain exact at replay. Variant solutions preserve slope, negative reciprocal, point-slope expansion and standard-form conversion sequences and instructional sentences, with streamlined parentheses/expansion rows: do not claim exact variant layout fidelity. No feedback added. All profiles and all bounded parameter values are exercised. Source values, sampling policy and fidelity limits remain separate.

## q-214033

DB 17592186176417; level easy; target (1, -5); standard reference (1, 3, 12) or two-point reference None; reference slope -1/3. Field 17592186174740, key field-1, type :answer-field.type/blank; bank profile none.

What is the equation of the line that passes through the point $(1,-5)$ and is perpendicular to $x + 3y = 12$?$y =$
{{field-1}}

Source key missing; derived addition; source solution missing, authored addition.

Fixed original solution:

Absent.

## q-23633

DB 17592186176432; level moderate; target (-3, -2); standard reference None or two-point reference ((2, 6), (-3, 1)); reference slope 1. Field 17592186174772, key selection, type :answer-field.type/radio; bank profile q-23633.

Find the equation of the line that passes through the point $(-3,-2)$ and is perpendicular to the line passing through the points $(2, 6)$ and $(-3, 1)$.

Source key missing; derived addition; source solution missing, authored addition.

- Source answer 17592186174773, field 17592186174772, exact value `x + y =-5`; recipe `1*x+(1)*y=-5+(1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23633.

- Source answer 17592186174774, field 17592186174772, exact value `2x - y =-4`; recipe `2*x+(-1)*y=-4+(-1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23633.

- Source answer 17592186174775, field 17592186174772, exact value `2x + 3y = 0`; recipe `2*x+(3)*y=0+(3)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23633.

- Source answer 17592186174776, field 17592186174772, exact value `x + y =-1`; recipe `1*x+(1)*y=-1+(1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23633.

- Source answer 17592186174777, field 17592186174772, exact value `x - y =-1`; recipe `1*x+(-1)*y=-1+(-1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23633.

Fixed original solution:

Absent.

## q-103449

DB 17592186238009; level moderate; target (-2, 2); standard reference None or two-point reference ((1, -1), (4, 1)); reference slope 2/3. Field 17592186237683, key selection, type :answer-field.type/radio; bank profile q-103449.

Find the equation of the line that passes through the point $(-2,2)$ and is perpendicular to the line passing through the points $(1,-1)$ and $(4,1).$

Source key present and verified; source solution present, exact replay.

- Source answer 17592186235858, field 17592186237683, exact value `3x+y=-4`; recipe `3*x+(1)*y=-4+(1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-103449.

- Source answer 17592186236143, field 17592186237683, exact value `3x-2y=-10`; recipe `3*x+(-2)*y=-10+(-2)*t`; reproduces entire original mathematical value at t=0: yes; profile q-103449.

- Source answer 17592186237036, field 17592186237683, exact value `x+2y=2`; recipe `1*x+(2)*y=2+(2)*t`; reproduces entire original mathematical value at t=0: yes; profile q-103449.

- Source answer 17592186237119, field 17592186237683, exact value `x-2y=-6`; recipe `1*x+(-2)*y=-6+(-2)*t`; reproduces entire original mathematical value at t=0: yes; profile q-103449.

- Source answer 17592186237390, field 17592186237683, exact value `3x+2y=-2`; recipe `3*x+(2)*y=-2+(2)*t`; reproduces entire original mathematical value at t=0: yes; profile q-103449.

Fixed original solution:

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

DB 17592186290470; level easy; target (-1, 1); standard reference (2, -3, -5) or two-point reference None; reference slope 2/3. Field 17592186290223, key selection, type :answer-field.type/radio; bank profile q-23631.

Find the equation of the line containing the point $(-1,1)$ that is perpendicular to $2x-3y=-5.$

Source key present and verified; source solution present, exact replay.

- Source answer 17592186288209, field 17592186290223, exact value `3x-2y=-5`; recipe `3*x+(-2)*y=-5+(-2)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23631.

- Source answer 17592186288552, field 17592186290223, exact value `x+y=0`; recipe `1*x+(1)*y=0+(1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23631.

- Source answer 17592186288663, field 17592186290223, exact value `2x+3y=1`; recipe `2*x+(3)*y=1+(3)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23631.

- Source answer 17592186288741, field 17592186290223, exact value `2x-3y=-5`; recipe `2*x+(-3)*y=-5+(-3)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23631.

- Source answer 17592186289064, field 17592186290223, exact value `3x+2y=-1`; recipe `3*x+(2)*y=-1+(2)*t`; reproduces entire original mathematical value at t=0: yes; profile q-23631.

Fixed original solution:

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

DB 17592186290500; level easy; target (-4, 3); standard reference (5, 1, 2) or two-point reference None; reference slope -5. Field 17592186289950, key field-1, type :answer-field.type/blank; bank profile none.

What is the equation of the line that passes through the point $(-4,3)$ and is perpendicular to $5x+y=2?$

$y=$
{{field-1}}

Source key present and verified; source solution present, exact replay.

- Source answer 17592186288506, field 17592186289950, exact value `\frac{1}{5}x+\frac{19}{5}`; recipe `m*x+(v+t-m*u), RHS only`; reproduces entire original mathematical value at t=0: yes; profile none.

Fixed original solution:

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

DB 17592186290501; level easy; target (-7, 0); standard reference (1, -6, -3) or two-point reference None; reference slope 1/6. Field 17592186289731, key field-1, type :answer-field.type/blank; bank profile none.

What is the equation of the line that passes through the point $(-7,0)$ and is perpendicular to $x-6y=-3?$

$y=$
{{field-1}}

Source key present and verified; source solution present, exact replay.

- Source answer 17592186288958, field 17592186289731, exact value `-6x-42`; recipe `m*x+(v+t-m*u), RHS only`; reproduces entire original mathematical value at t=0: yes; profile none.

Fixed original solution:

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

DB 17592186290502; level easy; target (1, 1); standard reference (4, -3, 7) or two-point reference None; reference slope 4/3. Field 17592186289749, key field-1, type :answer-field.type/blank; bank profile none.

What is the equation of the line that passes through the point $(1,1)$ and is perpendicular to $4x-3y=7?$

$y=$
{{field-1}}

Source key present and verified; source solution present, exact replay.

- Source answer 17592186288868, field 17592186289749, exact value `-\frac{3}{4}x+\frac{7}{4}`; recipe `m*x+(v+t-m*u), RHS only`; reproduces entire original mathematical value at t=0: yes; profile none.

Fixed original solution:

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

DB 17592186292541; level moderate; target (3, 4); standard reference None or two-point reference ((2, 2), (5, 8)); reference slope 2. Field 17592186292514, key selection, type :answer-field.type/radio; bank profile q-252524.

Find the equation of the line that passes through the point $(3,4)$ and is perpendicular to the line passing through the points $(2,2)$ and $(5,8).$

Source key present and verified; source solution present, exact replay.

- Source answer 17592186290780, field 17592186292514, exact value `2x-y=2`; recipe `2*x+(-1)*y=2+(-1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-252524.

- Source answer 17592186291272, field 17592186292514, exact value `2x+5y=26`; recipe `2*x+(5)*y=26+(5)*t`; reproduces entire original mathematical value at t=0: yes; profile q-252524.

- Source answer 17592186291284, field 17592186292514, exact value `2x+y=10`; recipe `2*x+(1)*y=10+(1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-252524.

- Source answer 17592186291519, field 17592186292514, exact value `x+2y=11`; recipe `1*x+(2)*y=11+(2)*t`; reproduces entire original mathematical value at t=0: yes; profile q-252524.

- Source answer 17592186291538, field 17592186292514, exact value `x+4y=19`; recipe `1*x+(4)*y=19+(4)*t`; reproduces entire original mathematical value at t=0: yes; profile q-252524.

Fixed original solution:

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

DB 17592186341836; level moderate; target (5, 1); standard reference None or two-point reference ((1, 5), (-3, -1)); reference slope 3/2. Field 17592186341536, key selection, type :answer-field.type/radio; bank profile q-72571.

Find the equation of the line that passes through the point $(5,1)$ and is perpendicular to the line passing through the points $(1,5)$ and $(-3,-1).$

Source key present and verified; source solution present, exact replay.

- Source answer 17592186339683, field 17592186341536, exact value `2x-3y=7`; recipe `2*x+(-3)*y=7+(-3)*t`; reproduces entire original mathematical value at t=0: yes; profile q-72571.

- Source answer 17592186339880, field 17592186341536, exact value `x+y=6`; recipe `1*x+(1)*y=6+(1)*t`; reproduces entire original mathematical value at t=0: yes; profile q-72571.

- Source answer 17592186340089, field 17592186341536, exact value `2x-3y=5`; recipe `2*x+(-3)*y=5+(-3)*t`; reproduces entire original mathematical value at t=0: yes; profile q-72571.

- Source answer 17592186340279, field 17592186341536, exact value `2x+3y=13`; recipe `2*x+(3)*y=13+(3)*t`; reproduces entire original mathematical value at t=0: yes; profile q-72571.

- Source answer 17592186340728, field 17592186341536, exact value `2x+3y=7`; recipe `2*x+(3)*y=7+(3)*t`; reproduces entire original mathematical value at t=0: yes; profile q-72571.

Fixed original solution:

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
