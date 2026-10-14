# Review: raw originals and generated variants

Original raw records preserve source mistakes and legacy-field presence. Historical amplitude variants are evidence-only empirical banks; normal generated variants use complete method-derived banks. Easy is authored supplied-curl scope. All source/bank repairs are documented in template-extraction.md.

## Raw original q-126566

Parameters: `{"amplitude": 1}`; profile `raw:q-126566`.

![](/media/jake/SSD/EDB/math/images/52/52815b087f869769950d37ab6b95edb75accf030e742ed16b4679b6a41d7d638.png)

Calculate ${∮}_{∂D}-{x}^{2}y\,dx+x{y}^{2}\,dy,$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{7\pi }{2}$
- $\frac{9\pi }{2}$
- $\frac{15\pi }{2}$ (correct)
- $\frac{11\pi }{2}$
- $\frac{13\pi }{2}$

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

## Generated historical-evidence amplitude variant q-126566

Parameters: `{"amplitude": 2}`; profile `raw:q-126566`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/579bbcfdc228114d333fd33f1f3d4d4c7bfa7a67783ed23456d37a214529da31.png)

Calculate $2\left({∮}_{∂D}-{x}^{2}y\,dx+x{y}^{2}\,dy,\right)$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $7 \pi$
- $9 \pi$
- $15 \pi$ (correct)
- $11 \pi$
- $13 \pi$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left(-{x}^{2}y\right)$ and $Q(x,y)=2\left(x{y}^{2}.\right)$ So,

$$
\frac{∂P}{∂y}=2\left(-{x}^{2},\right)\,\frac{∂Q}{∂x}=2\left({y}^{2}.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}-{x}^{2}y\,dx+x{y}^{2}\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}{y}^{2}-(-{x}^{2})\,\text{d}A \right)\\  & =2\left({∬}_{D}{x}^{2}+{y}^{2}\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$2\left(
Δ\right)=2\left(\{(r,\theta )\,:\,1\le r\le 2,\,0\le \theta \le 2\pi \}.
\right)$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}{x}^{2}+{y}^{2}\,\text{d}A \right)& =2\left({\int }_{0}^{2\pi }{\int }_{1}^{2}(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{2}{r}^{3}\,\text{d}r \right)\\  & =2\left(2\pi {\int }_{1}^{2}{r}^{3}\,\text{d}r \right)\\  & =2\left(2\pi \cdot {\frac{1}{4}{r}^{4}|}_{1}^{2} \right)\\  & =2\left(\frac{\pi }{2}\cdot ({2}^{4}-{1}^{4}) \right)\\  & =2\left(\frac{15\pi }{2}.\right)\end{aligned}
$$

## Raw original q-126645

Parameters: `{"amplitude": 1}`; profile `raw:q-126645`.

![](/media/jake/SSD/EDB/math/images/6b/6bda5a10df8a1ec081db97e7aa52755796f1d50be5447e3e64f55986116ada6e.png)

Calculate 
${∮}_{∂D}x{y}^{2}\,dx+({x}^{2}y+x{y}^{2})\,dy,$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $120$
- $138$
- $84$
- $169$
- $55$
Original correct designation absent; retained as evidence.

Field `selection` (:answer-field.type/radio):
- $138$ (correct)
- $120$
- $169$
- $55$
- $84$

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

## Generated historical-evidence amplitude variant q-126645

Parameters: `{"amplitude": 2}`; profile `raw:q-126645`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/91bd870e69124b842eae727f5c4fcd7d687731e9e3a8a141f2794f5a663fe09d.png)

Calculate 
$2\left({∮}_{∂D}x{y}^{2}\,dx+({x}^{2}y+x{y}^{2})\,dy,\right)$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $240$
- $276$
- $168$
- $338$
- $110$
Original correct designation absent; retained as evidence.

Field `selection` (:answer-field.type/radio):
- $276$ (correct)
- $240$
- $338$
- $110$
- $168$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left(x{y}^{2}\right)$ and $Q(x,y)=2\left({x}^{2}y+x{y}^{2}.\right)$ Therefore,

$$
\frac{∂P}{∂y}=2\left(2xy,\right)\,\frac{∂Q}{∂x}=2\left(2xy+{y}^{2}.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}x{y}^{2}\,dx+({x}^{2}y+x{y}^{2})\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}(2xy+{y}^{2})-2xy\,\text{d}A \right)\\  & =2\left({∬}_{D}{y}^{2}\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- $2\left({Δ}_{1}\right)=2\left({(x,y)\,:\,-4\le x\le 4,-3\le y\le 3}\right)$ is the region enclosed by the outer curve, and

- $2\left({Δ}_{2}\right)=2\left({(x,y)\,:\,0\le x\le 2,-1\le y\le 2}\right)$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}{y}^{2}\,\text{d}A \right)& =2\left({∬}_{{Δ}_{1}}{y}^{2}\,\text{d}A-{∬}_{{Δ}_{2}}{y}^{2}\,\text{d}A \right)\\  & =2\left({\int }_{-3}^{3}{\int }_{-4}^{4}{y}^{2}\,\text{d}x\,\text{d}y-{\int }_{-1}^{2}{\int }_{0}^{2}{y}^{2}\,\text{d}x\,\text{d}y \right)\\  & =2\left({\int }_{-4}^{4}\,\text{d}x{\int }_{-3}^{3}{y}^{2}\,\text{d}y-{\int }_{0}^{2}\,\text{d}x{\int }_{-1}^{2}{y}^{2}\,\text{d}y \right)\\  & =2\left(x\,{|}_{-4}^{4}\cdot \frac{{y}^{3}}{3}\,{|}_{-3}^{3}-x\,{|}_{0}^{2}\cdot \frac{{y}^{3}}{3}{|}_{-1}^{2} \right)\\  & =2\left((4-(-4))\cdot (9-(-9))-(2-0)\cdot (\frac{8}{3}-(-\frac{1}{3})) \right)\\  & =2\left(8\cdot 18-2\cdot 3 \right)\\  & =2\left(138.\right)\end{aligned}
$$

## Raw original q-169207

Parameters: `{"amplitude": 1}`; profile `raw:q-169207`.

![](/media/jake/SSD/EDB/math/images/83/8354a964dc235f1c9676754cf7d163cb4a54f05bd5899ff398acb11a4287861d.png)     
                                
                            

   

                            Let $∂R$ be the boundary of the region $R,$ shown above. Use Green's theorem to calculate the following integral:

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        ${∮}_{∂R}^{}F\cdot \text{d}r\,={∮}_{∂R}^{}3x{y}^{2}\,dx-{y}^{3}\,dy\,=$

                                    
                                
                                    
                            
                                        {{field-1}}

Field `field-1` (:answer-field.type/blank):
- $0$ (correct)

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

## Generated historical-evidence amplitude variant q-169207

Parameters: `{"amplitude": 2}`; profile `raw:q-169207`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/00d4c445f70759b5bcb2661f738ffda17d9a8b365cf2a5c5b2e3bf4b383fbc8f.png)     
                                
                            

   

                            Let $∂R$ be the boundary of the region $R,$ shown above. Use Green's theorem to calculate the following integral:

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        ${∮}_{∂R}^{}F\cdot \text{d}r\,=2\left({∮}_{∂R}^{}3x{y}^{2}\,dx-{y}^{3}\,dy\,\right)=$

                                    
                                
                                    
                            
                                        {{field-1}}

Field `field-1` (:answer-field.type/blank):
- $0$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates as 

$$2\left(
{∮}_{∂R}3x{y}^{2}\,dx-{y}^{3}\,dy\right)=2\left({∬}_{Δ}-3{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\text{d}\theta .
\right)$$

But this time, our region $R$ (in polar coordinates) is given by 

$$2\left(
Δ\right)=2\left({(r,\theta )\,:\,1\le r\le 2,\,0\le \theta <2\pi }.
\right)$$

Therefore, we get

$$
\begin{aligned}2\left({∬}_{Δ}-3{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\text{d}\theta  \right)& =2\left(-3{\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left(-3{\int }_{0}^{2\pi }\operatorname{sin}⁡(2\theta )\,\text{d}\theta \cdot {\int }_{1}^{2}{r}^{3}\,\text{d}r \right)\\  & =2\left(-3{[\frac{\operatorname{cos}⁡(2\theta )}{-2}]}_{\theta =0}^{\theta =2\pi }\cdot {[\frac{1}{4}{r}^{4}]}_{r=1}^{r=2}\,\text{d}r \right)\\  & =2\left(\frac{3}{2}(1-1)\cdot \frac{1}{4}({2}^{4}-{1}^{4}) \right)\\  & =2\left(0.\right)\end{aligned}
$$

## Raw original q-126935

Parameters: `{"amplitude": 1}`; profile `raw:q-126935`.

![](/media/jake/SSD/EDB/math/images/5c/5ca9f071eaeebb0b31fba99a48ca8f08bd6b4b73588838aad7b5f513c283fd6c.png)

Calculate ${∮}_{∂D}-({x}^{4}y+\frac{1}{3}{x}^{2}{y}^{3})\,dx+(x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2})\,dy,$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{728\pi }{3}$ (correct)
- $\frac{242\pi }{3}$
- $\frac{80\pi }{3}$
- $243\pi $
- $728\pi $

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

## Generated historical-evidence amplitude variant q-126935

Parameters: `{"amplitude": 2}`; profile `raw:q-126935`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/0abfccc370386839f8fc76bdfd988eb0fa9434fadb8e02d6630ed0b907b40588.png)

Calculate $2\left({∮}_{∂D}-({x}^{4}y+\frac{1}{3}{x}^{2}{y}^{3})\,dx+(x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2})\,dy,\right)$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{1456 \pi}{3}$ (correct)
- $\frac{484 \pi}{3}$
- $\frac{160 \pi}{3}$
- $486 \pi$
- $1456 \pi$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left(-{x}^{4}y-\frac{1}{3}{x}^{2}{y}^{3}\right)$ and $Q(x,y)=2\left(x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2}.\right)$ So,

$$
\frac{∂P}{∂y}=2\left(-{x}^{4}-{x}^{2}{y}^{2},\right)\,\frac{∂Q}{∂x}=2\left({y}^{4}+{x}^{2}{y}^{2}.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}-({x}^{4}y+\frac{1}{3}{x}^{2}{y}^{3})\,dx+(x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2})\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}{y}^{4}+{x}^{2}{y}^{2}-(-{x}^{4}-{x}^{2}{y}^{2})\,\text{d}A \right)\\  & =2\left({∬}_{D}{x}^{4}+2{x}^{2}{y}^{2}+{y}^{4}\,\text{d}A \right)\\  & =2\left({∬}_{D}({x}^{2}+{y}^{2})^{2}\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$2\left(
Δ\right)=2\left({(r,\theta )\,:\,1\le r\le 3,\,0\le \theta \le 2\pi }.
\right)$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}({x}^{2}+{y}^{2})^{2}\,\text{d}A \right)& =2\left({\int }_{0}^{2\pi }{\int }_{1}^{3}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})^{2}\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{4}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{5}\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{3}{r}^{5}\,\text{d}r \right)\\  & =2\left(2\pi {\int }_{1}^{3}{r}^{5}\,\text{d}r \right)\\  & =2\left(2\pi \cdot {\frac{1}{6}{r}^{6}|}_{1}^{3} \right)\\  & =2\left(\frac{\pi }{3}\cdot ({3}^{6}-{1}^{6}) \right)\\  & =2\left(\frac{728\pi }{3}.\right)\end{aligned}
$$

## Raw original q-126937

Parameters: `{"amplitude": 1}`; profile `raw:q-126937`.

![](/media/jake/SSD/EDB/math/images/e6/e6252037001e1a5548ede86a16b4ddde8f5aec8fd956bded55a3506f7b533dbe.png)

Calculate ${∮}_{∂D}(\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x)\,dx+(\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3})\,dy,$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $-145\pi $
- $120\pi $
- $-90\pi $
- $90\pi $
- $-120\pi $ (correct)

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

## Generated historical-evidence amplitude variant q-126937

Parameters: `{"amplitude": 2}`; profile `raw:q-126937`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/2e51a131a847edaf39f61aac753dfc21e216098b5938342ad9555562fd6cfa5d.png)

Calculate $2\left({∮}_{∂D}(\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x)\,dx+(\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3})\,dy,\right)$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- 290 \pi$
- $240 \pi$
- $- 180 \pi$
- $180 \pi$
- $- 240 \pi$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left(\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x\right)$ and $Q(x,y)=2\left(\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3}.\right)$ So,

$$
\frac{∂P}{∂y}=2\left({y}^{2},\right)\,\frac{∂Q}{∂x}=2\left(-{x}^{2}.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}(\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x)\,dx+(\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3})\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}-{x}^{2}-{y}^{2}\,\text{d}A \right)\\  & =2\left({∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$2\left(
Δ\right)=2\left({(r,\theta )\,:\,2\le r\le 4,\,0\le \theta \le 2\pi }.
\right)$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A \right)& =2\left({\int }_{0}^{2\pi }{\int }_{2}^{4}-((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }{\int }_{2}^{4}-{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }{\int }_{2}^{4}-{r}^{3}\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{2}^{4}-{r}^{3}\,\text{d}r \right)\\  & =2\left(-2\pi {\int }_{2}^{4}{r}^{3}\,\text{d}r \right)\\  & =2\left(-2\pi \cdot {\frac{1}{4}{r}^{4}|}_{2}^{4} \right)\\  & =2\left(-\frac{\pi }{2}\cdot ({4}^{4}-{2}^{4}) \right)\\  & =2\left(-120\pi .\right)\end{aligned}
$$

## Raw original q-126941

Parameters: `{"amplitude": 1}`; profile `raw:q-126941`.

![](/media/jake/SSD/EDB/math/images/b2/b232a4cddf05a425709c1b3204b69b0126e586b42a6af73b867dd75ee294d961.png)

Calculate 
${∮}_{∂D}({x}^{3}{y}^{3}+x)\,dx+({x}^{4}{y}^{2}-y)\,dy,$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $0$
- $-\frac{1}{3}$
- $-\frac{1}{12}$ (correct)
- $-1$
- $-\frac{1}{4}$

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

## Generated historical-evidence amplitude variant q-126941

Parameters: `{"amplitude": 2}`; profile `raw:q-126941`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/c5c06e02a9712b4a77958cc9afdfd45a7e176c5f426b35bc19572f8ba58bd65c.png)

Calculate 
$2\left({∮}_{∂D}({x}^{3}{y}^{3}+x)\,dx+({x}^{4}{y}^{2}-y)\,dy,\right)$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $0$
- $- \frac{2}{3}$
- $- \frac{1}{6}$ (correct)
- $-2$
- $- \frac{1}{2}$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left({x}^{3}{y}^{3}+x\right)$ and $Q(x,y)=2\left({x}^{4}{y}^{2}-y.\right)$ Therefore,

$$
\frac{∂P}{∂y}=2\left(3{x}^{3}{y}^{2},\right)\,\frac{∂Q}{∂x}=2\left(4{x}^{3}{y}^{2}.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}({x}^{3}{y}^{3}+x)\,dx+({x}^{4}{y}^{2}-y)\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}4{x}^{3}{y}^{2}-3{x}^{3}{y}^{2}\,\text{d}A \right)\\  & =2\left({∬}_{D}{x}^{3}{y}^{2}\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- $2\left({Δ}_{1}\right)=2\left({(x,y)\,:\,-2\le x\le 2,-1\le y\le 2}\right)$ is the region enclosed by the outer curve, and

- $2\left({Δ}_{2}\right)=2\left({(x,y)\,:\,0\le x\le 1,0\le y\le 1}\right)$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}{x}^{3}{y}^{2}\,\text{d}A \right)& =2\left({∬}_{{Δ}_{1}}{x}^{3}{y}^{2}\,\text{d}A-{∬}_{{Δ}_{2}}{x}^{3}{y}^{2}\,\text{d}A \right)\\  & =2\left({\int }_{-1}^{2}{\int }_{-2}^{2}{x}^{3}{y}^{2}\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{0}^{1}{x}^{3}{y}^{2}\,\text{d}x\,\text{d}y \right)\\  & =2\left({\int }_{-2}^{2}{x}^{3}\,\text{d}x{\int }_{-1}^{2}{y}^{2}\,\text{d}y-{\int }_{0}^{1}{x}^{3}\,\text{d}x{\int }_{0}^{1}{y}^{2}\,\text{d}y \right)\\  & =2\left(\frac{{x}^{4}}{4}\,{|}_{-2}^{2}\cdot \frac{{y}^{3}}{3}\,{|}_{-1}^{2}-\frac{{x}^{4}}{4}\,{|}_{0}^{1}\cdot \frac{{y}^{3}}{3}\,{|}_{0}^{1} \right)\\  & =2\left((4-4)\cdot (\frac{8}{3}-(-\frac{1}{3}))-(\frac{1}{4}-0)\cdot (\frac{1}{3}-0) \right)\\  & =2\left(0\cdot 3-\frac{1}{4}\cdot \frac{1}{3} \right)\\  & =2\left(-\frac{1}{12}.\right)\end{aligned}
$$

## Raw original q-126945

Parameters: `{"amplitude": 1}`; profile `raw:q-126945`.

![](/media/jake/SSD/EDB/math/images/75/754aa1ded10b20362350f3da9e5b4dbe5f9f194c2289af348ff9de34f2fb8cc5.png)

Calculate 
${∮}_{∂D}(x{y}^{2}+{x}^{3})\,dx+(2{x}^{2}y-{y}^{3})\,dy,$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $1$
- $-\frac{3}{2}$
- $\frac{1}{2}$
- $0$ (correct)
- $-\frac{7}{2}$

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

## Generated historical-evidence amplitude variant q-126945

Parameters: `{"amplitude": 2}`; profile `raw:q-126945`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/065bf7f7bcb59e7e386e581322b48d09577c7b650c42411c55b36d071fb11108.png)

Calculate 
$2\left({∮}_{∂D}(x{y}^{2}+{x}^{3})\,dx+(2{x}^{2}y-{y}^{3})\,dy,\right)$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $2$
- $-3$
- $1$
- $0$ (correct)
- $-7$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left(x{y}^{2}+{x}^{3}\right)$ and $Q(x,y)=2\left(2{x}^{2}y-{y}^{3}.\right)$ Therefore,

$$
\frac{∂P}{∂y}=2\left(2xy,\right)\,\frac{∂Q}{∂x}=2\left(4xy.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}(x{y}^{2}+{x}^{3})\,dx+(2{x}^{2}y-{y}^{3})\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =2\left({∬}_{D}4xy-2xy\,\text{d}A \right)\\  & =2\left({∬}_{D}2xy\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- $2\left({Δ}_{1}\right)=2\left({(x,y)\,:\,-2\le x\le 2,-1\le y\le 2}\right)$ is the region enclosed by the outer curve, and

- $2\left({Δ}_{2}\right)=2\left({(x,y)\,:\,-1\le x\le 1,0\le y\le 1}\right)$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}2xy\,\text{d}A \right)& =2\left({∬}_{{Δ}_{1}}2xy\,\text{d}A-{∬}_{{Δ}_{2}}2xy\,\text{d}A \right)\\  & =2\left({\int }_{-1}^{2}{\int }_{-2}^{2}2xy\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{-1}^{1}2xy\,\text{d}x\,\text{d}y \right)\\  & =2\left({\int }_{-2}^{2}2x\,\text{d}x{\int }_{-1}^{2}y\,\text{d}y-{\int }_{-1}^{1}2x\,\text{d}x{\int }_{0}^{1}y\,\text{d}y \right)\\  & =2\left({x}^{2}\,{|}_{-2}^{2}\cdot \frac{{y}^{2}}{2}\,{|}_{-1}^{2}-{x}^{2}\,{|}_{-1}^{1}\cdot \frac{{y}^{2}}{2}\,{|}_{0}^{1} \right)\\  & =2\left((4-4)\cdot (2-\frac{1}{2})-(1-1)\cdot (\frac{1}{2}-0) \right)\\  & =2\left(0\cdot \frac{3}{2}-0\cdot \frac{1}{2} \right)\\  & =2\left(0.\right)\end{aligned}
$$

## Raw original q-126939

Parameters: `{"amplitude": 1}`; profile `raw:q-126939`.

![](/media/jake/SSD/EDB/math/images/b1/b1a063fd261e790a8c3a56f741d0356f963300c3fbd88ddde03aa1744ef81053.png)

Calculate ${∮}_{∂D}({x}^{2}-{y}^{4})\,dx+({x}^{3}y-x{y}^{3})\,dy,$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $192$
- $189$
- $0$ (correct)
- $200$
- $180$

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

## Generated historical-evidence amplitude variant q-126939

Parameters: `{"amplitude": 2}`; profile `raw:q-126939`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/0c455798e950906ca16b855717c1cf7cea1c441efb0533c820cb166bbf8fba42.png)

Calculate $2\left({∮}_{∂D}({x}^{2}-{y}^{4})\,dx+({x}^{3}y-x{y}^{3})\,dy,\right)$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $384$
- $378$
- $0$ (correct)
- $400$
- $360$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left({x}^{2}-{y}^{4}\right)$ and $Q(x,y)=2\left(({x}^{3}y-x{y}^{3}).\right)$ So,

$$
\frac{∂P}{∂y}=2\left(-4{y}^{3},\right)\,\frac{∂Q}{∂x}=2\left(3{x}^{2}y-{y}^{3}.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}({x}^{2}-{y}^{4})\,dx+({x}^{3}y-x{y}^{3})\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}3{x}^{2}y-{y}^{3}-(-4{y}^{3})\,\text{d}A \right)\\  & =2\left({∬}_{D}3{x}^{2}y+3{y}^{3}\,\text{d}A \right)\\  & =2\left({∬}_{D}3y({x}^{2}+{y}^{2})\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$2\left(
Δ\right)=2\left(\{(r,\theta )\,:\,1\le r\le 4,\,0\le \theta \le 2\pi \}.
\right)$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}3y({x}^{2}+{y}^{2})\,\text{d}A \right)& =2\left({\int }_{0}^{2\pi }{\int }_{1}^{4}3\cdot r\operatorname{sin}⁡\theta \cdot ((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }{\int }_{1}^{4}3{r}^{2}\operatorname{sin}⁡\theta \cdot {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }{\int }_{1}^{4}3{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  \right)\\  & =2\left({\int }_{0}^{2\pi }\operatorname{sin}⁡\theta \,\text{d}\theta {\int }_{1}^{4}3{r}^{4}\,\text{d}r \right)\\  & =2\left(\operatorname{cos}⁡\theta \,{|}_{0}^{2\pi }\cdot \frac{3{r}^{5}}{5}\,{|}_{1}^{4} \right)\\  & =2\left((\operatorname{cos}⁡(2\pi )-\operatorname{cos}⁡(0))\cdot (\frac{3(4)^{5}}{5}-\frac{3(1)^{5}}{5}) \right)\\  & =2\left((1-1)\cdot (\frac{3(4)^{5}}{5}-\frac{3(1)^{5}}{5}) \right)\\  & =2\left(0.\right)\end{aligned}
$$

## Raw original q-126938

Parameters: `{"amplitude": 1}`; profile `raw:q-126938`.

![](/media/jake/SSD/EDB/math/images/5c/5ca9f071eaeebb0b31fba99a48ca8f08bd6b4b73588838aad7b5f513c283fd6c.png)

Calculate ${∮}_{∂D}-({x}^{2}y+{y}^{3})\,dx+({x}^{3}+x{y}^{2})\,dy,$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $140\pi $
- $80\pi $
- $100\pi $
- $160\pi $ (correct)
- $120\pi $

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

## Generated historical-evidence amplitude variant q-126938

Parameters: `{"amplitude": 2}`; profile `raw:q-126938`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/c48e6d58e3b95dcaad25d7b0e37cd1165034e4913440bcc588961298f1ad4a58.png)

Calculate $2\left({∮}_{∂D}-({x}^{2}y+{y}^{3})\,dx+({x}^{3}+x{y}^{2})\,dy,\right)$ where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $280 \pi$
- $160 \pi$
- $200 \pi$
- $320 \pi$ (correct)
- $240 \pi$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left(-{x}^{2}y-{y}^{3}\right)$ and $Q(x,y)=2\left({x}^{3}+x{y}^{2}.\right)$ So,

$$
\frac{∂P}{∂y}=2\left(-{x}^{2}-3{y}^{2},\right)\,\frac{∂Q}{∂x}=2\left(3{x}^{2}+{y}^{2}.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}-({x}^{2}y+{y}^{3})\,dx+({x}^{3}+x{y}^{2})\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}3{x}^{2}+{y}^{2}-(-{x}^{2}-3{y}^{2})\,\text{d}A \right)\\  & =2\left({∬}_{D}4{x}^{2}+4{y}^{2}\,\text{d}A \right)\\  & =2\left({∬}_{D}4({x}^{2}+{y}^{2})\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$2\left(
Δ\right)=2\left(\{(r,\theta )\,:\,1\le r\le 3,\,0\le \theta \le 2\pi \}.
\right)$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}4({x}^{2}+{y}^{2})\,\text{d}A \right)& =2\left(4{\int }_{0}^{2\pi }{\int }_{1}^{3}(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left(4{\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left(4{\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta  \right)\\  & =2\left(4{\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r \right)\\  & =2\left(8\pi {\int }_{1}^{2}{r}^{3}\,\text{d}r \right)\\  & =2\left(8\pi \cdot {\frac{1}{4}{r}^{4}|}_{1}^{3} \right)\\  & =2\left(2\pi \cdot ({3}^{4}-{1}^{4}) \right)\\  & =2\left(160\pi .\right)\end{aligned}
$$

## Raw original q-126942

Parameters: `{"amplitude": 1}`; profile `raw:q-126942`.

![](/media/jake/SSD/EDB/math/images/db/dbe6009d42623d3b3cd9f05380159bb0f4b8f22b920c1ef5d4d82b5dbf152d4a.png)

Calculate 
${∮}_{∂D}{y}^{2}(x+1)\,dx+(3{x}^{2}y+2xy)\,dy,$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $24$ (correct)
- $36$
- $42$
- $27$
- $16$

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

## Generated historical-evidence amplitude variant q-126942

Parameters: `{"amplitude": 2}`; profile `raw:q-126942`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/316ce23c75b69bb7cdbf4acdadfd5fe10f4c07cc062e89dfaad2ab6bc7a68d4c.png)

Calculate 
$2\left({∮}_{∂D}{y}^{2}(x+1)\,dx+(3{x}^{2}y+2xy)\,dy,\right)$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $48$ (correct)
- $72$
- $84$
- $54$
- $32$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left({y}^{2}(x+1)\right)$ and $Q(x,y)=2\left(3{x}^{2}y+2xy.\right)$ Therefore,

$$
\frac{∂P}{∂y}=2\left(2y(x+1),\right)\,\frac{∂Q}{∂x}=2\left(6xy+2y.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}{y}^{2}(x+1)\,dx+(3{x}^{2}y+2xy)\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}(6xy+2y)-2y(x+1)\,\text{d}A \right)\\  & =2\left({∬}_{D}4xy\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- $2\left({Δ}_{1}\right)=2\left(\{(x,y)\,:\,0\le x\le 3,-1\le y\le 2\}\right)$ is the region enclosed by the outer curve, and

- $2\left({Δ}_{2}\right)=2\left(\{(x,y)\,:\,1\le x\le 2,0\le y\le 1\}\right)$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}4xy\,\text{d}A \right)& =2\left({∬}_{{Δ}_{1}}4xy\,\text{d}A-{∬}_{{Δ}_{2}}4xy\,\text{d}A \right)\\  & =2\left({\int }_{-1}^{2}{\int }_{0}^{3}4xy\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{1}^{2}4xy\,\text{d}x\,\text{d}y \right)\\  & =2\left({\int }_{0}^{3}2x\,\text{d}x{\int }_{-1}^{2}2y\,\text{d}y-{\int }_{1}^{2}2x\,\text{d}x{\int }_{0}^{1}2y\,\text{d}y \right)\\  & =2\left({x}^{2}\,{|}_{0}^{3}\cdot {y}^{2}\,{|}_{-1}^{2}-{x}^{2}\,{|}_{1}^{2}\cdot {y}^{2}\,{|}_{0}^{1} \right)\\  & =2\left((9-0)\cdot (4-1)-(4-1)\cdot (1-0) \right)\\  & =2\left(9\cdot 3-3\cdot 1 \right)\\  & =2\left(24.\right)\end{aligned}
$$

## Raw original q-126946

Parameters: `{"amplitude": 1}`; profile `raw:q-126946`.

![](/media/jake/SSD/EDB/math/images/9b/9be396fd57559bb77f92d5a0421f3a7cdca577203904e577da0caf5326caac91.png)

Calculate 
${∮}_{∂D}(2{x}^{2}{y}^{4}-x)\,dx+(4{x}^{3}{y}^{3}-{y}^{2})\,dy,$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{3}{4}$
- $0$
- $\frac{2}{3}$
- $-\frac{1}{3}$ (correct)
- $-\frac{4}{3}$

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

## Generated historical-evidence amplitude variant q-126946

Parameters: `{"amplitude": 2}`; profile `raw:q-126946`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/f025b68c3a5175aff6d17d3ae3e4e843455aa07c498cb5c3db03e4436abb75c2.png)

Calculate 
$2\left({∮}_{∂D}(2{x}^{2}{y}^{4}-x)\,dx+(4{x}^{3}{y}^{3}-{y}^{2})\,dy,\right)$
where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{3}{2}$
- $0$
- $\frac{4}{3}$
- $- \frac{2}{3}$ (correct)
- $- \frac{8}{3}$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2\left(2{x}^{2}{y}^{4}-x\right)$ and $Q(x,y)=2\left(4{x}^{3}{y}^{3}-{y}^{2}.\right)$ Therefore,

$$
\frac{∂P}{∂y}=2\left(8{x}^{2}{y}^{3},\right)\,\frac{∂Q}{∂x}=2\left(12{x}^{2}{y}^{3}.
\right)$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}2\left({∮}_{∂D}(2{x}^{2}{y}^{4}-x)\,dx+(4{x}^{3}{y}^{3}-{y}^{2})\,dy \right)& ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =2\left({∬}_{D}12{x}^{2}{y}^{3}-8{x}^{2}{y}^{3}\,\text{d}A \right)\\  & =2\left({∬}_{D}4{x}^{2}{y}^{3}\,\text{d}A.\right)\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- $2\left({Δ}_{1}\right)=2\left(\{(x,y)\,:\,-1\le x\le 2,-2\le y\le 2\}\right)$ is the region enclosed by the outer curve, and

- $2\left({Δ}_{2}\right)=2\left(\{(x,y)\,:\,0\le x\le 1,0\le y\le 1\}\right)$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}2\left({∬}_{D}4{x}^{2}{y}^{3}\,\text{d}A \right)& =2\left({∬}_{{Δ}_{1}}4{x}^{2}{y}^{3}\,\text{d}A-{∬}_{{Δ}_{2}}4{x}^{2}{y}^{3}\,\text{d}A \right)\\  & =2\left({\int }_{-2}^{2}{\int }_{-1}^{2}4{x}^{2}{y}^{3}\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{0}^{1}4{x}^{2}{y}^{3}\,\text{d}x\,\text{d}y \right)\\  & =2\left({\int }_{-1}^{2}{x}^{2}\,\text{d}x{\int }_{-2}^{2}4{y}^{3}\,\text{d}y-{\int }_{0}^{1}{x}^{2}\,\text{d}x{\int }_{0}^{1}4{y}^{3}\,\text{d}y \right)\\  & =2\left(\frac{{x}^{3}}{3}\,{|}_{-1}^{2}\cdot {y}^{4}\,{|}_{-2}^{2}-\frac{{x}^{3}}{3}\,{|}_{0}^{1}\cdot {y}^{4}\,{|}_{0}^{1} \right)\\  & =2\left((\frac{8}{3}-(-\frac{1}{3}))\cdot (16-16)-(\frac{1}{3}-0)\cdot (1-0) \right)\\  & =2\left(3\cdot 0-\frac{1}{3}\cdot 1 \right)\\  & =2\left(-\frac{1}{3}.\right)\end{aligned}
$$

## Generated variant annulus_quadratic 0

Parameters: `{"c": -3, "inner": 3, "outer": 4}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/5674030d7a82bd3ad14e68ebd5e0a3bd4747c1a721e3d0c0b8648c41b5fa73e1.png)

Calculate $\oint_{\partial D}(3 x^{2} y)\,\mathrm dx+(- 3 x y^{2})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- \frac{1011 \pi}{2}$
- $- 74 \pi$
- $- 384 \pi$
- $\frac{525 \pi}{2}$
- $- \frac{525 \pi}{2}$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=3 x^{2} y$ and $Q(x,y)=- 3 x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(3 x^{2} y\right)=\left(3 x^{2}\right)=3 x^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x y^{2}\right)=\left(- 3 y^{2}\right)=- 3 y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=3 x^{2},\qquad\frac{\partial Q}{\partial x}=- 3 y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(3 x^{2} y)\,\mathrm dx+(- 3 x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 3 y^{2}-(3 x^{2})\right)\,\mathrm dA\\ & =\iint_D - 3 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 \left(x^{2} + y^{2}\right)\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}- 3 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =-3\left(\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}r^{3}\,\mathrm d r\right)\\ & =- 6 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 6 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =- 6 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =- 6 \pi\cdot \left(\frac{175}{4}\right)\\ & =- \frac{525 \pi}{2}.\end{aligned}
$$

## Generated variant annulus_quadratic 1

Parameters: `{"c": 1, "inner": 3, "outer": 5}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/b51fc221a1c5552c731d3e275795094e24083d242ed75cfa99f9a05b2bf20b4c.png)

Calculate $\oint_{\partial D}(- x^{2} y)\,\mathrm dx+(x y^{2})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- 272 \pi$
- $272 \pi$ (correct)
- $\frac{196 \pi}{3}$
- $\frac{625 \pi}{2}$
- $353 \pi$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- x^{2} y$ and $Q(x,y)=x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- x^{2} y\right)=\left(- x^{2}\right)=- x^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x y^{2}\right)=\left(y^{2}\right)=y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- x^{2},\qquad\frac{\partial Q}{\partial x}=y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- x^{2} y)\,\mathrm dx+(x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(y^{2}-(- x^{2})\right)\,\mathrm dA\\ & =\iint_D x^{2} + y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D x^{2} + y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{5}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{5}r^{3}\,\mathrm d r\\ & =2 \pi\cdot \int_{3}^{5}r^{3}\,\mathrm d r\\ & =2 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{5}\\ & =2 \pi\cdot (\left(\frac{625}{4}\right)-\left(\frac{81}{4}\right))\\ & =2 \pi\cdot \left(136\right)\\ & =272 \pi.\end{aligned}
$$

## Generated variant annulus_sin2 0

Parameters: `{"c": -3, "inner": 3, "outer": 4}`; profile `blank`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/1fd6034983bef512a19923f99bee68a96e236c01b9c5cd6489a44c20c17927db.png)

Let $\partial R$ be the boundary of the region $R,$ shown above. Use Green's theorem to calculate the following integral:

$\oint_{\partial R}\mathbf F\cdot\mathrm d\mathbf r=\oint_{\partial R}(- 9 x y^{2})\,\mathrm dx+(3 y^{3})\,\mathrm dy=$

{{field-1}}

Field `field-1` (:answer-field.type/blank):
- $0$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates. Holding the other coordinate fixed, we have that $P(x,y)=- 9 x y^{2}$ and $Q(x,y)=3 y^{3}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 9 x y^{2}\right)=\left(- 18 x y\right)=- 18 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(3 y^{3}\right)=\left(0\right)=0.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 18 x y,\qquad\frac{\partial Q}{\partial x}=0.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial R}(- 9 x y^{2})\,\mathrm dx+(3 y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(0-(- 18 x y)\right)\,\mathrm dA\\ & =\iint_D 18 x y\,\mathrm dA.\end{aligned}
$$

But this time, our region $R$ (in polar coordinates) is given by

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 18 x y\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}18(r\cos\theta)(r\sin\theta)r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}9r^3\sin(2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}9r^3\sin(2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =9\left(\int_{0}^{2 \pi}\sin{\left(2 \theta \right)}\,\mathrm d \theta\cdot \int_{3}^{4}r^{3}\,\mathrm d r\right)\\ & =9\left(- \frac{\cos{\left(2 \theta \right)}}{2}\big|_{0}^{2 \pi}\cdot \frac{r^{4}}{4}\big|_{3}^{4}\right)\\ & =9\left((\left(- \frac{1}{2}\right)-\left(- \frac{1}{2}\right))\cdot (\left(64\right)-\left(\frac{81}{4}\right))\right)\\ & =9\cdot \left(0\right)\cdot \left(\frac{175}{4}\right)\\ & =0.\end{aligned}
$$

## Generated variant annulus_sin2 1

Parameters: `{"c": 1, "inner": 3, "outer": 5}`; profile `blank`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/ba34895c53a21c0fcb333220a099a7feabf74e9f837bf0e8531912f8dfe17b3f.png)

Let $\partial R$ be the boundary of the region $R,$ shown above. Use Green's theorem to calculate the following integral:

$\oint_{\partial R}\mathbf F\cdot\mathrm d\mathbf r=\oint_{\partial R}(3 x y^{2})\,\mathrm dx+(- y^{3})\,\mathrm dy=$

{{field-1}}

Field `field-1` (:answer-field.type/blank):
- $0$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates. Holding the other coordinate fixed, we have that $P(x,y)=3 x y^{2}$ and $Q(x,y)=- y^{3}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(3 x y^{2}\right)=\left(6 x y\right)=6 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- y^{3}\right)=\left(0\right)=0.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=6 x y,\qquad\frac{\partial Q}{\partial x}=0.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial R}(3 x y^{2})\,\mathrm dx+(- y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(0-(6 x y)\right)\,\mathrm dA\\ & =\iint_D - 6 x y\,\mathrm dA.\end{aligned}
$$

But this time, our region $R$ (in polar coordinates) is given by

$$\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 6 x y\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{5}-6(r\cos\theta)(r\sin\theta)r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}-3r^3\sin(2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}-3r^3\sin(2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =-3\left(\int_{0}^{2 \pi}\sin{\left(2 \theta \right)}\,\mathrm d \theta\cdot \int_{3}^{5}r^{3}\,\mathrm d r\right)\\ & =-3\left(- \frac{\cos{\left(2 \theta \right)}}{2}\big|_{0}^{2 \pi}\cdot \frac{r^{4}}{4}\big|_{3}^{5}\right)\\ & =-3\left((\left(- \frac{1}{2}\right)-\left(- \frac{1}{2}\right))\cdot (\left(\frac{625}{4}\right)-\left(\frac{81}{4}\right))\right)\\ & =-3\cdot \left(0\right)\cdot \left(136\right)\\ & =0.\end{aligned}
$$

## Generated variant annulus_fourth 0

Parameters: `{"c": -3, "inner": 3, "outer": 4}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/22bbc13eebb2a40383bb6ebc19507f9a83eecaceb2340a92013d165d279bd13c.png)

Calculate $\oint_{\partial D}(3 x^{4} y + x^{2} y^{3})\,\mathrm dx+(- x^{3} y^{2} - 3 x y^{4})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- 4825 \pi$
- $- \frac{4686 \pi}{5}$
- $- 4096 \pi$
- $3367 \pi$
- $- 3367 \pi$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=3 x^{4} y + x^{2} y^{3}$ and $Q(x,y)=- x^{3} y^{2} - 3 x y^{4}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(3 x^{4} y + x^{2} y^{3}\right)=\left(3 x^{4}\right)+\left(3 x^{2} y^{2}\right)=3 x^{4} + 3 x^{2} y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- x^{3} y^{2} - 3 x y^{4}\right)=\left(- 3 y^{4}\right)+\left(- 3 x^{2} y^{2}\right)=- 3 x^{2} y^{2} - 3 y^{4}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=3 x^{4} + 3 x^{2} y^{2},\qquad\frac{\partial Q}{\partial x}=- 3 x^{2} y^{2} - 3 y^{4}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(3 x^{4} y + x^{2} y^{3})\,\mathrm dx+(- x^{3} y^{2} - 3 x y^{4})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 3 x^{2} y^{2} - 3 y^{4}-(3 x^{4} + 3 x^{2} y^{2})\right)\,\mathrm dA\\ & =\iint_D(- 3 x^{4} - 6 x^{2} y^{2} - 3 y^{4})\,\mathrm dA\\ & =\iint_D - 3 \left(x^{2} + y^{2}\right)^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 \left(x^{2} + y^{2}\right)^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(((r\cos\theta)^2+(r\sin\theta)^2)^2\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(r^{4}(\cos^2\theta+\sin^2\theta)^2\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}- 3 r^{5}\,\mathrm d r\,\mathrm d \theta\\ & =-3\left(\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}r^{5}\,\mathrm d r\right)\\ & =- 6 \pi\cdot \int_{3}^{4}r^{5}\,\mathrm d r\\ & =- 6 \pi\cdot \frac{r^{6}}{6}\big|_{3}^{4}\\ & =- 6 \pi\cdot (\left(\frac{2048}{3}\right)-\left(\frac{243}{2}\right))\\ & =- 6 \pi\cdot \left(\frac{3367}{6}\right)\\ & =- 3367 \pi.\end{aligned}
$$

## Generated variant annulus_fourth 1

Parameters: `{"c": 1, "inner": 3, "outer": 5}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/5d7977309edbabfedd2a151de487cf1f5e1ae8caed2147c9be4425d24c7c095a.png)

Calculate $\oint_{\partial D}(- x^{4} y - \frac{x^{2} y^{3}}{3})\,\mathrm dx+(\frac{x^{3} y^{2}}{3} + x y^{4})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- \frac{14896 \pi}{3}$
- $\frac{14896 \pi}{3}$ (correct)
- $\frac{5764 \pi}{5}$
- $\frac{15625 \pi}{3}$
- $\frac{16354 \pi}{3}$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- x^{4} y - \frac{x^{2} y^{3}}{3}$ and $Q(x,y)=\frac{x^{3} y^{2}}{3} + x y^{4}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- x^{4} y - \frac{x^{2} y^{3}}{3}\right)=\left(- x^{4}\right)+\left(- x^{2} y^{2}\right)=- x^{4} - x^{2} y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(\frac{x^{3} y^{2}}{3} + x y^{4}\right)=\left(y^{4}\right)+\left(x^{2} y^{2}\right)=x^{2} y^{2} + y^{4}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- x^{4} - x^{2} y^{2},\qquad\frac{\partial Q}{\partial x}=x^{2} y^{2} + y^{4}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- x^{4} y - \frac{x^{2} y^{3}}{3})\,\mathrm dx+(\frac{x^{3} y^{2}}{3} + x y^{4})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(x^{2} y^{2} + y^{4}-(- x^{4} - x^{2} y^{2})\right)\,\mathrm dA\\ & =\iint_D(x^{4} + 2 x^{2} y^{2} + y^{4})\,\mathrm dA\\ & =\iint_D \left(x^{2} + y^{2}\right)^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D \left(x^{2} + y^{2}\right)^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{5}((r\cos\theta)^2+(r\sin\theta)^2)^2\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}r^{4}(\cos^2\theta+\sin^2\theta)^2\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}r^{5}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{5}r^{5}\,\mathrm d r\\ & =2 \pi\cdot \int_{3}^{5}r^{5}\,\mathrm d r\\ & =2 \pi\cdot \frac{r^{6}}{6}\big|_{3}^{5}\\ & =2 \pi\cdot (\left(\frac{15625}{6}\right)-\left(\frac{243}{2}\right))\\ & =2 \pi\cdot \left(\frac{7448}{3}\right)\\ & =\frac{14896 \pi}{3}.\end{aligned}
$$

## Generated variant annulus_negative 0

Parameters: `{"c": -3, "inner": 3, "outer": 4}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/719cdf5de58766e1e2e96384c00f325f48db31cf617ab4b332329cb257596e91.png)

Calculate $\oint_{\partial D}(- y^{3} - 3 \cos{\left(x \right)})\,\mathrm dx+(x^{3} - 3 \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{1011 \pi}{2}$
- $74 \pi$
- $384 \pi$
- $- \frac{525 \pi}{2}$
- $\frac{525 \pi}{2}$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- y^{3} - 3 \cos{\left(x \right)}$ and $Q(x,y)=x^{3} - 3 \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- y^{3} - 3 \cos{\left(x \right)}\right)=\left(- 3 y^{2}\right)+\left(0\right)=- 3 y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{3} - 3 \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)}\right)=\left(3 x^{2}\right)+\left(0\right)=3 x^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 3 y^{2},\qquad\frac{\partial Q}{\partial x}=3 x^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- y^{3} - 3 \cos{\left(x \right)})\,\mathrm dx+(x^{3} - 3 \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(3 x^{2}-(- 3 y^{2})\right)\,\mathrm dA\\ & =\iint_D(3 x^{2} + 3 y^{2})\,\mathrm dA\\ & =\iint_D 3 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 3 \left(x^{2} + y^{2}\right)\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}3\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}3\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}3 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =3\left(\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}r^{3}\,\mathrm d r\right)\\ & =6 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =6 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =6 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =6 \pi\cdot \left(\frac{175}{4}\right)\\ & =\frac{525 \pi}{2}.\end{aligned}
$$

## Generated variant annulus_negative 1

Parameters: `{"c": 1, "inner": 3, "outer": 5}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/b404b24976bbb638c3d47fac6132c9e7d507d742a5d1f7121b87264cb5223303.png)

Calculate $\oint_{\partial D}(\frac{y^{3}}{3} + \cos{\left(x \right)})\,\mathrm dx+(- \frac{x^{3}}{3} + \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $272 \pi$
- $- 272 \pi$ (correct)
- $- \frac{196 \pi}{3}$
- $- \frac{625 \pi}{2}$
- $- 353 \pi$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=\frac{y^{3}}{3} + \cos{\left(x \right)}$ and $Q(x,y)=- \frac{x^{3}}{3} + \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(\frac{y^{3}}{3} + \cos{\left(x \right)}\right)=\left(y^{2}\right)+\left(0\right)=y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- \frac{x^{3}}{3} + \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)}\right)=\left(- x^{2}\right)+\left(0\right)=- x^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=y^{2},\qquad\frac{\partial Q}{\partial x}=- x^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(\frac{y^{3}}{3} + \cos{\left(x \right)})\,\mathrm dx+(- \frac{x^{3}}{3} + \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- x^{2}-(y^{2})\right)\,\mathrm dA\\ & =\iint_D(- x^{2} - y^{2})\,\mathrm dA\\ & =\iint_D - x^{2} - y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - x^{2} - y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{5}-1\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}-1\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}- r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =-1\left(\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{5}r^{3}\,\mathrm d r\right)\\ & =- 2 \pi\cdot \int_{3}^{5}r^{3}\,\mathrm d r\\ & =- 2 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{5}\\ & =- 2 \pi\cdot (\left(\frac{625}{4}\right)-\left(\frac{81}{4}\right))\\ & =- 2 \pi\cdot \left(136\right)\\ & =- 272 \pi.\end{aligned}
$$

## Generated variant annulus_odd 0

Parameters: `{"c": -3, "inner": 3, "outer": 4}`; profile `angular`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/89e569c414e2d495cc4d731b3f49f277639c51685832f87f5f26013661e41c67.png)

Calculate $\oint_{\partial D}(- 3 x^{2} + 3 y^{4})\,\mathrm dx+(- 3 x^{3} y + 3 x y^{3})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- \frac{14058 \pi}{5}$
- $- \frac{7029 \pi}{5}$
- $\frac{14058}{5}$
- $- \frac{14058}{5}$
- $0$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 x^{2} + 3 y^{4}$ and $Q(x,y)=- 3 x^{3} y + 3 x y^{3}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 x^{2} + 3 y^{4}\right)=\left(0\right)+\left(12 y^{3}\right)=12 y^{3}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x^{3} y + 3 x y^{3}\right)=\left(- 9 x^{2} y\right)+\left(3 y^{3}\right)=- 9 x^{2} y + 3 y^{3}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=12 y^{3},\qquad\frac{\partial Q}{\partial x}=- 9 x^{2} y + 3 y^{3}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 x^{2} + 3 y^{4})\,\mathrm dx+(- 3 x^{3} y + 3 x y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 9 x^{2} y + 3 y^{3}-(12 y^{3})\right)\,\mathrm dA\\ & =\iint_D(- 9 x^{2} y - 9 y^{3})\,\mathrm dA\\ & =\iint_D - 9 y \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 9 y \left(x^{2} + y^{2}\right)\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}-9\cdot r\sin\theta\cdot ((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-9r^2\sin\theta\cdot r^2(\cos^2\theta+\sin^2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}- 9 r^{4}\sin\theta\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\sin{\left(\theta \right)}\,\mathrm d \theta\cdot \int_{3}^{4}- 9 r^{4}\,\mathrm d r\\ & =- \cos{\left(\theta \right)}\big|_{0}^{2 \pi}\cdot - \frac{9 r^{5}}{5}\big|_{3}^{4}\\ & =(\left(-1\right)-\left(-1\right))\cdot (\left(- \frac{9216}{5}\right)-\left(- \frac{2187}{5}\right))\\ & =1\cdot \left(0\right)\cdot \left(- \frac{7029}{5}\right)\\ & =0.\end{aligned}
$$

## Generated variant annulus_odd 1

Parameters: `{"c": 1, "inner": 3, "outer": 5}`; profile `angular`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/cb216ce0afb62ed137a4fd1ec02e70a12de34d7068a64e1ba41efbb2a32999a2.png)

Calculate $\oint_{\partial D}(x^{2} - y^{4})\,\mathrm dx+(x^{3} y - x y^{3})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{17292}{5}$
- $0$ (correct)
- $\frac{8646 \pi}{5}$
- $- \frac{17292}{5}$
- $\frac{17292 \pi}{5}$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x^{2} - y^{4}$ and $Q(x,y)=x^{3} y - x y^{3}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x^{2} - y^{4}\right)=\left(0\right)+\left(- 4 y^{3}\right)=- 4 y^{3}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{3} y - x y^{3}\right)=\left(3 x^{2} y\right)+\left(- y^{3}\right)=3 x^{2} y - y^{3}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 4 y^{3},\qquad\frac{\partial Q}{\partial x}=3 x^{2} y - y^{3}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x^{2} - y^{4})\,\mathrm dx+(x^{3} y - x y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(3 x^{2} y - y^{3}-(- 4 y^{3})\right)\,\mathrm dA\\ & =\iint_D(3 x^{2} y + 3 y^{3})\,\mathrm dA\\ & =\iint_D 3 y \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 3 y \left(x^{2} + y^{2}\right)\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{5}3\cdot r\sin\theta\cdot ((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}3r^2\sin\theta\cdot r^2(\cos^2\theta+\sin^2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}3 r^{4}\sin\theta\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\sin{\left(\theta \right)}\,\mathrm d \theta\cdot \int_{3}^{5}3 r^{4}\,\mathrm d r\\ & =- \cos{\left(\theta \right)}\big|_{0}^{2 \pi}\cdot \frac{3 r^{5}}{5}\big|_{3}^{5}\\ & =(\left(-1\right)-\left(-1\right))\cdot (\left(1875\right)-\left(\frac{729}{5}\right))\\ & =1\cdot \left(0\right)\cdot \left(\frac{8646}{5}\right)\\ & =0.\end{aligned}
$$

## Generated variant annulus_four 0

Parameters: `{"c": -3, "inner": 3, "outer": 4}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/912b8246330b1561fca026dda1aa212b60637a6664b3751396a1768c4d45d3bc.png)

Calculate $\oint_{\partial D}(3 x^{2} y + 3 y^{3})\,\mathrm dx+(- 3 x^{3} - 3 x y^{2})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- 2022 \pi$
- $- 296 \pi$
- $- 1536 \pi$
- $1050 \pi$
- $- 1050 \pi$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=3 x^{2} y + 3 y^{3}$ and $Q(x,y)=- 3 x^{3} - 3 x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(3 x^{2} y + 3 y^{3}\right)=\left(9 y^{2}\right)+\left(3 x^{2}\right)=3 x^{2} + 9 y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x^{3} - 3 x y^{2}\right)=\left(- 9 x^{2}\right)+\left(- 3 y^{2}\right)=- 9 x^{2} - 3 y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=3 x^{2} + 9 y^{2},\qquad\frac{\partial Q}{\partial x}=- 9 x^{2} - 3 y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(3 x^{2} y + 3 y^{3})\,\mathrm dx+(- 3 x^{3} - 3 x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 9 x^{2} - 3 y^{2}-(3 x^{2} + 9 y^{2})\right)\,\mathrm dA\\ & =\iint_D(- 12 x^{2} - 12 y^{2})\,\mathrm dA\\ & =\iint_D - 12 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 12 \left(x^{2} + y^{2}\right)\,\mathrm dA & =-12\left(\int_{0}^{2 \pi}\int_{3}^{4}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\right)\\ & =-12\left(\int_{0}^{2 \pi}\int_{3}^{4}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\right)\\ & =-12\left(\int_{0}^{2 \pi}\int_{3}^{4}r^{3}\,\mathrm d r\,\mathrm d \theta\right)\\ & =-12\left(\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}r^{3}\,\mathrm d r\right)\\ & =- 24 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 24 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =- 24 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =- 24 \pi\cdot \left(\frac{175}{4}\right)\\ & =- 1050 \pi.\end{aligned}
$$

## Generated variant annulus_four 1

Parameters: `{"c": 1, "inner": 3, "outer": 5}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/40f5e61c3297a50d2ea5cb5c2022bc30e8d6c6069430aa268ceee2521d9ecefa.png)

Calculate $\oint_{\partial D}(- x^{2} y - y^{3})\,\mathrm dx+(x^{3} + x y^{2})\,\mathrm dy$, where $D$ is the annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- 1088 \pi$
- $1088 \pi$ (correct)
- $\frac{784 \pi}{3}$
- $1250 \pi$
- $1412 \pi$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- x^{2} y - y^{3}$ and $Q(x,y)=x^{3} + x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- x^{2} y - y^{3}\right)=\left(- 3 y^{2}\right)+\left(- x^{2}\right)=- x^{2} - 3 y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{3} + x y^{2}\right)=\left(3 x^{2}\right)+\left(y^{2}\right)=3 x^{2} + y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- x^{2} - 3 y^{2},\qquad\frac{\partial Q}{\partial x}=3 x^{2} + y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- x^{2} y - y^{3})\,\mathrm dx+(x^{3} + x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(3 x^{2} + y^{2}-(- x^{2} - 3 y^{2})\right)\,\mathrm dA\\ & =\iint_D(4 x^{2} + 4 y^{2})\,\mathrm dA\\ & =\iint_D 4 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 4 \left(x^{2} + y^{2}\right)\,\mathrm dA & =4\left(\int_{0}^{2 \pi}\int_{3}^{5}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\right)\\ & =4\left(\int_{0}^{2 \pi}\int_{3}^{5}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\right)\\ & =4\left(\int_{0}^{2 \pi}\int_{3}^{5}r^{3}\,\mathrm d r\,\mathrm d \theta\right)\\ & =4\left(\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{5}r^{3}\,\mathrm d r\right)\\ & =8 \pi\cdot \int_{3}^{5}r^{3}\,\mathrm d r\\ & =8 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{5}\\ & =8 \pi\cdot (\left(\frac{625}{4}\right)-\left(\frac{81}{4}\right))\\ & =8 \pi\cdot \left(136\right)\\ & =1088 \pi.\end{aligned}
$$

## Generated variant rectangle_y2 0

Parameters: `{"c": -3, "hole": [1, 3, -2, 1], "outer": [-3, 5, -4, 2]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/cf3302cb14e255673be2b00f6534497aa2e5b7cae1013baebd4e4913e599ee14.png)

Calculate $\oint_{\partial D}(- 3 x y^{2})\,\mathrm dx+(- 3 x^{2} y - 3 x y^{2})\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $558$
- $-306$
- $-576$
- $-594$
- $-558$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 x y^{2}$ and $Q(x,y)=- 3 x^{2} y - 3 x y^{2}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 x y^{2}\right)=\left(- 6 x y\right)=- 6 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x^{2} y - 3 x y^{2}\right)=\left(- 3 y^{2}\right)+\left(- 6 x y\right)=- 6 x y - 3 y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 6 x y,\qquad\frac{\partial Q}{\partial x}=- 6 x y - 3 y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 x y^{2})\,\mathrm dx+(- 3 x^{2} y - 3 x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 6 x y - 3 y^{2}-(- 6 x y)\right)\,\mathrm dA\\ & =\iint_D - 3 y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-3\le x\le 5,-4\le y\le 2\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 3,-2\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 y^{2}\,\mathrm dA & =\iint_{\Delta_1}- 3 y^{2}\,\mathrm dA-\iint_{\Delta_2}- 3 y^{2}\,\mathrm dA\\ & =\int_{-4}^{2}\int_{-3}^{5}- 3 y^{2}\,\mathrm d x\,\mathrm d y-\int_{-2}^{1}\int_{1}^{3}- 3 y^{2}\,\mathrm d x\,\mathrm d y\\ & =\int_{-3}^{5}-3\,\mathrm d x\cdot \int_{-4}^{2}y^{2}\,\mathrm d y-\int_{1}^{3}-3\,\mathrm d x\cdot \int_{-2}^{1}y^{2}\,\mathrm d y\\ & =- 3 x\big|_{-3}^{5}\cdot \frac{y^{3}}{3}\big|_{-4}^{2}-- 3 x\big|_{1}^{3}\cdot \frac{y^{3}}{3}\big|_{-2}^{1}\\ & =(\left(-15\right)-\left(9\right))\cdot (\left(\frac{8}{3}\right)-\left(- \frac{64}{3}\right))-(\left(-9\right)-\left(-3\right))\cdot (\left(\frac{1}{3}\right)-\left(- \frac{8}{3}\right))\\ & =\left(-24\right)\cdot \left(24\right)-\left(-6\right)\cdot \left(3\right)\\ & =-558.\end{aligned}
$$

## Generated variant rectangle_y2 1

Parameters: `{"c": 1, "hole": [1, 3, 0, 3], "outer": [-3, 5, -2, 4]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/82d12bb8cd2fdb27f7abf018677dcdcc5cc4b59f85c0b2979721e4042ee81a38.png)

Calculate $\oint_{\partial D}(x y^{2})\,\mathrm dx+(x^{2} y + x y^{2})\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $210$
- $174$ (correct)
- $234$
- $192$
- $-174$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x y^{2}$ and $Q(x,y)=x^{2} y + x y^{2}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x y^{2}\right)=\left(2 x y\right)=2 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{2} y + x y^{2}\right)=\left(y^{2}\right)+\left(2 x y\right)=2 x y + y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=2 x y,\qquad\frac{\partial Q}{\partial x}=2 x y + y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x y^{2})\,\mathrm dx+(x^{2} y + x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(2 x y + y^{2}-(2 x y)\right)\,\mathrm dA\\ & =\iint_D y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-3\le x\le 5,-2\le y\le 4\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 3,0\le y\le 3\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D y^{2}\,\mathrm dA & =\iint_{\Delta_1}y^{2}\,\mathrm dA-\iint_{\Delta_2}y^{2}\,\mathrm dA\\ & =\int_{-2}^{4}\int_{-3}^{5}y^{2}\,\mathrm d x\,\mathrm d y-\int_{0}^{3}\int_{1}^{3}y^{2}\,\mathrm d x\,\mathrm d y\\ & =\int_{-3}^{5}\,\mathrm d x\cdot \int_{-2}^{4}y^{2}\,\mathrm d y-\int_{1}^{3}\,\mathrm d x\cdot \int_{0}^{3}y^{2}\,\mathrm d y\\ & =x\big|_{-3}^{5}\cdot \frac{y^{3}}{3}\big|_{-2}^{4}-x\big|_{1}^{3}\cdot \frac{y^{3}}{3}\big|_{0}^{3}\\ & =(\left(5\right)-\left(-3\right))\cdot (\left(\frac{64}{3}\right)-\left(- \frac{8}{3}\right))-(\left(3\right)-\left(1\right))\cdot (\left(9\right)-\left(0\right))\\ & =\left(8\right)\cdot \left(24\right)-\left(2\right)\cdot \left(9\right)\\ & =174.\end{aligned}
$$

## Generated variant rectangle_x3y2 0

Parameters: `{"c": -3, "hole": [1, 2, -1, 0], "outer": [-1, 3, -2, 1]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/1f9a46e175bc13ea8ce93c76cd8eaa8799dc28a93dc892b6ca25f9b16f390762.png)

Calculate $\oint_{\partial D}(- 3 x^{3} y^{3} - 3 x)\,\mathrm dx+(- 3 x^{4} y^{2} + 3 y)\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{705}{4}$
- $-705$
- $-180$
- $- \frac{735}{4}$
- $- \frac{705}{4}$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 x^{3} y^{3} - 3 x$ and $Q(x,y)=- 3 x^{4} y^{2} + 3 y.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 x^{3} y^{3} - 3 x\right)=\left(0\right)+\left(- 9 x^{3} y^{2}\right)=- 9 x^{3} y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x^{4} y^{2} + 3 y\right)=\left(0\right)+\left(- 12 x^{3} y^{2}\right)=- 12 x^{3} y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 9 x^{3} y^{2},\qquad\frac{\partial Q}{\partial x}=- 12 x^{3} y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 x^{3} y^{3} - 3 x)\,\mathrm dx+(- 3 x^{4} y^{2} + 3 y)\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 12 x^{3} y^{2}-(- 9 x^{3} y^{2})\right)\,\mathrm dA\\ & =\iint_D - 3 x^{3} y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-1\le x\le 3,-2\le y\le 1\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 2,-1\le y\le 0\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 x^{3} y^{2}\,\mathrm dA & =\iint_{\Delta_1}- 3 x^{3} y^{2}\,\mathrm dA-\iint_{\Delta_2}- 3 x^{3} y^{2}\,\mathrm dA\\ & =\int_{-2}^{1}\int_{-1}^{3}- 3 x^{3} y^{2}\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{1}^{2}- 3 x^{3} y^{2}\,\mathrm d x\,\mathrm d y\\ & =\int_{-1}^{3}- 3 x^{3}\,\mathrm d x\cdot \int_{-2}^{1}y^{2}\,\mathrm d y-\int_{1}^{2}- 3 x^{3}\,\mathrm d x\cdot \int_{-1}^{0}y^{2}\,\mathrm d y\\ & =- \frac{3 x^{4}}{4}\big|_{-1}^{3}\cdot \frac{y^{3}}{3}\big|_{-2}^{1}-- \frac{3 x^{4}}{4}\big|_{1}^{2}\cdot \frac{y^{3}}{3}\big|_{-1}^{0}\\ & =(\left(- \frac{243}{4}\right)-\left(- \frac{3}{4}\right))\cdot (\left(\frac{1}{3}\right)-\left(- \frac{8}{3}\right))-(\left(-12\right)-\left(- \frac{3}{4}\right))\cdot (\left(0\right)-\left(- \frac{1}{3}\right))\\ & =\left(-60\right)\cdot \left(3\right)-\left(- \frac{45}{4}\right)\cdot \left(\frac{1}{3}\right)\\ & =- \frac{705}{4}.\end{aligned}
$$

## Generated variant rectangle_x3y2 1

Parameters: `{"c": 1, "hole": [1, 2, 1, 2], "outer": [-1, 3, 0, 3]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/8530c96fae6c16ce8b658fde560abf213dace198f9ed04724e6fda20290da646.png)

Calculate $\oint_{\partial D}(x^{3} y^{3} + x)\,\mathrm dx+(x^{4} y^{2} - y)\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $\frac{755}{4}$
- $\frac{685}{4}$ (correct)
- $685$
- $180$
- $- \frac{685}{4}$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x^{3} y^{3} + x$ and $Q(x,y)=x^{4} y^{2} - y.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x^{3} y^{3} + x\right)=\left(0\right)+\left(3 x^{3} y^{2}\right)=3 x^{3} y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{4} y^{2} - y\right)=\left(0\right)+\left(4 x^{3} y^{2}\right)=4 x^{3} y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=3 x^{3} y^{2},\qquad\frac{\partial Q}{\partial x}=4 x^{3} y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x^{3} y^{3} + x)\,\mathrm dx+(x^{4} y^{2} - y)\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(4 x^{3} y^{2}-(3 x^{3} y^{2})\right)\,\mathrm dA\\ & =\iint_D x^{3} y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-1\le x\le 3,0\le y\le 3\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 2,1\le y\le 2\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D x^{3} y^{2}\,\mathrm dA & =\iint_{\Delta_1}x^{3} y^{2}\,\mathrm dA-\iint_{\Delta_2}x^{3} y^{2}\,\mathrm dA\\ & =\int_{0}^{3}\int_{-1}^{3}x^{3} y^{2}\,\mathrm d x\,\mathrm d y-\int_{1}^{2}\int_{1}^{2}x^{3} y^{2}\,\mathrm d x\,\mathrm d y\\ & =\int_{-1}^{3}x^{3}\,\mathrm d x\cdot \int_{0}^{3}y^{2}\,\mathrm d y-\int_{1}^{2}x^{3}\,\mathrm d x\cdot \int_{1}^{2}y^{2}\,\mathrm d y\\ & =\frac{x^{4}}{4}\big|_{-1}^{3}\cdot \frac{y^{3}}{3}\big|_{0}^{3}-\frac{x^{4}}{4}\big|_{1}^{2}\cdot \frac{y^{3}}{3}\big|_{1}^{2}\\ & =(\left(\frac{81}{4}\right)-\left(\frac{1}{4}\right))\cdot (\left(9\right)-\left(0\right))-(\left(4\right)-\left(\frac{1}{4}\right))\cdot (\left(\frac{8}{3}\right)-\left(\frac{1}{3}\right))\\ & =\left(20\right)\cdot \left(9\right)-\left(\frac{15}{4}\right)\cdot \left(\frac{7}{3}\right)\\ & =\frac{685}{4}.\end{aligned}
$$

## Generated variant rectangle_xy 0

Parameters: `{"c": -3, "hole": [0, 2, -1, 0], "outer": [-1, 3, -2, 1]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/13e01534f15979442e09d179c4b9b049438bfbae753fed1fd121509551b9020d.png)

Calculate $\oint_{\partial D}(- 3 x^{3} - 3 x y^{2})\,\mathrm dx+(- 6 x^{2} y + 3 y^{3})\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $-30$
- $60$
- $36$
- $42$
- $30$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 x^{3} - 3 x y^{2}$ and $Q(x,y)=- 6 x^{2} y + 3 y^{3}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 x^{3} - 3 x y^{2}\right)=\left(0\right)+\left(- 6 x y\right)=- 6 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 6 x^{2} y + 3 y^{3}\right)=\left(0\right)+\left(- 12 x y\right)=- 12 x y.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 6 x y,\qquad\frac{\partial Q}{\partial x}=- 12 x y.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 x^{3} - 3 x y^{2})\,\mathrm dx+(- 6 x^{2} y + 3 y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 12 x y-(- 6 x y)\right)\,\mathrm dA\\ & =\iint_D - 6 x y\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-1\le x\le 3,-2\le y\le 1\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):0\le x\le 2,-1\le y\le 0\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 6 x y\,\mathrm dA & =\iint_{\Delta_1}- 6 x y\,\mathrm dA-\iint_{\Delta_2}- 6 x y\,\mathrm dA\\ & =\int_{-2}^{1}\int_{-1}^{3}- 6 x y\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{0}^{2}- 6 x y\,\mathrm d x\,\mathrm d y\\ & =\int_{-1}^{3}- 6 x\,\mathrm d x\cdot \int_{-2}^{1}y\,\mathrm d y-\int_{0}^{2}- 6 x\,\mathrm d x\cdot \int_{-1}^{0}y\,\mathrm d y\\ & =- 3 x^{2}\big|_{-1}^{3}\cdot \frac{y^{2}}{2}\big|_{-2}^{1}-- 3 x^{2}\big|_{0}^{2}\cdot \frac{y^{2}}{2}\big|_{-1}^{0}\\ & =(\left(-27\right)-\left(-3\right))\cdot (\left(\frac{1}{2}\right)-\left(2\right))-(\left(-12\right)-\left(0\right))\cdot (\left(0\right)-\left(\frac{1}{2}\right))\\ & =\left(-24\right)\cdot \left(- \frac{3}{2}\right)-\left(-12\right)\cdot \left(- \frac{1}{2}\right)\\ & =30.\end{aligned}
$$

## Generated variant rectangle_xy 1

Parameters: `{"c": 1, "hole": [0, 2, 1, 2], "outer": [-1, 3, 0, 3]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/bca1dcda2f6923f7219de2005b09c2b052923cc402cb693074e55f0864d88a10.png)

Calculate $\oint_{\partial D}(x^{3} + x y^{2})\,\mathrm dx+(2 x^{2} y - y^{3})\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $42$
- $30$ (correct)
- $60$
- $36$
- $-30$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x^{3} + x y^{2}$ and $Q(x,y)=2 x^{2} y - y^{3}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x^{3} + x y^{2}\right)=\left(0\right)+\left(2 x y\right)=2 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(2 x^{2} y - y^{3}\right)=\left(0\right)+\left(4 x y\right)=4 x y.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=2 x y,\qquad\frac{\partial Q}{\partial x}=4 x y.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x^{3} + x y^{2})\,\mathrm dx+(2 x^{2} y - y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(4 x y-(2 x y)\right)\,\mathrm dA\\ & =\iint_D 2 x y\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-1\le x\le 3,0\le y\le 3\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):0\le x\le 2,1\le y\le 2\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 2 x y\,\mathrm dA & =\iint_{\Delta_1}2 x y\,\mathrm dA-\iint_{\Delta_2}2 x y\,\mathrm dA\\ & =\int_{0}^{3}\int_{-1}^{3}2 x y\,\mathrm d x\,\mathrm d y-\int_{1}^{2}\int_{0}^{2}2 x y\,\mathrm d x\,\mathrm d y\\ & =\int_{-1}^{3}2 x\,\mathrm d x\cdot \int_{0}^{3}y\,\mathrm d y-\int_{0}^{2}2 x\,\mathrm d x\cdot \int_{1}^{2}y\,\mathrm d y\\ & =x^{2}\big|_{-1}^{3}\cdot \frac{y^{2}}{2}\big|_{0}^{3}-x^{2}\big|_{0}^{2}\cdot \frac{y^{2}}{2}\big|_{1}^{2}\\ & =(\left(9\right)-\left(1\right))\cdot (\left(\frac{9}{2}\right)-\left(0\right))-(\left(4\right)-\left(0\right))\cdot (\left(2\right)-\left(\frac{1}{2}\right))\\ & =\left(8\right)\cdot \left(\frac{9}{2}\right)-\left(4\right)\cdot \left(\frac{3}{2}\right)\\ & =30.\end{aligned}
$$

## Generated variant rectangle_shift 0

Parameters: `{"c": -3, "hole": [2, 3, -1, 0], "outer": [1, 4, -2, 1]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/abaaacb21e119430e55c1a70e417fc8c8d542facd821a51887570e91f9fd1a04.png)

Calculate $\oint_{\partial D}(- 3 y^{2} \left(x + 1\right))\,\mathrm dx+(- 9 x^{2} y - 6 x y)\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $-120$
- $204$
- $135$
- $150$
- $120$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 y^{2} \left(x + 1\right)$ and $Q(x,y)=- 9 x^{2} y - 6 x y.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 y^{2} \left(x + 1\right)\right)=\left(- 6 y \left(x + 1\right)\right)=- 6 y \left(x + 1\right)\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 9 x^{2} y - 6 x y\right)=\left(- 6 y\right)+\left(- 18 x y\right)=- 18 x y - 6 y.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 6 y \left(x + 1\right),\qquad\frac{\partial Q}{\partial x}=- 18 x y - 6 y.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 y^{2} \left(x + 1\right))\,\mathrm dx+(- 9 x^{2} y - 6 x y)\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 18 x y - 6 y-(- 6 y \left(x + 1\right))\right)\,\mathrm dA\\ & =\iint_D - 12 x y\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):1\le x\le 4,-2\le y\le 1\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):2\le x\le 3,-1\le y\le 0\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 12 x y\,\mathrm dA & =\iint_{\Delta_1}- 12 x y\,\mathrm dA-\iint_{\Delta_2}- 12 x y\,\mathrm dA\\ & =\int_{-2}^{1}\int_{1}^{4}- 12 x y\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{2}^{3}- 12 x y\,\mathrm d x\,\mathrm d y\\ & =\int_{1}^{4}- 6 x\,\mathrm d x\cdot \int_{-2}^{1}2 y\,\mathrm d y-\int_{2}^{3}- 6 x\,\mathrm d x\cdot \int_{-1}^{0}2 y\,\mathrm d y\\ & =- 3 x^{2}\big|_{1}^{4}\cdot y^{2}\big|_{-2}^{1}-- 3 x^{2}\big|_{2}^{3}\cdot y^{2}\big|_{-1}^{0}\\ & =(\left(-48\right)-\left(-3\right))\cdot (\left(1\right)-\left(4\right))-(\left(-27\right)-\left(-12\right))\cdot (\left(0\right)-\left(1\right))\\ & =\left(-45\right)\cdot \left(-3\right)-\left(-15\right)\cdot \left(-1\right)\\ & =120.\end{aligned}
$$

## Generated variant rectangle_shift 1

Parameters: `{"c": 1, "hole": [2, 3, 1, 2], "outer": [1, 4, 0, 3]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/3d83f7978a72d23bc3ecd2777d24e3615c4378c09de6290a9c1ae41f7ee1341d.png)

Calculate $\oint_{\partial D}(y^{2} \left(x + 1\right))\,\mathrm dx+(3 x^{2} y + 2 x y)\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $150$
- $120$ (correct)
- $204$
- $135$
- $-120$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=y^{2} \left(x + 1\right)$ and $Q(x,y)=3 x^{2} y + 2 x y.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(y^{2} \left(x + 1\right)\right)=\left(2 y \left(x + 1\right)\right)=2 y \left(x + 1\right)\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(3 x^{2} y + 2 x y\right)=\left(2 y\right)+\left(6 x y\right)=6 x y + 2 y.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=2 y \left(x + 1\right),\qquad\frac{\partial Q}{\partial x}=6 x y + 2 y.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(y^{2} \left(x + 1\right))\,\mathrm dx+(3 x^{2} y + 2 x y)\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(6 x y + 2 y-(2 y \left(x + 1\right))\right)\,\mathrm dA\\ & =\iint_D 4 x y\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):1\le x\le 4,0\le y\le 3\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):2\le x\le 3,1\le y\le 2\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 4 x y\,\mathrm dA & =\iint_{\Delta_1}4 x y\,\mathrm dA-\iint_{\Delta_2}4 x y\,\mathrm dA\\ & =\int_{0}^{3}\int_{1}^{4}4 x y\,\mathrm d x\,\mathrm d y-\int_{1}^{2}\int_{2}^{3}4 x y\,\mathrm d x\,\mathrm d y\\ & =\int_{1}^{4}2 x\,\mathrm d x\cdot \int_{0}^{3}2 y\,\mathrm d y-\int_{2}^{3}2 x\,\mathrm d x\cdot \int_{1}^{2}2 y\,\mathrm d y\\ & =x^{2}\big|_{1}^{4}\cdot y^{2}\big|_{0}^{3}-x^{2}\big|_{2}^{3}\cdot y^{2}\big|_{1}^{2}\\ & =(\left(16\right)-\left(1\right))\cdot (\left(9\right)-\left(0\right))-(\left(9\right)-\left(4\right))\cdot (\left(4\right)-\left(1\right))\\ & =\left(15\right)\cdot \left(9\right)-\left(5\right)\cdot \left(3\right)\\ & =120.\end{aligned}
$$

## Generated variant rectangle_x2y3 0

Parameters: `{"c": -3, "hole": [1, 2, -1, 0], "outer": [0, 3, -3, 1]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/f90d10a68abc03f88bf000dea7211d72f2bc844c2c9074e84ed934a6e96a8183.png)

Calculate $\oint_{\partial D}(- 6 x^{2} y^{4} + 3 x)\,\mathrm dx+(- 12 x^{3} y^{3} + 3 y^{2})\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $-2153$
- $6459$
- $2160$
- $2167$
- $2153$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 6 x^{2} y^{4} + 3 x$ and $Q(x,y)=- 12 x^{3} y^{3} + 3 y^{2}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 6 x^{2} y^{4} + 3 x\right)=\left(0\right)+\left(- 24 x^{2} y^{3}\right)=- 24 x^{2} y^{3}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 12 x^{3} y^{3} + 3 y^{2}\right)=\left(0\right)+\left(- 36 x^{2} y^{3}\right)=- 36 x^{2} y^{3}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 24 x^{2} y^{3},\qquad\frac{\partial Q}{\partial x}=- 36 x^{2} y^{3}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 6 x^{2} y^{4} + 3 x)\,\mathrm dx+(- 12 x^{3} y^{3} + 3 y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 36 x^{2} y^{3}-(- 24 x^{2} y^{3})\right)\,\mathrm dA\\ & =\iint_D - 12 x^{2} y^{3}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):0\le x\le 3,-3\le y\le 1\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 2,-1\le y\le 0\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 12 x^{2} y^{3}\,\mathrm dA & =\iint_{\Delta_1}- 12 x^{2} y^{3}\,\mathrm dA-\iint_{\Delta_2}- 12 x^{2} y^{3}\,\mathrm dA\\ & =\int_{-3}^{1}\int_{0}^{3}- 12 x^{2} y^{3}\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{1}^{2}- 12 x^{2} y^{3}\,\mathrm d x\,\mathrm d y\\ & =\int_{0}^{3}- 3 x^{2}\,\mathrm d x\cdot \int_{-3}^{1}4 y^{3}\,\mathrm d y-\int_{1}^{2}- 3 x^{2}\,\mathrm d x\cdot \int_{-1}^{0}4 y^{3}\,\mathrm d y\\ & =- x^{3}\big|_{0}^{3}\cdot y^{4}\big|_{-3}^{1}-- x^{3}\big|_{1}^{2}\cdot y^{4}\big|_{-1}^{0}\\ & =(\left(-27\right)-\left(0\right))\cdot (\left(1\right)-\left(81\right))-(\left(-8\right)-\left(-1\right))\cdot (\left(0\right)-\left(1\right))\\ & =\left(-27\right)\cdot \left(-80\right)-\left(-7\right)\cdot \left(-1\right)\\ & =2153.\end{aligned}
$$

## Generated variant rectangle_x2y3 1

Parameters: `{"c": 1, "hole": [1, 2, 1, 2], "outer": [0, 3, -1, 3]}`; profile `outer_minus_hole`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/526e86bbe4085c3822b0fffc54cdc0dec9aaf61a6fcd0ebf25d9442e510c2133.png)

Calculate $\oint_{\partial D}(2 x^{2} y^{4} - x)\,\mathrm dx+(4 x^{3} y^{3} - y^{2})\,\mathrm dy$, where $D$ is the region shown above.

Field `selection` (:answer-field.type/radio):
- $755$
- $685$ (correct)
- $2055$
- $720$
- $-685$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2 x^{2} y^{4} - x$ and $Q(x,y)=4 x^{3} y^{3} - y^{2}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(2 x^{2} y^{4} - x\right)=\left(0\right)+\left(8 x^{2} y^{3}\right)=8 x^{2} y^{3}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(4 x^{3} y^{3} - y^{2}\right)=\left(0\right)+\left(12 x^{2} y^{3}\right)=12 x^{2} y^{3}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=8 x^{2} y^{3},\qquad\frac{\partial Q}{\partial x}=12 x^{2} y^{3}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(2 x^{2} y^{4} - x)\,\mathrm dx+(4 x^{3} y^{3} - y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(12 x^{2} y^{3}-(8 x^{2} y^{3})\right)\,\mathrm dA\\ & =\iint_D 4 x^{2} y^{3}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):0\le x\le 3,-1\le y\le 3\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 2,1\le y\le 2\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 4 x^{2} y^{3}\,\mathrm dA & =\iint_{\Delta_1}4 x^{2} y^{3}\,\mathrm dA-\iint_{\Delta_2}4 x^{2} y^{3}\,\mathrm dA\\ & =\int_{-1}^{3}\int_{0}^{3}4 x^{2} y^{3}\,\mathrm d x\,\mathrm d y-\int_{1}^{2}\int_{1}^{2}4 x^{2} y^{3}\,\mathrm d x\,\mathrm d y\\ & =\int_{0}^{3}x^{2}\,\mathrm d x\cdot \int_{-1}^{3}4 y^{3}\,\mathrm d y-\int_{1}^{2}x^{2}\,\mathrm d x\cdot \int_{1}^{2}4 y^{3}\,\mathrm d y\\ & =\frac{x^{3}}{3}\big|_{0}^{3}\cdot y^{4}\big|_{-1}^{3}-\frac{x^{3}}{3}\big|_{1}^{2}\cdot y^{4}\big|_{1}^{2}\\ & =(\left(9\right)-\left(0\right))\cdot (\left(81\right)-\left(1\right))-(\left(\frac{8}{3}\right)-\left(\frac{1}{3}\right))\cdot (\left(16\right)-\left(1\right))\\ & =\left(9\right)\cdot \left(80\right)-\left(\frac{7}{3}\right)\cdot \left(15\right)\\ & =685.\end{aligned}
$$

## Generated variant annulus_supplied 0

Parameters: `{"c": -3, "inner": 3, "outer": 4}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/76502511aaf9b1a593bb5edeb33162f8f77ec409af528bfa7809a28469a8cef8.png)

Given $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=- 3 x^{2} - 3 y^{2}$, calculate $\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy$ over the positively oriented annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- \frac{1011 \pi}{2}$
- $- 74 \pi$
- $- 384 \pi$
- $\frac{525 \pi}{2}$
- $- \frac{525 \pi}{2}$ (correct)

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy & =\iint_D - 3 x^{2} - 3 y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 x^{2} - 3 y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}- 3 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =-3\left(\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}r^{3}\,\mathrm d r\right)\\ & =- 6 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 6 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =- 6 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =- 6 \pi\cdot \left(\frac{175}{4}\right)\\ & =- \frac{525 \pi}{2}.\end{aligned}
$$

## Generated variant annulus_supplied 1

Parameters: `{"c": 1, "inner": 3, "outer": 5}`; profile `radial`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133900/plots/aad42c90f3444694909fdbec882855272e736ce30edc582c3369dee9beb4f794.png)

Given $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=x^{2} + y^{2}$, calculate $\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy$ over the positively oriented annular region shown above.

Field `selection` (:answer-field.type/radio):
- $- 272 \pi$
- $272 \pi$ (correct)
- $\frac{196 \pi}{3}$
- $\frac{625 \pi}{2}$
- $353 \pi$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy & =\iint_D x^{2} + y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as

$$\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D x^{2} + y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{5}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{5}r^{3}\,\mathrm d r\\ & =2 \pi\cdot \int_{3}^{5}r^{3}\,\mathrm d r\\ & =2 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{5}\\ & =2 \pi\cdot (\left(\frac{625}{4}\right)-\left(\frac{81}{4}\right))\\ & =2 \pi\cdot \left(136\right)\\ & =272 \pi.\end{aligned}
$$

