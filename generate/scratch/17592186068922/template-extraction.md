# Template extraction

All source-specific components and raw bank values follow. Source values are observed evidence; proposed sampling k=2..9 is a narrower, explicit numerator/bank transport policy. k=1 is source replay. Changed numerators are variants, not new Markdown templates. Each radio source retains its complete bank profile; no recipes are pooled.

## q-49604

Source entity 17592186069379; UUID 1f6ebcba-4e39-5954-8ee8-c37c592d0f6b.

Given that

$$
\int \frac{13}{(3x+2)(2x-3)}\,\text{d}x=a\operatorname{ln}⁡|2x-3|+b\operatorname{ln}⁡|3x+2|+C,
$$

find the value of $a+b.$


Observed pattern: moderate, sum; numerator 13, ordered linear factors 2*x - 3 and 3*x + 2. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is one scalar coefficient sum.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field selection (:answer-field.type/radio).


- Choice 24ae7afd-8576-5602-9501-9c611ec3ed70: `0`; correct marker True; recipe k*(0); complete observed scalar-bank transport.


- Choice 4201b9e5-4180-5325-b8c7-2805b2c0f988: `-2`; correct marker False; recipe k*(-2); complete observed scalar-bank transport.


- Choice 7739fe2a-f91d-523e-b519-5eba915ac6ac: `2`; correct marker False; recipe k*(2); complete observed scalar-bank transport.


- Choice acecead2-9843-5d76-95c9-05999fbf5f2e: `1`; correct marker False; recipe k*(1); complete observed scalar-bank transport.


- Choice eb610479-69f3-5893-b5aa-5c24f871f951: `-1`; correct marker False; recipe k*(-1); complete observed scalar-bank transport.


Original worked solution:

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{13}{(3x+2)(2x-3)} & =\frac{A}{3x+2}+\frac{B}{2x-3},\end{aligned}
$$

which gives

$$
13=A(2x-3)+B(3x+2).
$$

Plugging in $x=\frac{3}{2},$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}13 & =A(2(\frac{3}{2})-3)+B(3(\frac{3}{2})+2) \\ 13 & =\frac{13}{2}B \\ B & =2\end{aligned}
$$

On the other hand, plugging in $x=-\frac{2}{3},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}13 & =A(2(-\frac{2}{3})-3)+B(3(-\frac{2}{3})+2) \\ 13 & =-\frac{13}{3}A \\ A & =-3\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{13}{(3x+2)(2x-3)}=-\frac{3}{3x+2}+\frac{2}{2x-3}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{13}{(3x+2)(2x-3)}\,\text{d}x & =\int (-\frac{3}{3x+2}+\frac{2}{2x-3})\text{d}x \\  & =-\int \frac{3}{3x+2}\,\text{d}x+\int \frac{2}{2x-3}\,\text{d}x \\  & =\operatorname{ln}⁡|2x-3|-\operatorname{ln}⁡|3x+2|+C.\end{aligned}
$$

Finally, $a=1,b=-1,$ and $a+b=1-1=0.$

## q-49904

Source entity 17592186069396; UUID f29adfb1-f6e4-5efe-acf8-fa2f7f98e7f2.

What is $\displaystyle \int(-5)/(x(x - 1))dx$?


Field selection (:answer-field.type/radio).


- Choice a8294469-b10f-5558-b3dc-de74f0bf019b: `5\ln\begin{vmatrix}x & -\frac{1}{5}\ln & x - 1\end{vmatrix}+ C`; correct marker False; recipe Unresolved/unsupported; original retained without inference.


- Choice f355ef9f-48e7-54fc-8ccf-5ff5b25fabf9: `\ln\begin{vmatrix}x & -\frac{1}{5}\ln & x - 1\end{vmatrix}+ C`; correct marker False; recipe Unresolved/unsupported; original retained without inference.


- Choice 14624ca2-6eee-5d13-acad-913c3ca49068: `\ln\begin{vmatrix}x & -5\ln & x - 1\end{vmatrix}+ C`; correct marker False; recipe Unresolved/unsupported; original retained without inference.


- Choice 2e883ada-9680-5bb3-be9b-032307e720ea: `5\ln\begin{vmatrix}x & -\ln & x - 1\end{vmatrix}+ C`; correct marker False; recipe Unresolved/unsupported; original retained without inference.


- Choice 35e6c592-3ab9-5f4b-b411-afed57d71194: `5\ln\begin{vmatrix}x & -5\ln & x - 1\end{vmatrix}+ C`; correct marker False; recipe Unresolved/unsupported; original retained without inference.


Original worked solution:

[Absent; unresolved]

## q-128339

Source entity 17592186235371; UUID 333f44c6-e7aa-5f32-a7e4-9a58be270016.

Given that

$$
{\int }_{4}^{\infty }f(x)\,\text{d}x=A{\int }_{4}^{\infty }\frac{\text{d}x}{x-3}+B{\int }_{4}^{\infty }\frac{\text{d}x}{2x+1}
$$

where $A$ and $B$ are constants, find $A$ and $B.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $A=$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                                

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $B=$

                                    
                                
                                    
                            
                                        {{field-2}}


Field field-1 (:answer-field.type/blank).


- Choice 71cce186-30b6-55d0-84d4-342f5c753f10: `1`; correct marker True; recipe Unresolved/unsupported; original retained without inference.


Field field-2 (:answer-field.type/blank).


- Choice f1e90155-6ac0-50f6-a4fb-8e3b6bbb20ef: `-2`; correct marker True; recipe Unresolved/unsupported; original retained without inference.


Original worked solution:

First, we factor the numerator and denominator of $f(x)$:

$$
f(x)=\frac{7}{2{x}^{2}-5x-3}=\frac{7}{(x-3)(2x+1)}
$$

Our task is to find $A$ and $B$ such that

$$
\frac{7}{(x-3)(2x+1)}=\frac{A}{x-3}+\frac{B}{2x+1}.
$$

Multiplying both sides by $(x-3)(2x+1)$ gives

$$
7=A(2x+1)+B(x-3).
$$

Substituting $x=-\frac{1}{2},$ we get

$$
\begin{aligned}7 & =A(2\cdot (-\frac{1}{2})+1)+B(-\frac{1}{2}-3) \\ 7 & =-\frac{7}{2}B \\ B & =-2.\end{aligned}
$$

Substituting $x=3,$ we get

$$
\begin{aligned}7 & =A(2\cdot 3+1)+B(3-3) \\ 7 & =7A \\ A & =1.\end{aligned}
$$

Hence,

$$
\frac{7}{(x-3)(2x+1)}=\frac{1}{x-3}-\frac{2}{2x+1}.
$$

Finally,

$$
\begin{aligned}{\int }_{4}^{\infty }f(x)\,\text{d}x & ={\int }_{4}^{\infty }(\frac{1}{x-3}-\frac{2}{2x+1})\,\text{d}x \\  & ={\int }_{4}^{\infty }\frac{\text{d}x}{x-3}-2{\int }_{4}^{\infty }\frac{\text{d}x}{2x+1}.\end{aligned}
$$

So, $A=1$ and $B=-2.$

## q-103988

Source entity 17592186240780; UUID ed315823-9912-53f6-ae66-2685405a1454.

$\int \frac{2x+7}{(2x+1)(x+2)}\,\text{d}x=$


Observed pattern: moderate, logs; numerator 2*x + 7, ordered linear factors 2*x + 1 and x + 2. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is one complete antiderivative modulo an additive constant.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field selection (:answer-field.type/radio).


- Choice 036e519f-c924-5649-b208-3cae45c9c3c1: `2\operatorname{ln}⁡|2x+1|+2\operatorname{ln}⁡|x+2|+C`; correct marker False; recipe k*(2) ln|2*x + 1| + k*(2) ln|x + 2| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 60b2f004-1b0a-52b0-9b2b-ebdac2ed1485: `4\operatorname{ln}⁡|2x+1|+\operatorname{ln}⁡|x+2|+C`; correct marker False; recipe k*(4) ln|2*x + 1| + k*(1) ln|x + 2| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 8e197d1b-f46a-5bca-b996-28be90359d6a: `4\operatorname{ln}⁡|2x+1|-\operatorname{ln}⁡|x+2|+C`; correct marker False; recipe k*(4) ln|2*x + 1| + k*(-1) ln|x + 2| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 9f7cf41d-bf13-5501-a648-617b7fb48f6b: `4\operatorname{ln}⁡|2x+1|-2\operatorname{ln}⁡|x+2|+C`; correct marker False; recipe k*(4) ln|2*x + 1| + k*(-2) ln|x + 2| + C; equality checked by differentiation on the real pole-free intervals.


- Choice c228a57c-3a58-5cc8-9d7b-d801859aadae: `2\operatorname{ln}⁡|2x+1|-\operatorname{ln}⁡|x+2|+C`; correct marker True; recipe k*(2) ln|2*x + 1| + k*(-1) ln|x + 2| + C; equality checked by differentiation on the real pole-free intervals.


Original worked solution:

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2x+7}{(2x+1)(x+2)} & =\frac{A}{2x+1}+\frac{B}{x+2},\end{aligned}
$$

which gives

$$
2x+7=A(x+2)+B(2x+1).
$$

Plugging in $x=-2,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}2(-2)+7 & =A((-2)+2)+B(2(-2)+1) \\ 3 & =-3B \\ B & =-1\end{aligned}
$$

On the other hand, plugging in $x=-\frac{1}{2},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2(-\frac{1}{2})+7 & =A(-\frac{1}{2}+2)+B(2(-\frac{1}{2})+1) \\ 6 & =A(\frac{3}{2}) \\ A & =4\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{2x+7}{(2x+1)(x+2)} & =\frac{4}{2x+1}-\frac{1}{x+2}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{2x+7}{(2x+1)(x+2)}\,\text{d}x & =\int (\frac{4}{2x+1}-\frac{1}{x+2})\text{d}x \\  & =4\int \frac{1}{2x+1}\,\text{d}x-\int \frac{1}{x+2}\,\text{d}x \\  & =2\operatorname{ln}⁡|2x+1|-\operatorname{ln}⁡|x+2|+C.\end{aligned}
$$

## q-103989

Source entity 17592186240781; UUID 992496e6-fae7-5b47-9d13-a4fe5d22fb68.

$\int \frac{2x-4}{x(x-4)}\,\text{d}x=$


Observed pattern: easy, logs; numerator 2*x - 4, ordered linear factors x and x - 4. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is one complete antiderivative modulo an additive constant.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field selection (:answer-field.type/radio).


- Choice 021f6895-433e-546e-8a64-b6694c9f9037: `\operatorname{ln}⁡|x|-\operatorname{ln}⁡|x-4|+C`; correct marker False; recipe k*(1) ln|x| + k*(-1) ln|x - 4| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 17632347-1091-5700-9637-3abb325c6ed6: `2\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x-4|+C`; correct marker False; recipe k*(2) ln|x| + k*(2) ln|x - 4| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 27e3c466-6f7a-56cd-9dc3-54816a11c3c6: `\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x-4|+C`; correct marker False; recipe k*(1) ln|x| + k*(2) ln|x - 4| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 83738b98-16d3-528c-b36c-5c5b3a4b4e3a: `2\operatorname{ln}⁡|x|-2\operatorname{ln}⁡|x-4|+C`; correct marker False; recipe k*(2) ln|x| + k*(-2) ln|x - 4| + C; equality checked by differentiation on the real pole-free intervals.


- Choice f85a7627-23df-52ea-bb89-b64fab1c596d: `\operatorname{ln}⁡|x|+\operatorname{ln}⁡|x-4|+C`; correct marker True; recipe k*(1) ln|x| + k*(1) ln|x - 4| + C; equality checked by differentiation on the real pole-free intervals.


Original worked solution:

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2x-4}{x(x-4)} & =\frac{A}{x}+\frac{B}{x-4},\end{aligned}
$$

which gives

$$
2x-4=A(x-4)+Bx.
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}2(4)-4 & =A(4-4)+B(4) \\ 4 & =4B \\ 1 & =B\end{aligned}
$$

On the other hand, plugging in $x=0,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2(0)-4 & =A(0-4)+B(0) \\ -4 & =-4A \\ A & =1\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{2x-4}{x(x-4)} & =\frac{1}{x}+\frac{1}{x-4}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{2x-4}{x(x-4)}\,\text{d}x & =\int (\frac{1}{x}+\frac{1}{x-4})\text{d}x \\  & =\int \frac{1}{x}\,\text{d}x+\int \frac{1}{x-4}\,\text{d}x \\  & =\operatorname{ln}⁡|x|+\operatorname{ln}⁡|x-4|+C.\end{aligned}
$$

## q-348896

Source entity 17592186319307; UUID 6e9f94ca-0527-57ee-8929-045d95cec1a8.

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{7x+7}{(x+3)(x-4)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|x+3|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x-4|+C$


Observed pattern: moderate, coefficients; numerator 7*x + 7, ordered linear factors x + 3 and x - 4. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is two scalar coefficients in field-1 then field-2.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field field-1 (:answer-field.type/blank).


- Choice 20c5029e-f1d7-5010-830c-c488b9a19a3d: `2`; correct marker True; recipe k*(2); exact scalar coefficient fragment, no distractors.


Field field-2 (:answer-field.type/blank).


- Choice a64c7100-7ebf-5dc1-a9ef-5db761aa5ae8: `5`; correct marker True; recipe k*(5); exact scalar coefficient fragment, no distractors.


Original worked solution:

First, we note that the denominator of the integrand can be factored as

$$
(x+3)(x-4).
$$

We convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{7x+7}{(x+3)(x-4)} & =\frac{A}{x+3}+\frac{B}{x-4},\end{aligned}
$$

which gives

$$
7x+7=A(x-4)+B(x+3).
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}7(4)+7 & =A(4-4)+B(4+3) \\ 35 & =7B \\ B & =5.\end{aligned}
$$

On the other hand, plugging in $x=-3,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}7(-3)+7 & =A(-3-4)+B(-3+3) \\ -14 & =-7A \\ A & =2.\end{aligned}
$$

Therefore,

$$
\frac{7x+7}{(x+3)(x-4)}=\frac{2}{x+3}+\frac{5}{x-4}.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{7x+7}{(x+3)(x-4)}\,\text{d}x & =2\int \frac{1}{x+3}\,\text{d}x+5\int \frac{1}{x-4}\,\text{d}x \\  & =2\,\operatorname{ln}⁡|x+3|+5\,\operatorname{ln}⁡|x-4|+C.\end{aligned}
$$

## q-348898

Source entity 17592186319308; UUID 9d366a4f-57bf-550b-968a-5c4e774413e6.

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{7x-11}{(x-8)(x+1)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|x-8|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x+1|+C$


Observed pattern: moderate, coefficients; numerator 7*x - 11, ordered linear factors x - 8 and x + 1. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is two scalar coefficients in field-1 then field-2.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field field-1 (:answer-field.type/blank).


- Choice 191068f5-0226-522d-8139-273589d252a5: `5`; correct marker True; recipe k*(5); exact scalar coefficient fragment, no distractors.


Field field-2 (:answer-field.type/blank).


- Choice fee16e3e-8324-5543-ac59-909d500e4767: `2`; correct marker True; recipe k*(2); exact scalar coefficient fragment, no distractors.


Original worked solution:

First, we note that the denominator of the integrand can be factored as

$$
(x-8)(x+1).
$$

We convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{7x-11}{(x-8)(x+1)} & =\frac{A}{x-8}+\frac{B}{x+1},\end{aligned}
$$

which gives

$$
7x-11=A(x+1)+B(x-8).
$$

Plugging in $x=8,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}7(8)-11 & =A(8+1)+B(8-8) \\ 45 & =9A \\ A & =5.\end{aligned}
$$

On the other hand, plugging in $x=-1,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}7(-1)-11 & =A(-1+1)+B(-1-8) \\ -18 & =-9B \\ B & =2.\end{aligned}
$$

Therefore,

$$
\frac{7x-11}{(x-8)(x+1)}=\frac{5}{x-8}+\frac{2}{x+1}.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{7x-11}{(x-8)(x+1)}\,\text{d}x & =5\int \frac{1}{x-8}\,\text{d}x+2\int \frac{1}{x+1}\,\text{d}x \\  & =5\,\operatorname{ln}⁡|x-8|+2\,\operatorname{ln}⁡|x+1|+C.\end{aligned}
$$

## q-348933

Source entity 17592186319310; UUID d78f678c-271e-5e6f-bc0e-d0b4c96c7b22.

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{11}{(2x+5)(x-2)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|2x+5|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x-2|+C$


Observed pattern: moderate, coefficients; numerator 11, ordered linear factors 2*x + 5 and x - 2. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is two scalar coefficients in field-1 then field-2.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field field-1 (:answer-field.type/blank).


- Choice d37eb2c0-6560-554b-bcb1-022f29baa596: `-\frac{11}{9}`; correct marker True; recipe k*(-11/9); exact scalar coefficient fragment, no distractors.


Field field-2 (:answer-field.type/blank).


- Choice af7b29aa-b092-5da7-b4e9-45228ee68f04: `\frac{11}{9}`; correct marker True; recipe k*(11/9); exact scalar coefficient fragment, no distractors.


Original worked solution:

First, we note that the denominator of the integrand can be factored as

$$
(2x+5)(x-2).
$$

We convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{11}{(2x+5)(x-2)} & =\frac{A}{2x+5}+\frac{B}{x-2},\end{aligned}
$$

which gives

$$
11=A(x-2)+B(2x+5).
$$

Plugging in $x=2,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}11 & =9B \\ B & =\frac{11}{9}.\end{aligned}
$$

On the other hand, plugging in $x=-\frac{5}{2},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}11 & =-\frac{9}{2}A \\ A & =-\frac{22}{9}.\end{aligned}
$$

Therefore,

$$
\frac{11}{(2x+5)(x-2)}=-\frac{22}{9(2x+5)}+\frac{11}{9(x-2)}.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{11}{(2x+5)(x-2)}\,\text{d}x & =-\frac{22}{9}\int \frac{1}{2x+5}\,\text{d}x+\frac{11}{9}\int \frac{1}{x-2}\,\text{d}x \\  & =-\frac{11}{9}\,\operatorname{ln}⁡|2x+5|+\frac{11}{9}\,\operatorname{ln}⁡|x-2|+C.\end{aligned}
$$

## q-49903

Source entity 17592186332785; UUID 6d10b74c-0855-5f3d-9ce9-b42a8bd557bc.

$\int \frac{6x+12}{x(x+3)}\,\text{d}x=$


Observed pattern: easy, logs; numerator 6*x + 12, ordered linear factors x and x + 3. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is one complete antiderivative modulo an additive constant.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field selection (:answer-field.type/radio).


- Choice 3093957e-b600-549a-aa94-f6eff16fa62b: `4\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x+3|+C`; correct marker True; recipe k*(4) ln|x| + k*(2) ln|x + 3| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 446fd5ce-d55b-5bca-8c08-7bebb04c4c2c: `\frac{1}{4}\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x+3|+C`; correct marker False; recipe k*(1/4) ln|x| + k*(2) ln|x + 3| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 57610450-810b-53cd-b769-0eeb48828a8a: `\frac{1}{4}\operatorname{ln}⁡|x|+\frac{1}{2}\operatorname{ln}⁡|x+3|+C`; correct marker False; recipe k*(1/4) ln|x| + k*(1/2) ln|x + 3| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 990e7f87-f46f-5c57-8462-75c680e07388: `\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x+3|+C`; correct marker False; recipe k*(1) ln|x| + k*(2) ln|x + 3| + C; equality checked by differentiation on the real pole-free intervals.


- Choice c40af496-e35d-5592-a703-fa0cf0ade2d3: `4\operatorname{ln}⁡|x|+\frac{1}{2}\operatorname{ln}⁡|x+3|+C`; correct marker False; recipe k*(4) ln|x| + k*(1/2) ln|x + 3| + C; equality checked by differentiation on the real pole-free intervals.


Original worked solution:

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{6x+12}{x(x+3)} & =\frac{A}{x}+\frac{B}{x+3},\end{aligned}
$$

which gives

$$
6x+12=A(x+3)+Bx.
$$

Plugging in $x=-3,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}6(-3)+12 & =A(-3+3)+B(-3) \\ -6 & =-3B \\ B & =2\end{aligned}
$$

On the other hand, plugging in $x=0,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}6(0)+12 & =A(0+3)+B(0) \\ 12 & =3A \\ A & =4\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{6x+12}{x(x+3)}=\frac{4}{x}+\frac{2}{x+3}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{6x+12}{x(x+3)}\,\text{d}x & =\int (\frac{4}{x}+\frac{2}{x+3})\text{d}x \\  & =4\int \frac{1}{x}\,\text{d}x+2\int \frac{1}{x+3}\,\text{d}x \\  & =4\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x+3|+C\end{aligned}
$$

## q-49905

Source entity 17592186332786; UUID 2807863a-263b-547c-96e7-4e784ccb6278.

Given that

$$
\int \frac{5x-1}{(x-3)(2x+1)}\,\text{d}x=a\operatorname{ln}⁡|x-3|+b\operatorname{ln}⁡|2x+1|+C,
$$

find the value of $a+b.$


Observed pattern: moderate, sum; numerator 5*x - 1, ordered linear factors x - 3 and 2*x + 1. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is one scalar coefficient sum.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field selection (:answer-field.type/radio).


- Choice 8eb71edc-1611-5574-8e7e-8f7b3936ff0e: `\frac{1}{2}`; correct marker False; recipe k*(1/2); complete observed scalar-bank transport.


- Choice 97f1817a-04e4-55bd-9d46-5de306b15c62: `\frac{3}{2}`; correct marker False; recipe k*(3/2); complete observed scalar-bank transport.


- Choice abcc04b6-41a0-58ce-94e2-8537295db75a: `2`; correct marker False; recipe k*(2); complete observed scalar-bank transport.


- Choice c490eb1b-6330-524a-a5e4-555370670a62: `\frac{5}{2}`; correct marker True; recipe k*(5/2); complete observed scalar-bank transport.


- Choice ffc8d2f7-7152-57db-b954-c96f6cb2f941: `\frac{7}{2}`; correct marker False; recipe k*(7/2); complete observed scalar-bank transport.


Original worked solution:

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{5x-1}{(x-3)(2x+1)} & =\frac{A}{x-3}+\frac{B}{2x+1},\end{aligned}
$$

which gives

$$
5x-1=A(2x+1)+B(x-3).
$$

Plugging in $x=-\frac{1}{2},$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}5(-\frac{1}{2})-1 & =A(2(-\frac{1}{2})+1)+B(-\frac{1}{2}-3) \\ -\frac{7}{2} & =-\frac{7}{2}B \\ B & =1\end{aligned}
$$

On the other hand, plugging in $x=3,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}5(3)-1 & =A(2(3)+1)+B(3-3) \\ 14 & =7A \\ A & =2\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{5x-1}{(x-3)(2x+1)}=\frac{2}{x-3}+\frac{1}{2x+1}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{5x-1}{(x-3)(2x+1)}\,\text{d}x & =\int (\frac{2}{x-3}+\frac{1}{2x+1})\text{d}x \\  & =2\int \frac{1}{x-3}\,\text{d}x+\frac{1}{2}\int \frac{2}{2x+1}\,\text{d}x \\  & =2\operatorname{ln}⁡|x-3|+\frac{1}{2}\operatorname{ln}⁡|2x+1|+C\end{aligned}
$$

Finally, $a=2,b=\frac{1}{2},$ and $a+b=2+\frac{1}{2}=\frac{5}{2}.$

## q-49908

Source entity 17592186332787; UUID b4836967-af93-5f43-b351-fdcfbef30921.

$\int \frac{2}{3{x}^{2}+x}\,\text{d}x=$


Observed pattern: moderate, logs; numerator 2, ordered linear factors x and 3*x + 1. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is one complete antiderivative modulo an additive constant.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field selection (:answer-field.type/radio).


- Choice 1bfc3304-e547-5d93-85cf-d63b46ad634d: `2\operatorname{ln}⁡|x|+\operatorname{ln}⁡|3x+1|+C`; correct marker False; recipe k*(2) ln|x| + k*(1) ln|3*x + 1| + C; equality checked by differentiation on the real pole-free intervals.


- Choice 945ced1f-8fea-5c1d-a75d-ca4b571df7b4: `\frac{1}{2}\operatorname{ln}⁡|x|-\operatorname{ln}⁡|3x+1|+C`; correct marker False; recipe k*(1/2) ln|x| + k*(-1) ln|3*x + 1| + C; equality checked by differentiation on the real pole-free intervals.


- Choice b3053017-09aa-5c07-8524-e09690ea6055: `\frac{1}{2}\operatorname{ln}⁡|x|+\frac{1}{2}\operatorname{ln}⁡|3x+1|+C`; correct marker False; recipe k*(1/2) ln|x| + k*(1/2) ln|3*x + 1| + C; equality checked by differentiation on the real pole-free intervals.


- Choice bf976cda-48d5-50b8-89c7-c7fb49822dfa: `2\operatorname{ln}⁡|x|-2\operatorname{ln}⁡|3x+1|+C`; correct marker True; recipe k*(2) ln|x| + k*(-2) ln|3*x + 1| + C; equality checked by differentiation on the real pole-free intervals.


- Choice fbc85048-9121-59e1-9a1e-20b6d9412725: `2\operatorname{ln}⁡|x|-3\operatorname{ln}⁡|3x+1|+C`; correct marker False; recipe k*(2) ln|x| + k*(-3) ln|3*x + 1| + C; equality checked by differentiation on the real pole-free intervals.


Original worked solution:

First, we note that the denominator of the integrand can be factored as

$$
3{x}^{2}+x=x(3x+1).
$$

We convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2}{x(3x+1)} & =\frac{A}{x}+\frac{B}{(3x+1)},\end{aligned}
$$

which gives

$$
2=A(3x+1)+Bx.
$$

Plugging in $x=-\frac{1}{3},$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}2 & =A(3(-\frac{1}{3})+1)+B(-\frac{1}{3}) \\ 2 & =-\frac{1}{3}B \\ 6 & =-B \\ B & =-6\end{aligned}
$$

On the other hand, plugging in $x=0,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2 & =A(3(0)+1)+B(0) \\ 2 & =A\end{aligned}
$$

Therefore

$$
\begin{aligned}\frac{2}{x(3x+1)}=\frac{2}{x}-\frac{6}{3x+1}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{2}{x(3x+1)}\,\text{d}x & =\int (\frac{2}{x}-\frac{6}{3x+1})\,\text{d}x \\  & =2\int \frac{1}{x}\,\text{d}x-2\int \frac{3}{3x+1}\,\text{d}x \\  & =2\operatorname{ln}⁡|x|-2\operatorname{ln}⁡|3x+1|+C\end{aligned}
$$

## q-103991

Source entity 17592186397787; UUID d8d217e5-8474-5d6b-93f2-6f6e1253c6f4.

Given that

$$
\int \frac{7}{(x-1)(x+6)}\,\text{d}x=a\operatorname{ln}⁡|x-1|+b\operatorname{ln}⁡|x+6|+C,
$$

find the value of $a+b.$


Observed pattern: easy, sum; numerator 7, ordered linear factors x - 1 and x + 6. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is one scalar coefficient sum.


Shared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.


Field selection (:answer-field.type/radio).


- Choice 2ec330cc-8c77-5e4b-b2b9-ffed05aa242e: `2`; correct marker False; recipe k*(2); complete observed scalar-bank transport.


- Choice 7c0961d6-77ee-5ef6-b56f-f97f7519ca2c: `1`; correct marker False; recipe k*(1); complete observed scalar-bank transport.


- Choice 67f68e51-f432-57bf-9c04-5cee503b7449: `0`; correct marker True; recipe k*(0); complete observed scalar-bank transport.


- Choice 297fec68-7633-5a4f-b758-461f512bfa1f: `-1`; correct marker False; recipe k*(-1); complete observed scalar-bank transport.


- Choice fc7e14f3-bd1f-5912-9586-f5fdac2f41f6: `-2`; correct marker False; recipe k*(-2); complete observed scalar-bank transport.


Original worked solution:

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{7}{(x-1)(x+6)} & =\frac{A}{x-1}+\frac{B}{x+6},\end{aligned}
$$

which gives

$$
7=A(x+6)+B(x-1).
$$

Plugging in $x=-6,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}7 & =A(-6+6)+B(-6-1) \\ 7 & =-7B \\ B & =-1\end{aligned}
$$

On the other hand, plugging in $x=1,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}7 & =A(1+6)+B(1-1) \\ 7 & =7A \\ A & =1\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{7}{(x-1)(x+6)} & =\frac{1}{x-1}-\frac{1}{x+6}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{7}{(x-1)(x+6)}\,\text{d}x & =\int (\frac{1}{x-1}-\frac{1}{x+6})\text{d}x \\  & =\int \frac{1}{x-1}\,\text{d}x-\int \frac{1}{x+6}\,\text{d}x \\  & =\operatorname{ln}⁡|x-1|-\operatorname{ln}⁡|x+6|+C.\end{aligned}
$$

Finally, $a=1,b=-1,$ and $a+b=1-1=0.$


## Constraints, calculations and rendering

k must be an integer from 1 through 9; production candidates use 2 through 9. Positive scaling preserves the observed sign pattern and algebraic workload, and exact SymPy rational arithmetic retains fractions. No source pole, leading coefficient, coefficient sum, blank field order or answer count is silently changed. Hard and excluded source profiles raise/reject rather than inventing banks. Before rendering, compute residues at the two poles, divide each by its linear-factor slope to obtain log coefficients, then transport the selected whole source bank. Reject collisions modulo additive constants for primitives or exact scalar equality for other responses. Domain is real x excluding both poles, with separate integration constants allowed on each connected interval.

The exact original prompt, solution and bank strings are replayed at k=1. At k>1 LaTeX notation is normalized while field shape, absolute-value logs, constant C and solution sequence remain. The transport recipe is a documented sampling extension, not a claimed misconception explanation. Every mathematical source bank is replayed in full, and each variant's printed values are independently checked. Unresolved malformed answers remain excluded.

Distinctness uses the reduced printed rational integrand, so equivalent expression forms, seed, UUID, answer order, solution text and profile choice do not establish novelty. A finite generator has 24 easy and 56 moderate candidate integrands before subtracting the database's existing/presented/reserved pool. Exhaustion leaves a finite-limit shortage explicit.
