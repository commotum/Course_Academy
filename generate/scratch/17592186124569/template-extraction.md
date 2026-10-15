# Template and complete-bank extraction

The generator supports 12 separate template/profile pairs, with one blank and eleven five-choice radio banks. Every source option, given derivative, primitive, and residual is explicitly mapped below. Choice-bank interpretation is deliberately literal: recipe j is k times the complete original potential expression B_j, followed by +C for radio equations. It is an exact structural expression recipe, not an inferred psychological error. For constants in distractors, k scales that explicit constant as well. The whole selected profile is used; recipes are never pooled across sources.

The sole variable is a common nonzero integer scale k in {-4,-3,-2,-1,1,2,3,4}. This is a conservative same-method generalization, not an observed independent coefficient domain. It scales the supplied vector field, x primitive, y residual, final potential, and complete choice bank together. The integration/differentiation operators, degrees, trig/exponential arguments, function arity, variable roles, and response layout remain fixed because altering them would change the observed method or workload. Negative scales introduce signs only, within the easy algebra used by the source. k=1 replays the complete original bank; all eight values are exhaustively validated. Different seeds and choice orders never expand this finite domain.

Each new solution preserves the shared source explanatory sentences and six ordered mathematical stages: gradient definition, the two derivative equations, x integration with g(y), y differentiation, residual matching/integration of g, and final substitution. Notation and aligned equations are normalized. Source replay fidelity is mathematical and field/bank fidelity, not byte-identical Markdown; the validation report distinguishes this from correctness and grading.

q-168602 is generated as a standalone question by supplying its explicitly recorded vector field. Its field key stays field-1, and the answer fragment excludes f(x,y)= and +C. Other supported sources retain key selection and five complete equations. q-81737 has y≠0; a potential is defined on either connected half-plane, with an independent arbitrary constant on each. Generated prompts explicitly state this domain. All other domains are R².

## q-35994 / 17592186124943

Original prompt:

Find $f(x,y)$ such that $∇f=F,$ where $F(x,y)=-y\,i+(3-x)\,j.$

Given P=`-y`, Q=`3-x`; x primitive A=`-x*y`; remaining H(y)=`3*y`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-35994-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)=-xy-y+C$ | `k*(-x*y-y)` then +C | False |
| 2 | $f(x,y)=3-xy+C$ | `k*(3-x*y)` then +C | False |
| 3 | $f(x,y)=-xy+2x+C$ | `k*(-x*y+2*x)` then +C | False |
| 4 | $f(x,y)=-xy+3y+C$ | `k*(-x*y+3*y)` then +C | True |
| 5 | $f(x,y)=\frac{y{x}^{2}}{2}+C$ | `k*(y*x**2/2)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=-y,\,\frac{∂f}{∂y}=3-x
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int (-y)\,\text{d}x \\  & =-xy+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=-x+{g}^{′}(y).
$$

Taking  $\frac{∂f}{∂y}=3-x$ into account, we obtain

$$
\begin{aligned}-x+{g}^{′}(y) & =3-x \\ {g}^{′}(y) & =3 \\ g(y) & =3y+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=3y+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)=-xy+3y+C.
$$

## q-168602 / 17592186235530

Original prompt:

Find $f(x,y)$ such that $∇f=F.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $f(x,y)=$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $+\,C,$
where $C$ is a constant-

Given P=`y**3-1`, Q=`3*x*y**2+1`; x primitive A=`x*y**3-x`; remaining H(y)=`y`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-168602-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $x{y}^{3}-x+y$ | `k*(x*y**3-x+y)` (fragment) | True |

Original worked solution, retained as fidelity evidence:

In part 1, we found that $a=1.$ So, 

$$
F(x,y)=({y}^{3}-1)\,i+(3x{y}^{2}+1)\,j.
$$

The gradient of the function $f(x,y)$ is defined as

$$
\begin{aligned}∇f(x,y) & =\frac{∂f}{∂x}\text{ }i+\frac{∂f}{∂y}\text{ }j.\end{aligned}
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}={y}^{3}-1,\,\frac{∂f}{∂y}=3x{y}^{2}+1
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int ({y}^{3}-1)\,\text{d}x \\  & =x{y}^{3}-x+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=3x{y}^{2}+{g}^{′}(y).
$$

Taking $\frac{∂f}{∂y}=3x{y}^{2}+1$ into account, we obtain

$$
\begin{aligned}3x{y}^{2}+{g}^{′}(y) & =3x{y}^{2}+1 \\ {g}^{′}(y) & =1 \\ g(y) & =y+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=y+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)=x{y}^{3}-x+y+C.
$$

## q-132077 / 17592186266129

Original prompt:

Find $f(x,y)$ such that $∇f=F,$ where $F(x,y)=(\operatorname{cos}⁡(x+y)+y)\,i+(\operatorname{cos}⁡(x+y)+x)\,j.$

Given P=`cos(x+y)+y`, Q=`cos(x+y)+x`; x primitive A=`sin(x+y)+x*y`; remaining H(y)=`0`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-132077-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)=\operatorname{sin}⁡(x+y)+\frac{1}{2}{x}^{2}y+C$ | `k*(sin(x+y)+x**2*y/2)` then +C | False |
| 2 | $f(x,y)=\operatorname{sin}⁡(x+y)+xy+C$ | `k*(sin(x+y)+x*y)` then +C | True |
| 3 | $f(x,y)=\operatorname{sin}⁡(x+y)+{y}^{2}+C$ | `k*(sin(x+y)+y**2)` then +C | False |
| 4 | $f(x,y)=\operatorname{sin}⁡(x+y)+x+y+C$ | `k*(sin(x+y)+x+y)` then +C | False |
| 5 | $f(x,y)=\operatorname{sin}⁡(x+y)+\frac{1}{2}{x}^{2}+\frac{1}{2}{y}^{2}+C$ | `k*(sin(x+y)+x**2/2+y**2/2)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=\operatorname{cos}⁡(x+y)+y,\,\frac{∂f}{∂y}=\operatorname{cos}⁡(x+y)+x
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int (\operatorname{cos}⁡(x+y)+y)\,\text{d}x \\  & =\operatorname{sin}⁡(x+y)+xy+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=\operatorname{cos}⁡(x+y)+x+{g}^{′}(y).
$$

Taking  $\frac{∂f}{∂y}=\operatorname{cos}⁡(x+y)+x$ into account, we obtain

$$
\begin{aligned}\operatorname{cos}⁡(x+y)+x+{g}^{′}(y) & =\operatorname{cos}⁡(x+y)+x \\ {g}^{′}(y) & =0 \\ g(y) & =C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=C$ into our expression for $f(x,y),$ we get

$$
f(x,y)=\operatorname{sin}⁡(x+y)+xy+C.
$$

## q-132079 / 17592186266130

Original prompt:

Find $f(x,y)$ such that $∇f=F,$ where $F(x,y)=({e}^{y}-y\operatorname{sin}⁡x)\,i+(x{e}^{y}+\operatorname{cos}⁡x)\,j.$

Given P=`exp(y)-y*sin(x)`, Q=`x*exp(y)+cos(x)`; x primitive A=`x*exp(y)+y*cos(x)`; remaining H(y)=`0`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-132079-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)={x}^{2}{e}^{y}+y\operatorname{cos}⁡x+C$ | `k*(x**2*exp(y)+y*cos(x))` then +C | False |
| 2 | $f(x,y)=x{e}^{y}+y\operatorname{sin}⁡x+C$ | `k*(x*exp(y)+y*sin(x))` then +C | False |
| 3 | $f(x,y)=y{e}^{y}+x\operatorname{cos}⁡x+C$ | `k*(y*exp(y)+x*cos(x))` then +C | False |
| 4 | $f(x,y)={y}^{2}{e}^{y}+x\operatorname{cos}⁡x+C$ | `k*(y**2*exp(y)+x*cos(x))` then +C | False |
| 5 | $f(x,y)=x{e}^{y}+y\operatorname{cos}⁡x+C$ | `k*(x*exp(y)+y*cos(x))` then +C | True |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}={e}^{y}-y\operatorname{sin}⁡x,\,\frac{∂f}{∂y}=x{e}^{y}+\operatorname{cos}⁡x
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int ({e}^{y}-y\operatorname{sin}⁡x)\,\text{d}x \\  & =x{e}^{y}+y\operatorname{cos}⁡x+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=x{e}^{y}+\operatorname{cos}⁡x+{g}^{′}(y).
$$

Taking  $\frac{∂f}{∂y}=x{e}^{y}+\operatorname{cos}⁡x$ into account, we obtain

$$
\begin{aligned}x{e}^{y}+\operatorname{cos}⁡x+{g}^{′}(y) & =x{e}^{y}+\operatorname{cos}⁡x \\ {g}^{′}(y) & =0 \\ g(y) & =C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=C$ into our expression for $f(x,y),$ we get

$$
f(x,y)=x{e}^{y}+y\operatorname{cos}⁡x+C.
$$

## q-132080 / 17592186266131

Original prompt:

Find $f(x,y)$ such that $∇f=F,$ where $F(x,y)={e}^{y}\,i+(x{e}^{y}+2y)\,j.$

Given P=`exp(y)`, Q=`x*exp(y)+2*y`; x primitive A=`x*exp(y)`; remaining H(y)=`y**2`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-132080-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)=2y{e}^{y}+{x}^{2}+C$ | `k*(2*y*exp(y)+x**2)` then +C | False |
| 2 | $f(x,y)=x{e}^{y}+{y}^{2}+C$ | `k*(x*exp(y)+y**2)` then +C | True |
| 3 | $f(x,y)=x{e}^{y}+y+C$ | `k*(x*exp(y)+y)` then +C | False |
| 4 | $f(x,y)=y{e}^{y}+x{y}^{2}+C$ | `k*(y*exp(y)+x*y**2)` then +C | False |
| 5 | $f(x,y)={x}^{2}{e}^{y}+y+C$ | `k*(x**2*exp(y)+y)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}={e}^{y},\,\frac{∂f}{∂y}=x{e}^{y}+2y
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int {e}^{y}\,\text{d}x \\  & =x{e}^{y}+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=x{e}^{y}+{g}^{′}(y).
$$

Taking  $\frac{∂f}{∂y}=x{e}^{y}+2y$ into account, we obtain

$$
\begin{aligned}x{e}^{y}+{g}^{′}(y) & =x{e}^{y}+2y \\ {g}^{′}(y) & =2y \\ g(y) & ={y}^{2}+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)={y}^{2}+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)=x{e}^{y}+{y}^{2}+C.
$$

## q-81734 / 17592186351356

Original prompt:

Find $f(x,y)$ such that $∇f=F,$ where $F(x,y)=(2x{y}^{2}+1)\,i+(2{x}^{2}y+1)\,j.$

Given P=`2*x*y**2+1`, Q=`2*x**2*y+1`; x primitive A=`x**2*y**2+x`; remaining H(y)=`y`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-81734-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)=2{x}^{2}{y}^{2}+C$ | `k*(2*x**2*y**2)` then +C | False |
| 2 | $f(x,y)={x}^{2}{y}^{2}+y+C$ | `k*(x**2*y**2+y)` then +C | False |
| 3 | $f(x,y)=2{x}^{2}{y}^{2}+x+C$ | `k*(2*x**2*y**2+x)` then +C | False |
| 4 | $f(x,y)={x}^{2}{y}^{2}+x+y+C$ | `k*(x**2*y**2+x+y)` then +C | True |
| 5 | $f(x,y)=4xy+xy+C$ | `k*(4*x*y+x*y)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=2x{y}^{2}+1,\,\frac{∂f}{∂y}=2{x}^{2}y+1
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int (2x{y}^{2}+1)\,\text{d}x \\  & ={x}^{2}{y}^{2}+x+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=2{x}^{2}y+{g}^{′}(y).
$$

Taking $\frac{∂f}{∂y}=2{x}^{2}y+1$ into account, we obtain

$$
\begin{aligned}2{x}^{2}y+{g}^{′}(y) & =2{x}^{2}y+1 \\ {g}^{′}(y) & =1 \\ g(y) & =y+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=y+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)={x}^{2}{y}^{2}+x+y+C.
$$

## q-81737 / 17592186351357

Original prompt:

Find $f(x,y)$ such that $∇f(x,y)=F(x,y),$ where $F(x,y)=(12{x}^{3}-\frac{1}{y})\,i+(\frac{x-1}{{y}^{2}})\,j.$

Given P=`12*x**3-1/y`, Q=`(x-1)/y**2`; x primitive A=`3*x**4-x/y`; remaining H(y)=`1/y`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-81737-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)=12{x}^{3}-\frac{1}{y}+C$ | `k*(12*x**3-1/y)` then +C | False |
| 2 | $f(x,y)=3{x}^{4}-\frac{1}{y}+C$ | `k*(3*x**4-1/y)` then +C | False |
| 3 | $f(x,y)=12{x}^{4}+\frac{{x}^{2}}{y}-\frac{x}{y}+C$ | `k*(12*x**4+x**2/y-x/y)` then +C | False |
| 4 | $f(x,y)=3{x}^{4}-\frac{x}{y}+\frac{1}{y}+C$ | `k*(3*x**4-x/y+1/y)` then +C | True |
| 5 | $f(x,y)=12{x}^{3}y-\frac{x}{y}+C$ | `k*(12*x**3*y-x/y)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=12{x}^{3}-\frac{1}{y},\,\frac{∂f}{∂y}=\frac{x-1}{{y}^{2}}
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int (12{x}^{3}-\frac{1}{y})\,\text{d}x \\  & =3{x}^{4}-\frac{x}{y}+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=\frac{x}{{y}^{2}}+{g}^{′}(y).
$$

Taking $\frac{∂f}{∂y}=\frac{x-1}{{y}^{2}}$ into account, we obtain

$$
\begin{aligned}\frac{x}{{y}^{2}}+{g}^{′}(y) & =\frac{x-1}{{y}^{2}} \\ \frac{x}{{y}^{2}}+{g}^{′}(y) & =\frac{x}{{y}^{2}}-\frac{1}{{y}^{2}} \\ {g}^{′}(y) & =-\frac{1}{{y}^{2}} \\ g(y) & =\frac{1}{y}+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=\frac{1}{y}+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)=3{x}^{4}-\frac{x}{y}+\frac{1}{y}+C.
$$

## q-81748 / 17592186351362

Original prompt:

Find $f(x,y)$ such that $∇f=F,$ where $F(x,y)=\operatorname{cos}⁡x\operatorname{sin}⁡y\,i+(\operatorname{sin}⁡x\operatorname{cos}⁡y+\operatorname{sin}⁡y)\,j.$

Given P=`cos(x)*sin(y)`, Q=`sin(x)*cos(y)+sin(y)`; x primitive A=`sin(x)*sin(y)`; remaining H(y)=`-cos(y)`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-81748-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)=\operatorname{sin}⁡x\operatorname{cos}⁡y+\operatorname{sin}⁡y+C$ | `k*(sin(x)*cos(y)+sin(y))` then +C | False |
| 2 | $f(x,y)={sin}^{2}⁡(x)+\operatorname{cos}⁡y+C$ | `k*(sin(x)**2+cos(y))` then +C | False |
| 3 | $f(x,y)=\operatorname{sin}⁡x\operatorname{sin}⁡y-\operatorname{cos}⁡y+C$ | `k*(sin(x)*sin(y)-cos(y))` then +C | True |
| 4 | $f(x,y)=\operatorname{sin}⁡(xy)+\operatorname{sin}⁡y+C$ | `k*(sin(x*y)+sin(y))` then +C | False |
| 5 | $f(x,y)=\operatorname{cos}⁡x\operatorname{cos}⁡y-\operatorname{cos}⁡y+C$ | `k*(cos(x)*cos(y)-cos(y))` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=\operatorname{cos}⁡x\operatorname{sin}⁡y,\,\frac{∂f}{∂y}=\operatorname{sin}⁡x\operatorname{cos}⁡y+\operatorname{sin}⁡y
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int \operatorname{cos}⁡x\operatorname{sin}⁡y\,\text{d}x \\  & =\operatorname{sin}⁡x\operatorname{sin}⁡y+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=\operatorname{sin}⁡x\operatorname{cos}⁡y+{g}^{′}(y).
$$

Taking  $\frac{∂f}{∂y}=\operatorname{sin}⁡x\operatorname{cos}⁡y+\operatorname{sin}⁡y$ into account, we obtain

$$
\begin{aligned}\operatorname{sin}⁡x\operatorname{cos}⁡y+{g}^{′}(y) & =\operatorname{sin}⁡x\operatorname{cos}⁡y+\operatorname{sin}⁡y \\ {g}^{′}(y) & =\operatorname{sin}⁡y \\ g(y) & =-\operatorname{cos}⁡y+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=-\operatorname{cos}⁡y+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)=\operatorname{sin}⁡x\operatorname{sin}⁡y-\operatorname{cos}⁡y+C.
$$

## q-81749 / 17592186351363

Original prompt:

Find $f(x,y)$ such that $∇f(x,y)=F(x,y),$ where $F(x,y)=y{e}^{xy}\text{ }i+(x{e}^{xy}+2y)\text{ }j.$

Given P=`y*exp(x*y)`, Q=`x*exp(x*y)+2*y`; x primitive A=`exp(x*y)`; remaining H(y)=`y**2`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-81749-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)=y{e}^{xy}+{x}^{2}+C$ | `k*(y*exp(x*y)+x**2)` then +C | False |
| 2 | $f(x,y)=xy{e}^{xy}+y+C$ | `k*(x*y*exp(x*y)+y)` then +C | False |
| 3 | $f(x,y)=x{e}^{xy}+2+C$ | `k*(x*exp(x*y)+2)` then +C | False |
| 4 | $f(x,y)={e}^{xy}+{y}^{2}+C$ | `k*(exp(x*y)+y**2)` then +C | True |
| 5 | $f(x,y)={e}^{xy}+xy+C$ | `k*(exp(x*y)+x*y)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=y{e}^{xy},\,\frac{∂f}{∂y}=x{e}^{xy}+2y
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int y{e}^{xy}\,\text{d}x \\  & ={e}^{xy}+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=x{e}^{xy}+{g}^{′}(y).
$$

Taking $\frac{∂f}{∂y}=x{e}^{xy}+2y$ into account, we obtain

$$
\begin{aligned}x{e}^{xy}+{g}^{′}(y) & =x{e}^{xy}+2y \\ {g}^{′}(y) & =2y \\ g(y) & ={y}^{2}+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)={y}^{2}+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)={e}^{xy}+{y}^{2}+C.
$$

## q-132084 / 17592186406697

Original prompt:

Find $f(x,y)$ such that $∇f=F,$ where $F(x,y)=2x\operatorname{sin}⁡y\,i+({x}^{2}\operatorname{cos}⁡y+3{y}^{2})\,j.$

Given P=`2*x*sin(y)`, Q=`x**2*cos(y)+3*y**2`; x primitive A=`x**2*sin(y)`; remaining H(y)=`y**3`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-132084-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)={x}^{2}\operatorname{sin}⁡y+{y}^{3}+C$ | `k*(x**2*sin(y)+y**3)` then +C | True |
| 2 | $f(x,y)={x}^{2}\operatorname{cos}⁡y+3y+C$ | `k*(x**2*cos(y)+3*y)` then +C | False |
| 3 | $f(x,y)={x}^{2}\operatorname{cos}⁡y+2y+C$ | `k*(x**2*cos(y)+2*y)` then +C | False |
| 4 | $f(x,y)=x\operatorname{sin}⁡y+{y}^{3}+C$ | `k*(x*sin(y)+y**3)` then +C | False |
| 5 | $f(x,y)=x\operatorname{sin}⁡y+{y}^{2}+C$ | `k*(x*sin(y)+y**2)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=2x\operatorname{sin}⁡y,\,\frac{∂f}{∂y}={x}^{2}\operatorname{cos}⁡y+3{y}^{2}
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int 2x\operatorname{sin}⁡y\,\text{d}x \\  & ={x}^{2}\operatorname{sin}⁡y+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}={x}^{2}\operatorname{cos}⁡y+{g}^{′}(y).
$$

Taking  $\frac{∂f}{∂y}={x}^{2}\operatorname{cos}⁡y+3{y}^{2}$ into account, we obtain

$$
\begin{aligned}{x}^{2}\operatorname{cos}⁡y+{g}^{′}(y) & ={x}^{2}\operatorname{cos}⁡y+3{y}^{2} \\ {g}^{′}(y) & =3{y}^{2} \\ g(y) & ={y}^{3}+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)={y}^{3}+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)={x}^{2}\operatorname{sin}⁡y+{y}^{3}+C.
$$

## q-81736 / 17592186406699

Original prompt:

Find $f(x,y)$ such that $∇f(x,y)=F(x,y),$ where $F(x,y)=(\operatorname{sin}⁡y+y)\text{ }i+(x\operatorname{cos}⁡y+x)\text{ }j.$

Given P=`sin(y)+y`, Q=`x*cos(y)+x`; x primitive A=`x*sin(y)+x*y`; remaining H(y)=`0`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-81736-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)=x\operatorname{sin}⁡y+xy+C$ | `k*(x*sin(y)+x*y)` then +C | True |
| 2 | $f(x,y)=\operatorname{cos}⁡(xy)+xy+C$ | `k*(cos(x*y)+x*y)` then +C | False |
| 3 | $f(x,y)={x}^{2}\operatorname{sin}⁡y+{x}^{2}y+C$ | `k*(x**2*sin(y)+x**2*y)` then +C | False |
| 4 | $f(x,y)=x\operatorname{cos}⁡y+x+C$ | `k*(x*cos(y)+x)` then +C | False |
| 5 | $f(x,y)=\operatorname{sin}⁡(xy)+y+C$ | `k*(sin(x*y)+y)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=\operatorname{sin}⁡y+y,\,\frac{∂f}{∂y}=x\operatorname{cos}⁡y+x
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int (\operatorname{sin}⁡y+y)\,\text{d}x \\  & =x\operatorname{sin}⁡y+xy+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=x\operatorname{cos}⁡y+x+{g}^{′}(y).
$$

Taking $\frac{∂f}{∂y}=x\operatorname{cos}⁡y+x$ into account, we obtain

$$
\begin{aligned}x\operatorname{cos}⁡y+x+{g}^{′}(y) & =x\operatorname{cos}⁡y+x \\ {g}^{′}(y) & =0 \\ g(y) & =C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=C$ into our expression for $f(x,y),$ we get

$$
f(x,y)=x\operatorname{sin}⁡y+xy+C.
$$

## q-81738 / 17592186421424

Original prompt:

Find $f(x,y)$ such that $∇f(x,y)=F(x,y),$ where $F(x,y)=(3{x}^{2}-{y}^{2})\text{ }i+(4-2xy)\text{ }j.$

Given P=`3*x**2-y**2`, Q=`4-2*x*y`; x primitive A=`x**3-x*y**2`; remaining H(y)=`4*y`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `q-81738-complete-bank`.

| Option | Original exact answer | Recipe at k | Correct |
|---|---|---|---|
| 1 | $f(x,y)={x}^{3}-x{y}^{2}+4y+C$ | `k*(x**3-x*y**2+4*y)` then +C | True |
| 2 | $f(x,y)={x}^{3}-{y}^{3}+4y-x{y}^{2}+C$ | `k*(x**3-y**3+4*y-x*y**2)` then +C | False |
| 3 | $f(x,y)=3{x}^{3}+4y-x{y}^{2}+C$ | `k*(3*x**3+4*y-x*y**2)` then +C | False |
| 4 | $f(x,y)=3{x}^{2}y-{y}^{3}+4y-x{y}^{2}+C$ | `k*(3*x**2*y-y**3+4*y-x*y**2)` then +C | False |
| 5 | $f(x,y)=3{x}^{2}y-{y}^{3}+4y+C$ | `k*(3*x**2*y-y**3+4*y)` then +C | False |

Original worked solution, retained as fidelity evidence:

The gradient of the function $f(x,y)$ is defined as

$$
∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.
$$

Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:

$$
\frac{∂f}{∂x}=3{x}^{2}-{y}^{2},\,\frac{∂f}{∂y}=4-2xy
$$

First, we integrate $\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$

$$
\begin{aligned}f(x,y) & =\int \frac{∂f}{∂x}\,\text{d}x \\  & =\int (3{x}^{2}-{y}^{2})\,\text{d}x \\  & ={x}^{3}-x{y}^{2}+g(y)\end{aligned}
$$

Now, differentiating the above expression with respect to $y,$ we obtain

$$
\frac{∂f}{∂y}=-2xy+{g}^{′}(y).
$$

Taking $\frac{∂f}{∂y}=4-2xy$ into account, we obtain

$$
\begin{aligned}-2xy+{g}^{′}(y) & =4-2xy \\ {g}^{′}(y) & =4 \\ g(y) & =4y+C,\end{aligned}
$$

where $C$ is a constant.

Finally, substituting $g(y)=4y+C$ into our expression for $f(x,y),$ we get

$$
f(x,y)={x}^{3}-x{y}^{2}+4y+C.
$$

## Explicit exclusions and capability limits

q-37346 has no source level, key, or solution. Its bank is retained in source evidence but is not supported in this generator. q-37343 has a keyed equation x²y+y³+C and a competing equation x²y+y³ with the same gradient. No duplicate answer family is admitted. These are exclusions, not successful bank replays.

Moderate and hard are unsupported in this version: no rated source, separate response contract, or greater-workload template supports assigning those bands. Larger scales do not justify relabeling easy tasks. Each has nominal shortage five, filled=false, and classification reopens on new rated evidence or a separately reviewed template. The bounded generator has 96 distinct vector-field tasks before existing-content, presentation-history and reservation exclusions. That finite policy is not a claim of mathematical impossibility beyond the package.
