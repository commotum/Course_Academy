# Review, basis 1356

Observed originals followed by parameterized replay. Generated examples are labeled separately.


## Original q-11728

Given that $f(x) = 5e^{x} + 2x^{2} - 3$, find $f^{′}(x)$.


Bank:
- $f^{′}(x) = 5e^{x} + 4x^{2} - 3$
- $f^{′}(x) = 5e^{x} + 4x^{2}$
- $f^{′}(x) = 5e^{x} + 4x$
- $f^{′}(x) = 5e^{x} + 4x - 3$
- $f^{′}(x) = e^{x} + 4x$

No supplied worked solution or source correct ref.


### Observed profile replay (notation normalized; supported repair labeled in extraction)

Given that $f(x) = 5{e}^{x} + 2{x}^{2} - 3$, find $f^{′}(x)$.

- $f^{′}(x) = 4 x + {e}^{x}$
- $f^{′}(x) = 4 x + 5 {e}^{x}$
- $f^{′}(x) = 4 x^{2} + 5 {e}^{x} - 3$
- $f^{′}(x) = 4 x^{2} + 5 {e}^{x}$
- $f^{′}(x) = 4 x + 5 {e}^{x} - 3$

Using the addition and the power rules, we get

$$
\begin{aligned}f'(x) & =\frac{\text{d}}{\text{d}x}(5{e}^{x}+2{x}^{2}-3) \\ & =\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(2{x}^{2})-\frac{\text{d}}{\text{d}x}(3) \\ & =5\frac{\text{d}}{\text{d}x}({e}^{x})+2\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(3) \\ & =5{e}^{x}+2(2x)-0 \\ & =5{e}^{x}+4x.\end{aligned}
$$


## Original q-167636

If $k(x)=g(x)-f(x),$ where $A=2$ and $B=3,$ then $\frac{\text{d}k}{\text{d}x}=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .


Bank:
- $3{e}^{x}-3{x}^{2}-2$

We found that $A=2$ and $B=3$ in steps 3 and 4, respectively. Therefore, we have

$$
\begin{aligned}y & =g(x)-f(x) \\  & =3{e}^{x}-({x}^{3}+2x) \\  & =3{e}^{x}-{x}^{3}-2x\end{aligned}
$$

Using the addition and power rules, we get

$$
\begin{aligned}\frac{\text{d}k}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3{e}^{x}-{x}^{3}-2x) \\  & =\frac{\text{d}}{\text{d}x}(3{e}^{x}+\frac{\text{d}}{\text{d}x}(-{x}^{3})+\frac{\text{d}}{\text{d}x}(-2x) \\  & =3\frac{\text{d}}{\text{d}x}({e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-2\frac{\text{d}}{\text{d}x}(x) \\  & =3{e}^{x}-3{x}^{2}-2.\end{aligned}
$$


### Observed profile replay (notation normalized; supported repair labeled in extraction)

If $k(x)=g(x)-f(x),$ where $A=2$ and $B=3,$ then $\frac{\text{d}k}{\text{d}x}=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

- $- 3 x^{2} + 3 {e}^{x} - 2$

We found that $A=2$ and $B=3$ in steps 3 and 4, respectively. Therefore, we have

$$
\begin{aligned}y & =g(x)-f(x) \\  & =3{e}^{x}-({x}^{3}+2x) \\  & =3{e}^{x}-{x}^{3}-2x\end{aligned}
$$

Using the addition and power rules, we get

$$
\begin{aligned}\frac{\text{d}k}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3{e}^{x}-{x}^{3}-2x) \\  & =\frac{\text{d}}{\text{d}x}(3{e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-\frac{\text{d}}{\text{d}x}(2x) \\  & =3\frac{\text{d}}{\text{d}x}({e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-2\frac{\text{d}}{\text{d}x}(x) \\  & =3{e}^{x}-3{x}^{2}-2.\end{aligned}
$$


## Original q-140431

Given that $f(x)=2{e}^{x}+4{x}^{2}-3$, find the slope of the tangent at $x=1.$


Bank:
- $e+4$
- $e+8$
- $2e$
- $2e+8$
- $2e+4$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+4{x}^{2}-3) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(4{x}^{2})+\frac{\text{d}}{\text{d}x}(-3) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})+4\frac{\text{d}}{\text{d}x}({x}^{2})+0 \\  & =2{e}^{x}+8x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=1} & ={(2{e}^{x}+8x)\,|}_{x=1} \\  & =2\cdot {e}^{1}+8\cdot 1 \\  & =2e+8.\end{aligned}
$$


### Observed profile replay (notation normalized; supported repair labeled in extraction)

Given that $f(x)=2{e}^{x}+4{x}^{2}-3$, find the slope of the tangent at $x=1.$

- $4 + 2 e$
- $2 e + 8$
- $e + 4$
- $e + 8$
- $2 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+4{x}^{2}-3) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(4{x}^{2})+\frac{\text{d}}{\text{d}x}(-3) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})+4\frac{\text{d}}{\text{d}x}({x}^{2})+0 \\  & =2{e}^{x}+8x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=1} & ={(2{e}^{x}+8x)\,|}_{x=1} \\  & =2{e}^{1}+8\cdot 1 \\  & =2 e + 8.\end{aligned}
$$


## Original q-140432

Given that $f(x)={x}^{2}+2x+6{e}^{x}$, find the slope of the tangent at $x=0.$


Bank:
- $8e$
- $2+6e$
- $1+6e$
- $6e$
- $8$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({x}^{2}+2x+6{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(2x)+\frac{\text{d}}{\text{d}x}(6{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{2})+2\frac{\text{d}}{\text{d}x}(x)+6\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =2x+2+6{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(2x+2+6{e}^{x})\,|}_{x=0} \\  & =2\cdot 0+2+6\cdot {e}^{0} \\  & =2+6\cdot 1 \\  & =8.\end{aligned}
$$


### Observed profile replay (notation normalized; supported repair labeled in extraction)

Given that $f(x)={x}^{2}+2x+6{e}^{x}$, find the slope of the tangent at $x=0.$

- $6 e$
- $8$
- $8 e$
- $2 + 6 e$
- $1 + 6 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({x}^{2}+2x+6{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(2x)+\frac{\text{d}}{\text{d}x}(6{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{2})+2\frac{\text{d}}{\text{d}x}(x)+6\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =2x+2+6{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(2x+2+6{e}^{x})\,|}_{x=0} \\  & =2\cdot 0+2+6{e}^{0} \\  & =2+6\cdot 1 \\  & =8.\end{aligned}
$$


## Original q-17247

Given that $f(x)=2{e}^{x}-3{x}^{2}$, find the slope of the tangent at $x=0.$


Bank:
- $2e-6$
- $1$
- $-4e$
- $2$
- $0$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}-3{x}^{2}) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})-\frac{\text{d}}{\text{d}x}(3{x}^{2}) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})-3\frac{\text{d}}{\text{d}x}({x}^{2}) \\  & =2{e}^{x}-3(2x) \\  & =2{e}^{x}-6x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(2{e}^{x}-6x)\,|}_{x=0} \\  & =2{e}^{0}-6\cdot 0 \\  & =2\cdot 1-0 \\  & =2.\end{aligned}
$$


### Observed profile replay (notation normalized; supported repair labeled in extraction)

Given that $f(x)=2{e}^{x}-3{x}^{2}$, find the slope of the tangent at $x=0.$

- $0$
- $2$
- $-6 + 2 e$
- $1$
- $- 4 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}-3{x}^{2}) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})-\frac{\text{d}}{\text{d}x}(3{x}^{2}) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})-3\frac{\text{d}}{\text{d}x}({x}^{2}) \\  & =2{e}^{x}-3(2x) \\  & =2{e}^{x}-6x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(2{e}^{x}-6x)\,|}_{x=0} \\  & =2{e}^{0}-6\cdot 0 \\  & =2\cdot 1-0 \\  & =2.\end{aligned}
$$


## Original q-304035

Given that $f(x)=6{x}^{7}+2{e}^{x}$, the exact value of the slope of the tangent line at $x=-1$ is{{field-1}}.


Bank:
- $42+\frac{2}{e}$
- $42x^6+2e^{x}$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(6{x}^{7}+2{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(6{x}^{7})+\frac{\text{d}}{\text{d}x}(2{e}^{x}) \\  & =6\frac{\text{d}}{\text{d}x}({x}^{7})+2\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =6(7{x}^{6})+2{e}^{x} \\  & =42{x}^{6}+2{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=-1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=-1} & ={(42{x}^{6}+2{e}^{x})\,|}_{x=-1} \\  & =42(-1)^{6}+2{e}^{-1} \\  & =42\cdot 1+\frac{2}{e} \\  & =42+\frac{2}{e}.\end{aligned}
$$


### Observed profile replay (notation normalized; supported repair labeled in extraction)

Given that $f(x)=6{x}^{7}+2{e}^{x}$, the exact value of the slope of the tangent line at $x=-1$ is{{field-1}}.

- $\frac{2}{e} + 42$
- $42 x^{6} + 2 {e}^{x}$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(6{x}^{7}+2{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(6{x}^{7})+\frac{\text{d}}{\text{d}x}(2{e}^{x}) \\  & =6\frac{\text{d}}{\text{d}x}({x}^{7})+2\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =6(7{x}^{6})+2{e}^{x} \\  & =42{x}^{6}+2{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=-1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=-1} & ={(42{x}^{6}+2{e}^{x})\,|}_{x=-1} \\  & =42\cdot (-1)^{6}+2{e}^{-1} \\  & =42\cdot 1+\frac{2}{e} \\  & =\frac{2}{e} + 42.\end{aligned}
$$


## Original q-11730

Given that $f(x) = 9e^{x} - 9x^{2} + 11x - 20$, find $f^{′}(x)$.


Bank:
- $f^{′}(x) = e^{x} - 18x + 11$
- $f^{′}(x) = 9e^{x} - 18x^{2} + 11x$
- $f^{′}(x) = 9e^{x} - 18x + 11$
- $f^{′}(x) = 9e^{x} - 18x^{2} + 11$
- $f^{′}(x) = 9e^{x} - 18x^{2} + 11x - 20$

No supplied worked solution or source correct ref.


### Observed profile replay (notation normalized; supported repair labeled in extraction)

Given that $f(x) = 9{e}^{x} - 9{x}^{2} + 11x - 20$, find $f^{′}(x)$.

- $f^{′}(x) = - 18 x^{2} + 11 x + 9 {e}^{x} - 20$
- $f^{′}(x) = - 18 x + 9 {e}^{x} + 11$
- $f^{′}(x) = - 18 x + {e}^{x} + 11$
- $f^{′}(x) = - 18 x^{2} + 11 x + 9 {e}^{x}$
- $f^{′}(x) = - 18 x^{2} + 9 {e}^{x} + 11$

Using the addition and the power rules, we get

$$
\begin{aligned}f'(x) & =\frac{\text{d}}{\text{d}x}(9{e}^{x}-9{x}^{2}+11x-20) \\ & =\frac{\text{d}}{\text{d}x}(9{e}^{x})-\frac{\text{d}}{\text{d}x}(9{x}^{2})+\frac{\text{d}}{\text{d}x}(11x)-\frac{\text{d}}{\text{d}x}(20) \\ & =9\frac{\text{d}}{\text{d}x}({e}^{x})-9\frac{\text{d}}{\text{d}x}({x}^{2})+11\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(20) \\ & =9{e}^{x}-9(2x)+11(1)-0 \\ & =9{e}^{x}-18x+11.\end{aligned}
$$


## Original q-167694

For $x<1,$ ${f}^{′}(x)=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .


Bank:
- ${e}^{x}+2x+1$

For $x<1,$ we use the expression $f(x)={e}^{x}+{x}^{2}+x,$ which is differentiable.

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({e}^{x}+{x}^{2}+x) \\  & =\frac{\text{d}}{\text{d}x}({e}^{x})+\frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(x) \\  & ={e}^{x}+2x+1.\end{aligned}
$$


### Observed profile replay (notation normalized; supported repair labeled in extraction)

For $x<1,$ ${f}^{′}(x)=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

- $2 x + {e}^{x} + 1$

For $x<1,$ we use the expression $f(x)={e}^{x}+{x}^{2}+x,$ which is differentiable.

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({e}^{x}+{x}^{2}+x) \\  & =\frac{\text{d}}{\text{d}x}({e}^{x})+\frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(x) \\  & ={e}^{x}+2x+1.\end{aligned}
$$


## Original q-17255

Given that $f(x)=11{e}^{x}+8{x}^{2}-12x-20$, find the slope of the tangent at $x=0.$


Bank:
- $-1$
- $0$
- $5$
- $-3$
- $1$

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(11{e}^{x}+8{x}^{2}-12x-20) \\  & =\frac{\text{d}}{\text{d}x}(11{e}^{x})+\frac{\text{d}}{\text{d}x}(8{x}^{2})-\frac{\text{d}}{\text{d}x}(12x)-\frac{\text{d}}{\text{d}x}(20) \\  & =11\frac{\text{d}}{\text{d}x}({e}^{x})+8\frac{\text{d}}{\text{d}x}({x}^{2})-12\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(20) \\  & =11{e}^{x}+8(2x)-12(1)-0 \\  & =11{e}^{x}+16x-12.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(11{e}^{x}+16x-12)|}_{x=0} \\  & =11{e}^{0}+16\cdot 0-12 \\  & =11\cdot 1+0-12 \\  & =11-12 \\  & =-1.\end{aligned}
$$


### Observed profile replay (notation normalized; supported repair labeled in extraction)

Given that $f(x)=11{e}^{x}+8{x}^{2}-12x-20$, find the slope of the tangent at $x=0.$

- $1$
- $-1$
- $0$
- $5$
- $-3$

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(11{e}^{x}+8{x}^{2}-12x-20) \\  & =\frac{\text{d}}{\text{d}x}(11{e}^{x})+\frac{\text{d}}{\text{d}x}(8{x}^{2})-\frac{\text{d}}{\text{d}x}(12x)-\frac{\text{d}}{\text{d}x}(20) \\  & =11\frac{\text{d}}{\text{d}x}({e}^{x})+8\frac{\text{d}}{\text{d}x}({x}^{2})-12\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(20) \\  & =11{e}^{x}+8(2x)-12(1)-0 \\  & =11{e}^{x}+16x-12.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(11{e}^{x}+16x-12)\,|}_{x=0} \\  & =11{e}^{0}+16\cdot 0-12 \\  & =11\cdot 1+0-12 \\  & =11-12 \\  & =-1.\end{aligned}
$$


## Generated easy / direct_quadratic / authored_method

Given that $f(x) = 2{e}^{x} + 6{x}^{2} + 7$, find $f^{′}(x)$.

- $f^{′}(x) = 12 x + 2 {e}^{x}$
- $f^{′}(x) = 6 x^{2} + 2 {e}^{x} + 7$
- $f^{′}(x) = 12 x$
- $f^{′}(x) = - 12 x + 2 {e}^{x}$
- $f^{′}(x) = 12 x^{2} + 2 {e}^{x}$

Using the addition and the power rules, we get

$$
\begin{aligned}f'(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}+7) \\ & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})+\frac{\text{d}}{\text{d}x}(7) \\ & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(7) \\ & =2{e}^{x}+6(2x)+0 \\ & =2{e}^{x}+12x.\end{aligned}
$$


## Generated easy / direct_quadratic / authored_method

Given that $g(x) = -5{e}^{x} + 3{x}^{2} - 16$, find $g^{′}(x)$.

- $g^{′}(x) = 3 x^{2} - 5 {e}^{x} - 16$
- $g^{′}(x) = 6 x^{2} - 5 {e}^{x}$
- $g^{′}(x) = 6 x$
- $g^{′}(x) = - 6 x - 5 {e}^{x}$
- $g^{′}(x) = 6 x - 5 {e}^{x}$

Using the addition and the power rules, we get

$$
\begin{aligned}g'(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}-16) \\ & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})-\frac{\text{d}}{\text{d}x}(16) \\ & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(16) \\ & =-5{e}^{x}+3(2x)-0 \\ & =-5{e}^{x}+6x.\end{aligned}
$$


## Generated easy / direct_quadratic / observed_direct_quadratic

Given that $f(x) = 2{e}^{x} + 6{x}^{2} + 7$, find $f^{′}(x)$.

- $f^{′}(x) = 12 x + 2 {e}^{x}$
- $f^{′}(x) = 12 x + {e}^{x}$
- $f^{′}(x) = 12 x^{2} + 2 {e}^{x} + 7$
- $f^{′}(x) = 12 x + 2 {e}^{x} + 7$
- $f^{′}(x) = 12 x^{2} + 2 {e}^{x}$

Using the addition and the power rules, we get

$$
\begin{aligned}f'(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}+7) \\ & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})+\frac{\text{d}}{\text{d}x}(7) \\ & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(7) \\ & =2{e}^{x}+6(2x)+0 \\ & =2{e}^{x}+12x.\end{aligned}
$$


## Generated easy / direct_quadratic / observed_direct_quadratic

Given that $f(x) = -5{e}^{x} + 3{x}^{2} - 16$, find $f^{′}(x)$.

- $f^{′}(x) = 6 x + {e}^{x}$
- $f^{′}(x) = 6 x^{2} - 5 {e}^{x}$
- $f^{′}(x) = 6 x^{2} - 5 {e}^{x} - 16$
- $f^{′}(x) = 6 x - 5 {e}^{x} - 16$
- $f^{′}(x) = 6 x - 5 {e}^{x}$

Using the addition and the power rules, we get

$$
\begin{aligned}f'(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}-16) \\ & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})-\frac{\text{d}}{\text{d}x}(16) \\ & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(16) \\ & =-5{e}^{x}+3(2x)-0 \\ & =-5{e}^{x}+6x.\end{aligned}
$$


## Generated easy / difference / fragment

Let $f(x)={x}^{3}+7x$ and $g(x)=7{e}^{x}$. If $k(x)=g(x)-f(x)$, then $\frac{\text{d}k}{\text{d}x}=$ {{field-1}}.

- $- 3 x^{2} + 7 {e}^{x} - 7$

Using the given definitions, we have

$$
\begin{aligned}k(x) & =g(x)-f(x) \\  & =7{e}^{x}-({x}^{3}+7x) \\  & =7{e}^{x}-{x}^{3}-7x\end{aligned}
$$

Using the addition and power rules, we get

$$
\begin{aligned}\frac{\text{d}k}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(7{e}^{x}-{x}^{3}-7x) \\  & =\frac{\text{d}}{\text{d}x}(7{e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-\frac{\text{d}}{\text{d}x}(7x) \\  & =7\frac{\text{d}}{\text{d}x}({e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-7\frac{\text{d}}{\text{d}x}(x) \\  & =7{e}^{x}-3{x}^{2}-7.\end{aligned}
$$


## Generated easy / difference / fragment

Let $f(x)={x}^{3}+3x$ and $g(x)=2{e}^{x}$. If $k(x)=g(x)-f(x)$, then $\frac{\text{d}k}{\text{d}x}=$ {{field-1}}.

- $- 3 x^{2} + 2 {e}^{x} - 3$

Using the given definitions, we have

$$
\begin{aligned}k(x) & =g(x)-f(x) \\  & =2{e}^{x}-({x}^{3}+3x) \\  & =2{e}^{x}-{x}^{3}-3x\end{aligned}
$$

Using the addition and power rules, we get

$$
\begin{aligned}\frac{\text{d}k}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2{e}^{x}-{x}^{3}-3x) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-\frac{\text{d}}{\text{d}x}(3x) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-3\frac{\text{d}}{\text{d}x}(x) \\  & =2{e}^{x}-3{x}^{2}-3.\end{aligned}
$$


## Generated easy / difference / observed_difference

If $k(x)=g(x)-f(x),$ where $A=7$ and $B=7,$ then $\frac{\text{d}k}{\text{d}x}=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

- $- 3 x^{2} + 7 {e}^{x} - 7$

We found that $A=7$ and $B=7$ in steps 3 and 4, respectively. Therefore, we have

$$
\begin{aligned}y & =g(x)-f(x) \\  & =7{e}^{x}-({x}^{3}+7x) \\  & =7{e}^{x}-{x}^{3}-7x\end{aligned}
$$

Using the addition and power rules, we get

$$
\begin{aligned}\frac{\text{d}k}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(7{e}^{x}-{x}^{3}-7x) \\  & =\frac{\text{d}}{\text{d}x}(7{e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-\frac{\text{d}}{\text{d}x}(7x) \\  & =7\frac{\text{d}}{\text{d}x}({e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-7\frac{\text{d}}{\text{d}x}(x) \\  & =7{e}^{x}-3{x}^{2}-7.\end{aligned}
$$


## Generated easy / difference / observed_difference

If $k(x)=g(x)-f(x),$ where $A=3$ and $B=2,$ then $\frac{\text{d}k}{\text{d}x}=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

- $- 3 x^{2} + 2 {e}^{x} - 3$

We found that $A=3$ and $B=2$ in steps 3 and 4, respectively. Therefore, we have

$$
\begin{aligned}y & =g(x)-f(x) \\  & =2{e}^{x}-({x}^{3}+3x) \\  & =2{e}^{x}-{x}^{3}-3x\end{aligned}
$$

Using the addition and power rules, we get

$$
\begin{aligned}\frac{\text{d}k}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2{e}^{x}-{x}^{3}-3x) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-\frac{\text{d}}{\text{d}x}(3x) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})-\frac{\text{d}}{\text{d}x}({x}^{3})-3\frac{\text{d}}{\text{d}x}(x) \\  & =2{e}^{x}-3{x}^{2}-3.\end{aligned}
$$


## Generated easy / slope_quad / authored_method

Given that $f(x)=2{e}^{x}+6{x}^{2}+7$, find the slope of the tangent at $x=1.$

- $2 e + 12$
- $e + 12$
- $12$
- $2 e + 13$
- $2$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}+7) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})+\frac{\text{d}}{\text{d}x}(7) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2})+0 \\  & =2{e}^{x}+12x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=1} & ={(2{e}^{x}+12x)\,|}_{x=1} \\  & =2{e}^{1}+12\cdot 1 \\  & =2 e + 12.\end{aligned}
$$


## Generated easy / slope_quad / authored_method

Given that $g(x)=-5{e}^{x}+3{x}^{2}-16$, find the slope of the tangent at $x=1.$

- $e + 6$
- $-5$
- $6$
- $- 5 e - 13$
- $6 - 5 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}-16) \\  & =\frac{\text{d}}{\text{d}x}(-5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(-16) \\  & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2})+0 \\  & =-5{e}^{x}+6x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}{\frac{\text{d}g}{\text{d}x}|}_{x=1} & ={(-5{e}^{x}+6x)\,|}_{x=1} \\  & =-5{e}^{1}+6\cdot 1 \\  & =6 - 5 e.\end{aligned}
$$


## Generated easy / slope_quad / observed_slope_quad

Given that $f(x)=2{e}^{x}+6{x}^{2}+7$, find the slope of the tangent at $x=1.$

- $2 e + 12$
- $2 e + 6$
- $e + 6$
- $2 e$
- $e + 12$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}+7) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})+\frac{\text{d}}{\text{d}x}(7) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2})+0 \\  & =2{e}^{x}+12x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=1} & ={(2{e}^{x}+12x)\,|}_{x=1} \\  & =2{e}^{1}+12\cdot 1 \\  & =2 e + 12.\end{aligned}
$$


## Generated easy / slope_quad / observed_slope_quad

Given that $f(x)=-5{e}^{x}+3{x}^{2}-16$, find the slope of the tangent at $x=1.$

- $3 - 5 e$
- $e + 6$
- $e + 3$
- $- 5 e$
- $6 - 5 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}-16) \\  & =\frac{\text{d}}{\text{d}x}(-5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(-16) \\  & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2})+0 \\  & =-5{e}^{x}+6x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=1} & ={(-5{e}^{x}+6x)\,|}_{x=1} \\  & =-5{e}^{1}+6\cdot 1 \\  & =6 - 5 e.\end{aligned}
$$


## Generated easy / slope_polyfirst / authored_method

Given that $f(x)=6{x}^{2}-x+2{e}^{x}$, find the slope of the tangent at $x=0.$

- $1$
- $0$
- $-1$
- $2$
- $2 e + 11$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(6{x}^{2}-x+2{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(6{x}^{2})-\frac{\text{d}}{\text{d}x}(x)+\frac{\text{d}}{\text{d}x}(2{e}^{x}) \\  & =6\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(x)+2\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =12x-1+2{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(12x-1+2{e}^{x})\,|}_{x=0} \\  & =12\cdot 0-1+2{e}^{0} \\  & =-1+2\cdot 1 \\  & =1.\end{aligned}
$$


## Generated easy / slope_polyfirst / authored_method

Given that $f(x)=3{x}^{2}+7x-5{e}^{x}$, find the slope of the tangent at $x=0.$

- $-5$
- $8$
- $7$
- $2$
- $13 - 5 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3{x}^{2}+7x-5{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(7x)-\frac{\text{d}}{\text{d}x}(5{e}^{x}) \\  & =3\frac{\text{d}}{\text{d}x}({x}^{2})+7\frac{\text{d}}{\text{d}x}(x)-5\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =6x+7-5{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(6x+7-5{e}^{x})\,|}_{x=0} \\  & =6\cdot 0+7-5{e}^{0} \\  & =7-5\cdot 1 \\  & =2.\end{aligned}
$$


## Generated easy / slope_polyfirst / observed_slope_polyfirst

Given that $f(x)=6{x}^{2}-x+2{e}^{x}$, find the slope of the tangent at $x=0.$

- $1$
- $2 e$
- $e$
- $2 e + 6$
- $-1 + 2 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(6{x}^{2}-x+2{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(6{x}^{2})-\frac{\text{d}}{\text{d}x}(x)+\frac{\text{d}}{\text{d}x}(2{e}^{x}) \\  & =6\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(x)+2\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =12x-1+2{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(12x-1+2{e}^{x})\,|}_{x=0} \\  & =12\cdot 0-1+2{e}^{0} \\  & =-1+2\cdot 1 \\  & =1.\end{aligned}
$$


## Generated easy / slope_polyfirst / observed_slope_polyfirst

Given that $f(x)=3{x}^{2}+7x-5{e}^{x}$, find the slope of the tangent at $x=0.$

- $3 - 5 e$
- $- 5 e$
- $2 e$
- $2$
- $7 - 5 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3{x}^{2}+7x-5{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(7x)-\frac{\text{d}}{\text{d}x}(5{e}^{x}) \\  & =3\frac{\text{d}}{\text{d}x}({x}^{2})+7\frac{\text{d}}{\text{d}x}(x)-5\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =6x+7-5{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(6x+7-5{e}^{x})\,|}_{x=0} \\  & =6\cdot 0+7-5{e}^{0} \\  & =7-5\cdot 1 \\  & =2.\end{aligned}
$$


## Generated easy / slope_zero / authored_method

Given that $g(x)=2{e}^{x}+6{x}^{2}$, find the slope of the tangent at $x=0.$

- $1$
- $0$
- $2 e + 6$
- $2 e + 12$
- $2$

First, using the addition and the power rules, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2}) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2}) \\  & =2{e}^{x}+6(2x) \\  & =2{e}^{x}+12x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}g}{\text{d}x}|}_{x=0} & ={(2{e}^{x}+12x)\,|}_{x=0} \\  & =2{e}^{0}+12\cdot 0 \\  & =2\cdot 1-0 \\  & =2.\end{aligned}
$$


## Generated easy / slope_zero / authored_method

Given that $f(x)=-5{e}^{x}+3{x}^{2}$, find the slope of the tangent at $x=0.$

- $3 - 5 e$
- $1$
- $0$
- $-5$
- $6 - 5 e$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}) \\  & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2}) \\  & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2}) \\  & =-5{e}^{x}+3(2x) \\  & =-5{e}^{x}+6x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(-5{e}^{x}+6x)\,|}_{x=0} \\  & =-5{e}^{0}+6\cdot 0 \\  & =-5\cdot 1-0 \\  & =-5.\end{aligned}
$$


## Generated easy / slope_zero / observed_slope_zero

Given that $f(x)=2{e}^{x}+6{x}^{2}$, find the slope of the tangent at $x=0.$

- $0$
- $2 e + 12$
- $14 e$
- $1$
- $2$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2}) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2}) \\  & =2{e}^{x}+6(2x) \\  & =2{e}^{x}+12x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(2{e}^{x}+12x)\,|}_{x=0} \\  & =2{e}^{0}+12\cdot 0 \\  & =2\cdot 1-0 \\  & =2.\end{aligned}
$$


## Generated easy / slope_zero / observed_slope_zero

Given that $f(x)=-5{e}^{x}+3{x}^{2}$, find the slope of the tangent at $x=0.$

- $e$
- $0$
- $6 - 5 e$
- $-5$
- $1$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}) \\  & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2}) \\  & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2}) \\  & =-5{e}^{x}+3(2x) \\  & =-5{e}^{x}+6x.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(-5{e}^{x}+6x)\,|}_{x=0} \\  & =-5{e}^{0}+6\cdot 0 \\  & =-5\cdot 1-0 \\  & =-5.\end{aligned}
$$


## Generated easy / slope_seventh / fragment

Given that $h(x)={x}^{5}+5{e}^{x}$, the exact value of the slope of the tangent line at $x=-1$ is{{field-1}}.

- $\frac{5}{e} + 5$

First, using the addition and the power rules, we get

$$
\begin{aligned}{h}^{′}(x) & =\frac{\text{d}}{\text{d}x}({x}^{5}+5{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{5})+\frac{\text{d}}{\text{d}x}(5{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{5})+5\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =(5{x}^{4})+5{e}^{x} \\  & =5{x}^{4}+5{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=-1$ is

$$
\begin{aligned}{\frac{\text{d}h}{\text{d}x}|}_{x=-1} & ={(5{x}^{4}+5{e}^{x})\,|}_{x=-1} \\  & =5\cdot (-1)^{4}+5{e}^{-1} \\  & =5\cdot 1+\frac{5}{e} \\  & =\frac{5}{e} + 5.\end{aligned}
$$


## Generated easy / slope_seventh / fragment

Given that $g(x)=3{x}^{3}+2{e}^{x}$, the exact value of the slope of the tangent line at $x=-1$ is{{field-1}}.

- $\frac{2}{e} + 9$

First, using the addition and the power rules, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3{x}^{3}+2{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(3{x}^{3})+\frac{\text{d}}{\text{d}x}(2{e}^{x}) \\  & =3\frac{\text{d}}{\text{d}x}({x}^{3})+2\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =3(3{x}^{2})+2{e}^{x} \\  & =9{x}^{2}+2{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=-1$ is

$$
\begin{aligned}{\frac{\text{d}g}{\text{d}x}|}_{x=-1} & ={(9{x}^{2}+2{e}^{x})\,|}_{x=-1} \\  & =9\cdot (-1)^{2}+2{e}^{-1} \\  & =9\cdot 1+\frac{2}{e} \\  & =\frac{2}{e} + 9.\end{aligned}
$$


## Generated easy / slope_seventh / observed_slope_seventh

Given that $f(x)={x}^{5}+5{e}^{x}$, the exact value of the slope of the tangent line at $x=-1$ is{{field-1}}.

- $\frac{5}{e} + 5$
- $5 x^{4} + 5 {e}^{x}$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({x}^{5}+5{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{5})+\frac{\text{d}}{\text{d}x}(5{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{5})+5\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =(5{x}^{4})+5{e}^{x} \\  & =5{x}^{4}+5{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=-1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=-1} & ={(5{x}^{4}+5{e}^{x})\,|}_{x=-1} \\  & =5\cdot (-1)^{4}+5{e}^{-1} \\  & =5\cdot 1+\frac{5}{e} \\  & =\frac{5}{e} + 5.\end{aligned}
$$


## Generated easy / slope_seventh / observed_slope_seventh

Given that $f(x)=3{x}^{3}+2{e}^{x}$, the exact value of the slope of the tangent line at $x=-1$ is{{field-1}}.

- $\frac{2}{e} + 9$
- $9 x^{2} + 2 {e}^{x}$

First, using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3{x}^{3}+2{e}^{x}) \\  & =\frac{\text{d}}{\text{d}x}(3{x}^{3})+\frac{\text{d}}{\text{d}x}(2{e}^{x}) \\  & =3\frac{\text{d}}{\text{d}x}({x}^{3})+2\frac{\text{d}}{\text{d}x}({e}^{x}) \\  & =3(3{x}^{2})+2{e}^{x} \\  & =9{x}^{2}+2{e}^{x}.\end{aligned}
$$

Therefore, the slope of the tangent at $x=-1$ is

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=-1} & ={(9{x}^{2}+2{e}^{x})\,|}_{x=-1} \\  & =9\cdot (-1)^{2}+2{e}^{-1} \\  & =9\cdot 1+\frac{2}{e} \\  & =\frac{2}{e} + 9.\end{aligned}
$$


## Generated moderate / direct_extended / authored_method

Given that $g(x) = 2{e}^{x} + 6{x}^{2} - x - 18$, find $g^{′}(x)$.

- $g^{′}(x) = 12 x + 2 {e}^{x} - 1$
- $g^{′}(x) = 12 x^{2} - x + 2 {e}^{x}$
- $g^{′}(x) = 12 x - 1$
- $g^{′}(x) = - 12 x + 2 {e}^{x} + 1$
- $g^{′}(x) = 6 x^{2} - x + 2 {e}^{x} - 18$

Using the addition and the power rules, we get

$$
\begin{aligned}g'(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}-x-18) \\ & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})-\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(18) \\ & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(18) \\ & =2{e}^{x}+6(2x)-(1)-0 \\ & =2{e}^{x}+12x-1.\end{aligned}
$$


## Generated moderate / direct_extended / authored_method

Given that $g(x) = -5{e}^{x} + 3{x}^{2} + 7x - 16$, find $g^{′}(x)$.

- $g^{′}(x) = 3 x^{2} + 7 x - 5 {e}^{x} - 16$
- $g^{′}(x) = 6 x^{2} + 7 x - 5 {e}^{x}$
- $g^{′}(x) = 6 x + 7$
- $g^{′}(x) = - 6 x - 5 {e}^{x} - 7$
- $g^{′}(x) = 6 x - 5 {e}^{x} + 7$

Using the addition and the power rules, we get

$$
\begin{aligned}g'(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}+7x-16) \\ & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(7x)-\frac{\text{d}}{\text{d}x}(16) \\ & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2})+7\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(16) \\ & =-5{e}^{x}+3(2x)+7(1)-0 \\ & =-5{e}^{x}+6x+7.\end{aligned}
$$


## Generated moderate / direct_extended / observed_direct_extended

Given that $f(x) = 2{e}^{x} + 6{x}^{2} - x - 18$, find $f^{′}(x)$.

- $f^{′}(x) = 12 x + 2 {e}^{x} - 1$
- $f^{′}(x) = 12 x^{2} - x + 2 {e}^{x}$
- $f^{′}(x) = 12 x + {e}^{x} - 1$
- $f^{′}(x) = 12 x^{2} + 2 {e}^{x} - 1$
- $f^{′}(x) = 12 x^{2} - x + 2 {e}^{x} - 18$

Using the addition and the power rules, we get

$$
\begin{aligned}f'(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}-x-18) \\ & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})-\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(18) \\ & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(18) \\ & =2{e}^{x}+6(2x)-(1)-0 \\ & =2{e}^{x}+12x-1.\end{aligned}
$$


## Generated moderate / direct_extended / observed_direct_extended

Given that $f(x) = -5{e}^{x} + 3{x}^{2} + 7x - 16$, find $f^{′}(x)$.

- $f^{′}(x) = 6 x^{2} + 7 x - 5 {e}^{x} - 16$
- $f^{′}(x) = 6 x^{2} + 7 x - 5 {e}^{x}$
- $f^{′}(x) = 6 x + {e}^{x} + 7$
- $f^{′}(x) = 6 x^{2} - 5 {e}^{x} + 7$
- $f^{′}(x) = 6 x - 5 {e}^{x} + 7$

Using the addition and the power rules, we get

$$
\begin{aligned}f'(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}+7x-16) \\ & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(7x)-\frac{\text{d}}{\text{d}x}(16) \\ & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2})+7\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(16) \\ & =-5{e}^{x}+3(2x)+7(1)-0 \\ & =-5{e}^{x}+6x+7.\end{aligned}
$$


## Generated moderate / branch / fragment

For $x<-3$, let $g(x)=2{e}^{x}+6{x}^{2}-x$. Then $g'(x)=$ {{field-1}}.

- $12 x + 2 {e}^{x} - 1$

For $x<-3,$ we use the expression $g(x)=2{e}^{x}+6{x}^{2}-x,$ which is differentiable.

Using the addition and the power rules, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}-x) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})-\frac{\text{d}}{\text{d}x}(x) \\  & =2{e}^{x}+12x-1.\end{aligned}
$$


## Generated moderate / branch / fragment

For $x<3$, let $f(x)=-5{e}^{x}+3{x}^{2}+7x$. Then $f'(x)=$ {{field-1}}.

- $6 x - 5 {e}^{x} + 7$

For $x<3,$ we use the expression $f(x)=-5{e}^{x}+3{x}^{2}+7x,$ which is differentiable.

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}+7x) \\  & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(7x) \\  & =-5{e}^{x}+6x+7.\end{aligned}
$$


## Generated moderate / branch / observed_branch

For $x<-3,$ ${f}^{′}(x)=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

- $12 x + 2 {e}^{x} - 1$

For $x<-3,$ we use the expression $f(x)=2{e}^{x}+6{x}^{2}-x,$ which is differentiable.

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}-x) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})-\frac{\text{d}}{\text{d}x}(x) \\  & =2{e}^{x}+12x-1.\end{aligned}
$$


## Generated moderate / branch / observed_branch

For $x<3,$ ${f}^{′}(x)=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

- $6 x - 5 {e}^{x} + 7$

For $x<3,$ we use the expression $f(x)=-5{e}^{x}+3{x}^{2}+7x,$ which is differentiable.

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}+7x) \\  & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(7x) \\  & =-5{e}^{x}+6x+7.\end{aligned}
$$


## Generated moderate / slope_extended / authored_method

Given that $g(x)=2{e}^{x}+6{x}^{2}-x-18$, find the slope of the tangent at $x=0.$

- $1$
- $2 e + 11$
- $-1$
- $-16$
- $0$

Using the addition and the power rules, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}-x-18) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})-\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(18) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(18) \\  & =2{e}^{x}+6(2x)-(1)-0 \\  & =2{e}^{x}+12x-1.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}g}{\text{d}x}|}_{x=0} & ={(2{e}^{x}+12x-1)\,|}_{x=0} \\  & =2{e}^{0}+12\cdot 0-1 \\  & =2\cdot 1+0-1 \\  & =2-1 \\  & =1.\end{aligned}
$$


## Generated moderate / slope_extended / authored_method

Given that $g(x)=-5{e}^{x}+3{x}^{2}+7x-16$, find the slope of the tangent at $x=0.$

- $8$
- $13 - 5 e$
- $7$
- $-21$
- $2$

Using the addition and the power rules, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}+7x-16) \\  & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(7x)-\frac{\text{d}}{\text{d}x}(16) \\  & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2})+7\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(16) \\  & =-5{e}^{x}+3(2x)+7(1)-0 \\  & =-5{e}^{x}+6x+7.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}g}{\text{d}x}|}_{x=0} & ={(-5{e}^{x}+6x+7)\,|}_{x=0} \\  & =-5{e}^{0}+6\cdot 0+7 \\  & =-5\cdot 1+0+7 \\  & =-5+7 \\  & =2.\end{aligned}
$$


## Generated moderate / slope_extended / observed_slope_extended

Given that $f(x)=2{e}^{x}+6{x}^{2}-x-18$, find the slope of the tangent at $x=0.$

- $1$
- $\frac{3}{2}$
- $0$
- $- \frac{1}{4}$
- $-1$

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{2}-x-18) \\  & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{2})-\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(18) \\  & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{2})-\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(18) \\  & =2{e}^{x}+6(2x)-(1)-0 \\  & =2{e}^{x}+12x-1.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(2{e}^{x}+12x-1)\,|}_{x=0} \\  & =2{e}^{0}+12\cdot 0-1 \\  & =2\cdot 1+0-1 \\  & =2-1 \\  & =1.\end{aligned}
$$


## Generated moderate / slope_extended / observed_slope_extended

Given that $f(x)=-5{e}^{x}+3{x}^{2}+7x-16$, find the slope of the tangent at $x=0.$

- $-2$
- $- \frac{3}{2}$
- $0$
- $\frac{7}{4}$
- $2$

Using the addition and the power rules, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{2}+7x-16) \\  & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{2})+\frac{\text{d}}{\text{d}x}(7x)-\frac{\text{d}}{\text{d}x}(16) \\  & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{2})+7\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(16) \\  & =-5{e}^{x}+3(2x)+7(1)-0 \\  & =-5{e}^{x}+6x+7.\end{aligned}
$$

Therefore, the slope of the tangent at $x=0$ is 

$$
\begin{aligned}{\frac{\text{d}f}{\text{d}x}|}_{x=0} & ={(-5{e}^{x}+6x+7)\,|}_{x=0} \\  & =-5{e}^{0}+6\cdot 0+7 \\  & =-5\cdot 1+0+7 \\  & =-5+7 \\  & =2.\end{aligned}
$$


## Generated hard / two_powers / fragment

Given that $h(x)=2{e}^{x}+6{x}^{4}-{x}^{3}$, find $h'(x)=$ {{field-1}}.

- $24 x^{3} - 3 x^{2} + 2 {e}^{x}$

Using the addition and the power rules, we get

$$
\begin{aligned}h'(x) & =\frac{\text{d}}{\text{d}x}(2{e}^{x}+6{x}^{4}-{x}^{3}) \\ & =\frac{\text{d}}{\text{d}x}(2{e}^{x})+\frac{\text{d}}{\text{d}x}(6{x}^{4})-\frac{\text{d}}{\text{d}x}({x}^{3}) \\ & =2\frac{\text{d}}{\text{d}x}({e}^{x})+6\frac{\text{d}}{\text{d}x}({x}^{4})-\frac{\text{d}}{\text{d}x}({x}^{3}) \\ & =2{e}^{x}+6(4{x}^{3})-(3{x}^{2}) \\ & =2{e}^{x}+24{x}^{3}-3{x}^{2}.\end{aligned}
$$


## Generated hard / two_powers / fragment

Given that $f(x)=-5{e}^{x}+3{x}^{4}+7{x}^{3}$, find $f'(x)=$ {{field-1}}.

- $12 x^{3} + 21 x^{2} - 5 {e}^{x}$

Using the addition and the power rules, we get

$$
\begin{aligned}f'(x) & =\frac{\text{d}}{\text{d}x}(-5{e}^{x}+3{x}^{4}+7{x}^{3}) \\ & =-\frac{\text{d}}{\text{d}x}(5{e}^{x})+\frac{\text{d}}{\text{d}x}(3{x}^{4})+\frac{\text{d}}{\text{d}x}(7{x}^{3}) \\ & =-5\frac{\text{d}}{\text{d}x}({e}^{x})+3\frac{\text{d}}{\text{d}x}({x}^{4})+7\frac{\text{d}}{\text{d}x}({x}^{3}) \\ & =-5{e}^{x}+3(4{x}^{3})+7(3{x}^{2}) \\ & =-5{e}^{x}+12{x}^{3}+21{x}^{2}.\end{aligned}
$$
