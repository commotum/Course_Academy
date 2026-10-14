# Template extraction

Backbone: equal positive cosine/sine amplitudes, complete 0<=theta<2pi domain; eliminate theta using cos²+sin²=1. Never generate ellipses, reversed sine/cosine roles, partial arcs, extra operations or whole-equation blanks. Moderate squares both equations then adds; hard isolates each trig term, divides by r, squares, adds and multiplies by r². Keys are the Cartesian circle or its three source equation fragments.

Parameter slots: r>0 with integer/half-integer forms; translated nonzero h,k independently signed integer, half or quarter values. Keep origin slots zero for moderate and y-shift zero for the observed x-only hard template. Conservative same-method generalization varies signs and magnitudes while preserving these roles. Sampling bounds r=n/d, n=1..14, d in {1,2}, r!=1; nonzero h,k=n/d, n=-13..13 excluding 0, d in {1,2,4}. Reject full-bank equivalences/collisions. Original replay can include all observed values; normal sampling is intentionally bounded.

Blank equation signs follow h,k; answers are abs(h), abs(k), r² in field-1/2/3 respectively. No new distractors or learner feedback. Full-domain sufficiency follows cosine/sine parametrization of every circle point.

Distinctness uses (positive radius, centre) even when banks or field layouts differ. Seed, UUID, option order, or alternative banks of the same circle never replenish another question.

Source wording retained at the operative stages; clean TeX and the correct term Pythagorean identity replace inconsistent source typography/theorem wording. Exact literal fidelity is not claimed. Replays compare full polynomials up to nonzero scale, keys and field layouts separately from prose.


## Bank origin-a

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(h, k, r**2, -1), (h, k, r, -1), (h, k, sqrt(r), 1), (h, k, r, 1), (h, k, r**2, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank origin-b

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(h, k, r**2, 1), (h, k, sqrt(r), -1), (h, k, 2*r**2, -1), (h, k, r, 1), (h, k, r**4, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank origin-c

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(h, k, 2*r, 1), (h, k, r, 1), (h, k, r**2 + r, -1), (h, k, r**2, 1), (h, k, sqrt(r), -1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank translated-a

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(-h, -k, r**2, 1), (h, k, r**2, 1), (k, h, r**2, 1), (h, k, r, 1), (-h, -k, r, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank translated-b

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(h, k, sqrt(r), 1), (h, k, r**2, 1), (-h, -k, r, 1), (-h, -k, r**2, 1), (h, k, r, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank translated-c

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(h, k, r**2, 1), (k, h, r, 1), (h, k, r, 1), (-h, -k, r**2, 1), (k, -h, 4*r, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank translated-d

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(-h, -k, r, 1), (h, k, r**2, 1), (-h, -k, 2*r**2, 1), (h, k, r, 1), (-h, -k, r**2, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank translated-e

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(h, k, 2*r, 1), (h, k, r**2, 1), (-h, -k, r**2, 1), (h, k, r, 1), (-h, -k, r, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank translated-f

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(h, k, r, 1), (-h, -k, r**2, 1), (h, r, r**2, 1), (h, k, r**2, 1), (-h, -r, r, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Bank unrated

Ordered recipes as (x-centre, y-centre, RHS, sign between squared terms):

[(h, k, r**2, 1), (h, k, r, 1), (-h, -k, r**2, 1), (-h, -k, 2*r, 1), (h, k, 2*r, 1)]

These preserve observed complete banks. Error interpretations are conservative: sign-reflected centres, swapped coordinates, unsquared/doubled radii and altered powers. Compound or sparse errors retain the expression pattern rather than claiming a psychological explanation. In translated-c, observed RHS 2 at r=1/2 is mapped to 4r; this interpretation is unresolved and the explicit recipe is a same-method bank extrapolation. Origin-b uses 2r² while origin-c uses r²+r; they are separate profiles.


## Source q-15799

{"source_id": "q-15799", "db_id": 17592186088020, "r": "9", "h": "-3", "k": "5", "profile": "unrated", "difficulty": "unclassified", "field_type": ":answer-field.type/radio"}

Determine the Cartesian equation of the circle

$x = 9\cos θ - 3, y = 9\sin θ + 5, 0 \le θ < 2π$.

Source values by field:

selection: ['(x + 3)^{2} + (y - 5)^{2} = 81', '(x + 3)^{2} + (y - 5)^{2} = 9', '(x - 3)^{2} + (y + 5)^{2} = 81', '(x - 3)^{2} + (y + 5)^{2} = 18', '(x + 3)^{2} + (y - 5)^{2} = 18']

Missing solution; excluded.


## Source q-6879

{"source_id": "q-6879", "db_id": 17592186088272, "r": "3", "h": "0", "k": "0", "profile": "origin-a", "difficulty": "moderate", "field_type": ":answer-field.type/radio"}

Calculate the Cartesian equation of the circle

$$
x=3\operatorname{cos}⁡\theta ,\,y=3\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['{x}^{2}-{y}^{2}=9', '{x}^{2}-{y}^{2}=3', '{x}^{2}+{y}^{2}=\\sqrt{3}', '{x}^{2}+{y}^{2}=3', '{x}^{2}+{y}^{2}=9']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By squaring the $x$-equation, we get

$$
\begin{aligned}x & =3\operatorname{cos}⁡\theta  \\ {x}^{2} & =(3\operatorname{cos}⁡\theta )^{2} \\  & =9{cos}^{2}⁡\theta .\end{aligned}
$$

By squaring the $y$-equation, we get

$$
\begin{aligned}y & =3\operatorname{sin}⁡\theta  \\ {y}^{2} & =(3\operatorname{sin}⁡\theta )^{2} \\  & =9{sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}{x}^{2}+{y}^{2} & =9{cos}^{2}⁡\theta +9{sin}^{2}⁡\theta  \\  & =9({cos}^{2}⁡\theta +{sin}^{2}⁡\theta ) \\  & =9(1) \\  & =9.\end{aligned}
$$

Therefore the Cartesian equation is ${x}^{2}+{y}^{2}=9.$


## Source q-106299

{"source_id": "q-106299", "db_id": 17592186241157, "r": "3/2", "h": "-1", "k": "-2", "profile": "translated-a", "difficulty": "hard", "field_type": ":answer-field.type/radio"}

Determine the Cartesian equation of the circle

$$
x=\frac{3}{2}\operatorname{cos}⁡\theta -1,\,y=\frac{3}{2}\operatorname{sin}⁡\theta -2,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['{(x-1)}^{2}+{(y-2)}^{2}=\\frac{9}{4}', '{(x+1)}^{2}+{(y+2)}^{2}=\\frac{9}{4}', '{(x+2)}^{2}+{(y+1)}^{2}=\\frac{9}{4}', '{(x+1)}^{2}+{(y+2)}^{2}=\\frac{3}{2}', '{(x-1)}^{2}+{(y-2)}^{2}=\\frac{3}{2}']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x+1 & =\frac{3}{2}\operatorname{cos}⁡\theta  \\ \frac{2}{3}(x+1) & =\operatorname{cos}⁡\theta  \\ \frac{4}{9}{(x+1)}^{2} & ={cos}^{2}⁡\theta \end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y+2 & =\frac{3}{2}\operatorname{sin}⁡\theta  \\ \frac{2}{3}(y+2) & ={sin}^{2}⁡\theta  \\ \frac{4}{9}{(y+2)}^{2} & ={sin}^{2}⁡\theta \end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{4}{9}{(x+1)}^{2}+\frac{4}{9}{(y+2)}^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ 4{(x+1)}^{2}+4{(y+2)}^{2} & =9 \\ {(x+1)}^{2}+{(y+2)}^{2} & =\frac{9}{4}\end{aligned}
$$

Therefore the Cartesian equation of the circle is ${(x+1)}^{2}+{(y+2)}^{2}=\frac{9}{4}.$


## Source q-106300

{"source_id": "q-106300", "db_id": 17592186241158, "r": "5", "h": "1/2", "k": "-1/2", "profile": "translated-b", "difficulty": "hard", "field_type": ":answer-field.type/radio"}

Determine the Cartesian equation of the circle

$$
x=5\operatorname{cos}⁡\theta +\frac{1}{2},\,y=5\operatorname{sin}⁡\theta -\frac{1}{2},\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['{(x-\\frac{1}{2})}^{2}+{(y+\\frac{1}{2})}^{2}=\\sqrt{5}', '{(x-\\frac{1}{2})}^{2}+{(y+\\frac{1}{2})}^{2}=25', '{(x+\\frac{1}{2})}^{2}+{(y-\\frac{1}{2})}^{2}=5', '{(x+\\frac{1}{2})}^{2}+{(y-\\frac{1}{2})}^{2}=25', '{(x-\\frac{1}{2})}^{2}+{(y+\\frac{1}{2})}^{2}=5']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}(x-\frac{1}{2}) & =5\operatorname{cos}⁡\theta  \\ \frac{1}{5}(x-\frac{1}{2}) & =\operatorname{cos}⁡\theta  \\ \frac{1}{25}{(x-\frac{1}{2})}^{2} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}(y+\frac{1}{2}) & =5\operatorname{sin}⁡\theta  \\ \frac{1}{5}(y+\frac{1}{2}) & =\operatorname{sin}⁡\theta  \\ \frac{1}{25}{(y+\frac{1}{2})}^{2} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{1}{25}{(x-\frac{1}{2})}^{2}+\frac{1}{25}{(y+\frac{1}{2})}^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{1}{25}{(x-\frac{1}{2})}^{2}+\frac{1}{25}{(y+\frac{1}{2})}^{2} & =1 \\ {(x-\frac{1}{2})}^{2}+{(y+\frac{1}{2})}^{2} & =25.\end{aligned}
$$

Therefore the Cartesian equation is ${(x-\frac{1}{2})}^{2}+{(y+\frac{1}{2})}^{2}=25.$


## Source q-106696

{"source_id": "q-106696", "db_id": 17592186243923, "r": "5/2", "h": "0", "k": "0", "profile": "origin-a", "difficulty": "moderate", "field_type": ":answer-field.type/radio"}

Calculate the Cartesian equation of the circle

$$
x=\frac{5}{2}\operatorname{cos}⁡\theta ,\,y=\frac{5}{2}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['{x}^{2}+{y}^{2}=\\frac{5}{2}', '{x}^{2}+{y}^{2}=\\frac{25}{4}', '{x}^{2}-{y}^{2}=\\frac{25}{4}', '{x}^{2}-{y}^{2}=\\frac{5}{2}', '{x}^{2}+{y}^{2}=\\sqrt{\\frac{5}{2}}']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By squaring the $x$-equation, we get

$$
\begin{aligned}x & =\frac{5}{2}\operatorname{cos}⁡\theta  \\ {x}^{2} & ={(\frac{5}{2}\operatorname{cos}⁡\theta )}^{2} \\  & =\frac{25}{4}{cos}^{2}⁡\theta .\end{aligned}
$$

By squaring the $y$-equation, we get

$$
\begin{aligned}y & =\frac{5}{2}\operatorname{sin}⁡\theta  \\ {y}^{2} & ={(\frac{5}{2}\operatorname{sin}⁡\theta )}^{2} \\  & =\frac{25}{4}{sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}{x}^{2}+{y}^{2} & =\frac{25}{4}{cos}^{2}⁡\theta +\frac{25}{4}{sin}^{2}⁡\theta  \\  & =\frac{25}{4}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta ) \\  & =\frac{25}{4}(1) \\  & =\frac{25}{4}.\end{aligned}
$$

Therefore the Cartesian equation is ${x}^{2}+{y}^{2}=\frac{25}{4}.$


## Source q-15793

{"source_id": "q-15793", "db_id": 17592186275404, "r": "2", "h": "0", "k": "0", "profile": "origin-b", "difficulty": "moderate", "field_type": ":answer-field.type/radio"}

Determine the Cartesian equation of the circle

$$
x=2\operatorname{cos}⁡\theta ,\,y=2\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['{x}^{2}+{y}^{2}=4', '{x}^{2}-{y}^{2}=\\sqrt{2}', '{x}^{2}-{y}^{2}=8', '{x}^{2}+{y}^{2}=2', '{x}^{2}+{y}^{2}=16']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By squaring the $x$-equation, we get

$$
\begin{aligned}x & =2\operatorname{cos}⁡\theta  \\ {x}^{2} & =(2\operatorname{cos}⁡\theta )^{2} \\  & =4{cos}^{2}⁡\theta .\end{aligned}
$$

By squaring the $y$-equation, we get

$$
\begin{aligned}y & =2\operatorname{sin}⁡\theta  \\ {y}^{2} & =(2\operatorname{sin}⁡\theta )^{2} \\  & =4{sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}{x}^{2}+{y}^{2} & =4{cos}^{2}⁡\theta +4{sin}^{2}⁡\theta  \\  & =4({cos}^{2}⁡\theta +{sin}^{2}⁡\theta ) \\  & =4(1) \\  & =4.\end{aligned}
$$

Therefore the Cartesian equation is ${x}^{2}+{y}^{2}=4.$


## Source q-15845

{"source_id": "q-15845", "db_id": 17592186278192, "r": "1/2", "h": "1", "k": "2", "profile": "translated-c", "difficulty": "hard", "field_type": ":answer-field.type/radio"}

Determine the Cartesian equation of the circle

$$
x=\frac{1}{2}\operatorname{cos}⁡\theta +1,\,y=\frac{1}{2}\operatorname{sin}⁡\theta +2,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['(x-1)^{2}+(y-2)^{2}=\\frac{1}{4}', '(x-2)^{2}+(y-1)^{2}=\\frac{1}{2}', '(x-1)^{2}+(y-2)^{2}=\\frac{1}{2}', '(x+1)^{2}+(y+2)^{2}=\\frac{1}{4}', '(x-2)^{2}+(y+1)^{2}=2']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x-1 & =\frac{1}{2}\operatorname{cos}⁡\theta  \\ 2(x-1) & =\operatorname{cos}⁡\theta  \\ 4(x-1)^{2} & ={cos}^{2}⁡\theta \end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y-2 & =\frac{1}{2}\operatorname{sin}⁡\theta  \\ 2(y-2) & ={sin}^{2}⁡\theta  \\ 4(y-2)^{2} & ={sin}^{2}⁡\theta \end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}4(x-1)^{2}+4(y-2)^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ 4(x-1)^{2}+4(y-2)^{2} & =1 \\ (x-1)^{2}+(y-2)^{2} & =\frac{1}{4}\end{aligned}
$$

Hence the Cartesian equation of the circle is $(x-1)^{2}+(y-2)^{2}=\frac{1}{4}.$


## Source q-275313

{"source_id": "q-275313", "db_id": 17592186292837, "r": "6", "h": "2", "k": "-1", "profile": "blank", "difficulty": "hard", "field_type": ":answer-field.type/blank"}

The Cartesian equation of the circle defined by the parametric equations

$$
x=6\operatorname{cos}⁡\theta +2,\,y=6\operatorname{sin}⁡\theta -1,\,0\le \theta <2\pi 
$$

is given by

$(x\,-$
{{field-1}}$)^{2}+(y\,+$
{{field-2}}$)^{2}=$
{{field-3}}.

Source values by field:

field-3: ['36']
field-2: ['1']
field-1: ['2']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}\frac{x-2}{6} & =\operatorname{cos}⁡\theta  \\ \frac{(x-2)^{2}}{{6}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x-2)^{2}}{36} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}\frac{y+1}{6} & =\operatorname{sin}⁡\theta  \\ \frac{(y+1)^{2}}{{6}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{(y+1)^{2}}{36} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x-2)^{2}}{36}+\frac{(y+1)^{2}}{36} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{(x-2)^{2}}{36}+\frac{(y+1)^{2}}{36} & =1 \\ (x-2)^{2}+(y+1)^{2} & =36\end{aligned}
$$

Therefore, the Cartesian equation is $(x-2)^{2}+(y+1)^{2}=36.$


## Source q-321986

{"source_id": "q-321986", "db_id": 17592186302103, "r": "5", "h": "-3", "k": "4", "profile": "blank", "difficulty": "hard", "field_type": ":answer-field.type/blank"}

The Cartesian equation of the circle defined by the parametric equations

$$
x=5\operatorname{cos}⁡\theta -3,\,y=5\operatorname{sin}⁡\theta +4,\,0\le \theta <2\pi 
$$

is given by

$(x\,+$
{{field-1}}$)^{2}+(y\,-$
{{field-2}}$)^{2}=$
{{field-3}}.

Source values by field:

field-1: ['3']
field-2: ['4']
field-3: ['25']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}\frac{x+3}{5} & =\operatorname{cos}⁡\theta  \\ \frac{(x+3)^{2}}{{5}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x+3)^{2}}{25} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}\frac{y-4}{5} & =\operatorname{sin}⁡\theta  \\ \frac{(y-4)^{2}}{{5}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{(y-4)^{2}}{25} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x+3)^{2}}{25}+\frac{(y-4)^{2}}{25} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{(x+3)^{2}}{25}+\frac{(y-4)^{2}}{25} & =1 \\ (x+3)^{2}+(y-4)^{2} & =25\end{aligned}
$$

Therefore, the Cartesian equation is $(x+3)^{2}+(y-4)^{2}=25.$


## Source q-321988

{"source_id": "q-321988", "db_id": 17592186302104, "r": "5/2", "h": "-3", "k": "1", "profile": "blank", "difficulty": "hard", "field_type": ":answer-field.type/blank"}

The Cartesian equation of the circle defined by the parametric equations

$$
x=\frac{5}{2}\operatorname{cos}⁡\theta -3,\,y=\frac{5}{2}\operatorname{sin}⁡\theta +1,\,0\le \theta <2\pi 
$$

is given by

$(x\,+$
{{field-1}}$)^{2}+(y\,-$
{{field-2}}$)^{2}=$
{{field-3}}.

Source values by field:

field-1: ['3']
field-3: ['\\frac{25}{4}']
field-2: ['1']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x+3 & =\frac{5}{2}\operatorname{cos}⁡\theta  \\ \frac{2}{5}(x+3) & =\operatorname{cos}⁡\theta  \\ \frac{4}{25}{(x+3)}^{2} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y-1 & =\frac{5}{2}\operatorname{sin}⁡\theta  \\ \frac{2}{5}(y-1) & =\operatorname{sin}⁡\theta  \\ \frac{4}{25}{(y-1)}^{2} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{4}{25}{(x+3)}^{2}+\frac{4}{25}{(y-1)}^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{4}{25}{(x+3)}^{2}+\frac{4}{25}{(y-1)}^{2} & =1 \\ {(x+3)}^{2}+{(y-1)}^{2} & =\frac{25}{4}.\end{aligned}
$$

Therefore, the Cartesian equation is ${(x+3)}^{2}+{(y-1)}^{2}=\frac{25}{4}.$


## Source q-321989

{"source_id": "q-321989", "db_id": 17592186302105, "r": "3", "h": "7/2", "k": "-11/4", "profile": "blank", "difficulty": "hard", "field_type": ":answer-field.type/blank"}

The Cartesian equation of the circle defined by the parametric equations

$$
x=3\operatorname{cos}⁡\theta +\frac{7}{2},\,y=3\operatorname{sin}⁡\theta -\frac{11}{4},\,0\le \theta <2\pi 
$$

is given by

$(x\,-$
{{field-1}}$)^{2}+(y\,+$
{{field-2}}$)^{2}=$
{{field-3}}.

Source values by field:

field-1: ['\\frac{7}{2}']
field-3: ['9']
field-2: ['\\frac{11}{4}']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x-\frac{7}{2} & =3\operatorname{cos}⁡\theta  \\ \frac{1}{3}(x-\frac{7}{2}) & =\operatorname{cos}⁡\theta  \\ \frac{1}{9}{(x-\frac{7}{2})}^{2} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y+\frac{11}{4} & =3\operatorname{sin}⁡\theta  \\ \frac{1}{3}(y+\frac{11}{4}) & =\operatorname{sin}⁡\theta  \\ \frac{1}{9}{(y+\frac{11}{4})}^{2} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{1}{9}{(x-\frac{7}{2})}^{2}+\frac{1}{9}{(y+\frac{11}{4})}^{2} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{1}{9}{(x-\frac{7}{2})}^{2}+\frac{1}{9}{(y+\frac{11}{4})}^{2} & =1 \\ {(x-\frac{7}{2})}^{2}+{(y+\frac{11}{4})}^{2} & =9.\end{aligned}
$$

Therefore, the Cartesian equation is ${(x-\frac{7}{2})}^{2}+{(y+\frac{11}{4})}^{2}=9.$


## Source q-321991

{"source_id": "q-321991", "db_id": 17592186302106, "r": "7", "h": "-5", "k": "13", "profile": "blank", "difficulty": "hard", "field_type": ":answer-field.type/blank"}

The Cartesian equation of the circle defined by the parametric equations

$$
x=7\operatorname{cos}⁡\theta -5,\,y=7\operatorname{sin}⁡\theta +13,\,0\le \theta <2\pi 
$$

is given by

$(x\,+$
{{field-1}}$)^{2}+(y\,-$
{{field-2}}$)^{2}=$
{{field-3}}.

Source values by field:

field-1: ['5']
field-2: ['13']
field-3: ['49']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}x+5 & =7\operatorname{cos}⁡\theta  \\ \frac{(x+5)^{2}}{{7}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{{(x+5)}^{2}}{49} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}y-13 & =7\operatorname{sin}⁡\theta  \\ \frac{(y-13)^{2}}{{7}^{2}} & =\operatorname{sin}⁡\theta  \\ \frac{{(y-13)}^{2}}{49} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{{(x+5)}^{2}}{49}+\frac{{(y-13)}^{2}}{49} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{{(x+5)}^{2}}{49}+\frac{{(y-13)}^{2}}{49} & =1 \\ {(x+5)}^{2}+{(y-13)}^{2} & =49.\end{aligned}
$$

Therefore, the Cartesian equation is ${(x+5)}^{2}+{(y-13)}^{2}=49.$


## Source q-79219

{"source_id": "q-79219", "db_id": 17592186348178, "r": "7", "h": "0", "k": "0", "profile": "origin-c", "difficulty": "moderate", "field_type": ":answer-field.type/radio"}

Calculate the Cartesian equation of the circle

$$
x=7\operatorname{cos}⁡\theta ,\,y=7\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['{x}^{2}+{y}^{2}=14', '{x}^{2}+{y}^{2}=7', '{x}^{2}-{y}^{2}=56', '{x}^{2}+{y}^{2}=49', '{x}^{2}-{y}^{2}=\\sqrt{7}']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By squaring the $x$-equation, we get

$$
\begin{aligned}x & =7\operatorname{cos}⁡\theta  \\ {x}^{2} & =(7\operatorname{cos}⁡\theta )^{2} \\  & =49{cos}^{2}⁡\theta .\end{aligned}
$$

By squaring the $y$-equation, we get

$$
\begin{aligned}y & =7\operatorname{sin}⁡\theta  \\ {y}^{2} & =(7\operatorname{sin}⁡\theta )^{2} \\  & =49{sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}{x}^{2}+{y}^{2} & =49{cos}^{2}⁡\theta +49{sin}^{2}⁡\theta  \\  & =49({cos}^{2}⁡\theta +{sin}^{2}⁡\theta ) \\  & =49(1) \\  & =49.\end{aligned}
$$

Therefore the Cartesian equation is ${x}^{2}+{y}^{2}=49.$


## Source q-79220

{"source_id": "q-79220", "db_id": 17592186348179, "r": "2", "h": "-1", "k": "4", "profile": "translated-d", "difficulty": "hard", "field_type": ":answer-field.type/radio"}

Determine the Cartesian equation of the circle

$$
x=2\operatorname{cos}⁡\theta -1,\,y=2\operatorname{sin}⁡\theta +4,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['(x-1)^{2}+(y+4)^{2}=2', '(x+1)^{2}+(y-4)^{2}=4', '(x-1)^{2}+(y+4)^{2}=8', '(x+1)^{2}+(y-4)^{2}=2', '(x-1)^{2}+(y+4)^{2}=4']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}\frac{x+1}{2} & =\operatorname{cos}⁡\theta  \\ \frac{(x+1)^{2}}{{2}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x+1)^{2}}{4} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}\frac{y-4}{2} & =\operatorname{sin}⁡\theta  \\ \frac{(y-4)^{2}}{{2}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{(y-4)^{2}}{4} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x+1)^{2}}{4}+\frac{(y-4)^{2}}{4} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{(x+1)^{2}}{4}+\frac{(y-4)^{2}}{4} & =1 \\ (x+1)^{2}+(y-4)^{2} & =4\end{aligned}
$$

Therefore the Cartesian equation is $(x+1)^{2}+(y-4)^{2}=4.$


## Source q-79221

{"source_id": "q-79221", "db_id": 17592186348180, "r": "3", "h": "-2", "k": "-3", "profile": "translated-e", "difficulty": "hard", "field_type": ":answer-field.type/radio"}

Determine the Cartesian equation of the circle

$$
x=3\operatorname{cos}⁡\theta -2,\,y=3\operatorname{sin}⁡\theta -3,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['(x+2)^{2}+(y+3)^{2}=6', '(x+2)^{2}+(y+3)^{2}=9', '(x-2)^{2}+(y-3)^{2}=9', '(x+2)^{2}+(y+3)^{2}=3', '(x-2)^{2}+(y-3)^{2}=3']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}\frac{x+2}{3} & =\operatorname{cos}⁡\theta  \\ \frac{(x+2)^{2}}{{3}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x+2)^{2}}{9} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}\frac{y+3}{3} & =\operatorname{sin}⁡\theta  \\ \frac{(y+3)^{2}}{{3}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{(y+3)^{2}}{9} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x+2)^{2}}{9}+\frac{(y+3)^{2}}{9} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{(x+2)^{2}}{9}+\frac{(y+3)^{2}}{9} & =1 \\ (x+2)^{2}+(y+3)^{2} & =9\end{aligned}
$$

Therefore the Cartesian equation is $(x+2)^{2}+(y+3)^{2}=9.$


## Source q-79222

{"source_id": "q-79222", "db_id": 17592186348181, "r": "4", "h": "5", "k": "0", "profile": "translated-f", "difficulty": "hard", "field_type": ":answer-field.type/radio"}

Determine the Cartesian equation of the circle

$$
x=4\operatorname{cos}⁡\theta +5,\,y=4\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi .
$$

Source values by field:

selection: ['(x-5)^{2}+{y}^{2}=4', '(x+5)^{2}+{y}^{2}=16', '(x-5)^{2}+(y-4)^{2}=16', '(x-5)^{2}+{y}^{2}=16', '(x+5)^{2}+(y+4)^{2}=4']

To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta .$ We can do this using the Pythagorean theorem.

By isolating the $\operatorname{cos}⁡\theta $ term in the $x$-equation and squaring, we get

$$
\begin{aligned}\frac{x-5}{4} & =\operatorname{cos}⁡\theta  \\ \frac{(x-5)^{2}}{{4}^{2}} & ={cos}^{2}⁡\theta  \\ \frac{(x-5)^{2}}{16} & ={cos}^{2}⁡\theta .\end{aligned}
$$

By isolating the $\operatorname{sin}⁡\theta $ term in the $y$-equation and squaring, we get

$$
\begin{aligned}\frac{y}{4} & =\operatorname{sin}⁡\theta  \\ \frac{{y}^{2}}{{4}^{2}} & ={sin}^{2}⁡\theta  \\ \frac{{y}^{2}}{16} & ={sin}^{2}⁡\theta .\end{aligned}
$$

Adding the two equations and using ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1,$ we get

$$
\begin{aligned}\frac{(x-5)^{2}}{16}+\frac{{y}^{2}}{16} & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\ \frac{(x-5)^{2}}{16}+\frac{{y}^{2}}{16} & =1 \\ (x-5)^{2}+{y}^{2} & =16\end{aligned}
$$

Therefore the Cartesian equation is $(x-5)^{2}+{y}^{2}=16.$
