# Chain and product rules: private draft

All observed raw records are evidence-only. Hard rating, missing key and polynomial solution are authored; seven E/M backbones preserve their source prose and stages.

## Original MA q-11599

If $y = x^{3}(2x^{2} + 1)^{3}$, find $\frac{dy}{dx}$.

- (12x^{4} + x^{2})(2x^{2} + 1)^{2}
- (12x^{4} + 3x^{2})(2x^{2} + 1)^{2}
- (18x^{4} + 3x^{2})(2x^{2} + 1)^{3}
- (18x^{4} + 3x^{2})(2x^{2} + 1)^{2}
- (3x^{4} + 12x^{2})(2x^{2} + 1)^{2}

## Original MA q-31240

Find the slope of $y = 2x\cos (2x + 3)$ at $x =-1$.

- 2\cos 1 + 2\sin 1
- \cos 1 + 2\sin 1
- 2\cos 1 + \sin 1
- 2\cos 1 + 4\sin 1
- \cos 5 + 2\sin 5

## Original MA q-11602

If $y=2{x}^{3}\sqrt{2{x}^{2}+7},$ find the value of $\frac{\text{d}y}{\text{d}x}$ at $x=2.$

This question requires the product rule. Let $u(x)=2{x}^{3}$ and $v(x)=\sqrt{2{x}^{2}+7}.$ Then

$$
{u}^{'}(x)=6{x}^{2},\,{v}^{'}(x)=\frac{2x}{\sqrt{2{x}^{2}+7}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(6{x}^{2})(\sqrt{2{x}^{2}+7})+(2{x}^{3})(\frac{2x}{\sqrt{2{x}^{2}+7}}) \\  & =6{x}^{2}\sqrt{2{x}^{2}+7}+\frac{4{x}^{4}}{\sqrt{2{x}^{2}+7}}.\end{aligned}
$$

Therefore, the value of $\frac{\text{d}y}{\text{d}x}$ at $x=2$ is

$$
\begin{aligned}{(\frac{\text{d}y}{\text{d}x})|}_{x=2} & =6(2)^{2}\sqrt{2(2)^{2}+7}+\frac{4(2)^{4}}{\sqrt{2(2)^{2}+7}} \\  & =24\sqrt{15}+\frac{64}{\sqrt{15}} \\  & =\frac{360+64}{\sqrt{15}} \\  & =\frac{424}{\sqrt{15}}.\end{aligned}
$$

## Original MA q-11603

If $y=3{x}^{2}{({x}^{3}-1)}^{4}$, find the value of $\frac{\text{d}y}{\text{d}x}$ at $x=1.$

This question requires the product rule. Let $u(x)=3{x}^{2}$ and $v(x)={({x}^{3}-1)}^{4}.$ Then

$$
{u}^{'}(x)=6x,\,{v}^{'}(x)=12{x}^{2}{({x}^{3}-1)}^{3}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(6x)(({x}^{3}-1)^{4})+(3{x}^{2})(12{x}^{2}({x}^{3}-1)^{3}) \\  & =6x({x}^{3}-1)^{4}+36{x}^{4}{({x}^{3}-1)}^{3} \\  & =(6x({x}^{3}-1)+36{x}^{4})\,{({x}^{3}-1)}^{3} \\  & =(6{x}^{4}-6x+36{x}^{4})\,{({x}^{3}-1)}^{3} \\  & =(42{x}^{4}-6x)\,{({x}^{3}-1)}^{3}.\end{aligned}
$$

To evaluate $\frac{\text{d}y}{\text{d}x}$ at $x=1$, we substitute $x=1:$

$$
\begin{aligned}{(\frac{\text{d}y}{\text{d}x})|}_{x=1} & =(42\cdot {1}^{4}-6\cdot 1){({1}^{3}-1)}^{3} \\  & =36\cdot 0 \\  & =0.\end{aligned}
$$

## Original MA q-11939

Given that $y=x\operatorname{ln}3x,$ find $\frac{\text{d}y}{\text{d}x}.$

This question requires the product rule. Let $u(x)=x$ and $v(x)=\operatorname{ln}3x.$ Then

$$
{u}^{'}(x)=1,\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(1)(\operatorname{ln}3x)+(x)(\frac{1}{x}) \\  & =\operatorname{ln}3x+1.\end{aligned}
$$

## Original MA q-143518

Find the acceleration function ${a}_{2}(t)$ of the second particle.

${a}_{2}(t)\,=\,$
{{field-1}}

- 2t\operatorname{sin}(3t)+3{t}^{2}\operatorname{cos}(3t)

In part 3, we saw that the derivative of a particle's velocity with respect to time gives its acceleration.

To differentiate ${v}_{2}(t),$ we require the product rule. Let $g(t)={t}^{2}$ and $h(t)=\operatorname{sin}(3t).$ Then

$$
{g}^{'}(t)=2t,\,{h}^{'}(t)=3\operatorname{cos}(3t).
$$

We used the chain rule to calculate ${h}^{'}(t).$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{a}_{2}(t) & ={v}_{2}^{'}(t) \\  & ={g}^{'}(t)\cdot h(t)+g(t)\cdot {h}^{'}(t) \\  & =(2t)(\operatorname{sin}(3t))+({t}^{2})(3\operatorname{cos}(3t)) \\  & =2t\operatorname{sin}(3t)+3{t}^{2}\operatorname{cos}(3t).\end{aligned}
$$

## Original MA q-16698

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{cos}3x.$

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{cos}3x.$ Then

$$
{u}^{'}(x)={e}^{x},\,{v}^{'}(x)=-3\operatorname{sin}3x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =({e}^{x})(\operatorname{cos}3x)+({e}^{x})(-3\operatorname{sin}3x) \\  & ={e}^{x}\operatorname{cos}3x-3{e}^{x}\operatorname{sin}3x \\  & ={e}^{x}(\operatorname{cos}3x-3\operatorname{sin}3x).\end{aligned}
$$

## Original MA q-313299

Find the slope $m$ of the tangent line to the curve $y={x}^{2}\operatorname{sin}(2x)$ at $x=\frac{\pi }{4}.$

$m=$
{{field-1}}



To find the slope at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}2x.$ Then

$$
{u}^{'}(x)=2x,\,{v}^{'}(x)=2\operatorname{cos}2x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(2x)(\operatorname{sin}2x)+({x}^{2})(2\operatorname{cos}2x) \\  & =2x\operatorname{sin}2x+2{x}^{2}\operatorname{cos}2x.\end{aligned}
$$

Therefore, the slope $m$ at $x=\frac{\pi }{4}$ is

$$
\begin{aligned}m & ={(\frac{\text{d}y}{\text{d}x})|}_{x=\pi /4} \\  & =2(\frac{\pi }{4})\cdot \operatorname{sin}(2\cdot \frac{\pi }{4})+2{(\frac{\pi }{4})}^{2}\operatorname{cos}(2\cdot \frac{\pi }{4}) \\  & =\frac{\pi }{2}\cdot \operatorname{sin}(\frac{\pi }{2})+2\cdot \frac{{\pi }^{2}}{16}\cdot \operatorname{cos}(\frac{\pi }{2}) \\  & =\frac{\pi }{2}\cdot 1+\frac{{\pi }^{2}}{8}\cdot 0 \\  & =\frac{\pi }{2}.\end{aligned}
$$

## Original MA q-343333

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{5x}\operatorname{ln}x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{5x}$

- 5\operatorname{ln}x+\frac{1}{x}

This question requires the product rule. Let $u(x)={e}^{5x}$ and $v(x)=\operatorname{ln}x.$ Then

$$
{u}^{'}(x)=5{e}^{5x},\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $u.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(5{e}^{5x})(\operatorname{ln}x)+({e}^{5x})\,(\frac{1}{x}) \\  & =(5\operatorname{ln}x+\frac{1}{x}){e}^{5x}.\end{aligned}
$$

## Original MA q-167572

Find the acceleration function ${a}_{2}(t)$ of the second particle.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        ${a}_{2}(t)\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

- \operatorname{cos}(t/2)-t/2\operatorname{sin}(t/2)

In part 3, we saw that the derivative of a particle's velocity with respect to time gives its acceleration.

To differentiate ${v}_{2}(t),$ we require the product rule. Let $g(t)=t$ and $h(t)=\operatorname{cos}⁡(\frac{t}{2}).$ Then

$$
{g}^{′}(t)=1,\,{h}^{′}(t)=-\frac{1}{2}\operatorname{sin}⁡(\frac{t}{2}).
$$

We used the chain rule to calculate ${h}^{′}(t).$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{a}_{2}(t) & ={v}_{2}^{′}(t) \\  & ={g}^{′}(t)\cdot h(t)+g(t)\cdot {h}^{′}(t) \\  & =(1)(\operatorname{cos}⁡(\frac{t}{2}))+(t)(-\frac{1}{2}\operatorname{sin}⁡(\frac{t}{2})) \\  & =\operatorname{cos}⁡(\frac{t}{2})-\frac{1}{2}t\operatorname{sin}⁡(\frac{t}{2}).\end{aligned}
$$

## Original MA q-10009

Find the slope of $y=\operatorname{sin}⁡2x\operatorname{cos}⁡3x$ at $x=\frac{\pi }{2}.$

- -1
- 0
- 1
- 2
- 3

To find the slope at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

This question requires the product rule. Let $u(x)=\operatorname{sin}⁡2x$ and $v(x)=\operatorname{cos}⁡3x.$ Then

$$
{u}^{′}(x)=2\operatorname{cos}⁡2x,\,{v}^{′}(x)=-3\operatorname{sin}⁡3x.
$$

Note that we used the chain rule to differentiate $u$ and $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2\operatorname{cos}⁡2x)(\operatorname{cos}⁡3x)+(\operatorname{sin}⁡2x)(-3\operatorname{sin}⁡3x) \\  & =2\operatorname{cos}⁡2x\operatorname{cos}⁡3x-3\operatorname{sin}⁡2x\operatorname{sin}⁡3x.\end{aligned}
$$

Therefore, the slope at $x=\frac{\pi }{2}$ is

$$
\begin{aligned}{(\frac{\text{d}y}{\text{d}x})|}_{x=\pi /2} & =2\operatorname{cos}⁡(2\cdot \frac{\pi }{2})\operatorname{cos}⁡(3\cdot \frac{\pi }{2})-3\operatorname{sin}⁡(2\cdot \frac{\pi }{2})\operatorname{sin}⁡(3\cdot \frac{\pi }{2}) \\  & =2\operatorname{cos}⁡(\pi )\operatorname{cos}⁡(\frac{3\pi }{2})-3\operatorname{sin}⁡(\pi )\operatorname{sin}⁡(\frac{3\pi }{2}) \\  & =0.\end{aligned}
$$

## Original MA q-11824

Given that $y=(x+1){e}^{9x},$ find $\frac{\text{d}y}{\text{d}x}.$

- (9x+1){e}^{9x}
- (9x+10){e}^{9x}
- (x+1){e}^{9x}
- 9x{e}^{9x}
- 9(x+1){e}^{9x}

This question requires the product rule. Let $u(x)=x+1$ and $v(x)={e}^{9x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=9{e}^{9x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{9x})+(x+1)(9{e}^{9x}) \\  & ={e}^{9x}+9(x+1){e}^{9x} \\  & =(1+9(x+1)){e}^{9x} \\  & =(9x+10){e}^{9x}.\end{aligned}
$$

## Original MA q-2392

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={a}^{3x}\operatorname{tan}⁡x.$

- {a}^{3x}({sec}^{2}⁡x+3\operatorname{ln}⁡a\operatorname{tan}⁡x)
- {a}^{3x}({sec}^{2}⁡x+3\operatorname{tan}⁡x)
- {a}^{3x}{sec}^{2}⁡x+3\operatorname{tan}⁡x
- 3{a}^{3x}({sec}^{2}⁡x+\operatorname{ln}⁡a\operatorname{tan}⁡x)
- 3{sec}^{2}⁡x+3{a}^{3x}\operatorname{tan}⁡x

This question requires the product rule. Let $u(x)=\operatorname{tan}⁡x$ and $v(x)={a}^{3x}.$ Then

$$
{u}^{′}(x)={sec}^{2}⁡x,\,{v}^{′}(x)=3{a}^{3x}\operatorname{ln}⁡a.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({sec}^{2}⁡x)({a}^{3x})+(\operatorname{tan}⁡x)(3{a}^{3x}\operatorname{ln}⁡a) \\  & ={a}^{3x}({sec}^{2}⁡x+3\operatorname{ln}⁡a\operatorname{tan}⁡x).\end{aligned}
$$

## Original MA q-2401

Find ${y}^{′}$ for $y=4{x}^{2}\sqrt{\operatorname{sin}⁡x}.$

- \frac{x\operatorname{cos}⁡x+2x\operatorname{sin}⁡x}{\operatorname{sin}⁡x}
- \frac{2{x}^{2}\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}-x\sqrt{\operatorname{sin}⁡x}
- \frac{2{x}^{2}\operatorname{sin}⁡x-8x\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- \frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- -\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{cos}⁡x}}+8x\sqrt{\operatorname{sin}⁡x}

This question requires the product rule. Let $u(x)=4{x}^{2}$ and $v(x)=\sqrt{\operatorname{sin}⁡x}.$ Then

$$
{u}^{′}(x)=8x,\,{v}^{′}(x)=\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{y}^{′}=\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(8x)(\sqrt{\operatorname{sin}⁡x})+(4{x}^{2})(\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}) \\  & =8x\sqrt{\operatorname{sin}⁡x}+\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}} \\  & =\frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}.\end{aligned}
$$

## Original MA q-343332

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{sin}⁡4x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{x}$

- \operatorname{sin}4x+4\operatorname{cos}4x

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}⁡4x.$ Then

$$
{u}^{′}(x)={e}^{x},\,{v}^{′}(x)=4\operatorname{cos}⁡4x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})(\operatorname{sin}⁡4x)+(4\operatorname{cos}⁡4x)({e}^{x}) \\  & =(\operatorname{sin}⁡4x+4\operatorname{cos}⁡4x){e}^{x}.\end{aligned}
$$

## Original MA q-343354

Given that $y=2x{e}^{6x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{6x}$

- 12x+2

This question requires the product rule. Let $u(x)=2x$ and $v(x)={e}^{6x}.$ Then

$$
{u}^{′}(x)=2,\,{v}^{′}(x)=6{e}^{6x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2)({e}^{6x})+(2x)(6{e}^{6x}) \\  & =(12x+2){e}^{6x}.\end{aligned}
$$

## Original MA q-9942

If $f(x)={x}^{2}\operatorname{sin}⁡(5x+2),$ find ${f}^{′}(x).$

- 2{x}^{2}\operatorname{sin}⁡(5x+2)+5x\operatorname{cos}⁡(5x+2)
- 2x\operatorname{sin}⁡(5x+2)+{x}^{2}\operatorname{cos}⁡(5x+2)
- 2\operatorname{sin}⁡(5x+2)+5{x}^{2}\operatorname{cos}⁡(5x+2)
- 2x\operatorname{sin}⁡(5x+2)+5{x}^{2}\operatorname{cos}⁡(5x+2)
- 5x\operatorname{sin}⁡(5x+2)+2{x}^{2}\operatorname{cos}⁡(5x+2)

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(5x+2).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=5\operatorname{cos}⁡(5x+2).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(5x+2))+({x}^{2})(5\operatorname{cos}⁡(5x+2)) \\  & =2x\operatorname{sin}⁡(5x+2)+5{x}^{2}\operatorname{cos}⁡(5x+2).\end{aligned}
$$

## Original MA q-9944

Find the slope of $f(x)={x}^{2}{sin}^{3}⁡x$ at $x=0.$

- -1
- 3
- 0
- 2
- 5

To find the slope at a given point, we have to find $\frac{\text{d}f}{\text{d}x}$ at that point.

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)={sin}^{3}⁡x.$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=3{sin}^{2}⁡x\operatorname{cos}⁡x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)({sin}^{3}⁡x)+({x}^{2})(3{sin}^{2}⁡x\operatorname{cos}⁡x) \\  & =2x{sin}^{3}⁡x+3{x}^{2}{sin}^{2}⁡x\operatorname{cos}⁡x.\end{aligned}
$$

Therefore, the slope at $x=0$ is

$$
\begin{aligned}{(\frac{\text{d}f}{\text{d}x})|}_{x=0} & =2\cdot 0\cdot {sin}^{3}⁡(0)+3\cdot {0}^{2}\cdot {sin}^{2}⁡(0)\operatorname{cos}⁡(0) \\  & =0.\end{aligned}
$$

## Eligible generated variant / easy / q-343332

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{sin}⁡4x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{x}$

- \operatorname{sin}4x+4\operatorname{cos}4x

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}⁡4x.$ Then

$$
{u}^{′}(x)={e}^{x},\,{v}^{′}(x)=4\operatorname{cos}⁡4x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})(\operatorname{sin}⁡4x)+(4\operatorname{cos}⁡4x)({e}^{x}) \\  & =(\operatorname{sin}⁡4x+4\operatorname{cos}⁡4x){e}^{x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343332

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{sin}⁡2x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{x}$

- \operatorname{sin}2x+2\operatorname{cos}2x

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}⁡2x.$ Then

$$
{u}^{′}(x)={e}^{x},\,{v}^{′}(x)=2\operatorname{cos}⁡2x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})(\operatorname{sin}⁡2x)+(2\operatorname{cos}⁡2x)({e}^{x}) \\  & =(\operatorname{sin}⁡2x+2\operatorname{cos}⁡2x){e}^{x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343332

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{sin}⁡16x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{x}$

- \operatorname{sin}16x+16\operatorname{cos}16x

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}⁡16x.$ Then

$$
{u}^{′}(x)={e}^{x},\,{v}^{′}(x)=16\operatorname{cos}⁡16x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})(\operatorname{sin}⁡16x)+(16\operatorname{cos}⁡16x)({e}^{x}) \\  & =(\operatorname{sin}⁡16x+16\operatorname{cos}⁡16x){e}^{x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343332

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{sin}⁡2x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{x}$

- \operatorname{sin}2x+2\operatorname{cos}2x

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}⁡2x.$ Then

$$
{u}^{′}(x)={e}^{x},\,{v}^{′}(x)=2\operatorname{cos}⁡2x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})(\operatorname{sin}⁡2x)+(2\operatorname{cos}⁡2x)({e}^{x}) \\  & =(\operatorname{sin}⁡2x+2\operatorname{cos}⁡2x){e}^{x}.\end{aligned}
$$

## Changed raw evidence / easy / q-343332

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{sin}⁡2x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{x}$

- \operatorname{sin}2x+2\operatorname{cos}2x

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}⁡2x.$ Then

$$
{u}^{′}(x)={e}^{x},\,{v}^{′}(x)=2\operatorname{cos}⁡2x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})(\operatorname{sin}⁡2x)+(2\operatorname{cos}⁡2x)({e}^{x}) \\  & =(\operatorname{sin}⁡2x+2\operatorname{cos}⁡2x){e}^{x}.\end{aligned}
$$

## Changed raw evidence / easy / q-343332

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{sin}⁡16x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{x}$

- \operatorname{sin}16x+16\operatorname{cos}16x

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}⁡16x.$ Then

$$
{u}^{′}(x)={e}^{x},\,{v}^{′}(x)=16\operatorname{cos}⁡16x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})(\operatorname{sin}⁡16x)+(16\operatorname{cos}⁡16x)({e}^{x}) \\  & =(\operatorname{sin}⁡16x+16\operatorname{cos}⁡16x){e}^{x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343333

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{5x}\operatorname{ln}x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{5x}$

- 5\operatorname{ln}x+\frac{1}{x}

This question requires the product rule. Let $u(x)={e}^{5x}$ and $v(x)=\operatorname{ln}x.$ Then

$$
{u}^{'}(x)=5{e}^{5x},\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $u.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(5{e}^{5x})(\operatorname{ln}x)+({e}^{5x})\,(\frac{1}{x}) \\  & =(5\operatorname{ln}x+\frac{1}{x}){e}^{5x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343333

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{2x}\operatorname{ln}x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{2x}$

- 2\operatorname{ln}x+\frac{1}{x}

This question requires the product rule. Let $u(x)={e}^{2x}$ and $v(x)=\operatorname{ln}x.$ Then

$$
{u}^{'}(x)=2{e}^{2x},\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $u.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(2{e}^{2x})(\operatorname{ln}x)+({e}^{2x})\,(\frac{1}{x}) \\  & =(2\operatorname{ln}x+\frac{1}{x}){e}^{2x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343333

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{16x}\operatorname{ln}x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{16x}$

- 16\operatorname{ln}x+\frac{1}{x}

This question requires the product rule. Let $u(x)={e}^{16x}$ and $v(x)=\operatorname{ln}x.$ Then

$$
{u}^{'}(x)=16{e}^{16x},\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $u.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(16{e}^{16x})(\operatorname{ln}x)+({e}^{16x})\,(\frac{1}{x}) \\  & =(16\operatorname{ln}x+\frac{1}{x}){e}^{16x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343333

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{2x}\operatorname{ln}x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{2x}$

- 2\operatorname{ln}x+\frac{1}{x}

This question requires the product rule. Let $u(x)={e}^{2x}$ and $v(x)=\operatorname{ln}x.$ Then

$$
{u}^{'}(x)=2{e}^{2x},\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $u.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(2{e}^{2x})(\operatorname{ln}x)+({e}^{2x})\,(\frac{1}{x}) \\  & =(2\operatorname{ln}x+\frac{1}{x}){e}^{2x}.\end{aligned}
$$

## Changed raw evidence / easy / q-343333

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{2x}\operatorname{ln}x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{2x}$

- 2\operatorname{ln}x+\frac{1}{x}

This question requires the product rule. Let $u(x)={e}^{2x}$ and $v(x)=\operatorname{ln}x.$ Then

$$
{u}^{'}(x)=2{e}^{2x},\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $u.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(2{e}^{2x})(\operatorname{ln}x)+({e}^{2x})\,(\frac{1}{x}) \\  & =(2\operatorname{ln}x+\frac{1}{x}){e}^{2x}.\end{aligned}
$$

## Changed raw evidence / easy / q-343333

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{16x}\operatorname{ln}x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{16x}$

- 16\operatorname{ln}x+\frac{1}{x}

This question requires the product rule. Let $u(x)={e}^{16x}$ and $v(x)=\operatorname{ln}x.$ Then

$$
{u}^{'}(x)=16{e}^{16x},\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $u.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(16{e}^{16x})(\operatorname{ln}x)+({e}^{16x})\,(\frac{1}{x}) \\  & =(16\operatorname{ln}x+\frac{1}{x}){e}^{16x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343354

Given that $y=2x{e}^{6x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{6x}$

- 12x+2

This question requires the product rule. Let $u(x)=2x$ and $v(x)={e}^{6x}.$ Then

$$
{u}^{′}(x)=2,\,{v}^{′}(x)=6{e}^{6x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2)({e}^{6x})+(2x)(6{e}^{6x}) \\  & =(12x+2){e}^{6x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343354

Given that $y=1x{e}^{2x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{2x}$

- 2x+1

This question requires the product rule. Let $u(x)=1x$ and $v(x)={e}^{2x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=2{e}^{2x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{2x})+(1x)(2{e}^{2x}) \\  & =(2x+1){e}^{2x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343354

Given that $y=6x{e}^{16x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{16x}$

- 96x+6

This question requires the product rule. Let $u(x)=6x$ and $v(x)={e}^{16x}.$ Then

$$
{u}^{′}(x)=6,\,{v}^{′}(x)=16{e}^{16x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(6)({e}^{16x})+(6x)(16{e}^{16x}) \\  & =(96x+6){e}^{16x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343354

Given that $y=1x{e}^{6x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{6x}$

- 6x+1

This question requires the product rule. Let $u(x)=1x$ and $v(x)={e}^{6x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=6{e}^{6x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{6x})+(1x)(6{e}^{6x}) \\  & =(6x+1){e}^{6x}.\end{aligned}
$$

## Eligible generated variant / easy / q-343354

Given that $y=2x{e}^{2x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{2x}$

- 4x+2

This question requires the product rule. Let $u(x)=2x$ and $v(x)={e}^{2x}.$ Then

$$
{u}^{′}(x)=2,\,{v}^{′}(x)=2{e}^{2x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2)({e}^{2x})+(2x)(2{e}^{2x}) \\  & =(4x+2){e}^{2x}.\end{aligned}
$$

## Changed raw evidence / easy / q-343354

Given that $y=1x{e}^{2x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{2x}$

- 2x+1

This question requires the product rule. Let $u(x)=1x$ and $v(x)={e}^{2x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=2{e}^{2x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{2x})+(1x)(2{e}^{2x}) \\  & =(2x+1){e}^{2x}.\end{aligned}
$$

## Changed raw evidence / easy / q-343354

Given that $y=6x{e}^{16x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{16x}$

- 96x+6

This question requires the product rule. Let $u(x)=6x$ and $v(x)={e}^{16x}.$ Then

$$
{u}^{′}(x)=6,\,{v}^{′}(x)=16{e}^{16x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(6)({e}^{16x})+(6x)(16{e}^{16x}) \\  & =(96x+6){e}^{16x}.\end{aligned}
$$

## Eligible generated variant / easy / q-11824

Given that $y=(x+1){e}^{9x},$ find $\frac{\text{d}y}{\text{d}x}.$

- (x+1){e}^{9x}
- (9x+10){e}^{9x}
- (9x+1){e}^{9x}
- 9(x+1){e}^{9x}
- 9x{e}^{9x}

This question requires the product rule. Let $u(x)=x+1$ and $v(x)={e}^{9x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=9{e}^{9x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{9x})+(x+1)(9{e}^{9x}) \\  & ={e}^{9x}+9(x+1){e}^{9x} \\  & =(1+9(x+1)){e}^{9x} \\  & =(9x+10){e}^{9x}.\end{aligned}
$$

## Eligible generated variant / easy / q-11824

Given that $y=(x+1){e}^{2x},$ find $\frac{\text{d}y}{\text{d}x}.$

- (x+1){e}^{2x}
- (2x+3){e}^{2x}
- (2x+1){e}^{2x}
- 2(x+1){e}^{2x}
- 2x{e}^{2x}

This question requires the product rule. Let $u(x)=x+1$ and $v(x)={e}^{2x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=2{e}^{2x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{2x})+(x+1)(2{e}^{2x}) \\  & ={e}^{2x}+2(x+1){e}^{2x} \\  & =(1+2(x+1)){e}^{2x} \\  & =(2x+3){e}^{2x}.\end{aligned}
$$

## Eligible generated variant / easy / q-11824

Given that $y=(x+1){e}^{16x},$ find $\frac{\text{d}y}{\text{d}x}.$

- 16(x+1){e}^{16x}
- (x+1){e}^{16x}
- 16x{e}^{16x}
- (16x+17){e}^{16x}
- (16x+1){e}^{16x}

This question requires the product rule. Let $u(x)=x+1$ and $v(x)={e}^{16x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=16{e}^{16x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{16x})+(x+1)(16{e}^{16x}) \\  & ={e}^{16x}+16(x+1){e}^{16x} \\  & =(1+16(x+1)){e}^{16x} \\  & =(16x+17){e}^{16x}.\end{aligned}
$$

## Eligible generated variant / easy / q-11824

Given that $y=(x+1){e}^{2x},$ find $\frac{\text{d}y}{\text{d}x}.$

- (x+1){e}^{2x}
- (2x+3){e}^{2x}
- (2x+1){e}^{2x}
- 2(x+1){e}^{2x}
- 2x{e}^{2x}

This question requires the product rule. Let $u(x)=x+1$ and $v(x)={e}^{2x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=2{e}^{2x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{2x})+(x+1)(2{e}^{2x}) \\  & ={e}^{2x}+2(x+1){e}^{2x} \\  & =(1+2(x+1)){e}^{2x} \\  & =(2x+3){e}^{2x}.\end{aligned}
$$

## Changed raw evidence / easy / q-11824

Given that $y=(x+1){e}^{2x},$ find $\frac{\text{d}y}{\text{d}x}.$

- (2x+1){e}^{2x}
- (2x+3){e}^{2x}
- (x+1){e}^{2x}
- 2x{e}^{2x}
- 2(x+1){e}^{2x}

This question requires the product rule. Let $u(x)=x+1$ and $v(x)={e}^{2x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=2{e}^{2x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{2x})+(x+1)(2{e}^{2x}) \\  & ={e}^{2x}+2(x+1){e}^{2x} \\  & =(1+2(x+1)){e}^{2x} \\  & =(2x+3){e}^{2x}.\end{aligned}
$$

## Changed raw evidence / easy / q-11824

Given that $y=(x+1){e}^{16x},$ find $\frac{\text{d}y}{\text{d}x}.$

- (16x+1){e}^{16x}
- (16x+17){e}^{16x}
- (x+1){e}^{16x}
- 16x{e}^{16x}
- 16(x+1){e}^{16x}

This question requires the product rule. Let $u(x)=x+1$ and $v(x)={e}^{16x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=16{e}^{16x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{16x})+(x+1)(16{e}^{16x}) \\  & ={e}^{16x}+16(x+1){e}^{16x} \\  & =(1+16(x+1)){e}^{16x} \\  & =(16x+17){e}^{16x}.\end{aligned}
$$

## Eligible generated variant / easy / q-2392

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={a}^{3x}\operatorname{tan}⁡x.$

- {a}^{3x}{sec}^{2}⁡x+3\operatorname{tan}⁡x
- {a}^{3x}({sec}^{2}⁡x+3\operatorname{tan}⁡x)
- {a}^{3x}({sec}^{2}⁡x+3\operatorname{ln}⁡a\operatorname{tan}⁡x)
- 3{sec}^{2}⁡x+3{a}^{3x}\operatorname{tan}⁡x
- 3{a}^{3x}({sec}^{2}⁡x+\operatorname{ln}⁡a\operatorname{tan}⁡x)

This question requires the product rule. Let $u(x)=\operatorname{tan}⁡x$ and $v(x)={a}^{3x}.$ Then

$$
{u}^{′}(x)={sec}^{2}⁡x,\,{v}^{′}(x)=3{a}^{3x}\operatorname{ln}⁡a.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({sec}^{2}⁡x)({a}^{3x})+(\operatorname{tan}⁡x)(3{a}^{3x}\operatorname{ln}⁡a) \\  & ={a}^{3x}({sec}^{2}⁡x+3\operatorname{ln}⁡a\operatorname{tan}⁡x).\end{aligned}
$$

## Eligible generated variant / easy / q-2392

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={a}^{2x}\operatorname{tan}⁡x.$

- {a}^{2x}{sec}^{2}⁡x+2\operatorname{tan}⁡x
- {a}^{2x}({sec}^{2}⁡x+2\operatorname{tan}⁡x)
- {a}^{2x}({sec}^{2}⁡x+2\operatorname{ln}⁡a\operatorname{tan}⁡x)
- 2{sec}^{2}⁡x+2{a}^{2x}\operatorname{tan}⁡x
- 2{a}^{2x}({sec}^{2}⁡x+\operatorname{ln}⁡a\operatorname{tan}⁡x)

This question requires the product rule. Let $u(x)=\operatorname{tan}⁡x$ and $v(x)={a}^{2x}.$ Then

$$
{u}^{′}(x)={sec}^{2}⁡x,\,{v}^{′}(x)=2{a}^{2x}\operatorname{ln}⁡a.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({sec}^{2}⁡x)({a}^{2x})+(\operatorname{tan}⁡x)(2{a}^{2x}\operatorname{ln}⁡a) \\  & ={a}^{2x}({sec}^{2}⁡x+2\operatorname{ln}⁡a\operatorname{tan}⁡x).\end{aligned}
$$

## Eligible generated variant / easy / q-2392

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={a}^{16x}\operatorname{tan}⁡x.$

- 16{sec}^{2}⁡x+16{a}^{16x}\operatorname{tan}⁡x
- {a}^{16x}{sec}^{2}⁡x+16\operatorname{tan}⁡x
- 16{a}^{16x}({sec}^{2}⁡x+\operatorname{ln}⁡a\operatorname{tan}⁡x)
- {a}^{16x}({sec}^{2}⁡x+16\operatorname{tan}⁡x)
- {a}^{16x}({sec}^{2}⁡x+16\operatorname{ln}⁡a\operatorname{tan}⁡x)

This question requires the product rule. Let $u(x)=\operatorname{tan}⁡x$ and $v(x)={a}^{16x}.$ Then

$$
{u}^{′}(x)={sec}^{2}⁡x,\,{v}^{′}(x)=16{a}^{16x}\operatorname{ln}⁡a.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({sec}^{2}⁡x)({a}^{16x})+(\operatorname{tan}⁡x)(16{a}^{16x}\operatorname{ln}⁡a) \\  & ={a}^{16x}({sec}^{2}⁡x+16\operatorname{ln}⁡a\operatorname{tan}⁡x).\end{aligned}
$$

## Eligible generated variant / easy / q-2392

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={a}^{2x}\operatorname{tan}⁡x.$

- {a}^{2x}{sec}^{2}⁡x+2\operatorname{tan}⁡x
- {a}^{2x}({sec}^{2}⁡x+2\operatorname{tan}⁡x)
- {a}^{2x}({sec}^{2}⁡x+2\operatorname{ln}⁡a\operatorname{tan}⁡x)
- 2{sec}^{2}⁡x+2{a}^{2x}\operatorname{tan}⁡x
- 2{a}^{2x}({sec}^{2}⁡x+\operatorname{ln}⁡a\operatorname{tan}⁡x)

This question requires the product rule. Let $u(x)=\operatorname{tan}⁡x$ and $v(x)={a}^{2x}.$ Then

$$
{u}^{′}(x)={sec}^{2}⁡x,\,{v}^{′}(x)=2{a}^{2x}\operatorname{ln}⁡a.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({sec}^{2}⁡x)({a}^{2x})+(\operatorname{tan}⁡x)(2{a}^{2x}\operatorname{ln}⁡a) \\  & ={a}^{2x}({sec}^{2}⁡x+2\operatorname{ln}⁡a\operatorname{tan}⁡x).\end{aligned}
$$

## Changed raw evidence / easy / q-2392

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={a}^{2x}\operatorname{tan}⁡x.$

- {a}^{2x}({sec}^{2}⁡x+2\operatorname{ln}⁡a\operatorname{tan}⁡x)
- {a}^{2x}({sec}^{2}⁡x+2\operatorname{tan}⁡x)
- {a}^{2x}{sec}^{2}⁡x+2\operatorname{tan}⁡x
- 2{a}^{2x}({sec}^{2}⁡x+\operatorname{ln}⁡a\operatorname{tan}⁡x)
- 2{sec}^{2}⁡x+2{a}^{2x}\operatorname{tan}⁡x

This question requires the product rule. Let $u(x)=\operatorname{tan}⁡x$ and $v(x)={a}^{2x}.$ Then

$$
{u}^{′}(x)={sec}^{2}⁡x,\,{v}^{′}(x)=2{a}^{2x}\operatorname{ln}⁡a.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({sec}^{2}⁡x)({a}^{2x})+(\operatorname{tan}⁡x)(2{a}^{2x}\operatorname{ln}⁡a) \\  & ={a}^{2x}({sec}^{2}⁡x+2\operatorname{ln}⁡a\operatorname{tan}⁡x).\end{aligned}
$$

## Changed raw evidence / easy / q-2392

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={a}^{16x}\operatorname{tan}⁡x.$

- {a}^{16x}({sec}^{2}⁡x+16\operatorname{ln}⁡a\operatorname{tan}⁡x)
- {a}^{16x}({sec}^{2}⁡x+16\operatorname{tan}⁡x)
- {a}^{16x}{sec}^{2}⁡x+16\operatorname{tan}⁡x
- 16{a}^{16x}({sec}^{2}⁡x+\operatorname{ln}⁡a\operatorname{tan}⁡x)
- 16{sec}^{2}⁡x+16{a}^{16x}\operatorname{tan}⁡x

This question requires the product rule. Let $u(x)=\operatorname{tan}⁡x$ and $v(x)={a}^{16x}.$ Then

$$
{u}^{′}(x)={sec}^{2}⁡x,\,{v}^{′}(x)=16{a}^{16x}\operatorname{ln}⁡a.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({sec}^{2}⁡x)({a}^{16x})+(\operatorname{tan}⁡x)(16{a}^{16x}\operatorname{ln}⁡a) \\  & ={a}^{16x}({sec}^{2}⁡x+16\operatorname{ln}⁡a\operatorname{tan}⁡x).\end{aligned}
$$

## Eligible generated variant / moderate / q-9942

If $f(x)={x}^{2}\operatorname{sin}⁡(5x+2),$ find ${f}^{′}(x).$

- 2\operatorname{sin}⁡(5x+2)+5{x}^{2}\operatorname{cos}⁡(5x+2)
- 2x\operatorname{sin}⁡(5x+2)+{x}^{2}\operatorname{cos}⁡(5x+2)
- 2{x}^{2}\operatorname{sin}⁡(5x+2)+5x\operatorname{cos}⁡(5x+2)
- 5x\operatorname{sin}⁡(5x+2)+2{x}^{2}\operatorname{cos}⁡(5x+2)
- 2x\operatorname{sin}⁡(5x+2)+5{x}^{2}\operatorname{cos}⁡(5x+2)

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(5x+2).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=5\operatorname{cos}⁡(5x+2).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(5x+2))+({x}^{2})(5\operatorname{cos}⁡(5x+2)) \\  & =2x\operatorname{sin}⁡(5x+2)+5{x}^{2}\operatorname{cos}⁡(5x+2).\end{aligned}
$$

## Eligible generated variant / moderate / q-9942

If $f(x)={x}^{2}\operatorname{sin}⁡(3x-5),$ find ${f}^{′}(x).$

- 2\operatorname{sin}⁡(3x-5)+3{x}^{2}\operatorname{cos}⁡(3x-5)
- 2x\operatorname{sin}⁡(3x-5)+{x}^{2}\operatorname{cos}⁡(3x-5)
- 2{x}^{2}\operatorname{sin}⁡(3x-5)+3x\operatorname{cos}⁡(3x-5)
- 3x\operatorname{sin}⁡(3x-5)+2{x}^{2}\operatorname{cos}⁡(3x-5)
- 2x\operatorname{sin}⁡(3x-5)+3{x}^{2}\operatorname{cos}⁡(3x-5)

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(3x-5).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=3\operatorname{cos}⁡(3x-5).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(3x-5))+({x}^{2})(3\operatorname{cos}⁡(3x-5)) \\  & =2x\operatorname{sin}⁡(3x-5)+3{x}^{2}\operatorname{cos}⁡(3x-5).\end{aligned}
$$

## Eligible generated variant / moderate / q-9942

If $f(x)={x}^{2}\operatorname{sin}⁡(16x+5),$ find ${f}^{′}(x).$

- 2\operatorname{sin}⁡(16x+5)+16{x}^{2}\operatorname{cos}⁡(16x+5)
- 2x\operatorname{sin}⁡(16x+5)+{x}^{2}\operatorname{cos}⁡(16x+5)
- 16x\operatorname{sin}⁡(16x+5)+2{x}^{2}\operatorname{cos}⁡(16x+5)
- 2{x}^{2}\operatorname{sin}⁡(16x+5)+16x\operatorname{cos}⁡(16x+5)
- 2x\operatorname{sin}⁡(16x+5)+16{x}^{2}\operatorname{cos}⁡(16x+5)

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(16x+5).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=16\operatorname{cos}⁡(16x+5).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(16x+5))+({x}^{2})(16\operatorname{cos}⁡(16x+5)) \\  & =2x\operatorname{sin}⁡(16x+5)+16{x}^{2}\operatorname{cos}⁡(16x+5).\end{aligned}
$$

## Eligible generated variant / moderate / q-9942

If $f(x)={x}^{2}\operatorname{sin}⁡(3x+2),$ find ${f}^{′}(x).$

- 2\operatorname{sin}⁡(3x+2)+3{x}^{2}\operatorname{cos}⁡(3x+2)
- 2x\operatorname{sin}⁡(3x+2)+{x}^{2}\operatorname{cos}⁡(3x+2)
- 2{x}^{2}\operatorname{sin}⁡(3x+2)+3x\operatorname{cos}⁡(3x+2)
- 3x\operatorname{sin}⁡(3x+2)+2{x}^{2}\operatorname{cos}⁡(3x+2)
- 2x\operatorname{sin}⁡(3x+2)+3{x}^{2}\operatorname{cos}⁡(3x+2)

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(3x+2).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=3\operatorname{cos}⁡(3x+2).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(3x+2))+({x}^{2})(3\operatorname{cos}⁡(3x+2)) \\  & =2x\operatorname{sin}⁡(3x+2)+3{x}^{2}\operatorname{cos}⁡(3x+2).\end{aligned}
$$

## Eligible generated variant / moderate / q-9942

If $f(x)={x}^{2}\operatorname{sin}⁡(5x-5),$ find ${f}^{′}(x).$

- 2\operatorname{sin}⁡(5x-5)+5{x}^{2}\operatorname{cos}⁡(5x-5)
- 2x\operatorname{sin}⁡(5x-5)+{x}^{2}\operatorname{cos}⁡(5x-5)
- 2{x}^{2}\operatorname{sin}⁡(5x-5)+5x\operatorname{cos}⁡(5x-5)
- 5x\operatorname{sin}⁡(5x-5)+2{x}^{2}\operatorname{cos}⁡(5x-5)
- 2x\operatorname{sin}⁡(5x-5)+5{x}^{2}\operatorname{cos}⁡(5x-5)

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(5x-5).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=5\operatorname{cos}⁡(5x-5).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(5x-5))+({x}^{2})(5\operatorname{cos}⁡(5x-5)) \\  & =2x\operatorname{sin}⁡(5x-5)+5{x}^{2}\operatorname{cos}⁡(5x-5).\end{aligned}
$$

## Changed raw evidence / moderate / q-9942

If $f(x)={x}^{2}\operatorname{sin}⁡(3x-5),$ find ${f}^{′}(x).$

- 2{x}^{2}\operatorname{sin}⁡(3x-5)+3x\operatorname{cos}⁡(3x-5)
- 2x\operatorname{sin}⁡(3x-5)+{x}^{2}\operatorname{cos}⁡(3x-5)
- 2\operatorname{sin}⁡(3x-5)+3{x}^{2}\operatorname{cos}⁡(3x-5)
- 2x\operatorname{sin}⁡(3x-5)+3{x}^{2}\operatorname{cos}⁡(3x-5)
- 3x\operatorname{sin}⁡(3x-5)+2{x}^{2}\operatorname{cos}⁡(3x-5)

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(3x-5).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=3\operatorname{cos}⁡(3x-5).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(3x-5))+({x}^{2})(3\operatorname{cos}⁡(3x-5)) \\  & =2x\operatorname{sin}⁡(3x-5)+3{x}^{2}\operatorname{cos}⁡(3x-5).\end{aligned}
$$

## Changed raw evidence / moderate / q-9942

If $f(x)={x}^{2}\operatorname{sin}⁡(16x+5),$ find ${f}^{′}(x).$

- 2{x}^{2}\operatorname{sin}⁡(16x+5)+16x\operatorname{cos}⁡(16x+5)
- 2x\operatorname{sin}⁡(16x+5)+{x}^{2}\operatorname{cos}⁡(16x+5)
- 2\operatorname{sin}⁡(16x+5)+16{x}^{2}\operatorname{cos}⁡(16x+5)
- 2x\operatorname{sin}⁡(16x+5)+16{x}^{2}\operatorname{cos}⁡(16x+5)
- 16x\operatorname{sin}⁡(16x+5)+2{x}^{2}\operatorname{cos}⁡(16x+5)

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(16x+5).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=16\operatorname{cos}⁡(16x+5).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(16x+5))+({x}^{2})(16\operatorname{cos}⁡(16x+5)) \\  & =2x\operatorname{sin}⁡(16x+5)+16{x}^{2}\operatorname{cos}⁡(16x+5).\end{aligned}
$$

## Eligible generated variant / moderate / q-2401

Find ${y}^{′}$ for $y=4{x}^{2}\sqrt{\operatorname{sin}⁡x}.$

- \frac{2{x}^{2}\operatorname{sin}⁡x-8x\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- \frac{2{x}^{2}\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}-x\sqrt{\operatorname{sin}⁡x}
- \frac{x\operatorname{cos}⁡x+2x\operatorname{sin}⁡x}{\operatorname{sin}⁡x}
- -\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{cos}⁡x}}+8x\sqrt{\operatorname{sin}⁡x}
- \frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}

This question requires the product rule. Let $u(x)=4{x}^{2}$ and $v(x)=\sqrt{\operatorname{sin}⁡x}.$ Then

$$
{u}^{′}(x)=8x,\,{v}^{′}(x)=\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{y}^{′}=\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(8x)(\sqrt{\operatorname{sin}⁡x})+(4{x}^{2})(\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}) \\  & =8x\sqrt{\operatorname{sin}⁡x}+\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}} \\  & =\frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}.\end{aligned}
$$

## Eligible generated variant / moderate / q-2401

Find ${y}^{′}$ for $y=4{x}^{2}\sqrt{\operatorname{sin}⁡x}.$

- \frac{2{x}^{2}\operatorname{sin}⁡x-8x\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- \frac{2{x}^{2}\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}-x\sqrt{\operatorname{sin}⁡x}
- \frac{x\operatorname{cos}⁡x+2x\operatorname{sin}⁡x}{\operatorname{sin}⁡x}
- -\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{cos}⁡x}}+8x\sqrt{\operatorname{sin}⁡x}
- \frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}

This question requires the product rule. Let $u(x)=4{x}^{2}$ and $v(x)=\sqrt{\operatorname{sin}⁡x}.$ Then

$$
{u}^{′}(x)=8x,\,{v}^{′}(x)=\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{y}^{′}=\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(8x)(\sqrt{\operatorname{sin}⁡x})+(4{x}^{2})(\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}) \\  & =8x\sqrt{\operatorname{sin}⁡x}+\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}} \\  & =\frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}.\end{aligned}
$$

## Eligible generated variant / moderate / q-2401

Find ${y}^{′}$ for $y=24{x}^{2}\sqrt{\operatorname{sin}⁡x}.$

- \frac{6x\operatorname{cos}⁡x+12x\operatorname{sin}⁡x}{\operatorname{sin}⁡x}
- \frac{12{x}^{2}\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}-6x\sqrt{\operatorname{sin}⁡x}
- \frac{48x\operatorname{sin}⁡x+12{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- \frac{12{x}^{2}\operatorname{sin}⁡x-48x\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- -\frac{12{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{cos}⁡x}}+48x\sqrt{\operatorname{sin}⁡x}

This question requires the product rule. Let $u(x)=24{x}^{2}$ and $v(x)=\sqrt{\operatorname{sin}⁡x}.$ Then

$$
{u}^{′}(x)=48x,\,{v}^{′}(x)=\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{y}^{′}=\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(48x)(\sqrt{\operatorname{sin}⁡x})+(24{x}^{2})(\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}) \\  & =48x\sqrt{\operatorname{sin}⁡x}+\frac{12{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}} \\  & =\frac{48x\operatorname{sin}⁡x+12{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}.\end{aligned}
$$

## Eligible generated variant / moderate / q-2401

Find ${y}^{′}$ for $y=8{x}^{2}\sqrt{\operatorname{sin}⁡x}.$

- \frac{4{x}^{2}\operatorname{sin}⁡x-16x\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- \frac{4{x}^{2}\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}-2x\sqrt{\operatorname{sin}⁡x}
- \frac{2x\operatorname{cos}⁡x+4x\operatorname{sin}⁡x}{\operatorname{sin}⁡x}
- -\frac{4{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{cos}⁡x}}+16x\sqrt{\operatorname{sin}⁡x}
- \frac{16x\operatorname{sin}⁡x+4{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}

This question requires the product rule. Let $u(x)=8{x}^{2}$ and $v(x)=\sqrt{\operatorname{sin}⁡x}.$ Then

$$
{u}^{′}(x)=16x,\,{v}^{′}(x)=\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{y}^{′}=\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(16x)(\sqrt{\operatorname{sin}⁡x})+(8{x}^{2})(\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}) \\  & =16x\sqrt{\operatorname{sin}⁡x}+\frac{4{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}} \\  & =\frac{16x\operatorname{sin}⁡x+4{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}.\end{aligned}
$$

## Changed raw evidence / moderate / q-2401

Find ${y}^{′}$ for $y=4{x}^{2}\sqrt{\operatorname{sin}⁡x}.$

- \frac{x\operatorname{cos}⁡x+2x\operatorname{sin}⁡x}{\operatorname{sin}⁡x}
- \frac{2{x}^{2}\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}-x\sqrt{\operatorname{sin}⁡x}
- \frac{2{x}^{2}\operatorname{sin}⁡x-8x\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- \frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- -\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{cos}⁡x}}+8x\sqrt{\operatorname{sin}⁡x}

This question requires the product rule. Let $u(x)=4{x}^{2}$ and $v(x)=\sqrt{\operatorname{sin}⁡x}.$ Then

$$
{u}^{′}(x)=8x,\,{v}^{′}(x)=\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{y}^{′}=\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(8x)(\sqrt{\operatorname{sin}⁡x})+(4{x}^{2})(\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}) \\  & =8x\sqrt{\operatorname{sin}⁡x}+\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}} \\  & =\frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}.\end{aligned}
$$

## Changed raw evidence / moderate / q-2401

Find ${y}^{′}$ for $y=24{x}^{2}\sqrt{\operatorname{sin}⁡x}.$

- \frac{6x\operatorname{cos}⁡x+12x\operatorname{sin}⁡x}{\operatorname{sin}⁡x}
- \frac{12{x}^{2}\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}-6x\sqrt{\operatorname{sin}⁡x}
- \frac{12{x}^{2}\operatorname{sin}⁡x-48x\operatorname{sin}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- \frac{48x\operatorname{sin}⁡x+12{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}
- -\frac{12{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{cos}⁡x}}+48x\sqrt{\operatorname{sin}⁡x}

This question requires the product rule. Let $u(x)=24{x}^{2}$ and $v(x)=\sqrt{\operatorname{sin}⁡x}.$ Then

$$
{u}^{′}(x)=48x,\,{v}^{′}(x)=\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{y}^{′}=\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(48x)(\sqrt{\operatorname{sin}⁡x})+(24{x}^{2})(\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}) \\  & =48x\sqrt{\operatorname{sin}⁡x}+\frac{12{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}} \\  & =\frac{48x\operatorname{sin}⁡x+12{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}.\end{aligned}
$$

## Eligible generated variant / hard / q-11599

If $y = x^{3}(2x^{2} + 1)^{3}$, find $\frac{dy}{dx}$.

- (18x^{4} + 3x^{2})(2x^{2} + 1)^{3}
- (12x^{4} + 3x^{2})(2x^{2} + 1)^{2}
- (12x^{4} + x^{2})(2x^{2} + 1)^{2}
- (3x^{4} + 12x^{2})(2x^{2} + 1)^{2}
- (18x^{4} + 3x^{2})(2x^{2} + 1)^{2}

This question requires the product rule. Let $u(x)=x^{3}$ and $v(x)=(2 x^{2} + 1)^{3}.$ Then

$$
u^{′}(x)=3x^{2},\,v^{′}(x)=12x(2 x^{2} + 1)^{2}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u^{′}(x)\cdot v(x)+u(x)\cdot v^{′}(x) \\  & =(3x^{2})((2 x^{2} + 1)^{3})+(x^{3})(12x(2 x^{2} + 1)^{2}) \\  & =3x^{2}(2 x^{2} + 1)^{3}+12x^{4}(2 x^{2} + 1)^{2} \\  & =(3x^{2}(2 x^{2} + 1)+12x^{4})(2 x^{2} + 1)^{2} \\  & =(18x^{4}+3x^{2})(2 x^{2} + 1)^{2}.\end{aligned}
$$

## Eligible generated variant / hard / q-11599

If $y = x^{3}(2x^{2} + 1)^{3}$, find $\frac{dy}{dx}$.

- (18x^{4} + 3x^{2})(2x^{2} + 1)^{3}
- (12x^{4} + 3x^{2})(2x^{2} + 1)^{2}
- (12x^{4} + x^{2})(2x^{2} + 1)^{2}
- (3x^{4} + 12x^{2})(2x^{2} + 1)^{2}
- (18x^{4} + 3x^{2})(2x^{2} + 1)^{2}

This question requires the product rule. Let $u(x)=x^{3}$ and $v(x)=(2 x^{2} + 1)^{3}.$ Then

$$
u^{′}(x)=3x^{2},\,v^{′}(x)=12x(2 x^{2} + 1)^{2}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u^{′}(x)\cdot v(x)+u(x)\cdot v^{′}(x) \\  & =(3x^{2})((2 x^{2} + 1)^{3})+(x^{3})(12x(2 x^{2} + 1)^{2}) \\  & =3x^{2}(2 x^{2} + 1)^{3}+12x^{4}(2 x^{2} + 1)^{2} \\  & =(3x^{2}(2 x^{2} + 1)+12x^{4})(2 x^{2} + 1)^{2} \\  & =(18x^{4}+3x^{2})(2 x^{2} + 1)^{2}.\end{aligned}
$$

## Eligible generated variant / hard / q-11599

If $y = x^{3}(9x^{2} + 9)^{3}$, find $\frac{dy}{dx}$.

- (54x^{4} + 27x^{2})(9x^{2} + 9)^{2}
- (27x^{4} + 54x^{2})(9x^{2} + 9)^{2}
- (81x^{4} + 27x^{2})(9x^{2} + 9)^{3}
- (54x^{4} + 9x^{2})(9x^{2} + 9)^{2}
- (81x^{4} + 27x^{2})(9x^{2} + 9)^{2}

This question requires the product rule. Let $u(x)=x^{3}$ and $v(x)=(9 x^{2} + 9)^{3}.$ Then

$$
u^{′}(x)=3x^{2},\,v^{′}(x)=54x(9 x^{2} + 9)^{2}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u^{′}(x)\cdot v(x)+u(x)\cdot v^{′}(x) \\  & =(3x^{2})((9 x^{2} + 9)^{3})+(x^{3})(54x(9 x^{2} + 9)^{2}) \\  & =3x^{2}(9 x^{2} + 9)^{3}+54x^{4}(9 x^{2} + 9)^{2} \\  & =(3x^{2}(9 x^{2} + 9)+54x^{4})(9 x^{2} + 9)^{2} \\  & =(81x^{4}+27x^{2})(9 x^{2} + 9)^{2}.\end{aligned}
$$

## Eligible generated variant / hard / q-11599

If $y = x^{3}(3x^{2} + 1)^{3}$, find $\frac{dy}{dx}$.

- (27x^{4} + 3x^{2})(3x^{2} + 1)^{3}
- (18x^{4} + 3x^{2})(3x^{2} + 1)^{2}
- (18x^{4} + x^{2})(3x^{2} + 1)^{2}
- (3x^{4} + 18x^{2})(3x^{2} + 1)^{2}
- (27x^{4} + 3x^{2})(3x^{2} + 1)^{2}

This question requires the product rule. Let $u(x)=x^{3}$ and $v(x)=(3 x^{2} + 1)^{3}.$ Then

$$
u^{′}(x)=3x^{2},\,v^{′}(x)=18x(3 x^{2} + 1)^{2}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u^{′}(x)\cdot v(x)+u(x)\cdot v^{′}(x) \\  & =(3x^{2})((3 x^{2} + 1)^{3})+(x^{3})(18x(3 x^{2} + 1)^{2}) \\  & =3x^{2}(3 x^{2} + 1)^{3}+18x^{4}(3 x^{2} + 1)^{2} \\  & =(3x^{2}(3 x^{2} + 1)+18x^{4})(3 x^{2} + 1)^{2} \\  & =(27x^{4}+3x^{2})(3 x^{2} + 1)^{2}.\end{aligned}
$$

## Eligible generated variant / hard / q-11599

If $y = x^{3}(2x^{2} + 2)^{3}$, find $\frac{dy}{dx}$.

- (18x^{4} + 6x^{2})(2x^{2} + 2)^{3}
- (12x^{4} + 6x^{2})(2x^{2} + 2)^{2}
- (12x^{4} + 2x^{2})(2x^{2} + 2)^{2}
- (6x^{4} + 12x^{2})(2x^{2} + 2)^{2}
- (18x^{4} + 6x^{2})(2x^{2} + 2)^{2}

This question requires the product rule. Let $u(x)=x^{3}$ and $v(x)=(2 x^{2} + 2)^{3}.$ Then

$$
u^{′}(x)=3x^{2},\,v^{′}(x)=12x(2 x^{2} + 2)^{2}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u^{′}(x)\cdot v(x)+u(x)\cdot v^{′}(x) \\  & =(3x^{2})((2 x^{2} + 2)^{3})+(x^{3})(12x(2 x^{2} + 2)^{2}) \\  & =3x^{2}(2 x^{2} + 2)^{3}+12x^{4}(2 x^{2} + 2)^{2} \\  & =(3x^{2}(2 x^{2} + 2)+12x^{4})(2 x^{2} + 2)^{2} \\  & =(18x^{4}+6x^{2})(2 x^{2} + 2)^{2}.\end{aligned}
$$

## Changed raw evidence / hard / q-11599

If $y = x^{3}(2x^{2} + 1)^{3}$, find $\frac{dy}{dx}$.

- (12x^{4} + x^{2})(2x^{2} + 1)^{2}
- (12x^{4} + 3x^{2})(2x^{2} + 1)^{2}
- (18x^{4} + 3x^{2})(2x^{2} + 1)^{3}
- (18x^{4} + 3x^{2})(2x^{2} + 1)^{2}
- (3x^{4} + 12x^{2})(2x^{2} + 1)^{2}

## Changed raw evidence / hard / q-11599

If $y = x^{3}(9x^{2} + 9)^{3}$, find $\frac{dy}{dx}$.

- (54x^{4} + 9x^{2})(9x^{2} + 9)^{2}
- (54x^{4} + 27x^{2})(9x^{2} + 9)^{2}
- (81x^{4} + 27x^{2})(9x^{2} + 9)^{3}
- (81x^{4} + 27x^{2})(9x^{2} + 9)^{2}
- (27x^{4} + 54x^{2})(9x^{2} + 9)^{2}
