# Template extraction

## Stage 1 — specific source observations

The exact immutable source copy is `source.json`. The following source-specific records include every prompt, field, complete bank, correct designation, and solution-stage sequence. All numerical constants are exact; decimal decay 0.03 means 3/100. Each radio bank is preserved separately because one complete bank does not identify the original wrong-answer algorithm.


### q-4019

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{y}^{2}}$ that satisfies $y(2)=\sqrt[3]{13}.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: ${y}^{3}=3{x}^{2}+1$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2x}{{y}^{2}} \\ {y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2x \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int 2x\,\text{d}x \\ \frac{{y}^{3}}{3} & ={x}^{2}+{C}_{1} \\ {y}^{3} & =3{x}^{2}+3{C}_{1}.\end{aligned}
$$

We conclude that the general solution is

$$
{y}^{3}=3{x}^{2}+C,
$$

where $C=3{C}_{1}$  is an arbitrary constant.

We now apply the condition $y(2)=\sqrt[3]{13}$ to find $C:$

$$
\begin{aligned}{(\sqrt[3]{13})}^{3} & =3(2)^{2}+C \\ 13 & =12+C \\ C & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{y}^{2}}$ that satisfies the condition $y(2)=\sqrt[3]{13}$ is

$$
{y}^{3}=3{x}^{2}+1.
$$

### q-8310

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{x}$ that satisfies $y(1)=2.$ Assume that $x>0.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $y=\frac{2}{1-2\operatorname{ln}⁡x}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{x} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{x} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{x}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{x}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{ln}⁡|x|+C \\ \frac{1}{y} & =-(\operatorname{ln}⁡|x|+C) \\ y & =-\frac{1}{\operatorname{ln}⁡|x|+C}\,.\end{aligned}
$$

Assuming $x>0,$ the general solution is

$$
y=-\frac{1}{\operatorname{ln}⁡x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=2$ to find $C:$

$$
\begin{aligned}y(1) & =2 \\ -\frac{1}{\operatorname{ln}⁡1+C} & =2 \\ -\frac{1}{C} & =2 \\ C & =-\frac{1}{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{x}$ that satisfies the condition $y(1)=2$ is

$$
y=\frac{-1}{(\operatorname{ln}⁡x-\frac{1}{2})}=\frac{2}{1-2\operatorname{ln}⁡x}\,.
$$

### q-168078

Let $\overset{^}{T}(t)$ be a particular solution of the differential equation from the previous part that satisfies the condition $\overset{^}{T}(0)=28.$ Find $\overset{^}{T}(t).$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $\overset{^}{T}(t)\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

Field: :answer-field.type/blank; key `field-1`; RHS expression only.

Correct: $25+3{e}^{-0.03t}$.

Original solution stages and shared sentences:

Previously, we found that the general solution is

$$
T=25+K{e}^{-0.03t}.
$$

where $K$ is an arbitrary constant.

We now apply the condition $T(0)=28$ to find $K:$

$$
\begin{aligned}28 & =25+K\,{e}^{-0.03(0)} \\ 28 & =25+K\,{e}^{0} \\ K & =3\end{aligned}
$$

Thus, the required particular solution is

$$
\overset{^}{T}(t)=25+3{e}^{-0.03t}.
$$

### q-104055

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡y}$ that satisfies $y(0)=\frac{\pi }{2}.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $\operatorname{cos}⁡y=-x$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\operatorname{sin}⁡y} \\ \operatorname{sin}⁡y\frac{\text{d}y}{\text{d}x} & =1 \\ \int \operatorname{sin}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \operatorname{sin}⁡y\,\text{d}y & =\int \,\text{d}x \\ -\operatorname{cos}⁡y & =x+C \\ \operatorname{cos}⁡y & =-x-C.\end{aligned}
$$

We now apply the condition $y(0)=\frac{\pi }{2}$ to find $C:$

$$
\begin{aligned}\operatorname{cos}⁡(\frac{\pi }{2}) & =-0-C \\ 0 & =0-C \\ C & =0\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\operatorname{cos}⁡y=-x
$$

### q-14310

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ given that  $y(\frac{\pi }{2})=1.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $y=\operatorname{tan}⁡(x-\frac{\pi }{4})$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}={y}^{2}+1 \\ \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{{y}^{2}+1}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{arctan}⁡(y) & =x+C \\ y & =\operatorname{tan}⁡(x+C).\end{aligned}
$$

We conclude that the general solution is

$$
y=\operatorname{tan}⁡(x+C).
$$

We now apply the condition $y(\frac{\pi }{2})=1$ to find $C$:

$$
\begin{aligned}1 & =\operatorname{tan}⁡(\frac{\pi }{2}+C) \\ \operatorname{arctan}⁡(1) & =\frac{\pi }{2}+C \\ \frac{\pi }{4} & =\frac{\pi }{2}+C \\ C & =\frac{\pi }{4}-\frac{\pi }{2} \\ C & =-\frac{\pi }{4}.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}={y}^{2}+1$ that satisfies the condition $y(\frac{\pi }{2})=1$ is

$$
y=\operatorname{tan}⁡(x-\frac{\pi }{4}).
$$

### q-14312

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y{e}^{-x}$ that satisfies $y(0)={e}^{-1}.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $y={e}^{-{e}^{-x}}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y{e}^{-x} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & ={e}^{-x} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,dx & =\int {e}^{-x}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {e}^{-x}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-{e}^{-x}+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-{e}^{-x}+C} \\ |y| & ={e}^{-{e}^{-x}+C} \\ y & =\pm {e}^{-{e}^{-x}+C} \\ y & =K{e}^{-{e}^{-x}}\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)={e}^{-1}$ to find $K:$ 

$$
\begin{aligned}{e}^{-1} & =K{e}^{-{e}^{-0}} \\ {e}^{-1} & =K{e}^{-1} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y{e}^{-x}$ that satisfies the condition $y(0)={e}^{-1}$ is

$$
y={e}^{-{e}^{-x}}.
$$

### q-14313

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}}{{y}^{2}}$  that satisfies $y(1)=2.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: ${y}^{3}={x}^{3}+7$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{x}^{2}}{{y}^{2}} \\ {y}^{2}\frac{\text{d}y}{\text{d}x} & ={x}^{2} \\ \int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ \frac{{y}^{3}}{3} & =\frac{{x}^{3}}{3}+{C}_{1} \\ {y}^{3} & ={x}^{3}+C,\end{aligned}
$$

where   $C=3{C}_{1}$ is an arbitrary constant.  

We now apply the condition $y(1)=2$ to find $C:$

$$
\begin{aligned}{2}^{3} & ={1}^{3}+C \\ 8-1 & =C \\ C & =7\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{y}^{3}={x}^{3}+7.
$$

### q-347853

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}+2{y}^{2}=0$
that satisfies the condition $y(0)=2.$

$y(x)=$
{{field-1}}

Field: :answer-field.type/blank; key `field-1`; RHS expression only.

Correct: $\frac{2}{4x+1}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+2{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-2{y}^{2} \\ -\frac{1}{{y}^{2}}\,\text{d}y & =2\,\text{d}x \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int 2\,\text{d}x \\ \frac{1}{y} & =2x+C \\ y & =\frac{1}{2x+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y(x)=\frac{1}{2x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(0)=2$ to find $C:$

$$
\begin{aligned}2 & =\frac{1}{2(0)+C} \\ C & =\frac{1}{2}\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\frac{2}{4x+1}.
$$

### q-355525

Find the particular solution to the differential equation $\operatorname{cos}⁡(3y){y}^{′}-\operatorname{sin}⁡(4x)=0$ that satisfies $y(\frac{\pi }{8})=0.$ Assume that $-\frac{\pi }{6}<y<\frac{\pi }{6}.$

$\operatorname{sin}⁡(3y)=$
{{field-1}}

Field: :answer-field.type/blank; key `field-1`; RHS expression only.

Correct: $-\frac{3}{4}\operatorname{cos}(4x)$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x}-\operatorname{sin}⁡(4x) & =0 \\ \operatorname{cos}⁡(3y)\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(4x) \\ \operatorname{cos}⁡(3y)\,\text{d}y & =\operatorname{sin}⁡(4x)\,\text{d}x \\ \int \operatorname{cos}⁡(3y)\,\text{d}y & =\int \operatorname{sin}⁡(4x)\,\text{d}x \\ \frac{1}{3}\operatorname{sin}⁡(3y) & =-\frac{1}{4}\operatorname{cos}⁡(4x)+{C}_{1} \\ \operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4x)+C,\end{aligned}
$$

where $C=3{C}_{1}.$

We now apply the condition $y(\frac{\pi }{8})=0$ to find $C:$

$$
\begin{aligned}y(\frac{\pi }{8}) & =0 \\ \operatorname{sin}⁡(3\cdot 0) & =-\frac{3}{4}\operatorname{cos}⁡(4\cdot \frac{\pi }{8})+C \\ 0 & =-\frac{3}{4}\operatorname{cos}⁡(\frac{\pi }{2})+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(3y) & =-\frac{3}{4}\operatorname{cos}⁡(4x)\end{aligned}
$$

### q-355528

Find the particular solution to the differential equation
$\frac{\text{d}y}{\text{d}x}=4x\sqrt{y}$
that satisfies the condition $y(1)=9.$  Assume that $y>0.$

$y(x)=$
{{field-1}}

Field: :answer-field.type/blank; key `field-1`; RHS expression only.

Correct: $({x}^{2}+2)^{2}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =4x\sqrt{y} \\ \frac{1}{\sqrt{y}}\,\text{d}y & =4x\,\text{d}x \\ \int \frac{1}{\sqrt{y}}\,\text{d}y & =\int 4x\,\text{d}x \\ 2\sqrt{y} & =2{x}^{2}+{C}_{1} \\ \sqrt{y} & ={x}^{2}+\frac{{C}_{1}}{2} \\ y & ={({x}^{2}+\frac{{C}_{1}}{2})}^{2}.\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y(x)=({x}^{2}+C)^{2},
$$

where $C=\frac{{C}_{1}}{2}$ is an arbitrary constant.

We now apply the condition $y(1)=9$ to find $C:$

$$
\begin{aligned}9 & =((1)^{2}+C)^{2} \\ 9 & =(1+C)^{2} \\ 3 & =1+C \\ C & =2\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=({x}^{2}+2)^{2}.
$$

### q-355544

Find the particular solution to the differential equation ${sec}^{2}⁡(4y){y}^{′}={sec}^{2}⁡(7x)$ that satisfies $y(0)=0.$ Assume that $-\frac{\pi }{8}<y<\frac{\pi }{8}.$

$\operatorname{tan}⁡(4y)=$
{{field-1}}

Field: :answer-field.type/blank; key `field-1`; RHS expression only.

Correct: $\frac{4}{7}\operatorname{tan}(7x)$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{sec}^{2}⁡(4y)\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(7x) \\ {sec}^{2}⁡(4y)\,\text{d}y & ={sec}^{2}⁡(7x)\,\text{d}x \\ \int {sec}^{2}⁡(4y)\,\text{d}y & =\int {sec}^{2}⁡(7x)\,\text{d}x \\ \frac{1}{4}\operatorname{tan}⁡(4y) & =\frac{1}{7}\operatorname{tan}⁡(7x)+{C}_{1} \\ \operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7x)+C,\end{aligned}
$$

where $C=4{C}_{1}.$

We now apply the condition $y(0)=0$ to find $C:$

$$
\begin{aligned}y(0) & =0 \\ \operatorname{tan}⁡(4\cdot 0) & =\frac{4}{7}\operatorname{tan}⁡(7\cdot 0)+C \\ 0 & =0+C \\ C & =0\end{aligned}
$$

So, we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{tan}⁡(4y) & =\frac{4}{7}\operatorname{tan}⁡(7x)\end{aligned}
$$

### q-355562

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=xy$  that satisfies $y(0)=1.$

$y=$
{{field-1}}

Field: :answer-field.type/blank; key `field-1`; RHS expression only.

Correct: ${e}^{{x}^{2}/2}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =xy \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =x \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,x\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{2}{x}^{2}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{x}^{2}/2+C} \\ |y| & ={e}^{{x}^{2}/2+C}\, \\ y & =\pm {e}^{{x}^{2}/2+C} \\ y & =K{e}^{{x}^{2}/2}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=xy$ that satisfies the condition $y(0)=1$ is

$$
y={e}^{{x}^{2}/2}\,.
$$

### q-355578

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}}=0$  that satisfies $y(1)=e.$

$y=$
{{field-1}}

Field: :answer-field.type/blank; key `field-1`; RHS expression only.

Correct: ${e}^{2-1/x}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}} & =0 \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{x}^{2}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{{x}^{2}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{{x}^{2}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\frac{1}{x}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-1/x+C} \\ |y| & ={e}^{-1/x+C}\, \\ |y| & ={e}^{-1/x}\cdot {e}^{C} \\ y & =K{e}^{-1/x}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(1)=e$ to find $K:$ 

$$
\begin{aligned}e & =K{e}^{-1} \\ K & ={e}^{2}\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}-\frac{y}{{x}^{2}}=0$ that satisfies the condition $y(1)=e$ is

$$
y={e}^{2-1/x}\,.
$$

### q-355579

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{x}}$  that satisfies $y(1)={e}^{2}.$

$y=$
{{field-1}}

Field: :answer-field.type/blank; key `field-1`; RHS expression only.

Correct: ${e}^{2\sqrt{x}}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{x}} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{x}} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\frac{1}{\sqrt{x}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\frac{1}{\sqrt{x}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =2\sqrt{x}+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{2\sqrt{x}+C} \\ |y| & ={e}^{2\sqrt{x}+C}\, \\ |y| & ={e}^{2\sqrt{x}}\cdot {e}^{C} \\ y & =K{e}^{2\sqrt{x}}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(1)={e}^{2}$ to find $K:$ 

$$
\begin{aligned}{e}^{2} & =K{e}^{2\sqrt{1}} \\ {e}^{2} & =K{e}^{2} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{y}{\sqrt{x}}$ that satisfies the condition $y(1)={e}^{2}$ is

$$
y={e}^{2\sqrt{x}}\,.
$$

### q-50220

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies $y(1)=1.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $y=\frac{1}{x}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{y}^{2} & =0 \\ \frac{\text{d}y}{\text{d}x} & =-{y}^{2} \\ -\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x} & =1 \\ -\int \frac{1}{{y}^{2}}\,\text{d}y & =\int \,\text{d}x \\ \frac{1}{y} & =x+C \\ y & =\frac{1}{x+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=\frac{1}{x+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=1$ to find $C:$

$$
\begin{aligned}1 & =\frac{1}{1+C} \\ 1+C & =1 \\ C & =0.\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}+{y}^{2}=0$ that satisfies the condition $y(1)=1$ is

$$
y=\frac{1}{x}.
$$

### q-50566

Find the particular solution to the differential equation $y\frac{\text{d}y}{\text{d}x}=x$  that satisfies  $y(-3)=1.$  Assume that $y>0.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $y=\sqrt{{x}^{2}-8}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x} & =x \\ \int y\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int x\,\text{d}x \\ \int y\text{d}y & =\int x\text{d}x \\ \frac{{y}^{2}}{2} & =\frac{{x}^{2}}{2}+{C}_{1} \\ {y}^{2} & ={x}^{2}+2{C}_{1} \\ y & =\pm \sqrt{{x}^{2}+2{C}_{1}}\end{aligned}
$$

Assuming $y>0,$ the general solution is

$$
y=\sqrt{{x}^{2}+C},
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(-3)=1$ to find $C:$

$$
\begin{aligned}1 & =\sqrt{(-3)^{2}+C} \\ 1 & =\sqrt{9+C} \\ C & =-8\end{aligned}
$$

Thus, the particular solution of $y\frac{\text{d}y}{\text{d}x}=x$ that satisfies the condition $y(-3)=1$ is

$$
y=\sqrt{{x}^{2}-8}.
$$

### q-8308

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y$  that satisfies $y(0)=1.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $y={e}^{x}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =1 \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{ln}⁡|y| & =x+C\,.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{x+C} \\ |y| & ={e}^{x+C}\, \\ y & =\pm {e}^{x+C} \\ y & =K{e}^{x}\,.\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the condition $y(0)=1$ to find $K:$ 

$$
\begin{aligned}1 & =K{e}^{0} \\ K & =1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=y$ that satisfies the condition $y(0)=1$ is

$$
y={e}^{x}\,.
$$

### q-8309

Find the particular solution to the differential equation ${y}^{′}=\frac{\operatorname{sin}⁡(3x)}{\operatorname{cos}⁡(2y)}$ that satisfies $y(0)=0.$ Assume that $-\frac{\pi }{4}<y<\frac{\pi }{4}.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x))$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\operatorname{sin}⁡(3x)}{\operatorname{cos}⁡(2y)} \\ (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(3x) \\ \int (\operatorname{cos}⁡(2y))\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(3x)\,\text{d}x \\ \int \operatorname{cos}⁡(2y)\,\text{d}y & =\int \operatorname{sin}⁡(3x)\,\text{d}x \\ \frac{1}{2}\operatorname{sin}⁡(2y) & =-\frac{1}{3}\operatorname{cos}⁡(3x)+C \\ \operatorname{sin}⁡(2y) & =-\frac{2}{3}\operatorname{cos}⁡(3x)+{C}_{1}\,,\end{aligned}
$$

where ${C}_{1}=2C.$

We now apply the condition $y(0)=0$ to find ${C}_{1}:$

$$
\begin{aligned}y(0) & =0 \\ \operatorname{sin}⁡(2\cdot 0) & =-\frac{2}{3}\operatorname{cos}⁡(3\cdot 0)+{C}_{1} \\ \operatorname{sin}⁡(0) & =-\frac{2}{3}\operatorname{cos}⁡(0)+{C}_{1} \\ 0 & =-\frac{2}{3}\cdot 1+{C}_{1} \\ {C}_{1} & =\frac{2}{3}\end{aligned}
$$

So we get the particular solution in implicit form:

$$
\begin{aligned}\operatorname{sin}⁡(2y) & =\frac{2}{3}-\frac{2}{3}\operatorname{cos}⁡(3x) \\  & =\frac{2}{3}(1-\operatorname{cos}⁡(3x))\end{aligned}
$$

Finally, we can write the above equation as

$$
3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x)).
$$

### q-14309

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+1}$  that satisfies $y(1)=1.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: $y=\frac{4}{\pi +4-4\operatorname{arctan}⁡(x)}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{x}^{2}+1} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}+1} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{{x}^{2}+1}\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =\int \frac{1}{{x}^{2}+1}\,\text{d}x \\ -\frac{1}{y} & =\operatorname{arctan}⁡(x)+C \\ \frac{1}{y} & =-(\operatorname{arctan}⁡(x)+C) \\ y & =-\frac{1}{\operatorname{arctan}⁡(x)+C}.\end{aligned}
$$

We conclude that the general solution is

$$
y=-\frac{1}{\operatorname{arctan}⁡(x)+C}.
$$

where $C$ is an arbitrary constant.

We now apply the condition $y(1)=1$ to find $C:$

$$
\begin{aligned}1 & =-\frac{1}{\operatorname{arctan}⁡(1)+C} \\ 1 & =-\frac{1}{\frac{\pi }{4}+C} \\ C & =-\frac{\pi }{4}-1\end{aligned}
$$

Thus, the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+1}$ that satisfies the condition $y(1)=1$ is

$$
y=-\frac{1}{\operatorname{arctan}⁡(x)-\frac{\pi }{4}-1}=\frac{4}{\pi +4-4\operatorname{arctan}⁡(x)}.
$$

### q-50219

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=-\frac{xy}{\operatorname{ln}⁡y}$ that satisfies $y(0)=e.$

Field: :answer-field.type/radio; key `selection`; Complete equations, with original signs/powers preserved.

Correct: ${ln}^{2}⁡y=1-{x}^{2}$.

Original solution stages and shared sentences:

We first find the general solution and then apply the given initial condition to find the particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{xy}{\operatorname{ln}⁡y} \\ \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x} & =-x \\ \int \frac{\operatorname{ln}⁡y}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =-\int x\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\,\text{d}y & =-\int x\,\text{d}x \\ \int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =-\frac{{x}^{2}}{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral in the left-hand side of this equality, we use a substitution $u=\operatorname{ln}⁡y.$ Then,  we have

$$
\frac{\text{d}u}{\text{d}y}=\frac{1}{y}\,⟹\,\text{d}u=\frac{1}{y}\,\text{d}y.
$$

So we get

$$
\begin{aligned}\int \frac{\operatorname{ln}⁡y}{y}\text{d}y & =\int \operatorname{ln}⁡y(\frac{1}{y}\,\text{d}y) \\  & =\int u\,\text{d}u \\  & =\frac{{u}^{2}}{2}+{C}_{2} \\  & =\frac{1}{2}{ln}^{2}⁡y+{C}_{2}.\end{aligned}
$$

Hence,

$$
\begin{aligned}\frac{1}{2}{ln}^{2}⁡y+{C}_{2} & =-\frac{{x}^{2}}{2}+{C}_{1} \\ {ln}^{2}⁡y & =-{x}^{2}+2({C}_{1}-{C}_{2}) \\ {ln}^{2}⁡y & =C-{x}^{2},\end{aligned}
$$

where $C=2({C}_{1}-{C}_{2})$ is an arbitrary constant.

We now apply the condition $y(0)=e$ to find $C:$

$$
\begin{aligned}{ln}^{2}⁡e & =C-{0}^{2} \\ {1}^{2} & =C \\ C & =1\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{ln}^{2}⁡y=1-{x}^{2}.
$$

## Stage 2 — common mathematical pattern

Separate the already separable equation, integrate, and apply one initial value to determine its integration constant. Preserve implicit equations where the original asks for them; preserve RHS fragments where a blank supplies its LHS. Sources with positive square-root or bounded trig assumptions retain those branches. Cooling supplies a preceding general solution and asks only for its particular constant. Each level is an unordered set of equally scoped independent instances.

## Stage 3 — components and complete profiles

In all rows below, `u=x-h`. Each original full equation is the empirical recipe L(y)=R(u); the source primitive and initial abscissa are translated consistently. These are defensible coordinate-substitution recipes, not a claim to have recovered psychological distractor intent or an original authoring algorithm. No polynomial fit or unrelated numerical perturbation is used. Original constants and anomalous-looking powers/signs are retained. The source at h=0 is obtained by the same normal renderer as every other exact rational h. Complete original profile `observed` is opt-in; default profile `authored` uses assessed-method mistakes in `authored_wrong`.


### Profile q-4019

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `446c4857-dd0c-5efd-afb0-2ea4ed0660a0` | ${y}^{3}=\frac{1}{3}{x}^{2}-1$ | `y**3 = u**2/3 - 1` | False |

| `748ec2ec-3297-5615-86ab-bc1f21ac26f1` | ${y}^{3}={x}^{2}+\frac{1}{3}$ | `y**3 = u**2 + 1/3` | False |

| `9c45be7d-d1cc-59a4-8002-8c72c910bd2c` | ${y}^{3}=3{x}^{2}+1$ | `y**3 = 3*u**2 + 1` | True |

| `d5becbca-f53a-5866-bb37-73887a660a89` | ${y}^{3}=\frac{1}{6}{x}^{2}+1$ | `y**3 = u**2/6 + 1` | False |

| `e7e878f5-c14b-5673-a208-7eea879de351` | ${y}^{3}={x}^{2}+1$ | `y**3 = u**2 + 1` | False |

### Profile q-8310

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `531c9876-41a6-5528-8716-512d9860a650` | $y=\frac{2}{\operatorname{ln}⁡x-1}$ | `y = 2/(log(u) - 1)` | False |

| `63de5349-a542-5177-bb56-e3b3bd658803` | $y=\frac{2}{1-2\operatorname{ln}⁡x}$ | `y = 2/(1 - 2*log(u))` | True |

| `86d94f8e-237b-5f46-bbef-54ff8f75c5cc` | $y=\frac{2}{\operatorname{ln}⁡x+1}$ | `y = 2/(log(u) + 1)` | False |

| `89e3ffe6-f402-5afd-82f1-aa385f26d411` | $y=\frac{2}{2\operatorname{ln}⁡x+1}$ | `y = 2/(2*log(u) + 1)` | False |

| `d835efde-95ab-5abd-b768-7494d10b73eb` | $y=\frac{2}{\operatorname{ln}⁡x-2}$ | `y = 2/(log(u) - 2)` | False |

### Profile q-168078

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `b45fa11b-7aeb-5dbf-a888-002c910fdf5e` | $25+3{e}^{-0.03t}$ | `25 + 3*exp(-3*t/100)` | True |

### Profile q-104055

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `2402a50b-0ada-5a95-bd1c-d60ffe3a7054` | $\operatorname{cos}⁡2y=-2x+1$ | `cos(2*y) = 1 - 2*u` | False |

| `3113425a-30f8-5c8b-88b3-34e913ccf225` | $\operatorname{sin}⁡y=-2x$ | `sin(y) = -2*u` | False |

| `79eaa63a-7157-5816-ab3b-72d58acb2790` | $\operatorname{sin}⁡y=x$ | `sin(y) = u` | False |

| `f7406111-8e32-5b08-aa41-0f61204a9031` | $\operatorname{cos}⁡y=x+1$ | `cos(y) = u + 1` | False |

| `fd71d029-d6be-50c5-9b70-7d320b3399c3` | $\operatorname{cos}⁡y=-x$ | `cos(y) = -u` | True |

### Profile q-14310

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `01b271c8-930d-55d2-b6c9-4d10415d1f40` | $y=\operatorname{tan}⁡(x-\frac{\pi }{4})$ | `y = -cot(u + pi/4)` | True |

| `453026c0-09cc-5849-a51c-b0765a6a347c` | $y=\operatorname{cot}⁡(x-\frac{\pi }{4})$ | `y = -tan(u + pi/4)` | False |

| `7f4bfc4f-7d7a-5012-b1f2-ad8906f9fa0d` | $y=\operatorname{tan}⁡(x+\frac{\pi }{4})$ | `y = tan(u + pi/4)` | False |

| `a9c5c442-efee-51ea-b4c4-619423884639` | $y=\operatorname{tan}⁡(x+\frac{\pi }{2})$ | `y = -cot(u)` | False |

| `dcd30bde-3736-5aa2-a5e8-1c3be5c7c83c` | $y=\operatorname{cot}⁡(x+\frac{\pi }{2})$ | `y = -tan(u)` | False |

### Profile q-14312

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `161701b8-cab3-5a52-baee-ca387468d340` | $y={e}^{-1+x}$ | `y = exp(u - 1)` | False |

| `50b36c20-41be-54bd-8252-8418beace6e0` | $y={e}^{-{e}^{-x}}$ | `y = exp(-exp(-u))` | True |

| `6737182b-f42e-57d4-b8d6-67a37fb50f8d` | $y={e}^{{e}^{x}}$ | `y = exp(exp(u))` | False |

| `7771e672-13a1-5981-b9ae-117088631933` | $y={e}^{-1-{e}^{x}}$ | `y = exp(-exp(u) - 1)` | False |

| `db69fd4d-8719-5651-b5ad-029bab24e359` | $y={e}^{-1+{e}^{-x}}$ | `y = exp(-1 + exp(-u))` | False |

### Profile q-14313

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `184695d3-9029-5e71-b2c0-44b31db02e5d` | ${y}^{3}=3{x}^{2}+5$ | `y**3 = 3*u**2 + 5` | False |

| `1bb941ed-69f9-51b5-84ab-9b185febcd77` | ${y}^{3}={x}^{2}+3$ | `y**3 = u**2 + 3` | False |

| `664df1fa-7210-55f4-b6c5-5c6c644b8caa` | ${y}^{3}={x}^{3}+7$ | `y**3 = u**3 + 7` | True |

| `7bb836b0-ad07-50fc-aaa1-78966b0fe6f2` | ${y}^{3}=5{x}^{3}+3$ | `y**3 = 5*u**3 + 3` | False |

| `93347f2d-2098-56c3-8973-3c2341f180fb` | ${y}^{3}=2{x}^{3}+2$ | `y**3 = 2*u**3 + 2` | False |

### Profile q-347853

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `dadf5567-9e34-5988-9b93-ee86c9c672c4` | $\frac{2}{4x+1}$ | `2/(4*u + 1)` | True |

### Profile q-355525

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `a8afe1cc-6a73-59a7-a3aa-86abc400ccd4` | $-\frac{3}{4}\operatorname{cos}(4x)$ | `-3*cos(4*u)/4` | True |

### Profile q-355528

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `a897ef12-2c09-5096-a8b5-ee77680d8d9c` | $({x}^{2}+2)^{2}$ | `(u**2 + 2)**2` | True |

### Profile q-355544

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `96ae4175-e85f-5fa0-9c66-e85a778d8d55` | $\frac{4}{7}\operatorname{tan}(7x)$ | `4*tan(7*u)/7` | True |

### Profile q-355562

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `a2e265e1-c3cb-5fab-b4f5-ccf995516d4e` | ${e}^{{x}^{2}/2}$ | `exp(u**2/2)` | True |

### Profile q-355578

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `ec80c9e4-ade4-588f-871a-59a453ae5b9a` | ${e}^{2-1/x}$ | `exp(2 - 1/u)` | True |

### Profile q-355579

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `1346830d-69d5-5e73-b008-864e705c06e1` | ${e}^{2\sqrt{x}}$ | `exp(2*sqrt(u))` | True |

### Profile q-50220

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `3e4267cc-bd1e-507b-8072-2b2a8c2eca09` | $y=\frac{2}{x}-1$ | `y = -1 + 2/u` | False |

| `8b417cb4-a6eb-5024-a1dc-ec0c00436d6b` | $y=\frac{1}{2x-1}$ | `y = 1/(2*u - 1)` | False |

| `a75d6c04-3e75-57b3-9835-3be982051f16` | $y=\frac{2}{x+1}$ | `y = 2/(u + 1)` | False |

| `bea71f13-c9fb-5f86-9a53-ebbcbb8c38fc` | $y=\frac{1}{x}$ | `y = 1/u` | True |

| `ee34aca2-9235-5324-8e51-2b3c711ec180` | $y=\frac{1}{2-x}$ | `y = 1/(2 - u)` | False |

### Profile q-50566

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `42390f84-76dd-513e-bfe6-30ef499d0b47` | $y=\sqrt{2{x}^{2}-4}$ | `y = sqrt(2*u**2 - 4)` | False |

| `551e91b4-3be3-55eb-845f-b95b7bb7e037` | $-y=\sqrt{x+4}$ | `-y = sqrt(u + 4)` | False |

| `625cb73d-fe58-5029-93a5-e925201b1fec` | $-y=\sqrt{2x+7}$ | `-y = sqrt(2*u + 7)` | False |

| `a48b421b-d946-5b0e-a7fc-5f7cf21d83e0` | $y=\frac{1}{4}\sqrt{2{x}^{2}-2}$ | `y = sqrt(2*u**2 - 2)/4` | False |

| `b2fdf6fa-d413-5479-9d2f-edfcccbd37ff` | $y=\sqrt{{x}^{2}-8}$ | `y = sqrt(u**2 - 8)` | True |

### Profile q-8308

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `30133227-afe7-5481-8b20-5e90c5357811` | $y={e}^{-x}$ | `y = exp(-u)` | False |

| `8dc6e6b6-7795-585f-872f-9399fa1852a0` | $y=1$ | `y = 1` | False |

| `9fbd50f1-5563-5199-adb8-f88d72b3446a` | $y={e}^{\operatorname{sin}⁡x}$ | `y = exp(sin(u))` | False |

| `dfced686-1189-5123-b1b4-8db75ac9b85e` | $y={e}^{x}$ | `y = exp(u)` | True |

| `f802ca15-9874-59ee-8efd-bf70059a7581` | $y=x+1$ | `y = u + 1` | False |

### Profile q-8309

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `2fa50117-feef-5fb7-b4c7-8d5074635199` | $3\operatorname{sin}⁡(2y)=1-\operatorname{cos}⁡(3x)$ | `3*sin(2*y) = 1 - cos(3*u)` | False |

| `452eaa99-839b-51b9-a716-4597a4aef31a` | $5\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x))$ | `5*sin(2*y) = 2 - 2*cos(3*u)` | False |

| `74fe7c6f-36b4-5a32-8184-47101e4f7568` | $\operatorname{sin}⁡(2y)=1-\operatorname{cos}⁡(3x)$ | `sin(2*y) = 1 - cos(3*u)` | False |

| `80940eb3-3340-5a50-8f91-c8c22404f7b2` | $3\operatorname{sin}⁡(2y)=2(1-\operatorname{cos}⁡(3x))$ | `3*sin(2*y) = 2 - 2*cos(3*u)` | True |

| `b1b526ac-6987-52e6-b725-e6fce574b42d` | $\operatorname{sin}⁡(2y)=\operatorname{cos}⁡(3x)$ | `sin(2*y) = cos(3*u)` | False |

### Profile q-14309

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `158f36f0-5c9f-5df4-b307-3df00e1927ac` | $y=\frac{2}{\pi +2-4\operatorname{arctan}⁡(x)}$ | `y = 2/(-4*atan(u) + 2 + pi)` | False |

| `394931cf-7701-52c5-939f-4d7925927a5c` | $y=\frac{4}{\pi +4-4\operatorname{arctan}⁡(x)}$ | `y = 4/(-4*atan(u) + pi + 4)` | True |

| `8a89762a-446c-538c-a5f1-db6c984332b1` | $y=\frac{1}{\pi +1-\operatorname{arctan}⁡(x)}$ | `y = 1/(-atan(u) + 1 + pi)` | False |

| `20d10a3f-7efd-565e-8b3b-25e4aed18fc9` | $y=\frac{1}{\pi -4+4\operatorname{arctan}⁡(x)}$ | `y = 1/(4*atan(u) - 4 + pi)` | False |

| `38fc6ca0-2882-53b5-a94f-8c1db20782e6` | $y=\frac{4}{\pi -1-\operatorname{arctan}⁡(x)}$ | `y = 4/(-atan(u) - 1 + pi)` | False |

### Profile q-50219

| Original answer ID | Exact source field value | Recipe in u | Correct |

|---|---|---|---|

| `4da866c3-3d7f-5b0b-a810-ac33ce6a862f` | ${ln}^{2}⁡y=(1-x)^{2}$ | `log(y)**2 = (1 - u)**2` | False |

| `ff36e7bd-a5e4-5f39-b596-7ff7d49622b4` | ${ln}^{2}⁡y=1-2{x}^{2}$ | `log(y)**2 = 1 - 2*u**2` | False |

| `b064fdd0-a36c-5cee-92e7-9e10247d699e` | ${ln}^{2}⁡y=1-{x}^{2}$ | `log(y)**2 = 1 - u**2` | True |

| `7c31dc57-4c05-53a8-8a8e-94c43bdec15e` | ${ln}^{2}⁡y={x}^{2}+1$ | `log(y)**2 = u**2 + 1` | False |

| `86e781a0-f04d-53d1-ab6b-bd9ecd3bb5ae` | ${ln}^{2}⁡y=2{x}^{2}+1$ | `log(y)**2 = 2*u**2 + 1` | False |

## Stage 4 — reusable rendering and constraints

For the twenty observed templates, retain all prose and aligned rows from the source; replace free x by u=x-h, translate calls y(x0) to y(x0+h), and preserve dx, integration variable labels, and the blank labels y(x), y, sin(3y), tan(4y). Source substitutions such as 13=12+C are the evaluated u-initial-value stages. At h=0 full banks and source-stage words match. For nonzero h the same separated primitives differentiate correctly because du/dx=1. Initial abscissas, domain singularities, and branches move with h; y-initial-values remain exact. Bounds sample integer h from -6 through 6, while explicit inputs support any rational including 1/2. This parameter changes actual initial abscissas, pole locations, and nonautonomous coefficients; it is an authored equal-workload variation, never evidence of a recovered source coefficient sampler. Repeated source families are already varied in their primitive structures, so coordinate variants do not stand in for new skills.

Cooling instead parameterizes ambient temperature A (sample integers 15..35) and initial A+3, preserving decay rate 3/100 and the RHS-only fragment. h must be zero. Its default standalone prompt gives the previously derived general solution, a contextual repair distinct from exact observed replay.

The three authored extensions parameterize a,b and h. Easy exponential y'=ay has y(h)=b; moderate reciprocal y'=-ay² has y(h)=b; hard trig cos(ay)y'=sin(b(x-h)) has y(h)=0 and -pi/(2a)<y<pi/(2a). All have precisely the source separation/integration/constant-finding demand. a,b sample integers 2..5 (hard b can become 6 when avoiding equality); exact positive rational inputs are accepted subject to whole-bank distinctness. These are extensions, not observed labels. They introduce no substitutions beyond the original hard chain-factor primitive. Original initial branch is enforced; hard local solution exists where |a(1-cos(bu))/b|<1.

Authored banks are complete five-option profiles. They use omitted integral multipliers, sign reversal, integration-constant mistakes, wrong integral functions, inversion, or wrong root branch; the script documents every four-expression bank. They are chosen as whole banks before the instance is constructed. The entire instance fails if any equation is equivalent to another. No learner-facing diagnosis is added. Exact source profiles and authored defaults have different question identities whenever banks differ, but the mathematical parameter fingerprint stays fixed.

All mathematics, provenance, recipes, branches, and sampling labels reside outside learner content. UUID identity includes parameter/domain fingerprint and sorted full displayed banks. Choice order or seed does not change content identity. Questions are local JSON review records, never transaction data.


## Authored default operation banks

These named operations are our authoring choices; they are not interpretations assigned to observed numerical banks. The complete four-member lists below share one correct value and are never mixed between profiles. `u=x-h`.

| Profile | Four wrong operations in displayed-bank order |
|---|---|
| q-4019 | omit the factor 3 clearing the y integral; divide by 3 instead; reverse integration constant sign; use initial y³ as the constant without subtracting the initial primitive |
| q-8310 | reverse the reciprocal integral sign; omit the factor 2 on ln u after inversion; use initial y as denominator constant; multiply by the reciprocal denominator instead of dividing |
| q-104055 | lose the minus in integrating sin y; lose minus and use sin(initial y)=1 as constant; use initial y itself as constant; double the x primitive |
| q-14310 | reverse the initial constant sign; use cotangent instead of tangent; use negative initial x as constant and omit arctan(initial y); omit the inverse tangent function |
| q-14312 | reverse the sign of the exponential primitive; report the coefficient function e^-u as y; reverse the exponent input sign in the primitive; use ln(initial y) as constant without subtracting the initial primitive |
| q-14313 | keep quadratic power and insert factor 3 when integrating x²; omit subtraction of the initial x primitive from initial y³; reverse constant sign; omit clearing the factor 1/3 on the y integral |
| q-50220 | reverse x-integral sign and set initial constant accordingly; use initial y as constant rather than subtracting initial x; double x-integral coefficient and fit initial condition; fail to invert reciprocal primitive |
| q-50566 | select negative square-root branch; omit factor 1/2 on x integral and fit initial constant; reverse constant sign; use initial y² as constant without subtracting initial x² |
| q-8308 | reverse primitive sign; keep initial y constant and omit exponential growth; double the integral of the constant coefficient; add the primitive to the initial value instead of exponentiating |
| q-8309 | omit the y chain factor when clearing the integral denominators; omit the x chain denominator; reverse the sign of cosine term; omit subtracting initial x primitive |
| q-14309 | reverse arctangent primitive sign; halve the arctangent coefficient; omit initial arctangent when setting constant; invert the final solution |
| q-50219 | reverse x primitive sign; double x primitive; square initial ln y minus x instead of integrating x; use initial y instead of its log-squared value as constant |

Authored easy rate extension: reverse exponential rate, divide by the rate rather than multiply, add a linear primitive instead of exponentiating, omit the initial amplitude. Authored moderate reciprocal extension: reverse x primitive sign, omit initial amplitude in the x coefficient, use initial y rather than its reciprocal as integration constant, omit inversion. Authored hard frequencies extension: omit y chain numerator, replace it with x frequency, reverse cosine sign, omit subtraction of the initial cosine contribution. Profiles require coefficient inequalities that keep these mistakes visible and distinct; invalid explicit inputs fail without resampling.

Source-widget archive check: `/home/jake/Developer/MA/DATA/Lessons/1179/Source/1179.json` and the owning Markdown were searched for the current q-355528 and other new blank IDs; those IDs are absent from that older archive. The basis-1356 captured widget fields remain authoritative here; no field-format anomaly requires reconstruction. The positive-inner-root condition is an independently derived domain clarification, not a correction of the supplied particular answer.
