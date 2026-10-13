# Arc length review

Source: math basis 1356, captured provenance retained in source.json. Original plots were inspected (source-plots-0–2.png). Generated variants are labeled below. Raw source solution punctuation is retained as evidence; q-20907 receives one closing-parenthesis repair in normal output.


## q-10255 (hard, radio)

### Original captured question

![](images/ac/ac040bc2c3eb943f947f34602c7c03e90f18e129a0fa7749d8ae60faaab12f71.png)

Find the arc length of the curve defined parametrically as

$$
x=t-\operatorname{sin}⁡t,\,y=1-\operatorname{cos}⁡t,\,t\in [0,\pi ].
$$

- $\pi $
- $4\pi $
- $\frac{\pi }{2}$
- $2\pi $
- $4$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(t-\operatorname{sin}⁡t)=1-\operatorname{cos}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(1-\operatorname{cos}⁡t)=\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{{(1-\operatorname{cos}⁡t)}^{2}+{(\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{1-2\operatorname{cos}⁡t+{cos}^{2}⁡t+{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{2-2\operatorname{cos}⁡t}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2\theta )=1-2{sin}^{2}⁡\theta .$ Substituting $\theta =\frac{t}{2},$ we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2\cdot \frac{t}{2}) & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ \operatorname{cos}⁡t & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ 1-\operatorname{cos}⁡t & =2{sin}^{2}⁡(\frac{t}{2}) \\ 2-2\operatorname{cos}⁡t & =4{sin}^{2}⁡(\frac{t}{2})\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\pi }\sqrt{2-2\operatorname{cos}⁡t}\,\text{d}t & ={\int }_{0}^{\pi }\sqrt{4{sin}^{2}⁡(\frac{t}{2})}\,\text{d}t \\  & =2{\int }_{0}^{\pi }\operatorname{sin}⁡(\frac{t}{2})\text{d}t \\  & =-2\cdot 2\cdot {\operatorname{cos}⁡(\frac{t}{2})|}_{0}^{\pi } \\  & =-4(\operatorname{cos}⁡(\frac{\pi }{2})-\operatorname{cos}⁡0) \\  & =-4(0-1) \\  & =4.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/2ac3abb74d81279f9567efc1350a0c3c45d24d1d897e2b997d9263a27a42a35c.png)

Find the arc length of the curve defined parametrically as

$$
x=t-\operatorname{sin}⁡t,\,y=1-\operatorname{cos}⁡t,\,t\in [0,\frac{2 \pi}{3}].
$$

- $\frac{2 \sqrt{3} \pi}{3}$
- $- \sqrt{3} + \frac{4 \pi}{3}$
- $1$
- $4$
- $2$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(t-\operatorname{sin}⁡t)=1-\operatorname{cos}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(1-\operatorname{cos}⁡t)=\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{{(1-\operatorname{cos}⁡t)}^{2}+{(\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{1-2\operatorname{cos}⁡t+{cos}^{2}⁡t+{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{2-2\operatorname{cos}⁡t}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2\theta )=1-2{sin}^{2}⁡\theta .$ Substituting $\theta =\frac{t}{2},$ we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2\cdot \frac{t}{2}) & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ \operatorname{cos}⁡t & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ 1-\operatorname{cos}⁡t & =2{sin}^{2}⁡(\frac{t}{2}) \\ 2-2\operatorname{cos}⁡t & =4{sin}^{2}⁡(\frac{t}{2})\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\frac{2 \pi}{3}}\sqrt{2-2\operatorname{cos}⁡t}\,\text{d}t & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{4{sin}^{2}⁡(\frac{t}{2})}\,\text{d}t \\  & =2{\int }_{0}^{\frac{2 \pi}{3}}\operatorname{sin}⁡(\frac{t}{2})\text{d}t \\  & =-2\cdot 2\cdot {\operatorname{cos}⁡(\frac{t}{2})|}_{0}^{\frac{2 \pi}{3}} \\  & =-4(\operatorname{cos}⁡(\frac{\pi}{3})-\operatorname{cos}⁡0) \\  & =-4(\frac{1}{2}-1) \\  & =2.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/c2fafe403fb1df06cd3e450bf22248ebe7c6174066b58305453c4eb6bdcc7785.png)

Find the arc length of the curve defined parametrically as

$$
x=5\left(t-\operatorname{sin}⁡t\right),\,y=5\left(1-\operatorname{cos}⁡t\right),\,t\in [0,\frac{2 \pi}{3}].
$$

- $20$
- $- 25 \sqrt{3} + \frac{100 \pi}{3}$
- $5$
- $10$
- $\frac{10 \sqrt{3} \pi}{3}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(t-\operatorname{sin}⁡t\right))=5\left(1-\operatorname{cos}⁡t\right) \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(1-\operatorname{cos}⁡t\right))=5\left(\operatorname{sin}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left({(1-\operatorname{cos}⁡t)}^{2}+{(\operatorname{sin}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(1-2\operatorname{cos}⁡t+{cos}^{2}⁡t+{sin}^{2}⁡t\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(2-2\operatorname{cos}⁡t\right)}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2\theta )=1-2{sin}^{2}⁡\theta .$ Substituting $\theta =\frac{t}{2},$ we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2\cdot \frac{t}{2}) & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ \operatorname{cos}⁡t & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ 1-\operatorname{cos}⁡t & =2{sin}^{2}⁡(\frac{t}{2}) \\ 2-2\operatorname{cos}⁡t & =4{sin}^{2}⁡(\frac{t}{2})\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(2-2\operatorname{cos}⁡t\right)}\,\text{d}t & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(4{sin}^{2}⁡(\frac{t}{2})\right)}\,\text{d}t \\  & =2\cdot 5\cdot {\int }_{0}^{\frac{2 \pi}{3}}\operatorname{sin}⁡(\frac{t}{2})\text{d}t \\  & =5\left(-2\cdot 2\cdot {\operatorname{cos}⁡(\frac{t}{2})}\right){|}_{0}^{\frac{2 \pi}{3}} \\  & =5\left(-4(\operatorname{cos}⁡(\frac{\pi}{3})-\operatorname{cos}⁡0)\right) \\  & =5\left(-4(\frac{1}{2}-1)\right) \\  & =5\left(2\right). \end{aligned}
$$


## q-10260 (easy, radio)

### Original captured question

![](images/51/5117030d23370b2167513b7a2eee5258aae4eb9f45ad428fd82e4334c4ce6638.png)

Find the arc length of the curve defined parametrically as

$$
x=1+3t,\,y=2{t}^{3/2},\,t\in [0,1].
$$

- $2\sqrt{\pi }-\pi $
- $4\sqrt{2}-2$
- $8\sqrt{2}-\pi $
- $\pi $
- $2\sqrt{2}-2$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(1+3t)=3\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2{t}^{3/2})=3{t}^{1/2}.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{{3}^{2}+{(3{t}^{1/2})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{9+9t}\,\text{d}t \\  & =3{\int }_{0}^{1}(1+t)^{1/2}\,\text{d}t \\  & =3\cdot {\frac{2}{3}(1+t)^{3/2}|}_{0}^{1} \\  & =2\sqrt{8}-2 \\  & =4\sqrt{2}-2.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/1c63af82b7fd67b1e1a6557108845a2d247fdaca735ee28ca05d65fb5fb2809b.png)

Find the arc length of the curve defined parametrically as

$$
x=1+3t,\,y=2{t}^{3/2},\,t\in [0,3].
$$

- $18$
- $\frac{135}{2}$
- $7$
- $28$
- $14$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(1+3t)=3\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2{t}^{3/2})=3{t}^{1/2}.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{{3}^{2}+{(3{t}^{1/2})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{9+9t}\,\text{d}t \\  & =3{\int }_{0}^{3}(1+t)^{1/2}\,\text{d}t \\  & =3\cdot {\frac{2}{3}(1+t)^{3/2}|}_{0}^{3} \\  & =2\sqrt{64}-2 \\  & =14.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/ef159cbc6f185dcaf9bfba56e0668632cba1b3be1c986b5d4cd9f45a21873742.png)

Find the arc length of the curve defined parametrically as

$$
x=5\left(1+3t\right),\,y=5\left(2{t}^{3/2}\right),\,t\in [0,3].
$$

- $140$
- $\frac{3375}{2}$
- $35$
- $70$
- $90$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(1+3t\right))=5\left(3\right) \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(2{t}^{3/2}\right))=5\left(3{t}^{1/2}\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left({3}^{2}+{(3{t}^{1/2})}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left(9+9t\right)}\,\text{d}t \\  & =3\cdot 5\cdot {\int }_{0}^{3}(1+t)^{1/2}\,\text{d}t \\  & =5\left(3\cdot {\frac{2}{3}(1+t)^{3/2}}\right){|}_{0}^{3} \\  & =5\left(2\sqrt{64}-2\right) \\  & =5\left(14\right). \end{aligned}
$$


## q-10256 (moderate, radio)

### Original captured question

![](images/da/da529910e268ea4c124d7c27b085ca1799e255604459c539cc8d5809dda8f95a.png)

Find the arc length of the curve defined parametrically as

$$
x={sin}^{3}⁡t,\,y={cos}^{3}⁡t,\,t\in [0,\frac{\pi }{2}].
$$

- $\frac{3}{2}$
- $1$
- $\frac{2}{3}$
- $\frac{3}{4}$
- $\frac{4}{3}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({sin}^{3}⁡t)=3{sin}^{2}⁡t\operatorname{cos}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({cos}^{3}⁡t)=-3{cos}^{2}⁡t\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{{(3{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}+{(-3{cos}^{2}⁡t\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{9{sin}^{4}⁡t{cos}^{2}⁡t+9{cos}^{4}⁡t{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{9{sin}^{2}⁡t{cos}^{2}⁡t({sin}^{2}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}3\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =\frac{3}{2}{\int }_{0}^{\pi /2}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =-\frac{3}{4}\operatorname{cos}⁡(2t){|}_{0}^{\pi /2} \\  & =-\frac{3}{4}(\operatorname{cos}⁡\pi -\operatorname{cos}⁡0) \\  & =-\frac{3}{4}(-1-1) \\  & =\frac{3}{2}.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/d1e67580acd526d467daad4c06b20742c0cf4611040d601c950f949248e0c156.png)

Find the arc length of the curve defined parametrically as

$$
x={sin}^{3}⁡t,\,y={cos}^{3}⁡t,\,t\in [0,\frac{\pi}{3}].
$$

- $\frac{\sqrt{3} \pi}{4}$
- $\frac{9 \sqrt{3}}{64} + \frac{3 \pi}{8}$
- $\frac{9}{16}$
- $\frac{9}{4}$
- $\frac{9}{8}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({sin}^{3}⁡t)=3{sin}^{2}⁡t\operatorname{cos}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({cos}^{3}⁡t)=-3{cos}^{2}⁡t\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{{(3{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}+{(-3{cos}^{2}⁡t\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{9{sin}^{4}⁡t{cos}^{2}⁡t+9{cos}^{4}⁡t{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{9{sin}^{2}⁡t{cos}^{2}⁡t({sin}^{2}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}3\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =\frac{3}{2}{\int }_{0}^{\frac{\pi}{3}}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =-\frac{3}{4}\operatorname{cos}⁡(2t){|}_{0}^{\frac{\pi}{3}} \\  & =-\frac{3}{4}(\operatorname{cos}⁡(\frac{2 \pi}{3})-\operatorname{cos}⁡0) \\  & =-\frac{3}{4}(- \frac{1}{2}-1) \\  & =\frac{9}{8}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/8bee81c0aeac9a62fb2a78add8445a3f06dea6f77ff50279b765a5976392e206.png)

Find the arc length of the curve defined parametrically as

$$
x=5\left({sin}^{3}⁡t\right),\,y=5\left({cos}^{3}⁡t\right),\,t\in [0,\frac{3 \pi}{8}].
$$

- $\frac{15 \sqrt{2}}{4} + \frac{15}{2}$
- $\frac{225}{32} + \frac{675 \pi}{64}$
- $\frac{15 \sqrt{2}}{16} + \frac{15}{8}$
- $\frac{15 \sqrt{2}}{8} + \frac{15}{4}$
- $\frac{45 \sqrt{2} \pi}{32}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left({sin}^{3}⁡t\right))=5\left(3{sin}^{2}⁡t\operatorname{cos}⁡t\right) \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left({cos}^{3}⁡t\right))=5\left(-3{cos}^{2}⁡t\operatorname{sin}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left({(3{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}+{(-3{cos}^{2}⁡t\operatorname{sin}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left(9{sin}^{4}⁡t{cos}^{2}⁡t+9{cos}^{4}⁡t{sin}^{2}⁡t\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left(9{sin}^{2}⁡t{cos}^{2}⁡t({sin}^{2}⁡t+{cos}^{2}⁡t)\right)}\,\text{d}t \\  & =5\cdot {\int }_{0}^{\frac{3 \pi}{8}}3\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =\frac{3}{2}\cdot 5\cdot {\int }_{0}^{\frac{3 \pi}{8}}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =5\left(-\frac{3}{4}\operatorname{cos}⁡(2t)\right){|}_{0}^{\frac{3 \pi}{8}} \\  & =5\left(-\frac{3}{4}(\operatorname{cos}⁡(\frac{3 \pi}{4})-\operatorname{cos}⁡0)\right) \\  & =5\left(-\frac{3}{4}(- \frac{\sqrt{2}}{2}-1)\right) \\  & =5\left(\frac{3 \sqrt{2}}{8} + \frac{3}{4}\right). \end{aligned}
$$


## q-10257 (moderate, radio)

### Original captured question

Find the arc length of the curve defined parametrically as

$$
x=2{cos}^{3}⁡t,\,y=2{sin}^{3}⁡t,\,t\in [0,\frac{\pi }{2}].
$$

- $\frac{3}{2}$
- $1$
- $\frac{2}{3}$
- $\frac{1}{2}$
- $3$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2{cos}^{3}⁡t)=-6{cos}^{2}⁡t\operatorname{sin}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2{sin}^{3}⁡t)=6{sin}^{2}⁡t\operatorname{cos}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{{(-6{cos}^{2}⁡t\operatorname{sin}⁡t)}^{2}+{(6{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{36{cos}^{4}⁡t{sin}^{2}⁡t+36{sin}^{4}⁡t{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{36{sin}^{2}⁡t{cos}^{2}⁡t({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}6\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =3{\int }_{0}^{\pi /2}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =-\frac{3}{2}\operatorname{cos}⁡(2t){|}_{0}^{\pi /2} \\  & =-\frac{3}{2}(\operatorname{cos}⁡\pi -\operatorname{cos}⁡0) \\  & =-\frac{3}{2}(-1-1) \\  & =3.\end{aligned}
$$


### Generated variant (seed 23)

Find the arc length of the curve defined parametrically as

$$
x=2{cos}^{3}⁡t,\,y=2{sin}^{3}⁡t,\,t\in [0,\frac{\pi}{3}].
$$

- $\frac{\sqrt{3} \pi}{2}$
- $\frac{9 \sqrt{3}}{16} + \frac{3 \pi}{2}$
- $\frac{9}{8}$
- $\frac{9}{2}$
- $\frac{9}{4}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2{cos}^{3}⁡t)=-6{cos}^{2}⁡t\operatorname{sin}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2{sin}^{3}⁡t)=6{sin}^{2}⁡t\operatorname{cos}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{{(-6{cos}^{2}⁡t\operatorname{sin}⁡t)}^{2}+{(6{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{36{cos}^{4}⁡t{sin}^{2}⁡t+36{sin}^{4}⁡t{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{36{sin}^{2}⁡t{cos}^{2}⁡t({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}6\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =3{\int }_{0}^{\frac{\pi}{3}}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =-\frac{3}{2}\operatorname{cos}⁡(2t){|}_{0}^{\frac{\pi}{3}} \\  & =-\frac{3}{2}(\operatorname{cos}⁡(\frac{2 \pi}{3})-\operatorname{cos}⁡0) \\  & =-\frac{3}{2}(- \frac{1}{2}-1) \\  & =\frac{9}{4}.\end{aligned}
$$


### Generated variant (seed 71)

Find the arc length of the curve defined parametrically as

$$
x=5\left(2{cos}^{3}⁡t\right),\,y=5\left(2{sin}^{3}⁡t\right),\,t\in [0,\frac{3 \pi}{8}].
$$

- $\frac{15 \sqrt{2}}{2} + 15$
- $\frac{225}{8} + \frac{675 \pi}{16}$
- $\frac{15 \sqrt{2}}{8} + \frac{15}{4}$
- $\frac{15 \sqrt{2}}{4} + \frac{15}{2}$
- $\frac{45 \sqrt{2} \pi}{16}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(2{cos}^{3}⁡t\right))=5\left(-6{cos}^{2}⁡t\operatorname{sin}⁡t\right) \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(2{sin}^{3}⁡t\right))=5\left(6{sin}^{2}⁡t\operatorname{cos}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left({(-6{cos}^{2}⁡t\operatorname{sin}⁡t)}^{2}+{(6{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left(36{cos}^{4}⁡t{sin}^{2}⁡t+36{sin}^{4}⁡t{cos}^{2}⁡t\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left(36{sin}^{2}⁡t{cos}^{2}⁡t({cos}^{2}⁡t+{sin}^{2}⁡t)\right)}\,\text{d}t \\  & =5\cdot {\int }_{0}^{\frac{3 \pi}{8}}6\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =3\cdot 5\cdot {\int }_{0}^{\frac{3 \pi}{8}}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =5\left(-\frac{3}{2}\operatorname{cos}⁡(2t)\right){|}_{0}^{\frac{3 \pi}{8}} \\  & =5\left(-\frac{3}{2}(\operatorname{cos}⁡(\frac{3 \pi}{4})-\operatorname{cos}⁡0)\right) \\  & =5\left(-\frac{3}{2}(- \frac{\sqrt{2}}{2}-1)\right) \\  & =5\left(\frac{3 \sqrt{2}}{4} + \frac{3}{2}\right). \end{aligned}
$$


## q-10258 (easy, radio)

### Original captured question

Find the arc length of the curve defined parametrically as

$$
x=2(\operatorname{sin}⁡t-t\operatorname{cos}⁡t),\,y=2(\operatorname{cos}⁡t+t\operatorname{sin}⁡t),\,t\in [0,\pi ].
$$

- $\frac{{\pi }^{2}}{4}$
- ${\pi }^{2}$
- $\frac{{\pi }^{2}}{2}$
- $2{\pi }^{2}$
- $\frac{\pi }{4}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2(\operatorname{sin}⁡t-t\operatorname{cos}⁡t)) \\  & =2\operatorname{cos}⁡t-2(\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =2t\operatorname{sin}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2(\operatorname{cos}⁡t+t\operatorname{sin}⁡t)) \\  & =-2\operatorname{sin}⁡t+2(\operatorname{sin}⁡t+t\operatorname{cos}⁡t) \\  & =2t\operatorname{cos}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{{(2t\operatorname{sin}⁡t)}^{2}+{(2t\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{4{t}^{2}({sin}^{2}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & =2{\int }_{0}^{\pi }t\,\text{d}t \\  & =2\cdot {\frac{{t}^{2}}{2}|}_{0}^{\pi } \\  & =2(\frac{{\pi }^{2}}{2}-0) \\  & ={\pi }^{2}.\end{aligned}
$$


### Generated variant (seed 23)

Find the arc length of the curve defined parametrically as

$$
x=2(\operatorname{sin}⁡t-t\operatorname{cos}⁡t),\,y=2(\operatorname{cos}⁡t+t\operatorname{sin}⁡t),\,t\in [0,\frac{5 \pi}{6}].
$$

- $\frac{25 \pi^{2}}{72}$
- $\frac{5 \pi}{3}$
- $\frac{25 \pi^{2}}{18}$
- $\frac{125 \pi^{3}}{162}$
- $\frac{25 \pi^{2}}{36}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2(\operatorname{sin}⁡t-t\operatorname{cos}⁡t)) \\  & =2\operatorname{cos}⁡t-2(\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =2t\operatorname{sin}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2(\operatorname{cos}⁡t+t\operatorname{sin}⁡t)) \\  & =-2\operatorname{sin}⁡t+2(\operatorname{sin}⁡t+t\operatorname{cos}⁡t) \\  & =2t\operatorname{cos}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{(2t\operatorname{sin}⁡t)}^{2}+{(2t\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{4{t}^{2}({sin}^{2}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & =2{\int }_{0}^{\frac{5 \pi}{6}}t\,\text{d}t \\  & =2\cdot {\frac{{t}^{2}}{2}|}_{0}^{\frac{5 \pi}{6}} \\  & =2(\frac{(\frac{5 \pi}{6})^{2}}{2}-0) \\  & =\frac{25 \pi^{2}}{36}.\end{aligned}
$$


### Generated variant (seed 71)

Find the arc length of the curve defined parametrically as

$$
x=5\left(2(\operatorname{sin}⁡t-t\operatorname{cos}⁡t)\right),\,y=5\left(2(\operatorname{cos}⁡t+t\operatorname{sin}⁡t)\right),\,t\in [0,\frac{11 \pi}{12}].
$$

- $\frac{33275 \pi^{3}}{1296}$
- $\frac{55 \pi}{6}$
- $\frac{605 \pi^{2}}{72}$
- $\frac{605 \pi^{2}}{144}$
- $\frac{121 \pi^{2}}{144}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(2(\operatorname{sin}⁡t-t\operatorname{cos}⁡t)\right)) \\  & =5\left(2\operatorname{cos}⁡t-2(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\right) \\  & =5\left(2t\operatorname{sin}⁡t\right) \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(2(\operatorname{cos}⁡t+t\operatorname{sin}⁡t)\right)) \\  & =5\left(-2\operatorname{sin}⁡t+2(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\right) \\  & =5\left(2t\operatorname{cos}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({(2t\operatorname{sin}⁡t)}^{2}+{(2t\operatorname{cos}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left(4{t}^{2}({sin}^{2}⁡t+{cos}^{2}⁡t)\right)}\,\text{d}t \\  & =2\cdot 5\cdot {\int }_{0}^{\frac{11 \pi}{12}}t\,\text{d}t \\  & =5\left(2\cdot {\frac{{t}^{2}}{2}}\right){|}_{0}^{\frac{11 \pi}{12}} \\  & =5\left(2(\frac{(\frac{11 \pi}{12})^{2}}{2}-0)\right) \\  & =5\left(\frac{121 \pi^{2}}{144}\right). \end{aligned}
$$


## q-10261 (hard, radio)

### Original captured question

![](images/82/8288453c2625dac592a51054df332abf8ee49dbf8cbcabaf327c3ffe63b55f71.png)

Find the arc length of the curve defined parametrically as

$$
x=2\operatorname{cos}⁡t-\operatorname{cos}⁡(2t),\,y=2\operatorname{sin}⁡t-\operatorname{sin}⁡(2t),\,t\in [0,\pi ].
$$

- $8$
- $2\pi $
- $1$
- $4\pi $
- $\frac{16}{3}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2\operatorname{cos}⁡t-\operatorname{cos}⁡(2t))=-2\operatorname{sin}⁡t+2\operatorname{sin}⁡(2t)\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t-\operatorname{sin}⁡(2t))=2\operatorname{cos}⁡t-2\operatorname{cos}⁡(2t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{{(-2\operatorname{sin}⁡t+2\operatorname{sin}⁡(2t))}^{2}+{(2\operatorname{cos}⁡t-2\operatorname{cos}⁡(2t))}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{4{sin}^{2}⁡t-8\operatorname{sin}⁡t\operatorname{sin}⁡(2t)+4{sin}^{2}⁡(2t)+4{cos}^{2}⁡t-8\operatorname{cos}⁡t\operatorname{cos}⁡(2t)+4{cos}^{2}⁡(2t)}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{4+4-8(\operatorname{cos}⁡t\operatorname{cos}⁡(2t)+\operatorname{sin}⁡t\operatorname{sin}⁡(2t))}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{8-8\operatorname{cos}⁡(2t-t)}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{8-8\operatorname{cos}⁡t}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2\theta )=1-2{sin}^{2}⁡\theta .$ Substituting $\theta =\frac{t}{2},$ we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2\cdot \frac{t}{2}) & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ \operatorname{cos}⁡t & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ 1-\operatorname{cos}⁡t & =2{sin}^{2}⁡(\frac{t}{2}) \\ 8-8\operatorname{cos}⁡t & =16{sin}^{2}⁡(\frac{t}{2})\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\pi }\sqrt{8-8\operatorname{cos}⁡t}\,\text{d}t & ={\int }_{0}^{\pi }\sqrt{16{sin}^{2}⁡(\frac{t}{2})}\,\text{d}t \\  & =4{\int }_{0}^{\pi }\operatorname{sin}⁡(\frac{t}{2})\,\text{d}t \\  & =-8{\operatorname{cos}⁡(\frac{t}{2})|}_{0}^{\pi } \\  & =-8(\operatorname{cos}⁡(\frac{\pi }{2})-\operatorname{cos}⁡0) \\  & =-8(0-1) \\  & =8.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/f953c47d4a838414993e46154820cb4b6772de0ef24d50a611411a8f9c24bea8.png)

Find the arc length of the curve defined parametrically as

$$
x=2\operatorname{cos}⁡t-\operatorname{cos}⁡(2t),\,y=2\operatorname{sin}⁡t-\operatorname{sin}⁡(2t),\,t\in [0,\frac{2 \pi}{3}].
$$

- $\frac{4 \sqrt{3} \pi}{3}$
- $- 4 \sqrt{3} + \frac{16 \pi}{3}$
- $2$
- $8$
- $4$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2\operatorname{cos}⁡t-\operatorname{cos}⁡(2t))=-2\operatorname{sin}⁡t+2\operatorname{sin}⁡(2t)\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t-\operatorname{sin}⁡(2t))=2\operatorname{cos}⁡t-2\operatorname{cos}⁡(2t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{{(-2\operatorname{sin}⁡t+2\operatorname{sin}⁡(2t))}^{2}+{(2\operatorname{cos}⁡t-2\operatorname{cos}⁡(2t))}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{4{sin}^{2}⁡t-8\operatorname{sin}⁡t\operatorname{sin}⁡(2t)+4{sin}^{2}⁡(2t)+4{cos}^{2}⁡t-8\operatorname{cos}⁡t\operatorname{cos}⁡(2t)+4{cos}^{2}⁡(2t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{4+4-8(\operatorname{cos}⁡t\operatorname{cos}⁡(2t)+\operatorname{sin}⁡t\operatorname{sin}⁡(2t))}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{8-8\operatorname{cos}⁡(2t-t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{8-8\operatorname{cos}⁡t}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2\theta )=1-2{sin}^{2}⁡\theta .$ Substituting $\theta =\frac{t}{2},$ we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2\cdot \frac{t}{2}) & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ \operatorname{cos}⁡t & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ 1-\operatorname{cos}⁡t & =2{sin}^{2}⁡(\frac{t}{2}) \\ 8-8\operatorname{cos}⁡t & =16{sin}^{2}⁡(\frac{t}{2})\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\frac{2 \pi}{3}}\sqrt{8-8\operatorname{cos}⁡t}\,\text{d}t & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{16{sin}^{2}⁡(\frac{t}{2})}\,\text{d}t \\  & =4{\int }_{0}^{\frac{2 \pi}{3}}\operatorname{sin}⁡(\frac{t}{2})\,\text{d}t \\  & =-8{\operatorname{cos}⁡(\frac{t}{2})|}_{0}^{\frac{2 \pi}{3}} \\  & =-8(\operatorname{cos}⁡(\frac{\pi}{3})-\operatorname{cos}⁡0) \\  & =-8(\frac{1}{2}-1) \\  & =4.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/3d127979a038cf328d9632a21d62f090437d6038edba0ffae236bbe108f41aff.png)

Find the arc length of the curve defined parametrically as

$$
x=5\left(2\operatorname{cos}⁡t-\operatorname{cos}⁡(2t)\right),\,y=5\left(2\operatorname{sin}⁡t-\operatorname{sin}⁡(2t)\right),\,t\in [0,\frac{2 \pi}{3}].
$$

- $40$
- $- 100 \sqrt{3} + \frac{400 \pi}{3}$
- $10$
- $20$
- $\frac{20 \sqrt{3} \pi}{3}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(2\operatorname{cos}⁡t-\operatorname{cos}⁡(2t)\right))=5\left(-2\operatorname{sin}⁡t+2\operatorname{sin}⁡(2t)\right) \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(2\operatorname{sin}⁡t-\operatorname{sin}⁡(2t)\right))=5\left(2\operatorname{cos}⁡t-2\operatorname{cos}⁡(2t)\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left({(-2\operatorname{sin}⁡t+2\operatorname{sin}⁡(2t))}^{2}+{(2\operatorname{cos}⁡t-2\operatorname{cos}⁡(2t))}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(4{sin}^{2}⁡t-8\operatorname{sin}⁡t\operatorname{sin}⁡(2t)+4{sin}^{2}⁡(2t)+4{cos}^{2}⁡t-8\operatorname{cos}⁡t\operatorname{cos}⁡(2t)+4{cos}^{2}⁡(2t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(4+4-8(\operatorname{cos}⁡t\operatorname{cos}⁡(2t)+\operatorname{sin}⁡t\operatorname{sin}⁡(2t))\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(8-8\operatorname{cos}⁡(2t-t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(8-8\operatorname{cos}⁡t\right)}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2\theta )=1-2{sin}^{2}⁡\theta .$ Substituting $\theta =\frac{t}{2},$ we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2\cdot \frac{t}{2}) & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ \operatorname{cos}⁡t & =1-2{sin}^{2}⁡(\frac{t}{2}) \\ 1-\operatorname{cos}⁡t & =2{sin}^{2}⁡(\frac{t}{2}) \\ 8-8\operatorname{cos}⁡t & =16{sin}^{2}⁡(\frac{t}{2})\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(8-8\operatorname{cos}⁡t\right)}\,\text{d}t & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{25\left(16{sin}^{2}⁡(\frac{t}{2})\right)}\,\text{d}t \\  & =4\cdot 5\cdot {\int }_{0}^{\frac{2 \pi}{3}}\operatorname{sin}⁡(\frac{t}{2})\,\text{d}t \\  & =5\left(-8{\operatorname{cos}⁡(\frac{t}{2})}\right){|}_{0}^{\frac{2 \pi}{3}} \\  & =5\left(-8(\operatorname{cos}⁡(\frac{\pi}{3})-\operatorname{cos}⁡0)\right) \\  & =5\left(-8(\frac{1}{2}-1)\right) \\  & =5\left(4\right). \end{aligned}
$$


## q-20907 (easy, radio)

### Original captured question

Find the arc length of the curve defined parametrically as

$$
x=4\operatorname{sin}⁡t+5,\,y=4(\operatorname{cos}⁡t+1),\,t\in [0,\frac{\pi }{2}].
$$

- $2\pi $
- $\pi $
- $3\pi $
- $4\pi $
- $5\pi $

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(4\operatorname{sin}⁡t+5))=4\operatorname{cos}⁡(t)\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(4(\operatorname{cos}⁡t+1))=-4\operatorname{sin}⁡(t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{(4\operatorname{cos}⁡(t))^{2}+(-4\operatorname{sin}⁡(t))^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{16{cos}^{2}⁡(t)+16{sin}^{2}⁡(t)}\,\text{d}t \\  & =4{\int }_{0}^{\pi /2}\sqrt{{cos}^{2}⁡(t)+{sin}^{2}⁡(t)}\,\text{d}t \\  & =4{\int }_{0}^{\pi /2}\sqrt{1}\,\text{d}t \\  & =4{\int }_{0}^{\pi /2}\,\text{d}t \\  & =4t{|}_{0}^{\pi /2} \\  & =4(\frac{\pi }{2}-0) \\  & =2\pi .\end{aligned}
$$


### Generated variant (seed 23)

Find the arc length of the curve defined parametrically as

$$
x=4\operatorname{sin}⁡t+5,\,y=4(\operatorname{cos}⁡t+1),\,t\in [0,\frac{5 \pi}{12}].
$$

- $\frac{5 \pi}{6}$
- $\frac{10 \pi}{3}$
- $\frac{20 \pi}{3}$
- $\frac{5 \sqrt{2} \pi}{6}$
- $\frac{5 \pi}{3}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(4\operatorname{sin}⁡t+5)=4\operatorname{cos}⁡(t)\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(4(\operatorname{cos}⁡t+1))=-4\operatorname{sin}⁡(t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{12}}\sqrt{(4\operatorname{cos}⁡(t))^{2}+(-4\operatorname{sin}⁡(t))^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{12}}\sqrt{16{cos}^{2}⁡(t)+16{sin}^{2}⁡(t)}\,\text{d}t \\  & =4{\int }_{0}^{\frac{5 \pi}{12}}\sqrt{{cos}^{2}⁡(t)+{sin}^{2}⁡(t)}\,\text{d}t \\  & =4{\int }_{0}^{\frac{5 \pi}{12}}\sqrt{1}\,\text{d}t \\  & =4{\int }_{0}^{\frac{5 \pi}{12}}\,\text{d}t \\  & =4t{|}_{0}^{\frac{5 \pi}{12}} \\  & =4(\frac{5 \pi}{12}-0) \\  & =\frac{5 \pi}{3}.\end{aligned}
$$


### Generated variant (seed 71)

Find the arc length of the curve defined parametrically as

$$
x=5\left(4\operatorname{sin}⁡t+5\right),\,y=5\left(4(\operatorname{cos}⁡t+1)\right),\,t\in [0,\frac{11 \pi}{24}].
$$

- $\frac{55 \sqrt{2} \pi}{12}$
- $\frac{55 \pi}{3}$
- $\frac{550 \pi}{3}$
- $\frac{55 \pi}{6}$
- $\frac{55 \pi}{12}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(4\operatorname{sin}⁡t+5\right))=5\left(4\operatorname{cos}⁡(t)\right) \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(4(\operatorname{cos}⁡t+1)\right))=5\left(-4\operatorname{sin}⁡(t)\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{24}}\sqrt{25\left((4\operatorname{cos}⁡(t))^{2}+(-4\operatorname{sin}⁡(t))^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{24}}\sqrt{25\left(16{cos}^{2}⁡(t)+16{sin}^{2}⁡(t)\right)}\,\text{d}t \\  & =4{\int }_{0}^{\frac{11 \pi}{24}}\sqrt{25\left({cos}^{2}⁡(t)+{sin}^{2}⁡(t)\right)}\,\text{d}t \\  & =4{\int }_{0}^{\frac{11 \pi}{24}}\sqrt{25\left(1\right)}\,\text{d}t \\  & =4\cdot 5\cdot {\int }_{0}^{\frac{11 \pi}{24}}\,\text{d}t \\  & =5\left(4t\right){|}_{0}^{\frac{11 \pi}{24}} \\  & =5\left(4(\frac{11 \pi}{24}-0)\right) \\  & =5\left(\frac{11 \pi}{6}\right). \end{aligned}
$$


## q-348086 (easy, blank)

### Original captured question

![](images/12/121012fc5671ada263e83ec6d3a897d187ecb3a9d56c8e4331a3c0c608a92622.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=\operatorname{sin}⁡t-t\operatorname{cos}⁡t,\,y=-\operatorname{cos}⁡t-t\operatorname{sin}⁡t,\,t\in [0,\pi ].
$$

Do not round the answer.

$L=$
{{field-1}}

- $\frac{{\pi }^{2}}{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t-t\operatorname{cos}⁡t) \\  & =\operatorname{cos}⁡t-(\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =t\operatorname{sin}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(-\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =\operatorname{sin}⁡t-(\operatorname{sin}⁡t+t\operatorname{cos}⁡t) \\  & =-t\operatorname{cos}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{{(t\operatorname{sin}⁡t)}^{2}+{(-t\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{{t}^{2}{sin}^{2}⁡t+{t}^{2}{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{{t}^{2}({sin}^{2}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }t\,\text{d}t \\  & =\frac{{t}^{2}}{2}\,{|}_{0}^{\pi } \\  & =\frac{{\pi }^{2}}{2}-0 \\  & =\frac{{\pi }^{2}}{2}.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/86c48853c31d2fc20f50f6b51c589898dd11a71c58ea27546cac234783fe10d7.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=\operatorname{sin}⁡t-t\operatorname{cos}⁡t,\,y=-\operatorname{cos}⁡t-t\operatorname{sin}⁡t,\,t\in [0,\frac{5 \pi}{6}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{25 \pi^{2}}{72}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t-t\operatorname{cos}⁡t) \\  & =\operatorname{cos}⁡t-(\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =t\operatorname{sin}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(-\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =\operatorname{sin}⁡t-(\operatorname{sin}⁡t+t\operatorname{cos}⁡t) \\  & =-t\operatorname{cos}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{(t\operatorname{sin}⁡t)}^{2}+{(-t\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{t}^{2}{sin}^{2}⁡t+{t}^{2}{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{t}^{2}({sin}^{2}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}t\,\text{d}t \\  & =\frac{{t}^{2}}{2}\,{|}_{0}^{\frac{5 \pi}{6}} \\  & =\frac{(\frac{5 \pi}{6})^{2}}{2}-0 \\  & =\frac{25 \pi^{2}}{72}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/a66610666be8b84af3aba891dc8fa89ebd3d13865be1b51a8c77ee70e128806f.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=5\left(\operatorname{sin}⁡t-t\operatorname{cos}⁡t\right),\,y=5\left(-\operatorname{cos}⁡t-t\operatorname{sin}⁡t\right),\,t\in [0,\frac{11 \pi}{12}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{605 \pi^{2}}{288}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(\operatorname{sin}⁡t-t\operatorname{cos}⁡t\right)) \\  & =5\left(\operatorname{cos}⁡t-(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\right) \\  & =5\left(t\operatorname{sin}⁡t\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(-\operatorname{cos}⁡t-t\operatorname{sin}⁡t\right)) \\  & =5\left(\operatorname{sin}⁡t-(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\right) \\  & =5\left(-t\operatorname{cos}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({(t\operatorname{sin}⁡t)}^{2}+{(-t\operatorname{cos}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({t}^{2}{sin}^{2}⁡t+{t}^{2}{cos}^{2}⁡t\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({t}^{2}({sin}^{2}⁡t+{cos}^{2}⁡t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({t}^{2}\right)}\,\text{d}t \\  & =5\cdot {\int }_{0}^{\frac{11 \pi}{12}}t\,\text{d}t \\  & =5\left(\frac{{t}^{2}}{2}\,\right){|}_{0}^{\frac{11 \pi}{12}} \\  & =5\left(\frac{(\frac{11 \pi}{12})^{2}}{2}-0\right) \\  & =5\left(\frac{121 \pi^{2}}{288}\right). \end{aligned}
$$


## q-348088 (easy, blank)

### Original captured question

![](images/be/be9e314ed11882842bbf9a74deeb3a994596c8275a4e854ffc66327fa0008058.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=\operatorname{cos}⁡t+t\operatorname{sin}⁡t,\,y=\operatorname{sin}⁡t-t\operatorname{cos}⁡t,\,t\in [0,2\pi ].
$$

Do not round the answer.

$L=$
{{field-1}}

- $2{\pi }^{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t+t\operatorname{sin}⁡t) \\  & =-\operatorname{sin}⁡t+(\operatorname{sin}⁡t+t\operatorname{cos}⁡t) \\  & =t\operatorname{cos}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t-t\operatorname{cos}⁡t) \\  & =\operatorname{cos}⁡t-(\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =t\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{2\pi }\sqrt{{(t\operatorname{cos}⁡t)}^{2}+{(t\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{2\pi }\sqrt{{t}^{2}{cos}^{2}⁡t+{t}^{2}{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{2\pi }\sqrt{{t}^{2}({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{2\pi }\sqrt{{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{2\pi }t\,\text{d}t \\  & =\frac{{t}^{2}}{2}\,{|}_{0}^{2\pi } \\  & =\frac{(2\pi )^{2}}{2}-0 \\  & =2{\pi }^{2}.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/d3a15dc1ddf02850f449a85105a1d2392febed8e56d44329f1feb72592ab72a0.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=\operatorname{cos}⁡t+t\operatorname{sin}⁡t,\,y=\operatorname{sin}⁡t-t\operatorname{cos}⁡t,\,t\in [0,\frac{5 \pi}{6}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{25 \pi^{2}}{72}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t+t\operatorname{sin}⁡t) \\  & =-\operatorname{sin}⁡t+(\operatorname{sin}⁡t+t\operatorname{cos}⁡t) \\  & =t\operatorname{cos}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t-t\operatorname{cos}⁡t) \\  & =\operatorname{cos}⁡t-(\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =t\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{(t\operatorname{cos}⁡t)}^{2}+{(t\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{t}^{2}{cos}^{2}⁡t+{t}^{2}{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{t}^{2}({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}\sqrt{{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{6}}t\,\text{d}t \\  & =\frac{{t}^{2}}{2}\,{|}_{0}^{\frac{5 \pi}{6}} \\  & =\frac{(\frac{5 \pi}{6})^{2}}{2}-0 \\  & =\frac{25 \pi^{2}}{72}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/95cc11bda2ae19d5b817adbe62521186a68a79a75a73dd6743c9637ac7b6a547.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=5\left(\operatorname{cos}⁡t+t\operatorname{sin}⁡t\right),\,y=5\left(\operatorname{sin}⁡t-t\operatorname{cos}⁡t\right),\,t\in [0,\frac{11 \pi}{12}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{605 \pi^{2}}{288}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(\operatorname{cos}⁡t+t\operatorname{sin}⁡t\right)) \\  & =5\left(-\operatorname{sin}⁡t+(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\right) \\  & =5\left(t\operatorname{cos}⁡t\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(\operatorname{sin}⁡t-t\operatorname{cos}⁡t\right)) \\  & =5\left(\operatorname{cos}⁡t-(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\right) \\  & =5\left(t\operatorname{sin}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({(t\operatorname{cos}⁡t)}^{2}+{(t\operatorname{sin}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({t}^{2}{cos}^{2}⁡t+{t}^{2}{sin}^{2}⁡t\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({t}^{2}({cos}^{2}⁡t+{sin}^{2}⁡t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{12}}\sqrt{25\left({t}^{2}\right)}\,\text{d}t \\  & =5\cdot {\int }_{0}^{\frac{11 \pi}{12}}t\,\text{d}t \\  & =5\left(\frac{{t}^{2}}{2}\,\right){|}_{0}^{\frac{11 \pi}{12}} \\  & =5\left(\frac{(\frac{11 \pi}{12})^{2}}{2}-0\right) \\  & =5\left(\frac{121 \pi^{2}}{288}\right). \end{aligned}
$$


## q-351427 (easy, blank)

### Original captured question

![](images/33/33939aec3ac1315771d36714d15b590980197aabf3c169cdea1a1108baf6d0fa.png)

Find the arc length of the curve defined parametrically as

$$
x=3\operatorname{sin}⁡t+2,\,y=3\operatorname{cos}⁡t-4,\,t\in [0,\frac{\pi }{3}].
$$

Do not round the answer.

$L=$
{{field-1}}

- $\pi $

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{sin}⁡t+2) \\  & =3\operatorname{cos}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{cos}⁡t-4) \\  & =-3\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /3}\sqrt{{(3\operatorname{cos}⁡t)}^{2}+{(-3\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /3}\sqrt{9{cos}^{2}⁡t+9{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /3}\sqrt{9({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\pi /3}\sqrt{9}\,\text{d}t \\  & =3{\int }_{0}^{\pi /3}\text{d}t \\  & =3t\,{|}_{0}^{\pi /3} \\  & =3(\frac{\pi }{3}-0) \\  & =\pi .\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/a79b68e549ac4cb1decac44d0a78865688dd3d0267dd71b066c914013b65b8cb.png)

Find the arc length of the curve defined parametrically as

$$
x=3\operatorname{sin}⁡t+2,\,y=3\operatorname{cos}⁡t-4,\,t\in [0,\frac{5 \pi}{12}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{5 \pi}{4}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{sin}⁡t+2) \\  & =3\operatorname{cos}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{cos}⁡t-4) \\  & =-3\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{12}}\sqrt{{(3\operatorname{cos}⁡t)}^{2}+{(-3\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{12}}\sqrt{9{cos}^{2}⁡t+9{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{12}}\sqrt{9({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{5 \pi}{12}}\sqrt{9}\,\text{d}t \\  & =3{\int }_{0}^{\frac{5 \pi}{12}}\text{d}t \\  & =3t\,{|}_{0}^{\frac{5 \pi}{12}} \\  & =3(\frac{5 \pi}{12}-0) \\  & =\frac{5 \pi}{4}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/4782254bfb02871b1005c03caf270533b14a48fdab2bcbdba984e025d1df9661.png)

Find the arc length of the curve defined parametrically as

$$
x=5\left(3\operatorname{sin}⁡t+2\right),\,y=5\left(3\operatorname{cos}⁡t-4\right),\,t\in [0,\frac{11 \pi}{24}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{55 \pi}{8}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(3\operatorname{sin}⁡t+2\right)) \\  & =5\left(3\operatorname{cos}⁡t\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(3\operatorname{cos}⁡t-4\right)) \\  & =5\left(-3\operatorname{sin}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{24}}\sqrt{25\left({(3\operatorname{cos}⁡t)}^{2}+{(-3\operatorname{sin}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{24}}\sqrt{25\left(9{cos}^{2}⁡t+9{sin}^{2}⁡t\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{24}}\sqrt{25\left(9({cos}^{2}⁡t+{sin}^{2}⁡t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{11 \pi}{24}}\sqrt{25\left(9\right)}\,\text{d}t \\  & =3\cdot 5\cdot {\int }_{0}^{\frac{11 \pi}{24}}\text{d}t \\  & =5\left(3t\,\right){|}_{0}^{\frac{11 \pi}{24}} \\  & =5\left(3(\frac{11 \pi}{24}-0)\right) \\  & =5\left(\frac{11 \pi}{8}\right). \end{aligned}
$$


## q-351428 (easy, blank)

### Original captured question

![](images/da/da2526ff7031c9dbc704b59e60c65df14dcd0678427e02c386fc16a86e1fc89c.png)

Find the arc length of the curve defined parametrically as

$$
x=5\operatorname{sin}⁡t-3,\,y=5\operatorname{cos}⁡t+1,\,t\in [\frac{\pi }{5},\frac{\pi }{2}].
$$

Do not round the answer.

$L=$
{{field-1}}

- $\frac{3\pi }{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\operatorname{sin}⁡t-3) \\  & =5\operatorname{cos}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\operatorname{cos}⁡t+1) \\  & =-5\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{\pi /5}^{\pi /2}\sqrt{{(5\operatorname{cos}⁡t)}^{2}+{(-5\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{\pi /5}^{\pi /2}\sqrt{25{cos}^{2}⁡t+25{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{\pi /5}^{\pi /2}\sqrt{25({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{\pi /5}^{\pi /2}\sqrt{25}\,\text{d}t \\  & =5{\int }_{\pi /5}^{\pi /2}\text{d}t \\  & =5t\,{|}_{\pi /5}^{\pi /2} \\  & =5(\frac{\pi }{2}-\frac{\pi }{5}) \\  & =5(\frac{3\pi }{10}) \\  & =\frac{3\pi }{2}.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/edb6f07010190e7fb9bbae766b3b773a5e923fb5ae2ef4dfbbf4f78cf45203dd.png)

Find the arc length of the curve defined parametrically as

$$
x=5\operatorname{sin}⁡t-3,\,y=5\operatorname{cos}⁡t+1,\,t\in [\frac{\pi}{5},\frac{37 \pi}{60}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{25 \pi}{12}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\operatorname{sin}⁡t-3) \\  & =5\operatorname{cos}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\operatorname{cos}⁡t+1) \\  & =-5\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{\frac{\pi}{5}}^{\frac{37 \pi}{60}}\sqrt{{(5\operatorname{cos}⁡t)}^{2}+{(-5\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{\frac{\pi}{5}}^{\frac{37 \pi}{60}}\sqrt{25{cos}^{2}⁡t+25{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{\frac{\pi}{5}}^{\frac{37 \pi}{60}}\sqrt{25({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{\frac{\pi}{5}}^{\frac{37 \pi}{60}}\sqrt{25}\,\text{d}t \\  & =5{\int }_{\frac{\pi}{5}}^{\frac{37 \pi}{60}}\text{d}t \\  & =5t\,{|}_{\frac{\pi}{5}}^{\frac{37 \pi}{60}} \\  & =5(\frac{37 \pi}{60}-\frac{\pi}{5}) \\  & =5(\frac{5 \pi}{12}) \\  & =\frac{25 \pi}{12}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/be8890ea91082fea54de2f8ffe5c5967a3a1c32b7dde320e6ef99bf85c19136c.png)

Find the arc length of the curve defined parametrically as

$$
x=5\left(5\operatorname{sin}⁡t-3\right),\,y=5\left(5\operatorname{cos}⁡t+1\right),\,t\in [\frac{\pi}{5},\frac{79 \pi}{120}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{275 \pi}{24}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(5\operatorname{sin}⁡t-3\right)) \\  & =5\left(5\operatorname{cos}⁡t\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(5\operatorname{cos}⁡t+1\right)) \\  & =5\left(-5\operatorname{sin}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{\frac{\pi}{5}}^{\frac{79 \pi}{120}}\sqrt{25\left({(5\operatorname{cos}⁡t)}^{2}+{(-5\operatorname{sin}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{\frac{\pi}{5}}^{\frac{79 \pi}{120}}\sqrt{25\left(25{cos}^{2}⁡t+25{sin}^{2}⁡t\right)}\,\text{d}t \\  & ={\int }_{\frac{\pi}{5}}^{\frac{79 \pi}{120}}\sqrt{25\left(25({cos}^{2}⁡t+{sin}^{2}⁡t)\right)}\,\text{d}t \\  & ={\int }_{\frac{\pi}{5}}^{\frac{79 \pi}{120}}\sqrt{25\left(25\right)}\,\text{d}t \\  & =5\cdot 5\cdot {\int }_{\frac{\pi}{5}}^{\frac{79 \pi}{120}}\text{d}t \\  & =5\left(5t\,\right){|}_{\frac{\pi}{5}}^{\frac{79 \pi}{120}} \\  & =5\left(5(\frac{79 \pi}{120}-\frac{\pi}{5})\right) \\  & =5\left(5(\frac{11 \pi}{24})\right) \\  & =5\left(\frac{55 \pi}{24}\right). \end{aligned}
$$


## q-351429 (easy, blank)

### Original captured question

![](images/5f/5fdcb137c459d5631db3dc3d02ff33ca0b791619694f1badbe7f3f2d0b19141d.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=\frac{1}{2}{t}^{2},\,y=\frac{1}{3}(2t+1)^{3/2},\,t\in [0,2].
$$

Do not round the answer.

$L=$
{{field-1}}

- $4$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{1}{2}{t}^{2}) \\  & =t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{1}{3}(2t+1)^{3/2}) \\  & =\frac{1}{3}\cdot \frac{3}{2}(2t+1)^{1/2}\cdot 2 \\  & =(2t+1)^{1/2}.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{2}\sqrt{(t)^{2}+{((2t+1)^{1/2})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{2}\sqrt{{t}^{2}+2t+1}\,\text{d}t \\  & ={\int }_{0}^{2}\sqrt{(t+1)^{2}}\,\text{d}t \\  & ={\int }_{0}^{2}|t+1|\,\text{d}t \\  & ={\int }_{0}^{2}(t+1)\,\text{d}t \\  & =(\frac{{t}^{2}}{2}+t)\,{|}_{0}^{2} \\  & =(\frac{4}{2}+2)-0 \\  & =4.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/6647574a10925627df5f2217010cf1dded892b906b8604e4dc73d9fe861bc905.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=\frac{1}{2}{t}^{2},\,y=\frac{1}{3}(2t+1)^{3/2},\,t\in [0,3].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{15}{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{1}{2}{t}^{2}) \\  & =t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{1}{3}(2t+1)^{3/2}) \\  & =\frac{1}{3}\cdot \frac{3}{2}(2t+1)^{1/2}\cdot 2 \\  & =(2t+1)^{1/2}.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{(t)^{2}+{((2t+1)^{1/2})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{{t}^{2}+2t+1}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{(t+1)^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}|t+1|\,\text{d}t \\  & ={\int }_{0}^{3}(t+1)\,\text{d}t \\  & =(\frac{{t}^{2}}{2}+t)\,{|}_{0}^{3} \\  & =(\frac{9}{2}+3)-0 \\  & =\frac{15}{2}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/b412b446aa4ec3e201bf04d1e8c12fc94d5f0891516b938f49f301b354165b58.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=5\left(\frac{1}{2}{t}^{2}\right),\,y=5\left(\frac{1}{3}(2t+1)^{3/2}\right),\,t\in [0,3].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{75}{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(\frac{1}{2}{t}^{2}\right)) \\  & =5\left(t\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(\frac{1}{3}(2t+1)^{3/2}\right)) \\  & =5\left(\frac{1}{3}\cdot \frac{3}{2}(2t+1)^{1/2}\cdot 2\right) \\  & =5\left((2t+1)^{1/2}\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left((t)^{2}+{((2t+1)^{1/2})}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left({t}^{2}+2t+1\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left((t+1)^{2}\right)}\,\text{d}t \\  & =5\cdot {\int }_{0}^{3}|t+1|\,\text{d}t \\  & =5\cdot {\int }_{0}^{3}(t+1)\,\text{d}t \\  & =5\left((\frac{{t}^{2}}{2}+t)\,\right){|}_{0}^{3} \\  & =5\left((\frac{9}{2}+3)-0\right) \\  & =5\left(\frac{15}{2}\right). \end{aligned}
$$


## q-351438 (moderate, blank)

### Original captured question

![](images/19/19f2adedfeac6e4c4af07c3d3742203020e10ce841dd22f8b2e22c36ee2bf8e1.png)

Find the arc length of the curve $L$ defined parametrically as

$$
x={e}^{2t}\operatorname{cos}⁡t,\,y={e}^{2t}\operatorname{sin}⁡t,\,t\in [0,\frac{\pi }{2}].
$$

Do not round the answer.

$L=\frac{\sqrt{5}}{2}(${{field-1}}$)$

- ${e}^{\pi }-1$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({e}^{2t}\operatorname{cos}⁡t) \\  & =2{e}^{2t}\operatorname{cos}⁡t-{e}^{2t}\operatorname{sin}⁡t \\  & ={e}^{2t}(2\operatorname{cos}⁡t-\operatorname{sin}⁡t),\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({e}^{2t}\operatorname{sin}⁡t) \\  & =2{e}^{2t}\operatorname{sin}⁡t+{e}^{2t}\operatorname{cos}⁡t \\  & ={e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{\pi /2}\sqrt{{({e}^{2t}(2\operatorname{cos}⁡t-\operatorname{sin}⁡t))}^{2}+{({e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t))}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{{e}^{4t}{(2\operatorname{cos}⁡t-\operatorname{sin}⁡t)}^{2}+{e}^{4t}{(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{{e}^{4t}({(2\operatorname{cos}⁡t-\operatorname{sin}⁡t)}^{2}+{(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}^{2})}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{{e}^{4t}(4{cos}^{2}⁡t-4\operatorname{cos}⁡t\operatorname{sin}⁡t+{sin}^{2}⁡t+4{sin}^{2}⁡t+4\operatorname{sin}⁡t\operatorname{cos}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{{e}^{4t}(4({cos}^{2}⁡t+{sin}^{2}⁡t)+{sin}^{2}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{5{e}^{4t}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\sqrt{5}\,{e}^{2t}\,\text{d}t \\  & =\sqrt{5}\cdot \frac{{e}^{2t}}{2}\,{|}_{0}^{\pi /2} \\  & =\frac{\sqrt{5}}{2}({e}^{\pi }-1).\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/8821ddda0086e0f0b35caf5d20a9cb0562d887235be77a5eb196fec054720955.png)

Find the arc length of the curve $L$ defined parametrically as

$$
x={e}^{2t}\operatorname{cos}⁡t,\,y={e}^{2t}\operatorname{sin}⁡t,\,t\in [0,\frac{\pi}{4}].
$$

Give an exact answer.

$L=\frac{\sqrt{5}}{2}(${{field-1}}$)$

- $-1 + {e}^{\frac{\pi}{2}}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({e}^{2t}\operatorname{cos}⁡t) \\  & =2{e}^{2t}\operatorname{cos}⁡t-{e}^{2t}\operatorname{sin}⁡t \\  & ={e}^{2t}(2\operatorname{cos}⁡t-\operatorname{sin}⁡t),\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({e}^{2t}\operatorname{sin}⁡t) \\  & =2{e}^{2t}\operatorname{sin}⁡t+{e}^{2t}\operatorname{cos}⁡t \\  & ={e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{{({e}^{2t}(2\operatorname{cos}⁡t-\operatorname{sin}⁡t))}^{2}+{({e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t))}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{{e}^{4t}{(2\operatorname{cos}⁡t-\operatorname{sin}⁡t)}^{2}+{e}^{4t}{(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{{e}^{4t}({(2\operatorname{cos}⁡t-\operatorname{sin}⁡t)}^{2}+{(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}^{2})}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{{e}^{4t}(4{cos}^{2}⁡t-4\operatorname{cos}⁡t\operatorname{sin}⁡t+{sin}^{2}⁡t+4{sin}^{2}⁡t+4\operatorname{sin}⁡t\operatorname{cos}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{{e}^{4t}(4({cos}^{2}⁡t+{sin}^{2}⁡t)+{sin}^{2}⁡t+{cos}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{5{e}^{4t}}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{5}\,{e}^{2t}\,\text{d}t \\  & =\sqrt{5}\cdot \frac{{e}^{2t}}{2}\,{|}_{0}^{\frac{\pi}{4}} \\  & =\frac{\sqrt{5}}{2}({e}^{\frac{\pi}{2}}-1).\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/476ab79c1cf3419cd77424bbbafa6cb0c46b9c41285b70714c2d3bbae9991425.png)

Find the arc length of the curve $L$ defined parametrically as

$$
x=5\left({e}^{2t}\operatorname{cos}⁡t\right),\,y=5\left({e}^{2t}\operatorname{sin}⁡t\right),\,t\in [0,\frac{\pi}{4}].
$$

Give an exact answer.

$L=\frac{5 \sqrt{5}}{2}(${{field-1}}$)$

- $-1 + {e}^{\frac{\pi}{2}}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left({e}^{2t}\operatorname{cos}⁡t\right)) \\  & =5\left(2{e}^{2t}\operatorname{cos}⁡t-{e}^{2t}\operatorname{sin}⁡t\right) \\  & =5\left({e}^{2t}(2\operatorname{cos}⁡t-\operatorname{sin}⁡t)\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left({e}^{2t}\operatorname{sin}⁡t\right)) \\  & =5\left(2{e}^{2t}\operatorname{sin}⁡t+{e}^{2t}\operatorname{cos}⁡t\right) \\  & =5\left({e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{25\left({({e}^{2t}(2\operatorname{cos}⁡t-\operatorname{sin}⁡t))}^{2}+{({e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t))}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{25\left({e}^{4t}{(2\operatorname{cos}⁡t-\operatorname{sin}⁡t)}^{2}+{e}^{4t}{(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{25\left({e}^{4t}({(2\operatorname{cos}⁡t-\operatorname{sin}⁡t)}^{2}+{(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}^{2})\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{25\left({e}^{4t}(4{cos}^{2}⁡t-4\operatorname{cos}⁡t\operatorname{sin}⁡t+{sin}^{2}⁡t+4{sin}^{2}⁡t+4\operatorname{sin}⁡t\operatorname{cos}⁡t+{cos}^{2}⁡t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{25\left({e}^{4t}(4({cos}^{2}⁡t+{sin}^{2}⁡t)+{sin}^{2}⁡t+{cos}^{2}⁡t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{25\left(5{e}^{4t}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{4}}\sqrt{25\left(5\right)}\,{e}^{2t}\,\text{d}t \\  & =5\left(\sqrt{5}\cdot \frac{{e}^{2t}}{2}\,\right){|}_{0}^{\frac{\pi}{4}} \\  & =5\left(\frac{\sqrt{5}}{2}({e}^{\frac{\pi}{2}}-1)\right). \end{aligned}
$$


## q-351439 (moderate, blank)

### Original captured question

![](images/0b/0b9c4ebc430e05ef205e3d8108f2e1649bbc51b1a6b54e8f47b48e7ddad1e9a6.png)

Find the arc length of the curve $L$ defined parametrically as

$$
x=4{cos}^{3}⁡t,\,y=4{sin}^{3}⁡t,\,t\in [0,\frac{\pi }{4}].
$$

Do not round the answer.

$L=$
{{field-1}}

- $3$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(4{cos}^{3}⁡t) \\  & =4\cdot 3{cos}^{2}⁡t\cdot (-\operatorname{sin}⁡t) \\  & =-12\operatorname{sin}⁡t{cos}^{2}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(4{sin}^{3}⁡t) \\  & =4\cdot 3{sin}^{2}⁡t\cdot \operatorname{cos}⁡t \\  & =12{sin}^{2}⁡t\operatorname{cos}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{\pi /4}\sqrt{{(-12\operatorname{sin}⁡t{cos}^{2}⁡t)}^{2}+{(12{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /4}\sqrt{144{sin}^{2}⁡t{cos}^{4}⁡t+144{sin}^{4}⁡t{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /4}\sqrt{144{sin}^{2}⁡t{cos}^{2}⁡t({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\pi /4}\sqrt{144{sin}^{2}⁡t{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /4}12|\operatorname{sin}⁡t\operatorname{cos}⁡t|\,\text{d}t \\  & ={\int }_{0}^{\pi /4}12\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =6{\int }_{0}^{\pi /4}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =-3\operatorname{cos}⁡(2t)\,{|}_{0}^{\pi /4} \\  & =-3\operatorname{cos}⁡(\frac{\pi }{2})+3\operatorname{cos}⁡0 \\  & =3.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/1e1f16b744ef046ad55274b12a76a684bbf9272e0be326d65be5f9b277a6ec57.png)

Find the arc length of the curve $L$ defined parametrically as

$$
x=4{cos}^{3}⁡t,\,y=4{sin}^{3}⁡t,\,t\in [0,\frac{\pi}{3}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{9}{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(4{cos}^{3}⁡t) \\  & =4\cdot 3{cos}^{2}⁡t\cdot (-\operatorname{sin}⁡t) \\  & =-12\operatorname{sin}⁡t{cos}^{2}⁡t,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(4{sin}^{3}⁡t) \\  & =4\cdot 3{sin}^{2}⁡t\cdot \operatorname{cos}⁡t \\  & =12{sin}^{2}⁡t\operatorname{cos}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{{(-12\operatorname{sin}⁡t{cos}^{2}⁡t)}^{2}+{(12{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{144{sin}^{2}⁡t{cos}^{4}⁡t+144{sin}^{4}⁡t{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{144{sin}^{2}⁡t{cos}^{2}⁡t({cos}^{2}⁡t+{sin}^{2}⁡t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}\sqrt{144{sin}^{2}⁡t{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}12|\operatorname{sin}⁡t\operatorname{cos}⁡t|\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{3}}12\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =6{\int }_{0}^{\frac{\pi}{3}}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =-3\operatorname{cos}⁡(2t)\,{|}_{0}^{\frac{\pi}{3}} \\  & =-3\operatorname{cos}⁡(\frac{2 \pi}{3})+3\operatorname{cos}⁡0 \\  & =\frac{9}{2}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/371efc8990445ce7cfa232901273a99e10a6c3fdf558c6c69160aad8c48125b1.png)

Find the arc length of the curve $L$ defined parametrically as

$$
x=5\left(4{cos}^{3}⁡t\right),\,y=5\left(4{sin}^{3}⁡t\right),\,t\in [0,\frac{3 \pi}{8}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{15 \sqrt{2}}{2} + 15$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(4{cos}^{3}⁡t\right)) \\  & =5\left(4\cdot 3{cos}^{2}⁡t\cdot (-\operatorname{sin}⁡t)\right) \\  & =5\left(-12\operatorname{sin}⁡t{cos}^{2}⁡t\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(4{sin}^{3}⁡t\right)) \\  & =5\left(4\cdot 3{sin}^{2}⁡t\cdot \operatorname{cos}⁡t\right) \\  & =5\left(12{sin}^{2}⁡t\operatorname{cos}⁡t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left({(-12\operatorname{sin}⁡t{cos}^{2}⁡t)}^{2}+{(12{sin}^{2}⁡t\operatorname{cos}⁡t)}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left(144{sin}^{2}⁡t{cos}^{4}⁡t+144{sin}^{4}⁡t{cos}^{2}⁡t\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left(144{sin}^{2}⁡t{cos}^{2}⁡t({cos}^{2}⁡t+{sin}^{2}⁡t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{8}}\sqrt{25\left(144{sin}^{2}⁡t{cos}^{2}⁡t\right)}\,\text{d}t \\  & =5\cdot {\int }_{0}^{\frac{3 \pi}{8}}12|\operatorname{sin}⁡t\operatorname{cos}⁡t|\,\text{d}t \\  & =5\cdot {\int }_{0}^{\frac{3 \pi}{8}}12\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & =6\cdot 5\cdot {\int }_{0}^{\frac{3 \pi}{8}}\operatorname{sin}⁡(2t)\,\text{d}t \\  & =5\left(-3\operatorname{cos}⁡(2t)\,\right){|}_{0}^{\frac{3 \pi}{8}} \\  & =5\left(-3\operatorname{cos}⁡(\frac{3 \pi}{4})+3\operatorname{cos}⁡0\right) \\  & =5\left(\frac{3 \sqrt{2}}{2} + 3\right). \end{aligned}
$$


## q-351471 (hard, blank)

### Original captured question

![](images/a4/a4d2cf1820b792d804ab4d1b17ce1f36c0b63e4f406f8692d47f64a823b805f1.png)

Find the arc length of the curve defined parametrically as

$$
x=3\operatorname{cos}⁡t-\operatorname{cos}⁡(3t),\,y=3\operatorname{sin}⁡t-\operatorname{sin}⁡(3t),\,t\in [0,\pi ].
$$

Do not round the answer.

$L=$
{{field-1}}

- $12$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{cos}⁡t-\operatorname{cos}⁡(3t)) \\  & =-3\operatorname{sin}⁡t+3\operatorname{sin}⁡(3t),\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{sin}⁡t-\operatorname{sin}⁡(3t)) \\  & =3\operatorname{cos}⁡t-3\operatorname{cos}⁡(3t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{{(-3\operatorname{sin}⁡t+3\operatorname{sin}⁡(3t))}^{2}+{(3\operatorname{cos}⁡t-3\operatorname{cos}⁡(3t))}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{9{sin}^{2}⁡t-18\operatorname{sin}⁡t\operatorname{sin}⁡(3t)+9{sin}^{2}⁡(3t)+9{cos}^{2}⁡t-18\operatorname{cos}⁡t\operatorname{cos}⁡(3t)+9{cos}^{2}⁡(3t)}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{9+9-18(\operatorname{cos}⁡t\operatorname{cos}⁡(3t)+\operatorname{sin}⁡t\operatorname{sin}⁡(3t))}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{18-18\operatorname{cos}⁡(3t-t)}\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{18-18\operatorname{cos}⁡(2t)}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2t)=1-2{sin}^{2}⁡t.$ Therefore, we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2t) & =1-2{sin}^{2}⁡(t) \\ 1-\operatorname{cos}⁡(2t) & =2{sin}^{2}⁡(t) \\ 18-18\operatorname{cos}⁡(2t) & =36{sin}^{2}⁡(t)\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\pi }\sqrt{18-18\operatorname{cos}⁡(2t)}\,\text{d}t & ={\int }_{0}^{\pi }\sqrt{36{sin}^{2}⁡(t)}\,\text{d}t \\  & =6{\int }_{0}^{\pi }|\operatorname{sin}⁡(t)|\,\text{d}t \\  & =6{\int }_{0}^{\pi }\operatorname{sin}⁡(t)\,\text{d}t \\  & =-6\operatorname{cos}⁡(t)\,{|}_{0}^{\pi } \\  & =-6(\operatorname{cos}⁡(\pi )-\operatorname{cos}⁡0) \\  & =-6(-1-1) \\  & =12.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/21f4742833da28ca417b899f678b45a05f23993c6502a1a1157419908721f571.png)

Find the arc length of the curve defined parametrically as

$$
x=3\operatorname{cos}⁡t-\operatorname{cos}⁡(3t),\,y=3\operatorname{sin}⁡t-\operatorname{sin}⁡(3t),\,t\in [0,\frac{2 \pi}{3}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $9$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{cos}⁡t-\operatorname{cos}⁡(3t)) \\  & =-3\operatorname{sin}⁡t+3\operatorname{sin}⁡(3t),\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{sin}⁡t-\operatorname{sin}⁡(3t)) \\  & =3\operatorname{cos}⁡t-3\operatorname{cos}⁡(3t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{{(-3\operatorname{sin}⁡t+3\operatorname{sin}⁡(3t))}^{2}+{(3\operatorname{cos}⁡t-3\operatorname{cos}⁡(3t))}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{9{sin}^{2}⁡t-18\operatorname{sin}⁡t\operatorname{sin}⁡(3t)+9{sin}^{2}⁡(3t)+9{cos}^{2}⁡t-18\operatorname{cos}⁡t\operatorname{cos}⁡(3t)+9{cos}^{2}⁡(3t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{9+9-18(\operatorname{cos}⁡t\operatorname{cos}⁡(3t)+\operatorname{sin}⁡t\operatorname{sin}⁡(3t))}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{18-18\operatorname{cos}⁡(3t-t)}\,\text{d}t \\  & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{18-18\operatorname{cos}⁡(2t)}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2t)=1-2{sin}^{2}⁡t.$ Therefore, we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2t) & =1-2{sin}^{2}⁡(t) \\ 1-\operatorname{cos}⁡(2t) & =2{sin}^{2}⁡(t) \\ 18-18\operatorname{cos}⁡(2t) & =36{sin}^{2}⁡(t)\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\frac{2 \pi}{3}}\sqrt{18-18\operatorname{cos}⁡(2t)}\,\text{d}t & ={\int }_{0}^{\frac{2 \pi}{3}}\sqrt{36{sin}^{2}⁡(t)}\,\text{d}t \\  & =6{\int }_{0}^{\frac{2 \pi}{3}}|\operatorname{sin}⁡(t)|\,\text{d}t \\  & =6{\int }_{0}^{\frac{2 \pi}{3}}\operatorname{sin}⁡(t)\,\text{d}t \\  & =-6\operatorname{cos}⁡(t)\,{|}_{0}^{\frac{2 \pi}{3}} \\  & =-6(\operatorname{cos}⁡(\frac{2 \pi}{3})-\operatorname{cos}⁡0) \\  & =-6(- \frac{1}{2}-1) \\  & =9.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/c8c7267dfb9a950239cf9d9a6b58c79463c80dc395231ba475c4f39eb604ad1b.png)

Find the arc length of the curve defined parametrically as

$$
x=5\left(3\operatorname{cos}⁡t-\operatorname{cos}⁡(3t)\right),\,y=5\left(3\operatorname{sin}⁡t-\operatorname{sin}⁡(3t)\right),\,t\in [0,\frac{3 \pi}{4}].
$$

Give an exact answer.

$L=$
{{field-1}}

- $15 \sqrt{2} + 30$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(3\operatorname{cos}⁡t-\operatorname{cos}⁡(3t)\right)) \\  & =5\left(-3\operatorname{sin}⁡t+3\operatorname{sin}⁡(3t)\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(3\operatorname{sin}⁡t-\operatorname{sin}⁡(3t)\right)) \\  & =5\left(3\operatorname{cos}⁡t-3\operatorname{cos}⁡(3t)\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{4}}\sqrt{25\left({(-3\operatorname{sin}⁡t+3\operatorname{sin}⁡(3t))}^{2}+{(3\operatorname{cos}⁡t-3\operatorname{cos}⁡(3t))}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{4}}\sqrt{25\left(9{sin}^{2}⁡t-18\operatorname{sin}⁡t\operatorname{sin}⁡(3t)+9{sin}^{2}⁡(3t)+9{cos}^{2}⁡t-18\operatorname{cos}⁡t\operatorname{cos}⁡(3t)+9{cos}^{2}⁡(3t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{4}}\sqrt{25\left(9+9-18(\operatorname{cos}⁡t\operatorname{cos}⁡(3t)+\operatorname{sin}⁡t\operatorname{sin}⁡(3t))\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{4}}\sqrt{25\left(18-18\operatorname{cos}⁡(3t-t)\right)}\,\text{d}t \\  & ={\int }_{0}^{\frac{3 \pi}{4}}\sqrt{25\left(18-18\operatorname{cos}⁡(2t)\right)}\,\text{d}t.\end{aligned}
$$

According to the double-angle formula for cosine, $\operatorname{cos}⁡(2t)=1-2{sin}^{2}⁡t.$ Therefore, we obtain

$$
\begin{aligned}\operatorname{cos}⁡(2t) & =1-2{sin}^{2}⁡(t) \\ 1-\operatorname{cos}⁡(2t) & =2{sin}^{2}⁡(t) \\ 18-18\operatorname{cos}⁡(2t) & =36{sin}^{2}⁡(t)\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\int }_{0}^{\frac{3 \pi}{4}}\sqrt{25\left(18-18\operatorname{cos}⁡(2t)\right)}\,\text{d}t & ={\int }_{0}^{\frac{3 \pi}{4}}\sqrt{25\left(36{sin}^{2}⁡(t)\right)}\,\text{d}t \\  & =6\cdot 5\cdot {\int }_{0}^{\frac{3 \pi}{4}}|\operatorname{sin}⁡(t)|\,\text{d}t \\  & =6\cdot 5\cdot {\int }_{0}^{\frac{3 \pi}{4}}\operatorname{sin}⁡(t)\,\text{d}t \\  & =5\left(-6\operatorname{cos}⁡(t)\,\right){|}_{0}^{\frac{3 \pi}{4}} \\  & =5\left(-6(\operatorname{cos}⁡(\frac{3 \pi}{4})-\operatorname{cos}⁡0)\right) \\  & =5\left(-6(- \frac{\sqrt{2}}{2}-1)\right) \\  & =5\left(3 \sqrt{2} + 6\right). \end{aligned}
$$


## q-351474 (easy, blank)

### Original captured question

![](images/cf/cf06561072376949c6df49aec94b45c57b1cd43fbb031ea7b157ea5dfbac877a.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=\frac{1}{9}(6t+1)^{3/2},\,y=\frac{3}{2}{t}^{2},\,t\in [0,1].
$$

Do not round the answer.

$L=$
{{field-1}}

- $\frac{5}{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{1}{9}(6t+1)^{3/2}) \\  & =\frac{1}{9}\cdot \frac{3}{2}(6t+1)^{1/2}\cdot 6 \\  & =(6t+1)^{1/2},\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{3}{2}{t}^{2}) \\  & =3t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{{((6t+1)^{1/2})}^{2}+(3t)^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{6t+1+9{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{(3t+1)^{2}}\,\text{d}t \\  & ={\int }_{0}^{1}|3t+1|\,\text{d}t \\  & ={\int }_{0}^{1}(3t+1)\,\text{d}t \\  & =(\frac{3{t}^{2}}{2}+t)\,{|}_{0}^{1} \\  & =(\frac{3}{2}+1)-0 \\  & =\frac{5}{2}.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/2fa6303151e1ef0c675562c58c67bfb2d8eec9c153ea982af311b0c620b3ab49.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=\frac{1}{9}(6t+1)^{3/2},\,y=\frac{3}{2}{t}^{2},\,t\in [0,3].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{33}{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{1}{9}(6t+1)^{3/2}) \\  & =\frac{1}{9}\cdot \frac{3}{2}(6t+1)^{1/2}\cdot 6 \\  & =(6t+1)^{1/2},\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{3}{2}{t}^{2}) \\  & =3t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{{((6t+1)^{1/2})}^{2}+(3t)^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{6t+1+9{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{(3t+1)^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}|3t+1|\,\text{d}t \\  & ={\int }_{0}^{3}(3t+1)\,\text{d}t \\  & =(\frac{3{t}^{2}}{2}+t)\,{|}_{0}^{3} \\  & =(\frac{27}{2}+3)-0 \\  & =\frac{33}{2}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/925733162a8f6f1c070441729049ca03b941ef783ec5765b7ec9682f7eecb907.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=5\left(\frac{1}{9}(6t+1)^{3/2}\right),\,y=5\left(\frac{3}{2}{t}^{2}\right),\,t\in [0,3].
$$

Give an exact answer.

$L=$
{{field-1}}

- $\frac{165}{2}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(\frac{1}{9}(6t+1)^{3/2}\right)) \\  & =5\left(\frac{1}{9}\cdot \frac{3}{2}(6t+1)^{1/2}\cdot 6\right) \\  & =5\left((6t+1)^{1/2}\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(\frac{3}{2}{t}^{2}\right)) \\  & =5\left(3t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left({((6t+1)^{1/2})}^{2}+(3t)^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left(6t+1+9{t}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left((3t+1)^{2}\right)}\,\text{d}t \\  & =5\cdot {\int }_{0}^{3}|3t+1|\,\text{d}t \\  & =5\cdot {\int }_{0}^{3}(3t+1)\,\text{d}t \\  & =5\left((\frac{3{t}^{2}}{2}+t)\,\right){|}_{0}^{3} \\  & =5\left((\frac{27}{2}+3)-0\right) \\  & =5\left(\frac{33}{2}\right). \end{aligned}
$$


## q-351505 (easy, blank)

### Original captured question

![](images/89/893efa56ec41ef2242a48831ad4f58b23edc791464ccc7dcb4dd104b87843360.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=t-\frac{{t}^{3}}{3},\,y={t}^{2},\,t\in [0,3].
$$

Do not round the answer.

$L=$
{{field-1}}

- $12$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(t-\frac{{t}^{3}}{3}) \\  & =1-{t}^{2},\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{2}) \\  & =2t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{(1-{t}^{2})^{2}+(2t)^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{1-2{t}^{2}+{t}^{4}+4{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{1+2{t}^{2}+{t}^{4}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{(1+{t}^{2})^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}(1+{t}^{2})\,\text{d}t \\  & =(t+\frac{{t}^{3}}{3})\,{|}_{0}^{3} \\  & =(3+\frac{27}{3})-0 \\  & =12.\end{aligned}
$$


### Generated variant (seed 23)

![](images/89/893efa56ec41ef2242a48831ad4f58b23edc791464ccc7dcb4dd104b87843360.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=t-\frac{{t}^{3}}{3},\,y={t}^{2},\,t\in [0,3].
$$

Give an exact answer.

$L=$
{{field-1}}

- $12$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(t-\frac{{t}^{3}}{3}) \\  & =1-{t}^{2},\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}({t}^{2}) \\  & =2t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{(1-{t}^{2})^{2}+(2t)^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{1-2{t}^{2}+{t}^{4}+4{t}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{1+2{t}^{2}+{t}^{4}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{(1+{t}^{2})^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}(1+{t}^{2})\,\text{d}t \\  & =(t+\frac{{t}^{3}}{3})\,{|}_{0}^{3} \\  & =(3+\frac{27}{3})-0 \\  & =12.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/73a9ff1225befe47efa9486ee6f330c1b87005784e1318c4d3cf29082f3bb2cd.png)

Find the arc length $L$ of the curve defined parametrically as

$$
x=5\left(t-\frac{{t}^{3}}{3}\right),\,y=5\left({t}^{2}\right),\,t\in [0,3].
$$

Give an exact answer.

$L=$
{{field-1}}

- $60$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(t-\frac{{t}^{3}}{3}\right)) \\  & =5\left(1-{t}^{2}\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left({t}^{2}\right)) \\  & =5\left(2t\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length, and get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left((1-{t}^{2})^{2}+(2t)^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left(1-2{t}^{2}+{t}^{4}+4{t}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left(1+2{t}^{2}+{t}^{4}\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left((1+{t}^{2})^{2}\right)}\,\text{d}t \\  & =5\cdot {\int }_{0}^{3}(1+{t}^{2})\,\text{d}t \\  & =5\left((t+\frac{{t}^{3}}{3})\,\right){|}_{0}^{3} \\  & =5\left((3+\frac{27}{3})-0\right) \\  & =5\left(12\right). \end{aligned}
$$


## q-351508 (moderate, blank)

### Original captured question

![](images/a6/a61d1a169971b5e0af320372885cdcbae794d163ab767685ef5b688a083aaadb.png)

Find the arc length of the curve defined parametrically as

$$
x=2+4t,\,y=\frac{8}{3}{t}^{3/2},\,t\in [0,2].
$$

$L=$
{{field-1}}

- $8\sqrt{3}-\frac{8}{3}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2+4t)=4,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{8}{3}{t}^{3/2})=4{t}^{1/2}.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{2}\sqrt{{4}^{2}+{(4{t}^{1/2})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{2}\sqrt{16+16t}\,\text{d}t \\  & =4{\int }_{0}^{2}(1+t)^{1/2}\,\text{d}t \\  & =4\cdot \frac{2}{3}(1+t)^{3/2}\,{|}_{0}^{2} \\  & =\frac{8}{3}({3}^{3/2}-{1}^{3/2}) \\  & =\frac{8}{3}(3\sqrt{3}-1) \\  & =8\sqrt{3}-\frac{8}{3}.\end{aligned}
$$


### Generated variant (seed 23)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/09448515ea67ade70e9a3114641de1b65a9a4c7a172b0d822d58a1bc005c2baf.png)

Find the arc length of the curve defined parametrically as

$$
x=2+4t,\,y=\frac{8}{3}{t}^{3/2},\,t\in [0,3].
$$

$L=$
{{field-1}}

- $\frac{56}{3}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2+4t)=4,\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(\frac{8}{3}{t}^{3/2})=4{t}^{1/2}.\end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{3}\sqrt{{4}^{2}+{(4{t}^{1/2})}^{2}}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{16+16t}\,\text{d}t \\  & =4{\int }_{0}^{3}(1+t)^{1/2}\,\text{d}t \\  & =4\cdot \frac{2}{3}(1+t)^{3/2}\,{|}_{0}^{3} \\  & =\frac{8}{3}((4)^{3/2}-1^{3/2}) \\  & =\frac{8}{3}(8-1) \\  & =\frac{56}{3}.\end{aligned}
$$


### Generated variant (seed 71)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186092377/plots/54628847ddbed53ce05f0b3be8cc04f550fe7cec7c8fa5f49df7d041e86e5e77.png)

Find the arc length of the curve defined parametrically as

$$
x=5\left(2+4t\right),\,y=5\left(\frac{8}{3}{t}^{3/2}\right),\,t\in [0,3].
$$

$L=$
{{field-1}}

- $\frac{280}{3}$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(2+4t\right))=5\left(4\right), \end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\left(\frac{8}{3}{t}^{3/2}\right))=5\left(4{t}^{1/2}\right). \end{aligned}
$$

We substitute these derivatives in the formula for arc length and get

$$
\begin{aligned}L & ={\int }_{0}^{3}\sqrt{25\left({4}^{2}+{(4{t}^{1/2})}^{2}\right)}\,\text{d}t \\  & ={\int }_{0}^{3}\sqrt{25\left(16+16t\right)}\,\text{d}t \\  & =4\cdot 5\cdot {\int }_{0}^{3}(1+t)^{1/2}\,\text{d}t \\  & =5\left(4\cdot \frac{2}{3}(1+t)^{3/2}\,\right){|}_{0}^{3} \\  & =5\left(\frac{8}{3}((4)^{3/2}-1^{3/2})\right) \\  & =5\left(\frac{8}{3}(8-1)\right) \\  & =5\left(\frac{56}{3}\right). \end{aligned}
$$
