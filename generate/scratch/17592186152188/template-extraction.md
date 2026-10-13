Stage 1 — Specific source inventory

Each source below records its full prompt, exact radius/translation components, field key/type, every original answer and designation, and the ordered axis/addition/conclusion block counts. All use x/y as coordinates and theta as the eliminated parameter (raw q-327811's t mismatch is explicitly recorded). Source number forms are positive integers, proper/reciprocal rational radii and familiar square roots. The fixed prose is stored in source.json and replayed through complete-component masks; it is not selected according to an error choice.

Stage 2 — Generalized mathematical pattern

Isolate cos(theta) and sin(theta), square each, evaluate radius squares, add using cos²+sin²=1, and state the Cartesian equation. Blanks supply only the required LHS fragment. Radio values are complete equations and are compared modulo nonzero scalar, independently of response-form eligibility. Domain is the entire [0,2pi), so no branch inequalities are introduced.

Stage 3 — Components and complete banks

The tuple (cx,cy,hx,ky) represents cx(x-hx)²+cy(y-ky)²=1 (the `=1` is omitted for the observed blank fragment). Every source option is independently matched to exactly one original operation tuple before parameters vary; source IDs or correct-index position cannot substitute for a value match. Raw bank operations reproduce values but do not prove historical intent. All source members are shown below.

### q-6881 — moderate

Determine the Cartesian equation of the ellipse

$$
x=2\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('2', '1', '0', '0')`; field `selection`, `radio`. Source method bank/fragment.

- `{x}^{2}+{y}^{2}=1` → operation 1 of `recipes("q-6881",p)`. Original tuple `(1, 1, 0, 0)`.
- `\frac{{x}^{2}}{4}-{y}^{2}=1` → operation 2 of `recipes("q-6881",p)`. Original tuple `(1/4, -1, 0, 0)`.
- **Correct** `\frac{{x}^{2}}{4}+{y}^{2}=1` → operation 3 of `recipes("q-6881",p)`. Original tuple `(1/4, 1, 0, 0)`.
- `\frac{{x}^{2}}{2}+{y}^{2}=1` → operation 4 of `recipes("q-6881",p)`. Original tuple `(1/2, 1, 0, 0)`.
- `{x}^{2}+\frac{{y}^{2}}{4}=1` → operation 5 of `recipes("q-6881",p)`. Original tuple `(1, 1/4, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =2\operatorname{cos}⁡\theta  \\ \frac{x}{2} & =\operatorname{cos}⁡\theta  \\ \frac{{x}^{2}}{{2}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{x}^{2}}{4} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =\operatorname{sin}⁡\theta  \\ {y}^{2} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{{x}^{2}}{4}+{y}^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
\frac{{x}^{2}}{4}+{y}^{2}=1.
$$

### q-79375 — hard

Calculate the Cartesian equation of the ellipse

$$
x=4\operatorname{cos}⁡\theta -1,\,y=\operatorname{sin}⁡\theta +1,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('4', '1', '-1', '1')`; field `selection`, `radio`. Opaque intent; raw bank evidence-only.

- `\frac{(x+1)^{2}}{16}+\frac{(y-1)^{2}}{4}=1` → operation 1 of `recipes("q-79375",p)`. Original tuple `(1/16, 1/4, -1, 1)`.
- `\frac{(x-1)^{2}}{16}+(y+1)^{2}=1` → operation 2 of `recipes("q-79375",p)`. Original tuple `(1/16, 1, 1, -1)`.
- `\frac{(x+1)^{2}}{4}+\frac{{y}^{2}}{4}=1` → operation 3 of `recipes("q-79375",p)`. Original tuple `(1/4, 1/4, -1, 0)`.
- `\frac{(x-1)^{2}}{4}+(y+1)^{2}=1` → operation 4 of `recipes("q-79375",p)`. Original tuple `(1/4, 1, 1, -1)`.
- **Correct** `\frac{(x+1)^{2}}{16}+(y-1)^{2}=1` → operation 5 of `recipes("q-79375",p)`. Original tuple `(1/16, 1, -1, 1)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =4\operatorname{cos}⁡\theta -1 \\ \frac{x+1}{4} & =\operatorname{cos}⁡\theta  \\ \frac{(x+1)^{2}}{{4}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x+1)^{2}}{16} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =\operatorname{sin}⁡\theta +1 \\ y-1 & =\operatorname{sin}⁡\theta  \\ (y-1)^{2} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x+1)^{2}}{16}+(y-1)^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
\frac{(x+1)^{2}}{16}+(y-1)^{2}=1.
$$

### q-106405 — moderate

Find the Cartesian equation of the ellipse

$$
x=5\operatorname{cos}⁡\theta ,\,y=4\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('5', '4', '0', '0')`; field `selection`, `radio`. Source method bank/fragment.

- `\frac{{x}^{2}}{16}+\frac{{y}^{2}}{25}=1` → operation 1 of `recipes("q-106405",p)`. Original tuple `(1/16, 1/25, 0, 0)`.
- `\frac{{x}^{2}}{25}-\frac{{y}^{2}}{16}=1` → operation 2 of `recipes("q-106405",p)`. Original tuple `(1/25, -1/16, 0, 0)`.
- **Correct** `\frac{{x}^{2}}{25}+\frac{{y}^{2}}{16}=1` → operation 3 of `recipes("q-106405",p)`. Original tuple `(1/25, 1/16, 0, 0)`.
- `\frac{{x}^{2}}{5}+\frac{{y}^{2}}{4}=1` → operation 4 of `recipes("q-106405",p)`. Original tuple `(1/5, 1/4, 0, 0)`.
- `\frac{{x}^{2}}{16}-\frac{{y}^{2}}{25}=1` → operation 5 of `recipes("q-106405",p)`. Original tuple `(1/16, -1/25, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =5\operatorname{cos}⁡\theta  \\ \frac{x}{5} & =\operatorname{cos}⁡\theta  \\ \frac{{x}^{2}}{{5}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{x}^{2}}{25} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =4\operatorname{sin}⁡\theta  \\ \frac{y}{4} & =\operatorname{sin}⁡\theta  \\ \frac{{y}^{2}}{{4}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{{y}^{2}}{16} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 
Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{{x}^{2}}{25}+\frac{{y}^{2}}{16} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
\frac{{x}^{2}}{25}+\frac{{y}^{2}}{16}=1.
$$

### q-106406 — moderate

Find the Cartesian equation of the ellipse

$$
x=\frac{1}{2}\operatorname{cos}⁡\theta ,\,y=\frac{1}{3}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('1/2', '1/3', '0', '0')`; field `selection`, `radio`. Source method bank/fragment.

- **Correct** `4{x}^{2}+9{y}^{2}=1` → operation 1 of `recipes("q-106406",p)`. Original tuple `(4, 9, 0, 0)`.
- `4{x}^{2}-9{y}^{2}=1` → operation 2 of `recipes("q-106406",p)`. Original tuple `(4, -9, 0, 0)`.
- `9{x}^{2}+4{y}^{2}=1` → operation 3 of `recipes("q-106406",p)`. Original tuple `(9, 4, 0, 0)`.
- `\frac{1}{4}{x}^{2}+\frac{1}{9}{y}^{2}=1` → operation 4 of `recipes("q-106406",p)`. Original tuple `(1/4, 1/9, 0, 0)`.
- `\frac{1}{4}{x}^{2}-\frac{1}{9}{y}^{2}=1` → operation 5 of `recipes("q-106406",p)`. Original tuple `(1/4, -1/9, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =\frac{1}{2}\operatorname{cos}⁡\theta  \\ 2x & =\operatorname{cos}⁡\theta  \\ 4{x}^{2} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =\frac{1}{3}\operatorname{sin}⁡\theta  \\ 3y & =\operatorname{sin}⁡\theta  \\ 9{y}^{2} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 
Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}4{x}^{2}+9{y}^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
4{x}^{2}+9{y}^{2}=1.
$$

### q-106407 — moderate

Find the Cartesian equation of the ellipse

$$
x=\frac{2}{3}\operatorname{cos}⁡\theta ,\,y=\frac{3}{2}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('2/3', '3/2', '0', '0')`; field `selection`, `radio`. Source method bank/fragment.

- `\frac{9}{4}{x}^{2}+\frac{9}{4}{y}^{2}=1` → operation 1 of `recipes("q-106407",p)`. Original tuple `(9/4, 9/4, 0, 0)`.
- `\frac{9}{4}{x}^{2}-\frac{4}{9}{y}^{2}=1` → operation 2 of `recipes("q-106407",p)`. Original tuple `(9/4, -4/9, 0, 0)`.
- `\frac{4}{9}{x}^{2}+\frac{9}{4}{y}^{2}=1` → operation 3 of `recipes("q-106407",p)`. Original tuple `(4/9, 9/4, 0, 0)`.
- `\frac{4}{9}{x}^{2}-\frac{9}{4}{y}^{2}=1` → operation 4 of `recipes("q-106407",p)`. Original tuple `(4/9, -9/4, 0, 0)`.
- **Correct** `\frac{9}{4}{x}^{2}+\frac{4}{9}{y}^{2}=1` → operation 5 of `recipes("q-106407",p)`. Original tuple `(9/4, 4/9, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =\frac{2}{3}\operatorname{cos}⁡\theta  \\ \frac{3}{2}x & =\operatorname{cos}⁡\theta  \\ \frac{9}{4}{x}^{2} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =\frac{3}{2}\operatorname{sin}⁡\theta  \\ \frac{2}{3}y & =\operatorname{sin}⁡\theta  \\ \frac{4}{9}{y}^{2} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 
Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{9}{4}{x}^{2}+\frac{4}{9}{y}^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
\frac{9}{4}{x}^{2}+\frac{4}{9}{y}^{2}=1.
$$

### q-106408 — hard

Calculate the Cartesian equation of the ellipse

$$
x=\frac{1}{2}\operatorname{cos}⁡\theta +2,\,y=\frac{1}{2}\operatorname{sin}⁡\theta +3,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('1/2', '1/2', '2', '3')`; field `selection`, `radio`. Source method bank/fragment.

- `\frac{1}{4}{(x-2)}^{2}+\frac{1}{4}{(y-3)}^{2}=1` → operation 1 of `recipes("q-106408",p)`. Original tuple `(1/4, 1/4, 2, 3)`.
- `4{(x-2)}^{2}-4{(y-3)}^{2}=1` → operation 2 of `recipes("q-106408",p)`. Original tuple `(4, -4, 2, 3)`.
- `4{(x-3)}^{2}+4{(y-2)}^{2}=1` → operation 3 of `recipes("q-106408",p)`. Original tuple `(4, 4, 3, 2)`.
- `\frac{1}{4}{(x-2)}^{2}-\frac{1}{4}{(y-3)}^{2}=1` → operation 4 of `recipes("q-106408",p)`. Original tuple `(1/4, -1/4, 2, 3)`.
- **Correct** `4{(x-2)}^{2}+4{(y-3)}^{2}=1` → operation 5 of `recipes("q-106408",p)`. Original tuple `(4, 4, 2, 3)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =\frac{1}{2}\operatorname{cos}⁡\theta +2 \\ x-2 & =\frac{1}{2}\operatorname{cos}⁡\theta  \\ 2(x-2) & =\operatorname{cos}⁡\theta  \\ 4{(x-2)}^{2} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =\frac{1}{2}\operatorname{sin}⁡\theta +3 \\ y-3 & =\frac{1}{2}\operatorname{sin}⁡\theta  \\ 2(y-3) & =\operatorname{sin}⁡\theta  \\ 4{(y-3)}^{2} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}4{(x-2)}^{2}+4{(y-3)}^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
4{(x-2)}^{2}+4{(y-3)}^{2}=1.
$$

### q-106715 — moderate

Determine the Cartesian equation of the ellipse

$$
x=3\operatorname{cos}⁡\theta ,\,y=5\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('3', '5', '0', '0')`; field `selection`, `radio`. Source method bank/fragment.

- `\frac{{x}^{2}}{9}-\frac{{y}^{2}}{25}=1` → operation 2 of `recipes("q-106715",p)`. Original tuple `(1/9, -1/25, 0, 0)`.
- **Correct** `\frac{{x}^{2}}{9}+\frac{{y}^{2}}{25}=1` → operation 3 of `recipes("q-106715",p)`. Original tuple `(1/9, 1/25, 0, 0)`.
- `\frac{{x}^{2}}{25}+\frac{{y}^{2}}{9}=1` → operation 1 of `recipes("q-106715",p)`. Original tuple `(1/25, 1/9, 0, 0)`.
- `\frac{{x}^{2}}{25}-\frac{{y}^{2}}{9}=1` → operation 5 of `recipes("q-106715",p)`. Original tuple `(1/25, -1/9, 0, 0)`.
- `\frac{{x}^{2}}{3}+\frac{{y}^{2}}{5}=1` → operation 4 of `recipes("q-106715",p)`. Original tuple `(1/3, 1/5, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =3\operatorname{cos}⁡\theta  \\ \frac{x}{3} & =\operatorname{cos}⁡\theta  \\ \frac{{x}^{2}}{{3}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{x}^{2}}{9} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =5\operatorname{sin}⁡\theta  \\ \frac{y}{5} & =\operatorname{sin}⁡\theta  \\ \frac{{y}^{2}}{{5}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{{y}^{2}}{25} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 
Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{{x}^{2}}{9}+\frac{{y}^{2}}{25} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
\frac{{x}^{2}}{9}+\frac{{y}^{2}}{25}=1.
$$

### q-15792 — moderate

Determine the Cartesian equation of the ellipse

$$
x=5\operatorname{cos}⁡\theta ,\,y=3\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('5', '3', '0', '0')`; field `selection`, `radio`. Source method bank/fragment.

- `\frac{{x}^{2}}{25}-\frac{{y}^{2}}{9}=1` → operation 2 of `recipes("q-15792",p)`. Original tuple `(1/25, -1/9, 0, 0)`.
- **Correct** `\frac{{x}^{2}}{25}+\frac{{y}^{2}}{9}=1` → operation 3 of `recipes("q-15792",p)`. Original tuple `(1/25, 1/9, 0, 0)`.
- `\frac{{x}^{2}}{5}+\frac{{y}^{2}}{3}=1` → operation 4 of `recipes("q-15792",p)`. Original tuple `(1/5, 1/3, 0, 0)`.
- `\frac{{x}^{2}}{9}-\frac{{y}^{2}}{25}=1` → operation 5 of `recipes("q-15792",p)`. Original tuple `(1/9, -1/25, 0, 0)`.
- `\frac{{x}^{2}}{9}+\frac{{y}^{2}}{25}=1` → operation 1 of `recipes("q-15792",p)`. Original tuple `(1/9, 1/25, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =5\operatorname{cos}⁡\theta  \\ \frac{x}{5} & =\operatorname{cos}⁡\theta  \\ \frac{{x}^{2}}{{5}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{x}^{2}}{25} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =3\operatorname{sin}⁡\theta  \\ \frac{y}{3} & =\operatorname{sin}⁡\theta  \\ \frac{{y}^{2}}{{3}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{{y}^{2}}{9} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 
Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{{x}^{2}}{25}+\frac{{y}^{2}}{9} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
\frac{{x}^{2}}{25}+\frac{{y}^{2}}{9}=1.
$$

### q-15843 — moderate

Determine the Cartesian equation of the ellipse

$$
x=6\operatorname{cos}⁡\theta ,\,y=2\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('6', '2', '0', '0')`; field `selection`, `radio`. Source method bank/fragment.

- `\frac{{y}^{2}}{36}-\frac{{x}^{2}}{4}=1` → operation 1 of `recipes("q-15843",p)`. Original tuple `(-1/4, 1/36, 0, 0)`.
- `\frac{{x}^{2}}{4}+\frac{{y}^{2}}{36}=1` → operation 2 of `recipes("q-15843",p)`. Original tuple `(1/4, 1/36, 0, 0)`.
- `\frac{{x}^{2}}{6}+\frac{{y}^{2}}{2}=1` → operation 3 of `recipes("q-15843",p)`. Original tuple `(1/6, 1/2, 0, 0)`.
- `\frac{{x}^{2}}{4}-\frac{{y}^{2}}{36}=1` → operation 4 of `recipes("q-15843",p)`. Original tuple `(1/4, -1/36, 0, 0)`.
- **Correct** `\frac{{x}^{2}}{36}+\frac{{y}^{2}}{4}=1` → operation 5 of `recipes("q-15843",p)`. Original tuple `(1/36, 1/4, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =6\operatorname{cos}⁡\theta  \\ \frac{x}{6} & =\operatorname{cos}⁡\theta  \\ \frac{{x}^{2}}{{6}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{x}^{2}}{36} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =2\operatorname{sin}⁡\theta  \\ \frac{y}{2} & =\operatorname{sin}⁡\theta  \\ \frac{{y}^{2}}{{2}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{{y}^{2}}{4} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 
Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{{x}^{2}}{36}+\frac{{y}^{2}}{4} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
\frac{{x}^{2}}{36}+\frac{{y}^{2}}{4}=1.
$$

### q-327798 — hard

The Cartesian equation of the ellipse defined by the parametric equations

$$
x=6\operatorname{cos}⁡\theta +3,\,y=2\sqrt{7}\operatorname{sin}⁡\theta -5,\,0\le \theta <2\pi .
$$

is given by

{{field-1}}
$=1.$

Parameters a,b,h,k: `('6', '2*sqrt(7)', '3', '-5')`; field `field-1`, `blank`. Source method bank/fragment.

- **Correct** `\frac{(x-3)^{2}}{36}+\frac{(y+5)^{2}}{28}` → operation 1 of `recipes("q-327798",p)`. Original tuple `(1/36, 1/28, 3, -5)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =6\operatorname{cos}⁡\theta +3 \\ \frac{x-3}{6} & =\operatorname{cos}⁡\theta  \\ \frac{(x-3)^{2}}{{6}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x-3)^{2}}{36} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we obtain

$$
\begin{aligned}y & =2\sqrt{7}\operatorname{sin}⁡\theta -5 \\ \frac{y+5}{2\sqrt{7}} & =\operatorname{sin}⁡\theta  \\ \frac{(y+5)^{2}}{(2\sqrt{7})^{2}} & ={sin}^{2}⁡\theta  \\ \frac{(y+5)^{2}}{28} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x-3)^{2}}{36}+\frac{(y+5)^{2}}{28} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So, the Cartesian equation of the ellipse is

$$
\frac{(x-3)^{2}}{36}+\frac{(y+5)^{2}}{28}=1.
$$

### q-327803 — hard

The Cartesian equation of the ellipse defined by the parametric equations

$$
x=10\operatorname{cos}⁡\theta -4,\,y=3\sqrt{11}\operatorname{sin}⁡\theta +12,\,0\le \theta <2\pi .
$$

is given by

{{field-1}}
$=1.$

Parameters a,b,h,k: `('10', '3*sqrt(11)', '-4', '12')`; field `field-1`, `blank`. Source method bank/fragment.

- **Correct** `\frac{(x+4)^{2}}{100}+\frac{(y-12)^{2}}{99}` → operation 1 of `recipes("q-327803",p)`. Original tuple `(1/100, 1/99, -4, 12)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter  $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =10\operatorname{cos}⁡\theta -4 \\ \frac{x+4}{10} & =\operatorname{cos}⁡\theta  \\ \frac{(x+4)^{2}}{{10}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x+4)^{2}}{100} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we obtain

$$
\begin{aligned}y & =3\sqrt{11}\operatorname{sin}⁡\theta +12 \\ \frac{y-12}{3\sqrt{11}} & =\operatorname{sin}⁡\theta  \\ \frac{(y-12)^{2}}{(3\sqrt{11})^{2}} & ={sin}^{2}⁡\theta  \\ \frac{(y-12)^{2}}{99} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x+4)^{2}}{100}+\frac{(y-12)^{2}}{99} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So, the Cartesian equation of the ellipse is

$$
\frac{(x+4)^{2}}{100}+\frac{(y-12)^{2}}{99}=1.
$$

### q-327808 — moderate

The Cartesian equation of the ellipse defined by the parametric equations

$$
x=4\sqrt{6}\operatorname{cos}⁡\theta ,\,y=5\sqrt{2}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

is given by

{{field-1}}
$=1.$

Parameters a,b,h,k: `('4*sqrt(6)', '5*sqrt(2)', '0', '0')`; field `field-1`, `blank`. Source method bank/fragment.

- **Correct** `\frac{{x}^{2}}{96}+\frac{{y}^{2}}{50}` → operation 1 of `recipes("q-327808",p)`. Original tuple `(1/96, 1/50, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =4\sqrt{6}\operatorname{cos}⁡\theta  \\ \frac{x}{4\sqrt{6}} & =\operatorname{cos}⁡\theta  \\ \frac{{x}^{2}}{(4\sqrt{6})^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{x}^{2}}{96} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we obtain

$$
\begin{aligned}y & =5\sqrt{2}\operatorname{sin}⁡\theta  \\ \frac{y}{5\sqrt{2}} & =\operatorname{sin}⁡\theta  \\ \frac{{y}^{2}}{(5\sqrt{2})^{2}} & ={sin}^{2}⁡\theta  \\ \frac{{y}^{2}}{50} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\frac{{x}^{2}}{96}+\frac{{y}^{2}}{50}={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.
$$

So, the Cartesian equation of the ellipse is

$$
\frac{{x}^{2}}{96}+\frac{{y}^{2}}{50}=1.
$$

### q-327809 — moderate

The Cartesian equation of the ellipse defined by the parametric equations

$$
x=9\operatorname{cos}⁡\theta ,\,y=4\sqrt{3}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

is given by

{{field-1}}
$=1.$

Parameters a,b,h,k: `('9', '4*sqrt(3)', '0', '0')`; field `field-1`, `blank`. Source method bank/fragment.

- **Correct** `\frac{{x}^{2}}{81}+\frac{{y}^{2}}{48}` → operation 1 of `recipes("q-327809",p)`. Original tuple `(1/81, 1/48, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =9\operatorname{cos}⁡\theta  \\ \frac{x}{9} & =\operatorname{cos}⁡\theta  \\ \frac{{x}^{2}}{{9}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{x}^{2}}{81} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we obtain

$$
\begin{aligned}y & =4\sqrt{3}\operatorname{sin}⁡\theta  \\ \frac{y}{4\sqrt{3}} & =\operatorname{sin}⁡\theta  \\ \frac{{y}^{2}}{(4\sqrt{3})^{2}} & ={sin}^{2}⁡\theta  \\ \frac{{y}^{2}}{48} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\frac{{x}^{2}}{81}+\frac{{y}^{2}}{48}={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.
$$

So, the Cartesian equation of the ellipse is

$$
\frac{{x}^{2}}{81}+\frac{{y}^{2}}{48}=1.
$$

### q-327811 — moderate

The Cartesian equation of the ellipse defined by the parametric equations

$$
x=6\sqrt{2}\operatorname{cos}⁡t,\,y=11\operatorname{sin}⁡t,\,0\le \theta <2\pi .
$$

is given by

{{field-1}}
$=1.$

Parameters a,b,h,k: `('6*sqrt(2)', '11', '0', '0')`; field `field-1`, `blank`. Source method bank/fragment.

- **Correct** `\frac{{x}^{2}}{72}+\frac{{y}^{2}}{121}` → operation 1 of `recipes("q-327811",p)`. Original tuple `(1/72, 1/121, 0, 0)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$  We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =6\sqrt{2}\operatorname{cos}⁡\theta  \\ \frac{x}{6\sqrt{2}} & =\operatorname{cos}⁡\theta  \\ \frac{{x}^{2}}{(6\sqrt{2})^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{x}^{2}}{72} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we obtain

$$
\begin{aligned}y & =11\operatorname{sin}⁡\theta  \\ \frac{y}{11} & =\operatorname{sin}⁡\theta  \\ \frac{{y}^{2}}{{11}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{{y}^{2}}{121} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\frac{{x}^{2}}{72}+\frac{{y}^{2}}{121}={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.
$$

So, the Cartesian equation of the ellipse is

$$
\frac{{x}^{2}}{72}+\frac{{y}^{2}}{121}=1.
$$

### q-79377 — hard

Determine the Cartesian equation of the ellipse

$$
x=3\operatorname{cos}⁡\theta -5,\,y=6\operatorname{sin}⁡\theta -2,\,0\le \theta <2\pi .
$$

Parameters a,b,h,k: `('3', '6', '-5', '-2')`; field `selection`, `radio`. Opaque intent; raw bank evidence-only.

- `\frac{(x-5)^{2}}{9}+\frac{(y-2)^{2}}{36}=1` → operation 1 of `recipes("q-79377",p)`. Original tuple `(1/9, 1/36, 5, 2)`.
- `\frac{(x+5)^{2}}{6}+\frac{(y+2)^{2}}{36}=1` → operation 2 of `recipes("q-79377",p)`. Original tuple `(1/6, 1/36, -5, -2)`.
- `\frac{(x+5)^{2}}{9}+\frac{(y+2)^{2}}{18}=1` → operation 3 of `recipes("q-79377",p)`. Original tuple `(1/9, 1/18, -5, -2)`.
- **Correct** `\frac{(x+5)^{2}}{9}+\frac{(y+2)^{2}}{36}=1` → operation 4 of `recipes("q-79377",p)`. Original tuple `(1/9, 1/36, -5, -2)`.
- `\frac{(x-5)^{2}}{3}+\frac{(y-5)^{2}}{6}=1` → operation 5 of `recipes("q-79377",p)`. Original tuple `(1/3, 1/6, 5, 5)`.

Fixed worked solution, with all prose/stages preserved:

To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x & =3\operatorname{cos}⁡\theta -5 \\ \frac{x+5}{3} & =\operatorname{cos}⁡\theta  \\ \frac{(x+5)^{2}}{{3}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x+5)^{2}}{9} & ={cos}^{2}⁡\theta ,\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y & =6\operatorname{sin}⁡\theta -2 \\ \frac{y+2}{6} & =\operatorname{sin}⁡\theta  \\ \frac{(y+2)^{2}}{{6}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{(y+2)^{2}}{36} & ={sin}^{2}⁡\theta .\end{aligned}
$$

 
Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x+5)^{2}}{9}+\frac{(y+2)^{2}}{36} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1.\end{aligned}
$$

So the Cartesian equation of the ellipse is

$$
\frac{(x+5)^{2}}{9}+\frac{(y+2)^{2}}{36}=1.
$$

Stage 4 — Reusable masks and constraints

Fixed: full source prose, prompt verb/layout, trigonometric functions, full interval, answer-field layout, addition identity and conclusion. Variable: complete coefficients, coordinate shift atoms, reciprocal multipliers, unevaluated squared denominators and evaluated denominator components. Conditional source stages are fixed by radius family: unit radii keep the two-row shortcut; reciprocal/fractional coefficients keep multiplication rows; integer/radical radii keep explicit squared-denominator rows. Reciprocal translated sources preserve their separate translation row. Every generated source mask preserves these structures exactly.

Samplers retain observed arithmetic forms: integer radii 2..12; reciprocal denominators 2..9; other reduced rational numerators/denominators 2..9; radical coefficient 2..6 times sqrt(r) with r in {2,3,5,6,7,10,11} and squared radius <=400. Both hard shifts are nonzero integers in [-12,12]. Source zero shifts stay zero, source unit radii stay one, and the equal-radius translated reciprocal mask stays equal-radius. Bounds apply to explicit parameters too. No arbitrary coefficient perturbation constructs wrong answers. Complete banks reject equivalent members rather than replace them. Normal opaque-family banks are explicitly authored method operations.

Variety exceeds the observed bank: authored supplied-isolation has 110 ordered unequal-radius tasks; integer-origin moderate has 110 per same-method bank before duplicate masks are removed. Translated integer families additionally vary 24×24 signed shift pairs. Reciprocal, general rational and familiar-radical sources add their same-method exact forms. Mathematical fingerprints exclude bank aliases, wording and option order, but include supplied-versus-required isolation. Content identity includes difficulty, actual prompt, fixed solution and complete displayed bank.

Native grading checks use the actual application grade_field through the captured in-memory batch executable: all radio selections, canonical blank fragments, independently expanded equivalent fragments and wrong fragments. Algebraic equivalence, response shape, source fidelity and native results have separate checks. The q-327811 spelling anomaly is not silently called a corrected raw source.


Complete generalized historical operations

Each tuple below supplies (cx,cy,hx,ky) for cx(x-hx)^2+cy(y-ky)^2=1. The source option mappings above select these complete operations independently of option ordering.

- `q-6881`: `(1, 1, h, k)`; `(a**(-2), -1/b**2, h, k)`; `(a**(-2), b**(-2), h, k)`; `(1/a, b**(-2), h, k)`; `(b**(-2), a**(-2), h, k)`
- `q-79375`: `(a**(-2), 1/a, h, k)`; `(a**(-2), b**(-2), -h, -k)`; `(1/a, 1/a, h, 0)`; `(1/a, b**(-2), -h, -k)`; `(a**(-2), b**(-2), h, k)`
- `q-106405`: `(b**(-2), a**(-2), h, k)`; `(a**(-2), -1/b**2, h, k)`; `(a**(-2), b**(-2), h, k)`; `(1/a, 1/b, h, k)`; `(b**(-2), -1/a**2, h, k)`
- `q-106406`: `(a**(-2), b**(-2), h, k)`; `(a**(-2), -1/b**2, h, k)`; `(b**(-2), a**(-2), h, k)`; `(a**2, b**2, h, k)`; `(a**2, -b**2, h, k)`
- `q-106407`: `(a**(-2), a**(-2), h, k)`; `(a**(-2), -1/b**2, h, k)`; `(b**(-2), a**(-2), h, k)`; `(b**(-2), -1/a**2, h, k)`; `(a**(-2), b**(-2), h, k)`
- `q-106408`: `(a**2, b**2, h, k)`; `(a**(-2), -1/b**2, h, k)`; `(a**(-2), b**(-2), k, h)`; `(a**2, -b**2, h, k)`; `(a**(-2), b**(-2), h, k)`
- `q-106715`: `(b**(-2), a**(-2), h, k)`; `(a**(-2), -1/b**2, h, k)`; `(a**(-2), b**(-2), h, k)`; `(1/a, 1/b, h, k)`; `(b**(-2), -1/a**2, h, k)`
- `q-15792`: `(b**(-2), a**(-2), h, k)`; `(a**(-2), -1/b**2, h, k)`; `(a**(-2), b**(-2), h, k)`; `(1/a, 1/b, h, k)`; `(b**(-2), -1/a**2, h, k)`
- `q-15843`: `(-1/b**2, a**(-2), h, k)`; `(b**(-2), a**(-2), h, k)`; `(1/a, 1/b, h, k)`; `(b**(-2), -1/a**2, h, k)`; `(a**(-2), b**(-2), h, k)`
- `q-327798`: `(a**(-2), b**(-2), h, k)`
- `q-327803`: `(a**(-2), b**(-2), h, k)`
- `q-327808`: `(a**(-2), b**(-2), h, k)`
- `q-327809`: `(a**(-2), b**(-2), h, k)`
- `q-327811`: `(a**(-2), b**(-2), h, k)`
- `q-79377`: `(a**(-2), b**(-2), -h, -k)`; `(1/(2*a), b**(-2), h, k)`; `(a**(-2), 1/(3*b), h, k)`; `(a**(-2), b**(-2), h, k)`; `(1/a, 1/b, -h, -h)`

The conventional origin integer bank is swapped squared scales; correct squared scales; sign error; both unsquared scales; swapped squared scales with subtraction. Reciprocal banks distinguish reciprocal-square versus direct-square operations. q-106407 additionally copies the first inverse-square factor to the second coordinate. q-106408 swaps the two translations. q-6881 removes scales or fails to square its sole nonunit scale. These method descriptions are interpretation claims limited to visibly defensible operations; q-79375 and q-79377 compounded scale/translation operations remain opaque.
