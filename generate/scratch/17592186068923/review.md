## source q-49761

Evaluate
${\int }_{2}^{3}\frac{3x+4}{{x}^{2}-16}\text{d}x.$

- $\operatorname{ln}(\frac{7}{36})$
- $\operatorname{ln}(\frac{7}{24})$ (correct)
- $\operatorname{ln}(168)$
- $\operatorname{ln}(17)$
- $\operatorname{ln}(\frac{7}{32})$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
{x}^{2}-16=(x+4)(x-4).
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{3x+4}{{x}^{2}-16} & =\frac{3x+4}{(x+4)(x-4)}=\frac{A}{(x+4)}+\frac{B}{(x-4)},\end{aligned}
$$

which gives

$$
3x+4=A(x-4)+B(x+4).
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}3(4)+4 & =A(4-4)+B(4+4) \\ 16 & =8B \\ B & =2\end{aligned}
$$

On the other hand, plugging in $x=-4,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}3(-4)+4 & =A(-4-4)+B(-4+4) \\ -8 & =-8A \\ A & =1\end{aligned}
$$

Therefore,

$$
\frac{3x+4}{{x}^{2}-16}=\frac{1}{(x+4)}+\frac{2}{(x-4)}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{3x+4}{{x}^{2}-16}\,\text{d}x & =\int (\frac{1}{(x+4)}+\frac{2}{(x-4)})\,\text{d}x \\  & =\int \frac{1}{x+4}\,\text{d}x+2\int \frac{1}{x-4}\,\text{d}x \\  & =\operatorname{ln}⁡|x+4|+2\operatorname{ln}⁡|x-4|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{3x+4}{{x}^{2}-16}\,\text{d}x & =\operatorname{ln}⁡|x+4|+2\operatorname{ln}⁡|x-4|+C \\  & =\operatorname{ln}⁡|x+4|+\operatorname{ln}⁡|(x-4)^{2}|+C \\  & =\operatorname{ln}⁡|(x+4)(x-4)^{2}|+C\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{2}^{3}\frac{3x+4}{{x}^{2}-16}\,\text{d}x & =\operatorname{ln}⁡|(x+4)(x-4)^{2}|{|}_{2}^{3} \\  & =\operatorname{ln}⁡(7)-\operatorname{ln}⁡(24) \\  & =\operatorname{ln}⁡(\frac{7}{24}).\end{aligned}
$$

## variant q-49761

Evaluate
${\int }_{2}^{3}\frac{6 x + 8}{x^{2} - 16}\,\text{d}x.$

- $- 4 \ln{\left(6 \right)} + 2 \ln{\left(7 \right)}$
- $- 2 \ln{\left(24 \right)} + 2 \ln{\left(7 \right)}$ (correct)
- $2 \ln{\left(168 \right)}$
- $2 \ln{\left(17 \right)}$
- $- 10 \ln{\left(2 \right)} + 2 \ln{\left(7 \right)}$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
x^{2} - 16=(x + 4)(x - 4)
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{6 x + 8}{x^{2} - 16} &= \frac{6 x + 8}{(x + 4)(x - 4)}=\frac{A}{x + 4}+\frac{B}{x - 4}\end{aligned}
$$

which gives

$$
6 x + 8=A(x - 4)+B(x + 4)
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}32 &= 8B \\ B &= 4\end{aligned}
$$

On the other hand, plugging in $x=-4,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}-16 &= -8A \\ A &= 2\end{aligned}
$$

Therefore,

$$
\frac{6 x + 8}{x^{2} - 16}=\frac{2}{x + 4} + \frac{4}{x - 4}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{6 x + 8}{x^{2} - 16}\,\text{d}x &= \int (\frac{2}{x + 4} + \frac{4}{x - 4})\,\text{d}x \\ &= 2\ln|x + 4|+4\ln|x - 4|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}2\ln|x + 4|+4\ln|x - 4|+C &= 1\ln|\left(x - 4\right)^{4} \left(x + 4\right)^{2}|+C\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{2}^{3}\frac{6 x + 8}{x^{2} - 16}\,\text{d}x &= [2\ln|x + 4|+4\ln|x - 4|]_{2}^{3} \\ &= (2 \ln{\left(7 \right)})-(4 \ln{\left(2 \right)} + 2 \ln{\left(6 \right)}) \\ &= - 2 \ln{\left(6 \right)} - 4 \ln{\left(2 \right)} + 2 \ln{\left(7 \right)}\end{aligned}
$$

## source q-49766

What is $\displaystyle \int_{4}^{7}(2x + 2)/((x - 3)(x + 5))dx$?

- $\ln (\frac{3}{4})$
- $\ln (\frac{20}{3})$
- $\ln (\frac{1}{4})$
- $\ln (\frac{32}{3})$
- $\ln (\frac{16}{3})$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2 x + 2}{(x - 3)(x + 5)} &= \frac{2 x + 2}{(x - 3)(x + 5)}=\frac{A}{x - 3}+\frac{B}{x + 5}\end{aligned}
$$

which gives

$$
2 x + 2=A(x + 5)+B(x - 3)
$$

Plugging in $x=-5,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}-8 &= -8B \\ B &= 1\end{aligned}
$$

On the other hand, plugging in $x=3,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}8 &= 8A \\ A &= 1\end{aligned}
$$

Therefore,

$$
\frac{2 x + 2}{(x - 3)(x + 5)}=\frac{1}{x + 5} + \frac{1}{x - 3}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{2 x + 2}{(x - 3)(x + 5)}\,\text{d}x &= \int (\frac{1}{x + 5} + \frac{1}{x - 3})\,\text{d}x \\ &= 1\ln|x - 3|+1\ln|x + 5|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}1\ln|x - 3|+1\ln|x + 5|+C &= 1\ln|\left(x - 3\right) \left(x + 5\right)|+C\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{4}^{7}\frac{2 x + 2}{(x - 3)(x + 5)}\,\text{d}x &= [1\ln|x - 3|+1\ln|x + 5|]_{4}^{7} \\ &= (\ln{\left(4 \right)} + \ln{\left(12 \right)})-(\ln{\left(9 \right)}) \\ &= - 2 \ln{\left(3 \right)} + 2 \ln{\left(2 \right)} + \ln{\left(12 \right)}\end{aligned}
$$

## variant q-49766

What is $\displaystyle {\int }_{4}^{7}\frac{4 x + 4}{(x - 3)(x + 5)}\,\text{d}x$?

- $- 4 \ln{\left(2 \right)} + 2 \ln{\left(3 \right)}$
- $- 2 \ln{\left(3 \right)} + 2 \ln{\left(20 \right)}$
- $- 4 \ln{\left(2 \right)}$
- $- 2 \ln{\left(3 \right)} + 10 \ln{\left(2 \right)}$
- $- 2 \ln{\left(3 \right)} + 8 \ln{\left(2 \right)}$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{4 x + 4}{(x - 3)(x + 5)} &= \frac{4 x + 4}{(x - 3)(x + 5)}=\frac{A}{x - 3}+\frac{B}{x + 5}\end{aligned}
$$

which gives

$$
4 x + 4=A(x + 5)+B(x - 3)
$$

Plugging in $x=-5,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}-16 &= -8B \\ B &= 2\end{aligned}
$$

On the other hand, plugging in $x=3,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}16 &= 8A \\ A &= 2\end{aligned}
$$

Therefore,

$$
\frac{4 x + 4}{(x - 3)(x + 5)}=\frac{2}{x + 5} + \frac{2}{x - 3}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{4 x + 4}{(x - 3)(x + 5)}\,\text{d}x &= \int (\frac{2}{x + 5} + \frac{2}{x - 3})\,\text{d}x \\ &= 2\ln|x - 3|+2\ln|x + 5|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}2\ln|x - 3|+2\ln|x + 5|+C &= 1\ln|\left(x - 3\right)^{2} \left(x + 5\right)^{2}|+C\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{4}^{7}\frac{4 x + 4}{(x - 3)(x + 5)}\,\text{d}x &= [2\ln|x - 3|+2\ln|x + 5|]_{4}^{7} \\ &= (2 \ln{\left(4 \right)} + 2 \ln{\left(12 \right)})-(2 \ln{\left(9 \right)}) \\ &= - 4 \ln{\left(3 \right)} + 4 \ln{\left(2 \right)} + 2 \ln{\left(12 \right)}\end{aligned}
$$

## source q-128238

Find the value of ${\int }_{-5}^{-4}\frac{x-2}{(x+3)(x+1)}\text{d}x.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        ${\int }_{-5}^{-4}\frac{x-2}{(x+3)(x+1)}\text{d}x=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $\frac{1}{2}\operatorname{ln}(\frac{2}{27})$ (correct)

Previously, we found that 

$$
\frac{x-2}{(x+3)(x+1)}=\frac{5}{2(x+3)}-\frac{3}{2(x+1)}.
$$

Now, we can integrate, as follows:

$$
\begin{aligned}\int \frac{x-2}{(x+3)(x+1)}\,\text{d}x & =\int (\frac{5}{2(x+3)}-\frac{3}{2(x+1)})\text{d}x \\  & =\frac{5}{2}\int \frac{1}{x+3}\,\text{d}x-\frac{3}{2}\int \frac{1}{x+1}\,\text{d}x \\  & =\frac{5}{2}\operatorname{ln}⁡|x+3|-\frac{3}{2}\operatorname{ln}⁡|x+1|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms:

$$
\begin{aligned}\frac{5}{2}\operatorname{ln}⁡|x+3|-\frac{3}{2}\operatorname{ln}⁡|x+1|+C & =\frac{1}{2}(5\operatorname{ln}⁡|x+3|-3\operatorname{ln}⁡|x+1|)+C \\  & =\frac{1}{2}(\operatorname{ln}⁡|x+3{|}^{5}-\operatorname{ln}⁡|x+1{|}^{3})+C \\  & =\frac{1}{2}\operatorname{ln}⁡|\frac{(x+3)^{5}}{(x+1)^{3}}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-5}^{-4}\frac{x-2}{(x+3)(x+1)}\,\text{d}x & ={[\frac{1}{2}\operatorname{ln}⁡|\frac{(x+3)^{5}}{(x+1)^{3}}|]}_{-5}^{-4} \\  & =\frac{1}{2}\operatorname{ln}⁡(\frac{1}{{3}^{3}})-\frac{1}{2}\operatorname{ln}⁡(\frac{{2}^{5}}{{4}^{3}}) \\  & =\frac{1}{2}\operatorname{ln}⁡(\frac{{4}^{3}}{{2}^{5}\cdot {3}^{3}}) \\  & =\frac{1}{2}\operatorname{ln}⁡(\frac{2}{27}).\end{aligned}
$$

## variant q-128238

Find the value of ${\int }_{-5}^{-4}\frac{2 x - 4}{(x + 3)(x + 1)}\,\text{d}x.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        ${\int }_{-5}^{-4}\frac{2 x - 4}{(x + 3)(x + 1)}\,\text{d}x=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $- 3 \ln{\left(3 \right)} + \ln{\left(2 \right)}$ (correct)

Previously, we found that 

$$
\frac{2 x - 4}{(x + 3)(x + 1)}=\frac{5}{x + 3} - \frac{3}{x + 1}
$$

Now, we can integrate, as follows:

$$
\begin{aligned}{\int }\frac{2 x - 4}{(x + 3)(x + 1)}\,\text{d}x &= \int (\frac{5}{x + 3} - \frac{3}{x + 1})\,\text{d}x \\ &= 5\ln|x + 3|-3\ln|x + 1|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms:

$$
\begin{aligned}5\ln|x + 3|-3\ln|x + 1|+C &= 1\ln|\frac{\left(x + 3\right)^{5}}{\left(x + 1\right)^{3}}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-5}^{-4}\frac{2 x - 4}{(x + 3)(x + 1)}\,\text{d}x &= [5\ln|x + 3|-3\ln|x + 1|]_{-5}^{-4} \\ &= (- 3 \ln{\left(3 \right)})-(- 3 \ln{\left(4 \right)} + 5 \ln{\left(2 \right)}) \\ &= - 3 \ln{\left(3 \right)} + \ln{\left(2 \right)}\end{aligned}
$$

## source q-347077

Evaluate the following integral. Do not round the answer.

${\int }_{3}^{6}\frac{2x+2}{(x-2)(x+4)}\text{d}x=$
{{field-1}}

- $\operatorname{ln}(\frac{40}{7})$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2x+2}{(x-2)(x+4)} & =\frac{A}{(x-2)}+\frac{B}{(x+4)},\end{aligned}
$$

which gives

$$
2x+2=A(x+4)+B(x-2).
$$

Plugging in $x=-4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}2(-4)+2 & =A(-4+4)+B(-4-2) \\ -6 & =-6B \\ B & =1\end{aligned}
$$

On the other hand, plugging in $x=2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2(2)+2 & =A(2+4)+B(2-2) \\ 6 & =6A \\ A & =1\end{aligned}
$$

Therefore,

$$
\frac{2x+2}{(x-2)(x+4)}=\frac{1}{x-2}+\frac{1}{x+4}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{2x+2}{(x-2)(x+4)}\,\text{d}x & =\int (\frac{1}{x-2}+\frac{1}{x+4})\text{d}x \\  & =\int \frac{1}{x-2}\,\text{d}x+\int \frac{1}{x+4}\,\text{d}x \\  & =\operatorname{ln}⁡|x-2|+\operatorname{ln}⁡|x+4|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{2x+2}{(x-2)(x+4)}\,\text{d}x & =\operatorname{ln}⁡|x-2|+\operatorname{ln}⁡|x+4|+C \\  & =\operatorname{ln}⁡|(x-2)(x+4)|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{3}^{6}\frac{2x+2}{(x-2)(x+4)}\,\text{d}x & =\operatorname{ln}⁡|(x-2)(x+4)|{|}_{3}^{6} \\  & =\operatorname{ln}⁡(40)-\operatorname{ln}⁡(7) \\  & =ln\,(\frac{40}{7}).\end{aligned}
$$

## variant q-347077

Evaluate the following integral. Do not round the answer.

${\int }_{3}^{6}\frac{4 x + 4}{(x - 2)(x + 4)}\,\text{d}x=$
{{field-1}}

- $- 2 \ln{\left(7 \right)} + 4 \ln{\left(2 \right)} + 2 \ln{\left(10 \right)}$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{4 x + 4}{(x - 2)(x + 4)} &= \frac{4 x + 4}{(x - 2)(x + 4)}=\frac{A}{x - 2}+\frac{B}{x + 4}\end{aligned}
$$

which gives

$$
4 x + 4=A(x + 4)+B(x - 2)
$$

Plugging in $x=-4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}-12 &= -6B \\ B &= 2\end{aligned}
$$

On the other hand, plugging in $x=2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}12 &= 6A \\ A &= 2\end{aligned}
$$

Therefore,

$$
\frac{4 x + 4}{(x - 2)(x + 4)}=\frac{2}{x + 4} + \frac{2}{x - 2}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{4 x + 4}{(x - 2)(x + 4)}\,\text{d}x &= \int (\frac{2}{x + 4} + \frac{2}{x - 2})\,\text{d}x \\ &= 2\ln|x - 2|+2\ln|x + 4|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}2\ln|x - 2|+2\ln|x + 4|+C &= 1\ln|\left(x - 2\right)^{2} \left(x + 4\right)^{2}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{3}^{6}\frac{4 x + 4}{(x - 2)(x + 4)}\,\text{d}x &= [2\ln|x - 2|+2\ln|x + 4|]_{3}^{6} \\ &= (2 \ln{\left(4 \right)} + 2 \ln{\left(10 \right)})-(2 \ln{\left(7 \right)}) \\ &= - 2 \ln{\left(7 \right)} + 4 \ln{\left(2 \right)} + 2 \ln{\left(10 \right)}\end{aligned}
$$

## source q-348975

Evaluate the following integral. Do not round the answer.

${\int }_{3}^{5}\frac{3x+7}{{x}^{2}-8x+12}\text{d}x=$
{{field-1}}

- $-\frac{19}{2}\operatorname{ln}(3)$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that the denominator of the integrand can be factored as

$$
{x}^{2}-8x+12=(x-2)(x-6).
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{3x+7}{{x}^{2}-8x+12} & =\frac{3x+7}{(x-2)(x-6)}=\frac{A}{x-2}+\frac{B}{x-6},\end{aligned}
$$

which gives

$$
3x+7=A(x-6)+B(x-2).
$$

Plugging in $x=6,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}3(6)+7 & =A(6-6)+B(6-2) \\ 25 & =4B \\ B & =\frac{25}{4}\end{aligned}
$$

On the other hand, plugging in $x=2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}3(2)+7 & =A(2-6)+B(2-2) \\ 13 & =-4A \\ A & =-\frac{13}{4}\end{aligned}
$$

Therefore,

$$
\frac{3x+7}{{x}^{2}-8x+12}=-\frac{13}{4(x-2)}+\frac{25}{4(x-6)}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{3x+7}{{x}^{2}-8x+12}\,\text{d}x & =\int (-\frac{13}{4(x-2)}+\frac{25}{4(x-6)})\text{d}x \\  & =-\frac{13}{4}\operatorname{ln}⁡|x-2|+\frac{25}{4}\operatorname{ln}⁡|x-6|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{3x+7}{{x}^{2}-8x+12}\,\text{d}x & =-\frac{13}{4}\operatorname{ln}⁡|x-2|+\frac{25}{4}\operatorname{ln}⁡|x-6|+C.\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{3}^{5}\frac{3x+7}{{x}^{2}-8x+12}\,\text{d}x & ={[-\frac{13}{4}\operatorname{ln}⁡|x-2|+\frac{25}{4}\operatorname{ln}⁡|x-6|]}_{3}^{5} \\  & =(-\frac{13}{4}\operatorname{ln}⁡(3)+\frac{25}{4}\operatorname{ln}⁡(1))-(-\frac{13}{4}\operatorname{ln}⁡(1)+\frac{25}{4}\operatorname{ln}⁡(3)) \\  & =-\frac{13}{4}\operatorname{ln}⁡(3)-\frac{25}{4}\operatorname{ln}⁡(3) \\  & =-\frac{19}{2}\operatorname{ln}⁡(3).\end{aligned}
$$

## variant q-348975

Evaluate the following integral. Do not round the answer.

${\int }_{3}^{5}\frac{6 x + 14}{x^{2} - 8 x + 12}\,\text{d}x=$
{{field-1}}

- $- 19 \ln{\left(3 \right)}$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that the denominator of the integrand can be factored as

$$
x^{2} - 8 x + 12=(x - 2)(x - 6)
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{6 x + 14}{x^{2} - 8 x + 12} &= \frac{6 x + 14}{(x - 2)(x - 6)}=\frac{A}{x - 2}+\frac{B}{x - 6}\end{aligned}
$$

which gives

$$
6 x + 14=A(x - 6)+B(x - 2)
$$

Plugging in $x=6,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}50 &= 4B \\ B &= \frac{25}{2}\end{aligned}
$$

On the other hand, plugging in $x=2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}26 &= -4A \\ A &= - \frac{13}{2}\end{aligned}
$$

Therefore,

$$
\frac{6 x + 14}{x^{2} - 8 x + 12}=- \frac{13}{2 \left(x - 2\right)} + \frac{25}{2 \left(x - 6\right)}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{6 x + 14}{x^{2} - 8 x + 12}\,\text{d}x &= \int (- \frac{13}{2 \left(x - 2\right)} + \frac{25}{2 \left(x - 6\right)})\,\text{d}x \\ &= - \frac{13}{2}\ln|x - 2|+\frac{25}{2}\ln|x - 6|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}- \frac{13}{2}\ln|x - 2|+\frac{25}{2}\ln|x - 6|+C &= \frac{1}{2}\ln|\frac{\left(x - 6\right)^{25}}{\left(x - 2\right)^{13}}|+C\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{3}^{5}\frac{6 x + 14}{x^{2} - 8 x + 12}\,\text{d}x &= [- \frac{13}{2}\ln|x - 2|+\frac{25}{2}\ln|x - 6|]_{3}^{5} \\ &= (- \frac{13 \ln{\left(3 \right)}}{2})-(\frac{25 \ln{\left(3 \right)}}{2}) \\ &= - 19 \ln{\left(3 \right)}\end{aligned}
$$

## source q-348976

Evaluate the following integral. Do not round the answer.

${\int }_{-4}^{0}\frac{5x-1}{{x}^{2}+4x-5}\text{d}x=$
{{field-1}}

- $\frac{11}{3}\operatorname{ln}(5)$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that the denominator of the integrand can be factored as

$$
{x}^{2}+4x-5=(x+5)(x-1).
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{5x-1}{{x}^{2}+4x-5} & =\frac{5x-1}{(x+5)(x-1)}=\frac{A}{x+5}+\frac{B}{x-1},\end{aligned}
$$

which gives

$$
5x-1=A(x-1)+B(x+5).
$$

Plugging in $x=1,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}5(1)-1 & =A(1-1)+B(1+5) \\ 4 & =6B \\ B & =\frac{2}{3}\end{aligned}
$$

On the other hand, plugging in $x=-5,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}5(-5)-1 & =A(-5-1)+B(-5+5) \\ -26 & =-6A \\ A & =\frac{13}{3}\end{aligned}
$$

Therefore,

$$
\frac{5x-1}{{x}^{2}+4x-5}=\frac{13}{3(x+5)}+\frac{2}{3(x-1)}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{5x-1}{{x}^{2}+4x-5}\,\text{d}x & =\int (\frac{13}{3(x+5)}+\frac{2}{3(x-1)})\text{d}x \\  & =\frac{13}{3}\operatorname{ln}⁡|x+5|+\frac{2}{3}\operatorname{ln}⁡|x-1|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{5x-1}{{x}^{2}+4x-5}\,\text{d}x & =\frac{13}{3}\operatorname{ln}⁡|x+5|+\frac{2}{3}\operatorname{ln}⁡|x-1|+C.\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{-4}^{0}\frac{5x-1}{{x}^{2}+4x-5}\,\text{d}x & ={[\frac{13}{3}\operatorname{ln}⁡|x+5|+\frac{2}{3}\operatorname{ln}⁡|x-1|]}_{-4}^{0} \\  & =(\frac{13}{3}\operatorname{ln}⁡(5)+\frac{2}{3}\operatorname{ln}⁡(1))-(\frac{13}{3}\operatorname{ln}⁡(1)+\frac{2}{3}\operatorname{ln}⁡(5)) \\  & =\frac{13}{3}\operatorname{ln}⁡(5)-\frac{2}{3}\operatorname{ln}⁡(5) \\  & =\frac{11}{3}\operatorname{ln}⁡(5).\end{aligned}
$$

## variant q-348976

Evaluate the following integral. Do not round the answer.

${\int }_{-4}^{0}\frac{10 x - 2}{x^{2} + 4 x - 5}\,\text{d}x=$
{{field-1}}

- $\frac{22 \ln{\left(5 \right)}}{3}$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that the denominator of the integrand can be factored as

$$
x^{2} + 4 x - 5=(x + 5)(x - 1)
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{10 x - 2}{x^{2} + 4 x - 5} &= \frac{10 x - 2}{(x + 5)(x - 1)}=\frac{A}{x + 5}+\frac{B}{x - 1}\end{aligned}
$$

which gives

$$
10 x - 2=A(x - 1)+B(x + 5)
$$

Plugging in $x=1,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}8 &= 6B \\ B &= \frac{4}{3}\end{aligned}
$$

On the other hand, plugging in $x=-5,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}-52 &= -6A \\ A &= \frac{26}{3}\end{aligned}
$$

Therefore,

$$
\frac{10 x - 2}{x^{2} + 4 x - 5}=\frac{26}{3 \left(x + 5\right)} + \frac{4}{3 \left(x - 1\right)}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{10 x - 2}{x^{2} + 4 x - 5}\,\text{d}x &= \int (\frac{26}{3 \left(x + 5\right)} + \frac{4}{3 \left(x - 1\right)})\,\text{d}x \\ &= \frac{26}{3}\ln|x + 5|+\frac{4}{3}\ln|x - 1|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\frac{26}{3}\ln|x + 5|+\frac{4}{3}\ln|x - 1|+C &= \frac{1}{3}\ln|\left(x - 1\right)^{4} \left(x + 5\right)^{26}|+C\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{-4}^{0}\frac{10 x - 2}{x^{2} + 4 x - 5}\,\text{d}x &= [\frac{26}{3}\ln|x + 5|+\frac{4}{3}\ln|x - 1|]_{-4}^{0} \\ &= (\frac{26 \ln{\left(5 \right)}}{3})-(\frac{4 \ln{\left(5 \right)}}{3}) \\ &= \frac{22 \ln{\left(5 \right)}}{3}\end{aligned}
$$

## source q-349040

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\frac{1}{2}}\frac{36x-10}{12{x}^{2}-x-6}\text{d}x=$
{{field-1}}

- $\operatorname{ln}(\frac{49}{48})$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
12{x}^{2}-x-6=(4x-3)(3x+2).
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{36x-10}{12{x}^{2}-x-6} & =\frac{36x-10}{(4x-3)(3x+2)}=\frac{A}{4x-3}+\frac{B}{3x+2},\end{aligned}
$$

which gives

$$
36x-10=A(3x+2)+B(4x-3).
$$

Plugging in $x=\frac{3}{4},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}36(\frac{3}{4})-10 & =A(3(\frac{3}{4})+2)+B(4(\frac{3}{4})-3) \\ 17 & =\frac{17}{4}A \\ A & =4\end{aligned}
$$

On the other hand, plugging in $x=-\frac{2}{3},$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}36(-\frac{2}{3})-10 & =A(3(-\frac{2}{3})+2)+B(4(-\frac{2}{3})-3) \\ -34 & =-\frac{17}{3}B \\ B & =6\end{aligned}
$$

Therefore,

$$
\frac{36x-10}{12{x}^{2}-x-6}=\frac{4}{4x-3}+\frac{6}{3x+2}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{36x-10}{12{x}^{2}-x-6}\,\text{d}x & =\int (\frac{4}{4x-3}+\frac{6}{3x+2})\text{d}x \\  & =\operatorname{ln}⁡|4x-3|+2\operatorname{ln}⁡|3x+2|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{36x-10}{12{x}^{2}-x-6}\,\text{d}x & =\operatorname{ln}⁡|4x-3|+2\operatorname{ln}⁡|3x+2|+C \\  & =\operatorname{ln}⁡|(4x-3)(3x+2)^{2}|+C.\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{0}^{\frac{1}{2}}\frac{36x-10}{12{x}^{2}-x-6}\,\text{d}x & =\operatorname{ln}⁡|(4x-3)(3x+2)^{2}|{|}_{0}^{\frac{1}{2}} \\  & =\operatorname{ln}⁡(\frac{49}{4})-\operatorname{ln}⁡(12) \\  & =\operatorname{ln}⁡(\frac{49}{48}) \\  & =\operatorname{ln}⁡(\frac{49}{48}).\end{aligned}
$$

## variant q-349040

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\frac{1}{2}}\frac{72 x - 20}{12 x^{2} - x - 6}\,\text{d}x=$
{{field-1}}

- $- 8 \ln{\left(2 \right)} - 2 \ln{\left(3 \right)} + 4 \ln{\left(7 \right)}$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
12 x^{2} - x - 6=(4 x - 3)(3 x + 2)
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{72 x - 20}{12 x^{2} - x - 6} &= \frac{72 x - 20}{(4 x - 3)(3 x + 2)}=\frac{A}{4 x - 3}+\frac{B}{3 x + 2}\end{aligned}
$$

which gives

$$
72 x - 20=A(3 x + 2)+B(4 x - 3)
$$

Plugging in $x=\frac{3}{4},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}34 &= \frac{17}{4}A \\ A &= 8\end{aligned}
$$

On the other hand, plugging in $x=-\frac{2}{3},$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}-68 &= - \frac{17}{3}B \\ B &= 12\end{aligned}
$$

Therefore,

$$
\frac{72 x - 20}{12 x^{2} - x - 6}=\frac{8}{4 x - 3} + \frac{12}{3 x + 2}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{72 x - 20}{12 x^{2} - x - 6}\,\text{d}x &= \int (\frac{8}{4 x - 3} + \frac{12}{3 x + 2})\,\text{d}x \\ &= 2\ln|4 x - 3|+4\ln|3 x + 2|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}2\ln|4 x - 3|+4\ln|3 x + 2|+C &= 1\ln|\left(3 x + 2\right)^{4} \left(4 x - 3\right)^{2}|+C\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{0}^{\frac{1}{2}}\frac{72 x - 20}{12 x^{2} - x - 6}\,\text{d}x &= [2\ln|4 x - 3|+4\ln|3 x + 2|]_{0}^{\frac{1}{2}} \\ &= (4 \ln{\left(\frac{7}{2} \right)})-(2 \ln{\left(3 \right)} + 4 \ln{\left(2 \right)}) \\ &= - 8 \ln{\left(2 \right)} - 2 \ln{\left(3 \right)} + 4 \ln{\left(7 \right)}\end{aligned}
$$

## source q-349041

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{2}\frac{15x-39}{5{x}^{2}-19x-4}\text{d}x=$
{{field-1}}

- $\operatorname{ln}(\frac{121}{2})$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
5{x}^{2}-19x-4=(5x+1)(x-4).
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{15x-39}{5{x}^{2}-19x-4} & =\frac{15x-39}{(5x+1)(x-4)}=\frac{A}{5x+1}+\frac{B}{x-4},\end{aligned}
$$

which gives

$$
15x-39=A(x-4)+B(5x+1).
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}15(4)-39 & =A(4-4)+B(5(4)+1) \\ 21 & =21B \\ B & =1\end{aligned}
$$

On the other hand, plugging in $x=-\frac{1}{5},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}15(-\frac{1}{5})-39 & =A(-\frac{1}{5}-4)+B(5(-\frac{1}{5})+1) \\ -42 & =-\frac{21}{5}A \\ A & =10\end{aligned}
$$

Therefore,

$$
\frac{15x-39}{5{x}^{2}-19x-4}=\frac{10}{5x+1}+\frac{1}{x-4}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{15x-39}{5{x}^{2}-19x-4}\,\text{d}x & =\int (\frac{10}{5x+1}+\frac{1}{x-4})\text{d}x \\  & =2\operatorname{ln}⁡|5x+1|+\operatorname{ln}⁡|x-4|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{15x-39}{5{x}^{2}-19x-4}\,\text{d}x & =2\operatorname{ln}⁡|5x+1|+\operatorname{ln}⁡|x-4|+C \\  & =\operatorname{ln}⁡|(5x+1)^{2}(x-4)|+C.\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{0}^{2}\frac{15x-39}{5{x}^{2}-19x-4}\,\text{d}x & =\operatorname{ln}⁡|(5x+1)^{2}(x-4)|{|}_{0}^{2} \\  & =\operatorname{ln}⁡(242)-\operatorname{ln}⁡(4) \\  & =\operatorname{ln}⁡(\frac{242}{4}) \\  & =\operatorname{ln}⁡(\frac{121}{2}).\end{aligned}
$$

## variant q-349041

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{2}\frac{30 x - 78}{5 x^{2} - 19 x - 4}\,\text{d}x=$
{{field-1}}

- $- 2 \ln{\left(2 \right)} + 4 \ln{\left(11 \right)}$ (correct)

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
5 x^{2} - 19 x - 4=(5 x + 1)(x - 4)
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{30 x - 78}{5 x^{2} - 19 x - 4} &= \frac{30 x - 78}{(5 x + 1)(x - 4)}=\frac{A}{5 x + 1}+\frac{B}{x - 4}\end{aligned}
$$

which gives

$$
30 x - 78=A(x - 4)+B(5 x + 1)
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}42 &= 21B \\ B &= 2\end{aligned}
$$

On the other hand, plugging in $x=-\frac{1}{5},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}-84 &= - \frac{21}{5}A \\ A &= 20\end{aligned}
$$

Therefore,

$$
\frac{30 x - 78}{5 x^{2} - 19 x - 4}=\frac{20}{5 x + 1} + \frac{2}{x - 4}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{30 x - 78}{5 x^{2} - 19 x - 4}\,\text{d}x &= \int (\frac{20}{5 x + 1} + \frac{2}{x - 4})\,\text{d}x \\ &= 4\ln|5 x + 1|+2\ln|x - 4|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}4\ln|5 x + 1|+2\ln|x - 4|+C &= 1\ln|\left(x - 4\right)^{2} \left(5 x + 1\right)^{4}|+C\end{aligned}
$$

Finally, the definite integral is

$$
\begin{aligned}{\int }_{0}^{2}\frac{30 x - 78}{5 x^{2} - 19 x - 4}\,\text{d}x &= [4\ln|5 x + 1|+2\ln|x - 4|]_{0}^{2} \\ &= (2 \ln{\left(2 \right)} + 4 \ln{\left(11 \right)})-(2 \ln{\left(4 \right)}) \\ &= - 2 \ln{\left(2 \right)} + 4 \ln{\left(11 \right)}\end{aligned}
$$

## source q-49762

Evaluate ${\int }_{-1}^{1}\frac{2x+6}{{x}^{2}-4}\text{d}x.$

- $3\operatorname{ln}2$
- $\operatorname{ln}3$
- $-3\operatorname{ln}3$ (correct)
- $-2\operatorname{ln}2$
- $-2\operatorname{ln}3$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
{x}^{2}-4=(x-2)(x+2).
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{2x+6}{{x}^{2}-4} & =\frac{2x+6}{(x-2)(x+2)}=\frac{A}{(x+2)}+\frac{B}{(x-2)},\end{aligned}
$$

which gives

$$
2x+6=A(x-2)+B(x+2).
$$

Plugging in $x=2,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}2(2)+6 & =A(2-2)+B(2+2) \\ 10 & =4B \\ B & =\frac{5}{2}\end{aligned}
$$

On the other hand, plugging in $x=-2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2(-2)+6 & =A(-2-2)+B(-2+2) \\ 2 & =-4A \\ A & =-\frac{1}{2}\end{aligned}
$$

Therefore,

$$
\frac{2x+6}{{x}^{2}-4}=-\frac{1}{2(x+2)}+\frac{5}{2(x-2)}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{2x+6}{{x}^{2}-4}\,\text{d}x & =\int (-\frac{1}{2(x+2)}+\frac{5}{2(x-2)})\text{d}x \\  & =-\frac{1}{2}\int \frac{1}{x+2}\,\text{d}x+\frac{5}{2}\int \frac{1}{x-2}\,\text{d}x \\  & =\frac{1}{2}\operatorname{ln}⁡|(x-2)^{5}|-\frac{1}{2}\operatorname{ln}⁡|x+2|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{2x+6}{{x}^{2}-4}\,\text{d}x & =\frac{1}{2}\operatorname{ln}⁡|(x-2)^{5}|-\frac{1}{2}\operatorname{ln}⁡|x+2|+C \\  & =\frac{1}{2}\operatorname{ln}⁡|\frac{(x-2)^{5}}{x+2}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-1}^{1}\frac{2x+6}{{x}^{2}-4}\,\text{d}x & =\frac{1}{2}\operatorname{ln}⁡|\frac{(x-2)^{5}}{x+2}|{|}_{-1}^{1} \\  & =\frac{1}{2}(\operatorname{ln}⁡|-\frac{1}{3}|-\operatorname{ln}⁡|-{3}^{5}|) \\  & =\frac{1}{2}(\operatorname{ln}⁡({3}^{-1})-\operatorname{ln}⁡({3}^{5})) \\  & =\frac{1}{2}(-\operatorname{ln}⁡3-5\operatorname{ln}⁡3) \\  & =\frac{1}{2}(-6\operatorname{ln}⁡3) \\  & =-3\operatorname{ln}⁡3.\end{aligned}
$$

## variant q-49762

Evaluate ${\int }_{-1}^{1}\frac{4 x + 12}{x^{2} - 4}\,\text{d}x.$

- $6 \ln{\left(2 \right)}$
- $2 \ln{\left(3 \right)}$
- $- 6 \ln{\left(3 \right)}$ (correct)
- $- 4 \ln{\left(2 \right)}$
- $- 4 \ln{\left(3 \right)}$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
x^{2} - 4=(x + 2)(x - 2)
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{4 x + 12}{x^{2} - 4} &= \frac{4 x + 12}{(x + 2)(x - 2)}=\frac{A}{x + 2}+\frac{B}{x - 2}\end{aligned}
$$

which gives

$$
4 x + 12=A(x - 2)+B(x + 2)
$$

Plugging in $x=2,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}20 &= 4B \\ B &= 5\end{aligned}
$$

On the other hand, plugging in $x=-2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}4 &= -4A \\ A &= -1\end{aligned}
$$

Therefore,

$$
\frac{4 x + 12}{x^{2} - 4}=- \frac{1}{x + 2} + \frac{5}{x - 2}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{4 x + 12}{x^{2} - 4}\,\text{d}x &= \int (- \frac{1}{x + 2} + \frac{5}{x - 2})\,\text{d}x \\ &= -1\ln|x + 2|+5\ln|x - 2|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}-1\ln|x + 2|+5\ln|x - 2|+C &= 1\ln|\frac{\left(x - 2\right)^{5}}{x + 2}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-1}^{1}\frac{4 x + 12}{x^{2} - 4}\,\text{d}x &= [-1\ln|x + 2|+5\ln|x - 2|]_{-1}^{1} \\ &= (- \ln{\left(3 \right)})-(5 \ln{\left(3 \right)}) \\ &= - 6 \ln{\left(3 \right)}\end{aligned}
$$

## source q-49764

${\int }_{-6}^{-5}\frac{5x+29}{(x+7)(x+4)}\text{d}x=$

- $\operatorname{ln}3$
- $5\operatorname{ln}2$
- $-\operatorname{ln}2$ (correct)
- $-2\operatorname{ln}3$
- $-\operatorname{ln}5$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{5x+29}{(x+7)(x+4)}=\frac{A}{(x+7)}+\frac{B}{(x+4)},\end{aligned}
$$

which gives

$$
5x+29=A(x+4)+B(x+7).
$$

Plugging in $x=-4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}5(-4)+29 & =A(-4+4)+B(-4+7) \\ 9 & =3B \\ B & =3\end{aligned}
$$

On the other hand, plugging in $x=-7,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}5(-7)+29 & =A(-7+4)+B(-7+7) \\ -6 & =-3A \\ A & =2\end{aligned}
$$

Therefore,

$$
\frac{5x+29}{(x+7)(x+4)}=\frac{2}{(x+7)}+\frac{3}{(x+4)}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{5x+29}{(x+7)(x+4)}\,\text{d}x & =\int (\frac{2}{x+7}+\frac{3}{x+4})\text{d}x \\  & =2\int \frac{1}{x+7}\,\text{d}x+3\int \frac{1}{x+4}\,\text{d}x \\  & =2\operatorname{ln}⁡|x+7|+3\operatorname{ln}⁡|x+4|+C \\  & =\operatorname{ln}⁡|(x+7)^{2}|+\operatorname{ln}⁡|(x+4)^{3}|+C \\  & =\operatorname{ln}⁡|(x+7)^{2}(x+4)^{3}|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{5x+29}{(x+7)(x+4)}\,\text{d}x & =\operatorname{ln}⁡|(x+7)^{2}|+\operatorname{ln}⁡|(x+4)^{3}|+C \\  & =\operatorname{ln}⁡|(x+7)^{2}(x+4)^{3}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-6}^{-5}\frac{5x+29}{(x+7)(x+4)}\,\text{d}x & =\operatorname{ln}⁡|(x+7)^{2}(x+4)^{3}|{|}_{-6}^{-5} \\  & =\operatorname{ln}⁡({2}^{2})-\operatorname{ln}⁡({2}^{3}) \\  & =2\operatorname{ln}⁡2-3\operatorname{ln}⁡2 \\  & =-\operatorname{ln}⁡2.\end{aligned}
$$

## variant q-49764

${\int }_{-6}^{-5}\frac{10 x + 58}{(x + 7)(x + 4)}\,\text{d}x=$

- $2 \ln{\left(3 \right)}$
- $10 \ln{\left(2 \right)}$
- $- 2 \ln{\left(2 \right)}$ (correct)
- $- 4 \ln{\left(3 \right)}$
- $- 2 \ln{\left(5 \right)}$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{10 x + 58}{(x + 7)(x + 4)} &= \frac{10 x + 58}{(x + 7)(x + 4)}=\frac{A}{x + 7}+\frac{B}{x + 4}\end{aligned}
$$

which gives

$$
10 x + 58=A(x + 4)+B(x + 7)
$$

Plugging in $x=-4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}18 &= 3B \\ B &= 6\end{aligned}
$$

On the other hand, plugging in $x=-7,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}-12 &= -3A \\ A &= 4\end{aligned}
$$

Therefore,

$$
\frac{10 x + 58}{(x + 7)(x + 4)}=\frac{4}{x + 7} + \frac{6}{x + 4}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{10 x + 58}{(x + 7)(x + 4)}\,\text{d}x &= \int (\frac{4}{x + 7} + \frac{6}{x + 4})\,\text{d}x \\ &= 4\ln|x + 7|+6\ln|x + 4|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}4\ln|x + 7|+6\ln|x + 4|+C &= 1\ln|\left(x + 4\right)^{6} \left(x + 7\right)^{4}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-6}^{-5}\frac{10 x + 58}{(x + 7)(x + 4)}\,\text{d}x &= [4\ln|x + 7|+6\ln|x + 4|]_{-6}^{-5} \\ &= (4 \ln{\left(2 \right)})-(6 \ln{\left(2 \right)}) \\ &= - 2 \ln{\left(2 \right)}\end{aligned}
$$

## source q-49765

Evaluate ${\int }_{-7}^{-3}\frac{11x+46}{(x+2)(x+8)}\text{d}x.$

- $5\operatorname{ln}2$
- $3\operatorname{ln}2$
- $2\operatorname{ln}5$
- $3\operatorname{ln}5$ (correct)
- $2\operatorname{ln}3$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{11x+46}{(x+2)(x+8)} & =\frac{A}{(x+2)}+\frac{B}{(x+8)},\end{aligned}
$$

which gives

$$
11x+46=A(x+8)+B(x+2).
$$

Plugging in $x=-8,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}11(-8)+46 & =A(-8+8)+B(-8+2) \\ -42 & =-6B \\ B & =7\end{aligned}
$$

On the other hand, plugging in $x=-2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}11(-2)+46 & =A(-2+8)+B(-2+2) \\ 24 & =6A \\ A & =4\end{aligned}
$$

Therefore,

$$
\frac{11x+46}{(x+2)(x+8)}=\frac{4}{(x+2)}+\frac{7}{(x+8)}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{11x+46}{(x+2)(x+8)}\,\text{d}x & =\int (\frac{4}{x+2}+\frac{7}{x+8})\text{d}x \\  & =4\int \frac{1}{x+2}\,\text{d}x+7\int \frac{1}{x+8}\,\text{d}x \\  & =4\operatorname{ln}⁡|x+2|+7\operatorname{ln}⁡|x+8|+C.\end{aligned}
$$

            

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{11x+46}{(x+2)(x+8)}\,\text{d}x & =4\operatorname{ln}⁡|x+2|+7\operatorname{ln}⁡|x+8|+C \\  & =\operatorname{ln}⁡|(x+2)^{4}(x+8)^{7}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-7}^{-3}\frac{11x+46}{(x+2)(x+8)}\,\text{d}x & =\operatorname{ln}⁡|(x+2)^{4}(x+8)^{7}|{|}_{-7}^{-3} \\  & =\operatorname{ln}⁡({5}^{7})-\operatorname{ln}⁡({5}^{4}) \\  & =7\operatorname{ln}⁡5-4\operatorname{ln}⁡5 \\  & =3\operatorname{ln}⁡5.\end{aligned}
$$

## variant q-49765

Evaluate ${\int }_{-7}^{-3}\frac{22 x + 92}{(x + 2)(x + 8)}\,\text{d}x.$

- $10 \ln{\left(2 \right)}$
- $6 \ln{\left(2 \right)}$
- $4 \ln{\left(5 \right)}$
- $6 \ln{\left(5 \right)}$ (correct)
- $4 \ln{\left(3 \right)}$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{22 x + 92}{(x + 2)(x + 8)} &= \frac{22 x + 92}{(x + 2)(x + 8)}=\frac{A}{x + 2}+\frac{B}{x + 8}\end{aligned}
$$

which gives

$$
22 x + 92=A(x + 8)+B(x + 2)
$$

Plugging in $x=-8,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}-84 &= -6B \\ B &= 14\end{aligned}
$$

On the other hand, plugging in $x=-2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}48 &= 6A \\ A &= 8\end{aligned}
$$

Therefore,

$$
\frac{22 x + 92}{(x + 2)(x + 8)}=\frac{14}{x + 8} + \frac{8}{x + 2}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{22 x + 92}{(x + 2)(x + 8)}\,\text{d}x &= \int (\frac{14}{x + 8} + \frac{8}{x + 2})\,\text{d}x \\ &= 8\ln|x + 2|+14\ln|x + 8|+C\end{aligned}
$$

            

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}8\ln|x + 2|+14\ln|x + 8|+C &= 1\ln|\left(x + 2\right)^{8} \left(x + 8\right)^{14}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-7}^{-3}\frac{22 x + 92}{(x + 2)(x + 8)}\,\text{d}x &= [8\ln|x + 2|+14\ln|x + 8|]_{-7}^{-3} \\ &= (14 \ln{\left(5 \right)})-(8 \ln{\left(5 \right)}) \\ &= 6 \ln{\left(5 \right)}\end{aligned}
$$

## source q-49769

Evaluate ${\int }_{-2}^{-1}\frac{x+1}{x(x+3)}\text{d}x.$

- $5\operatorname{ln}3$
- $\frac{3}{2}\operatorname{ln}5$
- $2\operatorname{ln}3$
- $\frac{1}{3}\operatorname{ln}2$ (correct)
- $2\operatorname{ln}5$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{x+1}{x(x+3)} & =\frac{A}{x}+\frac{B}{x+3},\end{aligned}
$$

which gives

$$
x+1=A(x+3)+Bx.
$$

Plugging in $x=-3,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}-3+1 & =A(-3+3)+B(-3) \\ -2 & =-3B \\ B & =\frac{2}{3}\end{aligned}
$$

On the other hand, plugging in $x=0,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}0+1 & =A(0+3)+B(0) \\ 1 & =3A \\ A & =\frac{1}{3}\end{aligned}
$$

Therefore,

$$
\frac{x+1}{x(x+3)}=\frac{1}{3x}+\frac{2}{3(x+3)}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{x+1}{x(x+3)}\,\text{d}x & =\int (\frac{1}{3x}+\frac{2}{3(x+3)})\text{d}x \\  & =\frac{1}{3}\int \frac{1}{x}\,\text{d}x+\frac{2}{3}\int \frac{1}{x+3}\,\text{d}x \\  & =\frac{1}{3}\operatorname{ln}⁡|x|+\frac{2}{3}\operatorname{ln}⁡|x+3|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{x+1}{x(x+3)}\,\text{d}x & =\frac{1}{3}\operatorname{ln}⁡|x|+\frac{2}{3}\operatorname{ln}⁡|x+3|+C \\  & =\frac{1}{3}\operatorname{ln}⁡|x(x+3)^{2}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-2}^{-1}\frac{x+1}{x(x+3)}\,\text{d}x & =\frac{1}{3}\operatorname{ln}⁡|x(x+3)^{2}|{|}_{-2}^{-1} \\  & =\frac{1}{3}(\operatorname{ln}⁡4-\operatorname{ln}⁡2) \\  & =\frac{1}{3}\operatorname{ln}⁡(\frac{4}{2}) \\  & =\frac{1}{3}\operatorname{ln}⁡2.\end{aligned}
$$

## variant q-49769

Evaluate ${\int }_{-2}^{-1}\frac{2 x + 2}{(x)(x + 3)}\,\text{d}x.$

- $10 \ln{\left(3 \right)}$
- $3 \ln{\left(5 \right)}$
- $4 \ln{\left(3 \right)}$
- $\frac{2 \ln{\left(2 \right)}}{3}$ (correct)
- $4 \ln{\left(5 \right)}$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2 x + 2}{(x)(x + 3)} &= \frac{2 x + 2}{(x)(x + 3)}=\frac{A}{x}+\frac{B}{x + 3}\end{aligned}
$$

which gives

$$
2 x + 2=A(x + 3)+B(x)
$$

Plugging in $x=-3,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}-4 &= -3B \\ B &= \frac{4}{3}\end{aligned}
$$

On the other hand, plugging in $x=0,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2 &= 3A \\ A &= \frac{2}{3}\end{aligned}
$$

Therefore,

$$
\frac{2 x + 2}{(x)(x + 3)}=\frac{4}{3 \left(x + 3\right)} + \frac{2}{3 x}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{2 x + 2}{(x)(x + 3)}\,\text{d}x &= \int (\frac{4}{3 \left(x + 3\right)} + \frac{2}{3 x})\,\text{d}x \\ &= \frac{2}{3}\ln|x|+\frac{4}{3}\ln|x + 3|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\frac{2}{3}\ln|x|+\frac{4}{3}\ln|x + 3|+C &= \frac{1}{3}\ln|x^{2} \left(x + 3\right)^{4}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-2}^{-1}\frac{2 x + 2}{(x)(x + 3)}\,\text{d}x &= [\frac{2}{3}\ln|x|+\frac{4}{3}\ln|x + 3|]_{-2}^{-1} \\ &= (\frac{4 \ln{\left(2 \right)}}{3})-(\frac{2 \ln{\left(2 \right)}}{3}) \\ &= \frac{2 \ln{\left(2 \right)}}{3}\end{aligned}
$$

## source q-75825

Evaluate
${\int }_{-1}^{3}\frac{3x-6}{{x}^{2}-2x-8}\text{d}x.$

- $3\operatorname{ln}5$
- $\operatorname{ln}3$
- $\operatorname{ln}5$ (correct)
- $2\operatorname{ln}3$
- $\operatorname{ln}2$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
{x}^{2}-2x-8=(x+2)(x-4).
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{3x-6}{{x}^{2}-2x-8} & =\frac{3x-6}{(x+2)(x-4)}=\frac{A}{x+2}+\frac{B}{x-4},\end{aligned}
$$

which gives

$$
3x-6=A(x-4)+B(x+2).
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}3(4)-6 & =A(4-4)+B(4+2) \\ 6 & =6B \\ B & =1\end{aligned}
$$

On the other hand, plugging in $x=-2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}3(-2)-6 & =A(-2-4)+B(-2+2) \\ -12 & =-6A \\ A & =2\end{aligned}
$$

Therefore,

$$
\frac{3x-6}{{x}^{2}-2x-8}=\frac{2}{x+2}+\frac{1}{x-4}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{3x-6}{{x}^{2}-2x-8}\,\text{d}x & =\int (\frac{2}{x+2}+\frac{1}{x-4})\text{d}x \\  & =2\int \frac{1}{x+2}\,\text{d}x+\int \frac{1}{x-4}\,\text{d}x \\  & =2\operatorname{ln}⁡|x+2|+\operatorname{ln}⁡|x-4|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{3x-6}{{x}^{2}-2x-8}\,\text{d}x & =2\operatorname{ln}⁡|x+2|+\operatorname{ln}⁡|x-4|+C \\  & =\operatorname{ln}⁡|(x+2)^{2}|+\operatorname{ln}⁡|x-4|+C \\  & =\operatorname{ln}⁡|(x+2)^{2}(x-4)|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-1}^{3}\frac{3x-6}{{x}^{2}-2x-8}\,\text{d}x & =\operatorname{ln}⁡|(x+2)^{2}(x-4)|{|}_{-1}^{3} \\  & =\operatorname{ln}⁡({5}^{2})-\operatorname{ln}⁡5 \\  & =2\operatorname{ln}⁡5-\operatorname{ln}⁡5 \\  & =\operatorname{ln}⁡5.\end{aligned}
$$

## variant q-75825

Evaluate
${\int }_{-1}^{3}\frac{6 x - 12}{x^{2} - 2 x - 8}\,\text{d}x.$

- $6 \ln{\left(5 \right)}$
- $2 \ln{\left(3 \right)}$
- $2 \ln{\left(5 \right)}$ (correct)
- $4 \ln{\left(3 \right)}$
- $2 \ln{\left(2 \right)}$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
x^{2} - 2 x - 8=(x + 2)(x - 4)
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{6 x - 12}{x^{2} - 2 x - 8} &= \frac{6 x - 12}{(x + 2)(x - 4)}=\frac{A}{x + 2}+\frac{B}{x - 4}\end{aligned}
$$

which gives

$$
6 x - 12=A(x - 4)+B(x + 2)
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}12 &= 6B \\ B &= 2\end{aligned}
$$

On the other hand, plugging in $x=-2,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}-24 &= -6A \\ A &= 4\end{aligned}
$$

Therefore,

$$
\frac{6 x - 12}{x^{2} - 2 x - 8}=\frac{4}{x + 2} + \frac{2}{x - 4}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{6 x - 12}{x^{2} - 2 x - 8}\,\text{d}x &= \int (\frac{4}{x + 2} + \frac{2}{x - 4})\,\text{d}x \\ &= 4\ln|x + 2|+2\ln|x - 4|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}4\ln|x + 2|+2\ln|x - 4|+C &= 1\ln|\left(x - 4\right)^{2} \left(x + 2\right)^{4}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{-1}^{3}\frac{6 x - 12}{x^{2} - 2 x - 8}\,\text{d}x &= [4\ln|x + 2|+2\ln|x - 4|]_{-1}^{3} \\ &= (4 \ln{\left(5 \right)})-(2 \ln{\left(5 \right)}) \\ &= 2 \ln{\left(5 \right)}\end{aligned}
$$

## source q-75828

Evaluate
${\int }_{4}^{11}\frac{14}{5{x}^{2}+16x+3}\text{d}x.$

- $\operatorname{ln}(12)$
- $\operatorname{ln}(\frac{2}{3})$
- $\operatorname{ln}(\frac{4}{3})$ (correct)
- $\operatorname{ln}(\frac{8}{7})$
- $\operatorname{ln}(28)$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
5{x}^{2}+16x+3=(5x+1)(x+3).
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{14}{5{x}^{2}+16x+3} & =\frac{14}{(5x+1)(x+3)}=\frac{A}{(5x+1)}+\frac{B}{(x+3)},\end{aligned}
$$

which gives

$$
14=A(x+3)+B(5x+1).
$$

Plugging in $x=-3,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}14 & =A(-3+3)+B(5(-3)+1) \\ 14 & =-14B \\ B & =-1\end{aligned}
$$

On the other hand, plugging in $x=-\frac{1}{5},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}14 & =A(-\frac{1}{5}+3)+B(5(-\frac{1}{5})+1) \\ 14 & =\frac{14}{5}A \\ A & =5\end{aligned}
$$

Therefore,

$$
\frac{14}{5{x}^{2}+16x+3}=\frac{5}{5x+1}-\frac{1}{(x+3)}.
$$

Now, we integrate, and we get

$$
\begin{aligned}\int \frac{14}{5{x}^{2}+16x+3}\,\text{d}x & =\int (\frac{5}{5x+1}-\frac{1}{x+3})\text{d}x \\  & =\int \frac{5}{5x+1}\,\text{d}x-\int \frac{1}{x+3}\,\text{d}x \\  & =\operatorname{ln}⁡|5x+1|-\operatorname{ln}⁡|x+3|+C.\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}\int \frac{14}{5{x}^{2}+16x+3}\,\text{d}x & =\operatorname{ln}⁡|5x+1|-\operatorname{ln}⁡|x+3|+C \\  & =\operatorname{ln}⁡|\frac{5x+1}{x+3}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{4}^{11}\frac{14}{5{x}^{2}+16x+3}\,\text{d}x & =\operatorname{ln}⁡|\frac{5x+1}{x+3}|{|}_{4}^{11} \\  & =\operatorname{ln}⁡(4)-\operatorname{ln}⁡(3) \\  & =\operatorname{ln}⁡(\frac{4}{3}).\end{aligned}
$$

## variant q-75828

Evaluate
${\int }_{4}^{11}\frac{28}{5 x^{2} + 16 x + 3}\,\text{d}x.$

- $2 \ln{\left(12 \right)}$
- $- 2 \ln{\left(3 \right)} + 2 \ln{\left(2 \right)}$
- $- 2 \ln{\left(3 \right)} + 4 \ln{\left(2 \right)}$ (correct)
- $- 2 \ln{\left(7 \right)} + 6 \ln{\left(2 \right)}$
- $2 \ln{\left(28 \right)}$

We'll work out the indefinite integral first and then proceed with the definite integral.

First, we note that a denominator of the integrand can be factored as

$$
5 x^{2} + 16 x + 3=(5 x + 1)(x + 3)
$$

So the integrand can be converted into a sum of partial fractions,

$$
\begin{aligned}\frac{28}{5 x^{2} + 16 x + 3} &= \frac{28}{(5 x + 1)(x + 3)}=\frac{A}{5 x + 1}+\frac{B}{x + 3}\end{aligned}
$$

which gives

$$
28=A(x + 3)+B(5 x + 1)
$$

Plugging in $x=-3,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}28 &= -14B \\ B &= -2\end{aligned}
$$

On the other hand, plugging in $x=-\frac{1}{5},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}28 &= \frac{14}{5}A \\ A &= 10\end{aligned}
$$

Therefore,

$$
\frac{28}{5 x^{2} + 16 x + 3}=\frac{10}{5 x + 1} - \frac{2}{x + 3}
$$

Now, we integrate, and we get

$$
\begin{aligned}{\int }\frac{28}{5 x^{2} + 16 x + 3}\,\text{d}x &= \int (\frac{10}{5 x + 1} - \frac{2}{x + 3})\,\text{d}x \\ &= 2\ln|5 x + 1|-2\ln|x + 3|+C\end{aligned}
$$

We can simplify the result using the laws of logarithms, as follows:

$$
\begin{aligned}2\ln|5 x + 1|-2\ln|x + 3|+C &= 1\ln|\frac{\left(5 x + 1\right)^{2}}{\left(x + 3\right)^{2}}|+C\end{aligned}
$$

Finally, the definite integral is 

$$
\begin{aligned}{\int }_{4}^{11}\frac{28}{5 x^{2} + 16 x + 3}\,\text{d}x &= [2\ln|5 x + 1|-2\ln|x + 3|]_{4}^{11} \\ &= (- 2 \ln{\left(14 \right)} + 2 \ln{\left(56 \right)})-(- 2 \ln{\left(7 \right)} + 2 \ln{\left(21 \right)}) \\ &= - 2 \ln{\left(21 \right)} - 2 \ln{\left(14 \right)} + 2 \ln{\left(7 \right)} + 2 \ln{\left(56 \right)}\end{aligned}
$$
