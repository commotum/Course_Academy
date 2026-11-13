# 17592186049091 Describing Properties of the Cosine Function

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186177064 — Introduction

Let's look again at the graph of the function $y=\cos x.$ 

![](images/88/88378ece5b1721cdc533d07d69c004901539c7f8fda9a5a3e5c5648ed32905c5.png)

The cosine function has infinitely many zeros and an infinite number of points where the function reaches its maximum and minimum value. Let's write general expressions for these properties, assuming $n$ is an integer.

**The Zeros of the Function**

From the graph, we see that the zeros of the function are $$
\displaystyle x=\pm\dfrac{\pi}{2}, \pm \dfrac{3\pi}{2}\dots
$$ 

A general expression for the zeros is

$$
x = \dfrac{\pi}{2} + n\pi.
$$

**The Maxima of the Function**

The function has a maximum when $x=0$ and is periodic with period $2\pi.$ Therefore, a general expression for the values of $x$ that maximize cosine is

$$
x = 2n\pi.
$$

**The Minima of the Function**

The function has a minimum when $x=\pi$ and is periodic with period $2\pi.$ Therefore, a general expression for the values of $x$ that minimize cosine is

$$
x = \pi + 2n\pi.
$$



### example 17592186175693 — Describing Properties of the Cosine Function

Which of the following statements are true regarding the function $y=\cos x?$ Assume that $n$ is an integer.

- The range of the function is $[-1,1].$

- The function has minimum values at $x =n\pi.$

- The function intersects the $x$-axis at $x=\dfrac{\pi}{2} +\pi n.$

First, let's plot the graph of $y=\cos{x}.$

![](images/88/88378ece5b1721cdc533d07d69c004901539c7f8fda9a5a3e5c5648ed32905c5.png)

Now, let's go through each statement.

- Statement I is true. The minimum value is $-1,$ and the maximum value is $1.$ Therefore, the range is $[-1,1].$

- Statement II is false. The function has a minimum at $x=\pi$ and the period is $2\pi.$ Therefore, the minimum values occur at $\pi+2n\pi.$

- Statement III is true. These are the zeros of the cosine curve. The cosine curve has zeros at $x=\dfrac{\pi}{2} + n\pi.$

In conclusion, only statements I and III are true.

### tutorial 17592186177065 — The Periodicity Property of the Cosine Function

Let's look at the graph of the cosine function again.

![](images/04/04f13f2dec860874174f51990f4260615e7be893a6be5f86b3b13857c4e8953f.png)

The periodicity of the function is another characteristic of its graph. The period of the cosine function is $2\pi,$ shown below:

![](images/78/789fa06939a3e3350a18c4e9cdf078bf6baf3f025709703e608cb3b7ba89e698.png)

This means that $\cos\left( x+2n\pi\right) = \cos \left( x\right)$ for any number $x$ and any integer $n.$



### example 17592186175694 — Utilizing the Periodicity Property of the Cosine Function

If $\cos x =- \dfrac {1}{3},$ find the value of $2\cos( x + 4\pi)+3.$

The period of $y = \cos x$ is $2\pi.$ Therefore, for any integer $n$ we have

$$
\cos{x} = \cos{(x+2n\pi)} .
$$

Substituting $n=2$ into the right-hand-side of the above gives

$$
\begin{aligned}\cos ⁡x & =\cos ⁡(x+2\cdot 2\cdot \pi ) \\  & =\cos ⁡(x+4\pi ).\end{aligned}
$$

Therefore, if $\cos{x} =- \dfrac {1}{3},$ then $\cos{(x+4\pi)} = - \dfrac {1}{3}.$

Finally, then

$$
\begin{aligned}2\cos ⁡(x+4\pi )+3 & =2\left(-\frac{1}{3}\right)+3 \\  & =-\frac{2}{3}+3 \\  & =\frac{7}{3}.\end{aligned}
$$

### tutorial 17592186177082 — The Evenness Property of the Cosine Function

Recall that a function $f(x)$ is *even* if it satisfies the property

$$
f(-x) = f(x).
$$

As it turns out, cosine is an even function! So, for any value of $x,$ we have

$$
\cos(-x) = \cos(x).
$$

Even functions are always symmetric about the $y$-axis. This is indeed true of the cosine function, as we can see from the diagram below. 

![](images/b1/b1f44126ba6188d147026b6fe5a4066b0051ec3b638bb2d3e34ee1cbb1708cae.png)

We can use the evenness property of cosine in conjunction with its periodicity property to simplify trigonometric expressions. Let's see an example.



### example 17592186175703 — Utilizing the Evenness Property of the Cosine Function

If $\cos x = \dfrac{\sqrt 3}{4},$ then find the value of $\cos (-x-6\pi).$

First, let's recall the graph of $y=\cos{x}.$

![](images/23/2373daf4b5fd26f098bf90e998e2685db6a8b793e94ac9d80b08ea423cb535c0.png)

From the graph, we note the following:

- The period of $\cos{x}$ is $2\pi.$

- Our graph is symmetric about the $y$-axis. This means that $\cos{x}$ is an *even* function, and we have

$$
\cos(-x) = \cos{x}.
$$

Let's now evaluate our expression:

- Firstly, using the periodicity of $\cos{x},$ we have

$$
\begin{aligned}\cos ⁡(-x-6\pi ) & =\cos ⁡(-x-2\pi \cdot 3) \\  & =\cos ⁡(-x).\end{aligned}
$$

- Secondly, using the evenness of $\cos{x},$ we have

$$
\begin{aligned}\cos ⁡(-x) & =\cos ⁡x \\  & =\frac{\sqrt{3}}{4}.\end{aligned}
$$

Therefore, $\cos (-x-6\pi)= \dfrac{\sqrt 3}{4}.$

## Representative practice (first three per skill; full bank in practice.json)

### Describing Properties of the Cosine Function (38 captured questions)

Question 17592186176448 — None

Which of the following statements are true regarding the function $y = \cos x$? Assume that $n$ is an integer.

Select all that apply.

Solution: Cosine attains its maxima at x=2n*pi, vanishes at x=3pi/2, and has range [-1,1]. Only statement “The function is zero at $x = \frac{3π}{2}$” is true.

Answer The function has maximum values at $x = \frac{π}{2} + nπ$.: false

Answer The function is zero at $x = \frac{3π}{2}$.: true

Answer The range of the function is $[- π, π]$.: false

Question 17592186176449 — None

Which of the following statements are true regarding the function $y = \cos x$? Assume that $n$ is an integer.

Select all that apply.

Solution: Cosine has zeros at x=pi/2+n*pi. At x=3pi/2+2n*pi it is zero, not maximal, and its range is [-1,1]. Only “The zeros of the function are $x = \frac{π}{2} + nπ$” is true.

Answer The function has maximum values at $x = \frac{3π}{2} + 2nπ$.: false

Answer The range of $y = \cos x$ is $[- 1, 0]$.: false

Answer The zeros of the function are $x = \frac{π}{2} + nπ$.: true

Question 17592186235452 — question.difficulty/moderate

Consider the functions $f(x)={x}^{B}+Ax,g(x)=B{e}^{x},$ and $h(x)=\sin ⁡x+1,$ where $A$ and $B$ are constants to be found.

Complete the following facts about the function $y=\sin ⁡x.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
The domain of the function is $x\in ($

                                    
                                
                                    
                            
{{field-1}}                
                                    
                                
                                    
                                        
                                        
$,$

                                    
                                
                                    
                            
{{field-2}}                
                                    
                                
                                    
                                        
                                        
$).$

                                    
                                
                                    
                                        
                                                

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
The range of the function is $[$

                                    
                                
                                    
                            
{{field-3}}                
                                    
                                
                                    
                                        
                                        
$,$

                                    
                                
                                    
                            
{{field-4}}                
                                    
                                
                                    
                                        
                                        
$].$

                                    
                                
                                    
                                        
                                                

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        The period of the function is

                                    
                                
                                    
                            
{{field-5}}                
                                    
                                
                                    
                                        
                                        .

Solution: Let's plot the graph of $y=\sin ⁡x.$

![](images/96/96bd60d23237f836b77a26c5c0461a5c2a474554f0a14266b53fc5e7d999f1b7.png)

Let's go through each statement.

* The domain of the function is $(-\infty ,\infty ).$

* The minimum value is $-1,$ and the maximum value is $1.$ Therefore, the range is $[-1,1].$

* The period of $\sin ⁡x$ is $2\pi .$

Answer field-1: -\infty 

Answer field-2: \infty 

Answer field-3: -1

Answer field-4: 1

Answer field-5: 2\pi 

### Utilizing the Periodicity Property of the Cosine Function (27 captured questions)

Question 17592186176546 — None

If $\cos x = \frac{\sqrt{3}}{2}$, then $4\cos (x - 6π) - 1 =$

Solution: Cosine has period $2\pi$, so $\cos(x-6\pi)=\cos x$. Hence $4\cos(x-6\pi)-1=4(\sqrt3/2)-1=2\sqrt3-1$.

Answer selection: 2\sqrt{3} - 1

Question 17592186176547 — question.difficulty/moderate

If $\cos x =-\frac{1}{\sqrt{3}}$, then $\cos (x + 10π) =$

Solution: The shift $10\pi$ is five full periods, so $\cos(x+10\pi)=\cos x=-1/\sqrt3$.

Answer selection: -\frac{1}{\sqrt{3}}

Question 17592186237984 — question.difficulty/moderate

If $\cos ⁡x=-\frac{5}{8},$ then $\cos ⁡(x+12\pi )=$

Solution: The period of $y=\cos ⁡x$ is $2\pi .$ Therefore, for an integer $n$ we have

$$
\cos ⁡x=\cos ⁡(x+2n\pi ).
$$

Substituting $n=6$ into the right-hand-side of the above gives

$$
\begin{aligned}\cos ⁡x=\cos ⁡(x+2\cdot 6\cdot \pi )=\cos ⁡(x+12\pi ).\end{aligned}
$$

Therefore, if $\cos ⁡x=-\frac{5}{8},$ then $\cos ⁡(x+12\pi )=-\frac{5}{8}.$

Answer selection: -\frac{5}{8}

### Utilizing the Evenness Property of the Cosine Function (23 captured questions)

Question 17592186176346 — question.difficulty/easy

If $\cos ⁡a=-\frac{1}{3},$ then $\cos ⁡(-a)=$

Solution: First, let's recall the graph of $y=\cos ⁡x.$

![](images/23/2373daf4b5fd26f098bf90e998e2685db6a8b793e94ac9d80b08ea423cb535c0.png)

Notice that our graph is symmetric about the $y$-axis. If we reflect the graph over the $y$-axis, we get the same picture. This means that $\cos ⁡x$ is an *even* function, and we have

$$
\cos ⁡(-x)=\cos ⁡x.
$$

Therefore,

$$
\begin{aligned}\cos ⁡(-a) & =\cos ⁡a \\  & =-\frac{1}{3}.\end{aligned}
$$

Answer selection: -\frac{1}{3}

Question 17592186176355 — None

If $\cos x =-\frac{11}{24}$, then $\cos (-x + 16π) =$

Solution: Cosine has period $2\pi$ and is even. Therefore $\cos(-x+16\pi)=\cos(-x)=\cos x=-11/24$.

Answer selection: -\frac{11}{24}

Question 17592186269129 — question.difficulty/easy

If $\cos ⁡x=-\frac{3}{10},$ then $\cos ⁡(-x)=$

Solution: First, let's recall the graph of $y=\cos ⁡x.$

![](images/23/2373daf4b5fd26f098bf90e998e2685db6a8b793e94ac9d80b08ea423cb535c0.png)

Notice that our graph is symmetric about the $y$-axis. If we reflect the graph over the $y$-axis, we get the same picture. This means that $\cos ⁡x$ is an *even* function, and we have

$$
\cos ⁡(-x)=\cos ⁡x.
$$

Therefore,

$$
\begin{aligned}\cos ⁡(-x) & =\cos ⁡x \\  & =-\frac{3}{10}.\end{aligned}
$$

Answer selection: -\frac{3}{10}
