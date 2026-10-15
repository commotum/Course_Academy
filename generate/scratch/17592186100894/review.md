Source q-20071

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{4x-y}$ that satisfies $y(0)=5.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{4x-y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{4x}\cdot {e}^{-y} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{4x} \\ \int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{4x}\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int {e}^{4x}\,\text{d}x \\ {e}^{y} & =\frac{{e}^{4x}}{4}+C\,.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(\frac{{e}^{4x}}{4}+C) \\ y & =\operatorname{ln}⁡(\frac{{e}^{4x}}{4}+C)\end{aligned}
$$

We now apply the condition $y(0)=5$ to find $C:$

$$
\begin{aligned}y(0) & =5 \\ \operatorname{ln}⁡(\frac{{e}^{4\cdot 0}}{4}+C) & =5 \\ \operatorname{ln}⁡(\frac{1}{4}+C) & =5 \\ \frac{1}{4}+C & ={e}^{5} \\ C & =\frac{4{e}^{5}-1}{4}\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{4x-y}$ that satisfies the condition $y(0)=5$ is

$$
y=\operatorname{ln}⁡(\frac{{e}^{4x}+4{e}^{5}-1}{4}).
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{4(x - 2)-y}$ that satisfies $y(2)=5.$

y=\operatorname{ln}⁡({e}^{4(x - 2)}-\frac{1}{4})
y=\operatorname{ln}⁡({e}^{4(x - 2)}+5)
y=\operatorname{ln}⁡(\frac{{e}^{4(x - 2)}}{4}+C)
y=\operatorname{ln}⁡(\frac{{e}^{4(x - 2)}+4{e}^{5}-1}{4})
y=\operatorname{ln}⁡(\frac{{e}^{4(x - 2)}}{4}+{e}^{5}+\frac{1}{4})

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{4(x - 2)-y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{4(x - 2)}\cdot {e}^{-y} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{4(x - 2)} \\ \int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{4(x - 2)}\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int {e}^{4(x - 2)}\,\text{d}x \\ {e}^{y} & =\frac{{e}^{4(x - 2)}}{4}+C\,.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(\frac{{e}^{4(x - 2)}}{4}+C) \\ y & =\operatorname{ln}⁡(\frac{{e}^{4(x - 2)}}{4}+C)\end{aligned}
$$

We now apply the condition $y(2)=5$ to find $C:$

$$
\begin{aligned}y(2) & =5 \\ \operatorname{ln}⁡(\frac{{e}^{4\cdot 0}}{4}+C) & =5 \\ \operatorname{ln}⁡(\frac{1}{4}+C) & =5 \\ \frac{1}{4}+C & ={e}^{5} \\ C & =\frac{4{e}^{5}-1}{4}\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{4(x - 2)-y}$ that satisfies the condition $y(2)=5$ is

$$
y=\operatorname{ln}⁡(\frac{{e}^{4(x - 2)}+4{e}^{5}-1}{4}).
$$

---

Source q-79372

Find the particular solution to the differential equation $(\frac{1}{xy}+\frac{1}{y})\frac{\text{d}y}{\text{d}x}=1$ that satisfies $y(1)=e.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}(\frac{1}{xy}+\frac{1}{y})\frac{\text{d}y}{\text{d}x} & =1 \\ \frac{1}{y}(\frac{1+x}{x})\frac{\text{d}y}{\text{d}x} & =1 \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{x}{x+1} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{x}{x+1}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (1-\frac{1}{x+1})\,\text{d}x \\ \operatorname{ln}⁡|y| & =x-\operatorname{ln}⁡|x+1|+C.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{x-\operatorname{ln}⁡|x+1|+C} \\ |y| & ={e}^{x-\operatorname{ln}⁡|x+1|+C} \\ |y| & ={e}^{x}\cdot {e}^{-\operatorname{ln}⁡|x+1|}\cdot {e}^{C} \\ y & =\frac{K{e}^{x}}{x+1},\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the initial condition $y(1)=e$ to find $K:$

$$
\begin{aligned}y(1) & =e \\ \frac{K{e}^{1}}{1+1} & =e \\ K & =2\,.\end{aligned}
$$

Thus the particular solution of $(\frac{1}{xy}+\frac{1}{y})\frac{\text{d}y}{\text{d}x}=1$ that satisfies the condition $y(1)=e$ is

$$
y=\frac{2{e}^{x}}{x+1}\,.
$$

Variant

Find the particular solution to the differential equation $(\frac{1}{(x - 2)y}+\frac{1}{y})\frac{\text{d}y}{\text{d}x}=1$ that satisfies $y(3)=e.$

y=\frac{4{e}^{(x - 2)}}{(x - 2)+2}
y=\frac{{e}^{(x - 2)+1}}{(x - 2)+1}
y=\frac{2{e}^{(x - 2)}}{(x - 2)+1}
y=\frac{2{e}^{-(x - 2)}}{{(x - 2)}^{2}+1}
y=\frac{4{e}^{-(x - 2)}}{{(x - 2)}^{2}+2}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}(\frac{1}{(x - 2)y}+\frac{1}{y})\frac{\text{d}y}{\text{d}x} & =1 \\ \frac{1}{y}(\frac{1+(x - 2)}{(x - 2)})\frac{\text{d}y}{\text{d}x} & =1 \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{(x - 2)}{(x - 2)+1} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{(x - 2)}{(x - 2)+1}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (1-\frac{1}{(x - 2)+1})\,\text{d}x \\ \operatorname{ln}⁡|y| & =(x - 2)-\operatorname{ln}⁡|(x - 2)+1|+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{(x - 2)-\operatorname{ln}⁡|(x - 2)+1|+C} \\ |y| & ={e}^{(x - 2)-\operatorname{ln}⁡|(x - 2)+1|+C} \\ |y| & ={e}^{(x - 2)}\cdot {e}^{-\operatorname{ln}⁡|(x - 2)+1|}\cdot {e}^{C} \\ y & =\frac{K{e}^{(x - 2)}}{(x - 2)+1},\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the initial condition $y(3)=e$ to find $K:$

$$
\begin{aligned}y(3) & =e \\ \frac{K{e}^{1}}{1+1} & =e \\ K & =2\,.\end{aligned}
$$

Thus the particular solution of $(\frac{1}{(x - 2)y}+\frac{1}{y})\frac{\text{d}y}{\text{d}x}=1$ that satisfies the condition $y(3)=e$ is

$$
y=\frac{2{e}^{(x - 2)}}{(x - 2)+1}\,.
$$

---

Source q-128192

Find the solution to the initial value problem 

$$
{y}^{′}=x{y}^{2},\,y(1)=2.
$$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $y(x)=\,\,$ 

                                    
                                
                                    
                            
                                        {{field-1}}

From part 6, we found the general solution

$$
\begin{aligned}y & =-2{({x}^{2}+K)}^{-1},\end{aligned}
$$

where $K$ is an arbitrary constant.

Now, we apply the initial condition $y(1)=2$ to find $K:$

$$
\begin{aligned}y(1) & =2 \\ -2{({1}^{2}+K)}^{-1} & =2 \\ 1+K & =-1 \\ K & =-2\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
y=-2({x}^{2}-2)^{-1}=-\frac{2}{{x}^{2}-2}.
$$

Variant

Find the solution to the initial value problem

$$
{y}^{′}=(x - 2){y}^{2},\,y(3)=2.
$$
$y(x)=\,\,$ {{field-1}}

-2/({(x - 2)}^{2}-2)

Separating variables and integrating, we find the general solution

$$
\begin{aligned}y & =-2{({(x - 2)}^{2}+K)}^{-1},\end{aligned}
$$

where $K$ is an arbitrary constant.

Now, we apply the initial condition $y(3)=2$ to find $K:$

$$
\begin{aligned}y(3) & =2 \\ -2{({1}^{2}+K)}^{-1} & =2 \\ 1+K & =-1 \\ K & =-2\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
y=-2({(x - 2)}^{2}-2)^{-1}=-\frac{2}{{(x - 2)}^{2}-2}.
$$

---

Source q-104059

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}}+{y}^{2}$ that satisfies $y(-1)=1.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{x}^{2}}+{y}^{2} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{x}^{2}}+1 \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{{x}^{2}}+1)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\text{d}y & =\int \frac{1}{{x}^{2}}\,\text{d}x+\int \,\text{d}x \\ -\frac{1}{y} & =-\frac{1}{x}+x+C \\ \frac{1}{y} & =\frac{1-{x}^{2}-Cx}{x} \\ y & =\frac{x}{1-{x}^{2}-Cx}.\end{aligned}
$$

We conclude that the general solution is

$$
\begin{aligned}y & =\frac{x}{1-{x}^{2}-Cx},\end{aligned}
$$

where $C$ is an arbitrary constant. 

We now apply the initial condition $y(-1)=1$ to find $C:$

$$
\begin{aligned}y(-1) & =1 \\ \frac{-1}{1-(-1)^{2}-C(-1)} & =1 \\ \frac{-1}{C} & =1 \\ C & =-1\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}}+{y}^{2}$ that satisfies the condition $y(-1)=1$ is

$$
y=\frac{x}{1+x-{x}^{2}}\,.
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{(x - 2)}^{2}}+{y}^{2}$ that satisfies $y(1)=1.$

y=\frac{(x - 2)}{1+(x - 2)-{(x - 2)}^{2}}
y=\frac{(x - 2)}{2+2(x - 2)-{(x - 2)}^{2}}
y=\frac{(x - 2)}{2(x - 2)+{(x - 2)}^{2}}
y=\frac{(x - 2)}{{(x - 2)}^{2}-2(x - 2)}
y=-\frac{(x - 2)}{1+(x - 2)+{(x - 2)}^{2}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{(x - 2)}^{2}}+{y}^{2} \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{(x - 2)}^{2}}+1 \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{{(x - 2)}^{2}}+1)\,\text{d}x \\ \int \frac{1}{{y}^{2}}\text{d}y & =\int \frac{1}{{(x - 2)}^{2}}\,\text{d}x+\int \,\text{d}x \\ -\frac{1}{y} & =-\frac{1}{(x - 2)}+(x - 2)+C \\ \frac{1}{y} & =\frac{1-{(x - 2)}^{2}-C(x - 2)}{(x - 2)} \\ y & =\frac{(x - 2)}{1-{(x - 2)}^{2}-C(x - 2)}.\end{aligned}
$$

We conclude that the general solution is

$$
\begin{aligned}y & =\frac{(x - 2)}{1-{(x - 2)}^{2}-C(x - 2)},\end{aligned}
$$

where $C$ is an arbitrary constant. 

We now apply the initial condition $y(1)=1$ to find $C:$

$$
\begin{aligned}y(1) & =1 \\ \frac{-1}{1-(-1)^{2}-C(-1)} & =1 \\ \frac{-1}{C} & =1 \\ C & =-1\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{(x - 2)}^{2}}+{y}^{2}$ that satisfies the condition $y(1)=1$ is

$$
y=\frac{(x - 2)}{1+(x - 2)-{(x - 2)}^{2}}\,.
$$

---

Source q-104064

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=3{y}^{2}{x}^{2}-4{y}^{2}{x}^{3}$ that satisfies $y(2)=\frac{1}{8}.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{y}^{2}{x}^{2}-4{y}^{2}{x}^{3} \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(3{x}^{2}-4{x}^{3}) \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}-4{x}^{3} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{x}^{2}-4{x}^{3})\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =3\int {x}^{2}\,\text{d}x-4\int {x}^{3}\,\text{d}x \\ -\frac{1}{y} & ={x}^{3}-{x}^{4}+C \\ y & =\frac{1}{{x}^{4}-{x}^{3}-C}.\end{aligned}
$$

We now apply the initial condition $y(2)=\frac{1}{8}$ to find $C:$

$$
\begin{aligned}y(2) & =\frac{1}{8} \\ \frac{1}{{2}^{4}-{2}^{3}-C} & =\frac{1}{8} \\ \frac{1}{8-C} & =\frac{1}{8} \\ C & =0\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}=3{y}^{2}{x}^{2}-4{y}^{2}{x}^{3}$ that satisfies the condition $y(2)=\frac{1}{8}$ is

$$
y=\frac{1}{{x}^{4}-{x}^{3}}\,.
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=3{y}^{2}{(x - 2)}^{2}-4{y}^{2}{(x - 2)}^{3}$ that satisfies $y(4)=\frac{1}{8}.$

y=\frac{1}{{(x - 2)}^{3}-{(x - 2)}^{4}+16}
y=\frac{1}{{(x - 2)}^{4}+{(x - 2)}^{3}-16}
y=\frac{1}{2{(x - 2)}^{3}+2{(x - 2)}^{2}}
y=\frac{1}{{(x - 2)}^{3}-{(x - 2)}^{2}+4}
y=\frac{1}{{(x - 2)}^{4}-{(x - 2)}^{3}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{y}^{2}{(x - 2)}^{2}-4{y}^{2}{(x - 2)}^{3} \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(3{(x - 2)}^{2}-4{(x - 2)}^{3}) \\ \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x} & =3{(x - 2)}^{2}-4{(x - 2)}^{3} \\ \int \frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{(x - 2)}^{2}-4{(x - 2)}^{3})\,\text{d}x \\ \int \frac{1}{{y}^{2}}\,\text{d}y & =3\int {(x - 2)}^{2}\,\text{d}x-4\int {(x - 2)}^{3}\,\text{d}x \\ -\frac{1}{y} & ={(x - 2)}^{3}-{(x - 2)}^{4}+C \\ y & =\frac{1}{{(x - 2)}^{4}-{(x - 2)}^{3}-C}.\end{aligned}
$$

We now apply the initial condition $y(4)=\frac{1}{8}$ to find $C:$

$$
\begin{aligned}y(4) & =\frac{1}{8} \\ \frac{1}{{2}^{4}-{2}^{3}-C} & =\frac{1}{8} \\ \frac{1}{8-C} & =\frac{1}{8} \\ C & =0\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}=3{y}^{2}{(x - 2)}^{2}-4{y}^{2}{(x - 2)}^{3}$ that satisfies the condition $y(4)=\frac{1}{8}$ is

$$
y=\frac{1}{{(x - 2)}^{4}-{(x - 2)}^{3}}\,.
$$

---

Source q-104065

Find the particular solution to the differential equation $\operatorname{sin}⁡x\frac{\text{d}y}{\text{d}x}-8x\operatorname{sin}⁡x=\operatorname{cos}⁡x$ that satisfies $y(\frac{\pi }{2})={\pi }^{2}.$ Assume that $0<x<\pi .$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\operatorname{sin}⁡x\frac{\text{d}y}{\text{d}x}-8x\operatorname{sin}⁡x & =\operatorname{cos}⁡x \\ \operatorname{sin}⁡x\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x+8x\operatorname{sin}⁡x \\ \frac{\text{d}y}{\text{d}x} & =\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}+8x \\ \int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}+8x)\,\text{d}x \\ \int \,\text{d}y & =\int \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x+8\int x\,\text{d}x \\ y & =\int \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x+4{x}^{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral on the right-hand side of this equality, we use a substitution

$$
u=\operatorname{sin}⁡x\,⟹\,\text{d}u=\operatorname{cos}⁡x\,\text{d}x.
$$

Then  we have

$$
\begin{aligned}\int \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x & =\int \frac{1}{\operatorname{sin}⁡x}(\operatorname{cos}⁡x\,\text{d}x) \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+{C}_{2} \\  & =\operatorname{ln}⁡(\operatorname{sin}⁡x)+{C}_{2},\end{aligned}
$$

where we used that $\operatorname{sin}⁡x>0.$

Hence,

$$
y=\operatorname{ln}⁡(\operatorname{sin}⁡x)+4{x}^{2}+C.
$$

where $C={C}_{1}+{C}_{2}$ is an arbitrary constant. 

We now apply the initial condition $y(\frac{\pi }{2})={\pi }^{2}$ to find $C:$

$$
\begin{aligned}y(\frac{\pi }{2}) & ={\pi }^{2} \\ \operatorname{ln}⁡(\operatorname{sin}⁡\frac{\pi }{2})+4{(\frac{\pi }{2})}^{2}+C & ={\pi }^{2} \\ \operatorname{ln}⁡1+{\pi }^{2}+C & ={\pi }^{2} \\ C & =0\,.\end{aligned}
$$

Thus the particular solution of $\operatorname{sin}⁡x\frac{\text{d}y}{\text{d}x}-8x\operatorname{sin}⁡x=\operatorname{cos}⁡x$ that satisfies the condition $y(\frac{\pi }{2})={\pi }^{2}$ is

$$
y=\operatorname{ln}⁡(\operatorname{sin}⁡x)+4{x}^{2}.
$$

Variant

Find the particular solution to the differential equation $\operatorname{sin}⁡(x - 2)\frac{\text{d}y}{\text{d}x}-8(x - 2)\operatorname{sin}⁡(x - 2)=\operatorname{cos}⁡(x - 2)$ that satisfies $y(\frac{\pi}{2} + 2)={\pi }^{2}.$ Assume that $0<(x - 2)<\pi .$

y=\operatorname{ln}⁡(\operatorname{sin}⁡(x - 2))+4{(x - 2)}^{2}
y=\operatorname{sin}⁡(x - 2)+4{(x - 2)}^{2}-1
y=\operatorname{cos}⁡(x - 2)+8{(x - 2)}^{2}-{\pi }^{2}
y=\operatorname{ln}⁡(\operatorname{sin}⁡(x - 2))+8{(x - 2)}^{2}-{\pi }^{2}
y=\operatorname{cos}⁡(x - 2)+4{(x - 2)}^{2}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\operatorname{sin}⁡(x - 2)\frac{\text{d}y}{\text{d}x}-8(x - 2)\operatorname{sin}⁡(x - 2) & =\operatorname{cos}⁡(x - 2) \\ \operatorname{sin}⁡(x - 2)\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡(x - 2)+8(x - 2)\operatorname{sin}⁡(x - 2) \\ \frac{\text{d}y}{\text{d}x} & =\frac{\operatorname{cos}⁡(x - 2)}{\operatorname{sin}⁡(x - 2)}+8(x - 2) \\ \int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{\operatorname{cos}⁡(x - 2)}{\operatorname{sin}⁡(x - 2)}+8(x - 2))\,\text{d}x \\ \int \,\text{d}y & =\int \frac{\operatorname{cos}⁡(x - 2)}{\operatorname{sin}⁡(x - 2)}\,\text{d}x+8\int (x - 2)\,\text{d}x \\ y & =\int \frac{\operatorname{cos}⁡(x - 2)}{\operatorname{sin}⁡(x - 2)}\,\text{d}x+4{(x - 2)}^{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral on the right-hand side of this equality, we use a substitution

$$
u=\operatorname{sin}⁡(x - 2)\,⟹\,\text{d}u=\operatorname{cos}⁡(x - 2)\,\text{d}x.
$$

Then  we have

$$
\begin{aligned}\int \frac{\operatorname{cos}⁡(x - 2)}{\operatorname{sin}⁡(x - 2)}\,\text{d}x & =\int \frac{1}{\operatorname{sin}⁡(x - 2)}(\operatorname{cos}⁡(x - 2)\,\text{d}x) \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+{C}_{2} \\  & =\operatorname{ln}⁡(\operatorname{sin}⁡(x - 2))+{C}_{2},\end{aligned}
$$

where we used that $\operatorname{sin}⁡(x - 2)>0.$

Hence,

$$
y=\operatorname{ln}⁡(\operatorname{sin}⁡(x - 2))+4{(x - 2)}^{2}+C.
$$

where $C={C}_{1}+{C}_{2}$ is an arbitrary constant. 

We now apply the initial condition $y(\frac{\pi}{2} + 2)={\pi }^{2}$ to find $C:$

$$
\begin{aligned}y(\frac{\pi}{2} + 2) & ={\pi }^{2} \\ \operatorname{ln}⁡(\operatorname{sin}⁡\frac{\pi }{2})+4{(\frac{\pi }{2})}^{2}+C & ={\pi }^{2} \\ \operatorname{ln}⁡1+{\pi }^{2}+C & ={\pi }^{2} \\ C & =0\,.\end{aligned}
$$

Thus the particular solution of $\operatorname{sin}⁡(x - 2)\frac{\text{d}y}{\text{d}x}-8(x - 2)\operatorname{sin}⁡(x - 2)=\operatorname{cos}⁡(x - 2)$ that satisfies the condition $y(\frac{\pi}{2} + 2)={\pi }^{2}$ is

$$
y=\operatorname{ln}⁡(\operatorname{sin}⁡(x - 2))+4{(x - 2)}^{2}.
$$

---

Source q-14267

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{x+y}$ given that  $\,y(0)=-\operatorname{ln}⁡2.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{x+y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{x}{e}^{y} \\ {e}^{-y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{x} \\ \int {e}^{-y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{x}\,\text{d}x \\ \int {e}^{-y}\,\text{d}y & =\int {e}^{x}\,\text{d}x \\ -{e}^{-y} & ={e}^{x}+{C}_{1} \\ {e}^{-y} & =-{e}^{x}+C\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{-y}) & =\operatorname{ln}⁡(-{e}^{x}+C) \\ -y & =\operatorname{ln}⁡(C-{e}^{x}) \\ y & =-\operatorname{ln}⁡(C-{e}^{x}).\end{aligned}
$$

We now apply the condition $y(0)=-\operatorname{ln}⁡2$ to find $C:$

$$
\begin{aligned}y(0) & =-\operatorname{ln}⁡2 \\ -\operatorname{ln}⁡(C-{e}^{0}) & =-\operatorname{ln}⁡2 \\ \operatorname{ln}⁡(C-1) & =\operatorname{ln}⁡2 \\ C-1 & =2 \\ C & =3\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{x+y}$ that satisfies the condition $y(0)=-\operatorname{ln}⁡2$ is

$$
y=-\operatorname{ln}⁡(3-{e}^{x}).
$$

Variant

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{(x - 2)+y}$ given that  $\,y(2)=-\operatorname{ln}⁡2.$

y=-\operatorname{ln}⁡(1+{e}^{(x - 2)})
y=-\operatorname{ln}⁡(1+(x - 2)+{e}^{(x - 2)})
y=-\operatorname{ln}⁡((x - 2)+{e}^{(x - 2)})
y=-\operatorname{ln}⁡(3-2(x - 2)-{e}^{(x - 2)})
y=-\operatorname{ln}⁡(3-{e}^{(x - 2)})

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{(x - 2)+y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{(x - 2)}{e}^{y} \\ {e}^{-y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{(x - 2)} \\ \int {e}^{-y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{(x - 2)}\,\text{d}x \\ \int {e}^{-y}\,\text{d}y & =\int {e}^{(x - 2)}\,\text{d}x \\ -{e}^{-y} & ={e}^{(x - 2)}+{C}_{1} \\ {e}^{-y} & =-{e}^{(x - 2)}+C\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{-y}) & =\operatorname{ln}⁡(-{e}^{(x - 2)}+C) \\ -y & =\operatorname{ln}⁡(C-{e}^{(x - 2)}) \\ y & =-\operatorname{ln}⁡(C-{e}^{(x - 2)}).\end{aligned}
$$

We now apply the condition $y(2)=-\operatorname{ln}⁡2$ to find $C:$

$$
\begin{aligned}y(2) & =-\operatorname{ln}⁡2 \\ -\operatorname{ln}⁡(C-{e}^{0}) & =-\operatorname{ln}⁡2 \\ \operatorname{ln}⁡(C-1) & =\operatorname{ln}⁡2 \\ C-1 & =2 \\ C & =3\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{(x - 2)+y}$ that satisfies the condition $y(2)=-\operatorname{ln}⁡2$ is

$$
y=-\operatorname{ln}⁡(3-{e}^{(x - 2)}).
$$

---

Source q-350957

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{e}^{-y}=6{x}^{2}{e}^{-y}$ that satisfies $y(1)=0.$

$y(x)=$
{{field-1}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{e}^{-y} & =6{x}^{2}{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =6{x}^{2}{e}^{-y}-{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =(6{x}^{2}-1){e}^{-y} \\ {e}^{y}\,\text{d}y & =(6{x}^{2}-1)\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (6{x}^{2}-1)\,\text{d}x \\ {e}^{y} & =2{x}^{3}-x+C.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(2{x}^{3}-x+C) \\ y & =\operatorname{ln}⁡(2{x}^{3}-x+C)\end{aligned}
$$

We now apply the initial condition $y(1)=0$ to find $C:$

$$
\begin{aligned}y(1) & =0 \\ \operatorname{ln}⁡(2\cdot {1}^{3}-1+C) & =0 \\ \operatorname{ln}⁡(1+C) & =0 \\ C & =0\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\operatorname{ln}⁡(2{x}^{3}-x).
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{e}^{-y}=6{(x - 2)}^{2}{e}^{-y}$ that satisfies $y(3)=0.$

$y(x)=$
{{field-1}}

\operatorname{ln}(2{(x - 2)}^{3}-(x - 2))

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{e}^{-y} & =6{(x - 2)}^{2}{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =6{(x - 2)}^{2}{e}^{-y}-{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =(6{(x - 2)}^{2}-1){e}^{-y} \\ {e}^{y}\,\text{d}y & =(6{(x - 2)}^{2}-1)\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (6{(x - 2)}^{2}-1)\,\text{d}x \\ {e}^{y} & =2{(x - 2)}^{3}-(x - 2)+C.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(2{(x - 2)}^{3}-(x - 2)+C) \\ y & =\operatorname{ln}⁡(2{(x - 2)}^{3}-(x - 2)+C)\end{aligned}
$$

We now apply the initial condition $y(3)=0$ to find $C:$

$$
\begin{aligned}y(3) & =0 \\ \operatorname{ln}⁡(2\cdot {1}^{3}-1+C) & =0 \\ \operatorname{ln}⁡(1+C) & =0 \\ C & =0\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\operatorname{ln}⁡(2{(x - 2)}^{3}-(x - 2)).
$$

---

Source q-355546

Find the particular solution to the differential equation ${x}^{2}\frac{\text{d}y}{\text{d}x}-8{x}^{3}=5$ that satisfies $y(1)=6.$

$y(x)=$
{{field-1}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{x}^{2}\frac{\text{d}y}{\text{d}x}-8{x}^{3} & =5 \\ {x}^{2}\frac{\text{d}y}{\text{d}x} & =5+8{x}^{3} \\ \text{d}y & =(5{x}^{-2}+8x)\,\text{d}x \\ \int \text{d}y & =\int (5{x}^{-2}+8x)\,\text{d}x \\ y & =-5{x}^{-1}+4{x}^{2}+C.\end{aligned}
$$

We now apply the initial condition $y(1)=6$ to find $C:$

$$
\begin{aligned}y(1) & =6 \\ -5(1)^{-1}+4(1)^{2}+C & =6 \\ C-1 & =6 \\ C & =7\end{aligned}
$$

Thus, the particular solution is

$$
\begin{aligned}y(x) & =-5{x}^{-1}+4{x}^{2}+7 \\  & =-\frac{5}{x}+4{x}^{2}+7.\end{aligned}
$$

Variant

Find the particular solution to the differential equation ${(x - 2)}^{2}\frac{\text{d}y}{\text{d}x}-8{(x - 2)}^{3}=5$ that satisfies $y(3)=6.$

$y(x)=$
{{field-1}}

-\frac{5}{(x - 2)}+4{(x - 2)}^{2}+7

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{(x - 2)}^{2}\frac{\text{d}y}{\text{d}x}-8{(x - 2)}^{3} & =5 \\ {(x - 2)}^{2}\frac{\text{d}y}{\text{d}x} & =5+8{(x - 2)}^{3} \\ \text{d}y & =(5{(x - 2)}^{-2}+8(x - 2))\,\text{d}x \\ \int \text{d}y & =\int (5{(x - 2)}^{-2}+8(x - 2))\,\text{d}x \\ y & =-5{(x - 2)}^{-1}+4{(x - 2)}^{2}+C.\end{aligned}
$$

We now apply the initial condition $y(3)=6$ to find $C:$

$$
\begin{aligned}y(3) & =6 \\ -5(1)^{-1}+4(1)^{2}+C & =6 \\ C-1 & =6 \\ C & =7\end{aligned}
$$

Thus, the particular solution is

$$
\begin{aligned}y(x) & =-5{(x - 2)}^{-1}+4{(x - 2)}^{2}+7 \\  & =-\frac{5}{(x - 2)}+4{(x - 2)}^{2}+7.\end{aligned}
$$

---

Source q-355547

Find the particular solution to the differential equation $\sqrt{x}\frac{\text{d}y}{\text{d}x}-4x\sqrt{x}=3$ that satisfies $y(1)=11.$

$y(x)=$
{{field-1}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\sqrt{x}\frac{\text{d}y}{\text{d}x}-4x\sqrt{x} & =3 \\ \sqrt{x}\frac{\text{d}y}{\text{d}x} & =3+4x\sqrt{x} \\ \text{d}y & =(3{x}^{-1/2}+4x)\,\text{d}x \\ \int \text{d}y & =\int (3{x}^{-1/2}+4x)\,\text{d}x \\ y & =6{x}^{1/2}+2{x}^{2}+C.\end{aligned}
$$

We now apply the initial condition $y(1)=11$ to find $C:$

$$
\begin{aligned}y(1) & =11 \\ 6(1)^{1/2}+2(1)^{2}+C & =11 \\ C+8 & =11 \\ C & =3\end{aligned}
$$

Thus, the particular solution is

$$
\begin{aligned}y(x) & =6{x}^{1/2}+2{x}^{2}+3 \\  & =6\sqrt{x}+2{x}^{2}+3.\end{aligned}
$$

Variant

Find the particular solution to the differential equation $\sqrt{(x - 2)}\frac{\text{d}y}{\text{d}x}-4(x - 2)\sqrt{(x - 2)}=3$ that satisfies $y(3)=11.$

$y(x)=$
{{field-1}}

6\sqrt{(x - 2)}+2{(x - 2)}^{2}+3

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\sqrt{(x - 2)}\frac{\text{d}y}{\text{d}x}-4(x - 2)\sqrt{(x - 2)} & =3 \\ \sqrt{(x - 2)}\frac{\text{d}y}{\text{d}x} & =3+4(x - 2)\sqrt{(x - 2)} \\ \text{d}y & =(3{(x - 2)}^{-1/2}+4(x - 2))\,\text{d}x \\ \int \text{d}y & =\int (3{(x - 2)}^{-1/2}+4(x - 2))\,\text{d}x \\ y & =6{(x - 2)}^{1/2}+2{(x - 2)}^{2}+C.\end{aligned}
$$

We now apply the initial condition $y(3)=11$ to find $C:$

$$
\begin{aligned}y(3) & =11 \\ 6(1)^{1/2}+2(1)^{2}+C & =11 \\ C+8 & =11 \\ C & =3\end{aligned}
$$

Thus, the particular solution is

$$
\begin{aligned}y(x) & =6{(x - 2)}^{1/2}+2{(x - 2)}^{2}+3 \\  & =6\sqrt{(x - 2)}+2{(x - 2)}^{2}+3.\end{aligned}
$$

---

Source q-355559

Find the particular solution to the differential equation $2y\frac{\text{d}y}{\text{d}x}-4x{y}^{2}=4x$ that satisfies $y(0)=1.$ Assume that $y>0.$

$y(x)=$
{{field-1}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}2y\frac{\text{d}y}{\text{d}x}-4x{y}^{2} & =4x \\ 2y\frac{\text{d}y}{\text{d}x} & =4x{y}^{2}+4x \\ 2y\frac{\text{d}y}{\text{d}x} & =4x({y}^{2}+1) \\ \frac{2y}{{y}^{2}+1}\,\text{d}y & =4x\,\text{d}x \\ \int \frac{2y}{{y}^{2}+1}\,\text{d}y & =\int 4x\,\text{d}x \\ \operatorname{ln}⁡({y}^{2}+1) & =2{x}^{2}+C.\end{aligned}
$$

Exponentiating both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡({y}^{2}+1)} & ={e}^{2{x}^{2}+C} \\ {y}^{2}+1 & =C{e}^{2{x}^{2}} \\ y & =\sqrt{C{e}^{2{x}^{2}}-1}\end{aligned}
$$

where we used that $y>0.$

We now apply the initial condition $y(0)=1$ to find $C:$

$$
\begin{aligned}y(0) & =1 \\ \sqrt{C{e}^{2(0)^{2}}-1} & =1 \\ \sqrt{C-1} & =1 \\ C-1 & =1 \\ C & =2\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\sqrt{2{e}^{2{x}^{2}}-1}.
$$

Variant

Find the particular solution to the differential equation $2y\frac{\text{d}y}{\text{d}x}-4(x - 2){y}^{2}=4(x - 2)$ that satisfies $y(2)=1.$ Assume that $y>0.$

$y(x)=$
{{field-1}}

\sqrt{2{e}^{2{(x - 2)}^{2}}-1}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}2y\frac{\text{d}y}{\text{d}x}-4(x - 2){y}^{2} & =4(x - 2) \\ 2y\frac{\text{d}y}{\text{d}x} & =4(x - 2){y}^{2}+4(x - 2) \\ 2y\frac{\text{d}y}{\text{d}x} & =4(x - 2)({y}^{2}+1) \\ \frac{2y}{{y}^{2}+1}\,\text{d}y & =4(x - 2)\,\text{d}x \\ \int \frac{2y}{{y}^{2}+1}\,\text{d}y & =\int 4(x - 2)\,\text{d}x \\ \operatorname{ln}⁡({y}^{2}+1) & =2{(x - 2)}^{2}+C.\end{aligned}
$$

Exponentiating both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡({y}^{2}+1)} & ={e}^{2{(x - 2)}^{2}+C} \\ {y}^{2}+1 & =C{e}^{2{(x - 2)}^{2}} \\ y & =\sqrt{C{e}^{2{(x - 2)}^{2}}-1}\end{aligned}
$$

where we used that $y>0.$

We now apply the initial condition $y(2)=1$ to find $C:$

$$
\begin{aligned}y(2) & =1 \\ \sqrt{C{e}^{2(0)^{2}}-1} & =1 \\ \sqrt{C-1} & =1 \\ C-1 & =1 \\ C & =2\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\sqrt{2{e}^{2{(x - 2)}^{2}}-1}.
$$

---

Source q-355564

Find the particular solution to the differential equation $(-\frac{1}{xy}+\frac{2}{y})\frac{\text{d}y}{\text{d}x}=4$ that satisfies $y(1)={e}^{2}.$

$y(x)=$
{{field-1}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}(-\frac{1}{xy}+\frac{2}{y})\frac{\text{d}y}{\text{d}x} & =4 \\ \frac{2x-1}{xy}\frac{\text{d}y}{\text{d}x} & =4 \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{4x}{2x-1} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =2+\frac{2}{2x-1} \\ \frac{1}{y}\,\text{d}y & =(2+\frac{2}{2x-1})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (2+\frac{2}{2x-1})\,\text{d}x \\ \operatorname{ln}⁡|y| & =2x+\operatorname{ln}⁡|2x-1|+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{2x+\operatorname{ln}⁡|2x-1|+C} \\ |y| & ={e}^{2x+\operatorname{ln}⁡|2x-1|+C} \\ |y| & ={e}^{2x}\cdot {e}^{\operatorname{ln}⁡|2x-1|}\cdot {e}^{C} \\ y & =K(2x-1){e}^{2x},\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the initial condition $y(1)={e}^{2}$ to find $K:$

$$
\begin{aligned}y(1) & ={e}^{2} \\ K(2(1)-1){e}^{2(1)} & ={e}^{2} \\ K{e}^{2} & ={e}^{2} \\ K & =1\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=(2x-1){e}^{2x}.
$$

Variant

Find the particular solution to the differential equation $(-\frac{1}{(x - 2)y}+\frac{2}{y})\frac{\text{d}y}{\text{d}x}=4$ that satisfies $y(3)={e}^{2}.$

$y(x)=$
{{field-1}}

(2(x - 2)-1){e}^{2(x - 2)}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}(-\frac{1}{(x - 2)y}+\frac{2}{y})\frac{\text{d}y}{\text{d}x} & =4 \\ \frac{2(x - 2)-1}{(x - 2)y}\frac{\text{d}y}{\text{d}x} & =4 \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =\frac{4(x - 2)}{2(x - 2)-1} \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =2+\frac{2}{2(x - 2)-1} \\ \frac{1}{y}\,\text{d}y & =(2+\frac{2}{2(x - 2)-1})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int (2+\frac{2}{2(x - 2)-1})\,\text{d}x \\ \operatorname{ln}⁡|y| & =2(x - 2)+\operatorname{ln}⁡|2(x - 2)-1|+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{2(x - 2)+\operatorname{ln}⁡|2(x - 2)-1|+C} \\ |y| & ={e}^{2(x - 2)+\operatorname{ln}⁡|2(x - 2)-1|+C} \\ |y| & ={e}^{2(x - 2)}\cdot {e}^{\operatorname{ln}⁡|2(x - 2)-1|}\cdot {e}^{C} \\ y & =K(2(x - 2)-1){e}^{2(x - 2)},\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the initial condition $y(3)={e}^{2}$ to find $K:$

$$
\begin{aligned}y(3) & ={e}^{2} \\ K(2(1)-1){e}^{2(1)} & ={e}^{2} \\ K{e}^{2} & ={e}^{2} \\ K & =1\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=(2(x - 2)-1){e}^{2(x - 2)}.
$$

---

Source q-355576

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{-2x-y}$ given that  $\,y(0)=2.$

$y(x)=\operatorname{ln}⁡($
{{field-1}} $)$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{-2x-y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{-2x}{e}^{-y} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{-2x} \\ \int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{-2x}\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int {e}^{-2x}\,\text{d}x \\ {e}^{y} & =-\frac{1}{2}{e}^{-2x}+C\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(-\frac{1}{2}{e}^{-2x}+C) \\ y & =\operatorname{ln}⁡(-\frac{1}{2}{e}^{-2x}+C).\end{aligned}
$$

We now apply the condition $y(0)=2$ to find $C:$

$$
\begin{aligned}y(0) & =2 \\ \operatorname{ln}⁡(-\frac{1}{2}{e}^{0}+C) & =2 \\ \operatorname{ln}⁡(C-\frac{1}{2}) & =2 \\ C-\frac{1}{2} & ={e}^{2} \\ C & =\frac{2{e}^{2}+1}{2}\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{-2x-y}$ that satisfies the condition $y(0)=2$ is

$$
y=\operatorname{ln}⁡(\frac{-{e}^{-2x}+2{e}^{2}+1}{2}).
$$

Variant

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{-2(x - 2)-y}$ given that  $\,y(2)=2.$

$y(x)=\operatorname{ln}⁡($
{{field-1}} $)$

\frac{-{e}^{-2(x - 2)}+2{e}^{2}+1}{2}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{-2(x - 2)-y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{-2(x - 2)}{e}^{-y} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{-2(x - 2)} \\ \int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{-2(x - 2)}\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int {e}^{-2(x - 2)}\,\text{d}x \\ {e}^{y} & =-\frac{1}{2}{e}^{-2(x - 2)}+C\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(-\frac{1}{2}{e}^{-2(x - 2)}+C) \\ y & =\operatorname{ln}⁡(-\frac{1}{2}{e}^{-2(x - 2)}+C).\end{aligned}
$$

We now apply the condition $y(2)=2$ to find $C:$

$$
\begin{aligned}y(2) & =2 \\ \operatorname{ln}⁡(-\frac{1}{2}{e}^{0}+C) & =2 \\ \operatorname{ln}⁡(C-\frac{1}{2}) & =2 \\ C-\frac{1}{2} & ={e}^{2} \\ C & =\frac{2{e}^{2}+1}{2}\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{-2(x - 2)-y}$ that satisfies the condition $y(2)=2$ is

$$
y=\operatorname{ln}⁡(\frac{-{e}^{-2(x - 2)}+2{e}^{2}+1}{2}).
$$

---

Source q-355577

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{-x-y}$ given that $\,y(0)=-\operatorname{ln}⁡4.$

$y(x)=$
{{field-1}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{-x-y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{-x}{e}^{-y} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{-x} \\ \int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{-x}\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int {e}^{-x}\,\text{d}x \\ {e}^{y} & =-{e}^{-x}+C\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(-{e}^{-x}+C) \\ y & =\operatorname{ln}⁡(-{e}^{-x}+C).\end{aligned}
$$

We now apply the condition $y(0)=-\operatorname{ln}⁡4$ to find $C:$

$$
\begin{aligned}y(0) & =-\operatorname{ln}⁡4 \\ \operatorname{ln}⁡(-{e}^{0}+C) & =-\operatorname{ln}⁡4 \\ \operatorname{ln}⁡(C-1) & =-\operatorname{ln}⁡4 \\ C-1 & =\frac{1}{4} \\ C & =\frac{5}{4}\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{-x-y}$ that satisfies the condition $y(0)=-\operatorname{ln}⁡4$ is

$$
y=\operatorname{ln}⁡(\frac{5}{4}-{e}^{-x}).
$$

Variant

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{-(x - 2)-y}$ given that $\,y(2)=-\operatorname{ln}⁡4.$

$y(x)=$
{{field-1}}

\operatorname{ln}(\frac{5}{4}-{e}^{-(x - 2)})

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{-(x - 2)-y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{-(x - 2)}{e}^{-y} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{-(x - 2)} \\ \int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{-(x - 2)}\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int {e}^{-(x - 2)}\,\text{d}x \\ {e}^{y} & =-{e}^{-(x - 2)}+C\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(-{e}^{-(x - 2)}+C) \\ y & =\operatorname{ln}⁡(-{e}^{-(x - 2)}+C).\end{aligned}
$$

We now apply the condition $y(2)=-\operatorname{ln}⁡4$ to find $C:$

$$
\begin{aligned}y(2) & =-\operatorname{ln}⁡4 \\ \operatorname{ln}⁡(-{e}^{0}+C) & =-\operatorname{ln}⁡4 \\ \operatorname{ln}⁡(C-1) & =-\operatorname{ln}⁡4 \\ C-1 & =\frac{1}{4} \\ C & =\frac{5}{4}\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{-(x - 2)-y}$ that satisfies the condition $y(2)=-\operatorname{ln}⁡4$ is

$$
y=\operatorname{ln}⁡(\frac{5}{4}-{e}^{-(x - 2)}).
$$

---

Source q-355582

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{-x-y}$ given that  $\,y(0)=0.$

$y(x)=$
{{field-1}}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{-x-y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{-x}{e}^{-y} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{-x} \\ \int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{-x}\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int {e}^{-x}\,\text{d}x \\ {e}^{y} & =-{e}^{-x}+C\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(-{e}^{-x}+C) \\ y & =\operatorname{ln}⁡(-{e}^{-x}+C).\end{aligned}
$$

We now apply the condition $y(0)=0$ to find $C:$

$$
\begin{aligned}y(0) & =0 \\ \operatorname{ln}⁡(-{e}^{0}+C) & =0 \\ \operatorname{ln}⁡(C-1) & =0 \\ C-1 & =1 \\ C & =2\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{-x-y}$ that satisfies the condition $y(0)=0$ is

$$
y=\operatorname{ln}⁡(2-{e}^{-x}).
$$

Variant

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{-(x - 2)-y}$ given that  $\,y(2)=0.$

$y(x)=$
{{field-1}}

\operatorname{ln}(2-{e}^{-(x - 2)})

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{-(x - 2)-y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{-(x - 2)}{e}^{-y} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{-(x - 2)} \\ \int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{-(x - 2)}\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int {e}^{-(x - 2)}\,\text{d}x \\ {e}^{y} & =-{e}^{-(x - 2)}+C\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡(-{e}^{-(x - 2)}+C) \\ y & =\operatorname{ln}⁡(-{e}^{-(x - 2)}+C).\end{aligned}
$$

We now apply the condition $y(2)=0$ to find $C:$

$$
\begin{aligned}y(2) & =0 \\ \operatorname{ln}⁡(-{e}^{0}+C) & =0 \\ \operatorname{ln}⁡(C-1) & =0 \\ C-1 & =1 \\ C & =2\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{-(x - 2)-y}$ that satisfies the condition $y(2)=0$ is

$$
y=\operatorname{ln}⁡(2-{e}^{-(x - 2)}).
$$

---

Source q-4016

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{x-2y}$ that satisfies $y(0)=0.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{x-2y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{x}\cdot {e}^{-2y} \\ \frac{\text{d}y}{\text{d}x} & =\frac{{e}^{x}}{{e}^{2y}} \\ {e}^{2y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{x} \\ \int {e}^{2y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{x}\,\text{d}x \\ \int {e}^{2y}\,\text{d}y & =\int {e}^{x}\,\text{d}x \\ \frac{1}{2}{e}^{2y} & ={e}^{x}+{C}_{1} \\ {e}^{2y} & =2{e}^{x}+C,\end{aligned}
$$

where $C=2{C}_{1}$ is an arbitrary constant.

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{2y}) & =\operatorname{ln}⁡(2{e}^{x}+C) \\ y & =\frac{1}{2}\operatorname{ln}⁡(2{e}^{x}+C).\end{aligned}
$$

We now apply the condition $y(0)=0$ to find $C:$

$$
\begin{aligned}y(0) & =0 \\ \frac{1}{2}\operatorname{ln}⁡(2{e}^{0}+C) & =0 \\ \operatorname{ln}⁡(2+C) & =0 \\ 2+C & =1 \\ C & =-1\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{x-2y}$ that satisfies the condition $y(0)=0$ is

$$
y=\frac{1}{2}\operatorname{ln}⁡(2{e}^{x}-1).
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{(x - 2)-2y}$ that satisfies $y(2)=0.$

y=\frac{1}{2}\operatorname{ln}⁡(2{e}^{(x - 2)}-1)
y=\operatorname{ln}⁡(2-{e}^{(x - 2)})
y=\frac{1}{2}\operatorname{ln}⁡((x - 2)+1)
y=\operatorname{ln}⁡(\frac{{e}^{(x - 2)}+1}{2})
y=\frac{1}{4}\operatorname{ln}⁡(4{e}^{(x - 2)}-3)

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{(x - 2)-2y} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{(x - 2)}\cdot {e}^{-2y} \\ \frac{\text{d}y}{\text{d}x} & =\frac{{e}^{(x - 2)}}{{e}^{2y}} \\ {e}^{2y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{(x - 2)} \\ \int {e}^{2y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{(x - 2)}\,\text{d}x \\ \int {e}^{2y}\,\text{d}y & =\int {e}^{(x - 2)}\,\text{d}x \\ \frac{1}{2}{e}^{2y} & ={e}^{(x - 2)}+{C}_{1} \\ {e}^{2y} & =2{e}^{(x - 2)}+C,\end{aligned}
$$

where $C=2{C}_{1}$ is an arbitrary constant.

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{2y}) & =\operatorname{ln}⁡(2{e}^{(x - 2)}+C) \\ y & =\frac{1}{2}\operatorname{ln}⁡(2{e}^{(x - 2)}+C).\end{aligned}
$$

We now apply the condition $y(2)=0$ to find $C:$

$$
\begin{aligned}y(2) & =0 \\ \frac{1}{2}\operatorname{ln}⁡(2{e}^{0}+C) & =0 \\ \operatorname{ln}⁡(2+C) & =0 \\ 2+C & =1 \\ C & =-1\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}={e}^{(x - 2)-2y}$ that satisfies the condition $y(2)=0$ is

$$
y=\frac{1}{2}\operatorname{ln}⁡(2{e}^{(x - 2)}-1).
$$

---

Source q-79371

Find the particular solution to the differential equation ${e}^{x}\frac{\text{d}y}{\text{d}x}-2x{e}^{x}=3$ that satisfies $y(0)=-3.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{e}^{x}\frac{\text{d}y}{\text{d}x}-2x{e}^{x} & =3 \\ {e}^{x}\frac{\text{d}y}{\text{d}x} & =3+2x{e}^{x} \\ \frac{\text{d}y}{\text{d}x} & =3{e}^{-x}+2x \\ \int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{e}^{-x}+2x)\,\text{d}x \\ \int \,\text{d}y & =\int 3{e}^{-x}\,\text{d}x+\int 2x\,\text{d}x \\ y & =-3{e}^{-x}+{x}^{2}+C.\end{aligned}
$$

We now apply the initial condition $y(0)=-3$ to find $C:$

$$
\begin{aligned}y(0) & =-3 \\ -3{e}^{-0}+{0}^{2}+C & =-3 \\ C-3 & =-3 \\ C & =0\,.\end{aligned}
$$

Thus the particular solution of ${e}^{x}\frac{\text{d}y}{\text{d}x}-2x{e}^{x}=3$ that satisfies the condition $y(0)=-3$ is

$$
y={x}^{2}-3{e}^{-x}.
$$

Variant

Find the particular solution to the differential equation ${e}^{(x - 2)}\frac{\text{d}y}{\text{d}x}-2(x - 2){e}^{(x - 2)}=3$ that satisfies $y(2)=-3.$

y=(x - 2)+{e}^{-3(x - 2)}-4
y={(x - 2)}^{2}-3{e}^{-(x - 2)}
y={(x - 2)}^{2}-3{e}^{-(x - 2)}+2
y=4(x - 2)+{e}^{-3(x - 2)}-4
y=-2{e}^{-(x - 2)}-1

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{e}^{(x - 2)}\frac{\text{d}y}{\text{d}x}-2(x - 2){e}^{(x - 2)} & =3 \\ {e}^{(x - 2)}\frac{\text{d}y}{\text{d}x} & =3+2(x - 2){e}^{(x - 2)} \\ \frac{\text{d}y}{\text{d}x} & =3{e}^{-(x - 2)}+2(x - 2) \\ \int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{e}^{-(x - 2)}+2(x - 2))\,\text{d}x \\ \int \,\text{d}y & =\int 3{e}^{-(x - 2)}\,\text{d}x+\int 2(x - 2)\,\text{d}x \\ y & =-3{e}^{-(x - 2)}+{(x - 2)}^{2}+C.\end{aligned}
$$

We now apply the initial condition $y(2)=-3$ to find $C:$

$$
\begin{aligned}y(2) & =-3 \\ -3{e}^{-0}+{0}^{2}+C & =-3 \\ C-3 & =-3 \\ C & =0\,.\end{aligned}
$$

Thus the particular solution of ${e}^{(x - 2)}\frac{\text{d}y}{\text{d}x}-2(x - 2){e}^{(x - 2)}=3$ that satisfies the condition $y(2)=-3$ is

$$
y={(x - 2)}^{2}-3{e}^{-(x - 2)}.
$$

---

Source q-79373

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{e}^{-y}=4{x}^{3}{e}^{-y}$ that satisfies $y(1)=0.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{e}^{-y} & =4{x}^{3}{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =4{x}^{3}{e}^{-y}-{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =(4{x}^{3}-1){e}^{-y} \\ {e}^{y}\frac{\text{d}y}{\text{d}x} & =4{x}^{3}-1 \\ \int {e}^{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (4{x}^{3}-1)\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (4{x}^{3}-1)\,\text{d}x \\ {e}^{y} & ={x}^{4}-x+C.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡({x}^{4}-x+C) \\ y & =\operatorname{ln}⁡({x}^{4}-x+C)\end{aligned}
$$

We now apply the initial condition $y(1)=0$ to find $C:$

$$
\begin{aligned}y(1) & =0 \\ \operatorname{ln}⁡({1}^{4}-1+C) & =0 \\ \operatorname{ln}⁡C & =0 \\ C & =1\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}+{e}^{-y}=4{x}^{3}{e}^{-y}$ that satisfies the condition $y(1)=0$ is

$$
y=\operatorname{ln}⁡({x}^{4}-x+1).
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+{e}^{-y}=4{(x - 2)}^{3}{e}^{-y}$ that satisfies $y(3)=0.$

y=\operatorname{ln}⁡(\frac{{(x - 2)}^{4}-(x - 2)+2}{2})
y=\operatorname{ln}⁡(\frac{{(x - 2)}^{2}+1}{2})
y=\operatorname{ln}⁡({(x - 2)}^{2}+2(x - 2)-2)
y=\operatorname{ln}⁡({(x - 2)}^{4}-(x - 2)+1)
y=\operatorname{ln}⁡({(x - 2)}^{4}-(x - 2))

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+{e}^{-y} & =4{(x - 2)}^{3}{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =4{(x - 2)}^{3}{e}^{-y}-{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =(4{(x - 2)}^{3}-1){e}^{-y} \\ {e}^{y}\frac{\text{d}y}{\text{d}x} & =4{(x - 2)}^{3}-1 \\ \int {e}^{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (4{(x - 2)}^{3}-1)\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (4{(x - 2)}^{3}-1)\,\text{d}x \\ {e}^{y} & ={(x - 2)}^{4}-(x - 2)+C.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡({(x - 2)}^{4}-(x - 2)+C) \\ y & =\operatorname{ln}⁡({(x - 2)}^{4}-(x - 2)+C)\end{aligned}
$$

We now apply the initial condition $y(3)=0$ to find $C:$

$$
\begin{aligned}y(3) & =0 \\ \operatorname{ln}⁡({1}^{4}-1+C) & =0 \\ \operatorname{ln}⁡C & =0 \\ C & =1\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}+{e}^{-y}=4{(x - 2)}^{3}{e}^{-y}$ that satisfies the condition $y(3)=0$ is

$$
y=\operatorname{ln}⁡({(x - 2)}^{4}-(x - 2)+1).
$$

---

Source q-79425

Find the particular solution to the differential equation $3{y}^{2}\frac{\text{d}y}{\text{d}x}-2x{y}^{3}=4x$ that satisfies $y(0)=1.$  Assume that $y>0.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}3{y}^{2}\frac{\text{d}y}{\text{d}x}-2x{y}^{3} & =4x \\ 3{y}^{2}\frac{\text{d}y}{\text{d}x} & =2x(2+{y}^{3}) \\ \frac{3{y}^{2}}{2+{y}^{3}}\frac{\text{d}y}{\text{d}x} & =2x \\ \int \frac{3{y}^{2}}{2+{y}^{3}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int \frac{3{y}^{2}}{2+{y}^{3}}\,\text{d}y & ={x}^{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral on the left-hand side of this equality, we use a substitution

$$
u=2+{y}^{3}\,⟹\,\text{d}u=3{y}^{2}\,\text{d}y.
$$

Then  we have

$$
\begin{aligned}\int \frac{3{y}^{2}}{2+{y}^{3}}\text{d}y & =\int \frac{1}{2+{y}^{3}}(3{y}^{2}\,\text{d}y) \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+{C}_{2} \\  & =\operatorname{ln}⁡(2+{y}^{3})+{C}_{2},\end{aligned}
$$

where we used that $y>0.$

Hence,

$$
\begin{aligned}\operatorname{ln}⁡(2+{y}^{3})+{C}_{2} & ={x}^{2}+{C}_{1} \\ \operatorname{ln}⁡(2+{y}^{3}) & ={x}^{2}+{C}_{1}-{C}_{2} \\ {e}^{\operatorname{ln}⁡(2+{y}^{3})} & ={e}^{{x}^{2}+{C}_{1}-{C}_{2}} \\ 2+{y}^{3} & =K{e}^{{x}^{2}} \\ {y}^{3} & =K{e}^{{x}^{2}}-2,\end{aligned}
$$

where $K=\pm {e}^{{C}_{1}-{C}_{2}}$ is an arbitrary constant. 

We now apply the initial condition $y(0)=1$ to find $K:$

$$
\begin{aligned}{1}^{3} & =K{e}^{{0}^{2}}-2 \\ 1 & =K-2 \\ K & =3\,.\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{y}^{3}=3{e}^{{x}^{2}}-2.
$$

Variant

Find the particular solution to the differential equation $3{y}^{2}\frac{\text{d}y}{\text{d}x}-2(x - 2){y}^{3}=4(x - 2)$ that satisfies $y(2)=1.$  Assume that $y>0.$

{y}^{2}=3{e}^{(x - 2)}-2
{y}^{2}=2{e}^{{(x - 2)}^{2}}-1
y=2{e}^{(x - 2)}-1
{y}^{3}={e}^{{(x - 2)}^{2}}
{y}^{3}=3{e}^{{(x - 2)}^{2}}-2

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}3{y}^{2}\frac{\text{d}y}{\text{d}x}-2(x - 2){y}^{3} & =4(x - 2) \\ 3{y}^{2}\frac{\text{d}y}{\text{d}x} & =2(x - 2)(2+{y}^{3}) \\ \frac{3{y}^{2}}{2+{y}^{3}}\frac{\text{d}y}{\text{d}x} & =2(x - 2) \\ \int \frac{3{y}^{2}}{2+{y}^{3}}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2(x - 2)\,\text{d}x \\ \int \frac{3{y}^{2}}{2+{y}^{3}}\,\text{d}y & ={(x - 2)}^{2}+{C}_{1}.\end{aligned}
$$

To calculate the integral on the left-hand side of this equality, we use a substitution

$$
u=2+{y}^{3}\,⟹\,\text{d}u=3{y}^{2}\,\text{d}y.
$$

Then  we have

$$
\begin{aligned}\int \frac{3{y}^{2}}{2+{y}^{3}}\text{d}y & =\int \frac{1}{2+{y}^{3}}(3{y}^{2}\,\text{d}y) \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+{C}_{2} \\  & =\operatorname{ln}⁡(2+{y}^{3})+{C}_{2},\end{aligned}
$$

where we used that $y>0.$

Hence,

$$
\begin{aligned}\operatorname{ln}⁡(2+{y}^{3})+{C}_{2} & ={(x - 2)}^{2}+{C}_{1} \\ \operatorname{ln}⁡(2+{y}^{3}) & ={(x - 2)}^{2}+{C}_{1}-{C}_{2} \\ {e}^{\operatorname{ln}⁡(2+{y}^{3})} & ={e}^{{(x - 2)}^{2}+{C}_{1}-{C}_{2}} \\ 2+{y}^{3} & =K{e}^{{(x - 2)}^{2}} \\ {y}^{3} & =K{e}^{{(x - 2)}^{2}}-2,\end{aligned}
$$

where $K={e}^{{C}_{1}-{C}_{2}}$ is an arbitrary constant. 

We now apply the initial condition $y(2)=1$ to find $K:$

$$
\begin{aligned}{1}^{3} & =K{e}^{{0}^{2}}-2 \\ 1 & =K-2 \\ K & =3\,.\end{aligned}
$$

So we get the particular solution in implicit form:

$$
{y}^{3}=3{e}^{{(x - 2)}^{2}}-2.
$$

---

Source q-355560

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{4{y}^{2}}{{x}^{2}}+{y}^{2}$ that satisfies $y(2)=-1.$

|  | $y(x)=$ | $x$ |
| --- | --- | --- |
|  |  | {{field-1}} |

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4{y}^{2}}{{x}^{2}}+{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(\frac{4}{{x}^{2}}+1) \\ \frac{1}{{y}^{2}}\,\text{d}y & =(4{x}^{-2}+1)\,\text{d}x \\ \int {y}^{-2}\,\text{d}y & =\int (4{x}^{-2}+1)\,\text{d}x \\ -{y}^{-1} & =-4{x}^{-1}+x+C \\ -\frac{1}{y} & =-\frac{4}{x}+x+C\end{aligned}
$$

Solving for $y$, we find the general solution:

$$
\begin{aligned}\frac{1}{y} & =\frac{4}{x}-x-C \\ \frac{1}{y} & =\frac{4-{x}^{2}-Cx}{x} \\ y & =\frac{x}{4-{x}^{2}-Cx}\end{aligned}
$$

We now apply the initial condition $y(2)=-1$ to find $C:$

$$
\begin{aligned}y(2) & =-1 \\ \frac{2}{4-{2}^{2}-C(2)} & =-1 \\ \frac{2}{-2C} & =-1 \\ -\frac{1}{C} & =-1 \\ C & =1\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\frac{x}{4-x-{x}^{2}}.
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{4{y}^{2}}{{(x - 2)}^{2}}+{y}^{2}$ that satisfies $y(4)=-1.$

$y(x)=\frac{(x - 2)}{\boxed{\text{denominator}}}$

Denominator: {{field-1}}

4-(x - 2)-{(x - 2)}^{2}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4{y}^{2}}{{(x - 2)}^{2}}+{y}^{2} \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}(\frac{4}{{(x - 2)}^{2}}+1) \\ \frac{1}{{y}^{2}}\,\text{d}y & =(4{(x - 2)}^{-2}+1)\,\text{d}x \\ \int {y}^{-2}\,\text{d}y & =\int (4{(x - 2)}^{-2}+1)\,\text{d}x \\ -{y}^{-1} & =-4{(x - 2)}^{-1}+(x - 2)+C \\ -\frac{1}{y} & =-\frac{4}{(x - 2)}+(x - 2)+C\end{aligned}
$$

Solving for $y$, we find the general solution:

$$
\begin{aligned}\frac{1}{y} & =\frac{4}{(x - 2)}-(x - 2)-C \\ \frac{1}{y} & =\frac{4-{(x - 2)}^{2}-C(x - 2)}{(x - 2)} \\ y & =\frac{(x - 2)}{4-{(x - 2)}^{2}-C(x - 2)}\end{aligned}
$$

We now apply the initial condition $y(4)=-1$ to find $C:$

$$
\begin{aligned}y(4) & =-1 \\ \frac{2}{4-{2}^{2}-C(2)} & =-1 \\ \frac{2}{-2C} & =-1 \\ -\frac{1}{C} & =-1 \\ C & =1\end{aligned}
$$

Thus, the particular solution is

$$
y(x)=\frac{(x - 2)}{4-(x - 2)-{(x - 2)}^{2}}.
$$

---

Source q-104056

Find the particular solution to the differential equation ${e}^{x}\frac{\text{d}y}{\text{d}x}+4x{e}^{x}=1$ that satisfies $y(0)=7.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{e}^{x}\frac{\text{d}y}{\text{d}x}+4x{e}^{x} & =1 \\ {e}^{x}\frac{\text{d}y}{\text{d}x} & =1-4x{e}^{x} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{-x}-4x \\ \int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int ({e}^{-x}-4x)\,\text{d}x \\ \int \,\text{d}y & =\int {e}^{-x}\,\text{d}x-4\int x\,\text{d}x \\ y & =-{e}^{-x}-2{x}^{2}+C.\end{aligned}
$$

We now apply the initial condition $y(0)=7$ to find $C:$

$$
\begin{aligned}y(0) & =7 \\ -{e}^{-0}+2\cdot {0}^{2}+C & =7 \\ C-1 & =7 \\ C & =8\,.\end{aligned}
$$

Thus the particular solution of ${e}^{x}\frac{\text{d}y}{\text{d}x}+4x{e}^{x}=1$ that satisfies the condition $y(0)=7$ is

$$
y=-{e}^{-x}-2{x}^{2}+8.
$$

Variant

Find the particular solution to the differential equation ${e}^{(x - 2)}\frac{\text{d}y}{\text{d}x}+4(x - 2){e}^{(x - 2)}=1$ that satisfies $y(2)=7.$

y=-{e}^{-(x - 2)}-4(x - 2)+8
y={e}^{-(x - 2)}-2{(x - 2)}^{2}+6
y={e}^{(x - 2)}-4{(x - 2)}^{2}+6
y={e}^{(x - 2)}-2{(x - 2)}^{2}+6
y=-{e}^{-(x - 2)}-2{(x - 2)}^{2}+8

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}{e}^{(x - 2)}\frac{\text{d}y}{\text{d}x}+4(x - 2){e}^{(x - 2)} & =1 \\ {e}^{(x - 2)}\frac{\text{d}y}{\text{d}x} & =1-4(x - 2){e}^{(x - 2)} \\ \frac{\text{d}y}{\text{d}x} & ={e}^{-(x - 2)}-4(x - 2) \\ \int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int ({e}^{-(x - 2)}-4(x - 2))\,\text{d}x \\ \int \,\text{d}y & =\int {e}^{-(x - 2)}\,\text{d}x-4\int (x - 2)\,\text{d}x \\ y & =-{e}^{-(x - 2)}-2{(x - 2)}^{2}+C.\end{aligned}
$$

We now apply the initial condition $y(2)=7$ to find $C:$

$$
\begin{aligned}y(2) & =7 \\ -{e}^{-0}-2\cdot {0}^{2}+C & =7 \\ C-1 & =7 \\ C & =8\,.\end{aligned}
$$

Thus the particular solution of ${e}^{(x - 2)}\frac{\text{d}y}{\text{d}x}+4(x - 2){e}^{(x - 2)}=1$ that satisfies the condition $y(2)=7$ is

$$
y=-{e}^{-(x - 2)}-2{(x - 2)}^{2}+8.
$$

---

Source q-104057

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+2x{e}^{-y}=3{x}^{2}{e}^{-y}$ that satisfies $y(1)=1.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+2x{e}^{-y} & =3{x}^{2}{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =3{x}^{2}{e}^{-y}-2x{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =(3{x}^{2}-2x){e}^{-y} \\ {e}^{y}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}-2x \\ \int {e}^{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{x}^{2}-2x)\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (3{x}^{2}-2x)\,\text{d}x \\ {e}^{y} & ={x}^{3}-{x}^{2}+C.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡({x}^{3}-{x}^{2}+C) \\ y & =\operatorname{ln}⁡({x}^{3}-{x}^{2}+C)\end{aligned}
$$

We now apply the initial condition $y(1)=1$ to find $C:$

$$
\begin{aligned}y(1) & =1 \\ \operatorname{ln}⁡({1}^{3}-{1}^{2}+C) & =1 \\ \operatorname{ln}⁡C & =1 \\ C & =e\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}+2x{e}^{-y}=3{x}^{2}{e}^{-y}$ that satisfies the condition $y(1)=1$ is

$$
y=\operatorname{ln}⁡({x}^{3}-{x}^{2}+e).
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}+2(x - 2){e}^{-y}=3{(x - 2)}^{2}{e}^{-y}$ that satisfies $y(3)=1.$

y=\operatorname{ln}⁡({(x - 2)}^{3}-{(x - 2)}^{2})
y=\operatorname{ln}⁡({(x - 2)}^{3}-{(x - 2)}^{2}+e)
y=\operatorname{ln}⁡(\frac{{(x - 2)}^{3}-{(x - 2)}^{2}+2e}{2})
y=\operatorname{ln}⁡({(x - 2)}^{2}+2(x - 2)-3+e)
y=\operatorname{ln}⁡(\frac{e{(x - 2)}^{2}+e}{2})

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}+2(x - 2){e}^{-y} & =3{(x - 2)}^{2}{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =3{(x - 2)}^{2}{e}^{-y}-2(x - 2){e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =(3{(x - 2)}^{2}-2(x - 2)){e}^{-y} \\ {e}^{y}\frac{\text{d}y}{\text{d}x} & =3{(x - 2)}^{2}-2(x - 2) \\ \int {e}^{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (3{(x - 2)}^{2}-2(x - 2))\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (3{(x - 2)}^{2}-2(x - 2))\,\text{d}x \\ {e}^{y} & ={(x - 2)}^{3}-{(x - 2)}^{2}+C.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}\operatorname{ln}⁡({e}^{y}) & =\operatorname{ln}⁡({(x - 2)}^{3}-{(x - 2)}^{2}+C) \\ y & =\operatorname{ln}⁡({(x - 2)}^{3}-{(x - 2)}^{2}+C)\end{aligned}
$$

We now apply the initial condition $y(3)=1$ to find $C:$

$$
\begin{aligned}y(3) & =1 \\ \operatorname{ln}⁡({1}^{3}-{1}^{2}+C) & =1 \\ \operatorname{ln}⁡C & =1 \\ C & =e\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}+2(x - 2){e}^{-y}=3{(x - 2)}^{2}{e}^{-y}$ that satisfies the condition $y(3)=1$ is

$$
y=\operatorname{ln}⁡({(x - 2)}^{3}-{(x - 2)}^{2}+e).
$$

---

Source q-8306

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=2yx+y{x}^{2}$ that satisfies $y(1)=1.$

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2yx+y{x}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(2x+{x}^{2}) \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =2x+{x}^{2} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2x+{x}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =2\int x\,\text{d}x+\int {x}^{2}\,\text{d}x \\ \operatorname{ln}⁡|y| & ={x}^{2}+\frac{{x}^{3}}{3}+C.\end{aligned}
$$

Applying the natural logarithm to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{x}^{2}+{x}^{3}/3+C} \\ |y| & ={e}^{{x}^{2}+{x}^{3}/3+C} \\ y & =\pm {e}^{{x}^{2}+{x}^{3}/3+C} \\ y & =K{e}^{{x}^{2}+{x}^{3}/3},\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the initial condition $y(1)=1$ to find $K:$

$$
\begin{aligned}y(1) & =1 \\ K{e}^{{1}^{2}+{1}^{3}/3} & =1 \\ K{e}^{4/3} & =1 \\ K & ={e}^{-4/3}\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}=2yx+y{x}^{2}$ that satisfies the condition $y(1)=1$ is

$$
y={e}^{-4/3}\cdot {e}^{{x}^{2}+{x}^{3}/3}={e}^{({x}^{3}+3{x}^{2}-4)/3}\,.
$$

Variant

Find the particular solution to the differential equation $\frac{\text{d}y}{\text{d}x}=2y(x - 2)+y{(x - 2)}^{2}$ that satisfies $y(3)=1.$

y={e}^{3{(x - 2)}^{3}+{(x - 2)}^{2}-1}
y={e}^{({(x - 2)}^{3}+{(x - 2)}^{2}-2)/3}
y={e}^{(2{(x - 2)}^{3}+{(x - 2)}^{2}-1)/3}
y={e}^{{(x - 2)}^{3}+4{(x - 2)}^{2}-5}
y={e}^{({(x - 2)}^{3}+3{(x - 2)}^{2}-4)/3}

We first find the general solution and then apply the given initial condition to find a particular solution.

Separating variables and integrating both sides with respect to $x,$ we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2y(x - 2)+y{(x - 2)}^{2} \\ \frac{\text{d}y}{\text{d}x} & =y(x^{2} + 2 x + 2) \\ \frac{1}{y}\frac{\text{d}y}{\text{d}x} & =2(x - 2)+{(x - 2)}^{2} \\ \int \frac{1}{y}\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2(x - 2)+{(x - 2)}^{2})\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =2\int (x - 2)\,\text{d}x+\int {(x - 2)}^{2}\,\text{d}x \\ \operatorname{ln}⁡|y| & ={(x - 2)}^{2}+\frac{{(x - 2)}^{3}}{3}+C.\end{aligned}
$$

Applying the exponential function to both sides, we find the general solution:

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{(x - 2)}^{2}+{(x - 2)}^{3}/3+C} \\ |y| & ={e}^{{(x - 2)}^{2}+{(x - 2)}^{3}/3+C} \\ y & =\pm {e}^{{(x - 2)}^{2}+{(x - 2)}^{3}/3+C} \\ y & =K{e}^{{(x - 2)}^{2}+{(x - 2)}^{3}/3},\end{aligned}
$$

where $K=\pm {e}^{C}$ is an arbitrary constant. 

We now apply the initial condition $y(3)=1$ to find $K:$

$$
\begin{aligned}y(3) & =1 \\ K{e}^{{1}^{2}+{1}^{3}/3} & =1 \\ K{e}^{4/3} & =1 \\ K & ={e}^{-4/3}\,.\end{aligned}
$$

Thus the particular solution of $\frac{\text{d}y}{\text{d}x}=2y(x - 2)+y{(x - 2)}^{2}$ that satisfies the condition $y(3)=1$ is

$$
y={e}^{-4/3}\cdot {e}^{{(x - 2)}^{2}+{(x - 2)}^{3}/3}={e}^{({(x - 2)}^{3}+3{(x - 2)}^{2}-4)/3}\,.
$$