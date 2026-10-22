Find the general nonzero real solution to the differential equation

$$
\frac{\text{d}y}{\text{d}x}-y={y}^{2}{e}^{(x+1)}.
$$

Work on an interval where $x+1>0$. Choose constants and intervals on which all displayed real expressions are defined.

{{selection}}

- $y=\frac{2{e}^{(x+1)}}{C-{e}^{2\cdot (x+1)}}$ [key]
- $y=\frac{C-{e}^{(x+1)}}{2{e}^{(x+1)}}$
- $y=\frac{C-{e}^{2\cdot (x+1)}}{2{e}^{(x+1)}}$
- $y=\frac{{e}^{(x+1)}}{C-2{e}^{(x+1)}}$
- $y=\frac{2\cdot (x+1){e}^{(x+1)}}{C-2{e}^{2\cdot (x+1)}}$

Notice that our equation is an instance of the Bernoulli differential equation

$$
\frac{dy}{dx}+p(x)y=q(x){y}^{n}.
$$

In this case, we have

$$
p(x)=-1,\,q(x)={e}^{(x+1)},\,n=2.
$$

First, we divide the differential equation by ${y}^{2},$ and we get

$$
{y}^{-2}\frac{dy}{dx}-{y}^{-1}={e}^{(x+1)}.\,\,(∗)
$$

Then, we make the substitution

$$
z={y}^{1-n}={y}^{-1}.
$$

Differentiating $z(x)$ using the chain rule, we get 

$$
\frac{\text{d}z}{\text{d}x}=-{y}^{-2}\,\frac{\text{d}y}{\text{d}x}\,⟹\,{y}^{-2}\frac{\text{d}y}{\text{d}x}=-\,\frac{\text{d}z}{\text{d}x}.
$$

 

Therefore, the original equation can be written in terms of $z(x)$ as follows:

$$
-\,\frac{\text{d}z}{\text{d}x}-z={e}^{(x+1)}
$$

This differential equation is linear, so we can use the method of integrating factors. But first, we write the above equation in standard form:

$$
\frac{\text{d}z}{\text{d}x}+z=-{e}^{(x+1)}
$$

The above equation is in the standard form

$$
\frac{\text{d}z}{\text{d}x}+P(x)z=Q(x)
$$

with

$$
\begin{aligned}P(x)=1,\,Q(x)=-{e}^{(x+1)}\,.\end{aligned}
$$

We then compute an integrating factor:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (1)\,\text{d}x} \\  & ={e}^{(x+1)}\end{aligned}
$$

Multiplying both sides of the standard form equation by $I(x)={e}^{(x+1)}$ yields

$$
\begin{aligned}{e}^{(x+1)}\cdot (\frac{\text{d}z}{\text{d}x}+z) & ={e}^{(x+1)}\cdot (-{e}^{(x+1)}) \\ {e}^{(x+1)}\cdot \frac{\text{d}z}{\text{d}x}+z{e}^{(x+1)} & =-{e}^{2\cdot (x+1)} \\ \frac{\text{d}}{\text{d}x}(z{e}^{(x+1)}) & =-{e}^{2\cdot (x+1)}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(z{e}^{(x+1)})\,\text{d}x & =-\int {e}^{2\cdot (x+1)}\,\text{d}x \\ z{e}^{(x+1)} & =-\frac{1}{2}{e}^{2\cdot (x+1)}+{C}_{1} \\ z & =\frac{C-{e}^{2\cdot (x+1)}}{2{e}^{(x+1)}},\end{aligned}
$$

where $C=2{C}_{1}.$

Finally, we determine $y(x)$ by writing $z={y}^{-1}.$ This results in

$$
\begin{aligned}{y}^{-1}=\frac{C-{e}^{2\cdot (x+1)}}{2{e}^{(x+1)}}\,⇒\,y=\frac{2{e}^{(x+1)}}{C-{e}^{2\cdot (x+1)}}.\end{aligned}
$$

These are the nonzero real solutions on the specified intervals; exclude denominator zeros and restrict constants and intervals to the real branches used above.

---

Find the general nonzero real solution to the differential equation

$$
\frac{\text{d}y}{\text{d}x}-\frac{y}{(x-3)}=\sqrt{(x-3)}\,{y}^{2}.
$$

Work on an interval where $x-3>0$. Choose constants and intervals on which all displayed real expressions are defined.

{{selection}}

- $y=\frac{5\cdot (x-3)}{C+{(x-3)}^{3/2}}$
- $y=\frac{{(x-3)}^{2}}{C-5{(x-3)}^{5/2}}$
- $y=\frac{5\cdot (x-3)}{C-2{(x-3)}^{5/2}}$ [key]
- $y={(\frac{2\cdot (x-3)}{C-{(x-3)}^{3/2}})}^{2}$
- $y=\pm \sqrt{\frac{(x-3)}{C+{(x-3)}^{5/2}}}$

Notice that our equation is an instance of the Bernoulli differential equation

$$
\frac{dy}{dx}+p(x)y=q(x){y}^{n}.
$$

In this case, we have

$$
p(x)=-\frac{1}{(x-3)},\,q(x)=\sqrt{(x-3)},\,n=2.
$$

First, we divide the differential equation by ${y}^{2},$ and we get

$$
{y}^{-2}\frac{dy}{dx}-\frac{1}{(x-3)}{y}^{-1}=\sqrt{(x-3)}.\,\,(∗)
$$

Then, we make the substitution

$$
z={y}^{1-n}={y}^{-1}.
$$

Differentiating $z(x)$ using the chain rule, we get 

$$
\frac{\text{d}z}{\text{d}x}=-{y}^{-2}\,\frac{\text{d}y}{\text{d}x}\,⟹\,{y}^{-2}\frac{\text{d}y}{\text{d}x}=-\,\frac{\text{d}z}{\text{d}x}.
$$

 

Therefore, the original equation can be written in terms of $z(x)$ as follows:

$$
-\,\frac{\text{d}z}{\text{d}x}-\frac{1}{(x-3)}z=\sqrt{(x-3)}
$$

This differential equation is linear, so we can use the method of integrating factors. But first, we write the above equation in standard form:

$$
\frac{\text{d}z}{\text{d}x}+\frac{1}{(x-3)}z=-\sqrt{(x-3)}
$$

The above equation is in the standard form

$$
\frac{\text{d}z}{\text{d}x}+P(x)z=Q(x)
$$

with

$$
\begin{aligned}P(x)=\frac{1}{(x-3)},\,Q(x)=-\sqrt{(x-3)}\,.\end{aligned}
$$

We then compute an integrating factor:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (1/(x-3))\,\text{d}x} \\  & ={e}^{\operatorname{ln}⁡(x-3)} \\  & =(x-3)\end{aligned}
$$

Multiplying both sides of the standard form equation by $I(x)=(x-3)$ yields

$$
\begin{aligned}(x-3)\cdot (\frac{\text{d}z}{\text{d}x}+\frac{1}{(x-3)}z) & =(x-3)\cdot (-\sqrt{(x-3)}) \\ (x-3)\cdot \frac{\text{d}z}{\text{d}x}+z & =-(x-3)\sqrt{(x-3)} \\ \frac{\text{d}}{\text{d}x}((x-3)z) & =-{(x-3)}^{3/2}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}((x-3)z)\,\text{d}x & =\int -{(x-3)}^{3/2}\,\text{d}x \\ (x-3)z & =-\frac{2{(x-3)}^{5/2}}{5}+{C}_{1} \\ z & =\frac{C-2{(x-3)}^{5/2}}{5\cdot (x-3)},\end{aligned}
$$

where $C=5{C}_{1}.$

Finally, we determine $y(x)$ by writing $z={y}^{-1}.$ This results in

$$
\begin{aligned}{y}^{-1}=\frac{C-2{(x-3)}^{5/2}}{5\cdot (x-3)}\,⇒\,y=\frac{5\cdot (x-3)}{C-2{(x-3)}^{5/2}}.\end{aligned}
$$

These are the nonzero real solutions on the specified intervals; exclude denominator zeros and restrict constants and intervals to the real branches used above.

---

Find the general nonzero real solution to the differential equation

$$
\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}+2\cdot (x+1)y}{{(x+1)}^{2}}.
$$

Work on an interval where $x+1>0$. Choose constants and intervals on which all displayed real expressions are defined.

{{selection}}

- $y=\frac{{(x+1)}^{2}}{C-(x+1)}$ [key]
- $y=\frac{(x+1)+C}{{(x+1)}^{3}}$
- $y=\frac{C-(x+1)}{2{(x+1)}^{2}}$
- $y=\frac{{(x+1)}^{2}}{C\cdot (x+1)+2}$
- $y=\frac{2{(x+1)}^{2}}{C-4\cdot (x+1)}$

First, we rearrange the equation, as follows:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}+2\cdot (x+1)y}{{(x+1)}^{2}} \\ \frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{(x+1)}^{2}}+\frac{2\cdot (x+1)y}{{(x+1)}^{2}} \\ \frac{\text{d}y}{\text{d}x}-2{(x+1)}^{-1}y & ={(x+1)}^{-2}{y}^{2}\end{aligned}
$$

Notice that our equation is an instance of the Bernoulli differential equation

$$
\frac{dy}{dx}+p(x)y=q(x){y}^{n}.
$$

In this case, we have

$$
p(x)=-2{(x+1)}^{-1},\,q(x)={(x+1)}^{-2},\,n=2.
$$

Now, we divide the differential equation by ${y}^{2},$ and we get

$$
{y}^{-2}\frac{dy}{dx}-2{(x+1)}^{-1}{y}^{-1}={(x+1)}^{-2}.\,\,(∗)
$$

Then, we make the substitution

$$
z={y}^{1-n}={y}^{-1}.
$$

Differentiating $z(x)$ using the chain rule, we get 

$$
\frac{\text{d}z}{\text{d}x}=-{y}^{-2}\,\frac{\text{d}y}{\text{d}x}\,⟹\,{y}^{-2}\frac{\text{d}y}{\text{d}x}=-\,\frac{\text{d}z}{\text{d}x}.
$$

 

Therefore, equation $(∗)$ can be written as a linear equation in $z(x)$ as follows:

$$
-\,\frac{\text{d}z}{\text{d}x}-2{(x+1)}^{-1}z={(x+1)}^{-2}
$$

This differential equation is linear, so we can use the method of integrating factors. But first, we write the above equation in standard form:

$$
\frac{\text{d}z}{\text{d}x}+2{(x+1)}^{-1}z=-{(x+1)}^{-2}
$$

The above equation is now in the standard form

$$
\frac{\text{d}z}{\text{d}x}+P(x)z=Q(x),
$$

with

$$
\begin{aligned}P(x)=\frac{2}{(x+1)},\,Q(x)=-\frac{1}{{(x+1)}^{2}}\,.\end{aligned}
$$

We then compute an integrating factor:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/(x+1))\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡(x+1)} \\  & ={(x+1)}^{2}\end{aligned}
$$

Multiplying both sides of the standard form equation by $I(x)={(x+1)}^{2}$ yields

$$
\begin{aligned}{(x+1)}^{2}\cdot (\frac{\text{d}z}{\text{d}x}+2{(x+1)}^{-1}z) & ={(x+1)}^{2}\cdot (-{(x+1)}^{-2}) \\ {(x+1)}^{2}\cdot \frac{\text{d}z}{\text{d}x}+2\cdot (x+1)z & =-1 \\ \frac{\text{d}}{\text{d}x}({(x+1)}^{2}z) & =-1.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}({(x+1)}^{2}z)\,\text{d}x & =-\int 1\,\text{d}x \\ {(x+1)}^{2}z & =-(x+1)+C \\ z & =\frac{C-(x+1)}{{(x+1)}^{2}}.\end{aligned}
$$

Finally, we determine $y(x)$ by writing $z={y}^{-1}.$ This results in

$$
{y}^{-1}=\frac{C-(x+1)}{{(x+1)}^{2}}\,⇒\,y=\frac{{(x+1)}^{2}}{C-(x+1)}\,.
$$

These are the nonzero real solutions on the specified intervals; exclude denominator zeros and restrict constants and intervals to the real branches used above.

---

Find the general nonzero real solution to the differential equation

$$
\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}+2\cdot (x+2)y}{{(x+2)}^{2}}.
$$

Work on an interval where $x+2>0$. Choose constants and intervals on which all displayed real expressions are defined.

{{selection}}

- $y=\frac{{(x+2)}^{2}}{C-(x+2)}$ [key]
- $y=\frac{(x+2)+C}{{(x+2)}^{3}}$
- $y=\frac{C-(x+2)}{2{(x+2)}^{2}}$
- $y=\frac{{(x+2)}^{2}}{C\cdot (x+2)+2}$
- $y=\frac{2{(x+2)}^{2}}{C-4\cdot (x+2)}$

First, we rearrange the equation, as follows:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}+2\cdot (x+2)y}{{(x+2)}^{2}} \\ \frac{\text{d}y}{\text{d}x} & =\frac{{y}^{2}}{{(x+2)}^{2}}+\frac{2\cdot (x+2)y}{{(x+2)}^{2}} \\ \frac{\text{d}y}{\text{d}x}-2{(x+2)}^{-1}y & ={(x+2)}^{-2}{y}^{2}\end{aligned}
$$

Notice that our equation is an instance of the Bernoulli differential equation

$$
\frac{dy}{dx}+p(x)y=q(x){y}^{n}.
$$

In this case, we have

$$
p(x)=-2{(x+2)}^{-1},\,q(x)={(x+2)}^{-2},\,n=2.
$$

Now, we divide the differential equation by ${y}^{2},$ and we get

$$
{y}^{-2}\frac{dy}{dx}-2{(x+2)}^{-1}{y}^{-1}={(x+2)}^{-2}.\,\,(∗)
$$

Then, we make the substitution

$$
z={y}^{1-n}={y}^{-1}.
$$

Differentiating $z(x)$ using the chain rule, we get 

$$
\frac{\text{d}z}{\text{d}x}=-{y}^{-2}\,\frac{\text{d}y}{\text{d}x}\,⟹\,{y}^{-2}\frac{\text{d}y}{\text{d}x}=-\,\frac{\text{d}z}{\text{d}x}.
$$

 

Therefore, equation $(∗)$ can be written as a linear equation in $z(x)$ as follows:

$$
-\,\frac{\text{d}z}{\text{d}x}-2{(x+2)}^{-1}z={(x+2)}^{-2}
$$

This differential equation is linear, so we can use the method of integrating factors. But first, we write the above equation in standard form:

$$
\frac{\text{d}z}{\text{d}x}+2{(x+2)}^{-1}z=-{(x+2)}^{-2}
$$

The above equation is now in the standard form

$$
\frac{\text{d}z}{\text{d}x}+P(x)z=Q(x),
$$

with

$$
\begin{aligned}P(x)=\frac{2}{(x+2)},\,Q(x)=-\frac{1}{{(x+2)}^{2}}\,.\end{aligned}
$$

We then compute an integrating factor:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/(x+2))\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡(x+2)} \\  & ={(x+2)}^{2}\end{aligned}
$$

Multiplying both sides of the standard form equation by $I(x)={(x+2)}^{2}$ yields

$$
\begin{aligned}{(x+2)}^{2}\cdot (\frac{\text{d}z}{\text{d}x}+2{(x+2)}^{-1}z) & ={(x+2)}^{2}\cdot (-{(x+2)}^{-2}) \\ {(x+2)}^{2}\cdot \frac{\text{d}z}{\text{d}x}+2\cdot (x+2)z & =-1 \\ \frac{\text{d}}{\text{d}x}({(x+2)}^{2}z) & =-1.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}({(x+2)}^{2}z)\,\text{d}x & =-\int 1\,\text{d}x \\ {(x+2)}^{2}z & =-(x+2)+C \\ z & =\frac{C-(x+2)}{{(x+2)}^{2}}.\end{aligned}
$$

Finally, we determine $y(x)$ by writing $z={y}^{-1}.$ This results in

$$
{y}^{-1}=\frac{C-(x+2)}{{(x+2)}^{2}}\,⇒\,y=\frac{{(x+2)}^{2}}{C-(x+2)}\,.
$$

These are the nonzero real solutions on the specified intervals; exclude denominator zeros and restrict constants and intervals to the real branches used above.

---

Find the general nonzero real solution to the differential equation

$$
(x-2)\,\frac{\text{d}y}{\text{d}x}+y={(x-2)}^{2}{y}^{3/4}.
$$

Work on an interval where $x-2>0$. Choose constants and intervals on which all displayed real expressions are defined. Take $y>0$.

{{selection}}

- $y={(\frac{{(x-2)}^{5/4}+C}{5{(x-2)}^{1/4}})}^{4}$
- $y={(\frac{C{(x-2)}^{1/2}-2}{4{(x-2)}^{1/2}})}^{2}$
- $y=\frac{{(x-2)}^{1/4}+C}{4{(x-2)}^{9/4}}$
- $y={(\frac{{(x-2)}^{9/4}+C}{9{(x-2)}^{1/4}})}^{4}$ [key]
- $y=\frac{4{(x-2)}^{5/4}+C}{3{(x-2)}^{1/4}}$

First, we rearrange the equation, as follows:

$$
\begin{aligned}(x-2)\,\frac{\text{d}y}{\text{d}x}+y={(x-2)}^{2}{y}^{3/4} \\ \frac{\text{d}y}{\text{d}x}+\frac{y}{(x-2)} & =(x-2){y}^{3/4}\end{aligned}
$$

Notice that our equation is an instance of the Bernoulli differential equation

$$
\frac{dy}{dx}+p(x)y=q(x){y}^{n}.
$$

In this case, we have

$$
p(x)={(x-2)}^{-1},\,q(x)=(x-2),\,n=\frac{3}{4}.
$$

Now, we divide the differential equation by ${y}^{3/4},$ and we get

$$
{y}^{-3/4}\frac{dy}{dx}+{(x-2)}^{-1}{y}^{1/4}=(x-2).\,\,(∗)
$$

Then, we make the substitution

$$
z={y}^{1-n}={y}^{1/4}.
$$

Differentiating $z(x)$ using the chain rule, we get 

$$
\frac{\text{d}z}{\text{d}x}=\frac{1}{4}{y}^{-3/4}\,\frac{\text{d}y}{\text{d}x}\,⟹\,{y}^{-3/4}\frac{\text{d}y}{\text{d}x}=4\,\frac{\text{d}z}{\text{d}x}.
$$

 

Therefore, equation $(∗)$ can be written as a linear equation in $z(x)$ as follows:

$$
4\,\frac{\text{d}z}{\text{d}x}+{(x-2)}^{-1}z=(x-2)
$$

This differential equation is linear, so we can use the method of integrating factors. But first, we write the above equation in standard form:

$$
\frac{\text{d}z}{\text{d}x}+\frac{1}{4}{(x-2)}^{-1}z=\frac{(x-2)}{4}
$$

The above equation is now in the standard form

$$
\frac{\text{d}z}{\text{d}x}+P(x)z=Q(x),
$$

with

$$
\begin{aligned}P(x)=\frac{1}{4\cdot (x-2)},\,Q(x)=\frac{(x-2)}{4}\,.\end{aligned}
$$

We then compute an integrating factor:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (\frac{1}{4\cdot (x-2)})\,\text{d}x} \\  & ={e}^{(1/4)\operatorname{ln}⁡(x-2)} \\  & ={(x-2)}^{1/4}\end{aligned}
$$

Multiplying both sides of the standard form equation by $I(x)={(x-2)}^{1/4}$ yields

$$
\begin{aligned}{(x-2)}^{1/4}\cdot (\frac{\text{d}z}{\text{d}x}+\frac{1}{4}{(x-2)}^{-1}z) & ={(x-2)}^{1/4}\cdot (\frac{(x-2)}{4}) \\ {(x-2)}^{1/4}\cdot \frac{\text{d}z}{\text{d}x}+\frac{1}{4}{(x-2)}^{-3/4}z & =\frac{{(x-2)}^{5/4}}{4} \\ \frac{\text{d}}{\text{d}x}(z{(x-2)}^{1/4}) & =\frac{{(x-2)}^{5/4}}{4}.\end{aligned}
$$

Now, we integrate with respect to $x:$

$$
\begin{aligned}\int \frac{\text{d}}{\text{d}x}(z{(x-2)}^{1/4})\,\text{d}x & =\int \frac{{(x-2)}^{5/4}}{4}\,\text{d}x \\ z{(x-2)}^{1/4} & =\frac{1}{9}{(x-2)}^{9/4}+{C}_{1} \\ z & =\frac{{(x-2)}^{9/4}+C}{9{(x-2)}^{1/4}},\end{aligned}
$$

where $C=9{C}_{1}.$

Finally, we determine $y(x)$ by writing $z={y}^{1/4}.$ This results in

$$
{y}^{1/4}=\frac{{(x-2)}^{9/4}+C}{9{(x-2)}^{1/4}}\,⇒\,y={(\frac{{(x-2)}^{9/4}+C}{9{(x-2)}^{1/4}})}^{4}\,.
$$

These are the nonzero real solutions on the specified intervals; exclude denominator zeros and restrict constants and intervals to the real branches used above. Since $z=y^{1/4}>0$, retain only intervals where the displayed expression for $z$ is positive.