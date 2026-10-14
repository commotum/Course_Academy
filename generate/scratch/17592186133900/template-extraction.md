# Template extraction

## 1. Specific sources

All raw prompts, solutions, banks and designation presence are retained in source.json. The following component mapping covers every displayed original option. `amplitude` acts linearly on P,Q, their held partials, curl and complete integral calculation sides. It does not alter the theorem, domain, or polar change-of-variables statement. Named F and the generic curl of the parameterized P,Q already incorporate amplitude and are not multiplied a second time. Complete source expressions are masked; no short numeric replacement is used. Identity amplitude is the same recipe at its original input. Historical numerical shapes alone do not identify author intent. Raw banks are empirical linear-amplitude replay recipes, **evidence only**, not recovered mistakes or normal defaults.

### q-126566 / annulus_quadratic

Prompt: ![](images/52/52815b087f869769950d37ab6b95edb75accf030e742ed16b4679b6a41d7d638.png)

Calculate ${∮}_{∂D}-{x}^{2}y\,dx+x{y}^{2}\,dy,$ where $D$ is the annular region shown above.

P = `-x**2*y`; Q = `x*y**2`

Geometry: `(1, 2)`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / b24f5ff7-bafc-59bf-b1fe-ef9b2d41540e|`\frac{15\pi }{2}`|`amplitude * (15*pi/2)`|correct|
|selection / b24f5ff7-bafc-59bf-b1fe-ef9b2d41540e|`\frac{9\pi }{2}`|`amplitude * (9*pi/2)`|incorrect; operation opaque|
|selection / b24f5ff7-bafc-59bf-b1fe-ef9b2d41540e|`\frac{7\pi }{2}`|`amplitude * (7*pi/2)`|incorrect; operation opaque|
|selection / b24f5ff7-bafc-59bf-b1fe-ef9b2d41540e|`\frac{13\pi }{2}`|`amplitude * (13*pi/2)`|incorrect; operation opaque|
|selection / b24f5ff7-bafc-59bf-b1fe-ef9b2d41540e|`\frac{11\pi }{2}`|`amplitude * (11*pi/2)`|incorrect; operation opaque|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{2}y$ and $Q(x,y)=x{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{2},\,\frac{∂Q}{∂x}={y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-{x}^{2}y\,dx+x{y}^{2}\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}{y}^{2}-(-{x}^{2})\,\text{d}A \\  & ={∬}_{D}{x}^{2}+{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 2,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{x}^{2}+{y}^{2}\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{2}(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =2\pi {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =2\pi \cdot {\frac{1}{4}{r}^{4}|}_{1}^{2} \\  & =\frac{\pi }{2}\cdot ({2}^{4}-{1}^{4}) \\  & =\frac{15\pi }{2}.\end{aligned}
$$

### q-126645 / rectangle_y2

Prompt: ![](images/6b/6bda5a10df8a1ec081db97e7aa52755796f1d50be5447e3e64f55986116ada6e.png)

Calculate 
${∮}_{∂D}x{y}^{2}\,dx+({x}^{2}y+x{y}^{2})\,dy,$
where $D$ is the region shown above.

P = `x*y**2`; Q = `x**2*y + x*y**2`

Geometry: `([-4, 4, -3, 3], [0, 2, -1, 2])`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / af970c9a-4925-5b83-89f9-f1d57c4e3ec6|`84`|`amplitude * (84)`|missing original designation|
|selection / af970c9a-4925-5b83-89f9-f1d57c4e3ec6|`138`|`amplitude * (138)`|missing original designation|
|selection / af970c9a-4925-5b83-89f9-f1d57c4e3ec6|`120`|`amplitude * (120)`|missing original designation|
|selection / af970c9a-4925-5b83-89f9-f1d57c4e3ec6|`55`|`amplitude * (55)`|missing original designation|
|selection / af970c9a-4925-5b83-89f9-f1d57c4e3ec6|`169`|`amplitude * (169)`|missing original designation|
|selection / 83851aef-4707-5c37-b41d-06a411ef4f5f|`55`|`amplitude * (55)`|incorrect; operation opaque|
|selection / 83851aef-4707-5c37-b41d-06a411ef4f5f|`84`|`amplitude * (84)`|incorrect; operation opaque|
|selection / 83851aef-4707-5c37-b41d-06a411ef4f5f|`138`|`amplitude * (138)`|correct|
|selection / 83851aef-4707-5c37-b41d-06a411ef4f5f|`120`|`amplitude * (120)`|incorrect; operation opaque|
|selection / 83851aef-4707-5c37-b41d-06a411ef4f5f|`169`|`amplitude * (169)`|incorrect; operation opaque|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x{y}^{2}$ and $Q(x,y)={x}^{2}y+x{y}^{2}.$ Therefore,

$$
\frac{∂P}{∂y}=2xy,\,\frac{∂Q}{∂x}=2xy+{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}x{y}^{2}\,dx+({x}^{2}y+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}(2xy+{y}^{2})-2xy\,\text{d}A \\  & ={∬}_{D}{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-4\le x\le 4,-3\le y\le 3}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,0\le x\le 2,-1\le y\le 2}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{y}^{2}\,\text{d}A & ={∬}_{{Δ}_{1}}{y}^{2}\,\text{d}A-{∬}_{{Δ}_{2}}{y}^{2}\,\text{d}A \\  & ={\int }_{-3}^{3}{\int }_{-4}^{4}{y}^{2}\,\text{d}x\,\text{d}y-{\int }_{-1}^{2}{\int }_{0}^{2}{y}^{2}\,\text{d}x\,\text{d}y \\  & ={\int }_{-4}^{4}\,\text{d}x{\int }_{-3}^{3}{y}^{2}\,\text{d}y-{\int }_{0}^{2}\,\text{d}x{\int }_{-1}^{2}{y}^{2}\,\text{d}y \\  & =x\,{|}_{-4}^{4}\cdot \frac{{y}^{3}}{3}\,{|}_{-3}^{3}-x\,{|}_{0}^{2}\cdot \frac{{y}^{3}}{3}{|}_{-1}^{2} \\  & =(4-(-4))\cdot (9-(-9))-(2-0)\cdot (\frac{8}{3}-(-\frac{1}{3})) \\  & =8\cdot 18-2\cdot 3 \\  & =138.\end{aligned}
$$

### q-169207 / annulus_sin2

Prompt: ![](images/83/8354a964dc235f1c9676754cf7d163cb4a54f05bd5899ff398acb11a4287861d.png)     
                                
                            

   

                            Let $∂R$ be the boundary of the region $R,$ shown above. Use Green's theorem to calculate the following integral:

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        ${∮}_{∂R}^{}F\cdot \text{d}r\,={∮}_{∂R}^{}3x{y}^{2}\,dx-{y}^{3}\,dy\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

P = `3*x*y**2`; Q = `-y**3`

Geometry: `(1, 2)`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|field-1 / 53b1b3ff-21b1-5213-8b9c-584dd6a1a1eb|`0`|`amplitude * (0)`|correct|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates as 

$$
{∮}_{∂R}3x{y}^{2}\,dx-{y}^{3}\,dy={∬}_{Δ}-3{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\text{d}\theta .
$$

But this time, our region $R$ (in polar coordinates) is given by 

$$
Δ={(r,\theta )\,:\,1\le r\le 2,\,0\le \theta <2\pi }.
$$

Therefore, we get

$$
\begin{aligned}{∬}_{Δ}-3{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\text{d}\theta  & =-3{\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta  \\  & =-3{\int }_{0}^{2\pi }\operatorname{sin}⁡(2\theta )\,\text{d}\theta \cdot {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =-3{[\frac{\operatorname{cos}⁡(2\theta )}{-2}]}_{\theta =0}^{\theta =2\pi }\cdot {[\frac{1}{4}{r}^{4}]}_{r=1}^{r=2}\,\text{d}r \\  & =\frac{3}{2}(1-1)\cdot \frac{1}{4}({2}^{4}-{1}^{4}) \\  & =0.\end{aligned}
$$

### q-126935 / annulus_fourth

Prompt: ![](images/5c/5ca9f071eaeebb0b31fba99a48ca8f08bd6b4b73588838aad7b5f513c283fd6c.png)

Calculate ${∮}_{∂D}-({x}^{4}y+\frac{1}{3}{x}^{2}{y}^{3})\,dx+(x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2})\,dy,$ where $D$ is the annular region shown above.

P = `-x**4*y - x**2*y**3/3`; Q = `x**3*y**2/3 + x*y**4`

Geometry: `(1, 3)`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / 0fe2c0c3-ccf0-5837-bf7d-eba354f732ab|`\frac{80\pi }{3}`|`amplitude * (80*pi/3)`|incorrect; operation opaque|
|selection / 0fe2c0c3-ccf0-5837-bf7d-eba354f732ab|`\frac{242\pi }{3}`|`amplitude * (242*pi/3)`|incorrect; operation opaque|
|selection / 0fe2c0c3-ccf0-5837-bf7d-eba354f732ab|`\frac{728\pi }{3}`|`amplitude * (728*pi/3)`|correct|
|selection / 0fe2c0c3-ccf0-5837-bf7d-eba354f732ab|`728\pi `|`amplitude * (728*pi)`|incorrect; operation opaque|
|selection / 0fe2c0c3-ccf0-5837-bf7d-eba354f732ab|`243\pi `|`amplitude * (243*pi)`|incorrect; operation opaque|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{4}y-\frac{1}{3}{x}^{2}{y}^{3}$ and $Q(x,y)=x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{4}-{x}^{2}{y}^{2},\,\frac{∂Q}{∂x}={y}^{4}+{x}^{2}{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-({x}^{4}y+\frac{1}{3}{x}^{2}{y}^{3})\,dx+(x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}{y}^{4}+{x}^{2}{y}^{2}-(-{x}^{4}-{x}^{2}{y}^{2})\,\text{d}A \\  & ={∬}_{D}{x}^{4}+2{x}^{2}{y}^{2}+{y}^{4}\,\text{d}A \\  & ={∬}_{D}({x}^{2}+{y}^{2})^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ={(r,\theta )\,:\,1\le r\le 3,\,0\le \theta \le 2\pi }.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})^{2}\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{3}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{4}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{5}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{3}{r}^{5}\,\text{d}r \\  & =2\pi {\int }_{1}^{3}{r}^{5}\,\text{d}r \\  & =2\pi \cdot {\frac{1}{6}{r}^{6}|}_{1}^{3} \\  & =\frac{\pi }{3}\cdot ({3}^{6}-{1}^{6}) \\  & =\frac{728\pi }{3}.\end{aligned}
$$

### q-126937 / annulus_negative

Prompt: ![](images/e6/e6252037001e1a5548ede86a16b4ddde8f5aec8fd956bded55a3506f7b533dbe.png)

Calculate ${∮}_{∂D}(\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x)\,dx+(\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3})\,dy,$ where $D$ is the annular region shown above.

P = `y**3/3 + cos(x)`; Q = `-x**3/3 + log(sin(y)**2 + 1)` (normal logarithm has the documented domain repair)

Geometry: `(2, 4)`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / 1d326558-bc4e-5ef3-84ac-5f28a471d7e6|`-90\pi `|`amplitude * (-90*pi)`|incorrect; operation opaque|
|selection / 1d326558-bc4e-5ef3-84ac-5f28a471d7e6|`120\pi `|`amplitude * (120*pi)`|incorrect; operation opaque|
|selection / 1d326558-bc4e-5ef3-84ac-5f28a471d7e6|`-145\pi `|`amplitude * (-145*pi)`|incorrect; operation opaque|
|selection / 1d326558-bc4e-5ef3-84ac-5f28a471d7e6|`-120\pi `|`amplitude * (-120*pi)`|correct|
|selection / 1d326558-bc4e-5ef3-84ac-5f28a471d7e6|`90\pi `|`amplitude * (90*pi)`|incorrect; operation opaque|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x$ and $Q(x,y)=\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3}.$ So,

$$
\frac{∂P}{∂y}={y}^{2},\,\frac{∂Q}{∂x}=-{x}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x)\,dx+(\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}-{x}^{2}-{y}^{2}\,\text{d}A \\  & ={∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ={(r,\theta )\,:\,2\le r\le 4,\,0\le \theta \le 2\pi }.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{2}^{4}-{r}^{3}\,\text{d}r \\  & =-2\pi {\int }_{2}^{4}{r}^{3}\,\text{d}r \\  & =-2\pi \cdot {\frac{1}{4}{r}^{4}|}_{2}^{4} \\  & =-\frac{\pi }{2}\cdot ({4}^{4}-{2}^{4}) \\  & =-120\pi .\end{aligned}
$$

### q-126941 / rectangle_x3y2

Prompt: ![](images/b2/b232a4cddf05a425709c1b3204b69b0126e586b42a6af73b867dd75ee294d961.png)

Calculate 
${∮}_{∂D}({x}^{3}{y}^{3}+x)\,dx+({x}^{4}{y}^{2}-y)\,dy,$
where $D$ is the region shown above.

P = `x**3*y**3 + x`; Q = `x**4*y**2 - y`

Geometry: `([-2, 2, -1, 2], [0, 1, 0, 1])`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / 38c1ef24-72d4-585c-9c7b-034e01ca1112|`-\frac{1}{12}`|`amplitude * (-1/12)`|correct|
|selection / 38c1ef24-72d4-585c-9c7b-034e01ca1112|`-\frac{1}{3}`|`amplitude * (-1/3)`|incorrect; operation opaque|
|selection / 38c1ef24-72d4-585c-9c7b-034e01ca1112|`0`|`amplitude * (0)`|incorrect; operation opaque|
|selection / 38c1ef24-72d4-585c-9c7b-034e01ca1112|`-\frac{1}{4}`|`amplitude * (-1/4)`|incorrect; operation opaque|
|selection / 38c1ef24-72d4-585c-9c7b-034e01ca1112|`-1`|`amplitude * (-1)`|incorrect; operation opaque|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={x}^{3}{y}^{3}+x$ and $Q(x,y)={x}^{4}{y}^{2}-y.$ Therefore,

$$
\frac{∂P}{∂y}=3{x}^{3}{y}^{2},\,\frac{∂Q}{∂x}=4{x}^{3}{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}({x}^{3}{y}^{3}+x)\,dx+({x}^{4}{y}^{2}-y)\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}4{x}^{3}{y}^{2}-3{x}^{3}{y}^{2}\,\text{d}A \\  & ={∬}_{D}{x}^{3}{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-2\le x\le 2,-1\le y\le 2}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,0\le x\le 1,0\le y\le 1}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{x}^{3}{y}^{2}\,\text{d}A & ={∬}_{{Δ}_{1}}{x}^{3}{y}^{2}\,\text{d}A-{∬}_{{Δ}_{2}}{x}^{3}{y}^{2}\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{-2}^{2}{x}^{3}{y}^{2}\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{0}^{1}{x}^{3}{y}^{2}\,\text{d}x\,\text{d}y \\  & ={\int }_{-2}^{2}{x}^{3}\,\text{d}x{\int }_{-1}^{2}{y}^{2}\,\text{d}y-{\int }_{0}^{1}{x}^{3}\,\text{d}x{\int }_{0}^{1}{y}^{2}\,\text{d}y \\  & =\frac{{x}^{4}}{4}\,{|}_{-2}^{2}\cdot \frac{{y}^{3}}{3}\,{|}_{-1}^{2}-\frac{{x}^{4}}{4}\,{|}_{0}^{1}\cdot \frac{{y}^{3}}{3}\,{|}_{0}^{1} \\  & =(4-4)\cdot (\frac{8}{3}-(-\frac{1}{3}))-(\frac{1}{4}-0)\cdot (\frac{1}{3}-0) \\  & =0\cdot 3-\frac{1}{4}\cdot \frac{1}{3} \\  & =-\frac{1}{12}.\end{aligned}
$$

### q-126945 / rectangle_xy

Prompt: ![](images/75/754aa1ded10b20362350f3da9e5b4dbe5f9f194c2289af348ff9de34f2fb8cc5.png)

Calculate 
${∮}_{∂D}(x{y}^{2}+{x}^{3})\,dx+(2{x}^{2}y-{y}^{3})\,dy,$
where $D$ is the region shown above.

P = `x**3 + x*y**2`; Q = `2*x**2*y - y**3`

Geometry: `([-2, 2, -1, 2], [-1, 1, 0, 1])`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / 1303c02b-a3ee-52e9-98a2-763dbec18e4b|`\frac{1}{2}`|`amplitude * (1/2)`|incorrect; operation opaque|
|selection / 1303c02b-a3ee-52e9-98a2-763dbec18e4b|`-\frac{3}{2}`|`amplitude * (-3/2)`|incorrect; operation opaque|
|selection / 1303c02b-a3ee-52e9-98a2-763dbec18e4b|`1`|`amplitude * (1)`|incorrect; operation opaque|
|selection / 1303c02b-a3ee-52e9-98a2-763dbec18e4b|`-\frac{7}{2}`|`amplitude * (-7/2)`|incorrect; operation opaque|
|selection / 1303c02b-a3ee-52e9-98a2-763dbec18e4b|`0`|`amplitude * (0)`|correct|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x{y}^{2}+{x}^{3}$ and $Q(x,y)=2{x}^{2}y-{y}^{3}.$ Therefore,

$$
\frac{∂P}{∂y}=2xy,\,\frac{∂Q}{∂x}=4xy.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(x{y}^{2}+{x}^{3})\,dx+(2{x}^{2}y-{y}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}4xy-2xy\,\text{d}A \\  & ={∬}_{D}2xy\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-2\le x\le 2,-1\le y\le 2}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,-1\le x\le 1,0\le y\le 1}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}2xy\,\text{d}A & ={∬}_{{Δ}_{1}}2xy\,\text{d}A-{∬}_{{Δ}_{2}}2xy\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{-2}^{2}2xy\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{-1}^{1}2xy\,\text{d}x\,\text{d}y \\  & ={\int }_{-2}^{2}2x\,\text{d}x{\int }_{-1}^{2}y\,\text{d}y-{\int }_{-1}^{1}2x\,\text{d}x{\int }_{0}^{1}y\,\text{d}y \\  & ={x}^{2}\,{|}_{-2}^{2}\cdot \frac{{y}^{2}}{2}\,{|}_{-1}^{2}-{x}^{2}\,{|}_{-1}^{1}\cdot \frac{{y}^{2}}{2}\,{|}_{0}^{1} \\  & =(4-4)\cdot (2-\frac{1}{2})-(1-1)\cdot (\frac{1}{2}-0) \\  & =0\cdot \frac{3}{2}-0\cdot \frac{1}{2} \\  & =0.\end{aligned}
$$

### q-126939 / annulus_odd

Prompt: ![](images/b1/b1a063fd261e790a8c3a56f741d0356f963300c3fbd88ddde03aa1744ef81053.png)

Calculate ${∮}_{∂D}({x}^{2}-{y}^{4})\,dx+({x}^{3}y-x{y}^{3})\,dy,$ where $D$ is the annular region shown above.

P = `x**2 - y**4`; Q = `x**3*y - x*y**3`

Geometry: `(1, 4)`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / 4a97b187-3262-5c06-b7ed-fed9c7d6dc5c|`0`|`amplitude * (0)`|correct|
|selection / 4a97b187-3262-5c06-b7ed-fed9c7d6dc5c|`189`|`amplitude * (189)`|incorrect; operation opaque|
|selection / 4a97b187-3262-5c06-b7ed-fed9c7d6dc5c|`192`|`amplitude * (192)`|incorrect; operation opaque|
|selection / 4a97b187-3262-5c06-b7ed-fed9c7d6dc5c|`180`|`amplitude * (180)`|incorrect; operation opaque|
|selection / 4a97b187-3262-5c06-b7ed-fed9c7d6dc5c|`200`|`amplitude * (200)`|incorrect; operation opaque|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={x}^{2}-{y}^{4}$ and $Q(x,y)=({x}^{3}y-x{y}^{3}).$ So,

$$
\frac{∂P}{∂y}=-4{y}^{3},\,\frac{∂Q}{∂x}=3{x}^{2}y-{y}^{3}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}({x}^{2}-{y}^{4})\,dx+({x}^{3}y-x{y}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}y-{y}^{3}-(-4{y}^{3})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}y+3{y}^{3}\,\text{d}A \\  & ={∬}_{D}3y({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 4,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}3y({x}^{2}+{y}^{2})\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3\cdot r\operatorname{sin}⁡\theta \cdot ((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3{r}^{2}\operatorname{sin}⁡\theta \cdot {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\operatorname{sin}⁡\theta \,\text{d}\theta {\int }_{1}^{4}3{r}^{4}\,\text{d}r \\  & =\operatorname{cos}⁡\theta \,{|}_{0}^{2\pi }\cdot \frac{3{r}^{5}}{5}\,{|}_{1}^{4} \\  & =(\operatorname{cos}⁡(2\pi )-\operatorname{cos}⁡(0))\cdot (\frac{3(4)^{5}}{5}-\frac{3(1)^{5}}{5}) \\  & =(1-1)\cdot (\frac{3(4)^{5}}{5}-\frac{3(1)^{5}}{5}) \\  & =0.\end{aligned}
$$

### q-126938 / annulus_four

Prompt: ![](images/5c/5ca9f071eaeebb0b31fba99a48ca8f08bd6b4b73588838aad7b5f513c283fd6c.png)

Calculate ${∮}_{∂D}-({x}^{2}y+{y}^{3})\,dx+({x}^{3}+x{y}^{2})\,dy,$ where $D$ is the annular region shown above.

P = `-x**2*y - y**3`; Q = `x**3 + x*y**2`

Geometry: `(1, 3)`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / 2b281059-95fd-5ff3-8dbf-e28f1dfbb9f1|`100\pi `|`amplitude * (100*pi)`|incorrect; operation opaque|
|selection / 2b281059-95fd-5ff3-8dbf-e28f1dfbb9f1|`80\pi `|`amplitude * (80*pi)`|incorrect; operation opaque|
|selection / 2b281059-95fd-5ff3-8dbf-e28f1dfbb9f1|`140\pi `|`amplitude * (140*pi)`|incorrect; operation opaque|
|selection / 2b281059-95fd-5ff3-8dbf-e28f1dfbb9f1|`120\pi `|`amplitude * (120*pi)`|incorrect; operation opaque|
|selection / 2b281059-95fd-5ff3-8dbf-e28f1dfbb9f1|`160\pi `|`amplitude * (160*pi)`|correct|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{2}y-{y}^{3}$ and $Q(x,y)={x}^{3}+x{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{2}-3{y}^{2},\,\frac{∂Q}{∂x}=3{x}^{2}+{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-({x}^{2}y+{y}^{3})\,dx+({x}^{3}+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}+{y}^{2}-(-{x}^{2}-3{y}^{2})\,\text{d}A \\  & ={∬}_{D}4{x}^{2}+4{y}^{2}\,\text{d}A \\  & ={∬}_{D}4({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 3,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4({x}^{2}+{y}^{2})\,\text{d}A & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r \\  & =8\pi {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =8\pi \cdot {\frac{1}{4}{r}^{4}|}_{1}^{3} \\  & =2\pi \cdot ({3}^{4}-{1}^{4}) \\  & =160\pi .\end{aligned}
$$

### q-126942 / rectangle_shift

Prompt: ![](images/db/dbe6009d42623d3b3cd9f05380159bb0f4b8f22b920c1ef5d4d82b5dbf152d4a.png)

Calculate 
${∮}_{∂D}{y}^{2}(x+1)\,dx+(3{x}^{2}y+2xy)\,dy,$
where $D$ is the region shown above.

P = `y**2*(x + 1)`; Q = `3*x**2*y + 2*x*y`

Geometry: `([0, 3, -1, 2], [1, 2, 0, 1])`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / d21d5399-1389-5996-9269-7e769b0bb606|`42`|`amplitude * (42)`|incorrect; operation opaque|
|selection / d21d5399-1389-5996-9269-7e769b0bb606|`36`|`amplitude * (36)`|incorrect; operation opaque|
|selection / d21d5399-1389-5996-9269-7e769b0bb606|`24`|`amplitude * (24)`|correct|
|selection / d21d5399-1389-5996-9269-7e769b0bb606|`16`|`amplitude * (16)`|incorrect; operation opaque|
|selection / d21d5399-1389-5996-9269-7e769b0bb606|`27`|`amplitude * (27)`|incorrect; operation opaque|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={y}^{2}(x+1)$ and $Q(x,y)=3{x}^{2}y+2xy.$ Therefore,

$$
\frac{∂P}{∂y}=2y(x+1),\,\frac{∂Q}{∂x}=6xy+2y.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}{y}^{2}(x+1)\,dx+(3{x}^{2}y+2xy)\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}(6xy+2y)-2y(x+1)\,\text{d}A \\  & ={∬}_{D}4xy\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}=\{(x,y)\,:\,0\le x\le 3,-1\le y\le 2\}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}=\{(x,y)\,:\,1\le x\le 2,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4xy\,\text{d}A & ={∬}_{{Δ}_{1}}4xy\,\text{d}A-{∬}_{{Δ}_{2}}4xy\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{0}^{3}4xy\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{1}^{2}4xy\,\text{d}x\,\text{d}y \\  & ={\int }_{0}^{3}2x\,\text{d}x{\int }_{-1}^{2}2y\,\text{d}y-{\int }_{1}^{2}2x\,\text{d}x{\int }_{0}^{1}2y\,\text{d}y \\  & ={x}^{2}\,{|}_{0}^{3}\cdot {y}^{2}\,{|}_{-1}^{2}-{x}^{2}\,{|}_{1}^{2}\cdot {y}^{2}\,{|}_{0}^{1} \\  & =(9-0)\cdot (4-1)-(4-1)\cdot (1-0) \\  & =9\cdot 3-3\cdot 1 \\  & =24.\end{aligned}
$$

### q-126946 / rectangle_x2y3

Prompt: ![](images/9b/9be396fd57559bb77f92d5a0421f3a7cdca577203904e577da0caf5326caac91.png)

Calculate 
${∮}_{∂D}(2{x}^{2}{y}^{4}-x)\,dx+(4{x}^{3}{y}^{3}-{y}^{2})\,dy,$
where $D$ is the region shown above.

P = `2*x**2*y**4 - x`; Q = `4*x**3*y**3 - y**2`

Geometry: `([-1, 2, -2, 2], [0, 1, 0, 1])`. Exact integer bounds, polynomial powers, signs and unit/rational coefficients are held in the family.

| Field | Source value | Exact empirical amplitude recipe | Designation |
|---|---|---|---|
|selection / 5e0020cb-0a2c-5126-8edf-5125f13da402|`\frac{2}{3}`|`amplitude * (2/3)`|incorrect; operation opaque|
|selection / 5e0020cb-0a2c-5126-8edf-5125f13da402|`0`|`amplitude * (0)`|incorrect; operation opaque|
|selection / 5e0020cb-0a2c-5126-8edf-5125f13da402|`\frac{3}{4}`|`amplitude * (3/4)`|incorrect; operation opaque|
|selection / 5e0020cb-0a2c-5126-8edf-5125f13da402|`-\frac{4}{3}`|`amplitude * (-4/3)`|incorrect; operation opaque|
|selection / 5e0020cb-0a2c-5126-8edf-5125f13da402|`-\frac{1}{3}`|`amplitude * (-1/3)`|correct|

Source solution stage sequence (unaltered in raw replay):

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2{x}^{2}{y}^{4}-x$ and $Q(x,y)=4{x}^{3}{y}^{3}-{y}^{2}.$ Therefore,

$$
\frac{∂P}{∂y}=8{x}^{2}{y}^{3},\,\frac{∂Q}{∂x}=12{x}^{2}{y}^{3}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(2{x}^{2}{y}^{4}-x)\,dx+(4{x}^{3}{y}^{3}-{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}12{x}^{2}{y}^{3}-8{x}^{2}{y}^{3}\,\text{d}A \\  & ={∬}_{D}4{x}^{2}{y}^{3}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}=\{(x,y)\,:\,-1\le x\le 2,-2\le y\le 2\}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}=\{(x,y)\,:\,0\le x\le 1,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4{x}^{2}{y}^{3}\,\text{d}A & ={∬}_{{Δ}_{1}}4{x}^{2}{y}^{3}\,\text{d}A-{∬}_{{Δ}_{2}}4{x}^{2}{y}^{3}\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}4{x}^{2}{y}^{3}\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{0}^{1}4{x}^{2}{y}^{3}\,\text{d}x\,\text{d}y \\  & ={\int }_{-1}^{2}{x}^{2}\,\text{d}x{\int }_{-2}^{2}4{y}^{3}\,\text{d}y-{\int }_{0}^{1}{x}^{2}\,\text{d}x{\int }_{0}^{1}4{y}^{3}\,\text{d}y \\  & =\frac{{x}^{3}}{3}\,{|}_{-1}^{2}\cdot {y}^{4}\,{|}_{-2}^{2}-\frac{{x}^{3}}{3}\,{|}_{0}^{1}\cdot {y}^{4}\,{|}_{0}^{1} \\  & =(\frac{8}{3}-(-\frac{1}{3}))\cdot (16-16)-(\frac{1}{3}-0)\cdot (1-0) \\  & =3\cdot 0-\frac{1}{3}\cdot 1 \\  & =-\frac{1}{3}.\end{aligned}
$$

## 2. Generalized method

Green’s theorem converts the positively oriented boundary circulation into the integral of Q_x−P_y. Moderate annuli require partial derivatives and radial factorization/cancellation before polar integration. Hard rectangles require partial derivatives, outer-minus-hole decomposition, actual dx then dy order, separable products, independent primitives, individual upper/lower endpoint components, differences and final result.

## 3. Complete normal operation banks

Radial annulus bank: correct integral; reverse Q_x−P_y sign; omit inner radius; add inner contribution; omit Jacobian r. Odd-sine annulus bank: correct zero; replace full turn by half turn; add cosine endpoints; omit sine; use π as angular measure. The sine-double-angle family retains its observed blank shape with correct zero. Rectangle bank: correct outer-minus-hole; add hole; omit hole; reverse subtraction; integrate Q_x only (omit P_y). These operations derive complete mathematical values from actual instance expressions. Pairwise scalar comparison covers correct and incorrect options alike; ANY collision rejects the entire instance. Symmetric rectangle anchors can make this operation bank ineligible; their historical banks remain publicly replayable and normal sampling uses same-family translated rectangles with nonzero eligible moments. There is no post-hoc option replacement.

## 4. Reusable masks, constraints and authored bounds

Moderate/hard field-family P,Q formulas are fixed up to signed integer amplitude c, 1≤|c|≤3. Annulus radii are integers 1≤inner<outer≤5. Hard uses the source rectangle geometry translated by x/y shifts −1,0,1, bounds |coordinate|≤6; explicit API permits other strict nested integer rectangles within these arithmetic bounds. Hard always has one strict interior rectangular hole. No new integration method or boundary orientation question is introduced. A normal smooth same-variable term does not change the held partial assessment.

The easy authored family supplies c(x²+y²) as curl, so learners perform the same advanced annular-region integral without the moderate field differentiation. It is a design claim, not an observed easy level. Lesson route (follow first-step/next): Introduction → Circulation tutorial → sibling circulation KP → Extending Green’s Theorem tutorial → Orientation intuition → sibling simple-hole Green KP → A Note About Double Integrals Over Regions With Holes → this advanced KP → extension proof. The immediate preceding note establishes outer-minus-hole subtraction, canonical e-9558 establishes separated Cartesian monomial integration, and prerequisite Green’s Theorem in Polar Coordinates establishes the annular conversion. Easy removes derivative setup while retaining the annular hole; it does not repurpose the sibling circulation-sum KP or introduce area calculations.

Normal family chains retain the shared Green theorem wording, held coordinate convention, derivative signs, factorizations, cancellation, integration order and source primitive factor conventions. Mathematical notation is normalized to standard TeX; a supplemental held-operator/component block retains every zero coordinate-derivative contribution before reduction; supplemental individual endpoint rows are added in polar families, without replacing the primitive and collected stages. q-169207 retains its boundary R / vector-line-integral / blank layout and shared “As we saw earlier” and “But this time” prose, with explicit held partials added for stand-alone use. Normal source-format fidelity is therefore structural/presentation-normalized, not raw text exact.

## Source errors and separate repairs

- q-126645: duplicate same-key legacy field lacks correct ref. The other captured field and source worked solution designate 138. Raw presence is preserved; no missing ref is counted as matched. Normal has one complete field.
- q-126937: ln(sin²y) is undefined at y=0, crossing both circles. Its stated circulation is invalid, despite the formal curl and −120π calculation. Normal minimal repair is ln(1+sin²y), smooth everywhere and with held Q_x unchanged. This is a domain correction, not a recovered variation or new assessed branch.
- q-126939: primitive of sin θ is −cos θ. The raw source incorrectly prints +cos θ, masked by the full-turn zero. Normal includes the negative sign at BOTH endpoints.
- q-126938: isolated intermediate radial upper limit2 conflicts with outer radius3; normal uses the actual outer radius throughout. Missing integrand parentheses in radial substitutions are normalized.

Raw masks preserve these source errors as evidence. Validation reports raw-exact text/bank counts separately from normal correctness and native grading. No source error is silently promoted to normal defaults.

## Identity

Content ID uses generator version, actual difficulty, complete learner prompt, fixed solution, full owned banks and correct-value presence. It excludes seed, option order and unused profile aliases. Mathematical-task fingerprint excludes profiles/banks and zero-held-partial additions. Full-turn odd/sin2 cancellation fingerprints omit amplitude and annular radii because they do not change the assessed zero angular operation. Supplied-curl information differs from field-differentiation demand. Nonzero held partial components remain in the task identity because different derivative work can lead to the same curl. Rectangle geometry and curl determine the integral; only one hole is supported, so same-role hole interchangeability is vacuous here. Full presentation metadata and plot geometry remain available separately.
