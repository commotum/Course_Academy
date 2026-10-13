# Template extraction

## Stage 1 — Specific source records

All records use an origin O and nonparallel position vectors to the segment endpoints. A third point internally divides that segment in the stated ordered ratio. Every known vector has coefficient +1; all ratios are positive integers. The radio answer is the complete target vector equation; blanks are scalar coefficients in the supplied endpoint-vector order. No vector coordinate computations occur.

## Stage 2 — Generalized pattern

If AX:XB=r:s, AB=b−a, AX=r/(r+s)(b−a), OX=a+AX=s/(r+s)a+r/(r+s)b. The learner must preserve the orientation and ratio order.

## Stage 3 — Complete component and bank map

Notation: r=first segment ratio, s=second, D=r+s. Recipe intent is underdetermined for several scalar banks. The following expressions are explicit parameterized value patterns that reproduce complete observed banks. They are restricted to explicit replay profiles; normal radio generation uses its separately labeled operation bank. Fixed candidate halves/thirds and numerator offsets reproduce observed candidate structure, without claiming recovered historical errors.

### q-12212

Parameters: `{"A": "A", "B": "B", "X": "T", "u": "a", "v": "b", "r": 1, "s": 1}`. Layout: radio.

![](images/c2/c2406e6f3cb76f50bfcc73a348b38d93b7a24da8e4314e0b3523bb4cbf143364.png)

Consider the diagram above, where $\overset{\to }{OA}=a,$ $\overset{\to }{OB}=b$, and $T$ divides $\overset{―}{AB}$ in the ratio $AT:TB=1:1.$ Find $\overset{\to }{OT}.$

Field 1, option 1: `OT^(→) = a + \frac{1}{2}b`; recipe `(1, r/(r + s))`; stored correct: False.

Field 1, option 2: `OT^(→) = \frac{2}{3}a + \frac{1}{3}b`; recipe `(2*r/(2*r + s), s/(2*r + s))`; stored correct: False.

Field 1, option 3: `OT^(→) = \frac{1}{3}a + \frac{2}{3}b`; recipe `(s/(2*r + s), 2*r/(2*r + s))`; stored correct: False.

Field 1, option 4: `OT^(→) = \frac{1}{2}a + b`; recipe `(r/(r + s), 1)`; stored correct: False.

Field 1, option 5: `OT^(→) = \frac{1}{2}a + \frac{1}{2}b`; recipe `(s/(r + s), r/(r + s))`; stored correct: False.

Correct designation absent in capture. Inferred separately from the internal-section formula; no claim of a matched source designation.

Field 2, option 1: `\overset{\to }{OT}=\frac{1}{2}a+b`; recipe `(r/(r + s), 1)`; stored correct: False.

Field 2, option 2: `\overset{\to }{OT}=\frac{1}{2}a+\frac{1}{2}b`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 2, option 3: `\overset{\to }{OT}=\frac{2}{3}a+\frac{1}{3}b`; recipe `(2*r/(2*r + s), s/(2*r + s))`; stored correct: False.

Field 2, option 4: `\overset{\to }{OT}=\frac{1}{3}a+\frac{2}{3}b`; recipe `(s/(2*r + s), 2*r/(2*r + s))`; stored correct: False.

Field 2, option 5: `\overset{\to }{OT}=a+\frac{1}{2}b`; recipe `(1, r/(r + s))`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OT}=\overset{\to }{OA}+\overset{\to }{AT}.
$$

We're told that $\overset{\to }{OA}=a,$ so we just need to work out $\overset{\to }{AT}.$

First, from $△OAB,$ we have

$$
\begin{aligned}\overset{\to }{AB} & =\overset{\to }{AO}+\overset{\to }{OB} \\  & =-\overset{\to }{OA}+\overset{\to }{OB} \\  & =-a+b \\  & =b-a.\end{aligned}
$$

Since $AT:TB=1:1,$ we have

$$
\overset{\to }{AT}=\frac{1}{2}\overset{\to }{AB}=\frac{1}{2}(b-a).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OT} & =\overset{\to }{OA}+\overset{\to }{AT} \\  & =a+\frac{1}{2}(b-a) \\  & =\frac{1}{2}a+\frac{1}{2}b.\end{aligned}
$$

### q-42659

Parameters: `{"A": "P", "B": "Q", "X": "R", "u": "p", "v": "q", "r": 1, "s": 2}`. Layout: radio.

![](images/fb/fb31653c9fc5031372c4b08e8fba0ec809c7e58a7a2321a8a7eb027b8eacd48a.png)

Consider the diagram above, where $OP^(→) = p$, $OQ^(→) = q$ and $R$ divides $PQ^(―)$ in the ratio $PR: RQ = 1: 2$. Find $OR^(→)$.

Field 1, option 1: `OR^(→) = \frac{3}{4}p + \frac{1}{4}q`; recipe `((r + s)/(2*r + s), r/(2*r + s))`; stored correct: False.

Field 1, option 2: `OR^(→) = \frac{2}{3}p + \frac{1}{3}q`; recipe `(s/(r + s), r/(r + s))`; stored correct: False.

Field 1, option 3: `OR^(→) = \frac{1}{2}p + \frac{1}{2}q`; recipe `(1/2, 1/2)`; stored correct: False.

Field 1, option 4: `OR^(→) = \frac{1}{3}p + \frac{2}{3}q`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 5: `OR^(→) = \frac{1}{4}p + \frac{3}{4}q`; recipe `(r/(2*r + s), (r + s)/(2*r + s))`; stored correct: False.

Correct designation absent in capture. Inferred separately from the internal-section formula; no claim of a matched source designation.

Fixed solution: Absent. Authored using the complete shared ordered source solution.

### q-120285

Parameters: `{"A": "H", "B": "I", "X": "J", "u": "h", "v": "i", "r": 3, "s": 7}`. Layout: radio.

![](images/c4/c4d26b3db6446f586ca47634d9f9a3a004968a0081b8859ce46b4b4af799d066.png)

Consider the diagram above, where $\overset{\to }{OH}=h,$ $\overset{\to }{OI}=i$ and $J$ divides $\overset{―}{HI}$ in the ratio $HJ:JI=3:7.$ Find $\overset{\to }{OJ}.$

Field 1, option 1: `\overset{\to }{OJ}=\frac{3}{10}h+\frac{7}{10}i`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 2: `\overset{\to }{OJ}=\frac{3}{5}h+\frac{2}{5}i`; recipe `(2*r/(r + s), -2*r/(r + s) + 1)`; stored correct: False.

Field 1, option 3: `\overset{\to }{OJ}=\frac{1}{2}h+\frac{1}{2}i`; recipe `(1/2, 1/2)`; stored correct: False.

Field 1, option 4: `\overset{\to }{OJ}=\frac{7}{10}h+\frac{3}{10}i`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 5: `\overset{\to }{OJ}=\frac{2}{5}h+\frac{3}{5}i`; recipe `(-2*r/(r + s) + 1, 2*r/(r + s))`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OJ}=\overset{\to }{OH}+\overset{\to }{HJ}.
$$

We're told that $\overset{\to }{OH}=h,$ so we just need to work out $\overset{\to }{HJ}.$

First, from $△OHI,$ we have

$$
\begin{aligned}\overset{\to }{HI} & =\overset{\to }{HO}+\overset{\to }{OI} \\  & =-\overset{\to }{OH}+\overset{\to }{OI} \\  & =-h+i \\  & =i-h.\end{aligned}
$$

Since $HJ:JI=3:7,$ we have

$$
\overset{\to }{HJ}=\frac{3}{10}\overset{\to }{HI}=\frac{3}{10}(i-h).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OJ} & =\overset{\to }{OH}+\overset{\to }{HJ} \\  & =h+\frac{3}{10}(i-h) \\  & =\frac{7}{10}h+\frac{3}{10}i.\end{aligned}
$$

### q-120294

Parameters: `{"A": "U", "B": "V", "X": "W", "u": "u", "v": "v", "r": 7, "s": 2}`. Layout: radio.

![](images/70/707beca1d856414e25874cc0b56c6654fbb41d699f01106b6749d49408b39aee.png)

Consider the diagram above, where $\overset{\to }{OU}=u,$ $\overset{\to }{OV}=v$ and $W$ divides $\overset{―}{UV}$ in the ratio $UW:WV=7:2.$ Find $\overset{\to }{OW}.$

Field 1, option 1: `\overset{\to }{OW}=\frac{2}{9}u+\frac{7}{9}v`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 2: `\overset{\to }{OW}=\frac{1}{3}u+\frac{2}{3}v`; recipe `(1/3, 2/3)`; stored correct: False.

Field 1, option 3: `\overset{\to }{OW}=\frac{7}{9}u+\frac{2}{9}v`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 4: `\overset{\to }{OW}=\frac{5}{7}u+\frac{2}{7}v`; recipe `((r - s)/r, s/r)`; stored correct: False.

Field 1, option 5: `\overset{\to }{OW}=\frac{2}{3}u+\frac{1}{3}v`; recipe `(2/3, 1/3)`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OW}=\overset{\to }{OU}+\overset{\to }{UW}.
$$

We're told that $\overset{\to }{OU}=u,$ so we just need to work out $\overset{\to }{UW}.$

First, from $△OUV,$ we have

$$
\begin{aligned}\overset{\to }{UV} & =\overset{\to }{UO}+\overset{\to }{OV} \\  & =-\overset{\to }{OU}+\overset{\to }{OV} \\  & =-u+v \\  & =v-u.\end{aligned}
$$

Since $UW:WV=7:2,$ we have

$$
\overset{\to }{UW}=\frac{7}{9}\overset{\to }{UV}=\frac{7}{9}(v-u).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OW} & =\overset{\to }{OU}+\overset{\to }{UW} \\  & =u+\frac{7}{9}(v-u) \\  & =\frac{2}{9}u+\frac{7}{9}v.\end{aligned}
$$

### q-120303

Parameters: `{"A": "M", "B": "N", "X": "P", "u": "m", "v": "n", "r": 2, "s": 1}`. Layout: radio.

![](images/50/50b87e86bd2985e54ce0a8fe6b3e23986f7e1946a5284d0ae297d96b9cbc60f6.png)

Consider the diagram above, where $\overset{\to }{OM}=m,$ $\overset{\to }{ON}=n$ and $P$ divides $\overset{―}{MN}$ in the ratio $MP:PN=2:1.$ Find $\overset{\to }{OP}.$

Field 1, option 1: `\overset{\to }{OP}=\frac{5}{9}m+\frac{4}{9}n`; recipe `((2*r + s)/(r + s)**2, 1 - (2*r + s)/(r + s)**2)`; stored correct: False.

Field 1, option 2: `\overset{\to }{OP}=\frac{1}{3}m+\frac{2}{3}n`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 3: `\overset{\to }{OP}=\frac{1}{2}m+\frac{1}{2}n`; recipe `(1/2, 1/2)`; stored correct: False.

Field 1, option 4: `\overset{\to }{OP}=\frac{2}{3}m+\frac{1}{3}n`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 5: `\overset{\to }{OP}=\frac{4}{9}m+\frac{5}{9}n`; recipe `(1 - (2*r + s)/(r + s)**2, (2*r + s)/(r + s)**2)`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OP}=\overset{\to }{OM}+\overset{\to }{MP}.
$$

We're told that $\overset{\to }{OM}=m,$ so we just need to work out $\overset{\to }{MP}.$

First, from $△OMN,$ we have

$$
\begin{aligned}\overset{\to }{MN} & =\overset{\to }{MO}+\overset{\to }{ON} \\  & =-\overset{\to }{OM}+\overset{\to }{ON} \\  & =-m+n \\  & =n-m.\end{aligned}
$$

Since $MP:PN=2:1,$ we have

$$
\overset{\to }{MP}=\frac{2}{3}\overset{\to }{MN}=\frac{2}{3}(n-m).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OP} & =\overset{\to }{OM}+\overset{\to }{MP} \\  & =m+\frac{2}{3}(n-m) \\  & =\frac{1}{3}m+\frac{2}{3}n.\end{aligned}
$$

### q-12214

Parameters: `{"A": "A", "B": "B", "X": "T", "u": "a", "v": "b", "r": 1, "s": 6}`. Layout: radio.

![](images/42/4205d878409776be6c18735910a2f8ece019418452df83cb75d197531f057532.png)

Consider the diagram above, where $\overset{\to }{OA}=a,$ $\overset{\to }{OB}=b$ and $T$ divides $\overset{―}{AB}$ in the ratio $AT:TB=1:6.$ Find $\overset{\to }{OT}.$

Field 1, option 1: `\overset{\to }{OT}=-\frac{6}{7}a+\frac{1}{7}b`; recipe `(-s/(r + s), r/(r + s))`; stored correct: False.

Field 1, option 2: `\overset{\to }{OT}=\frac{6}{7}a-\frac{1}{7}b`; recipe `(s/(r + s), -r/(r + s))`; stored correct: False.

Field 1, option 3: `\overset{\to }{OT}=\frac{5}{7}a+\frac{1}{7}b`; recipe `((-r + s)/(r + s), r/(r + s))`; stored correct: False.

Field 1, option 4: `\overset{\to }{OT}=\frac{6}{7}a+\frac{1}{7}b`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 5: `\overset{\to }{OT}=\frac{3}{7}a+\frac{1}{7}b`; recipe `(s/(2*r + 2*s), r/(r + s))`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OT}=\overset{\to }{OA}+\overset{\to }{AT}.
$$

We're told that $\overset{\to }{OA}=a,$ so we just need to work out $\overset{\to }{AT}.$

First, from $△OAB,$ we have

$$
\begin{aligned}\overset{\to }{AB} & =\overset{\to }{AO}+\overset{\to }{OB} \\  & =-\overset{\to }{OA}+\overset{\to }{OB} \\  & =-a+b \\  & =b-a.\end{aligned}
$$

Since $AT:TB=1:6,$ we have

$$
\overset{\to }{AT}=\frac{1}{7}\overset{\to }{AB}=\frac{1}{7}(b-a).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OT} & =\overset{\to }{OA}+\overset{\to }{AT} \\  & =a+\frac{1}{7}(b-a) \\  & =\frac{6}{7}a+\frac{1}{7}b.\end{aligned}
$$

### q-12233

Parameters: `{"A": "X", "B": "Y", "X": "Z", "u": "a", "v": "b", "r": 5, "s": 2}`. Layout: radio.

![](images/2f/2f0d9df3316615646dfbd994a378293dacf937050514080b5fe66af9794ae9e3.png)

Consider the diagram above, where $\overset{\to }{OX}=a,$ $\overset{\to }{OY}=b$ and $Z$ divides $\overset{―}{XY}$ in the ratio $XZ:ZY=5:2.$ Find $\overset{\to }{OZ}.$

Field 1, option 1: `\overset{\to }{OZ}=\frac{1}{7}a-\frac{6}{7}b`; recipe `((s - 1)/(r + s), (-r - 1)/(r + s))`; stored correct: False.

Field 1, option 2: `\overset{\to }{OZ}=\frac{1}{7}a+\frac{6}{7}b`; recipe `((s - 1)/(r + s), (r + 1)/(r + s))`; stored correct: False.

Field 1, option 3: `\overset{\to }{OZ}=\frac{2}{7}a+\frac{6}{7}b`; recipe `(s/(r + s), (r + 1)/(r + s))`; stored correct: False.

Field 1, option 4: `\overset{\to }{OZ}=\frac{2}{7}a+\frac{5}{7}b`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 5: `\overset{\to }{OZ}=\frac{2}{7}a-\frac{5}{7}b`; recipe `(s/(r + s), -r/(r + s))`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OZ}=\overset{\to }{OX}+\overset{\to }{XZ}.
$$

We're told that $\overset{\to }{OX}=a,$ so we just need to work out $\overset{\to }{XZ}.$

First, from $△OXY,$ we have

$$
\begin{aligned}\overset{\to }{XY} & =\overset{\to }{XO}+\overset{\to }{OY} \\  & =-\overset{\to }{OX}+\overset{\to }{OY} \\  & =-a+b \\  & =b-a.\end{aligned}
$$

Since $XZ:ZY=5:2,$ we have

$$
\overset{\to }{XZ}=\frac{5}{7}\overset{\to }{XY}=\frac{5}{7}(b-a).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OZ} & =\overset{\to }{OX}+\overset{\to }{XZ} \\  & =a+\frac{5}{7}(b-a) \\  & =\frac{2}{7}a+\frac{5}{7}b.\end{aligned}
$$

### q-12235

Parameters: `{"A": "A", "B": "B", "X": "C", "u": "a", "v": "b", "r": 5, "s": 1}`. Layout: radio.

![](images/45/45110269c8a1ca9ad80cabc2f6c44592dca781afde7347d9d0a7e3363a76563a.png)

Consider the diagram above, where $\overset{\to }{OA}=a,$ $\overset{\to }{OB}=b$ and $C$ divides $\overset{―}{AB}$ in the ratio $AC:CB=5:1.$ Find $\overset{\to }{OC}.$

Field 1, option 1: `\overset{\to }{OC}=\frac{1}{3}a-\frac{2}{3}b`; recipe `(2*s/(r + s), (-r + s)/(r + s))`; stored correct: False.

Field 1, option 2: `\overset{\to }{OC}=\frac{5}{6}a+\frac{1}{6}b`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 3: `\overset{\to }{OC}=\frac{1}{6}a+\frac{5}{6}b`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 4: `\overset{\to }{OC}=\frac{1}{3}a+\frac{2}{3}b`; recipe `(2*s/(r + s), (r - s)/(r + s))`; stored correct: False.

Field 1, option 5: `\overset{\to }{OC}=\frac{1}{6}a-\frac{5}{6}b`; recipe `(s/(r + s), -r/(r + s))`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OC}=\overset{\to }{OA}+\overset{\to }{AC}.
$$

We're told that $\overset{\to }{OA}=a,$ so we just need to work out $\overset{\to }{AC}.$

First, from $△OAB,$ we have

$$
\begin{aligned}\overset{\to }{AB} & =\overset{\to }{AO}+\overset{\to }{OB} \\  & =-\overset{\to }{OA}+\overset{\to }{OB} \\  & =-a+b \\  & =b-a.\end{aligned}
$$

Since $AC:CB=5:1,$ we have

$$
\overset{\to }{AC}=\frac{5}{6}\overset{\to }{AB}=\frac{5}{6}(b-a).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OC} & =\overset{\to }{OA}+\overset{\to }{AC} \\  & =a+\frac{5}{6}(b-a) \\  & =\frac{1}{6}a+\frac{5}{6}b.\end{aligned}
$$

### q-278263

Parameters: `{"A": "D", "B": "E", "X": "F", "u": "d", "v": "e", "r": 2, "s": 3}`. Layout: coefficients.

![](images/c2/c26ec7e1fccc5ada4c43eef55faf9e4fa3e17ed896b1546f472edf744404da1a.png)

Consider the diagram above, where $\overset{\to }{OD}=d,$ $\overset{\to }{OE}=e,$ and $F$ divides $\overset{―}{DE}$ in the ratio $DF:FE=2:3.$ Express $\overset{\to }{OF}$ via the vectors $d$ and $e.$

$\,\overset{\to }{OF}=$
{{field-1}}
$d+$
{{field-2}}
$e$

Field 1, option 1: `\frac{2}{5}`; recipe `r/(r + s), s/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{3}{5}`; recipe `r/(r + s), s/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OF}=\overset{\to }{OD}+\overset{\to }{DF}.
$$

We're told that $\overset{\to }{OD}=d,$ so we just need to work out $\overset{\to }{DF}.$

First, from $△ODE,$ we have

$$
\begin{aligned}\overset{\to }{DE} & =\overset{\to }{DO}+\overset{\to }{OE} \\  & =-\overset{\to }{OD}+\overset{\to }{OE} \\  & =-d+e \\  & =e-d.\end{aligned}
$$

Since $DF:FE=2:3,$ we have

$$
\overset{\to }{DF}=\frac{2}{5}\overset{\to }{DE}=\frac{2}{5}(e-d).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OF} & =\overset{\to }{OD}+\overset{\to }{DF} \\  & =d+\frac{2}{5}(e-d) \\  & =\frac{3}{5}d+\frac{2}{5}e.\end{aligned}
$$

### q-278290

Parameters: `{"A": "F", "B": "G", "X": "P", "u": "f", "v": "g", "r": 8, "s": 5}`. Layout: radio.

![](images/36/36aeda6b6f5ce46552f55f458da60ef46a646d737c452d586389c03c47d1c9cb.png)

Consider the diagram above, where $\overset{\to }{OF}=f,$ $\overset{\to }{OG}=g$ and $P$ divides $\overset{―}{FG}$ in the ratio $FP:PG=8:5.$ Find $\overset{\to }{OP}.$

Field 1, option 1: `\overset{\to }{OP}=f+\frac{8}{5}g`; recipe `(1, r/s)`; stored correct: False.

Field 1, option 2: `\overset{\to }{OP}=\frac{5}{8}f+\frac{1}{8}g`; recipe `(s/r, 1/r)`; stored correct: False.

Field 1, option 3: `\overset{\to }{OP}=\frac{5}{13}f+\frac{8}{13}g`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 4: `\overset{\to }{OP}=\frac{1}{8}f+\frac{1}{5}g`; recipe `(1/r, 1/s)`; stored correct: False.

Field 1, option 5: `\overset{\to }{OP}=\frac{8}{13}f+\frac{5}{13}g`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OP}=\overset{\to }{OF}+\overset{\to }{FP}.
$$

We're told that $\overset{\to }{OF}=f,$ so we just need to work out $\overset{\to }{FP}.$

First, from $△OFG,$ we have

$$
\begin{aligned}\overset{\to }{FG} & =\overset{\to }{FO}+\overset{\to }{OG} \\  & =-\overset{\to }{OF}+\overset{\to }{OG} \\  & =-f+g \\  & =g-f.\end{aligned}
$$

Since $FP:PG=8:5,$ we have

$$
\overset{\to }{FP}=\frac{8}{13}\overset{\to }{FG}=\frac{8}{13}(g-f).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OP} & =\overset{\to }{OF}+\overset{\to }{FP} \\  & =f+\frac{8}{13}(g-f) \\  & =\frac{5}{13}f+\frac{8}{13}g.\end{aligned}
$$

### q-322568

Parameters: `{"A": "D", "B": "E", "X": "F", "u": "d", "v": "e", "r": 3, "s": 4}`. Layout: coefficients.

![](images/7e/7e92a09f8448f4d320f86656bc0774e6167b96156041c32eb7a64ba5e8820128.png)

Consider the diagram above, where $\overset{\to }{OD}=d,$ $\overset{\to }{OE}=e,$ and $F$ divides $\overset{―}{DE}$ in the ratio $DF:FE=3:4.$ Express $\overset{\to }{OF}$ via the vectors $d$ and $e.$

$\,\overset{\to }{OF}=$
{{field-1}}
$d+$
{{field-2}}
$e$

Field 1, option 1: `\frac{3}{7}`; recipe `r/(r + s), s/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{4}{7}`; recipe `r/(r + s), s/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OF}=\overset{\to }{OD}+\overset{\to }{DF}.
$$

We're told that $\overset{\to }{OD}=d,$ so we just need to work out $\overset{\to }{DF}.$

First, from $△ODE,$ we have

$$
\begin{aligned}\overset{\to }{DE} & =\overset{\to }{DO}+\overset{\to }{OE} \\  & =-\overset{\to }{OD}+\overset{\to }{OE} \\  & =-d+e \\  & =e-d.\end{aligned}
$$

Since $DF:FE=3:4,$ we have

$$
\overset{\to }{DF}=\frac{3}{7}\overset{\to }{DE}=\frac{3}{7}(e-d).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OF} & =\overset{\to }{OD}+\overset{\to }{DF} \\  & =d+\frac{3}{7}(e-d) \\  & =\frac{4}{7}d+\frac{3}{7}e.\end{aligned}
$$

### q-322574

Parameters: `{"A": "G", "B": "H", "X": "J", "u": "g", "v": "h", "r": 6, "s": 7}`. Layout: coefficients.

![](images/2a/2a9cacfc6787e60229076c4abd2854709d51ac718c8d519256a61dbe92852b05.png)

Consider the diagram above, where $\overset{\to }{OG}=g,$ $\overset{\to }{OH}=h,$ and $J$ divides $\overset{―}{GH}$ in the ratio $GJ:JH=6:7.$ Express $\overset{\to }{OJ}$ via the vectors $g$ and $h.$

$\,\overset{\to }{OJ}=$
{{field-1}}
$g+$
{{field-2}}
$h$

Field 1, option 1: `\frac{7}{13}`; recipe `s/(r + s), r/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{6}{13}`; recipe `s/(r + s), r/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OJ}=\overset{\to }{OG}+\overset{\to }{GJ}.
$$

We're told that $\overset{\to }{OG}=g,$ so we just need to work out $\overset{\to }{GJ}.$

First, from $△OGH,$ we have

$$
\begin{aligned}\overset{\to }{GH} & =\overset{\to }{GO}+\overset{\to }{OH} \\  & =-\overset{\to }{OG}+\overset{\to }{OH} \\  & =-g+h \\  & =h-g.\end{aligned}
$$

Since $GJ:JH=6:7,$ we have

$$
\overset{\to }{GJ}=\frac{6}{13}\overset{\to }{GH}=\frac{6}{13}(h-g).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OJ} & =\overset{\to }{OG}+\overset{\to }{GJ} \\  & =g+\frac{6}{13}(h-g) \\  & =\frac{7}{13}g+\frac{6}{13}h.\end{aligned}
$$

### q-322575

Parameters: `{"A": "P", "B": "Q", "X": "R", "u": "p", "v": "q", "r": 4, "s": 9}`. Layout: coefficients.

![](images/d9/d9448f9f05666f9806975b37a73f09c492eb73139b6f9395b619f077f3a584c9.png)

Consider the diagram above, where $\overset{\to }{OP}=p,$ $\overset{\to }{OQ}=q,$ and $R$ divides $\overset{―}{PQ}$ in the ratio $PR:RQ=4:9.$ Express $\overset{\to }{OR}$ via the vectors $p$ and $q.$

$\,\overset{\to }{OR}=$
{{field-1}}
$p+$
{{field-2}}
$q$

Field 1, option 1: `\frac{9}{13}`; recipe `s/(r + s), r/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{4}{13}`; recipe `s/(r + s), r/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OR}=\overset{\to }{OP}+\overset{\to }{PR}.
$$

We're told that $\overset{\to }{OP}=p,$ so we just need to work out $\overset{\to }{PR}.$

First, from $△OPQ,$ we have

$$
\begin{aligned}\overset{\to }{PQ} & =\overset{\to }{PO}+\overset{\to }{OQ} \\  & =-\overset{\to }{OP}+\overset{\to }{OQ} \\  & =-p+q \\  & =q-p.\end{aligned}
$$

Since $PR:RQ=4:9,$ we have

$$
\overset{\to }{PR}=\frac{4}{13}\overset{\to }{PQ}=\frac{4}{13}(q-p).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OR} & =\overset{\to }{OP}+\overset{\to }{PR} \\  & =p+\frac{4}{13}(q-p) \\  & =\frac{9}{13}p+\frac{4}{13}q.\end{aligned}
$$

### q-322576

Parameters: `{"A": "M", "B": "N", "X": "T", "u": "d", "v": "e", "r": 8, "s": 3}`. Layout: coefficients.

![](images/36/36742531a5f9f5d77c5f7e90980120479f4142cecaf6e84937d76d938688409d.png)

Consider the diagram above, where $\overset{\to }{OM}=d,$ $\overset{\to }{ON}=e,$ and $T$ divides $\overset{―}{MN}$ in the ratio $MT:TN=8:3.$ Express $\overset{\to }{OT}$ via the vectors $d$ and $e.$

$\,\overset{\to }{OT}=$
{{field-1}}
$d+$
{{field-2}}
$e$

Field 1, option 1: `\frac{8}{11}`; recipe `r/(r + s), s/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{3}{11}`; recipe `r/(r + s), s/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OT}=\overset{\to }{OM}+\overset{\to }{MT}.
$$

We're told that $\overset{\to }{OM}=d,$ so we just need to work out $\overset{\to }{MT}.$

First, from $△OMN,$ we have

$$
\begin{aligned}\overset{\to }{MN} & =\overset{\to }{MO}+\overset{\to }{ON} \\  & =-\overset{\to }{OM}+\overset{\to }{ON} \\  & =-d+e \\  & =e-d.\end{aligned}
$$

Since $MT:TN=8:3,$ we have

$$
\overset{\to }{MT}=\frac{8}{11}\overset{\to }{MN}=\frac{8}{11}(e-d).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OT} & =\overset{\to }{OM}+\overset{\to }{MT} \\  & =d+\frac{8}{11}(e-d) \\  & =\frac{3}{11}d+\frac{8}{11}e.\end{aligned}
$$

### q-322577

Parameters: `{"A": "U", "B": "V", "X": "W", "u": "u", "v": "v", "r": 9, "s": 8}`. Layout: coefficients.

![](images/de/de33644bcad663e67dc19c687dc0ef959310a50ddb83203031e66b951700510b.png)

Consider the diagram above, where $\overset{\to }{OU}=u,$ $\overset{\to }{OV}=v,$ and $W$ divides $\overset{―}{UV}$ in the ratio $UW:WV=9:8.$ Express $\overset{\to }{OW}$ via the vectors $u$ and $v.$

$\,\overset{\to }{OW}=$
{{field-1}}
$u+$
{{field-2}}
$v$

Field 1, option 1: `\frac{8}{17}`; recipe `s/(r + s), r/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{9}{17}`; recipe `s/(r + s), r/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OW}=\overset{\to }{OU}+\overset{\to }{UW}.
$$

We're told that $\overset{\to }{OU}=u,$ so we just need to work out $\overset{\to }{UW}.$

First, from $△OUV,$ we have

$$
\begin{aligned}\overset{\to }{UV} & =\overset{\to }{UO}+\overset{\to }{OV} \\  & =-\overset{\to }{OU}+\overset{\to }{OV} \\  & =-u+v \\  & =v-u.\end{aligned}
$$

Since $UW:WV=9:8,$ we have

$$
\overset{\to }{UW}=\frac{9}{17}\overset{\to }{UV}=\frac{9}{17}(v-u).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OW} & =\overset{\to }{OU}+\overset{\to }{UW} \\  & =u+\frac{9}{17}(v-u) \\  & =\frac{8}{17}u+\frac{9}{17}v.\end{aligned}
$$

### q-322578

Parameters: `{"A": "S", "B": "T", "X": "L", "u": "s", "v": "t", "r": 11, "s": 4}`. Layout: coefficients.

![](images/84/84ba52159416b3b420daa1ebd82dccac2411aee420201b9b9604937995d9553c.png)

Consider the diagram above, where $\overset{\to }{OS}=s,$ $\overset{\to }{OT}=t,$ and $L$ divides $\overset{―}{ST}$ in the ratio $SL:LT=11:4.$ Express $\overset{\to }{OL}$ via the vectors $s$ and $t.$

$\,\overset{\to }{OL}=$
{{field-1}}
$s+$
{{field-2}}
$t$

Field 1, option 1: `\frac{4}{15}`; recipe `s/(r + s), r/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{11}{15}`; recipe `s/(r + s), r/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OL}=\overset{\to }{OS}+\overset{\to }{SL}.
$$

We're told that $\overset{\to }{OS}=s,$ so we just need to work out $\overset{\to }{SL}.$

First, from $△OST,$ we have

$$
\begin{aligned}\overset{\to }{ST} & =\overset{\to }{SO}+\overset{\to }{OT} \\  & =-\overset{\to }{OS}+\overset{\to }{OT} \\  & =-s+t \\  & =t-s.\end{aligned}
$$

Since $SL:LT=11:4,$ we have

$$
\overset{\to }{SL}=\frac{11}{15}\overset{\to }{ST}=\frac{11}{15}(t-s).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OL} & =\overset{\to }{OS}+\overset{\to }{SL} \\  & =s+\frac{11}{15}(t-s) \\  & =\frac{4}{15}s+\frac{11}{15}t.\end{aligned}
$$

### q-322582

Parameters: `{"A": "K", "B": "Z", "X": "Y", "u": "k", "v": "z", "r": 10, "s": 7}`. Layout: coefficients.

![](images/76/76ddb750ca447fd7f73f2481ecd46bb53eba12e392e81e8b64c2c23589e11694.png)

Consider the diagram above, where $\overset{\to }{OK}=k,$ $\overset{\to }{OZ}=z,$ and $Y$ divides $\overset{―}{KZ}$ in the ratio $KY:YZ=10:7.$ Express $\overset{\to }{OY}$ via the vectors $k$ and $z.$

$\,\overset{\to }{OY}=$
{{field-1}}
$k+$
{{field-2}}
$z$

Field 1, option 1: `\frac{7}{17}`; recipe `s/(r + s), r/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{10}{17}`; recipe `s/(r + s), r/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OY}=\overset{\to }{OK}+\overset{\to }{KY}.
$$

We're told that $\overset{\to }{OK}=k,$ so we just need to work out $\overset{\to }{KY}.$

First, from $△OKZ,$ we have

$$
\begin{aligned}\overset{\to }{KZ} & =\overset{\to }{KO}+\overset{\to }{OZ} \\  & =-\overset{\to }{OK}+\overset{\to }{OZ} \\  & =-k+z \\  & =z-k.\end{aligned}
$$

Since $KY:YZ=10:7,$ we have

$$
\overset{\to }{KY}=\frac{10}{17}\overset{\to }{KZ}=\frac{10}{17}(z-k).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OY} & =\overset{\to }{OK}+\overset{\to }{KY} \\  & =k+\frac{10}{17}(z-k) \\  & =\frac{7}{17}k+\frac{10}{17}z.\end{aligned}
$$

### q-322583

Parameters: `{"A": "A", "B": "Q", "X": "N", "u": "a", "v": "q", "r": 12, "s": 7}`. Layout: coefficients.

![](images/d0/d0e71a97dc559536c25b63fda50805875d4651166a9442ae0d3d081704edebb2.png)

Consider the diagram above, where $\overset{\to }{OA}=a,$ $\overset{\to }{OQ}=q,$ and $N$ divides $\overset{―}{AQ}$ in the ratio $AN:NQ=12:7.$ Express $\overset{\to }{ON}$ via the vectors $a$ and $q.$

$\,\overset{\to }{ON}=$
{{field-1}}
$a+$
{{field-2}}
$q$

Field 1, option 1: `\frac{7}{19}`; recipe `s/(r + s), r/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{12}{19}`; recipe `s/(r + s), r/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{ON}=\overset{\to }{OA}+\overset{\to }{AN}.
$$

We're told that $\overset{\to }{OA}=a,$ so we just need to work out $\overset{\to }{AN}.$

First, from $△OAQ,$ we have

$$
\begin{aligned}\overset{\to }{AQ} & =\overset{\to }{AO}+\overset{\to }{OQ} \\  & =-\overset{\to }{OA}+\overset{\to }{OQ} \\  & =-a+q \\  & =q-a.\end{aligned}
$$

Since $AN:NQ=12:7,$ we have

$$
\overset{\to }{AN}=\frac{12}{19}\overset{\to }{AQ}=\frac{12}{19}(q-a).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{ON} & =\overset{\to }{OA}+\overset{\to }{AN} \\  & =a+\frac{12}{19}(q-a) \\  & =\frac{7}{19}a+\frac{12}{19}q.\end{aligned}
$$

### q-322586

Parameters: `{"A": "L", "B": "P", "X": "Q", "u": "l", "v": "p", "r": 7, "s": 9}`. Layout: coefficients.

![](images/1d/1deea2da05b0d12c7e9afbb12f0340bdbfef18ff37dc49c506929028bfeb67c4.png)

Consider the diagram above, where $\overset{\to }{OL}=l,$ $\overset{\to }{OP}=p,$ and $Q$ divides $\overset{―}{LP}$ in the ratio $LQ:QP=7:9.$ Express $\overset{\to }{OQ}$ via the vectors $l$ and $p.$

$\,\overset{\to }{OQ}=$
{{field-1}}
$l+$
{{field-2}}
$p$

Field 1, option 1: `\frac{7}{16}`; recipe `r/(r + s), s/(r + s) (field 1)`; stored correct: True.

Field 2, option 1: `\frac{9}{16}`; recipe `r/(r + s), s/(r + s) (field 2)`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OQ}=\overset{\to }{OL}+\overset{\to }{LQ}.
$$

We're told that $\overset{\to }{OL}=l,$ so we just need to work out $\overset{\to }{LQ}.$

First, from $△OLP,$ we have

$$
\begin{aligned}\overset{\to }{LP} & =\overset{\to }{LO}+\overset{\to }{OP} \\  & =-\overset{\to }{OL}+\overset{\to }{OP} \\  & =-l+p \\  & =p-l.\end{aligned}
$$

Since $LQ:QP=7:9,$ we have

$$
\overset{\to }{LQ}=\frac{7}{16}\overset{\to }{LP}=\frac{7}{16}(p-l).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OQ} & =\overset{\to }{OL}+\overset{\to }{LQ} \\  & =l+\frac{7}{16}(p-l) \\  & =\frac{9}{16}l+\frac{7}{16}p.\end{aligned}
$$

### q-42669

Parameters: `{"A": "U", "B": "V", "X": "W", "u": "u", "v": "v", "r": 2, "s": 7}`. Layout: radio.

![](images/04/040127594f639248736d4492f1853bcb1e6ef18c37db9242ebe466045713628a.png)

Consider the diagram above, where $\overset{\to }{OU}=u,$ $\overset{\to }{OV}=v$ and $W$ divides $\overset{―}{UV}$ in the ratio $UW:WV=2:7.$ Find $\overset{\to }{OW}.$

Field 1, option 1: `\overset{\to }{OW}=\frac{1}{3}u+\frac{2}{3}v`; recipe `(1/3, 2/3)`; stored correct: False.

Field 1, option 2: `\overset{\to }{OW}=\frac{7}{9}v-\frac{2}{9}u`; recipe `(-r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 3: `\overset{\to }{OW}=\frac{7}{9}u+\frac{2}{9}v`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 4: `\overset{\to }{OW}=\frac{2}{3}u+\frac{1}{3}v`; recipe `(2/3, 1/3)`; stored correct: False.

Field 1, option 5: `\overset{\to }{OW}=-\frac{1}{3}v+\frac{2}{3}u`; recipe `(2/3, -1/3)`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OW}=\overset{\to }{OU}+\overset{\to }{UW}.
$$

We're told that $\overset{\to }{OU}=u,$ so we just need to work out $\overset{\to }{UW}.$

First, from $△OUV,$ we have

$$
\begin{aligned}\overset{\to }{UV} & =\overset{\to }{UO}+\overset{\to }{OV} \\  & =-\overset{\to }{OU}+\overset{\to }{OV} \\  & =-u+v \\  & =v-u.\end{aligned}
$$

Since $UW:WV=2:7,$ we have

$$
\overset{\to }{UW}=\frac{2}{9}\overset{\to }{UV}=\frac{2}{9}(v-u).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OW} & =\overset{\to }{OU}+\overset{\to }{UW} \\  & =u+\frac{2}{9}(v-u) \\  & =\frac{7}{9}u+\frac{2}{9}v.\end{aligned}
$$

### q-120304

Parameters: `{"A": "H", "B": "I", "X": "J", "u": "h", "v": "i", "r": 5, "s": 3}`. Layout: radio.

![](images/65/6560a7f05ae95638cbfe902dfa022b2d8de6b07c6e1e6f85051ccf87b92ec338.png)

Consider the diagram above, where $\overset{\to }{OH}=h,$ $\overset{\to }{OI}=i$ and $J$ divides $\overset{―}{HI}$ in the ratio $HJ:JI=5:3.$ Find $\overset{\to }{OJ}.$

Field 1, option 1: `\overset{\to }{OJ}=\frac{1}{2}h+\frac{1}{2}i`; recipe `(1/2, 1/2)`; stored correct: False.

Field 1, option 2: `\overset{\to }{OJ}=\frac{3}{4}h+\frac{1}{4}i`; recipe `((s + 3)/(r + s), (r - 3)/(r + s))`; stored correct: False.

Field 1, option 3: `\overset{\to }{OJ}=\frac{5}{8}h+\frac{3}{8}i`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 4: `\overset{\to }{OJ}=\frac{1}{8}h+\frac{3}{4}i`; recipe `((s - 2)/(r + s), (r + 1)/(r + s))`; stored correct: False.

Field 1, option 5: `\overset{\to }{OJ}=\frac{3}{8}h+\frac{5}{8}i`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OJ}=\overset{\to }{OH}+\overset{\to }{HJ}.
$$

We're told that $\overset{\to }{OH}=h,$ so we just need to work out $\overset{\to }{HJ}.$

First, from $△OHI,$ we have

$$
\begin{aligned}\overset{\to }{HI} & =\overset{\to }{HO}+\overset{\to }{OI} \\  & =-\overset{\to }{OH}+\overset{\to }{OI} \\  & =-h+i \\  & =i-h.\end{aligned}
$$

Since $HJ:JI=5:3,$ we have

$$
\overset{\to }{HJ}=\frac{5}{8}\overset{\to }{HI}=\frac{5}{8}(i-h).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OJ} & =\overset{\to }{OH}+\overset{\to }{HJ} \\  & =h+\frac{5}{8}(i-h) \\  & =\frac{3}{8}h+\frac{5}{8}i.\end{aligned}
$$

### q-278288

Parameters: `{"A": "R", "B": "S", "X": "V", "u": "r", "v": "s", "r": 6, "s": 5}`. Layout: radio.

![](images/ba/ba82c6b68026b0f4339c1e4fa01c4b1aa1b7aee74b74176f81bba1c0e1de259f.png)

Consider the diagram above, where $\overset{\to }{OR}=r,$ $\overset{\to }{OS}=s$ and $V$ divides $\overset{―}{RS}$ in the ratio $RV:VS=6:5.$ Find $\overset{\to }{OV}.$

Field 1, option 1: `\overset{\to }{OV}=\frac{5}{6}r+\frac{1}{6}s`; recipe `(s/r, 1/r)`; stored correct: False.

Field 1, option 2: `\overset{\to }{OV}=\frac{6}{11}r+\frac{5}{11}s`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 3: `\overset{\to }{OV}=r+\frac{5}{6}s`; recipe `(1, s/r)`; stored correct: False.

Field 1, option 4: `\overset{\to }{OV}=\frac{5}{11}r+\frac{6}{11}s`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 5: `\overset{\to }{OV}=\frac{1}{11}r+s`; recipe `(1/(r + s), 1)`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OV}=\overset{\to }{OR}+\overset{\to }{RV}.
$$

We're told that $\overset{\to }{OR}=r,$ so we just need to work out $\overset{\to }{RV}.$

First, from $△ORS,$ we have

$$
\begin{aligned}\overset{\to }{RS} & =\overset{\to }{RO}+\overset{\to }{OS} \\  & =-\overset{\to }{OR}+\overset{\to }{OS} \\  & =-r+s \\  & =s-r.\end{aligned}
$$

Since $RV:VS=6:5,$ we have

$$
\overset{\to }{RV}=\frac{6}{11}\overset{\to }{RS}=\frac{6}{11}(s-r).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OV} & =\overset{\to }{OR}+\overset{\to }{RV} \\  & =r+\frac{6}{11}(s-r) \\  & =\frac{5}{11}r+\frac{6}{11}s.\end{aligned}
$$

### q-120289

Parameters: `{"A": "A", "B": "B", "X": "T", "u": "a", "v": "b", "r": 3, "s": 5}`. Layout: radio.

![](images/52/52e25ccc5b59b3eecd914c5b141e443475a5de58299404528d27f1fc85db97ea.png)

Consider the diagram above, where $\overset{\to }{OA}=a,$ $\overset{\to }{OB}=b$, and $T$ divides $\overset{―}{AB}$ in the ratio $AT:TB=3:5.$ Find $\overset{\to }{OT}.$

Field 1, option 1: `\overset{\to }{OT}=\frac{1}{4}a+\frac{3}{4}b`; recipe `((r - 1)/(r + s), (s + 1)/(r + s))`; stored correct: False.

Field 1, option 2: `\overset{\to }{OT}=\frac{5}{8}a+\frac{3}{8}b`; recipe `(s/(r + s), r/(r + s))`; stored correct: True.

Field 1, option 3: `\overset{\to }{OT}=\frac{3}{8}a+\frac{5}{8}b`; recipe `(r/(r + s), s/(r + s))`; stored correct: False.

Field 1, option 4: `\overset{\to }{OT}=\frac{3}{4}a+\frac{1}{4}b`; recipe `((s + 1)/(r + s), (r - 1)/(r + s))`; stored correct: False.

Field 1, option 5: `\overset{\to }{OT}=\frac{7}{8}a+\frac{1}{8}b`; recipe `((s + 2)/(r + s), (r - 2)/(r + s))`; stored correct: False.

Fixed solution: From the diagram, we see that

$$
\overset{\to }{OT}=\overset{\to }{OA}+\overset{\to }{AT}.
$$

We're told that $\overset{\to }{OA}=a,$ so we just need to work out $\overset{\to }{AT}.$

First, from $△OAB,$ we have

$$
\begin{aligned}\overset{\to }{AB} & =\overset{\to }{AO}+\overset{\to }{OB} \\  & =-\overset{\to }{OA}+\overset{\to }{OB} \\  & =-a+b \\  & =b-a.\end{aligned}
$$

Since $AT:TB=3:5,$ we have

$$
\overset{\to }{AT}=\frac{3}{8}\overset{\to }{AB}=\frac{3}{8}(b-a).
$$

Therefore,

$$
\begin{aligned}\overset{\to }{OT} & =\overset{\to }{OA}+\overset{\to }{AT} \\  & =a+\frac{3}{8}(b-a) \\  & =\frac{5}{8}a+\frac{3}{8}b.\end{aligned}
$$

## Stage 4 — Reusable masks and calculations

Prompt text remains source-shaped; only the complete ratio component and linked diagram asset vary for observed replay. Labels stay fixed in each observed profile. The shared solution reconstructs four displayed blocks, with nine structural rows: path relation; four AB reversal/difference rows; AX scalar-difference chain; three OX substitution/collection rows. All 22 present source solution strings match exactly at source parameters. The blank layout has field-1 and field-2 placeholders in its original line sequence.

Normal authored radio bank is chosen whole: correct (s/D,r/D), reversed weights (r/D,s/D), omitted subtraction of a (1,r/D), negated b coefficient (s/D,−r/D), negated a coefficient (−s/D,r/D). Reject r=s for this radio bank and every whole-bank equivalence collision. No feedback diagnosis is added to learner content. Authored coefficient blanks accept r=s because they contain no distractors.

Mathematical task fingerprints use the normalized ordered weight pair; relabeling vectors or scaling a ratio does not inflate task counts. Complete prompt, fixed solution and displayed bank determine presentation identity, independently of seed/shuffle/profile aliases.

## Source anomalies and repairs

q-278263 (2:3), q-322568 (3:4), q-322576 (8:3), q-322586 (7:9) store both coefficient keys in reversed order relative to supplied vector order and their own correct fixed worked solutions. Raw profiles replay those keys for evidence, native ID/value grading follows those keys, and independent mathematics marks the four source records wrong. `-repaired` profiles put s/D in field-1 and r/D in field-2. All normal authored generation uses the mathematically correct coefficient order.

q-42659 has no difficulty, worked solution or correct designation. The captured authoritative 1106 widget confirms the five choice values and one assessment. The correct 2/3 p+1/3 q is independently derived; the complete shared worked solution and moderate assignment are authored. q-12212 duplicate legacy bank is preserved separately, with missing designation inferred.

Legacy q-42659 prompt/bank uses OP^(→) notation; it remains explicit raw replay evidence. Authored output uses the course overset-arrow vector notation. Choice whitespace is normalized while complete equations, every coefficient, signs and term ordering are preserved mathematically. Regenerated diagrams replace source asset paths, so graph-file bytes are not claimed exact.

Hard admission requires coprime ratio entries: both reduced numerator weights are at least 5 and the irreducible denominator is at least 19 and at most 39. Scaling an easy ratio does not make it hard. Explicit (10,10) and (20,10) regression cases reject; mathematical task identity deduplicates common ratio scaling.
