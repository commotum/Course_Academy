# Original source evidence and generated review

Original math database basis 1356. All generated records below are explicitly labeled; raw originals remain in source.json.

## q-48391 — original

If a curve $C$ is given by $y = 2e^{x}(x + 1)$, calculate the slope of the tangent line to the curve at the point where $x = 0$.

[No captured worked solution]


Original banks: [[{":answer/id": "a701631f-ee6f-5c74-8945-ae030b322172", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "2", ":db/id": 17592186095407}, {":answer/id": "b33ae4fd-7df5-5668-be3f-6da8b92a1f35", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "4", ":db/id": 17592186095408}, {":answer/id": "e5c620ec-258c-57ed-8f58-6c1af87e31f9", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "\\sqrt{2}e", ":db/id": 17592186095409}, {":answer/id": "30ae4bc2-f079-544b-81c3-abc3d5c10ec8", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "0", ":db/id": 17592186095410}, {":answer/id": "497ee82d-da93-5f82-adc3-3cb7e1142e53", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "2e", ":db/id": 17592186095411}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(2 e^{x})\cdot (x + 1)$, calculate the slope of the tangent line to the curve at the point where $x=0$.

- $2$
- $\sqrt{2} e$
- $4$
- $0$
- $2 e$

We differentiate using the product rule. Let $u(x)=2 e^{x}$ and $v(x)=x + 1.$ Then, we have

$$
u'(x)=2 e^{x},\quad v'(x)=1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(2 e^{x})\cdot (1)+(x + 1)\cdot (2 e^{x}) \\ &=2 x e^{x} + 4 e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=2 (0) e^{(0)} + 4 e^{(0)} \\ &=(2)\cdot (1)+(1)\cdot (2) \\ &=4.\end{aligned}
$$

Therefore, the slope of the tangent line is $4.$

## q-48901 — original

If a curve $C$ is given by $y = 8x^{3}\sin x$, calculate the slope of the tangent line to the curve at the point where $x = \frac{π}{2}$.

[No captured worked solution]


Original banks: [[{":answer/id": "9c7eb625-3ff4-5e82-bd70-a085123a70c7", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "3π^{2}", ":db/id": 17592186095485}, {":answer/id": "d4b825b6-1cae-5e24-9e36-665ccf694b7d", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-6π^{2}", ":db/id": 17592186095486}, {":answer/id": "3ab1f0af-b2c2-5a25-97d0-1ea8b6003204", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-3π^{2}", ":db/id": 17592186095487}, {":answer/id": "5e676af8-cf84-5f73-998c-145d20246a1c", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "0", ":db/id": 17592186095488}, {":answer/id": "73d74933-2b73-5e41-8a53-45938d45db82", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "6π^{2}", ":db/id": 17592186095489}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(8 x^{3})\cdot (\sin{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=\frac{\pi}{2}$.

- $3 \pi^{2}$
- $- 3 \pi^{2}$
- $- 6 \pi^{2}$
- $0$
- $6 \pi^{2}$

We differentiate using the product rule. Let $u(x)=8 x^{3}$ and $v(x)=\sin{\left(x \right)}.$ Then, we have

$$
u'(x)=24 x^{2},\quad v'(x)=\cos{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(8 x^{3})\cdot (\cos{\left(x \right)})+(\sin{\left(x \right)})\cdot (24 x^{2}) \\ &=8 x^{3} \cos{\left(x \right)} + 24 x^{2} \sin{\left(x \right)}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{2}} &=8 (\frac{\pi}{2})^{3} \cos{\left((\frac{\pi}{2}) \right)} + 24 (\frac{\pi}{2})^{2} \sin{\left((\frac{\pi}{2}) \right)} \\ &=(\pi^{3})\cdot (0)+(1)\cdot (6 \pi^{2}) \\ &=6 \pi^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $6 \pi^{2}.$

## q-31226 — original

If a curve $C$ is given by $y=3{x}^{2}\operatorname{tan}x,$ calculate the slope of the tangent line to the curve at the point where $x=\pi .$

We differentiate using the product rule. Let $u(x)=3{x}^{2}$ and $v(x)=\operatorname{tan}x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=6x,\,\frac{\text{d}v}{\text{d}x}={sec}^{2}x.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & =(3{x}^{2})({sec}^{2}x)+(\operatorname{tan}x)(6x) \\  & =3{x}^{2}{sec}^{2}x+6x\operatorname{tan}x.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi $ into the formula and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}{|}_{x=\pi } & =3{x}^{2}{sec}^{2}x+6x\operatorname{tan}x{|}_{x=\pi } \\  & =3(\pi )^{2}{sec}^{2}(\pi )+6(\pi )\operatorname{tan}(\pi ) \\  & =3{\pi }^{2}\cdot 1+6\pi \cdot 0 \\  & =3{\pi }^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $3{\pi }^{2}.$


Original banks: []

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(3 x^{2})\cdot (\tan{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

Slope $=$ {{field-1}}

- $3 \pi^{2}$

We differentiate using the product rule. Let $u(x)=3 x^{2}$ and $v(x)=\tan{\left(x \right)}.$ Then, we have

$$
u'(x)=6 x,\quad v'(x)=\tan^{2}{\left(x \right)} + 1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x^{2})\cdot (\tan^{2}{\left(x \right)} + 1)+(\tan{\left(x \right)})\cdot (6 x) \\ &=3 x^{2}\sec^{2}x+6 x\tan x.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=\left.3 x^{2}\sec^{2}x+6 x\tan x\right|_{x=\pi} \\ &=3 (\pi)^{2}\sec^{2}(\pi)+6 (\pi)\tan (\pi) \\ &=(3 \pi^{2})\cdot (1)+(0)\cdot (6 \pi) \\ &=3 \pi^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $3 \pi^{2}.$

## q-319825 — original

If a curve $C$ is given by $y=(x-1)\operatorname{ln}(2x+1),$ calculate the slope of the tangent line to the curve at the point where $x=0$ is{{field-1}}.

We differentiate using the product rule. Let $u(x)=x-1$ and $v(x)=\operatorname{ln}(2x+1).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=1,\,\frac{\text{d}v}{\text{d}x}=\frac{2}{2x+1}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & =(x-1)\cdot \frac{2}{2x+1}+\operatorname{ln}(2x+1)\cdot 1 \\  & =\frac{2(x-1)}{2x+1}+\operatorname{ln}(2x+1).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=0} & =\frac{2(0-1)}{2(0)+1}+\operatorname{ln}(2(0)+1) \\  & =(-2)+\operatorname{ln}(1) \\  & =-2.\end{aligned}
$$

Therefore, the slope of the tangent line is $-2.$


Original banks: [[{":answer/id": "0b9bc784-4648-528a-ac26-6d3516a71384", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-2", ":db/id": 17592186232589}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(x - 1)\cdot (\ln{\left(2 x + 1 \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=0$ is{{field-1}}.

- $-2$

We differentiate using the product rule. Let $u(x)=x - 1$ and $v(x)=\ln{\left(2 x + 1 \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=\frac{2}{2 x + 1}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x - 1)\cdot (\frac{2}{2 x + 1})+(\ln{\left(2 x + 1 \right)})\cdot (1) \\ &=\frac{2(x - 1)}{2 x + 1}+(1)\cdot (\ln{\left(2 x + 1 \right)}).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=\frac{2((0) - 1)}{2 (0) + 1}+(1)\cdot (\ln{\left(2 (0) + 1 \right)}) \\ &=(-2)+1\ln(1) \\ &=-2.\end{aligned}
$$

Therefore, the slope of the tangent line is $-2.$

## q-167326 — original

If a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\pi .$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

We differentiate using the product rule. Recall that $f(x)=\frac{1}{2}{e}^{x}$ and $h(x)=-4\operatorname{sin}⁡x.$ Then,

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(\frac{1}{2}{e}^{x})=\frac{1}{2}{e}^{x} \\ \frac{\text{d}h}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-4\operatorname{sin}⁡x)=-4\operatorname{cos}⁡x.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =f\frac{\text{d}h}{\text{d}x}+h\frac{\text{d}f}{\text{d}x} \\  & =\frac{1}{2}{e}^{x}\cdot (-4\operatorname{cos}⁡x)+(-4\operatorname{sin}⁡x)\cdot \frac{1}{2}{e}^{x} \\  & =-2{e}^{x}(\operatorname{cos}⁡x+\operatorname{sin}⁡x).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi $ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=\pi } & =-2{e}^{\pi }(\operatorname{cos}⁡\pi +\operatorname{sin}⁡\pi ) \\  & =-2{e}^{\pi }(-1+0) \\  & =2{e}^{\pi }.\end{aligned}
$$

Therefore, the slope of the tangent line is $2{e}^{\pi }.$


Original banks: [[{":answer/id": "ead734d2-e970-5e92-9ac3-1260bbfab982", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "2{e}^{\\pi }", ":db/id": 17592186234918}]]

### Generated original-parameter normalized replay

Given $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 4 \sin{\left(x \right)}$, if a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $2 e^{\pi}$

We differentiate using the product rule. Recall that $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 4 \sin{\left(x \right)}.$ Then,

$$
\begin{aligned}\frac{\mathrm df}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(\frac{e^{x}}{2})=\frac{e^{x}}{2} \\ \frac{\mathrm dh}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(- 4 \sin{\left(x \right)})=- 4 \cos{\left(x \right)}.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=fh'(x)+hf'(x) \\ &=(\frac{e^{x}}{2})\cdot (- 4 \cos{\left(x \right)})+(- 4 \sin{\left(x \right)})\cdot (\frac{e^{x}}{2}) \\ &=- 2 e^{x}(\cos x+\sin x).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=- 2 e^{(\pi)}(\cos (\pi)+\sin (\pi)) \\ &=- 2 e^{\pi}(-1+0) \\ &=2 e^{\pi}.\end{aligned}
$$

Therefore, the slope of the tangent line is $2 e^{\pi}.$

## q-167780 — original

If a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\pi .$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

We differentiate using the product rule. Recall that $f(x)=\frac{1}{2}{e}^{x}$ and $h(x)=-4\operatorname{sin}⁡(x).$ Then,

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(\frac{1}{2}{e}^{x})=\frac{1}{2}{e}^{x} \\ \frac{\text{d}h}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-4\operatorname{sin}⁡x)=-4\operatorname{cos}⁡(x).\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =f\frac{\text{d}h}{\text{d}x}+h\frac{\text{d}f}{\text{d}x} \\  & =\frac{1}{2}{e}^{x}\cdot (-4\operatorname{cos}⁡(x))+(-4\operatorname{sin}⁡(x))\cdot \frac{1}{2}{e}^{x} \\  & =-2{e}^{x}(\operatorname{cos}⁡(x)+\operatorname{sin}⁡(x)).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi $ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=\pi } & =-2{e}^{\pi }(\operatorname{cos}⁡(\pi )+\operatorname{sin}⁡(\pi )) \\  & =-2{e}^{\pi }(-1+0) \\  & =2{e}^{\pi }.\end{aligned}
$$

Therefore, the slope of the tangent line is $2{e}^{\pi }.$


Original banks: [[{":answer/id": "dbf988f2-8940-5547-8a0c-461e7fba4865", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "2{e}^{\\pi }", ":db/id": 17592186234891}]]

### Generated original-parameter normalized replay

Given $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 4 \sin{\left(x \right)}$, if a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $2 e^{\pi}$

We differentiate using the product rule. Recall that $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 4 \sin{\left(x \right)}.$ Then,

$$
\begin{aligned}\frac{\mathrm df}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(\frac{e^{x}}{2})=\frac{e^{x}}{2} \\ \frac{\mathrm dh}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(- 4 \sin{\left(x \right)})=- 4 \cos{\left(x \right)}.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=fh'(x)+hf'(x) \\ &=(\frac{e^{x}}{2})\cdot (- 4 \cos{\left(x \right)})+(- 4 \sin{\left(x \right)})\cdot (\frac{e^{x}}{2}) \\ &=- 2 e^{x}(\cos x+\sin x).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=- 2 e^{(\pi)}(\cos (\pi)+\sin (\pi)) \\ &=- 2 e^{\pi}(-1+0) \\ &=2 e^{\pi}.\end{aligned}
$$

Therefore, the slope of the tangent line is $2 e^{\pi}.$

## q-319806 — original

If a curve $C$ is given by $y=(x+2)cos⁡x,$ then the slope of the tangent line to the curve at the point where $x=\frac{\pi }{2}$ is{{field-1}}.

We differentiate using the product rule. Let $u(x)=x+2$ and $v(x)=cos⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=1,\,\frac{\text{d}v}{\text{d}x}=-sin⁡x.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & =(x+2)\cdot (-sin⁡x)+cos⁡x\cdot 1 \\  & =-(x+2)sin⁡x+cos⁡x.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi }{2}$ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=\frac{\pi }{2}} & =-(\frac{\pi }{2}+2)sin⁡\frac{\pi }{2}+cos⁡\frac{\pi }{2} \\  & =-(\frac{\pi }{2}+2)(1)+0 \\  & =-\frac{\pi }{2}-2.\end{aligned}
$$

Therefore, the slope of the tangent line is $-\frac{\pi }{2}-2.$


Original banks: [[{":answer/id": "94fe4615-3627-5184-b596-faacf4579fe9", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-\\frac{\\pi }{2}-2", ":db/id": 17592186298195}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(x + 2)\cdot (\cos{\left(x \right)}),$ then the slope of the tangent line to the curve at the point where $x=\frac{\pi}{2}$ is{{field-1}}.

- $-2 - \frac{\pi}{2}$

We differentiate using the product rule. Let $u(x)=x + 2$ and $v(x)=\cos{\left(x \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=- \sin{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x + 2)\cdot (- \sin{\left(x \right)})+(\cos{\left(x \right)})\cdot (1) \\ &=-(x + 2)\sin x+1\cos x.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{2}} &=-((\frac{\pi}{2}) + 2)\sin (\frac{\pi}{2})+1\cos (\frac{\pi}{2}) \\ &=(\frac{\pi}{2} + 2)\cdot (-1)+(0)\cdot (1) \\ &=-2 - \frac{\pi}{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $-2 - \frac{\pi}{2}.$

## q-319829 — original

If a curve $C$ is given by $y=(x-1)ln⁡(4x-3),$ calculate the slope of the tangent line to the curve at the point where $x=1$ is{{field-1}}.

We differentiate using the product rule. Let $u(x)=x-1$ and $v(x)=ln⁡(4x-3).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=1,\,\frac{\text{d}v}{\text{d}x}=\frac{4}{4x-3}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & =(x-1)\cdot \frac{4}{4x-3}+ln⁡(4x-3).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & =(1-1)\cdot \frac{4}{4(1)-3}+ln⁡(4(1)-3) \\  & =0+ln⁡(1)=0.\end{aligned}
$$

Therefore, the slope of the tangent line is $0.$


Original banks: [[{":answer/id": "7a9ff769-7920-54d9-9d56-bc88c33849af", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "0", ":db/id": 17592186298084}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(x - 1)\cdot (\ln{\left(4 x - 3 \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=1$ is{{field-1}}.

- $0$

We differentiate using the product rule. Let $u(x)=x - 1$ and $v(x)=\ln{\left(4 x - 3 \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=\frac{4}{4 x - 3}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x - 1)\cdot (\frac{4}{4 x - 3})+(\ln{\left(4 x - 3 \right)})\cdot (1).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=1} &=\frac{4((1) - 1)}{4 (1) - 3}+(1)\cdot (\ln{\left(4 (1) - 3 \right)}) \\ &=(0)+1\ln(1)=0.\end{aligned}
$$

Therefore, the slope of the tangent line is $0.$

## q-319842 — original

If a curve $C$ is given by $y=({x}^{2}-4x+7){e}^{x},$ calculate the slope of the tangent line to the curve at the point where $x=0$ is{{field-1}}.

We differentiate using the product rule. Let $u(x)={x}^{2}-4x+7$ and $v(x)={e}^{x}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=2x-4,\,\frac{\text{d}v}{\text{d}x}={e}^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & =({x}^{2}-4x+7)\cdot {e}^{x}+{e}^{x}\cdot (2x-4) \\  & ={e}^{x}({x}^{2}-2x+3).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=0} & ={{e}^{x}({x}^{2}-2x+3)|}_{x=0} \\  & =1\cdot (0-0+3)=3.\end{aligned}
$$

Therefore, the slope of the tangent line is $3.$


Original banks: [[{":answer/id": "8bfce910-f1a6-55e0-aa0a-ef391e8972f8", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "3", ":db/id": 17592186298162}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(x^{2} - 4 x + 7)\cdot (e^{x}),$ calculate the slope of the tangent line to the curve at the point where $x=0$ is{{field-1}}.

- $3$

We differentiate using the product rule. Let $u(x)=x^{2} - 4 x + 7$ and $v(x)=e^{x}.$ Then, we have

$$
u'(x)=2 x - 4,\quad v'(x)=e^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x^{2} - 4 x + 7)\cdot (e^{x})+(e^{x})\cdot (2 x - 4) \\ &=e^{x}(x^{2} - 2 x + 3).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=\left.e^{x}(x^{2} - 2 x + 3)\right|_{x=0} \\ &=1\cdot (0-0+3)=3.\end{aligned}
$$

Therefore, the slope of the tangent line is $3.$

## q-48515 — original

If a curve $C$ is given by $y=(3x-2)\operatorname{ln}⁡x,$ calculate the slope of the tangent line to the curve at the point where $x=1.$

We differentiate using the product rule. Let $u(x)=3x-2$ and $v(x)=\operatorname{ln}⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=3,\,\frac{\text{d}v}{\text{d}x}=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & =(3x-2)\cdot \frac{1}{x}+(\operatorname{ln}⁡x)\cdot 3 \\  & =\frac{3x-2}{x}+3\operatorname{ln}⁡x.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{3x-2}{x}+3\operatorname{ln}⁡x)|}_{x=1} \\  & =\frac{3(1)-2}{1}+3\operatorname{ln}⁡1 \\  & =1.\end{aligned}
$$

Therefore, the slope of the tangent line is $1.$


Original banks: [[{":answer/id": "4d41e3a6-5106-5f1f-89a7-bdf0659fd667", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "\\operatorname{ln}⁡3", ":db/id": 17592186327605}, {":answer/id": "5722ae40-633d-5817-9b2f-fd696d396624", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "1", ":db/id": 17592186327690}, {":answer/id": "7d059a2c-54e1-581a-9631-274cba73cd9c", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "1-\\operatorname{ln}⁡2", ":db/id": 17592186328010}, {":answer/id": "e54916ae-cb46-54d5-9769-ffc8af47b71e", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "5+2\\operatorname{ln}⁡5", ":db/id": 17592186328941}, {":answer/id": "ef1b3eab-bf60-5779-ac14-8316a78be3d4", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-4", ":db/id": 17592186329022}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(3 x - 2)\cdot (\ln{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=1.$

- $\ln{\left(3 \right)}$
- $1 - \ln{\left(2 \right)}$
- $1$
- $\ln{\left(25 \right)} + 5$
- $-4$

We differentiate using the product rule. Let $u(x)=3 x - 2$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=3,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x - 2)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (3) \\ &=\frac{3 x - 2}{x}+(3)\cdot (\ln{\left(x \right)}).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=1} &=\left.\frac{3 x - 2}{x}+(3)\cdot (\ln{\left(x \right)})\right|_{x=1} \\ &=\frac{3 (1) - 2}{(1)}+(3)\cdot (\ln{\left((1) \right)}) \\ &=1.\end{aligned}
$$

Therefore, the slope of the tangent line is $1.$

## q-48516 — original

If a curve $C$ is given by $y={e}^{x}sin⁡x,$ calculate the slope of the tangent line to the curve at the point where $x=\pi .$

We differentiate using the product rule. Let $u(x)={e}^{x}$ and $v(x)=sin⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}={e}^{x},\,\frac{\text{d}v}{\text{d}x}=cos⁡x.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & ={e}^{x}\cdot cos⁡x+(sin⁡x)\cdot {e}^{x} \\  & ={e}^{x}(cos⁡x+sin⁡x).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi $ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=\pi } & ={{e}^{x}(cos⁡x+sin⁡x)|}_{x=\pi } \\  & ={e}^{\pi }(-1+0) \\  & =-{e}^{\pi }.\end{aligned}
$$

Therefore, the slope of the tangent line is $-{e}^{\pi }.$


Original banks: [[{":answer/id": "02bc770f-35b5-51f7-ac23-0dd7e7626849", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "0", ":db/id": 17592186326966}, {":answer/id": "a57078c9-1989-5bc2-8b84-47cb7c7b7fce", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "{e}^{\\pi }", ":db/id": 17592186328362}, {":answer/id": "acccd38a-7649-5753-9632-b00f2c05b4e5", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-{e}^{\\pi }", ":db/id": 17592186328433}, {":answer/id": "bce8eacc-997c-5af0-a8a5-5af0dda6e688", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "\\pi {e}^{\\pi }", ":db/id": 17592186328578}, {":answer/id": "d019d383-2037-503a-8480-3e5bdb84df98", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-\\pi {e}^{\\pi }", ":db/id": 17592186328764}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(e^{x})\cdot (\sin{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

- $0$
- $- e^{\pi}$
- $e^{\pi}$
- $\pi e^{\pi}$
- $- \pi e^{\pi}$

We differentiate using the product rule. Let $u(x)=e^{x}$ and $v(x)=\sin{\left(x \right)}.$ Then, we have

$$
u'(x)=e^{x},\quad v'(x)=\cos{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(e^{x})\cdot (\cos{\left(x \right)})+(\sin{\left(x \right)})\cdot (e^{x}) \\ &=e^{x}(\cos x+\sin x).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=\left.e^{x}(\cos x+\sin x)\right|_{x=\pi} \\ &=e^{\pi}(-1+0) \\ &=- e^{\pi}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- e^{\pi}.$

## q-48517 — original

If a curve $C$ is given by $y=({x}^{3}-1){e}^{x},$ calculate the slope of the tangent line to the curve at the point where $x=2.$

We differentiate using the product rule. Let $u(x)={x}^{3}-1$ and $v(x)={e}^{x}.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2},\,\frac{\text{d}v}{\text{d}x}={e}^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & =({x}^{3}-1)\cdot {e}^{x}+{e}^{x}\cdot (3{x}^{2}) \\  & ={e}^{x}({x}^{3}+3{x}^{2}-1).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2$ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={{e}^{x}({x}^{3}+3{x}^{2}-1)|}_{x=2} \\  & ={e}^{2}({2}^{3}+3(2)^{2}-1) \\  & =19{e}^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $19{e}^{2}.$


Original banks: [[{":answer/id": "122dcace-6bca-59bb-b96f-a96026e9a833", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "3e+5", ":db/id": 17592186327088}, {":answer/id": "29771cef-6628-575d-b6d2-039fa89b2a35", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "{e}^{2}+2", ":db/id": 17592186327286}, {":answer/id": "3101f4e9-df22-5461-be7e-f6674a765dce", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "{e}^{2}-1", ":db/id": 17592186327368}, {":answer/id": "c3e4fd4c-0122-574c-8317-faf21984d650", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "19{e}^{2}", ":db/id": 17592186328648}, {":answer/id": "e154d586-179b-57cc-acf3-bc95bc04c67c", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "4e", ":db/id": 17592186328905}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(x^{3} - 1)\cdot (e^{x}),$ calculate the slope of the tangent line to the curve at the point where $x=2.$

- $5 + 3 e$
- $-1 + e^{2}$
- $2 + e^{2}$
- $19 e^{2}$
- $4 e$

We differentiate using the product rule. Let $u(x)=x^{3} - 1$ and $v(x)=e^{x}.$ Then, we have

$$
u'(x)=3 x^{2},\quad v'(x)=e^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x^{3} - 1)\cdot (e^{x})+(e^{x})\cdot (3 x^{2}) \\ &=e^{x}(x^{3} + 3 x^{2} - 1).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2} &=\left.e^{x}(x^{3} + 3 x^{2} - 1)\right|_{x=2} \\ &=e^{(2)}((2)^{3} + 3 (2)^{2} - 1) \\ &=19 e^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $19 e^{2}.$

## q-48993 — original

If a curve $C$ is given by $y=x\operatorname{ln}⁡x,$ calculate the slope of the tangent line to the curve at the point where $x=e.$

We differentiate using the product rule. Let $u(x)=x$ and $v(x)=\operatorname{ln}⁡x.$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=1,\,\frac{\text{d}v}{\text{d}x}=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u\frac{\text{d}v}{\text{d}x}+v\frac{\text{d}u}{\text{d}x} \\  & =x\cdot \frac{1}{x}+(\operatorname{ln}⁡x)\cdot 1 \\  & =1+\operatorname{ln}⁡x.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=e} & =1+\operatorname{ln}⁡x \\  & =1+\operatorname{ln}⁡e \\  & =2.\end{aligned}
$$

Therefore, the slope of the tangent line is $2.$


Original banks: [[{":answer/id": "0fb89b95-0bba-5b10-8fe3-527b548e1601", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "2", ":db/id": 17592186327074}, {":answer/id": "8a5aa1e3-21ee-5889-8055-e0735761bea1", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "e", ":db/id": 17592186328124}, {":answer/id": "c4cf7b66-0f01-5eca-acc9-cb3a3d67bb13", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-e", ":db/id": 17592186328659}, {":answer/id": "d10f42e2-911f-5fb9-b0b0-c03a2475a986", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-2", ":db/id": 17592186328770}, {":answer/id": "e360ba04-1df2-5392-a2fb-baf0e0e1b838", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "0", ":db/id": 17592186328927}]]

### Generated original-parameter normalized replay

If a curve $C$ is given by $y=(x)\cdot (\ln{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=e.$

- $2$
- $- e$
- $e$
- $-2$
- $0$

We differentiate using the product rule. Let $u(x)=x$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (1) \\ &=1+(1)\cdot (\ln{\left(x \right)}).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=\left.1+(1)\cdot (\ln{\left(x \right)})\right|_{x=e} \\ &=1+1\ln(e) \\ &=2.\end{aligned}
$$

Therefore, the slope of the tangent line is $2.$

## Generated variant: q-48391 / easy

If a curve $C$ is given by $y=(3 e^{x})\cdot (x + 1)$, calculate the slope of the tangent line to the curve at the point where $x=0$.

- $3 e$
- $6$
- $0$
- $3$
- $\sqrt{3} e$

We differentiate using the product rule. Let $u(x)=3 e^{x}$ and $v(x)=x + 1.$ Then, we have

$$
u'(x)=3 e^{x},\quad v'(x)=1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 e^{x})\cdot (1)+(x + 1)\cdot (3 e^{x}) \\ &=3 x e^{x} + 6 e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=3 (0) e^{(0)} + 6 e^{(0)} \\ &=(3)\cdot (1)+(1)\cdot (3) \\ &=6.\end{aligned}
$$

Therefore, the slope of the tangent line is $6.$

## Generated variant: q-48901 / moderate

If a curve $C$ is given by $y=(4 x^{3})\cdot (\sin{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=\frac{\pi}{2}$.

- $3 \pi^{2}$
- $- 3 \pi^{2}$
- $0$
- $\frac{3 \pi^{2}}{2}$
- $- \frac{3 \pi^{2}}{2}$

We differentiate using the product rule. Let $u(x)=4 x^{3}$ and $v(x)=\sin{\left(x \right)}.$ Then, we have

$$
u'(x)=12 x^{2},\quad v'(x)=\cos{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(4 x^{3})\cdot (\cos{\left(x \right)})+(\sin{\left(x \right)})\cdot (12 x^{2}) \\ &=4 x^{3} \cos{\left(x \right)} + 12 x^{2} \sin{\left(x \right)}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{2}} &=4 (\frac{\pi}{2})^{3} \cos{\left((\frac{\pi}{2}) \right)} + 12 (\frac{\pi}{2})^{2} \sin{\left((\frac{\pi}{2}) \right)} \\ &=(\frac{\pi^{3}}{2})\cdot (0)+(1)\cdot (3 \pi^{2}) \\ &=3 \pi^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $3 \pi^{2}.$

## Generated variant: q-31226 / moderate

If a curve $C$ is given by $y=(2 x^{2})\cdot (\tan{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

Slope $=$ {{field-1}}

- $2 \pi^{2}$

We differentiate using the product rule. Let $u(x)=2 x^{2}$ and $v(x)=\tan{\left(x \right)}.$ Then, we have

$$
u'(x)=4 x,\quad v'(x)=\tan^{2}{\left(x \right)} + 1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(2 x^{2})\cdot (\tan^{2}{\left(x \right)} + 1)+(\tan{\left(x \right)})\cdot (4 x) \\ &=2 x^{2}\sec^{2}x+4 x\tan x.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=\left.2 x^{2}\sec^{2}x+4 x\tan x\right|_{x=\pi} \\ &=2 (\pi)^{2}\sec^{2}(\pi)+4 (\pi)\tan (\pi) \\ &=(2 \pi^{2})\cdot (1)+(0)\cdot (4 \pi) \\ &=2 \pi^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $2 \pi^{2}.$

## Generated variant: q-319825 / moderate

If a curve $C$ is given by $y=(2 x - 1)\cdot (\ln{\left(2 x + 1 \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=0$ is{{field-1}}.

- $-2$

We differentiate using the product rule. Let $u(x)=2 x - 1$ and $v(x)=\ln{\left(2 x + 1 \right)}.$ Then, we have

$$
u'(x)=2,\quad v'(x)=\frac{2}{2 x + 1}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(2 x - 1)\cdot (\frac{2}{2 x + 1})+(\ln{\left(2 x + 1 \right)})\cdot (2) \\ &=\frac{2(2 x - 1)}{2 x + 1}+(2)\cdot (\ln{\left(2 x + 1 \right)}).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=\frac{2(2 (0) - 1)}{2 (0) + 1}+(2)\cdot (\ln{\left(2 (0) + 1 \right)}) \\ &=(-2)+2\ln(1) \\ &=-2.\end{aligned}
$$

Therefore, the slope of the tangent line is $-2.$

## Generated variant: q-167326 / moderate

Given $f(x)=2 e^{x}$ and $h(x)=- 4 \sin{\left(x \right)}$, if a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $8 e^{\pi}$

We differentiate using the product rule. Recall that $f(x)=2 e^{x}$ and $h(x)=- 4 \sin{\left(x \right)}.$ Then,

$$
\begin{aligned}\frac{\mathrm df}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(2 e^{x})=2 e^{x} \\ \frac{\mathrm dh}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(- 4 \sin{\left(x \right)})=- 4 \cos{\left(x \right)}.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=fh'(x)+hf'(x) \\ &=(2 e^{x})\cdot (- 4 \cos{\left(x \right)})+(- 4 \sin{\left(x \right)})\cdot (2 e^{x}) \\ &=- 8 e^{x}(\cos x+\sin x).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=- 8 e^{(\pi)}(\cos (\pi)+\sin (\pi)) \\ &=- 8 e^{\pi}(-1+0) \\ &=8 e^{\pi}.\end{aligned}
$$

Therefore, the slope of the tangent line is $8 e^{\pi}.$

## Generated variant: q-167780 / moderate

Given $f(x)=2 e^{x}$ and $h(x)=- 4 \sin{\left(x \right)}$, if a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $8 e^{\pi}$

We differentiate using the product rule. Recall that $f(x)=2 e^{x}$ and $h(x)=- 4 \sin{\left(x \right)}.$ Then,

$$
\begin{aligned}\frac{\mathrm df}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(2 e^{x})=2 e^{x} \\ \frac{\mathrm dh}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(- 4 \sin{\left(x \right)})=- 4 \cos{\left(x \right)}.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=fh'(x)+hf'(x) \\ &=(2 e^{x})\cdot (- 4 \cos{\left(x \right)})+(- 4 \sin{\left(x \right)})\cdot (2 e^{x}) \\ &=- 8 e^{x}(\cos x+\sin x).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=- 8 e^{(\pi)}(\cos (\pi)+\sin (\pi)) \\ &=- 8 e^{\pi}(-1+0) \\ &=8 e^{\pi}.\end{aligned}
$$

Therefore, the slope of the tangent line is $8 e^{\pi}.$

## Generated variant: q-319806 / moderate

If a curve $C$ is given by $y=(2 x + 2)\cdot (\cos{\left(x \right)}),$ then the slope of the tangent line to the curve at the point where $x=\frac{\pi}{2}$ is{{field-1}}.

- $- \pi - 2$

We differentiate using the product rule. Let $u(x)=2 x + 2$ and $v(x)=\cos{\left(x \right)}.$ Then, we have

$$
u'(x)=2,\quad v'(x)=- \sin{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(2 x + 2)\cdot (- \sin{\left(x \right)})+(\cos{\left(x \right)})\cdot (2) \\ &=-(2 x + 2)\sin x+2\cos x.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{2}} &=-(2 (\frac{\pi}{2}) + 2)\sin (\frac{\pi}{2})+2\cos (\frac{\pi}{2}) \\ &=(2 + \pi)\cdot (-1)+(0)\cdot (2) \\ &=- \pi - 2.\end{aligned}
$$

Therefore, the slope of the tangent line is $- \pi - 2.$

## Generated variant: q-319829 / moderate

If a curve $C$ is given by $y=(2 x - 1)\cdot (\ln{\left(4 x - 3 \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=1$ is{{field-1}}.

- $4$

We differentiate using the product rule. Let $u(x)=2 x - 1$ and $v(x)=\ln{\left(4 x - 3 \right)}.$ Then, we have

$$
u'(x)=2,\quad v'(x)=\frac{4}{4 x - 3}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(2 x - 1)\cdot (\frac{4}{4 x - 3})+(\ln{\left(4 x - 3 \right)})\cdot (2).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=1} &=\frac{4(2 (1) - 1)}{4 (1) - 3}+(2)\cdot (\ln{\left(4 (1) - 3 \right)}) \\ &=(4)+2\ln(1)=4.\end{aligned}
$$

Therefore, the slope of the tangent line is $4.$

## Generated variant: q-319842 / moderate

If a curve $C$ is given by $y=(2 x^{2} - 4 x + 7)\cdot (e^{x}),$ calculate the slope of the tangent line to the curve at the point where $x=0$ is{{field-1}}.

- $3$

We differentiate using the product rule. Let $u(x)=2 x^{2} - 4 x + 7$ and $v(x)=e^{x}.$ Then, we have

$$
u'(x)=4 x - 4,\quad v'(x)=e^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(2 x^{2} - 4 x + 7)\cdot (e^{x})+(e^{x})\cdot (4 x - 4) \\ &=e^{x}(2 x^{2} + 3).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=\left.e^{x}(2 x^{2} + 3)\right|_{x=0} \\ &=1\cdot (0+3)=3.\end{aligned}
$$

Therefore, the slope of the tangent line is $3.$

## Generated variant: q-48515 / moderate

If a curve $C$ is given by $y=(4 x - 2)\cdot (\ln{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=1.$

- $-6$
- $2$
- $2 \ln{\left(6 \right)} + 6$
- $\ln{\left(4 \right)}$
- $2 - \ln{\left(2 \right)}$

We differentiate using the product rule. Let $u(x)=4 x - 2$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=4,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(4 x - 2)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (4) \\ &=\frac{4 x - 2}{x}+(4)\cdot (\ln{\left(x \right)}).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=1} &=\left.\frac{4 x - 2}{x}+(4)\cdot (\ln{\left(x \right)})\right|_{x=1} \\ &=\frac{4 (1) - 2}{(1)}+(4)\cdot (\ln{\left((1) \right)}) \\ &=2.\end{aligned}
$$

Therefore, the slope of the tangent line is $2.$

## Generated variant: q-48516 / moderate

If a curve $C$ is given by $y=(2 e^{x})\cdot (\sin{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

- $- 2 \pi e^{\pi}$
- $2 e^{\pi}$
- $2 \pi e^{\pi}$
- $0$
- $- 2 e^{\pi}$

We differentiate using the product rule. Let $u(x)=2 e^{x}$ and $v(x)=\sin{\left(x \right)}.$ Then, we have

$$
u'(x)=2 e^{x},\quad v'(x)=\cos{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(2 e^{x})\cdot (\cos{\left(x \right)})+(\sin{\left(x \right)})\cdot (2 e^{x}) \\ &=2 e^{x}(\cos x+\sin x).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=\left.2 e^{x}(\cos x+\sin x)\right|_{x=\pi} \\ &=2 e^{\pi}(-1+0) \\ &=- 2 e^{\pi}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- 2 e^{\pi}.$

## Generated variant: q-48517 / moderate

If a curve $C$ is given by $y=(x^{3} - 2)\cdot (e^{x}),$ calculate the slope of the tangent line to the curve at the point where $x=2.$

- $4 e$
- $2 + e^{2}$
- $18 e^{2}$
- $4 + 3 e$
- $-2 + e^{2}$

We differentiate using the product rule. Let $u(x)=x^{3} - 2$ and $v(x)=e^{x}.$ Then, we have

$$
u'(x)=3 x^{2},\quad v'(x)=e^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x^{3} - 2)\cdot (e^{x})+(e^{x})\cdot (3 x^{2}) \\ &=e^{x}(x^{3} + 3 x^{2} - 2).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2} &=\left.e^{x}(x^{3} + 3 x^{2} - 2)\right|_{x=2} \\ &=e^{(2)}((2)^{3} + 3 (2)^{2} - 2) \\ &=18 e^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $18 e^{2}.$

## Generated variant: q-48993 / moderate

If a curve $C$ is given by $y=(2 x)\cdot (\ln{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=e.$

- $0$
- $2 e$
- $-4$
- $4$
- $- 2 e$

We differentiate using the product rule. Let $u(x)=2 x$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=2,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(2 x)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (2) \\ &=2+(2)\cdot (\ln{\left(x \right)}).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=\left.2+(2)\cdot (\ln{\left(x \right)})\right|_{x=e} \\ &=2+2\ln(e) \\ &=4.\end{aligned}
$$

Therefore, the slope of the tangent line is $4.$

## Generated variant: q-48391 / easy

If a curve $C$ is given by $y=(3 e^{x})\cdot (x + 3)$, calculate the slope of the tangent line to the curve at the point where $x=0$.

- $12$
- $9$
- $-12$
- $4$
- $2$

We differentiate using the product rule. Let $u(x)=3 e^{x}$ and $v(x)=x + 3.$ Then, we have

$$
u'(x)=3 e^{x},\quad v'(x)=1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 e^{x})\cdot (1)+(x + 3)\cdot (3 e^{x}) \\ &=3 \left(x + 4\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=(3 e^{(0)})\cdot (1)+((0) + 3)\cdot (3 e^{(0)}) \\ &=(3)\cdot (1)+(3)\cdot (3) \\ &=12.\end{aligned}
$$

Therefore, the slope of the tangent line is $12.$

## Generated variant: q-48391 / easy

If a curve $C$ is given by $y=(- 2 e^{x})\cdot (x + 3)$, calculate the slope of the tangent line to the curve at the point where $x=0$.

- $-3$
- $-6$
- $8$
- $-1$
- $-8$

We differentiate using the product rule. Let $u(x)=- 2 e^{x}$ and $v(x)=x + 3.$ Then, we have

$$
u'(x)=- 2 e^{x},\quad v'(x)=1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 e^{x})\cdot (1)+(x + 3)\cdot (- 2 e^{x}) \\ &=- 2 \left(x + 4\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=(- 2 e^{(0)})\cdot (1)+((0) + 3)\cdot (- 2 e^{(0)}) \\ &=(-2)\cdot (1)+(3)\cdot (-2) \\ &=-8.\end{aligned}
$$

Therefore, the slope of the tangent line is $-8.$

## Generated variant: q-48901 / moderate

If a curve $C$ is given by $y=(3 x^{3})\cdot (\sin{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=\frac{3 \pi}{2}$.

- $- \frac{81 \pi^{2}}{4}$
- $- \frac{81 \pi^{3}}{8}$
- $\frac{81 \pi^{2}}{4}$
- $- \frac{243 \pi^{3}}{8}$
- $- \frac{27 \pi^{2}}{4}$

We differentiate using the product rule. Let $u(x)=3 x^{3}$ and $v(x)=\sin{\left(x \right)}.$ Then, we have

$$
u'(x)=9 x^{2},\quad v'(x)=\cos{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x^{3})\cdot (\cos{\left(x \right)})+(\sin{\left(x \right)})\cdot (9 x^{2}) \\ &=3 x^{2} \left(x \cos{\left(x \right)} + 3 \sin{\left(x \right)}\right).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{3 \pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{3 \pi}{2}} &=(3 (\frac{3 \pi}{2})^{3})\cdot (\cos{\left((\frac{3 \pi}{2}) \right)})+(\sin{\left((\frac{3 \pi}{2}) \right)})\cdot (9 (\frac{3 \pi}{2})^{2}) \\ &=(\frac{81 \pi^{3}}{8})\cdot (0)+(-1)\cdot (\frac{81 \pi^{2}}{4}) \\ &=- \frac{81 \pi^{2}}{4}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- \frac{81 \pi^{2}}{4}.$

## Generated variant: q-48901 / moderate

If a curve $C$ is given by $y=(- 2 x^{3})\cdot (\sin{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=\frac{3 \pi}{2}$.

- $\frac{9 \pi^{2}}{2}$
- $\frac{27 \pi^{3}}{4}$
- $- \frac{27 \pi^{2}}{2}$
- $\frac{81 \pi^{3}}{4}$
- $\frac{27 \pi^{2}}{2}$

We differentiate using the product rule. Let $u(x)=- 2 x^{3}$ and $v(x)=\sin{\left(x \right)}.$ Then, we have

$$
u'(x)=- 6 x^{2},\quad v'(x)=\cos{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 x^{3})\cdot (\cos{\left(x \right)})+(\sin{\left(x \right)})\cdot (- 6 x^{2}) \\ &=- 2 x^{2} \left(x \cos{\left(x \right)} + 3 \sin{\left(x \right)}\right).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{3 \pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{3 \pi}{2}} &=(- 2 (\frac{3 \pi}{2})^{3})\cdot (\cos{\left((\frac{3 \pi}{2}) \right)})+(\sin{\left((\frac{3 \pi}{2}) \right)})\cdot (- 6 (\frac{3 \pi}{2})^{2}) \\ &=(- \frac{27 \pi^{3}}{4})\cdot (0)+(-1)\cdot (- \frac{27 \pi^{2}}{2}) \\ &=\frac{27 \pi^{2}}{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $\frac{27 \pi^{2}}{2}.$

## Generated variant: q-31226 / moderate

If a curve $C$ is given by $y=(3 x^{2})\cdot (\tan{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=2 \pi.$

Slope $=$ {{field-1}}

- $12 \pi^{2}$

We differentiate using the product rule. Let $u(x)=3 x^{2}$ and $v(x)=\tan{\left(x \right)}.$ Then, we have

$$
u'(x)=6 x,\quad v'(x)=\tan^{2}{\left(x \right)} + 1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x^{2})\cdot (\tan^{2}{\left(x \right)} + 1)+(\tan{\left(x \right)})\cdot (6 x) \\ &=3 x \left(x \tan^{2}{\left(x \right)} + x + 2 \tan{\left(x \right)}\right).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2 \pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2 \pi} &=(3 (2 \pi)^{2})\cdot (\tan^{2}{\left((2 \pi) \right)} + 1)+(\tan{\left((2 \pi) \right)})\cdot (6 (2 \pi)) \\ &=(12 \pi^{2})\cdot (1)+(0)\cdot (12 \pi) \\ &=12 \pi^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $12 \pi^{2}.$

## Generated variant: q-31226 / moderate

If a curve $C$ is given by $y=(- 2 x^{2})\cdot (\tan{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=2 \pi.$

Slope $=$ {{field-1}}

- $- 8 \pi^{2}$

We differentiate using the product rule. Let $u(x)=- 2 x^{2}$ and $v(x)=\tan{\left(x \right)}.$ Then, we have

$$
u'(x)=- 4 x,\quad v'(x)=\tan^{2}{\left(x \right)} + 1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 x^{2})\cdot (\tan^{2}{\left(x \right)} + 1)+(\tan{\left(x \right)})\cdot (- 4 x) \\ &=- 2 x \left(x \tan^{2}{\left(x \right)} + x + 2 \tan{\left(x \right)}\right).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2 \pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2 \pi} &=(- 2 (2 \pi)^{2})\cdot (\tan^{2}{\left((2 \pi) \right)} + 1)+(\tan{\left((2 \pi) \right)})\cdot (- 4 (2 \pi)) \\ &=(- 8 \pi^{2})\cdot (1)+(0)\cdot (- 8 \pi) \\ &=- 8 \pi^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- 8 \pi^{2}.$

## Generated variant: q-319825 / moderate

If a curve $C$ is given by $y=(x - 3)\cdot (\ln{\left(3 x - 2 \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=1$ is{{field-1}}.

- $-6$

We differentiate using the product rule. Let $u(x)=x - 3$ and $v(x)=\ln{\left(3 x - 2 \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=\frac{3}{3 x - 2}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x - 3)\cdot (\frac{3}{3 x - 2})+(\ln{\left(3 x - 2 \right)})\cdot (1) \\ &=\frac{3 x \ln{\left(3 x - 2 \right)} + 3 x - 2 \ln{\left(3 x - 2 \right)} - 9}{3 x - 2}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=1} &=((1) - 3)\cdot (\frac{3}{3 (1) - 2})+(\ln{\left(3 (1) - 2 \right)})\cdot (1) \\ &=(-2)\cdot (3)+(0)\cdot (1) \\ &=-6.\end{aligned}
$$

Therefore, the slope of the tangent line is $-6.$

## Generated variant: q-319825 / moderate

If a curve $C$ is given by $y=(x - 3)\cdot (\ln{\left(3 x - 5 \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=2$ is{{field-1}}.

- $-3$

We differentiate using the product rule. Let $u(x)=x - 3$ and $v(x)=\ln{\left(3 x - 5 \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=\frac{3}{3 x - 5}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x - 3)\cdot (\frac{3}{3 x - 5})+(\ln{\left(3 x - 5 \right)})\cdot (1) \\ &=\frac{3 x \ln{\left(3 x - 5 \right)} + 3 x - 5 \ln{\left(3 x - 5 \right)} - 9}{3 x - 5}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2} &=((2) - 3)\cdot (\frac{3}{3 (2) - 5})+(\ln{\left(3 (2) - 5 \right)})\cdot (1) \\ &=(-1)\cdot (3)+(0)\cdot (1) \\ &=-3.\end{aligned}
$$

Therefore, the slope of the tangent line is $-3.$

## Generated variant: q-167326 / moderate

Given $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 6 \sin{\left(x \right)}$, if a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\frac{\pi}{2}.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $- 3 e^{\frac{\pi}{2}}$

We differentiate using the product rule. Recall that $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 6 \sin{\left(x \right)}.$ Then,

$$
\begin{aligned}\frac{\mathrm df}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(\frac{e^{x}}{2})=\frac{e^{x}}{2} \\ \frac{\mathrm dh}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(- 6 \sin{\left(x \right)})=- 6 \cos{\left(x \right)}.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=fh'(x)+hf'(x) \\ &=(\frac{e^{x}}{2})\cdot (- 6 \cos{\left(x \right)})+(- 6 \sin{\left(x \right)})\cdot (\frac{e^{x}}{2}) \\ &=- 3 \left(\sin{\left(x \right)} + \cos{\left(x \right)}\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{2}} &=(\frac{e^{(\frac{\pi}{2})}}{2})\cdot (- 6 \cos{\left((\frac{\pi}{2}) \right)})+(- 6 \sin{\left((\frac{\pi}{2}) \right)})\cdot (\frac{e^{(\frac{\pi}{2})}}{2}) \\ &=(\frac{e^{\frac{\pi}{2}}}{2})\cdot (0)+(-6)\cdot (\frac{e^{\frac{\pi}{2}}}{2}) \\ &=- 3 e^{\frac{\pi}{2}}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- 3 e^{\frac{\pi}{2}}.$

## Generated variant: q-167326 / moderate

Given $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 6 \sin{\left(x \right)}$, if a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\frac{\pi}{2}.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $- 3 e^{\frac{\pi}{2}}$

We differentiate using the product rule. Recall that $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 6 \sin{\left(x \right)}.$ Then,

$$
\begin{aligned}\frac{\mathrm df}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(\frac{e^{x}}{2})=\frac{e^{x}}{2} \\ \frac{\mathrm dh}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(- 6 \sin{\left(x \right)})=- 6 \cos{\left(x \right)}.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=fh'(x)+hf'(x) \\ &=(\frac{e^{x}}{2})\cdot (- 6 \cos{\left(x \right)})+(- 6 \sin{\left(x \right)})\cdot (\frac{e^{x}}{2}) \\ &=- 3 \left(\sin{\left(x \right)} + \cos{\left(x \right)}\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{2}} &=(\frac{e^{(\frac{\pi}{2})}}{2})\cdot (- 6 \cos{\left((\frac{\pi}{2}) \right)})+(- 6 \sin{\left((\frac{\pi}{2}) \right)})\cdot (\frac{e^{(\frac{\pi}{2})}}{2}) \\ &=(\frac{e^{\frac{\pi}{2}}}{2})\cdot (0)+(-6)\cdot (\frac{e^{\frac{\pi}{2}}}{2}) \\ &=- 3 e^{\frac{\pi}{2}}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- 3 e^{\frac{\pi}{2}}.$

## Generated variant: q-167780 / moderate

Given $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 6 \sin{\left(x \right)}$, if a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\frac{\pi}{2}.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $- 3 e^{\frac{\pi}{2}}$

We differentiate using the product rule. Recall that $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 6 \sin{\left(x \right)}.$ Then,

$$
\begin{aligned}\frac{\mathrm df}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(\frac{e^{x}}{2})=\frac{e^{x}}{2} \\ \frac{\mathrm dh}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(- 6 \sin{\left(x \right)})=- 6 \cos{\left(x \right)}.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=fh'(x)+hf'(x) \\ &=(\frac{e^{x}}{2})\cdot (- 6 \cos{\left(x \right)})+(- 6 \sin{\left(x \right)})\cdot (\frac{e^{x}}{2}) \\ &=- 3 \left(\sin{\left(x \right)} + \cos{\left(x \right)}\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{2}} &=(\frac{e^{(\frac{\pi}{2})}}{2})\cdot (- 6 \cos{\left((\frac{\pi}{2}) \right)})+(- 6 \sin{\left((\frac{\pi}{2}) \right)})\cdot (\frac{e^{(\frac{\pi}{2})}}{2}) \\ &=(\frac{e^{\frac{\pi}{2}}}{2})\cdot (0)+(-6)\cdot (\frac{e^{\frac{\pi}{2}}}{2}) \\ &=- 3 e^{\frac{\pi}{2}}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- 3 e^{\frac{\pi}{2}}.$

## Generated variant: q-167780 / moderate

Given $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 6 \sin{\left(x \right)}$, if a curve $C$ is defined by the equation $y=f(x)\cdot h(x),$ calculate the slope of the tangent line to the curve at the point where $x=\frac{\pi}{2}.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        Slope $\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

- $- 3 e^{\frac{\pi}{2}}$

We differentiate using the product rule. Recall that $f(x)=\frac{e^{x}}{2}$ and $h(x)=- 6 \sin{\left(x \right)}.$ Then,

$$
\begin{aligned}\frac{\mathrm df}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(\frac{e^{x}}{2})=\frac{e^{x}}{2} \\ \frac{\mathrm dh}{\mathrm dx} &=\frac{\mathrm d}{\mathrm dx}(- 6 \sin{\left(x \right)})=- 6 \cos{\left(x \right)}.\end{aligned}
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=fh'(x)+hf'(x) \\ &=(\frac{e^{x}}{2})\cdot (- 6 \cos{\left(x \right)})+(- 6 \sin{\left(x \right)})\cdot (\frac{e^{x}}{2}) \\ &=- 3 \left(\sin{\left(x \right)} + \cos{\left(x \right)}\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{2}} &=(\frac{e^{(\frac{\pi}{2})}}{2})\cdot (- 6 \cos{\left((\frac{\pi}{2}) \right)})+(- 6 \sin{\left((\frac{\pi}{2}) \right)})\cdot (\frac{e^{(\frac{\pi}{2})}}{2}) \\ &=(\frac{e^{\frac{\pi}{2}}}{2})\cdot (0)+(-6)\cdot (\frac{e^{\frac{\pi}{2}}}{2}) \\ &=- 3 e^{\frac{\pi}{2}}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- 3 e^{\frac{\pi}{2}}.$

## Generated variant: q-319806 / moderate

If a curve $C$ is given by $y=(x - 3)\cdot (\cos{\left(x \right)}),$ then the slope of the tangent line to the curve at the point where $x=\frac{3 \pi}{2}$ is{{field-1}}.

- $-3 + \frac{3 \pi}{2}$

We differentiate using the product rule. Let $u(x)=x - 3$ and $v(x)=\cos{\left(x \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=- \sin{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x - 3)\cdot (- \sin{\left(x \right)})+(\cos{\left(x \right)})\cdot (1) \\ &=- x \sin{\left(x \right)} + 3 \sin{\left(x \right)} + \cos{\left(x \right)}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{3 \pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{3 \pi}{2}} &=((\frac{3 \pi}{2}) - 3)\cdot (- \sin{\left((\frac{3 \pi}{2}) \right)})+(\cos{\left((\frac{3 \pi}{2}) \right)})\cdot (1) \\ &=(-3 + \frac{3 \pi}{2})\cdot (1)+(0)\cdot (1) \\ &=-3 + \frac{3 \pi}{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $-3 + \frac{3 \pi}{2}.$

## Generated variant: q-319806 / moderate

If a curve $C$ is given by $y=(x - 3)\cdot (\cos{\left(x \right)}),$ then the slope of the tangent line to the curve at the point where $x=\frac{3 \pi}{2}$ is{{field-1}}.

- $-3 + \frac{3 \pi}{2}$

We differentiate using the product rule. Let $u(x)=x - 3$ and $v(x)=\cos{\left(x \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=- \sin{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x - 3)\cdot (- \sin{\left(x \right)})+(\cos{\left(x \right)})\cdot (1) \\ &=- x \sin{\left(x \right)} + 3 \sin{\left(x \right)} + \cos{\left(x \right)}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{3 \pi}{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{3 \pi}{2}} &=((\frac{3 \pi}{2}) - 3)\cdot (- \sin{\left((\frac{3 \pi}{2}) \right)})+(\cos{\left((\frac{3 \pi}{2}) \right)})\cdot (1) \\ &=(-3 + \frac{3 \pi}{2})\cdot (1)+(0)\cdot (1) \\ &=-3 + \frac{3 \pi}{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $-3 + \frac{3 \pi}{2}.$

## Generated variant: q-319829 / moderate

If a curve $C$ is given by $y=(x - 3)\cdot (\ln{\left(3 x - 2 \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=1$ is{{field-1}}.

- $-6$

We differentiate using the product rule. Let $u(x)=x - 3$ and $v(x)=\ln{\left(3 x - 2 \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=\frac{3}{3 x - 2}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x - 3)\cdot (\frac{3}{3 x - 2})+(\ln{\left(3 x - 2 \right)})\cdot (1) \\ &=\frac{3 x \ln{\left(3 x - 2 \right)} + 3 x - 2 \ln{\left(3 x - 2 \right)} - 9}{3 x - 2}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=1} &=((1) - 3)\cdot (\frac{3}{3 (1) - 2})+(\ln{\left(3 (1) - 2 \right)})\cdot (1) \\ &=(-2)\cdot (3)+(0)\cdot (1) \\ &=-6.\end{aligned}
$$

Therefore, the slope of the tangent line is $-6.$

## Generated variant: q-319829 / moderate

If a curve $C$ is given by $y=(x - 3)\cdot (\ln{\left(3 x - 5 \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=2$ is{{field-1}}.

- $-3$

We differentiate using the product rule. Let $u(x)=x - 3$ and $v(x)=\ln{\left(3 x - 5 \right)}.$ Then, we have

$$
u'(x)=1,\quad v'(x)=\frac{3}{3 x - 5}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x - 3)\cdot (\frac{3}{3 x - 5})+(\ln{\left(3 x - 5 \right)})\cdot (1) \\ &=\frac{3 x \ln{\left(3 x - 5 \right)} + 3 x - 5 \ln{\left(3 x - 5 \right)} - 9}{3 x - 5}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2} &=((2) - 3)\cdot (\frac{3}{3 (2) - 5})+(\ln{\left(3 (2) - 5 \right)})\cdot (1) \\ &=(-1)\cdot (3)+(0)\cdot (1) \\ &=-3.\end{aligned}
$$

Therefore, the slope of the tangent line is $-3.$

## Generated variant: q-319842 / moderate

If a curve $C$ is given by $y=(x^{2} - 3 x + 5)\cdot (e^{x}),$ calculate the slope of the tangent line to the curve at the point where $x=1$ is{{field-1}}.

- $2 e$

We differentiate using the product rule. Let $u(x)=x^{2} - 3 x + 5$ and $v(x)=e^{x}.$ Then, we have

$$
u'(x)=2 x - 3,\quad v'(x)=e^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x^{2} - 3 x + 5)\cdot (e^{x})+(e^{x})\cdot (2 x - 3) \\ &=\left(x^{2} - x + 2\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=1$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=1} &=((1)^{2} - 3 (1) + 5)\cdot (e^{(1)})+(e^{(1)})\cdot (2 (1) - 3) \\ &=(3)\cdot (e)+(e)\cdot (-1) \\ &=2 e.\end{aligned}
$$

Therefore, the slope of the tangent line is $2 e.$

## Generated variant: q-319842 / moderate

If a curve $C$ is given by $y=(x^{2} - 3 x + 5)\cdot (e^{x}),$ calculate the slope of the tangent line to the curve at the point where $x=2$ is{{field-1}}.

- $4 e^{2}$

We differentiate using the product rule. Let $u(x)=x^{2} - 3 x + 5$ and $v(x)=e^{x}.$ Then, we have

$$
u'(x)=2 x - 3,\quad v'(x)=e^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(x^{2} - 3 x + 5)\cdot (e^{x})+(e^{x})\cdot (2 x - 3) \\ &=\left(x^{2} - x + 2\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2} &=((2)^{2} - 3 (2) + 5)\cdot (e^{(2)})+(e^{(2)})\cdot (2 (2) - 3) \\ &=(3)\cdot (e^{2})+(e^{2})\cdot (1) \\ &=4 e^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $4 e^{2}.$

## Generated variant: q-48515 / moderate

If a curve $C$ is given by $y=(3 x - 3)\cdot (\ln{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=e.$

- $6 - \frac{3}{e}$
- $-3 + 3 e$
- $-6 + \frac{3}{e}$
- $e^{-1} + 3$
- $3 - e^{-1}$

We differentiate using the product rule. Let $u(x)=3 x - 3$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=3,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x - 3)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (3) \\ &=\frac{3 \left(x \ln{\left(x \right)} + x - 1\right)}{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=(3 (e) - 3)\cdot (\frac{1}{(e)})+(\ln{\left((e) \right)})\cdot (3) \\ &=(-3 + 3 e)\cdot (e^{-1})+(1)\cdot (3) \\ &=6 - \frac{3}{e}.\end{aligned}
$$

Therefore, the slope of the tangent line is $6 - \frac{3}{e}.$

## Generated variant: q-48515 / moderate

If a curve $C$ is given by $y=(- 2 x - 3)\cdot (\ln{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=e.$

- $-2 - e^{-1}$
- $- 2 e - 3$
- $\frac{3}{e} + 4$
- $-2 + e^{-1}$
- $-4 - \frac{3}{e}$

We differentiate using the product rule. Let $u(x)=- 2 x - 3$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=-2,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 x - 3)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (-2) \\ &=- \frac{2 x \ln{\left(x \right)} + 2 x + 3}{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=(- 2 (e) - 3)\cdot (\frac{1}{(e)})+(\ln{\left((e) \right)})\cdot (-2) \\ &=(- 2 e - 3)\cdot (e^{-1})+(1)\cdot (-2) \\ &=-4 - \frac{3}{e}.\end{aligned}
$$

Therefore, the slope of the tangent line is $-4 - \frac{3}{e}.$

## Generated variant: q-48516 / moderate

If a curve $C$ is given by $y=(- 2 e^{x})\cdot (\sin{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

- $- 2 e^{\pi}$
- $2 e^{\pi}$
- $- 2 e^{\pi} - 1$
- $0$
- $1 - 2 e^{\pi}$

We differentiate using the product rule. Let $u(x)=- 2 e^{x}$ and $v(x)=\sin{\left(x \right)}.$ Then, we have

$$
u'(x)=- 2 e^{x},\quad v'(x)=\cos{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 e^{x})\cdot (\cos{\left(x \right)})+(\sin{\left(x \right)})\cdot (- 2 e^{x}) \\ &=- 2 \left(\sin{\left(x \right)} + \cos{\left(x \right)}\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=(- 2 e^{(\pi)})\cdot (\cos{\left((\pi) \right)})+(\sin{\left((\pi) \right)})\cdot (- 2 e^{(\pi)}) \\ &=(- 2 e^{\pi})\cdot (-1)+(0)\cdot (- 2 e^{\pi}) \\ &=2 e^{\pi}.\end{aligned}
$$

Therefore, the slope of the tangent line is $2 e^{\pi}.$

## Generated variant: q-48516 / moderate

If a curve $C$ is given by $y=(- 4 e^{x})\cdot (\sin{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=\pi.$

- $- 4 e^{\pi}$
- $1 - 4 e^{\pi}$
- $0$
- $4 e^{\pi}$
- $- 4 e^{\pi} - 1$

We differentiate using the product rule. Let $u(x)=- 4 e^{x}$ and $v(x)=\sin{\left(x \right)}.$ Then, we have

$$
u'(x)=- 4 e^{x},\quad v'(x)=\cos{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 4 e^{x})\cdot (\cos{\left(x \right)})+(\sin{\left(x \right)})\cdot (- 4 e^{x}) \\ &=- 4 \left(\sin{\left(x \right)} + \cos{\left(x \right)}\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\pi$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\pi} &=(- 4 e^{(\pi)})\cdot (\cos{\left((\pi) \right)})+(\sin{\left((\pi) \right)})\cdot (- 4 e^{(\pi)}) \\ &=(- 4 e^{\pi})\cdot (-1)+(0)\cdot (- 4 e^{\pi}) \\ &=4 e^{\pi}.\end{aligned}
$$

Therefore, the slope of the tangent line is $4 e^{\pi}.$

## Generated variant: q-48517 / moderate

If a curve $C$ is given by $y=(3 x^{3} - 3)\cdot (e^{x}),$ calculate the slope of the tangent line to the curve at the point where $x=2.$

- $57 e^{2}$
- $21 e^{2}$
- $- 57 e^{2}$
- $e^{2} + 36$
- $36 - e^{2}$

We differentiate using the product rule. Let $u(x)=3 x^{3} - 3$ and $v(x)=e^{x}.$ Then, we have

$$
u'(x)=9 x^{2},\quad v'(x)=e^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x^{3} - 3)\cdot (e^{x})+(e^{x})\cdot (9 x^{2}) \\ &=3 \left(x^{3} + 3 x^{2} - 1\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2} &=(3 (2)^{3} - 3)\cdot (e^{(2)})+(e^{(2)})\cdot (9 (2)^{2}) \\ &=(21)\cdot (e^{2})+(e^{2})\cdot (36) \\ &=57 e^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $57 e^{2}.$

## Generated variant: q-48517 / moderate

If a curve $C$ is given by $y=(- 2 x^{3} - 3)\cdot (e^{x}),$ calculate the slope of the tangent line to the curve at the point where $x=2.$

- $-24 - e^{2}$
- $- 19 e^{2}$
- $43 e^{2}$
- $-24 + e^{2}$
- $- 43 e^{2}$

We differentiate using the product rule. Let $u(x)=- 2 x^{3} - 3$ and $v(x)=e^{x}.$ Then, we have

$$
u'(x)=- 6 x^{2},\quad v'(x)=e^{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 x^{3} - 3)\cdot (e^{x})+(e^{x})\cdot (- 6 x^{2}) \\ &=- \left(2 x^{3} + 6 x^{2} + 3\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=2$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=2} &=(- 2 (2)^{3} - 3)\cdot (e^{(2)})+(e^{(2)})\cdot (- 6 (2)^{2}) \\ &=(-19)\cdot (e^{2})+(e^{2})\cdot (-24) \\ &=- 43 e^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- 43 e^{2}.$

## Generated variant: q-48993 / moderate

If a curve $C$ is given by $y=(3 x - 3)\cdot (\ln{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=e.$

- $6 - \frac{3}{e}$
- $-3 + 3 e$
- $-6 + \frac{3}{e}$
- $e^{-1} + 3$
- $3 - e^{-1}$

We differentiate using the product rule. Let $u(x)=3 x - 3$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=3,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x - 3)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (3) \\ &=\frac{3 \left(x \ln{\left(x \right)} + x - 1\right)}{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=(3 (e) - 3)\cdot (\frac{1}{(e)})+(\ln{\left((e) \right)})\cdot (3) \\ &=(-3 + 3 e)\cdot (e^{-1})+(1)\cdot (3) \\ &=6 - \frac{3}{e}.\end{aligned}
$$

Therefore, the slope of the tangent line is $6 - \frac{3}{e}.$

## Generated variant: q-48993 / moderate

If a curve $C$ is given by $y=(- 2 x - 3)\cdot (\ln{\left(x \right)}),$ calculate the slope of the tangent line to the curve at the point where $x=e.$

- $-2 - e^{-1}$
- $- 2 e - 3$
- $\frac{3}{e} + 4$
- $-2 + e^{-1}$
- $-4 - \frac{3}{e}$

We differentiate using the product rule. Let $u(x)=- 2 x - 3$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=-2,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 x - 3)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (-2) \\ &=- \frac{2 x \ln{\left(x \right)} + 2 x + 3}{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=(- 2 (e) - 3)\cdot (\frac{1}{(e)})+(\ln{\left((e) \right)})\cdot (-2) \\ &=(- 2 e - 3)\cdot (e^{-1})+(1)\cdot (-2) \\ &=-4 - \frac{3}{e}.\end{aligned}
$$

Therefore, the slope of the tangent line is $-4 - \frac{3}{e}.$

## Generated variant: easy_exp_linear / easy

If a curve $C$ is given by $y=(3 e^{x})\cdot (x + 3)$, calculate the slope of the tangent line to the curve at the point where $x=0$.

Slope $=$ {{field-1}}

- $12$

We differentiate using the product rule. Let $u(x)=3 e^{x}$ and $v(x)=x + 3.$ Then, we have

$$
u'(x)=3 e^{x},\quad v'(x)=1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 e^{x})\cdot (1)+(x + 3)\cdot (3 e^{x}) \\ &=3 \left(x + 4\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=(3 e^{(0)})\cdot (1)+((0) + 3)\cdot (3 e^{(0)}) \\ &=(3)\cdot (1)+(3)\cdot (3) \\ &=12.\end{aligned}
$$

Therefore, the slope of the tangent line is $12.$

## Generated variant: easy_exp_linear / easy

If a curve $C$ is given by $y=(- 2 e^{x})\cdot (x + 3)$, calculate the slope of the tangent line to the curve at the point where $x=0$.

Slope $=$ {{field-1}}

- $-8$

We differentiate using the product rule. Let $u(x)=- 2 e^{x}$ and $v(x)=x + 3.$ Then, we have

$$
u'(x)=- 2 e^{x},\quad v'(x)=1.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 e^{x})\cdot (1)+(x + 3)\cdot (- 2 e^{x}) \\ &=- 2 \left(x + 4\right) e^{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=0$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=0} &=(- 2 e^{(0)})\cdot (1)+((0) + 3)\cdot (- 2 e^{(0)}) \\ &=(-2)\cdot (1)+(3)\cdot (-2) \\ &=-8.\end{aligned}
$$

Therefore, the slope of the tangent line is $-8.$

## Generated variant: easy_linear_log / easy

If a curve $C$ is given by $y=(3 x)\cdot (\ln{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=e$.

Slope $=$ {{field-1}}

- $6$

We differentiate using the product rule. Let $u(x)=3 x$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=3,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (3) \\ &=3 \left(\ln{\left(x \right)} + 1\right).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=(3 (e))\cdot (\frac{1}{(e)})+(\ln{\left((e) \right)})\cdot (3) \\ &=(3 e)\cdot (e^{-1})+(1)\cdot (3) \\ &=6.\end{aligned}
$$

Therefore, the slope of the tangent line is $6.$

## Generated variant: easy_linear_log / easy

If a curve $C$ is given by $y=(- 2 x)\cdot (\ln{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=e$.

Slope $=$ {{field-1}}

- $-4$

We differentiate using the product rule. Let $u(x)=- 2 x$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=-2,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 x)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (-2) \\ &=- 2 \left(\ln{\left(x \right)} + 1\right).\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=(- 2 (e))\cdot (\frac{1}{(e)})+(\ln{\left((e) \right)})\cdot (-2) \\ &=(- 2 e)\cdot (e^{-1})+(1)\cdot (-2) \\ &=-4.\end{aligned}
$$

Therefore, the slope of the tangent line is $-4.$

## Generated variant: hard_poly_trig / hard

If a curve $C$ is given by $y=(3 x^{2} - 3 x + 1)\cdot (\cos{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=\frac{7 \pi}{4}$.

Slope $=$ {{field-1}}

- $\frac{\sqrt{2} \left(-32 + 84 \pi + 147 \pi^{2}\right)}{32}$

We differentiate using the product rule. Let $u(x)=3 x^{2} - 3 x + 1$ and $v(x)=\cos{\left(x \right)}.$ Then, we have

$$
u'(x)=6 x - 3,\quad v'(x)=- \sin{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x^{2} - 3 x + 1)\cdot (- \sin{\left(x \right)})+(\cos{\left(x \right)})\cdot (6 x - 3) \\ &=- 3 x^{2} \sin{\left(x \right)} + 3 x \sin{\left(x \right)} + 6 x \cos{\left(x \right)} - \sin{\left(x \right)} - 3 \cos{\left(x \right)}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{7 \pi}{4}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{7 \pi}{4}} &=(3 (\frac{7 \pi}{4})^{2} - 3 (\frac{7 \pi}{4}) + 1)\cdot (- \sin{\left((\frac{7 \pi}{4}) \right)})+(\cos{\left((\frac{7 \pi}{4}) \right)})\cdot (6 (\frac{7 \pi}{4}) - 3) \\ &=(- \frac{21 \pi}{4} + 1 + \frac{147 \pi^{2}}{16})\cdot (\frac{\sqrt{2}}{2})+(\frac{\sqrt{2}}{2})\cdot (-3 + \frac{21 \pi}{2}) \\ &=\frac{\sqrt{2} \left(-32 + 84 \pi + 147 \pi^{2}\right)}{32}.\end{aligned}
$$

Therefore, the slope of the tangent line is $\frac{\sqrt{2} \left(-32 + 84 \pi + 147 \pi^{2}\right)}{32}.$

## Generated variant: hard_poly_trig / hard

If a curve $C$ is given by $y=(- 2 x^{2} - 3 x + 1)\cdot (\cos{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=\frac{\pi}{4}$.

Slope $=$ {{field-1}}

- $\frac{\sqrt{2} \left(-32 - 2 \pi + \pi^{2}\right)}{16}$

We differentiate using the product rule. Let $u(x)=- 2 x^{2} - 3 x + 1$ and $v(x)=\cos{\left(x \right)}.$ Then, we have

$$
u'(x)=- 4 x - 3,\quad v'(x)=- \sin{\left(x \right)}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 x^{2} - 3 x + 1)\cdot (- \sin{\left(x \right)})+(\cos{\left(x \right)})\cdot (- 4 x - 3) \\ &=2 x^{2} \sin{\left(x \right)} + 3 x \sin{\left(x \right)} - 4 x \cos{\left(x \right)} - \sin{\left(x \right)} - 3 \cos{\left(x \right)}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=\frac{\pi}{4}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=\frac{\pi}{4}} &=(- 2 (\frac{\pi}{4})^{2} - 3 (\frac{\pi}{4}) + 1)\cdot (- \sin{\left((\frac{\pi}{4}) \right)})+(\cos{\left((\frac{\pi}{4}) \right)})\cdot (- 4 (\frac{\pi}{4}) - 3) \\ &=(- \frac{3 \pi}{4} - \frac{\pi^{2}}{8} + 1)\cdot (- \frac{\sqrt{2}}{2})+(\frac{\sqrt{2}}{2})\cdot (- \pi - 3) \\ &=\frac{\sqrt{2} \left(-32 - 2 \pi + \pi^{2}\right)}{16}.\end{aligned}
$$

Therefore, the slope of the tangent line is $\frac{\sqrt{2} \left(-32 - 2 \pi + \pi^{2}\right)}{16}.$

## Generated variant: hard_poly_log / hard

If a curve $C$ is given by $y=(3 x^{2} - 3 x + 1)\cdot (\ln{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=e^{2}$.

Slope $=$ {{field-1}}

- $-9 + e^{-2} + 15 e^{2}$

We differentiate using the product rule. Let $u(x)=3 x^{2} - 3 x + 1$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=6 x - 3,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(3 x^{2} - 3 x + 1)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (6 x - 3) \\ &=\frac{6 x^{2} \ln{\left(x \right)} + 3 x^{2} - 3 x \ln{\left(x \right)} - 3 x + 1}{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e^{2}$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e^{2}} &=(3 (e^{2})^{2} - 3 (e^{2}) + 1)\cdot (\frac{1}{(e^{2})})+(\ln{\left((e^{2}) \right)})\cdot (6 (e^{2}) - 3) \\ &=(- 3 e^{2} + 1 + 3 e^{4})\cdot (e^{-2})+(2)\cdot (-3 + 6 e^{2}) \\ &=-9 + e^{-2} + 15 e^{2}.\end{aligned}
$$

Therefore, the slope of the tangent line is $-9 + e^{-2} + 15 e^{2}.$

## Generated variant: hard_poly_log / hard

If a curve $C$ is given by $y=(- 2 x^{2} - 3 x + 1)\cdot (\ln{\left(x \right)})$, calculate the slope of the tangent line to the curve at the point where $x=e$.

Slope $=$ {{field-1}}

- $- 6 e - 6 + e^{-1}$

We differentiate using the product rule. Let $u(x)=- 2 x^{2} - 3 x + 1$ and $v(x)=\ln{\left(x \right)}.$ Then, we have

$$
u'(x)=- 4 x - 3,\quad v'(x)=\frac{1}{x}.
$$

Applying the product rule gives

$$
\begin{aligned}\frac{\mathrm dy}{\mathrm dx} &=uv'(x)+vu'(x) \\ &=(- 2 x^{2} - 3 x + 1)\cdot (\frac{1}{x})+(\ln{\left(x \right)})\cdot (- 4 x - 3) \\ &=- \frac{4 x^{2} \ln{\left(x \right)} + 2 x^{2} + 3 x \ln{\left(x \right)} + 3 x - 1}{x}.\end{aligned}
$$

To find the slope of the tangent line, we now substitute $x=e$ into the formula and get

$$
\begin{aligned}\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x=e} &=(- 2 (e)^{2} - 3 (e) + 1)\cdot (\frac{1}{(e)})+(\ln{\left((e) \right)})\cdot (- 4 (e) - 3) \\ &=(- 2 e^{2} - 3 e + 1)\cdot (e^{-1})+(1)\cdot (- 4 e - 3) \\ &=- 6 e - 6 + e^{-1}.\end{aligned}
$$

Therefore, the slope of the tangent line is $- 6 e - 6 + e^{-1}.$