# 17592186050336 The Angle Between Two Vectors

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186107072 — Introduction

Consider the two vectors $\mathbf{a}=\langle 1,-2, 2 \rangle$ and $\mathbf{b}=\langle 3,0,-1 \rangle$ shown in the picture below.

![](images/87/87395f5fe6657cec5dd98eed9c3c535a5f6dc9f259d4558c86a4d618c904e5c1.png)

To find the angle $\theta$ between the vectors, we can rearrange the dot product formula:

$$
\begin{aligned}a\cdot b & =|\,a\,|\cdot |\,b\,|\cdot \operatorname{cos}⁡\theta  \\ \operatorname{cos}⁡\theta  & =\frac{a\cdot b}{|\,a\,||\,b\,|} \\ \theta  & =\operatorname{arccos}⁡\left(\frac{a\cdot b}{|\,a\,||\,b\,|}\right)\end{aligned}
$$

The dot product is given by

$$
\begin{aligned}a\cdot b & ={a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z} \\  & =1\cdot 3+(-2)\cdot 0+2\cdot (-1) \\  & =1,\end{aligned}
$$

and the magnitudes of $\mathbf{a}$ and $\mathbf{b}$ are

$$
\begin{aligned}|\,a\,| & =\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}} \\  & =\sqrt{{1}^{2}+(-2)^{2}+{2}^{2}} \\  & =3, \\ |\,b\,| & =\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}} \\  & =\sqrt{{3}^{2}+{0}^{2}+(-1)^{2}} \\  & =\sqrt{10}.\end{aligned}
$$

Therefore,

$$
\theta = \arccos \Bigg( \dfrac{1}{3\sqrt{10}} \Bigg) \approx 83.9^\circ.
$$



### example 17592186105588 — Finding the Angle Between Two Vectors Given Their Components

Find the angle between $\mathbf{a}=\langle 2,-1,1 \rangle$ and $\mathbf{b}=\langle 1,5,-2 \rangle$. Round your answer to $1$ decimal place.

Rearranging the dot product formula, we have:

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{a\cdot b}{|\,a\,||\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{2\cdot 1+(-1)\cdot 5+1\cdot (-2)}{\sqrt{{2}^{2}+(-1)^{2}+{1}^{2}}\sqrt{{1}^{2}+{5}^{2}+(-2)^{2}}} \\  & =\frac{-5}{\sqrt{6}\cdot \sqrt{30}} \\  & =\frac{-5}{\sqrt{6}\cdot \sqrt{6}\cdot \sqrt{5}} \\  & =-\frac{\sqrt{5}}{6}\end{aligned}
$$

Therefore,

$$
\theta = \arccos \left( -\dfrac{\sqrt{5}}{6} \right) \approx 111.9^\circ.
$$

### example 17592186105589 — Finding the Angle Between Two Vectors Given Three Points

Find $\angle BAC$ given the points $A(2,-1,-5)$, $B(-1,0,-4)$, and $C(5,1,1).$ Round your answer to $1$ decimal place.

Note that the position vectors of the points $A$, $B$, $C$ are

$$
\begin{aligned}a=⟨2,-1,-5⟩,\,b=⟨-1,0,-4⟩,\,c=⟨5,1,1⟩.\end{aligned}
$$

The triangle $\triangle ABC$ is shown (schematically) in the diagram below, where we denote $\angle BAC = \theta.$

![](images/28/285b8343208079181ac6036cf9ca16abc974d59b9262878ed40c0da9af5683d0.png)

First, we find the components of $\overrightarrow{AB}$ and $\overrightarrow{AC}\mathbin{:}$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =⟨-1,0,-4⟩-⟨2,-1,-5⟩ \\  & =⟨-3,1,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =⟨5,1,1⟩-⟨2,-1,-5⟩ \\  & =⟨3,2,6⟩\end{aligned}
$$

Now, the cosine of the angle between $\overrightarrow{AB}$ and $\overrightarrow{AC}$ is

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{\overset{\to }{AB}\cdot \overset{\to }{AC}}{|\overset{\to }{AB}||\overset{\to }{AC}|} \\  & =\frac{-3\cdot 3+1\cdot 2+1\cdot 6}{\sqrt{(-3)^{2}+{1}^{2}+{1}^{2}}\sqrt{{3}^{2}+{2}^{2}+{6}^{2}}} \\  & =\frac{-1}{\sqrt{11}\sqrt{49}} \\  & =-\frac{1}{7\sqrt{11}}.\end{aligned}
$$

Therefore,

$$
\theta = \arccos \left( -\dfrac{1}{7\sqrt{11}} \right) \approx 92.5^\circ.
$$

### example 17592186105606 — Finding the Angle Between Two Vectors Given the Value of Their Dot Product

Given that $\mathbf{a}\cdot \mathbf{b}=-4$, find the angle between $\mathbf{a}=\langle t, \, -2 \rangle$ and $\mathbf{b}=\langle 6, \, t \rangle$. Round your answer to $1$ decimal place.

First, since $\mathbf{a}\cdot \mathbf{b}=-4$, we can solve for $t$, as follows:

$$
\begin{aligned}a\cdot b & =-4 \\ t\cdot 6+(-2)\cdot t & =-4 \\ 6t-2t & =-4 \\ 4t & =-4 \\ t & =-1\end{aligned}
$$

So, 

$$
\begin{aligned}a=⟨-1,-2⟩,\,b=⟨6,-1⟩.\end{aligned}
$$

Now, the cosine of the angle between $\mathbf{a}$ and $\mathbf{b}$ is

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{a\cdot b}{|\,a\,||\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}}\sqrt{{b}_{x}^{2}+{b}_{y}^{2}}} \\  & =\frac{-4}{\sqrt{(-1)^{2}+(-2)^{2}}\cdot \sqrt{{6}^{2}+(-1)^{2}}} \\  & =-\frac{4}{\sqrt{5}\cdot \sqrt{37}} \\  & =-\frac{4}{\sqrt{185}}.\end{aligned}
$$

Therefore,

$$
\theta = \arccos \left( -\dfrac{4}{\sqrt{185}} \right) \approx 107.1^\circ.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Angle Between Two Vectors Given Their Components (18 captured questions)

Question 17592186106097 — question.difficulty/easy

Find the angle between $a=\begin{bmatrix}2 \\ 7\end{bmatrix}$ and $b=\begin{bmatrix}6 \\ 1\end{bmatrix}.$ Round your answer to $1$ decimal place.

Solution: Rearranging the dot product formula, we have:

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{a\cdot b}{|\,a\,||\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}}\sqrt{{b}_{x}^{2}+{b}_{y}^{2}}} \\  & =\frac{2\cdot 6+7\cdot 1}{\sqrt{{2}^{2}+{7}^{2}}\sqrt{{6}^{2}+{1}^{2}}} \\  & =\frac{19}{\sqrt{53}\cdot \sqrt{37}} \\  & =\frac{19}{\sqrt{1961}}\end{aligned}
$$

Therefore,

$$
\theta =\operatorname{arccos}⁡\left(\frac{19}{\sqrt{1961}}\right)≈{64.6}^{∘}.
$$

Answer selection: {64.6}^{∘}

Question 17592186106106 — question.difficulty/easy

Find the angle between $a=⟨3,2,1⟩$ and $b=⟨1,2,3⟩.$ Round your answer to the nearest degree.

Solution: Rearranging the dot product formula, we have:

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{a\cdot b}{|\,a\,||\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{3\cdot 1+2\cdot 2+1\cdot 3}{\sqrt{{3}^{2}+{2}^{2}+{1}^{2}}\sqrt{{1}^{2}+{2}^{2}+{3}^{2}}} \\  & =\frac{10}{\sqrt{14}\cdot \sqrt{14}} \\  & =\frac{10}{14} \\  & =\frac{5}{7}\end{aligned}
$$

Therefore,

$$
\theta =\operatorname{arccos}⁡\left(\frac{5}{7}\right)≈{44}^{∘}.
$$

Answer selection: {44}^{∘}

Question 17592186235514 — question.difficulty/easy

An ambulance service helicopter takes off from a hospital helipad three times on a particular day. The helicopter's location a few seconds after these takeoffs are given by points $P,$ $Q,$ and $R.$

Find the angle $\theta $ between vectors $q$ and $r.$ Round your answer to the nearest degree.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
$\theta =$

                                    
                                
                                    
                            
{{field-1}}                
                                    
                                
                                    
                                        
${}^{∘}$

Solution: To find the angle $\theta $ between the vectors, we can rearrange the dot product formula:

$$
\begin{aligned}q\cdot r & =|\,q\,|\cdot |\,r\,|\cdot \operatorname{cos}⁡\theta  \\ \operatorname{cos}⁡\theta  & =\frac{q\cdot r}{|\,q\,||\,r\,|}\end{aligned}
$$

From part 4, we have $|\,q\,|=\sqrt{13}$ and $|\,r\,|=5.$ Also, from part 5, we have $q\cdot r=-6.$ Therefore, 

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{q\cdot r}{|\,q\,||\,r\,|} \\  & =\frac{(-6)}{\sqrt{13}\cdot 5} \\  & =-\frac{6}{5\sqrt{13}}\end{aligned}
$$

Finally,

$$
\theta =\operatorname{arccos}⁡\left(-\frac{6}{5\sqrt{13}}\right)≈{109}^{∘}.
$$

Answer field-1: 109

### Finding the Angle Between Two Vectors Given Three Points (16 captured questions)

Question 17592186106107 — question.difficulty/moderate

Find $∠QPR$ given the points $P(0,4,5)$, $Q(1,5,4)$, and $R(2,3,6).$

Solution: Note that the position vectors of the points $P$, $Q$, $R$ are

$$
\begin{aligned}p=⟨0,4,5⟩,\,q=⟨1,5,4⟩,\,r=⟨2,3,6⟩.\end{aligned}
$$

The $△PQR$ is shown (schematically) in the diagram below, where we denote $∠QPR=\theta .$ 

![](images/30/3003f0cb329a8f8ef9bc315c70df4773ac1f0c54843dea1208c68bd0f6227bd1.png)

First, we find the components of $\overset{\to }{PQ}$ and $\overset{\to }{PR}$:

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =⟨1,5,4⟩-⟨0,4,5⟩ \\  & =⟨1,1,-1⟩ \\ \overset{\to }{PR} & =r-p \\  & =⟨2,3,6⟩-⟨0,4,5⟩ \\  & =⟨2,-1,1⟩\end{aligned}
$$

Now, the cosine of the angle between $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{\overset{\to }{PQ}\cdot \overset{\to }{PR}}{|\overset{\to }{PQ}||\overset{\to }{PR}|} \\  & =\frac{1\cdot 2+1\cdot (-1)+(-1)\cdot 1}{\sqrt{{1}^{2}+{1}^{2}+(-1)^{2}}\sqrt{{2}^{2}+(-1)^{2}+{1}^{2}}} \\  & =\frac{0}{\sqrt{3}\cdot \sqrt{6}} \\  & =0.\end{aligned}
$$

Therefore,

$$
\theta =\operatorname{arccos}⁡(0)={90}^{∘}.
$$

Answer selection: {90}^{∘}

Question 17592186106108 — question.difficulty/moderate

Find $∠BAC$ given the points $A(3,-3,1)$, $B(5,-3,3)$, and $C(3,-2,3).$ Round your answer to the nearest degree.

Solution: Note that the position vectors of the points $A$, $B$, $C$ are

$$
\begin{aligned}a=⟨3,-3,1⟩,\,b=⟨5,-3,3⟩,\,c=⟨3,-2,3⟩.\end{aligned}
$$

The triangle $△ABC$ is shown (schematically) in the diagram below, where we denote $∠BAC=\theta .$

![](images/28/285b8343208079181ac6036cf9ca16abc974d59b9262878ed40c0da9af5683d0.png)

First, we find the components of $\overset{\to }{AB}$ and $\overset{\to }{AC}$:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =⟨5,-3,3⟩-⟨3,-3,1⟩ \\  & =⟨2,0,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =⟨3,-2,3⟩-⟨3,-3,1⟩ \\  & =⟨0,1,2⟩.\end{aligned}
$$

Now, the cosine of the angle between $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{\overset{\to }{AB}\cdot \overset{\to }{AC}}{|\overset{\to }{AB}||\overset{\to }{AC}|} \\  & =\frac{2\cdot 0+0\cdot 1+2\cdot 2}{\sqrt{{2}^{2}+{0}^{2}+{2}^{2}}\sqrt{{0}^{2}+{1}^{2}+{2}^{2}}} \\  & =\frac{4}{\sqrt{8}\cdot \sqrt{5}} \\  & =\frac{4}{2\sqrt{10}} \\  & =\frac{2}{\sqrt{10}}\,.\end{aligned}
$$

Hence,

$$
\theta =\operatorname{arccos}⁡\left(\frac{2}{\sqrt{10}}\right)≈{51}^{∘}.
$$

Answer selection: {51}^{∘}

Question 17592186237832 — question.difficulty/moderate

Find $∠QPR$ given the points $P(1,5,-1)$, $Q(5,1,1)$, and $R(2,5,0).$

Solution: Note that the position vectors of the points $P$, $Q$, $R$ are

$$
\begin{aligned}p=⟨1,5,-1⟩,\,q=⟨5,1,1⟩,\,r=⟨2,5,0⟩.\end{aligned}
$$

The $△PQR$ is shown (schematically) in the diagram below, where we denote $∠QPR=\theta .$ 

![](images/30/3003f0cb329a8f8ef9bc315c70df4773ac1f0c54843dea1208c68bd0f6227bd1.png)

First, we find the components of $\overset{\to }{PQ}$ and $\overset{\to }{PR}$:

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =⟨5,1,1⟩-⟨1,5,-1⟩ \\  & =⟨4,-4,2⟩ \\ \overset{\to }{PR} & =r-p \\  & =⟨2,5,0⟩-⟨1,5,-1⟩ \\  & =⟨1,0,1⟩\end{aligned}
$$

Now, the cosine of the angle between $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{\overset{\to }{PQ}\cdot \overset{\to }{PR}}{|\overset{\to }{PQ}||\overset{\to }{PR}|} \\  & =\frac{4\cdot 1+(-4)\cdot 0+2\cdot 1}{\sqrt{{4}^{2}+(-4)^{2}+{2}^{2}}\sqrt{{1}^{2}+{0}^{2}+{1}^{2}}} \\  & =\frac{6}{\sqrt{36}\cdot \sqrt{2}} \\  & =\frac{1}{\sqrt{2}}.\end{aligned}
$$

Therefore,

$$
\theta =\operatorname{arccos}⁡\left(\frac{1}{\sqrt{2}}\right)={45}^{∘}.
$$

Answer selection: {45}^{∘}

### Finding the Angle Between Two Vectors Given the Value of Their Dot Product (17 captured questions)

Question 17592186106105 — question.difficulty/moderate

Given that $a\cdot b=-8$, find the angle between $a=⟨2t,2t⟩$ and $b=⟨4,-2⟩.$ Round your answer to $1$ decimal place.

Solution: First, since $a\cdot b=-8$, we can solve for $t$, as follows:

$$
\begin{aligned}a\cdot b & =-8 \\ 2t\cdot 4+2t\cdot (-2) & =-8 \\ 8t-4t & =-8 \\ 4t & =-8 \\ t & =-2\end{aligned}
$$

So, 

$$
\begin{aligned}a & =⟨2(-2),\,2(-2)⟩ \\  & =⟨-4,-4⟩.\end{aligned}
$$

Now, the cosine of the angle between $a$ and $b$ is

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{a\cdot b}{|\,a\,||\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}}\sqrt{{b}_{x}^{2}+{b}_{y}^{2}}} \\  & =\frac{-8}{\sqrt{(-4)^{2}+(-4)^{2}}\sqrt{{4}^{2}+(-2)^{2}}} \\  & =-\frac{8}{4\sqrt{2}\cdot 2\sqrt{5}} \\  & =-\frac{1}{\sqrt{10}}.\end{aligned}
$$

Therefore,

$$
\theta =\operatorname{arccos}⁡\left(-\frac{1}{\sqrt{10}}\right)≈{108.4}^{∘}.
$$

Answer selection: {108.4}^{∘}

Question 17592186106109 — question.difficulty/hard

Consider the points $A(t,2,1)$, $B(2t,3,1)$ and $C(2,{t}^{2},-1).$ Find $∠BAC$ given that $\overset{\to }{AB}\cdot \overset{\to }{AC}=2.$ Round your answer to $2$ decimal places.

Solution: Note that the position vectors of the points $A$, $B$, $C$ are

$$
\begin{aligned}a=⟨t,\,2,\,1⟩,\,b=⟨2t,\,3,\,1⟩,\,c=⟨2,\,{t}^{2},\,-1⟩.\end{aligned}
$$

The triangle $△ABC$ is shown (schematically) in the diagram below, where we denote $∠BAC=\theta .$

![](images/28/285b8343208079181ac6036cf9ca16abc974d59b9262878ed40c0da9af5683d0.png)

First, we find the components of $\overset{\to }{AB}$ and $\overset{\to }{AC}$:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =⟨2t,\,3,\,1⟩-⟨t,\,2,\,1⟩ \\  & =⟨t,\,1,\,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =⟨2,\,{t}^{2},\,-1⟩-⟨t,\,2,\,1⟩ \\  & =⟨2-t,\,{t}^{2}-2,\,-2⟩\end{aligned}
$$

Now, since $\overset{\to }{AB}\cdot \overset{\to }{AC}=2$, we can solve for $t$, as follows:

$$
\begin{aligned}\overset{\to }{AB}\cdot \overset{\to }{AC} & =2 \\ t\cdot (2-t)+1\cdot ({t}^{2}-2)+0\cdot (-2) & =2 \\ 2t-{t}^{2}+{t}^{2}-2+0 & =2 \\ 2t-2 & =2 \\ 2t & =4 \\ t & =2\end{aligned}
$$

So, 

$$
\begin{aligned}\overset{\to }{AB} & =⟨2,1,0⟩, \\ \overset{\to }{AC} & =⟨2-2,\,{2}^{2}-2,\,-2⟩ \\  & =⟨0,2,-2⟩.\end{aligned}
$$

Next, the cosine of the angle between $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{\overset{\to }{AB}\cdot \overset{\to }{AC}}{|\overset{\to }{AB}||\overset{\to }{AC}|} \\  & =\frac{2}{\sqrt{{2}^{2}+{1}^{2}+{0}^{2}}\sqrt{{0}^{2}+{2}^{2}+(-2)^{2}}} \\  & =\frac{2}{\sqrt{5}\cdot \sqrt{8}} \\  & =\frac{2}{2\sqrt{10}} \\  & =\frac{1}{\sqrt{10}}.\end{aligned}
$$

Therefore,

$$
\theta =\operatorname{arccos}⁡\left(\frac{1}{\sqrt{10}}\right)≈{71.57}^{∘}.
$$

Answer selection: {71.57}^{∘}

Question 17592186237837 — question.difficulty/moderate

Given that $a\cdot b=-5$, find the angle between $a=⟨2t,t⟩$ and $b=⟨1,3⟩.$

Solution: First, since $a\cdot b=-5$, we can solve for $t$, as follows:

$$
\begin{aligned}a\cdot b & =-5 \\ 2t\cdot 1+t\cdot 3 & =-5 \\ 2t+3t & =-5 \\ 5t & =-5 \\ t & =-1\end{aligned}
$$

So, 

$$
\begin{aligned}a & =⟨2(-1),\,(-1)⟩ \\  & =⟨-2,-1⟩.\end{aligned}
$$

Now, the cosine of the angle between $a$ and $b$ is

$$
\begin{aligned}\operatorname{cos}⁡\theta  & =\frac{a\cdot b}{|\,a\,||\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}}\sqrt{{b}_{x}^{2}+{b}_{y}^{2}}} \\  & =\frac{-5}{\sqrt{(-2)^{2}+(-1)^{2}}\sqrt{{1}^{2}+{3}^{2}}} \\  & =-\frac{5}{\sqrt{5}\cdot \sqrt{10}} \\  & =-\frac{5}{5\sqrt{2}} \\  & =-\frac{1}{\sqrt{2}}.\end{aligned}
$$

Therefore,

$$
\theta =\operatorname{arccos}⁡\left(-\frac{1}{\sqrt{2}}\right)={135}^{∘}.
$$

Answer selection: {135}^{∘}
