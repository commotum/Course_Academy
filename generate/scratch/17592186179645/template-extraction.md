# Template extraction — Finding an Integral Expression for Flux

Captured math basis 2694, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All thirteen practice records are in source.json; the canonical example is supporting evidence only.

## Backbone and slots

Easy: supply a polynomial Cartesian vector field and a centered circle, provide its outward unit normal, and request only the missing integrand in the flux integral. The ordered solution states the flux definition, substitutes F and n, takes the dot product, combines like terms where the source does, and identifies the expression. No integration is required.

Moderate: supply a polynomial field and a diagram of a square or rectangle, request the integrand across the selected side, infer its outward axis unit normal, substitute, and take the dot product. Pure powers, mixed monomials and nested squared binomials retain their structures. The selected sides cover right/top/left/bottom and retain their specific sign and component roles.

One scalar k multiplies both supplied field components, every solution intermediate, the final integrand, and every complete source-bank expression. Observed parameters are k=1. Proposed bounded same-method generalization is k in {-8,…,-1,2,…,8}; coefficients remain exact integers. Both signs change the supplied mathematics; seed and option order do not establish variation. The normal, radius, diagram, selected side, exponents, operators, field keys, response type, number of choices and solution stages stay fixed for each profile.

This is a deliberately narrow whole-field generalization. Target sides are not claimed to be inherently fixed mathematical objects. Their outward sign and selected field component define different projection recipes and their existing source assets. The sampler does not claim arbitrary side/geometry slots, change those roles or infer new complete banks. Four normal directions are already represented by source profiles. Circle-radius changes would require coordinated new geometry and normal hints, so this version reuses original geometry and varies the field.

Choices are not pooled. Each of the eleven source profiles carries its entire original bank, with every expression multiplied by k. source-choice-mapping.json records each source field, choice identity, full expression, exact scalar recipe and replay outcome. Incorrect-option cognitive mechanisms remain unresolved. Polynomial equivalence checks full values; no source option is omitted or replaced.

The blanks q-167889 and q-168603 are excluded from standalone generation and inventory. The former lacks the prior part defining E and n; the latter omits F. Their unchanged source evidence is retained, and their mathematical answer shape is one expression in field-1. No distractors are invented.

## Per-source components

### q-126833

Source entity 17592186180034; :question.difficulty/easy; :answer-field.type/radio; key selection.

Consider the vector field $F(x,y)={x}^{2}\,i-{y}^{2}\,j$ and the circle $C$ given by ${x}^{2}+{y}^{2}=1.$ If the flux of $F$ across $C$ is given by

$$
{∮}_{C}\boxed{}\,\text{d}s,
$$

what is the missing expression?

*Hint: The outward-pointing unit normal vector to $C$ is $n=x\,i+y\,j.$*

Supplied P=x**2, Q=-y**2; circle radius 1. Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-126833.

Source answer bank: ${x}^{3}+{y}^{3}$, $x-y$, ${x}^{3}{y}^{3}$, ${x}^{2}-{y}^{2}$, ${x}^{3}-{y}^{3}$ (correct)

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

![](images/38/386f010932b5846e7f47a605a94a5b5d580bd35dbe37512b1583d15d29f3dc70.png)

In our case, we have

$$
\begin{aligned}{∮}_{C}F\cdot n\,\text{d}s & ={∮}_{C}({x}^{2}\,i-{y}^{2}\,j)\cdot (xi+y\,j)\,\text{d}s \\  & ={∮}_{C}{x}^{3}-{y}^{3}\,\text{d}s.\end{aligned}
$$

Therefore, the missing expression is ${x}^{3}-{y}^{3}.$

### q-126850

Source entity 17592186180035; :question.difficulty/moderate; :answer-field.type/radio; key selection.

![](images/b3/b37c10064003374c146c58bba99ff55304529ee66c9fb38c44246ccc90e8f402.png)

Consider the vector field $F(x,y)={x}^{2}\,i+{y}^{2}\,j$ and the square $C$ with side length $4$ centered at $O,$ shown above. If the flux of $F$ across the side ${C}_{1}$ is given by

$$
{\int }_{{C}_{1}}\boxed{}\,\text{d}s,
$$

what is the missing expression?

Supplied P=x**2, Q=y**2; outward normal (1, 0). Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-126850.

Source answer bank: ${x}^{2}+{y}^{2}$, ${x}^{2}-{y}^{2}$, ${x}^{2}$ (correct), ${y}^{2}$, ${x}^{2}{y}^{2}$

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

In our case, we need to find an expression for the flux across only the part ${C}_{1}$ of the closed curve $C.$ Since this side is perpendicular to the $x$-axis and we require an outward-pointing unit normal vector, we must have $n=i.$

![](images/c4/c4c4f2f3d5b6188ac5a6ec41bb96fc0c7132cc39308cebfa16ee759eabac2c75.png)

Therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot n\,\text{d}s & ={\int }_{{C}_{1}}({x}^{2}\,i+{y}^{2}\,j)\cdot i\,\text{d}s \\  & ={\int }_{{C}_{1}}{x}^{2}\,\text{d}s\end{aligned}
$$

Therefore, the missing expression is ${x}^{2}.$

### q-168603

Source entity 17592186235531; :question.difficulty/moderate; :answer-field.type/blank; key field-1.

![](images/64/642a546fc498dfb0f01c0729959f9f68b8dc2d142d966673f204eda910f19211.png)     
                                
                            

   

                            Consider the square $C$ with side length $8$ centered at $O,$ shown above. The flux of $F$ across the side ${C}_{1}$ is given by

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        ${\int }_{{C}_{1}}^{}$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$\text{d}s.$

Excluded: Prompt and inspected diagram supply the square but omit the vector field F.

Source answer bank: ${y}^{3}-1$ (correct)

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

In our case, we need to find an expression for the flux across only the part ${C}_{1}$ of the closed curve $C.$ Since this side is perpendicular to the $x$-axis and we require an outward-pointing unit normal vector, we must have $n=i.$

![](images/19/1939a274191b89f69e51a929654489ed9038df0313f6e47b15e0ff55ad813066.png)

Therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot n\,\text{d}s & ={\int }_{{C}_{1}}(({y}^{3}-1)\,i+(3x{y}^{2}+1)\,j)\cdot i\,\text{d}s \\  & ={\int }_{{C}_{1}}{y}^{3}-1\,\text{d}s.\end{aligned}
$$

### q-127049

Source entity 17592186262697; :question.difficulty/easy; :answer-field.type/radio; key selection.

Consider the vector field $F(x,y)=2{x}^{2}\,i+2{y}^{2}\,j$ and the circle $C$ given by ${x}^{2}+{y}^{2}=4.$ If the flux of $F$ across $C$ is given by

$$
{∮}_{C}\boxed{}\,\text{d}s,
$$

what is the missing expression?

*Hint: The outward-pointing unit normal vector to $C$ is $n=\frac{x}{2}\,i+\frac{y}{2}\,j.$*

Supplied P=2*x**2, Q=2*y**2; circle radius 2. Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127049.

Source answer bank: ${x}^{2}-{y}^{2}$, ${x}^{2}+2{y}^{2}$, $x+y$, ${x}^{3}+{y}^{3}$ (correct), ${x}^{4}{y}^{4}$

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

![](images/ff/ff84680c55f5349431cf3d70066eeaba2c680569faa3b2210e5d14ef63ccd99e.png)

In our case, we have

$$
\begin{aligned}{∮}_{C}F\cdot n\,\text{d}s & ={∮}_{C}(2{x}^{2}\,i+2{y}^{2}\,j)\cdot (\frac{x}{2}i+\frac{y}{2}\,j)\text{d}s \\  & ={∮}_{C}{x}^{3}+{y}^{3}\,\text{d}s.\end{aligned}
$$

Therefore, the missing expression is ${x}^{3}+{y}^{3}.$

### q-127050

Source entity 17592186262698; :question.difficulty/moderate; :answer-field.type/radio; key selection.

![](images/4f/4f8af75aece2346ffbf7a09e1ee90b6e0270f5661dd74e068abb2b2a848e5b97.png)

Consider the vector field $F(x,y)={x}^{3}\,i+3{y}^{2}\,j$ and the square $C$ with side length $4$ centered at $O,$ shown above. If the flux of $F$ across the side ${C}_{2}$ is given by

$$
{\int }_{{C}_{2}}\boxed{}\,\text{d}s,
$$

what is the missing expression?

Supplied P=x**3, Q=3*y**2; outward normal (0, 1). Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127050.

Source answer bank: ${x}^{3}$, ${y}^{3}$, $2x{y}^{2}$, ${x}^{3}{y}^{2}$, $3{y}^{2}$ (correct)

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

In our case, we need to find an expression for the flux across only the part ${C}_{2}$ of the closed curve $C.$ Since this side is perpendicular to the $y$-axis and we require an outward-pointing unit normal vector, we must have $n=j.$ 

![](images/a8/a83c3476bbe2ed2872ed8938dda59c5d0e6d58d05ecaf662748e7a184a4994a4.png)

Therefore,

$$
\begin{aligned}{\int }_{{C}_{2}}F\cdot n\,\text{d}s & ={\int }_{{C}_{2}}({x}^{3}\,i+3{y}^{2}\,j)\cdot j\,\text{d}s \\  & ={\int }_{{C}_{2}}3{y}^{2}\,\text{d}s\end{aligned}
$$

Therefore, the missing expression is $3{y}^{2}.$

### q-127053

Source entity 17592186262699; :question.difficulty/moderate; :answer-field.type/radio; key selection.

![](images/4d/4d9663a0a40f3c3860cce0712e9e9aab41d55251ea15fca33ec663515af57d10.png)

Consider the vector field $F(x,y)={x}^{3}y\,i-x{y}^{2}\,j$ and the rectangle $C,$ shown above. If the flux of $F$ across the side ${C}_{3}$ is given by

$$
{\int }_{{C}_{3}}\boxed{}\,\text{d}s,
$$

what is the missing expression?

Supplied P=x**3*y, Q=-x*y**2; outward normal (-1, 0). Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127053.

Source answer bank: $-{x}^{3}{y}^{2}$, ${x}^{3}y$, $x{y}^{2}$, $-{x}^{3}y$ (correct), $-x{y}^{2}$

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

In our case, we need to find an expression for the flux across only the part ${C}_{3}$ of the closed curve $C.$ Since this side is perpendicular to the $x$-axis and we require an outward-pointing unit normal vector, we must have $n=-i.$

![](images/c6/c6dd493e02633854184be1be0f38246e1e9dce2949f9cc1aa93b943c91d1e44c.png)

Therefore,

$$
\begin{aligned}{\int }_{{C}_{3}}F\cdot n\,\text{d}s & ={\int }_{{C}_{3}}({x}^{3}y\,i-x{y}^{2}\,j)\cdot (-i)\,\text{d}s \\  & ={\int }_{{C}_{3}}-{x}^{3}y\,\text{d}s\end{aligned}
$$

Therefore, the missing expression is $-{x}^{3}y.$

### q-127056

Source entity 17592186262700; :question.difficulty/easy; :answer-field.type/radio; key selection.

Consider the vector field $F(x,y)=15xy\,i+5{x}^{2}\,j$ and the circle $C$ given by ${x}^{2}+{y}^{2}=25.$ If the flux of $F$ across $C$ is given by

$$
{∮}_{C}\boxed{}\,\text{d}s,
$$

what is the missing expression?

*Hint: The outward-pointing unit normal vector to $C$ is $n=\frac{x}{5}\,i+\frac{y}{5}\,j.$*

Supplied P=15*x*y, Q=5*x**2; circle radius 5. Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127056.

Source answer bank: $2xy+{x}^{2}y$, $4{x}^{2}y$ (correct), $3x{y}^{2}+x$, $xy+3x{y}^{2}$, $3x{y}^{2}$

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

![](images/d3/d3d68329d81150c4a975bae4963d4e480cefaef0f2a0a29a0648c3793e9fb462.png)

In our case, we have

$$
\begin{aligned}{∮}_{C}F\cdot n\,\text{d}s & ={∮}_{C}(15xy\,i+5{x}^{2}\,j)\cdot (\frac{x}{5}\,i+\frac{y}{5}\,j)\text{d}s \\  & ={∮}_{C}3{x}^{2}y+{x}^{2}y\,\text{d}s \\  & ={∮}_{C}4{x}^{2}y\,\text{d}s.\end{aligned}
$$

Therefore, the missing expression is $4{x}^{2}y.$

### q-127057

Source entity 17592186262701; :question.difficulty/easy; :answer-field.type/radio; key selection.

Consider the vector field $F(x,y)=4{x}^{2}{y}^{2}\,i+2{x}^{3}y\,j$ and the circle $C$ given by ${x}^{2}+{y}^{2}=4.$ If the flux of $F$ across $C$ is given by  

$$
{∮}_{C}\boxed{}\,\text{d}s,
$$

what is the missing expression?

*Hint: The outward-pointing unit normal vector to $C$ is $n=\frac{x}{2}\,i+\frac{y}{2}\,j.$*

Supplied P=4*x**2*y**2, Q=2*x**3*y; circle radius 2. Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127057.

Source answer bank: $2{x}^{2}y+{y}^{3}x$, $3{x}^{3}{y}^{2}$ (correct), $6x{y}^{2}$, $3x+{y}^{3}$, $x{y}^{3}$

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

![](images/ff/ff84680c55f5349431cf3d70066eeaba2c680569faa3b2210e5d14ef63ccd99e.png)

In our case, we have

$$
\begin{aligned}{∮}_{C}F\cdot n\,\text{d}s & ={∮}_{C}(4{x}^{2}{y}^{2}\,i+2{x}^{3}y\,j)\cdot (\frac{x}{2}i+\frac{y}{2}\,j)\text{d}s \\  & ={∮}_{C}2{x}^{3}{y}^{2}+{x}^{3}{y}^{2}\,\text{d}s \\  & ={∮}_{C}3{x}^{3}{y}^{2}\,\text{d}s.\end{aligned}
$$

Therefore, the missing expression is $3{x}^{3}{y}^{2}.$

### q-167889

Source entity 17592186362496; :question.difficulty/easy; :answer-field.type/blank; key field-1.

Water flows over the element $E$ according to the vector field 

$$
F(x,y)=6y\,i+x\,j.
$$

Since the outward-pointing unit normal vector to $E$ found in part 5 has zero $k$-component, it may be considered a two-dimensional vector defined in terms of $i$ and $j$ only. Use this to find an expression for the flux of $F$ across the element in terms of $x$ and $y.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Flux = 
${∮}_{E}$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$\text{d}s.$

Excluded: Prompt requires the normal from part 5; element E and its normal are not supplied.

Source answer bank: $\frac{7}{3}xy$ (correct)

Source operative solution:

If $F$ is a vector field and $E$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $E$ is given by

$$
{∮}_{E}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit vector to $E.$

![](images/2c/2cd5e4c7ab86cdb999e239e986713a51c07b8decb629b1ee4a656077590f04bb.png)

In our case, we have

$$
\begin{aligned}{∮}_{E}F\cdot n\,\text{d}s & ={∮}_{E}(6y\,i+x\,j)\cdot (\frac{x}{3}\,i+\frac{y}{3}\,j)\,\text{d}s \\  & ={∮}_{E}2xy+\frac{1}{3}xy\,\text{d}s \\  & ={∮}_{E}\frac{7}{3}xy\,\text{d}s.\end{aligned}
$$

### q-127058

Source entity 17592186420909; :question.difficulty/moderate; :answer-field.type/radio; key selection.

![](images/65/653699a9c78577272425de7f8e6d015743e2c2e8c6e9a21bef189dc06fd80684.png)

Consider the vector field $F(x,y)={x}^{5}{y}^{7}\,i+x{y}^{3}\,j$ and the rectangle $C$ shown above. If the flux of $F$ across the side ${C}_{1}$ is given by

$$
{\int }_{{C}_{1}}\boxed{}\,\text{d}s,
$$

what is the missing expression?

Supplied P=x**5*y**7, Q=x*y**3; outward normal (1, 0). Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127058.

Source answer bank: $-x{y}^{3}$, ${x}^{5}{y}^{7}$ (correct), $3{x}^{3}{y}^{2}$, $x{y}^{3}$, $3x{y}^{2}$

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

In our case, we need to find an expression for the flux across only the part ${C}_{1}$ of the closed curve $C.$ Since this side is perpendicular to the $x$-axis and we require an outward-pointing unit normal vector, we must have $n=i.$

![](images/35/35e33731fbe85305a4308ef03c9f793b77558d66350d9345c30e643df1c40ba1.png)

Therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot n\,\text{d}s & ={\int }_{{C}_{1}}({x}^{5}{y}^{7}\,i+x{y}^{3}\,j)\cdot i\,\text{d}s \\  & ={\int }_{{C}_{1}}{x}^{5}{y}^{7}\,\text{d}s\end{aligned}
$$

Therefore, the missing expression is ${x}^{5}{y}^{7}.$

### q-127059

Source entity 17592186420913; :question.difficulty/moderate; :answer-field.type/radio; key selection.

![](images/1b/1b08e4cc9dd6ebde7f4bf544d7a76c4706dbd69a2c31d4c0fda8f816d4f871b5.png)

Consider the vector field $F(x,y)=(x+y)^{2}\,i+(x-y)^{2}\,j$ and the rectangle $C$  shown above. If the flux of $F$ across the side ${C}_{2}$ is given by

$$
{\int }_{{C}_{2}}\boxed{}\,\text{d}s,
$$

what is the missing expression?

Supplied P=(x + y)**2, Q=(x - y)**2; outward normal (0, 1). Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127059.

Source answer bank: $-4xy$, $4xy$, $(x-y)^{2}$ (correct), $y-x$, $-(x-y)^{2}$

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

In our case, we need to find an expression for the flux across only the part ${C}_{2}$ of the closed curve $C.$ Since this side is perpendicular to the $y$-axis and we require an outward-pointing unit normal vector, we must have $n=j.$ 

![](images/5d/5d0e9699f75e1f3f727c5c771fdce1a66311496cb55d31c0aac789901feed0cb.png)

Therefore,

$$
\begin{aligned}{\int }_{{C}_{2}}F\cdot n\,\text{d}s & ={\int }_{{C}_{2}}((x+y)^{2}\,i+(x-y)^{2}\,j)\cdot j\,\text{d}s \\  & ={\int }_{{C}_{2}}(x-y)^{2}\,\text{d}s\end{aligned}
$$

Therefore, the missing expression is $(x-y)^{2}.$

### q-127052

Source entity 17592186552465; :question.difficulty/easy; :answer-field.type/radio; key selection.

Consider the vector field $F(x,y)=3xy\,i-{x}^{2}\,j$ and the circle $C$ given by ${x}^{2}+{y}^{2}=1.$ If the flux of $F$ across $C$ is given by

$$
{∮}_{C}\boxed{}\,\text{d}s,
$$

what is the missing expression?

*Hint: The outward-pointing unit normal vector to $C$ is $n=x\,i+y\,j.$*

Supplied P=3*x*y, Q=-x**2; circle radius 1. Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127052.

Source answer bank: ${x}^{3}y+{x}^{2}y$, $2{x}^{2}y$ (correct), ${x}^{2}-3{x}^{3}y$, $xy-x{y}^{2}$, $3{x}^{3}{y}^{2}-{x}^{3}$

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

![](images/38/386f010932b5846e7f47a605a94a5b5d580bd35dbe37512b1583d15d29f3dc70.png)

In our case, we have

$$
\begin{aligned}{∮}_{C}F\cdot n\,\text{d}s & ={∮}_{C}(3xy\,i-{x}^{2}\,j)\cdot (xi+y\,j)\,\text{d}s \\  & ={∮}_{C}3{x}^{2}y-{x}^{2}y\,\text{d}s \\  & ={∮}_{C}2{x}^{2}y\,\text{d}s.\end{aligned}
$$

Therefore, the missing expression is $2{x}^{2}y.$

### q-127054

Source entity 17592186552470; :question.difficulty/moderate; :answer-field.type/radio; key selection.

![](images/0d/0dd48f19e9940f1684c0cbb723e772384dda3d7429fc89c2c9dc528f7ebfe42c.png)

Consider the vector field $F(x,y)=xy\,i-{x}^{2}y\,j$ and the square $C$ with side length $4$ centered at $O,$ shown above. If the flux of $F$ across the side ${C}_{4}$ is given by

$$
{\int }_{{C}_{4}}\boxed{}\,\text{d}s,
$$

what is the missing expression?

Supplied P=x*y, Q=-x**2*y; outward normal (0, -1). Correct expression follows (kP,kQ)·n. All original domain and figure relationships are unchanged. Profile: observed-whole-field-scale:q-127054.

Source answer bank: $-y$, $xy$, ${x}^{2}$, $-xy$, ${x}^{2}y$ (correct)

Source operative solution:

If $F$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the flux of $F$ across $C$ is given by

$$
{∮}_{C}F\cdot n\,\text{d}s,
$$

where $n$ denotes the outward-pointing unit normal vector to $C.$

In our case, we need to find an expression for the flux across only the part ${C}_{4}$ of the closed curve $C.$ Since this side is perpendicular to the $y$-axis and we require an outward-pointing unit normal vector, we must have $n=-j.$

![](images/c5/c591fedf1b1c8ea705f0c13fbfd96bc7f1f6701841e3eff03bd0578aa2f8ab06.png)

Therefore,

$$
\begin{aligned}{\int }_{{C}_{4}}F\cdot n\,\text{d}s & ={\int }_{{C}_{4}}(xy\,i-{x}^{2}y\,j)\cdot (-j)\,\text{d}s \\  & ={\int }_{{C}_{4}}{x}^{2}y\,\text{d}s\end{aligned}
$$

Therefore, the missing expression is ${x}^{2}y.$
