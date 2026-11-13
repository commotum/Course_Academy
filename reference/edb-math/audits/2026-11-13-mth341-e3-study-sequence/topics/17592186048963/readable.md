# 17592186048963 Solving Perfect Square Quadratic Equations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186111918 — Introduction

Suppose that we want to solve the following quadratic equation:

$$
(x+1)^2 = 4
$$

Notice that the left-hand side is a perfect square and the right-hand side is a constant:

$$
\underbrace{(x+1)^2}_{\large\color{blue}\textrm{perfect square}} = \overbrace{\!\!\!\!\!4\!\!\!\!\!}^{\large\color{red}\textrm{constant}} \!\!\!\!\!
$$

In this case, we can solve the equation using the square root method. First, we take the square root of both sides:

$$
\begin{aligned}
(x + 1)^{2} &= 4 \\
\sqrt{(x + 1)^{2}} &= \sqrt{4} \\
\mid x + 1 \mid &= 2
\end{aligned}
$$

Then, we solve the resulting absolute value equation:

$$
\begin{aligned}
\mid x + 1 \mid &= 2 \\
x + 1 &= ± 2 \\
x &= -1 ± 2
\end{aligned}
$$

Finally, we simplify the two solutions:

$$
\begin{aligned}
x &= -1 + 2 = 1 \\
x &= -1 - 2 =-3
\end{aligned}
$$

Therefore, the solutions are $x=-3$ and $x=1$.



### example 17592186110344 — Equations Where the Perfect Square is Isolated

Solve $(3y +2)^2 = 4$.

We solve the equation using the square root method:

$$
\begin{aligned}
(3y + 2)^{2} &= 4 \\
\sqrt{(3y + 2)^{2}} &= \sqrt{4} \\
\mid 3y + 2 \mid &= 2 \\
3y + 2 &= ± 2 \\
3y &= -2 ± 2 \\
y &= \frac{-2 ± 2}{3}
\end{aligned}
$$

Next, we simplify the two solutions:

$$
\begin{aligned}
y &= \frac{-2 + 2}{3} = 0 \\
y &= \frac{-2 - 2}{3} =-\frac{4}{3}
\end{aligned}
$$

Therefore, the solutions are

$$
y=-\dfrac{4}{3}
$$

and $y=0$.

### example 17592186110345 — Equations Where the Perfect Square Is Not Isolated

If $-2(3x - 6)^2 + 1 = -9$, then calculate $x$.

First, we isolate the perfect square:

$$
\begin{aligned}
-2(3x - 6)^{2} + 1 &= -9 \\
- 2(3x - 6)^{2} &= -10 \\
(3x - 6)^{2} &= 5
\end{aligned}
$$

Then, we solve the equation using the square root method:

$$
\begin{aligned}
\sqrt{(3x - 6)^{2}} &= \sqrt{5} \\
\mid 3x - 6 \mid &= \sqrt{5} \\
3x - 6 &= ± \sqrt{5} \\
3x &= 6 ± \sqrt{5} \\
x &= \frac{6 ± \sqrt{5}}{3} \\
x &= \frac{6}{3} ± \frac{\sqrt{5}}{3} \\
x &= 2 ± \frac{\sqrt{5}}{3}
\end{aligned}
$$

The two solutions are

$$
x= 2 + \dfrac{\sqrt{5}}{3}\quad \textrm{and}\quad x= 2 - \dfrac{\sqrt{5}}{3}
$$

However, because these solutions cannot be simplified any further, we will keep the "$\pm$" symbol in our final answer. So our final answer is

$$
x = 2 \pm \dfrac{\sqrt{5}}{3}
$$

### example 17592186110347 — Solving Equations by Factoring

Given that $t^2 -10t +25 = 121$, what are the values of $t$?

First, notice that the left-hand side is a perfect square. It just needs to be factored:

$$
\begin{aligned}
t^{2} - 10t + 25 &= 121 \\
t^{2} - 2 \cdot 5 \cdot t + 5^{2} &= 121 \\
(t - 5)^{2} &= 121
\end{aligned}
$$

From here, we solve the equation using the square root method:

$$
\begin{aligned}
\sqrt{(t - 5)^{2}} &= \sqrt{121} \\
\mid t - 5 \mid &= 11 \\
t - 5 &= ± 11 \\
t &= 5 ± 11
\end{aligned}
$$

Next, we simplify the two solutions:

$$
\begin{aligned}
t &= 5 + 11 = 16 \\
t &= 5 - 11 =-6
\end{aligned}
$$

Therefore, the solutions are $t=-6$ and $t=16$.

## Representative practice (first three per skill; full bank in practice.json)

### Equations Where the Perfect Square is Isolated (18 captured questions)

Question 17592186110960 — None

In **ascending order**, the solutions to $(4y - 3)^{2} = 25$ are$y =$ {{field-1}}
and
$y =$ {{field-2}}.

Solution: 

Question 17592186111157 — None

Solve $(y - 2)^{2} = 49$.

Solution: 

Question 17592186683901 — question.difficulty/moderate

In **ascending order**, the solutions to $(3y-2)^2=16$ are

$y=$ {{field-1}} and $y=$ {{field-2}}.

Solution: Take square roots before undoing the operations inside the square. Since $\sqrt{(3y-2)^2}=\lvert3y-2\rvert$, there are two branches:

$$
\begin{aligned}
(3y-2)^2&=16\\
\lvert3y-2\rvert&=4\\
3y-2&=\pm4\\
3y&=2\pm4\\
y&=\frac{2\pm4}{3}.
\end{aligned}
$$

Evaluate each branch:

$$
y=\frac{2-4}{3}=-\frac{2}{3}\qquad\text{or}\qquad y=\frac{2+4}{3}=2.
$$

The solutions in ascending order are $-\frac{2}{3}$ and $2$. Substitution gives inner values $-4$ and $4$, respectively, and each squares to $16$.

Answer field-1: -\frac{2}{3}

Answer field-2: 2

### Equations Where the Perfect Square Is Not Isolated (20 captured questions)

Question 17592186110970 — None

In **ascending order**, the solutions to $3(2y + 3)^{2} - 5 = 70$ are$y =$ {{field-1}}
and
$y =$ {{field-2}}.

Solution: 

Question 17592186111156 — None

If $2(y + 3)^{2} = 32$, then calculate $y$.

Solution: 

Question 17592186235497 — question.difficulty/moderate

![](images/ae/ae44c9f19c7afc26c399999105b7d17c6e2e6b3e020e7b419065a8514741dc9b.png)

 

Consider a circle with radius $3$ centered at the point $(3,0),$ shown above.

Write the equations of the upper and lower semicircles.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
Upper: $\,\,\,y=$

                                    
                                
                                    
                            
{{field-1}}                
                                    
                                
                                    
                                        
                                                

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
Lower: $\,\,\,y=$

                                    
                                
                                    
                            
{{field-2}}

Solution: We make $y$ the subject of the equation, as follows:

$$
\begin{aligned}(x-3)^{2}+{y}^{2} & =9 \\ {y}^{2} & =9-(x-3)^{2} \\ \sqrt{{y}^{2}} & =\sqrt{9-(x-3)^{2}} \\ |y| & =\sqrt{9-({x}^{2}-6x+9)} \\ y & =\pm \sqrt{6x-{x}^{2}}\end{aligned}
$$

 

Therefore,

* the equation with the positive square root, $y=\sqrt{6x-{x}^{2}}$, describes the upper semicircle, and 

* the equation with the negative square root, $y=-\sqrt{6x-{x}^{2}}$, describes the lower semicircle.

Answer field-1: \sqrt{6x-{x}^{2}}

Answer field-2: -\sqrt{6x-{x}^{2}}

### Solving Equations by Factoring (3 captured questions)

Question 17592186110961 — None

In **ascending order**, the solutions to $25x^{2} + 20x + 4 = 1$ are$x =$ {{field-1}}
and
$x =$ {{field-2}}.

Solution: 

Question 17592186110971 — None

In **ascending order**, the solutions to $36x^{2} - 24x + 4 = 20$ are$x =$ {{field-1}}
and
$x =$ {{field-2}}.

Solution: 

Question 17592186111234 — None

Given that $y^{2} - 6y + 9 = 4$, what are the values of $y$?

Solution: 
