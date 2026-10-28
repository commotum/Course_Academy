# Originals and generated peers

Raw originals below are evidence, including incorrect/missing labels and refs. Generated records use the documented minimal teaching-label/layout repairs. Observed-bank variants are separate from default authored-bank variants. Moderate/hard are authored levels; source q-37196 is unrated. All examples are deterministic and use the normal generator.

## Raw original q-37192

Given that $f(x,y)=2xy+{y}^{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

Field 0; selection; original correct: ABSENT

- $2r^{2}\cos (2θ) + r^{2}\sin (2θ)$

- $3r^{2}\cos (2θ)$

- $2r\sin (2θ) + 2r\sin^{2} θ$

- $2r\cos (2θ) + r\sin (2θ)$

- $r^{2}\cos θ + r^{2}\sin θ$

Field 1; selection; original correct: 2{r}^{2}\operatorname{cos}⁡(2\theta )+{r}^{2}\operatorname{sin}⁡(2\theta )

- ${r}^{2}\operatorname{cos}⁡\theta +{r}^{2}\operatorname{sin}⁡\theta $

- $2r\operatorname{cos}⁡(2\theta )+r\operatorname{sin}⁡(2\theta )$

- $2r\operatorname{sin}⁡(2\theta )+2r{sin}^{2}⁡\theta $

- $3{r}^{2}\operatorname{cos}⁡(2\theta )$

- $2{r}^{2}\operatorname{cos}⁡(2\theta )+{r}^{2}\operatorname{sin}⁡(2\theta )$

Original worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂f}{∂x}r\operatorname{sin}⁡\theta +\frac{∂f}{∂y}r\operatorname{cos}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=2y,\,\frac{∂f}{∂y}=2x+2y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2r\operatorname{sin}⁡\theta , \\ \frac{∂f}{∂y} & =2r\operatorname{cos}⁡\theta +2r\operatorname{sin}⁡\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta } & =-2r\operatorname{sin}⁡\theta \,r\operatorname{sin}⁡\theta +(2r\operatorname{cos}⁡\theta +2r\operatorname{sin}⁡\theta )r\operatorname{cos}⁡\theta  \\  & =2{r}^{2}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )+{r}^{2}\operatorname{sin}⁡(2\theta ) \\  & =2{r}^{2}\operatorname{cos}⁡(2\theta )+{r}^{2}\operatorname{sin}⁡(2\theta ).\end{aligned}
$$

## Raw original q-37196

Given that $g(x, y) = \ln (x + y)$, find $\frac{∂g}{∂r}$, where $(x, y)$ are Cartesian coordinates and $(r, θ)$ are the corresponding plane polar coordinates.

Field 0; selection; original correct: ABSENT

- $\frac{1}{r}$

- $r$

- $\frac{\cos θ - \sin θ}{\cos θ + \sin θ}$

- $\frac{1}{r\cos θ + r\sin θ}$

- $r^{2}\sin θ$

Original worked solution:

ABSENT; generated solution is authored.

## Raw original q-94999

Given that $h(x,y)={x}^{2}y,$ find $\frac{∂h}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

Field 0; selection; original correct: 3{r}^{2}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta 

- $2{r}^{3}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta $

- $3{r}^{2}\operatorname{cos}⁡\theta $

- ${r}^{2}{cos}^{2}⁡\theta $

- $3{r}^{2}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta $

- $2{r}^{2}{sin}^{2}⁡\theta $

Original worked solution:

Applying the multivariable chain rule for the function $h(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we have

$$
\begin{aligned}\frac{∂h}{∂r} & =\frac{∂h}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂h}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂h}{∂x}\operatorname{cos}⁡\theta +\frac{∂g}{∂y}\operatorname{sin}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂h}{∂x}=2xy,\,\frac{∂h}{∂y}={x}^{2}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂h}{∂x} & =2{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta , \\ \frac{∂h}{∂y} & ={r}^{2}{cos}^{2}⁡\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂h}{∂r} & =(2{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta +({r}^{2}{cos}^{2}⁡\theta )\operatorname{sin}⁡\theta  \\  & =2{r}^{2}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta +{r}^{2}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta  \\  & =3{r}^{2}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta .\end{aligned}
$$

## Raw original q-95109

Given that $w(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}),$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

Field 0; selection; original correct: \frac{2}{r}

- $2{cos}^{2}⁡\theta -1$

- $\frac{r}{2}$

- $2r$

- $\frac{2}{r}$

- ${r}^{2}\operatorname{cos}⁡\theta $

Original worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\operatorname{cos}⁡\theta +\frac{∂w}{∂y}\operatorname{sin}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{∂w}{∂y}=\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =\frac{2r\operatorname{cos}⁡\theta }{{r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta }, \\ \frac{∂w}{∂y} & =\frac{2r\operatorname{sin}⁡\theta }{{r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(\frac{2r\operatorname{cos}⁡\theta }{{r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta })\operatorname{cos}⁡\theta +(\frac{2r\operatorname{sin}⁡\theta }{{r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta })\operatorname{sin}⁡\theta  \\  & =\frac{2r({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )} \\  & =\frac{2}{r}.\end{aligned}
$$

## Raw original q-95112

Given that $f(x,y)={x}^{2},$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

Field 0; selection; original correct: 2r{cos}^{2}⁡\theta 

- $2r{cos}^{2}⁡\theta $

- $2r{sin}^{2}⁡\theta $

- $2r\operatorname{cos}⁡(2\theta )$

- $r{cos}^{2}⁡\theta $

- $r\operatorname{cos}⁡(2\theta )$

Original worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\operatorname{cos}⁡\theta +\frac{∂f}{∂y}\operatorname{sin}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=0\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2r\operatorname{cos}⁡\theta , \\ \frac{∂f}{∂y} & =0.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(2r\operatorname{cos}⁡\theta )\operatorname{cos}⁡\theta +0\,(\operatorname{sin}⁡\theta ) \\  & =2r{cos}^{2}⁡\theta .\end{aligned}
$$

## Raw original q-95113

Given that $g(x,y)={y}^{2},$ find $\frac{∂g}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

Field 0; selection; original correct: {r}^{2}\operatorname{sin}⁡(2\theta )

- $r{cos}^{2}⁡\theta $

- ${r}^{2}(1-{sin}^{2}⁡\theta )$

- $r\operatorname{sin}⁡(2\theta )$

- ${r}^{2}{sin}^{2}⁡\theta $

- ${r}^{2}\operatorname{sin}⁡(2\theta )$

Original worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we have

$$
\begin{aligned}\frac{∂g}{∂\theta } & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂g}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂g}{∂x}r\operatorname{sin}⁡\theta +\frac{∂g}{∂y}r\operatorname{cos}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=0,\,\frac{∂g}{∂y}=2y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂g}{∂y} & =0, \\ \frac{∂g}{∂y} & =2r\operatorname{sin}⁡\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂\theta } & =0\,(-r\operatorname{sin}⁡\theta )+(2r\operatorname{sin}⁡\theta )\,r\operatorname{cos}⁡\theta  \\  & ={r}^{2}\operatorname{sin}⁡(2\theta ).\end{aligned}
$$

## Raw original q-95116

Given that $w(x,y)=\frac{{x}^{2}}{2}+\frac{{y}^{2}}{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

Field 0; selection; original correct: 0

- $1-{r}^{2}\operatorname{sin}⁡(2\theta )$

- ${r}^{2}\operatorname{sin}⁡(2\theta )$

- $0$

- $r{sin}^{2}⁡\theta $

- $r{cos}^{2}⁡\theta $

Original worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta } & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂w}{∂x}r\operatorname{sin}⁡\theta +\frac{∂w}{∂y}r\operatorname{cos}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=x,\,\frac{∂w}{∂y}=y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂y} & =r\operatorname{cos}⁡\theta , \\ \frac{∂w}{∂y} & =r\operatorname{sin}⁡\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta } & =-(r\operatorname{cos}⁡\theta )\,r\operatorname{sin}⁡\theta +(r\operatorname{sin}⁡\theta )\,r\operatorname{cos}⁡\theta  \\  & =-{r}^{2}\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta +{r}^{2}\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta  \\  & =0\end{aligned}
$$

## Generated easy / cross_theta / observed / 1

Parameters: `{"a": 2, "name": "f"}`. Observed complete bank scaled as expression patterns.

Given that $f(x,y)=4xy+2{y}^{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $2\left(2{r}^{2}\cos(2\theta )+{r}^{2}\sin(2\theta )\right)$

B. $2\left(2r\cos(2\theta )+r\sin(2\theta )\right)$

C. $2\left({r}^{2}\cos\theta +{r}^{2}\sin\theta \right)$

D. $2\left(3{r}^{2}\cos(2\theta )\right)$

E. $2\left(2r\sin(2\theta )+2r\sin^{2}\theta \right)$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂f}{∂x}r\sin\theta +\frac{∂f}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=4y,\,\frac{∂f}{∂y}=4x+4y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4r\sin\theta , \\ \frac{∂f}{∂y} & =4r\cos\theta +4r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta} & =-4r\sin\theta \,r\sin\theta +(4r\cos\theta +4r\sin\theta )r\cos\theta  \\ & =4{r}^{2}(\cos^{2}\theta -\sin^{2}\theta )+2{r}^{2}\sin(2\theta) \\ & =4{r}^{2}\cos(2\theta)+2{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / cross_theta / observed / 2

Parameters: `{"a": 3, "name": "w"}`. Observed complete bank scaled as expression patterns.

Given that $w(x,y)=6xy+3{y}^{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $3\left(2{r}^{2}\cos(2\theta )+{r}^{2}\sin(2\theta )\right)$

B. $3\left(2r\sin(2\theta )+2r\sin^{2}\theta \right)$

C. $3\left({r}^{2}\cos\theta +{r}^{2}\sin\theta \right)$

D. $3\left(2r\cos(2\theta )+r\sin(2\theta )\right)$

E. $3\left(3{r}^{2}\cos(2\theta )\right)$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta } & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂w}{∂x}r\sin\theta +\frac{∂w}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=6y,\,\frac{∂w}{∂y}=6x+6y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =6r\sin\theta , \\ \frac{∂w}{∂y} & =6r\cos\theta +6r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =-6r\sin\theta \,r\sin\theta +(6r\cos\theta +6r\sin\theta )r\cos\theta  \\ & =6{r}^{2}(\cos^{2}\theta -\sin^{2}\theta )+3{r}^{2}\sin(2\theta) \\ & =6{r}^{2}\cos(2\theta)+3{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / cross_theta / authored / 1

Parameters: `{"a": 2, "name": "f"}`. Authored default operation bank.

Given that $f(x,y)=4xy+2{y}^{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $- 4 r^{2} \sin^{2}{\left(\theta \right)}$

B. $4 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r^{2} \cos^{2}{\left(\theta \right)}$

C. $- 4 r^{2} \sin^{2}{\left(\theta \right)} + 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}$

D. $4 r \sin^{2}{\left(\theta \right)} + 8 r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $- 4 r \sin^{2}{\left(\theta \right)} + 4 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂f}{∂x}r\sin\theta +\frac{∂f}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=4y,\,\frac{∂f}{∂y}=4x+4y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4r\sin\theta , \\ \frac{∂f}{∂y} & =4r\cos\theta +4r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta} & =-4r\sin\theta \,r\sin\theta +(4r\cos\theta +4r\sin\theta )r\cos\theta  \\ & =4{r}^{2}(\cos^{2}\theta -\sin^{2}\theta )+2{r}^{2}\sin(2\theta) \\ & =4{r}^{2}\cos(2\theta)+2{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / cross_theta / authored / 2

Parameters: `{"a": 3, "name": "w"}`. Authored default operation bank.

Given that $w(x,y)=6xy+3{y}^{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $- 6 r^{2} \sin^{2}{\left(\theta \right)}$

B. $- 6 r \sin^{2}{\left(\theta \right)} + 6 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r \cos^{2}{\left(\theta \right)}$

C. $- 6 r^{2} \sin^{2}{\left(\theta \right)} + 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r^{2} \cos^{2}{\left(\theta \right)}$

D. $6 r^{2} \sin^{2}{\left(\theta \right)} - 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 6 r^{2} \cos^{2}{\left(\theta \right)}$

E. $6 r \sin^{2}{\left(\theta \right)} + 12 r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta } & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂w}{∂x}r\sin\theta +\frac{∂w}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=6y,\,\frac{∂w}{∂y}=6x+6y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =6r\sin\theta , \\ \frac{∂w}{∂y} & =6r\cos\theta +6r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =-6r\sin\theta \,r\sin\theta +(6r\cos\theta +6r\sin\theta )r\cos\theta  \\ & =6{r}^{2}(\cos^{2}\theta -\sin^{2}\theta )+3{r}^{2}\sin(2\theta) \\ & =6{r}^{2}\cos(2\theta)+3{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / cross_theta / legacy / 1

Parameters: `{"a": 2, "name": "f"}`. Observed complete bank scaled as expression patterns.

Given that $f(x,y)=4xy+2{y}^{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $2\left(r^{2}\cos \theta + r^{2}\sin \theta\right)$

B. $2\left(3r^{2}\cos (2\theta)\right)$

C. $2\left(2r^{2}\cos (2\theta) + r^{2}\sin (2\theta)\right)$

D. $2\left(2r\cos (2\theta) + r\sin (2\theta)\right)$

E. $2\left(2r\sin (2\theta) + 2r\sin^{2} \theta\right)$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂f}{∂x}r\sin\theta +\frac{∂f}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=4y,\,\frac{∂f}{∂y}=4x+4y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4r\sin\theta , \\ \frac{∂f}{∂y} & =4r\cos\theta +4r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta} & =-4r\sin\theta \,r\sin\theta +(4r\cos\theta +4r\sin\theta )r\cos\theta  \\ & =4{r}^{2}(\cos^{2}\theta -\sin^{2}\theta )+2{r}^{2}\sin(2\theta) \\ & =4{r}^{2}\cos(2\theta)+2{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / cross_theta / legacy / 2

Parameters: `{"a": 3, "name": "w"}`. Observed complete bank scaled as expression patterns.

Given that $w(x,y)=6xy+3{y}^{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $3\left(r^{2}\cos \theta + r^{2}\sin \theta\right)$

B. $3\left(2r\sin (2\theta) + 2r\sin^{2} \theta\right)$

C. $3\left(2r^{2}\cos (2\theta) + r^{2}\sin (2\theta)\right)$

D. $3\left(3r^{2}\cos (2\theta)\right)$

E. $3\left(2r\cos (2\theta) + r\sin (2\theta)\right)$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta } & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂w}{∂x}r\sin\theta +\frac{∂w}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=6y,\,\frac{∂w}{∂y}=6x+6y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =6r\sin\theta , \\ \frac{∂w}{∂y} & =6r\cos\theta +6r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =-6r\sin\theta \,r\sin\theta +(6r\cos\theta +6r\sin\theta )r\cos\theta  \\ & =6{r}^{2}(\cos^{2}\theta -\sin^{2}\theta )+3{r}^{2}\sin(2\theta) \\ & =6{r}^{2}\cos(2\theta)+3{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / log_linear_r / observed / 1

Parameters: `{"a": 2, "name": "f"}`. Observed complete bank scaled as expression patterns.

Given that $f(x, y) = 2\ln(x+y)$, find $\frac{∂f}{∂r}$, where $(x, y)$ are Cartesian coordinates and $(r, \theta)$ are the corresponding plane polar coordinates.

A. $2\left(r^{2}\sin \theta\right)$

B. $2\left(r\right)$

C. $2\left(\frac{1}{r}\right)$

D. $2\left(\frac{1}{r\cos \theta + r\sin \theta}\right)$

E. $2\left(\frac{\cos \theta - \sin \theta}{\cos \theta + \sin \theta}\right)$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\cos\theta +\frac{∂f}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{2}{x+y},\,\frac{∂f}{∂y}=\frac{2}{x+y}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{2}{r\cos\theta +r\sin\theta }, \\ \frac{∂f}{∂y} & =\frac{2}{r\cos\theta +r\sin\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(\frac{2}{r\cos\theta +r\sin\theta })\cos\theta +(\frac{2}{r\cos\theta +r\sin\theta })\sin\theta  \\ & =\frac{2(\cos\theta +\sin\theta )}{r(\cos\theta +\sin\theta )} \\ & =\frac{2}{r}\end{aligned}
$$

## Generated easy / log_linear_r / observed / 2

Parameters: `{"a": 3, "name": "w"}`. Observed complete bank scaled as expression patterns.

Given that $w(x, y) = 3\ln(x+y)$, find $\frac{∂w}{∂r}$, where $(x, y)$ are Cartesian coordinates and $(r, \theta)$ are the corresponding plane polar coordinates.

A. $3\left(r^{2}\sin \theta\right)$

B. $3\left(\frac{\cos \theta - \sin \theta}{\cos \theta + \sin \theta}\right)$

C. $3\left(\frac{1}{r}\right)$

D. $3\left(r\right)$

E. $3\left(\frac{1}{r\cos \theta + r\sin \theta}\right)$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\cos\theta +\frac{∂w}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=\frac{3}{x+y},\,\frac{∂w}{∂y}=\frac{3}{x+y}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =\frac{3}{r\cos\theta +r\sin\theta }, \\ \frac{∂w}{∂y} & =\frac{3}{r\cos\theta +r\sin\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(\frac{3}{r\cos\theta +r\sin\theta })\cos\theta +(\frac{3}{r\cos\theta +r\sin\theta })\sin\theta  \\ & =\frac{3(\cos\theta +\sin\theta )}{r(\cos\theta +\sin\theta )} \\ & =\frac{3}{r}\end{aligned}
$$

## Generated easy / log_linear_r / authored / 1

Parameters: `{"a": 2, "name": "f"}`. Authored default operation bank.

Given that $f(x, y) = 2\ln(x+y)$, find $\frac{∂f}{∂r}$, where $(x, y)$ are Cartesian coordinates and $(r, \theta)$ are the corresponding plane polar coordinates.

A. $2 r$

B. $- \frac{2}{r}$

C. $\frac{2}{r}$

D. $\frac{- 2 \sin{\left(\theta \right)} + 2 \cos{\left(\theta \right)}}{\sin{\left(\theta \right)} + \cos{\left(\theta \right)}}$

E. $\frac{2}{r \sin{\left(\theta \right)} + r \cos{\left(\theta \right)}}$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\cos\theta +\frac{∂f}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{2}{x+y},\,\frac{∂f}{∂y}=\frac{2}{x+y}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{2}{r\cos\theta +r\sin\theta }, \\ \frac{∂f}{∂y} & =\frac{2}{r\cos\theta +r\sin\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(\frac{2}{r\cos\theta +r\sin\theta })\cos\theta +(\frac{2}{r\cos\theta +r\sin\theta })\sin\theta  \\ & =\frac{2(\cos\theta +\sin\theta )}{r(\cos\theta +\sin\theta )} \\ & =\frac{2}{r}\end{aligned}
$$

## Generated easy / log_linear_r / authored / 2

Parameters: `{"a": 3, "name": "w"}`. Authored default operation bank.

Given that $w(x, y) = 3\ln(x+y)$, find $\frac{∂w}{∂r}$, where $(x, y)$ are Cartesian coordinates and $(r, \theta)$ are the corresponding plane polar coordinates.

A. $3 r$

B. $\frac{3}{r \sin{\left(\theta \right)} + r \cos{\left(\theta \right)}}$

C. $\frac{3}{r}$

D. $- \frac{3}{r}$

E. $\frac{- 3 \sin{\left(\theta \right)} + 3 \cos{\left(\theta \right)}}{\sin{\left(\theta \right)} + \cos{\left(\theta \right)}}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\cos\theta +\frac{∂w}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=\frac{3}{x+y},\,\frac{∂w}{∂y}=\frac{3}{x+y}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =\frac{3}{r\cos\theta +r\sin\theta }, \\ \frac{∂w}{∂y} & =\frac{3}{r\cos\theta +r\sin\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(\frac{3}{r\cos\theta +r\sin\theta })\cos\theta +(\frac{3}{r\cos\theta +r\sin\theta })\sin\theta  \\ & =\frac{3(\cos\theta +\sin\theta )}{r(\cos\theta +\sin\theta )} \\ & =\frac{3}{r}\end{aligned}
$$

## Generated easy / cubic_r / observed / 1

Parameters: `{"a": 2, "name": "f"}`. Observed complete bank scaled as expression patterns.

Given that $f(x,y)=2{x}^{2}y,$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $2\left(2{r}^{2}\sin^{2}\theta \right)$

B. $2\left(3{r}^{2}\cos\theta \right)$

C. $2\left(2{r}^{3}\cos\theta \sin^{2}\theta \right)$

D. $2\left(3{r}^{2}\cos^{2}\theta \sin\theta \right)$

E. $2\left({r}^{2}\cos^{2}\theta \right)$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\cos\theta +\frac{∂f}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=4xy,\,\frac{∂f}{∂y}=2{x}^{2}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4{r}^{2}\cos\theta \sin\theta , \\ \frac{∂f}{∂y} & =2{r}^{2}\cos^{2}\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(4{r}^{2}\cos\theta \sin\theta )\cos\theta +(2{r}^{2}\cos^{2}\theta )\sin\theta  \\ & =4{r}^{2}\cos^{2}\theta \sin\theta +2{r}^{2}\cos^{2}\theta \sin\theta  \\ & =6{r}^{2}\cos^{2}\theta \sin\theta \end{aligned}
$$

## Generated easy / cubic_r / observed / 2

Parameters: `{"a": 3, "name": "w"}`. Observed complete bank scaled as expression patterns.

Given that $w(x,y)=3{x}^{2}y,$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $3\left(2{r}^{2}\sin^{2}\theta \right)$

B. $3\left({r}^{2}\cos^{2}\theta \right)$

C. $3\left(2{r}^{3}\cos\theta \sin^{2}\theta \right)$

D. $3\left(3{r}^{2}\cos\theta \right)$

E. $3\left(3{r}^{2}\cos^{2}\theta \sin\theta \right)$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\cos\theta +\frac{∂w}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=6xy,\,\frac{∂w}{∂y}=3{x}^{2}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =6{r}^{2}\cos\theta \sin\theta , \\ \frac{∂w}{∂y} & =3{r}^{2}\cos^{2}\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(6{r}^{2}\cos\theta \sin\theta )\cos\theta +(3{r}^{2}\cos^{2}\theta )\sin\theta  \\ & =6{r}^{2}\cos^{2}\theta \sin\theta +3{r}^{2}\cos^{2}\theta \sin\theta  \\ & =9{r}^{2}\cos^{2}\theta \sin\theta \end{aligned}
$$

## Generated easy / cubic_r / authored / 1

Parameters: `{"a": 2, "name": "f"}`. Authored default operation bank.

Given that $f(x,y)=2{x}^{2}y,$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $6 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

B. $- 6 r^{2} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

C. $6 r^{2} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

D. $2 r^{2} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

E. $6 r \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\cos\theta +\frac{∂f}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=4xy,\,\frac{∂f}{∂y}=2{x}^{2}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4{r}^{2}\cos\theta \sin\theta , \\ \frac{∂f}{∂y} & =2{r}^{2}\cos^{2}\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(4{r}^{2}\cos\theta \sin\theta )\cos\theta +(2{r}^{2}\cos^{2}\theta )\sin\theta  \\ & =4{r}^{2}\cos^{2}\theta \sin\theta +2{r}^{2}\cos^{2}\theta \sin\theta  \\ & =6{r}^{2}\cos^{2}\theta \sin\theta \end{aligned}
$$

## Generated easy / cubic_r / authored / 2

Parameters: `{"a": 3, "name": "w"}`. Authored default operation bank.

Given that $w(x,y)=3{x}^{2}y,$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $9 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

B. $9 r \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

C. $9 r^{2} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

D. $- 9 r^{2} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

E. $3 r^{2} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\cos\theta +\frac{∂w}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=6xy,\,\frac{∂w}{∂y}=3{x}^{2}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =6{r}^{2}\cos\theta \sin\theta , \\ \frac{∂w}{∂y} & =3{r}^{2}\cos^{2}\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(6{r}^{2}\cos\theta \sin\theta )\cos\theta +(3{r}^{2}\cos^{2}\theta )\sin\theta  \\ & =6{r}^{2}\cos^{2}\theta \sin\theta +3{r}^{2}\cos^{2}\theta \sin\theta  \\ & =9{r}^{2}\cos^{2}\theta \sin\theta \end{aligned}
$$

## Generated easy / log_radial_r / observed / 1

Parameters: `{"a": 2, "name": "f"}`. Observed complete bank scaled as expression patterns.

Given that $f(x,y)=2\ln({x}^{2}+{y}^{2}),$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $2\left({r}^{2}\cos\theta \right)$

B. $2\left(\frac{r}{2}\right)$

C. $2\left(2\cos^{2}\theta -1\right)$

D. $2\left(\frac{2}{r}\right)$

E. $2\left(2r\right)$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\cos\theta +\frac{∂f}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{4x}{{x}^{2}+{y}^{2}},\,\frac{∂f}{∂y}=\frac{4y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{4r\cos\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta }, \\ \frac{∂f}{∂y} & =\frac{4r\sin\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(\frac{4r\cos\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta })\cos\theta +(\frac{4r\sin\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta })\sin\theta  \\ & =\frac{4r(\cos^{2}\theta +\sin^{2}\theta )}{{r}^{2}(\cos^{2}\theta +\sin^{2}\theta )} \\ & =\frac{4}{r}\end{aligned}
$$

## Generated easy / log_radial_r / observed / 2

Parameters: `{"a": 3, "name": "w"}`. Observed complete bank scaled as expression patterns.

Given that $w(x,y)=3\ln({x}^{2}+{y}^{2}),$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $3\left({r}^{2}\cos\theta \right)$

B. $3\left(2r\right)$

C. $3\left(2\cos^{2}\theta -1\right)$

D. $3\left(\frac{r}{2}\right)$

E. $3\left(\frac{2}{r}\right)$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\cos\theta +\frac{∂w}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=\frac{6x}{{x}^{2}+{y}^{2}},\,\frac{∂w}{∂y}=\frac{6y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =\frac{6r\cos\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta }, \\ \frac{∂w}{∂y} & =\frac{6r\sin\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(\frac{6r\cos\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta })\cos\theta +(\frac{6r\sin\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta })\sin\theta  \\ & =\frac{6r(\cos^{2}\theta +\sin^{2}\theta )}{{r}^{2}(\cos^{2}\theta +\sin^{2}\theta )} \\ & =\frac{6}{r}\end{aligned}
$$

## Generated easy / log_radial_r / authored / 1

Parameters: `{"a": 2, "name": "f"}`. Authored default operation bank.

Given that $f(x,y)=2\ln({x}^{2}+{y}^{2}),$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $0$

B. $- \frac{4}{r}$

C. $\frac{4}{r}$

D. $\frac{1}{r}$

E. $4 r$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\cos\theta +\frac{∂f}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{4x}{{x}^{2}+{y}^{2}},\,\frac{∂f}{∂y}=\frac{4y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{4r\cos\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta }, \\ \frac{∂f}{∂y} & =\frac{4r\sin\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(\frac{4r\cos\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta })\cos\theta +(\frac{4r\sin\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta })\sin\theta  \\ & =\frac{4r(\cos^{2}\theta +\sin^{2}\theta )}{{r}^{2}(\cos^{2}\theta +\sin^{2}\theta )} \\ & =\frac{4}{r}\end{aligned}
$$

## Generated easy / log_radial_r / authored / 2

Parameters: `{"a": 3, "name": "w"}`. Authored default operation bank.

Given that $w(x,y)=3\ln({x}^{2}+{y}^{2}),$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $0$

B. $6 r$

C. $\frac{6}{r}$

D. $- \frac{6}{r}$

E. $\frac{3}{2 r}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\cos\theta +\frac{∂w}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=\frac{6x}{{x}^{2}+{y}^{2}},\,\frac{∂w}{∂y}=\frac{6y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =\frac{6r\cos\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta }, \\ \frac{∂w}{∂y} & =\frac{6r\sin\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta }.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(\frac{6r\cos\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta })\cos\theta +(\frac{6r\sin\theta }{{r}^{2}\cos^{2}\theta +{r}^{2}\sin^{2}\theta })\sin\theta  \\ & =\frac{6r(\cos^{2}\theta +\sin^{2}\theta )}{{r}^{2}(\cos^{2}\theta +\sin^{2}\theta )} \\ & =\frac{6}{r}\end{aligned}
$$

## Generated easy / x_square_r / observed / 1

Parameters: `{"a": 2, "name": "f"}`. Observed complete bank scaled as expression patterns.

Given that $f(x,y)=2{x}^{2},$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $2\left(r\cos(2\theta )\right)$

B. $2\left(2r\sin^{2}\theta \right)$

C. $2\left(2r\cos^{2}\theta \right)$

D. $2\left(r\cos^{2}\theta \right)$

E. $2\left(2r\cos(2\theta )\right)$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\cos\theta +\frac{∂f}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=4x,\,\frac{∂f}{∂y}=0\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4r\cos\theta , \\ \frac{∂f}{∂y} & =0.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(4r\cos\theta )\cos\theta +0\,(\sin\theta ) \\ & =4r\cos^{2}\theta \end{aligned}
$$

## Generated easy / x_square_r / observed / 2

Parameters: `{"a": 3, "name": "w"}`. Observed complete bank scaled as expression patterns.

Given that $w(x,y)=3{x}^{2},$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $3\left(r\cos(2\theta )\right)$

B. $3\left(2r\cos(2\theta )\right)$

C. $3\left(2r\cos^{2}\theta \right)$

D. $3\left(2r\sin^{2}\theta \right)$

E. $3\left(r\cos^{2}\theta \right)$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\cos\theta +\frac{∂w}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=6x,\,\frac{∂w}{∂y}=0\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =6r\cos\theta , \\ \frac{∂w}{∂y} & =0.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(6r\cos\theta )\cos\theta +0\,(\sin\theta ) \\ & =6r\cos^{2}\theta \end{aligned}
$$

## Generated easy / x_square_r / authored / 1

Parameters: `{"a": 2, "name": "f"}`. Authored default operation bank.

Given that $f(x,y)=2{x}^{2},$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $4 r \cos{\left(\theta \right)}$

B. $4 r \sin^{2}{\left(\theta \right)}$

C. $4 r \cos^{2}{\left(\theta \right)}$

D. $- 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $2 r \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂f}{∂x}\cos\theta +\frac{∂f}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=4x,\,\frac{∂f}{∂y}=0\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4r\cos\theta , \\ \frac{∂f}{∂y} & =0.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(4r\cos\theta )\cos\theta +0\,(\sin\theta ) \\ & =4r\cos^{2}\theta \end{aligned}
$$

## Generated easy / x_square_r / authored / 2

Parameters: `{"a": 3, "name": "w"}`. Authored default operation bank.

Given that $w(x,y)=3{x}^{2},$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $6 r \cos{\left(\theta \right)}$

B. $3 r \cos^{2}{\left(\theta \right)}$

C. $6 r \cos^{2}{\left(\theta \right)}$

D. $6 r \sin^{2}{\left(\theta \right)}$

E. $- 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =\frac{∂w}{∂x}\cos\theta +\frac{∂w}{∂y}\sin\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=6x,\,\frac{∂w}{∂y}=0\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =6r\cos\theta , \\ \frac{∂w}{∂y} & =0.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(6r\cos\theta )\cos\theta +0\,(\sin\theta ) \\ & =6r\cos^{2}\theta \end{aligned}
$$

## Generated easy / y_square_theta / observed / 1

Parameters: `{"a": 2, "name": "f"}`. Observed complete bank scaled as expression patterns.

Given that $f(x,y)=2{y}^{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $2\left({r}^{2}\sin(2\theta )\right)$

B. $2\left({r}^{2}(1-\sin^{2}\theta )\right)$

C. $2\left(r\cos^{2}\theta \right)$

D. $2\left({r}^{2}\sin^{2}\theta \right)$

E. $2\left(r\sin(2\theta )\right)$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂f}{∂x}r\sin\theta +\frac{∂f}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=0,\,\frac{∂f}{∂y}=4y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =0, \\ \frac{∂f}{∂y} & =4r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta} & =0\,(-r\sin\theta )+(4r\sin\theta )\,r\cos\theta  \\ & =2{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / y_square_theta / observed / 2

Parameters: `{"a": 3, "name": "w"}`. Observed complete bank scaled as expression patterns.

Given that $w(x,y)=3{y}^{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $3\left({r}^{2}\sin(2\theta )\right)$

B. $3\left(r\sin(2\theta )\right)$

C. $3\left(r\cos^{2}\theta \right)$

D. $3\left({r}^{2}(1-\sin^{2}\theta )\right)$

E. $3\left({r}^{2}\sin^{2}\theta \right)$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta } & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂w}{∂x}r\sin\theta +\frac{∂w}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=0,\,\frac{∂w}{∂y}=6y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =0, \\ \frac{∂w}{∂y} & =6r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =0\,(-r\sin\theta )+(6r\sin\theta )\,r\cos\theta  \\ & =3{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / y_square_theta / authored / 1

Parameters: `{"a": 2, "name": "f"}`. Authored default operation bank.

Given that $f(x,y)=2{y}^{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $4 r \sin{\left(\theta \right)}$

B. $- 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

C. $4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

D. $4 r \sin^{2}{\left(\theta \right)}$

E. $4 r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂f}{∂x}r\sin\theta +\frac{∂f}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=0,\,\frac{∂f}{∂y}=4y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =0, \\ \frac{∂f}{∂y} & =4r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta} & =0\,(-r\sin\theta )+(4r\sin\theta )\,r\cos\theta  \\ & =2{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / y_square_theta / authored / 2

Parameters: `{"a": 3, "name": "w"}`. Authored default operation bank.

Given that $w(x,y)=3{y}^{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $6 r \sin{\left(\theta \right)}$

B. $6 r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

C. $6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

D. $- 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $6 r \sin^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta } & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂w}{∂x}r\sin\theta +\frac{∂w}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=0,\,\frac{∂w}{∂y}=6y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =0, \\ \frac{∂w}{∂y} & =6r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =0\,(-r\sin\theta )+(6r\sin\theta )\,r\cos\theta  \\ & =3{r}^{2}\sin(2\theta)\end{aligned}
$$

## Generated easy / radial_theta / observed / 1

Parameters: `{"a": 2, "name": "f"}`. Observed complete bank scaled as expression patterns.

Given that $f(x,y)=\frac{2{x}^{2}}{2}+\frac{2{y}^{2}}{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $2\left(r\cos^{2}\theta \right)$

B. $2\left({r}^{2}\sin(2\theta )\right)$

C. $2\left(1-{r}^{2}\sin(2\theta )\right)$

D. $2\left(r\sin^{2}\theta \right)$

E. $0$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂f}{∂x}r\sin\theta +\frac{∂f}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=2y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2r\cos\theta , \\ \frac{∂f}{∂y} & =2r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta} & =-(2r\cos\theta )\,r\sin\theta +(2r\sin\theta )\,r\cos\theta  \\ & =-2{r}^{2}\sin\theta \cos\theta +2{r}^{2}\sin\theta \cos\theta  \\ & =0\end{aligned}
$$

## Generated easy / radial_theta / observed / 2

Parameters: `{"a": 3, "name": "w"}`. Observed complete bank scaled as expression patterns.

Given that $w(x,y)=\frac{3{x}^{2}}{2}+\frac{3{y}^{2}}{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $3\left(r\cos^{2}\theta \right)$

B. $0$

C. $3\left(1-{r}^{2}\sin(2\theta )\right)$

D. $3\left({r}^{2}\sin(2\theta )\right)$

E. $3\left(r\sin^{2}\theta \right)$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta } & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂w}{∂x}r\sin\theta +\frac{∂w}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=3x,\,\frac{∂w}{∂y}=3y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =3r\cos\theta , \\ \frac{∂w}{∂y} & =3r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =-(3r\cos\theta )\,r\sin\theta +(3r\sin\theta )\,r\cos\theta  \\ & =-3{r}^{2}\sin\theta \cos\theta +3{r}^{2}\sin\theta \cos\theta  \\ & =0\end{aligned}
$$

## Generated easy / radial_theta / authored / 1

Parameters: `{"a": 2, "name": "f"}`. Authored default operation bank.

Given that $f(x,y)=\frac{2{x}^{2}}{2}+\frac{2{y}^{2}}{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $2 r$

B. $- 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

C. $0$

D. $4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂f}{∂x}r\sin\theta +\frac{∂f}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=2y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2r\cos\theta , \\ \frac{∂f}{∂y} & =2r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta} & =-(2r\cos\theta )\,r\sin\theta +(2r\sin\theta )\,r\cos\theta  \\ & =-2{r}^{2}\sin\theta \cos\theta +2{r}^{2}\sin\theta \cos\theta  \\ & =0\end{aligned}
$$

## Generated easy / radial_theta / authored / 2

Parameters: `{"a": 3, "name": "w"}`. Authored default operation bank.

Given that $w(x,y)=\frac{3{x}^{2}}{2}+\frac{3{y}^{2}}{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

A. $3 r$

B. $3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

C. $0$

D. $- 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta ,$ where $x=r\cos\theta $ and $y=r\sin\theta ,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta } & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta } \\  & =-\frac{∂w}{∂x}r\sin\theta +\frac{∂w}{∂y}r\cos\theta .\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=3x,\,\frac{∂w}{∂y}=3y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta ,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =3r\cos\theta , \\ \frac{∂w}{∂y} & =3r\sin\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =-(3r\cos\theta )\,r\sin\theta +(3r\sin\theta )\,r\cos\theta  \\ & =-3{r}^{2}\sin\theta \cos\theta +3{r}^{2}\sin\theta \cos\theta  \\ & =0\end{aligned}
$$

## Generated moderate / quadratic_r / authored / 1

Parameters: `{"a": 2, "b": -1, "c": 4, "name": "h"}`. Authored level and bank.

Given that $h(x,y)=2 x^{2} - x y + 4 y^{2},$ find $\frac{∂h}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $8 r \sin^{2}{\left(\theta \right)} - r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

B. $- 8 r \sin^{2}{\left(\theta \right)} + 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}$

C. $8 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r \cos^{2}{\left(\theta \right)}$

D. $- r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r \cos^{2}{\left(\theta \right)}$

E. $\frac{8 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r \cos^{2}{\left(\theta \right)}}{r}$

Worked solution:

Applying the multivariable chain rule for the function $h(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂h}{∂r} & =\frac{∂h}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂h}{∂y}\cdot \frac{∂y}{∂r} \\  & =(\frac{∂h}{∂x})(\cos{\left(\theta \right)})+(\frac{∂h}{∂y})(\sin{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂h}{∂x}=4 x - y,\,\frac{∂h}{∂y}=- x + 8 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂h}{∂x} & =- r \sin{\left(\theta \right)} + 4 r \cos{\left(\theta \right)}, \\ \frac{∂h}{∂y} & =8 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂h}{∂r} & =(- r \sin{\left(\theta \right)} + 4 r \cos{\left(\theta \right)})(\cos{\left(\theta \right)})+(8 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)})(\sin{\left(\theta \right)}) \\  & =(- r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r \cos^{2}{\left(\theta \right)})+(8 r \sin^{2}{\left(\theta \right)} - r \sin{\left(\theta \right)} \cos{\left(\theta \right)}) \\  & =8 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r \cos^{2}{\left(\theta \right)}\end{aligned}
$$

## Generated moderate / quadratic_r / authored / 2

Parameters: `{"a": 3, "b": -2, "c": 4, "name": "g"}`. Authored level and bank.

Given that $g(x,y)=3 x^{2} - 2 x y + 4 y^{2},$ find $\frac{∂g}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $8 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

B. $\frac{8 r \sin^{2}{\left(\theta \right)} - 4 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r \cos^{2}{\left(\theta \right)}}{r}$

C. $8 r \sin^{2}{\left(\theta \right)} - 4 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r \cos^{2}{\left(\theta \right)}$

D. $- 8 r \sin^{2}{\left(\theta \right)} + 4 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 6 r \cos^{2}{\left(\theta \right)}$

E. $- 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂g}{∂r} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂r} \\  & =(\frac{∂g}{∂x})(\cos{\left(\theta \right)})+(\frac{∂g}{∂y})(\sin{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=6 x - 2 y,\,\frac{∂g}{∂y}=- 2 x + 8 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =- 2 r \sin{\left(\theta \right)} + 6 r \cos{\left(\theta \right)}, \\ \frac{∂g}{∂y} & =8 r \sin{\left(\theta \right)} - 2 r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂r} & =(- 2 r \sin{\left(\theta \right)} + 6 r \cos{\left(\theta \right)})(\cos{\left(\theta \right)})+(8 r \sin{\left(\theta \right)} - 2 r \cos{\left(\theta \right)})(\sin{\left(\theta \right)}) \\  & =(- 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r \cos^{2}{\left(\theta \right)})+(8 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)}) \\  & =8 r \sin^{2}{\left(\theta \right)} - 4 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r \cos^{2}{\left(\theta \right)}\end{aligned}
$$

## Generated moderate / quadratic_theta / authored / 1

Parameters: `{"a": 2, "b": -1, "c": 4, "name": "h"}`. Authored level and bank.

Given that $h(x,y)=2 x^{2} - x y + 4 y^{2},$ find $\frac{∂h}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}$

B. $- r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + r^{2} \cos^{2}{\left(\theta \right)}$

C. $r^{2} \sin^{2}{\left(\theta \right)} + 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}$

D. $r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $\frac{r^{2} \sin^{2}{\left(\theta \right)} + 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}}{r}$

Worked solution:

Applying the multivariable chain rule for the function $h(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂h}{∂\theta} & =\frac{∂h}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂h}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂h}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂h}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂h}{∂x}=4 x - y,\,\frac{∂h}{∂y}=- x + 8 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂h}{∂x} & =- r \sin{\left(\theta \right)} + 4 r \cos{\left(\theta \right)}, \\ \frac{∂h}{∂y} & =8 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂h}{∂\theta} & =(- r \sin{\left(\theta \right)} + 4 r \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(8 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})+(8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}) \\  & =r^{2} \sin^{2}{\left(\theta \right)} + 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}\end{aligned}
$$

## Generated moderate / quadratic_theta / authored / 2

Parameters: `{"a": 3, "b": -2, "c": 4, "name": "g"}`. Authored level and bank.

Given that $g(x,y)=3 x^{2} - 2 x y + 4 y^{2},$ find $\frac{∂g}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)}$

B. $\frac{2 r^{2} \sin^{2}{\left(\theta \right)} + 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)}}{r}$

C. $2 r^{2} \sin^{2}{\left(\theta \right)} + 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)}$

D. $- 2 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}$

E. $2 r^{2} \sin^{2}{\left(\theta \right)} - 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂g}{∂\theta} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂g}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂g}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=6 x - 2 y,\,\frac{∂g}{∂y}=- 2 x + 8 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =- 2 r \sin{\left(\theta \right)} + 6 r \cos{\left(\theta \right)}, \\ \frac{∂g}{∂y} & =8 r \sin{\left(\theta \right)} - 2 r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂\theta} & =(- 2 r \sin{\left(\theta \right)} + 6 r \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(8 r \sin{\left(\theta \right)} - 2 r \cos{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(2 r^{2} \sin^{2}{\left(\theta \right)} - 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})+(8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)}) \\  & =2 r^{2} \sin^{2}{\left(\theta \right)} + 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)}\end{aligned}
$$

## Generated hard / cubic_sum_theta / authored / 1

Parameters: `{"a": 2, "b": -1, "name": "g"}`. Authored level and bank.

Given that $g(x,y)=2 x^{2} y - x y^{2},$ find $\frac{∂g}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $- 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 2 r^{3} \cos^{3}{\left(\theta \right)}$

B. $- r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}$

C. $r^{3} \sin^{3}{\left(\theta \right)} - 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 2 r^{3} \cos^{3}{\left(\theta \right)}$

D. $r^{3} \sin^{3}{\left(\theta \right)} - 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $\frac{r^{3} \sin^{3}{\left(\theta \right)} - 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 2 r^{3} \cos^{3}{\left(\theta \right)}}{r}$

Worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂g}{∂\theta} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂g}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂g}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=4 x y - y^{2},\,\frac{∂g}{∂y}=2 x^{2} - 2 x y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =- r^{2} \sin^{2}{\left(\theta \right)} + 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}, \\ \frac{∂g}{∂y} & =- 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂\theta} & =(- r^{2} \sin^{2}{\left(\theta \right)} + 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(- 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(r^{3} \sin^{3}{\left(\theta \right)} - 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)})+(- 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 2 r^{3} \cos^{3}{\left(\theta \right)}) \\  & =r^{3} \sin^{3}{\left(\theta \right)} - 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 2 r^{3} \cos^{3}{\left(\theta \right)}\end{aligned}
$$

## Generated hard / cubic_sum_theta / authored / 2

Parameters: `{"a": 3, "b": -2, "name": "h"}`. Authored level and bank.

Given that $h(x,y)=3 x^{2} y - 2 x y^{2},$ find $\frac{∂h}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $- 4 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 3 r^{3} \cos^{3}{\left(\theta \right)}$

B. $\frac{2 r^{3} \sin^{3}{\left(\theta \right)} - 6 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 3 r^{3} \cos^{3}{\left(\theta \right)}}{r}$

C. $2 r^{3} \sin^{3}{\left(\theta \right)} - 6 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 3 r^{3} \cos^{3}{\left(\theta \right)}$

D. $- 2 r^{3} \sin^{3}{\left(\theta \right)} + 6 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 3 r^{3} \cos^{3}{\left(\theta \right)}$

E. $2 r^{3} \sin^{3}{\left(\theta \right)} - 6 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $h(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂h}{∂\theta} & =\frac{∂h}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂h}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂h}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂h}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂h}{∂x}=6 x y - 2 y^{2},\,\frac{∂h}{∂y}=3 x^{2} - 4 x y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂h}{∂x} & =- 2 r^{2} \sin^{2}{\left(\theta \right)} + 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}, \\ \frac{∂h}{∂y} & =- 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂h}{∂\theta} & =(- 2 r^{2} \sin^{2}{\left(\theta \right)} + 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(- 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(2 r^{3} \sin^{3}{\left(\theta \right)} - 6 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)})+(- 4 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 3 r^{3} \cos^{3}{\left(\theta \right)}) \\  & =2 r^{3} \sin^{3}{\left(\theta \right)} - 6 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 3 r^{3} \cos^{3}{\left(\theta \right)}\end{aligned}
$$

## Generated hard / log_quadratic_theta / authored / 1

Parameters: `{"a": 2, "b": -1, "c": 4, "name": "h"}`. Authored level and bank.

Given that $h(x,y)=\ln{\left(2 x^{2} - x y + 4 y^{2} \right)},$ find $\frac{∂h}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $\frac{8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{r^{2} \cos^{2}{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}}$

B. $- \frac{\sin^{2}{\left(\theta \right)} + 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - \cos^{2}{\left(\theta \right)}}{4 \sin^{2}{\left(\theta \right)} - \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 \cos^{2}{\left(\theta \right)}}$

C. $\frac{\sin^{2}{\left(\theta \right)} + 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - \cos^{2}{\left(\theta \right)}}{4 \sin^{2}{\left(\theta \right)} - \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 \cos^{2}{\left(\theta \right)}}$

D. $\frac{r^{2} \sin^{2}{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}}$

E. $\frac{\sin^{2}{\left(\theta \right)} + 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - \cos^{2}{\left(\theta \right)}}{r \left(4 \sin^{2}{\left(\theta \right)} - \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 \cos^{2}{\left(\theta \right)}\right)}$

Worked solution:

Applying the multivariable chain rule for the function $h(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂h}{∂\theta} & =\frac{∂h}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂h}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂h}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂h}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂h}{∂x}=\frac{4 x - y}{2 x^{2} - x y + 4 y^{2}},\,\frac{∂h}{∂y}=\frac{- x + 8 y}{2 x^{2} - x y + 4 y^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂h}{∂x} & =\frac{- r \sin{\left(\theta \right)} + 4 r \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}}, \\ \frac{∂h}{∂y} & =\frac{8 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂h}{∂\theta} & =(\frac{- r \sin{\left(\theta \right)} + 4 r \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}})(- r \sin{\left(\theta \right)})+(\frac{8 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}})(r \cos{\left(\theta \right)}) \\  & =(\frac{r^{2} \sin^{2}{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}})+(\frac{8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{r^{2} \cos^{2}{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{2} \cos^{2}{\left(\theta \right)}}) \\  & =\frac{\sin^{2}{\left(\theta \right)} + 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - \cos^{2}{\left(\theta \right)}}{4 \sin^{2}{\left(\theta \right)} - \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 \cos^{2}{\left(\theta \right)}}\end{aligned}
$$

## Generated hard / log_quadratic_theta / authored / 2

Parameters: `{"a": 3, "b": -2, "c": 4, "name": "g"}`. Authored level and bank.

Given that $g(x,y)=\ln{\left(3 x^{2} - 2 x y + 4 y^{2} \right)},$ find $\frac{∂g}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $\frac{8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{2 r^{2} \cos^{2}{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}}$

B. $\frac{2 \sin^{2}{\left(\theta \right)} + 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 \cos^{2}{\left(\theta \right)}}{r \left(4 \sin^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 \cos^{2}{\left(\theta \right)}\right)}$

C. $\frac{2 \sin^{2}{\left(\theta \right)} + 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 \cos^{2}{\left(\theta \right)}}{4 \sin^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 \cos^{2}{\left(\theta \right)}}$

D. $- \frac{2 \sin^{2}{\left(\theta \right)} + 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 \cos^{2}{\left(\theta \right)}}{4 \sin^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 \cos^{2}{\left(\theta \right)}}$

E. $\frac{2 r^{2} \sin^{2}{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}}$

Worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂g}{∂\theta} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂g}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂g}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=\frac{6 x - 2 y}{3 x^{2} - 2 x y + 4 y^{2}},\,\frac{∂g}{∂y}=\frac{- 2 x + 8 y}{3 x^{2} - 2 x y + 4 y^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{- 2 r \sin{\left(\theta \right)} + 6 r \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}}, \\ \frac{∂g}{∂y} & =\frac{8 r \sin{\left(\theta \right)} - 2 r \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂\theta} & =(\frac{- 2 r \sin{\left(\theta \right)} + 6 r \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}})(- r \sin{\left(\theta \right)})+(\frac{8 r \sin{\left(\theta \right)} - 2 r \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}})(r \cos{\left(\theta \right)}) \\  & =(\frac{2 r^{2} \sin^{2}{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}})+(\frac{8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{2 r^{2} \cos^{2}{\left(\theta \right)}}{4 r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}}) \\  & =\frac{2 \sin^{2}{\left(\theta \right)} + 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 \cos^{2}{\left(\theta \right)}}{4 \sin^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 \cos^{2}{\left(\theta \right)}}\end{aligned}
$$
