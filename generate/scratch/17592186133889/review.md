# Three-dimensional divergence review

Author review: Original, Generated, difficulty and Correct labels are explicit. Raw incomplete source prompts remain evidence only.


## Original — q-105555 — easy

Consider the vector field $F=\operatorname{ln}⁡(xy)\,i-y\operatorname{cos}⁡x\,j+y{z}^{3}\,k.$ 
Find $∇\cdot F.$

- $\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}$ **Correct**

- $\frac{1}{x}+\operatorname{sin}⁡x+3y{z}^{2}$

- $\frac{1}{xy}-\operatorname{cos}⁡x+{z}^{3}$

- $\frac{1}{xy}\,i-\operatorname{cos}⁡x\,j+{z}^{3}\,k$

- $\frac{1}{y}\,i-\operatorname{sin}⁡x\,j+3y{z}^{2}\,k$


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡(xy))+\frac{∂}{∂y}(-y\operatorname{cos}⁡x)+\frac{∂}{∂z}(y{z}^{3}) \\  & =\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}.\end{aligned}
$$

## Generated — easy

Template: `source_q-105555`; profile: `observed_q-105555`; evidence only

Consider the vector field $F=\operatorname{ln}⁡(xy)\,i-y\operatorname{cos}⁡x\,j+y{z}^{3}\,k.$ 
Find $∇\cdot F.$

- $\frac{1}{xy}-\operatorname{cos}⁡x+{z}^{3}$
- $\frac{1}{x}+\operatorname{sin}⁡x+3y{z}^{2}$
- $\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}$ **Correct**
- $\frac{1}{y}\,i-\operatorname{sin}⁡x\,j+3y{z}^{2}\,k$
- $\frac{1}{xy}\,i-\operatorname{cos}⁡x\,j+{z}^{3}\,k$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡(xy))+\frac{∂}{∂y}(-y\operatorname{cos}⁡x)+\frac{∂}{∂z}(y{z}^{3}) \\  & =\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}.\end{aligned}
$$

## Generated — easy

Template: `source_q-105555`; profile: `observed_q-105555`; evidence only

Consider the vector field $F=2\left(\operatorname{ln}⁡(xy)\right)\,i+2\left(-y\operatorname{cos}⁡x\right)\,j+2\left(y{z}^{3}\right)\,k.$ 
Find $∇\cdot F.$

- $2\left(\frac{1}{xy}-\operatorname{cos}⁡x+{z}^{3}\right)$
- $2\left(\frac{1}{x}+\operatorname{sin}⁡x+3y{z}^{2}\right)$
- $2\left(\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}\right)$ **Correct**
- $2\left(\frac{1}{y}\,i-\operatorname{sin}⁡x\,j+3y{z}^{2}\,k\right)$
- $2\left(\frac{1}{xy}\,i-\operatorname{cos}⁡x\,j+{z}^{3}\,k\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left(\operatorname{ln}⁡(xy)\right))+\frac{∂}{∂y}(2\left(-y\operatorname{cos}⁡x\right))+\frac{∂}{∂z}(2\left(y{z}^{3}\right)) \\  & =2\left(\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}\right).\end{aligned}
$$


## Original — q-41839 — moderate

Consider the vector field $F=xyz\,i+{e}^{-y}\operatorname{cos}⁡\pi x\,j+({e}^{-y}\operatorname{sin}⁡\pi z+2xz)\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,0,0).$

- $1$

- $1-\pi $

- $3-\pi $

- $\pi +1$

- $\pi +3$ **Correct**


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(xyz)+\frac{∂}{∂y}({e}^{-y}\operatorname{cos}⁡\pi x)+\frac{∂}{∂z}({e}^{-y}\operatorname{sin}⁡\pi z+2xz) \\  & =yz-{e}^{-y}\operatorname{cos}⁡\pi x+\pi {e}^{-y}\operatorname{cos}⁡\pi z+2x.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,0) & =(0)(0)-{e}^{0}\operatorname{cos}⁡\pi +\pi {e}^{0}\operatorname{cos}⁡0+2(1) \\  & =0-(-1)+\pi (1)+2 \\  & =1+\pi +2 \\  & =\pi +3.\end{aligned}
$$

## Generated — moderate

Template: `source_q-41839`; profile: `observed_q-41839`; evidence only

Consider the vector field $F=xyz\,i+{e}^{-y}\operatorname{cos}⁡\pi x\,j+({e}^{-y}\operatorname{sin}⁡\pi z+2xz)\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,0,0).$

- $3-\pi $
- $1-\pi $
- $1$
- $\pi +3$ **Correct**
- $\pi +1$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(xyz)+\frac{∂}{∂y}({e}^{-y}\operatorname{cos}⁡\pi x)+\frac{∂}{∂z}({e}^{-y}\operatorname{sin}⁡\pi z+2xz) \\  & =yz-{e}^{-y}\operatorname{cos}⁡\pi x+\pi {e}^{-y}\operatorname{cos}⁡\pi z+2x.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,0) & =(0)(0)-{e}^{0}\operatorname{cos}⁡\pi +\pi {e}^{0}\operatorname{cos}⁡0+2(1) \\  & =0-(-1)+\pi (1)+2 \\  & =1+\pi +2 \\  & =\pi +3.\end{aligned}
$$

## Generated — moderate

Template: `source_q-41839`; profile: `observed_q-41839`; evidence only

Consider the vector field $F=2\left(xyz\right)\,i+2\left({e}^{-y}\operatorname{cos}⁡\pi x\right)\,j+(2\left({e}^{-y}\operatorname{sin}⁡\pi z+2xz\right))\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,0,0).$

- $2\left(3-\pi \right)$
- $2\left(1-\pi \right)$
- $2\left(1\right)$
- $2\left(\pi +3\right)$ **Correct**
- $2\left(\pi +1\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left(xyz\right))+\frac{∂}{∂y}(2\left({e}^{-y}\operatorname{cos}⁡\pi x\right))+\frac{∂}{∂z}(2\left({e}^{-y}\operatorname{sin}⁡\pi z+2xz\right)) \\  & =2\left(yz-{e}^{-y}\operatorname{cos}⁡\pi x+\pi {e}^{-y}\operatorname{cos}⁡\pi z+2x\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,0) & =2\left((0)(0)-{e}^{0}\operatorname{cos}⁡\pi +\pi {e}^{0}\operatorname{cos}⁡0+2(1)\right) \\  & =2\left(0-(-1)+\pi (1)+2\right) \\  & =2\left(1+\pi +2\right) \\  & =2\left(\pi +3\right).\end{aligned}
$$


## Original — q-168615 — easy

$\text{div}\,F\,=$

                            
                                    
                            
                                        {{field-1}}

- $2x$ **Correct**


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}\text{div}F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({z}^{2})+\frac{∂}{∂y}(2xy)+\frac{∂}{∂z}(x{y}^{2}) \\  & =0+2x+0 \\  & =2x.\end{aligned}
$$

## Generated — easy

Template: `source_q-168615`; profile: `observed_q-168615`; evidence only

$\text{div}\,F\,=$

                            
                                    
                            
                                        {{field-1}}

- $2x$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}\text{div}F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({z}^{2})+\frac{∂}{∂y}(2xy)+\frac{∂}{∂z}(x{y}^{2}) \\  & =0+2x+0 \\  & =2x.\end{aligned}
$$

## Generated — easy

Template: `source_q-168615`; profile: `observed_q-168615`; evidence only

$\text{div}\,F\,=$

                            
                                    
                            
                                        {{field-1}}

- $2\left(2x\right)$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}\text{div}F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left({z}^{2}\right))+\frac{∂}{∂y}(2\left(2xy\right))+\frac{∂}{∂z}(2\left(x{y}^{2}\right)) \\  & =2\left(0+2x+0\right) \\  & =2\left(2x\right).\end{aligned}
$$


## Original — q-123176 — easy

Consider the vector field $F=⟨{e}^{x}\operatorname{sin}⁡yz,\,xyz,2⟩.$ Find $\text{div}\,F.$

- ${e}^{x}\operatorname{cos}⁡yz+xz$

- ${e}^{x}\operatorname{cos}⁡yz$

- ${e}^{x}\operatorname{cos}⁡yz+xz+2$

- ${e}^{x}\operatorname{sin}⁡yz+xyz+2$

- ${e}^{x}\operatorname{sin}⁡yz+xz$ **Correct**


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({e}^{x}\operatorname{sin}⁡yz)+\frac{∂}{∂y}(xyz)+\frac{∂}{∂z}(2) \\  & ={e}^{x}\operatorname{sin}⁡yz+xz.\end{aligned}
$$

## Generated — easy

Template: `source_q-123176`; profile: `observed_q-123176`; evidence only

Consider the vector field $F=⟨{e}^{x}\operatorname{sin}⁡yz,\,xyz,2⟩.$ Find $\text{div}\,F.$

- ${e}^{x}\operatorname{cos}⁡yz+xz+2$
- ${e}^{x}\operatorname{cos}⁡yz$
- ${e}^{x}\operatorname{cos}⁡yz+xz$
- ${e}^{x}\operatorname{sin}⁡yz+xz$ **Correct**
- ${e}^{x}\operatorname{sin}⁡yz+xyz+2$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({e}^{x}\operatorname{sin}⁡yz)+\frac{∂}{∂y}(xyz)+\frac{∂}{∂z}(2) \\  & ={e}^{x}\operatorname{sin}⁡yz+xz.\end{aligned}
$$

## Generated — easy

Template: `source_q-123176`; profile: `observed_q-123176`; evidence only

Consider the vector field $F=⟨2\left({e}^{x}\operatorname{sin}⁡yz\right),\,2\left(xyz\right),2\left(2\right)⟩.$ Find $\text{div}\,F.$

- $2\left({e}^{x}\operatorname{cos}⁡yz+xz+2\right)$
- $2\left({e}^{x}\operatorname{cos}⁡yz\right)$
- $2\left({e}^{x}\operatorname{cos}⁡yz+xz\right)$
- $2\left({e}^{x}\operatorname{sin}⁡yz+xz\right)$ **Correct**
- $2\left({e}^{x}\operatorname{sin}⁡yz+xyz+2\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left({e}^{x}\operatorname{sin}⁡yz\right))+\frac{∂}{∂y}(2\left(xyz\right))+\frac{∂}{∂z}(2\left(2\right)) \\  & =2\left({e}^{x}\operatorname{sin}⁡yz+xz\right).\end{aligned}
$$


## Original — q-123179 — easy

Consider the vector field $F=(2x+3y-4z)^{2}\,i+(2x+3y-4z)^{2}\,j+(2x+3y-4z)^{2}\,k.$ 
Find $∇\cdot F.$

- $6x+9y-12z$

- $4x+6y-8z$ **Correct**

- $8x+12y-16z$

- $(2x+3y-4z)^{2}$

- $x+2y-4z$


**Original worked solution**


If $F=P\,+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((2x+3y-4z)^{2})+\frac{∂}{∂y}((2x+3y-4z)^{2})+\frac{∂}{∂z}((2x+3y-4z)^{2}) \\  & =4(2x+3y-4z)+6(2x+3y-4z)-8(2x+3y-4z) \\  & =2(2x+3y-4z) \\  & =4x+6y-8z.\end{aligned}
$$

## Generated — easy

Template: `source_q-123179`; profile: `observed_q-123179`; evidence only

Consider the vector field $F=(2x+3y-4z)^{2}\,i+(2x+3y-4z)^{2}\,j+(2x+3y-4z)^{2}\,k.$ 
Find $∇\cdot F.$

- $8x+12y-16z$
- $4x+6y-8z$ **Correct**
- $6x+9y-12z$
- $x+2y-4z$
- $(2x+3y-4z)^{2}$

**Worked solution**

If $F=P\,+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((2x+3y-4z)^{2})+\frac{∂}{∂y}((2x+3y-4z)^{2})+\frac{∂}{∂z}((2x+3y-4z)^{2}) \\  & =4(2x+3y-4z)+6(2x+3y-4z)-8(2x+3y-4z) \\  & =2(2x+3y-4z) \\  & =4x+6y-8z.\end{aligned}
$$

## Generated — easy

Template: `source_q-123179`; profile: `observed_q-123179`; evidence only

Consider the vector field $F=2\left((2x+3y-4z)^{2}\right)\,i+2\left((2x+3y-4z)^{2}\right)\,j+2\left((2x+3y-4z)^{2}\right)\,k.$ 
Find $∇\cdot F.$

- $2\left(8x+12y-16z\right)$
- $2\left(4x+6y-8z\right)$ **Correct**
- $2\left(6x+9y-12z\right)$
- $2\left(x+2y-4z\right)$
- $2\left((2x+3y-4z)^{2}\right)$

**Worked solution**

If $F=P\,+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left((2x+3y-4z)^{2}\right))+\frac{∂}{∂y}(2\left((2x+3y-4z)^{2}\right))+\frac{∂}{∂z}(2\left((2x+3y-4z)^{2}\right)) \\  & =2\left(4(2x+3y-4z)+6(2x+3y-4z)-8(2x+3y-4z)\right) \\  & =2\left(2(2x+3y-4z)\right) \\  & =2\left(4x+6y-8z\right).\end{aligned}
$$


## Original — q-123200 — moderate

Consider the vector field $F=(x-y)^{3}\,i+(y+z)^{3}\,j+(x+z)^{3}\,k.$ Evaluate $\text{div}\,F$ at the point $(-2,2,2).$

- $144$

- $76$

- $48$

- $96$ **Correct**

- $84$


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((x-y)^{3})+\frac{∂}{∂y}((y+z)^{3})+\frac{∂}{∂z}((x+z)^{3}) \\  & =3(x-y)^{2}+3(y+z)^{2}+3(x+z)^{2}.\end{aligned}
$$

 

Finally, we evaluate $\text{div}\,F$ at the point $(-2,2,2),$ and obtain

$$
\begin{aligned}\text{div}\,F(-2,2,2) & =3((-2)-(2))^{2}+3((2)+(2))^{2}+3((-2)+(2))^{2} \\  & =3(-4)^{2}+3(4)^{2}+3(0)^{2} \\  & =96.\end{aligned}
$$

## Generated — moderate

Template: `source_q-123200`; profile: `observed_q-123200`; evidence only

Consider the vector field $F=(x-y)^{3}\,i+(y+z)^{3}\,j+(x+z)^{3}\,k.$ Evaluate $\text{div}\,F$ at the point $(-2,2,2).$

- $48$
- $76$
- $144$
- $84$
- $96$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((x-y)^{3})+\frac{∂}{∂y}((y+z)^{3})+\frac{∂}{∂z}((x+z)^{3}) \\  & =3(x-y)^{2}+3(y+z)^{2}+3(x+z)^{2}.\end{aligned}
$$

 

Finally, we evaluate $\text{div}\,F$ at the point $(-2,2,2),$ and obtain

$$
\begin{aligned}\text{div}\,F(-2,2,2) & =3((-2)-(2))^{2}+3((2)+(2))^{2}+3((-2)+(2))^{2} \\  & =3(-4)^{2}+3(4)^{2}+3(0)^{2} \\  & =96.\end{aligned}
$$

## Generated — moderate

Template: `source_q-123200`; profile: `observed_q-123200`; evidence only

Consider the vector field $F=2\left((x-y)^{3}\right)\,i+2\left((y+z)^{3}\right)\,j+2\left((x+z)^{3}\right)\,k.$ Evaluate $\text{div}\,F$ at the point $(-2,2,2).$

- $2\left(48\right)$
- $2\left(76\right)$
- $2\left(144\right)$
- $2\left(84\right)$
- $2\left(96\right)$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left((x-y)^{3}\right))+\frac{∂}{∂y}(2\left((y+z)^{3}\right))+\frac{∂}{∂z}(2\left((x+z)^{3}\right)) \\  & =2\left(3(x-y)^{2}+3(y+z)^{2}+3(x+z)^{2}\right).\end{aligned}
$$

 

Finally, we evaluate $\text{div}\,F$ at the point $(-2,2,2),$ and obtain

$$
\begin{aligned}\text{div}\,F(-2,2,2) & =2\left(3((-2)-(2))^{2}+3((2)+(2))^{2}+3((-2)+(2))^{2}\right) \\  & =2\left(3(-4)^{2}+3(4)^{2}+3(0)^{2}\right) \\  & =2\left(96\right).\end{aligned}
$$


## Original — q-131176 — easy

Consider the vector field $F=2xy{z}^{2}\,i+x{e}^{y}\,j+y{z}^{3}\,k.$ 
Find $∇\cdot F.$

- $xy{z}^{2}+xz$

- $y{z}^{2}+xy{e}^{y}$

- $5y{z}^{2}+x{e}^{y}$ **Correct**

- $y{z}^{2}+xy+y$

- $x+{e}^{y}+{z}^{2}$


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2xy{z}^{2})+\frac{∂}{∂y}(x{e}^{y})+\frac{∂}{∂z}(y{z}^{3}) \\  & =2y{z}^{2}+x{e}^{y}+3y{z}^{2} \\  & =5y{z}^{2}+x{e}^{y}.\end{aligned}
$$

## Generated — easy

Template: `source_q-131176`; profile: `observed_q-131176`; evidence only

Consider the vector field $F=2xy{z}^{2}\,i+x{e}^{y}\,j+y{z}^{3}\,k.$ 
Find $∇\cdot F.$

- $5y{z}^{2}+x{e}^{y}$ **Correct**
- $y{z}^{2}+xy{e}^{y}$
- $xy{z}^{2}+xz$
- $x+{e}^{y}+{z}^{2}$
- $y{z}^{2}+xy+y$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2xy{z}^{2})+\frac{∂}{∂y}(x{e}^{y})+\frac{∂}{∂z}(y{z}^{3}) \\  & =2y{z}^{2}+x{e}^{y}+3y{z}^{2} \\  & =5y{z}^{2}+x{e}^{y}.\end{aligned}
$$

## Generated — easy

Template: `source_q-131176`; profile: `observed_q-131176`; evidence only

Consider the vector field $F=2\left(2xy{z}^{2}\right)\,i+2\left(x{e}^{y}\right)\,j+2\left(y{z}^{3}\right)\,k.$ 
Find $∇\cdot F.$

- $2\left(5y{z}^{2}+x{e}^{y}\right)$ **Correct**
- $2\left(y{z}^{2}+xy{e}^{y}\right)$
- $2\left(xy{z}^{2}+xz\right)$
- $2\left(x+{e}^{y}+{z}^{2}\right)$
- $2\left(y{z}^{2}+xy+y\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left(2xy{z}^{2}\right))+\frac{∂}{∂y}(2\left(x{e}^{y}\right))+\frac{∂}{∂z}(2\left(y{z}^{3}\right)) \\  & =2\left(2y{z}^{2}+x{e}^{y}+3y{z}^{2}\right) \\  & =2\left(5y{z}^{2}+x{e}^{y}\right).\end{aligned}
$$


## Original — q-131178 — moderate

Consider the vector field $F=xz\operatorname{cos}⁡y\,i+y{x}^{2}\,j+x{z}^{2}{e}^{y}\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,0,-2).$

- $-5$ **Correct**

- $4$

- $-2$

- $3$

- $0$


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(xz\operatorname{cos}⁡y)+\frac{∂}{∂y}(y{x}^{2})+\frac{∂}{∂z}(x{z}^{2}{e}^{y}) \\  & =z\operatorname{cos}⁡y+{x}^{2}+2xz{e}^{y}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,-2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,-2) & =(-2)\cdot \operatorname{cos}⁡0+{1}^{2}+2\cdot 1\cdot (-2)\cdot {e}^{0} \\  & =-2+1-4 \\  & =-5\end{aligned}
$$

## Generated — moderate

Template: `source_q-131178`; profile: `observed_q-131178`; evidence only

Consider the vector field $F=xz\operatorname{cos}⁡y\,i+y{x}^{2}\,j+x{z}^{2}{e}^{y}\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,0,-2).$

- $-2$
- $4$
- $-5$ **Correct**
- $0$
- $3$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(xz\operatorname{cos}⁡y)+\frac{∂}{∂y}(y{x}^{2})+\frac{∂}{∂z}(x{z}^{2}{e}^{y}) \\  & =z\operatorname{cos}⁡y+{x}^{2}+2xz{e}^{y}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,-2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,-2) & =(-2)\cdot \operatorname{cos}⁡0+{1}^{2}+2\cdot 1\cdot (-2)\cdot {e}^{0} \\  & =-2+1-4 \\  & =-5\end{aligned}
$$

## Generated — moderate

Template: `source_q-131178`; profile: `observed_q-131178`; evidence only

Consider the vector field $F=2\left(xz\operatorname{cos}⁡y\right)\,i+2\left(y{x}^{2}\right)\,j+2\left(x{z}^{2}{e}^{y}\right)\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,0,-2).$

- $2\left(-2\right)$
- $2\left(4\right)$
- $2\left(-5\right)$ **Correct**
- $2\left(0\right)$
- $2\left(3\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left(xz\operatorname{cos}⁡y\right))+\frac{∂}{∂y}(2\left(y{x}^{2}\right))+\frac{∂}{∂z}(2\left(x{z}^{2}{e}^{y}\right)) \\  & =2\left(z\operatorname{cos}⁡y+{x}^{2}+2xz{e}^{y}\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,-2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,-2) & =2\left((-2)\cdot \operatorname{cos}⁡0+{1}^{2}+2\cdot 1\cdot (-2)\cdot {e}^{0}\right) \\  & =2\left(-2+1-4\right) \\  & =2\left(-5\right)\end{aligned}
$$


## Original — q-131179 — moderate

Consider the vector field $F=x(y{e}^{z}+\operatorname{ln}⁡y)\,i+xy{e}^{z}\,j+z(x+1)\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,1,0).$

- $0$

- $2$

- $3$

- $6$

- $4$ **Correct**


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(x(y{e}^{z}+\operatorname{ln}⁡y))+\frac{∂}{∂y}(xy{e}^{z})+\frac{∂}{∂z}(z(x+1)) \\  & =(y{e}^{z}+\operatorname{ln}⁡y)+x{e}^{z}+(x+1) \\  & =y{e}^{z}+\operatorname{ln}⁡y+x{e}^{z}+x+1\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,1,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,1,0) & =1\cdot {e}^{0}+\operatorname{ln}⁡1+1\cdot {e}^{0}+1+1 \\  & =1+0+1+1+1 \\  & =4.\end{aligned}
$$

## Generated — moderate

Template: `source_q-131179`; profile: `observed_q-131179`; evidence only

Consider the vector field $F=x(y{e}^{z}+\operatorname{ln}⁡y)\,i+xy{e}^{z}\,j+z(x+1)\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,1,0).$

- $3$
- $2$
- $0$
- $4$ **Correct**
- $6$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(x(y{e}^{z}+\operatorname{ln}⁡y))+\frac{∂}{∂y}(xy{e}^{z})+\frac{∂}{∂z}(z(x+1)) \\  & =(y{e}^{z}+\operatorname{ln}⁡y)+x{e}^{z}+(x+1) \\  & =y{e}^{z}+\operatorname{ln}⁡y+x{e}^{z}+x+1\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,1,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,1,0) & =1\cdot {e}^{0}+\operatorname{ln}⁡1+1\cdot {e}^{0}+1+1 \\  & =1+0+1+1+1 \\  & =4.\end{aligned}
$$

## Generated — moderate

Template: `source_q-131179`; profile: `observed_q-131179`; evidence only

Consider the vector field $F=2\left(x(y{e}^{z}+\operatorname{ln}⁡y)\right)\,i+2\left(xy{e}^{z}\right)\,j+2\left(z(x+1)\right)\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,1,0).$

- $2\left(3\right)$
- $2\left(2\right)$
- $2\left(0\right)$
- $2\left(4\right)$ **Correct**
- $2\left(6\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left(x(y{e}^{z}+\operatorname{ln}⁡y)\right))+\frac{∂}{∂y}(2\left(xy{e}^{z}\right))+\frac{∂}{∂z}(2\left(z(x+1)\right)) \\  & =2\left((y{e}^{z}+\operatorname{ln}⁡y)+x{e}^{z}+(x+1)\right) \\  & =2\left(y{e}^{z}+\operatorname{ln}⁡y+x{e}^{z}+x+1\right)\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,1,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,1,0) & =2\left(1\cdot {e}^{0}+\operatorname{ln}⁡1+1\cdot {e}^{0}+1+1\right) \\  & =2\left(1+0+1+1+1\right) \\  & =2\left(4\right).\end{aligned}
$$


## Original — q-168624 — easy

$∇\cdot G=\,$

                            
                                    
                            
                                        {{field-1}}

- $-4z$ **Correct**


**Original worked solution**


If $G=P\,\text{i}+Q\,\text{j}+R\,\text{k}$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $G$ all exist, then the divergence of $G$ is the scalar field given by

$$
∇\cdot G=\text{div}\,G=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

Therefore, we have

$$
\begin{aligned}∇\cdot G & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(0)+\frac{∂}{∂y}(0)+\frac{∂}{∂z}(-xy-2{z}^{2}) \\  & =-4z.\end{aligned}
$$

## Generated — easy

Template: `source_q-168624`; profile: `observed_q-168624`; evidence only

$∇\cdot G=\,$

                            
                                    
                            
                                        {{field-1}}

- $-4z$ **Correct**

**Worked solution**

If $G=P\,\text{i}+Q\,\text{j}+R\,\text{k}$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $G$ all exist, then the divergence of $G$ is the scalar field given by

$$
∇\cdot G=\text{div}\,G=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

Therefore, we have

$$
\begin{aligned}∇\cdot G & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(0)+\frac{∂}{∂y}(0)+\frac{∂}{∂z}(-xy-2{z}^{2}) \\  & =-4z.\end{aligned}
$$

## Generated — easy

Template: `source_q-168624`; profile: `observed_q-168624`; evidence only

$∇\cdot G=\,$

                            
                                    
                            
                                        {{field-1}}

- $2\left(-4z\right)$ **Correct**

**Worked solution**

If $G=P\,\text{i}+Q\,\text{j}+R\,\text{k}$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $G$ all exist, then the divergence of $G$ is the scalar field given by

$$
∇\cdot G=\text{div}\,G=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

Therefore, we have

$$
\begin{aligned}∇\cdot G & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left(0\right))+\frac{∂}{∂y}(2\left(0\right))+\frac{∂}{∂z}(2\left(-xy-2{z}^{2}\right)) \\  & =2\left(-4z\right).\end{aligned}
$$


## Original — q-123192 — moderate

Consider the vector field $F={x}^{2}yz\,i+x{y}^{2}z\,j+xy{z}^{2}\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,2,2).$

- $20$

- $16$

- $32$

- $18$

- $24$ **Correct**


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({x}^{2}yz)+\frac{∂}{∂y}(x{y}^{2}z)+\frac{∂}{∂z}(xy{z}^{2}) \\  & =2xyz+2xyz+2xyz \\  & =6xyz.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,2,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,2,2) & =6(1)(2)(2) \\  & =6\cdot 4 \\  & =24.\end{aligned}
$$

## Generated — moderate

Template: `source_q-123192`; profile: `observed_q-123192`; evidence only

Consider the vector field $F={x}^{2}yz\,i+x{y}^{2}z\,j+xy{z}^{2}\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,2,2).$

- $32$
- $16$
- $20$
- $24$ **Correct**
- $18$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({x}^{2}yz)+\frac{∂}{∂y}(x{y}^{2}z)+\frac{∂}{∂z}(xy{z}^{2}) \\  & =2xyz+2xyz+2xyz \\  & =6xyz.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,2,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,2,2) & =6(1)(2)(2) \\  & =6\cdot 4 \\  & =24.\end{aligned}
$$

## Generated — moderate

Template: `source_q-123192`; profile: `observed_q-123192`; evidence only

Consider the vector field $F=2\left({x}^{2}yz\right)\,i+2\left(x{y}^{2}z\right)\,j+2\left(xy{z}^{2}\right)\,k.$ 
Evaluate $∇\cdot F$ at the point $(1,2,2).$

- $2\left(32\right)$
- $2\left(16\right)$
- $2\left(20\right)$
- $2\left(24\right)$ **Correct**
- $2\left(18\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left({x}^{2}yz\right))+\frac{∂}{∂y}(2\left(x{y}^{2}z\right))+\frac{∂}{∂z}(2\left(xy{z}^{2}\right)) \\  & =2\left(2xyz+2xyz+2xyz\right) \\  & =2\left(6xyz\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,2,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,2,2) & =2\left(6(1)(2)(2)\right) \\  & =2\left(6\cdot 4\right) \\  & =2\left(24\right).\end{aligned}
$$


## Original — q-41837 — easy

Consider the vector field $F=⟨{e}^{xz}\operatorname{cos}⁡y,\,0,\,\operatorname{ln}⁡yz⟩.$ Find $\text{div}\,F.$

- $z{e}^{xz}\operatorname{sin}⁡y-\frac{1}{z}$

- $z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{{y}^{2}z}$

- $z{e}^{xz}\operatorname{cos}⁡y-{e}^{xy}\operatorname{sin}⁡y+\frac{1}{z}$

- $xz{e}^{xz}\operatorname{cos}⁡y+\frac{1}{yz}$

- $z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}$ **Correct**


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({e}^{xz}\operatorname{cos}⁡y)+\frac{∂}{∂y}(0)+\frac{∂}{∂z}(\operatorname{ln}⁡yz) \\  & =z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}.\end{aligned}
$$

## Generated — easy

Template: `source_q-41837`; profile: `observed_q-41837`; evidence only

Consider the vector field $F=⟨{e}^{xz}\operatorname{cos}⁡y,\,0,\,\operatorname{ln}⁡yz⟩.$ Find $\text{div}\,F.$

- $z{e}^{xz}\operatorname{cos}⁡y-{e}^{xy}\operatorname{sin}⁡y+\frac{1}{z}$
- $z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{{y}^{2}z}$
- $z{e}^{xz}\operatorname{sin}⁡y-\frac{1}{z}$
- $z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}$ **Correct**
- $xz{e}^{xz}\operatorname{cos}⁡y+\frac{1}{yz}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({e}^{xz}\operatorname{cos}⁡y)+\frac{∂}{∂y}(0)+\frac{∂}{∂z}(\operatorname{ln}⁡yz) \\  & =z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}.\end{aligned}
$$

## Generated — easy

Template: `source_q-41837`; profile: `observed_q-41837`; evidence only

Consider the vector field $F=⟨2\left({e}^{xz}\operatorname{cos}⁡y\right),\,2\left(0\right),\,2\left(\operatorname{ln}⁡yz\right)⟩.$ Find $\text{div}\,F.$

- $2\left(z{e}^{xz}\operatorname{cos}⁡y-{e}^{xy}\operatorname{sin}⁡y+\frac{1}{z}\right)$
- $2\left(z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{{y}^{2}z}\right)$
- $2\left(z{e}^{xz}\operatorname{sin}⁡y-\frac{1}{z}\right)$
- $2\left(z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}\right)$ **Correct**
- $2\left(xz{e}^{xz}\operatorname{cos}⁡y+\frac{1}{yz}\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left({e}^{xz}\operatorname{cos}⁡y\right))+\frac{∂}{∂y}(2\left(0\right))+\frac{∂}{∂z}(2\left(\operatorname{ln}⁡yz\right)) \\  & =2\left(z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}\right).\end{aligned}
$$


## Original — q-105559 — moderate

Consider the vector field $F=\operatorname{cos}⁡\pi x\,i+y\operatorname{sin}⁡\pi y\,j+{e}^{2z}\,k.$ 
Evaluate $∇\cdot F$ at the point $(0,1,0).$

- $2-\pi $ **Correct**

- $\pi $

- $-\pi $

- $3-\pi $

- $1+\pi $


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(\operatorname{cos}⁡\pi x)+\frac{∂}{∂y}(y\operatorname{sin}⁡\pi y)+\frac{∂}{∂z}({e}^{2z}) \\  & =-\pi \operatorname{sin}⁡\pi x+\operatorname{sin}⁡\pi y+\pi y\operatorname{cos}⁡\pi y+2{e}^{2z}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(0,1,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(0,1,0) & =-\pi \operatorname{sin}⁡(0)+\operatorname{sin}⁡(\pi )+\pi \operatorname{cos}⁡(\pi )+2{e}^{0} \\  & =0+0-\pi +2 \\  & =2-\pi .\end{aligned}
$$

## Generated — moderate

Template: `source_q-105559`; profile: `observed_q-105559`; evidence only

Consider the vector field $F=\operatorname{cos}⁡\pi x\,i+y\operatorname{sin}⁡\pi y\,j+{e}^{2z}\,k.$ 
Evaluate $∇\cdot F$ at the point $(0,1,0).$

- $-\pi $
- $\pi $
- $2-\pi $ **Correct**
- $1+\pi $
- $3-\pi $

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(\operatorname{cos}⁡\pi x)+\frac{∂}{∂y}(y\operatorname{sin}⁡\pi y)+\frac{∂}{∂z}({e}^{2z}) \\  & =-\pi \operatorname{sin}⁡\pi x+\operatorname{sin}⁡\pi y+\pi y\operatorname{cos}⁡\pi y+2{e}^{2z}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(0,1,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(0,1,0) & =-\pi \operatorname{sin}⁡(0)+\operatorname{sin}⁡(\pi )+\pi \operatorname{cos}⁡(\pi )+2{e}^{0} \\  & =0+0-\pi +2 \\  & =2-\pi .\end{aligned}
$$

## Generated — moderate

Template: `source_q-105559`; profile: `observed_q-105559`; evidence only

Consider the vector field $F=2\left(\operatorname{cos}⁡\pi x\right)\,i+2\left(y\operatorname{sin}⁡\pi y\right)\,j+2\left({e}^{2z}\right)\,k.$ 
Evaluate $∇\cdot F$ at the point $(0,1,0).$

- $2\left(-\pi \right)$
- $2\left(\pi \right)$
- $2\left(2-\pi \right)$ **Correct**
- $2\left(1+\pi \right)$
- $2\left(3-\pi \right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
∇\cdot F=\text{div}\,F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left(\operatorname{cos}⁡\pi x\right))+\frac{∂}{∂y}(2\left(y\operatorname{sin}⁡\pi y\right))+\frac{∂}{∂z}(2\left({e}^{2z}\right)) \\  & =2\left(-\pi \operatorname{sin}⁡\pi x+\operatorname{sin}⁡\pi y+\pi y\operatorname{cos}⁡\pi y+2{e}^{2z}\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(0,1,0),$ and obtain

$$
\begin{aligned}(∇\cdot F)(0,1,0) & =2\left(-\pi \operatorname{sin}⁡(0)+\operatorname{sin}⁡(\pi )+\pi \operatorname{cos}⁡(\pi )+2{e}^{0}\right) \\  & =2\left(0+0-\pi +2\right) \\  & =2\left(2-\pi \right).\end{aligned}
$$


## Original — q-123196 — moderate

Consider the vector field $F=(x+y)^{2}\,i+(y+z)^{2}\,j+(x+z)^{2}\,k.$ Evaluate $\text{div}\,F$ at the point $(-2,1,-1).$

- $-6$

- $-8$ **Correct**

- $-4$

- $10$

- $4$


**Original worked solution**


If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((x+y)^{2})+\frac{∂}{∂y}((y+z)^{2})+\frac{∂}{∂z}((x+z)^{2}) \\  & =2(x+y)+2(y+z)+2(x+z) \\  & =4(x+y+z).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(-2,1,-1),$ and obtain

$$
\begin{aligned}\text{div}\,F(-2,1,-1) & =4((-2)+(1)+(-1)) \\  & =4\cdot (-2) \\  & =-8.\end{aligned}
$$

## Generated — moderate

Template: `source_q-123196`; profile: `observed_q-123196`; evidence only

Consider the vector field $F=(x+y)^{2}\,i+(y+z)^{2}\,j+(x+z)^{2}\,k.$ Evaluate $\text{div}\,F$ at the point $(-2,1,-1).$

- $-4$
- $-8$ **Correct**
- $-6$
- $4$
- $10$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((x+y)^{2})+\frac{∂}{∂y}((y+z)^{2})+\frac{∂}{∂z}((x+z)^{2}) \\  & =2(x+y)+2(y+z)+2(x+z) \\  & =4(x+y+z).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(-2,1,-1),$ and obtain

$$
\begin{aligned}\text{div}\,F(-2,1,-1) & =4((-2)+(1)+(-1)) \\  & =4\cdot (-2) \\  & =-8.\end{aligned}
$$

## Generated — moderate

Template: `source_q-123196`; profile: `observed_q-123196`; evidence only

Consider the vector field $F=2\left((x+y)^{2}\right)\,i+2\left((y+z)^{2}\right)\,j+2\left((x+z)^{2}\right)\,k.$ Evaluate $\text{div}\,F$ at the point $(-2,1,-1).$

- $2\left(-4\right)$
- $2\left(-8\right)$ **Correct**
- $2\left(-6\right)$
- $2\left(4\right)$
- $2\left(10\right)$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left((x+y)^{2}\right))+\frac{∂}{∂y}(2\left((y+z)^{2}\right))+\frac{∂}{∂z}(2\left((x+z)^{2}\right)) \\  & =2\left(2(x+y)+2(y+z)+2(x+z)\right) \\  & =2\left(4(x+y+z)\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(-2,1,-1),$ and obtain

$$
\begin{aligned}\text{div}\,F(-2,1,-1) & =2\left(4((-2)+(1)+(-1))\right) \\  & =2\left(4\cdot (-2)\right) \\  & =2\left(-8\right).\end{aligned}
$$

## Generated — easy

Template: `exp_sine`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨e^{x} \sin{\left(y z \right)},\,- 3 x y z,\,2⟩.$ Find $\text{div}\,F.$

- $- 3 x z$
- $e^{x} \sin{\left(y z \right)}$
- $- 3 x z + e^{x} \sin{\left(y z \right)}$ **Correct**
- $- 3 x z + e^{x} \sin{\left(y z \right)} + 2$
- $- 3 x z - e^{x} \sin{\left(y z \right)}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(e^{x} \sin{\left(y z \right)})+\frac{∂}{∂y}(- 3 x y z)+\frac{∂}{∂z}(2) \\ & =(e^{x} \sin{\left(y z \right)})+(- 3 x z)+(0) \\ & =- 3 x z + e^{x} \sin{\left(y z \right)}.\end{aligned}
$$

## Generated — easy

Template: `exp_sine`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨- 2 e^{2 x} \sin{\left(y z \right)},\,- 3 x y z,\,2⟩.$ Find $\text{div}\,F.$

- $- 3 x z$
- $- 3 x z + 4 e^{2 x} \sin{\left(y z \right)}$
- $- 3 x z - 4 e^{2 x} \sin{\left(y z \right)} + 2$
- $- 3 x z - 4 e^{2 x} \sin{\left(y z \right)}$ **Correct**
- $- 4 e^{2 x} \sin{\left(y z \right)}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 e^{2 x} \sin{\left(y z \right)})+\frac{∂}{∂y}(- 3 x y z)+\frac{∂}{∂z}(2) \\ & =(- 4 e^{2 x} \sin{\left(y z \right)})+(- 3 x z)+(0) \\ & =- 3 x z - 4 e^{2 x} \sin{\left(y z \right)}.\end{aligned}
$$

## Generated — easy

Template: `exp_sine`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨e^{x} \sin{\left(y z \right)},\,- 3 x y z,\,2⟩.$ Find $\text{div}\,F.$

$\text{div}\,F=$ {{field-1}}

- $- 3 x z + e^{x} \sin{\left(y z \right)}$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(e^{x} \sin{\left(y z \right)})+\frac{∂}{∂y}(- 3 x y z)+\frac{∂}{∂z}(2) \\ & =(e^{x} \sin{\left(y z \right)})+(- 3 x z)+(0) \\ & =- 3 x z + e^{x} \sin{\left(y z \right)}.\end{aligned}
$$

## Generated — easy

Template: `exp_sine`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨- 2 e^{2 x} \sin{\left(y z \right)},\,- 3 x y z,\,2⟩.$ Find $\text{div}\,F.$

$\text{div}\,F=$ {{field-1}}

- $- 3 x z - 4 e^{2 x} \sin{\left(y z \right)}$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 e^{2 x} \sin{\left(y z \right)})+\frac{∂}{∂y}(- 3 x y z)+\frac{∂}{∂z}(2) \\ & =(- 4 e^{2 x} \sin{\left(y z \right)})+(- 3 x z)+(0) \\ & =- 3 x z - 4 e^{2 x} \sin{\left(y z \right)}.\end{aligned}
$$

## Generated — easy

Template: `monomial`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨x y z^{2},\,x e^{y},\,- 3 y z^{3}⟩.$ Find $\text{div}\,F.$

- $- 8 y z^{2}$
- $x e^{y} - 9 y z^{2}$
- $x e^{y} - 8 y z^{2}$ **Correct**
- $- x e^{y} + 8 y z^{2}$
- $x e^{y} + y z^{2}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x y z^{2})+\frac{∂}{∂y}(x e^{y})+\frac{∂}{∂z}(- 3 y z^{3}) \\ & =(y z^{2})+(x e^{y})+(- 9 y z^{2}) \\ & =x e^{y} - 8 y z^{2}.\end{aligned}
$$

## Generated — easy

Template: `monomial`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨- 2 x y z^{2},\,2 x e^{y},\,- 3 y z^{3}⟩.$ Find $\text{div}\,F.$

- $- 11 y z^{2}$
- $2 x e^{y} - 2 y z^{2}$
- $- 2 x e^{y} + 11 y z^{2}$
- $2 x e^{y} - 11 y z^{2}$ **Correct**
- $2 x e^{y} - 9 y z^{2}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x y z^{2})+\frac{∂}{∂y}(2 x e^{y})+\frac{∂}{∂z}(- 3 y z^{3}) \\ & =(- 2 y z^{2})+(2 x e^{y})+(- 9 y z^{2}) \\ & =2 x e^{y} - 11 y z^{2}.\end{aligned}
$$

## Generated — easy

Template: `monomial`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨x y z^{2},\,x e^{y},\,- 3 y z^{3}⟩.$ Find $\text{div}\,F.$

$\text{div}\,F=$ {{field-1}}

- $x e^{y} - 8 y z^{2}$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x y z^{2})+\frac{∂}{∂y}(x e^{y})+\frac{∂}{∂z}(- 3 y z^{3}) \\ & =(y z^{2})+(x e^{y})+(- 9 y z^{2}) \\ & =x e^{y} - 8 y z^{2}.\end{aligned}
$$

## Generated — easy

Template: `monomial`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨- 2 x y z^{2},\,2 x e^{y},\,- 3 y z^{3}⟩.$ Find $\text{div}\,F.$

$\text{div}\,F=$ {{field-1}}

- $2 x e^{y} - 11 y z^{2}$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x y z^{2})+\frac{∂}{∂y}(2 x e^{y})+\frac{∂}{∂z}(- 3 y z^{3}) \\ & =(- 2 y z^{2})+(2 x e^{y})+(- 9 y z^{2}) \\ & =2 x e^{y} - 11 y z^{2}.\end{aligned}
$$

## Generated — easy

Template: `shared_square`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨\left(- x + 2 y + z\right)^{2},\,\left(- x + 2 y + z\right)^{2},\,\left(- x + 2 y + z\right)^{2}⟩.$ Find $\text{div}\,F.$

- $0$
- $- 6 x + 12 y + 6 z$
- $- 4 x + 8 y + 4 z$ **Correct**
- $4 x - 8 y - 4 z$
- $- 2 x + 4 y + 2 z$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(\left(- x + 2 y + z\right)^{2})+\frac{∂}{∂y}(\left(- x + 2 y + z\right)^{2})+\frac{∂}{∂z}(\left(- x + 2 y + z\right)^{2}) \\ & =(2 x - 4 y - 2 z)+(- 4 x + 8 y + 4 z)+(- 2 x + 4 y + 2 z) \\ & =- 4 x + 8 y + 4 z.\end{aligned}
$$

## Generated — easy

Template: `shared_square`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨\left(- 2 x + 2 y - 3 z\right)^{2},\,\left(- 2 x + 2 y - 3 z\right)^{2},\,\left(- 2 x + 2 y - 3 z\right)^{2}⟩.$ Find $\text{div}\,F.$

- $20 x - 20 y + 30 z$
- $0$
- $- 12 x + 12 y - 18 z$
- $12 x - 12 y + 18 z$ **Correct**
- $4 x - 4 y + 6 z$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(\left(- 2 x + 2 y - 3 z\right)^{2})+\frac{∂}{∂y}(\left(- 2 x + 2 y - 3 z\right)^{2})+\frac{∂}{∂z}(\left(- 2 x + 2 y - 3 z\right)^{2}) \\ & =(8 x - 8 y + 12 z)+(- 8 x + 8 y - 12 z)+(12 x - 12 y + 18 z) \\ & =12 x - 12 y + 18 z.\end{aligned}
$$

## Generated — easy

Template: `shared_square`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨\left(x + y - 3 z\right)^{2},\,\left(x + y - 3 z\right)^{2},\,\left(x + y - 3 z\right)^{2}⟩.$ Find $\text{div}\,F.$

$\text{div}\,F=$ {{field-1}}

- $- 2 x - 2 y + 6 z$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(\left(x + y - 3 z\right)^{2})+\frac{∂}{∂y}(\left(x + y - 3 z\right)^{2})+\frac{∂}{∂z}(\left(x + y - 3 z\right)^{2}) \\ & =(2 x + 2 y - 6 z)+(2 x + 2 y - 6 z)+(- 6 x - 6 y + 18 z) \\ & =- 2 x - 2 y + 6 z.\end{aligned}
$$

## Generated — easy

Template: `shared_square`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨\left(- 2 x + 2 y - 3 z\right)^{2},\,\left(- 2 x + 2 y - 3 z\right)^{2},\,\left(- 2 x + 2 y - 3 z\right)^{2}⟩.$ Find $\text{div}\,F.$

$\text{div}\,F=$ {{field-1}}

- $12 x - 12 y + 18 z$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(\left(- 2 x + 2 y - 3 z\right)^{2})+\frac{∂}{∂y}(\left(- 2 x + 2 y - 3 z\right)^{2})+\frac{∂}{∂z}(\left(- 2 x + 2 y - 3 z\right)^{2}) \\ & =(8 x - 8 y + 12 z)+(- 8 x + 8 y - 12 z)+(12 x - 12 y + 18 z) \\ & =12 x - 12 y + 18 z.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_monomial`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨- 2 x^{2} y z,\,- 3 x y^{2} z,\,2 x y z^{2}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,-1,1).$

- $0$
- $2$
- $6$ **Correct**
- $-6$
- $10$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x^{2} y z)+\frac{∂}{∂y}(- 3 x y^{2} z)+\frac{∂}{∂z}(2 x y z^{2}) \\ & =(- 4 x y z)+(- 6 x y z)+(4 x y z) \\ & =- 6 x y z.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,-1,1),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,-1,1) & =(- 4 (1) (-1) (1))+(- 6 (1) (-1) (1))+(4 (1) (-1) (1)) \\ & =(4)+(6)+(-4) \\ & =6.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_monomial`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨- 2 x^{2} y z,\,2 x y^{2} z,\,- 3 x y z^{2}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,-2,2).$

- $40$
- $0$
- $-24$
- $24$ **Correct**
- $8$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x^{2} y z)+\frac{∂}{∂y}(2 x y^{2} z)+\frac{∂}{∂z}(- 3 x y z^{2}) \\ & =(- 4 x y z)+(4 x y z)+(- 6 x y z) \\ & =- 6 x y z.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,-2,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,-2,2) & =(- 4 (1) (-2) (2))+(4 (1) (-2) (2))+(- 6 (1) (-2) (2)) \\ & =(16)+(-16)+(24) \\ & =24.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_monomial`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨x^{2} y z,\,x y^{2} z,\,- 3 x y z^{2}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,2,2).$

{{field-1}}

- $-8$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x^{2} y z)+\frac{∂}{∂y}(x y^{2} z)+\frac{∂}{∂z}(- 3 x y z^{2}) \\ & =(2 x y z)+(2 x y z)+(- 6 x y z) \\ & =- 2 x y z.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,2,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,2,2) & =(2 (1) (2) (2))+(2 (1) (2) (2))+(- 6 (1) (2) (2)) \\ & =(8)+(8)+(-24) \\ & =-8.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_monomial`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨- 2 x^{2} y z,\,2 x y^{2} z,\,- 3 x y z^{2}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,-2,2).$

{{field-1}}

- $24$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x^{2} y z)+\frac{∂}{∂y}(2 x y^{2} z)+\frac{∂}{∂z}(- 3 x y z^{2}) \\ & =(- 4 x y z)+(4 x y z)+(- 6 x y z) \\ & =- 6 x y z.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,-2,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,-2,2) & =(- 4 (1) (-2) (2))+(4 (1) (-2) (2))+(- 6 (1) (-2) (2)) \\ & =(16)+(-16)+(24) \\ & =24.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_square`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨\left(x + y\right)^{2},\,\left(y + z\right)^{2},\,- 3 \left(x + z\right)^{2}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,2,2).$

- $-12$
- $-10$
- $-4$ **Correct**
- $4$
- $14$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(\left(x + y\right)^{2})+\frac{∂}{∂y}(\left(y + z\right)^{2})+\frac{∂}{∂z}(- 3 \left(x + z\right)^{2}) \\ & =(2 x + 2 y)+(2 y + 2 z)+(- 6 x - 6 z) \\ & =- 4 x + 4 y - 4 z.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,2,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,2,2) & =(2 (1) + 2 (2))+(2 (2) + 2 (2))+(- 6 (1) - 6 (2)) \\ & =(6)+(8)+(-18) \\ & =-4.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_square`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨- \left(x + y\right)^{2},\,3 \left(y + z\right)^{2},\,- 2 \left(x + z\right)^{2}⟩.$ Evaluate $\text{div}\,F$ at the point $(-2,1,-2).$

- $18$
- $-4$
- $-12$
- $12$ **Correct**
- $10$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- \left(x + y\right)^{2})+\frac{∂}{∂y}(3 \left(y + z\right)^{2})+\frac{∂}{∂z}(- 2 \left(x + z\right)^{2}) \\ & =(- 2 x - 2 y)+(6 y + 6 z)+(- 4 x - 4 z) \\ & =- 6 x + 4 y + 2 z.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(-2,1,-2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(-2,1,-2) & =(- 2 (-2) - 2 (1))+(6 (1) + 6 (-2))+(- 4 (-2) - 4 (-2)) \\ & =(2)+(-6)+(16) \\ & =12.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_square`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨\left(x + y\right)^{2},\,\left(y + z\right)^{2},\,- 3 \left(x + z\right)^{2}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,2,2).$

{{field-1}}

- $-4$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(\left(x + y\right)^{2})+\frac{∂}{∂y}(\left(y + z\right)^{2})+\frac{∂}{∂z}(- 3 \left(x + z\right)^{2}) \\ & =(2 x + 2 y)+(2 y + 2 z)+(- 6 x - 6 z) \\ & =- 4 x + 4 y - 4 z.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,2,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,2,2) & =(2 (1) + 2 (2))+(2 (2) + 2 (2))+(- 6 (1) - 6 (2)) \\ & =(6)+(8)+(-18) \\ & =-4.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_square`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨- \left(x + y\right)^{2},\,3 \left(y + z\right)^{2},\,- 2 \left(x + z\right)^{2}⟩.$ Evaluate $\text{div}\,F$ at the point $(-2,1,-2).$

{{field-1}}

- $12$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- \left(x + y\right)^{2})+\frac{∂}{∂y}(3 \left(y + z\right)^{2})+\frac{∂}{∂z}(- 2 \left(x + z\right)^{2}) \\ & =(- 2 x - 2 y)+(6 y + 6 z)+(- 4 x - 4 z) \\ & =- 6 x + 4 y + 2 z.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(-2,1,-2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(-2,1,-2) & =(- 2 (-2) - 2 (1))+(6 (1) + 6 (-2))+(- 4 (-2) - 4 (-2)) \\ & =(2)+(-6)+(16) \\ & =12.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_exp_trig`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨x z \cos{\left(y \right)},\,x^{2} y,\,- 3 x z^{2} e^{y}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,0,2).$

- $-10$
- $-11$
- $-9$ **Correct**
- $9$
- $3$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x z \cos{\left(y \right)})+\frac{∂}{∂y}(x^{2} y)+\frac{∂}{∂z}(- 3 x z^{2} e^{y}) \\ & =(z \cos{\left(y \right)})+(x^{2})+(- 6 x z e^{y}) \\ & =x^{2} - 6 x z e^{y} + z \cos{\left(y \right)}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,2) & =((2) \cos{\left((0) \right)})+((1)^{2})+(- 6 (1) (2) e^{(0)}) \\ & =(2)+(1)+(-12) \\ & =-9.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_exp_trig`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨- 2 x z \cos{\left(y \right)},\,2 x^{2} y,\,- 3 x z^{2} e^{y}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,0,-2).$

- $16$
- $6$
- $-18$
- $18$ **Correct**
- $14$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x z \cos{\left(y \right)})+\frac{∂}{∂y}(2 x^{2} y)+\frac{∂}{∂z}(- 3 x z^{2} e^{y}) \\ & =(- 2 z \cos{\left(y \right)})+(2 x^{2})+(- 6 x z e^{y}) \\ & =2 x^{2} - 6 x z e^{y} - 2 z \cos{\left(y \right)}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,-2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,-2) & =(- 2 (-2) \cos{\left((0) \right)})+(2 (1)^{2})+(- 6 (1) (-2) e^{(0)}) \\ & =(4)+(2)+(12) \\ & =18.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_exp_trig`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨x z \cos{\left(y \right)},\,x^{2} y,\,- 3 x z^{2} e^{y}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,0,2).$

{{field-1}}

- $-9$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x z \cos{\left(y \right)})+\frac{∂}{∂y}(x^{2} y)+\frac{∂}{∂z}(- 3 x z^{2} e^{y}) \\ & =(z \cos{\left(y \right)})+(x^{2})+(- 6 x z e^{y}) \\ & =x^{2} - 6 x z e^{y} + z \cos{\left(y \right)}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,2) & =((2) \cos{\left((0) \right)})+((1)^{2})+(- 6 (1) (2) e^{(0)}) \\ & =(2)+(1)+(-12) \\ & =-9.\end{aligned}
$$

## Generated — moderate

Template: `evaluated_exp_trig`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨- 2 x z \cos{\left(y \right)},\,2 x^{2} y,\,- 3 x z^{2} e^{y}⟩.$ Evaluate $\text{div}\,F$ at the point $(1,0,-2).$

{{field-1}}

- $18$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x z \cos{\left(y \right)})+\frac{∂}{∂y}(2 x^{2} y)+\frac{∂}{∂z}(- 3 x z^{2} e^{y}) \\ & =(- 2 z \cos{\left(y \right)})+(2 x^{2})+(- 6 x z e^{y}) \\ & =2 x^{2} - 6 x z e^{y} - 2 z \cos{\left(y \right)}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(1,0,-2),$ and obtain

$$
\begin{aligned}(∇\cdot F)(1,0,-2) & =(- 2 (-2) \cos{\left((0) \right)})+(2 (1)^{2})+(- 6 (1) (-2) e^{(0)}) \\ & =(4)+(2)+(12) \\ & =18.\end{aligned}
$$

## Generated — hard

Template: `product_exp`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨x^{2} e^{x y},\,y e^{- 3 y z},\,z \left(x + y z\right)^{2}⟩.$ Find $\text{div}\,F.$

- $x^{2} y e^{x y} + x^{2} + 4 x y z + 2 x e^{x y} + 3 y^{2} z^{2}$
- $x^{2} + 4 x y z + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}$
- $x^{2} y e^{x y} + x^{2} + 4 x y z + 2 x e^{x y} + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}$ **Correct**
- $- x^{2} y e^{x y} - x^{2} - 4 x y z - 2 x e^{x y} - 3 y^{2} z^{2} + 3 y z e^{- 3 y z} - e^{- 3 y z}$
- $x^{2} y e^{x y} + x^{2} + 4 x y z + 2 x e^{x y} + 3 y^{2} z^{2} - 2 y z \left(x + y z\right) - 3 y z e^{- 3 y z} - \left(x + y z\right)^{2} + e^{- 3 y z}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x^{2} e^{x y})+\frac{∂}{∂y}(y e^{- 3 y z})+\frac{∂}{∂z}(z \left(x + y z\right)^{2}) \\ & =(x^{2} y e^{x y} + 2 x e^{x y})+(- 3 y z e^{- 3 y z} + e^{- 3 y z})+(2 y z \left(x + y z\right) + \left(x + y z\right)^{2}) \\ & =x^{2} y e^{x y} + x^{2} + 4 x y z + 2 x e^{x y} + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}.\end{aligned}
$$

## Generated — hard

Template: `product_exp`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨- 2 x^{2} e^{2 x y},\,y e^{- 3 y z},\,z \left(x + y z\right)^{2}⟩.$ Find $\text{div}\,F.$

- $- 4 x^{2} y e^{2 x y} + x^{2} + 4 x y z - 4 x e^{2 x y} + 3 y^{2} z^{2}$
- $- 4 x^{2} y e^{2 x y} + x^{2} + 4 x y z - 4 x e^{2 x y} + 3 y^{2} z^{2} - 2 y z \left(x + y z\right) - 3 y z e^{- 3 y z} - \left(x + y z\right)^{2} + e^{- 3 y z}$
- $4 x^{2} y e^{2 x y} - x^{2} - 4 x y z + 4 x e^{2 x y} - 3 y^{2} z^{2} + 3 y z e^{- 3 y z} - e^{- 3 y z}$
- $- 4 x^{2} y e^{2 x y} + x^{2} + 4 x y z - 4 x e^{2 x y} + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}$ **Correct**
- $x^{2} + 4 x y z + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x^{2} e^{2 x y})+\frac{∂}{∂y}(y e^{- 3 y z})+\frac{∂}{∂z}(z \left(x + y z\right)^{2}) \\ & =(- 4 x^{2} y e^{2 x y} - 4 x e^{2 x y})+(- 3 y z e^{- 3 y z} + e^{- 3 y z})+(2 y z \left(x + y z\right) + \left(x + y z\right)^{2}) \\ & =- 4 x^{2} y e^{2 x y} + x^{2} + 4 x y z - 4 x e^{2 x y} + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}.\end{aligned}
$$

## Generated — hard

Template: `product_exp`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨x^{2} e^{x y},\,y e^{- 3 y z},\,z \left(x + y z\right)^{2}⟩.$ Find $\text{div}\,F.$

$\text{div}\,F=$ {{field-1}}

- $x^{2} y e^{x y} + x^{2} + 4 x y z + 2 x e^{x y} + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x^{2} e^{x y})+\frac{∂}{∂y}(y e^{- 3 y z})+\frac{∂}{∂z}(z \left(x + y z\right)^{2}) \\ & =(x^{2} y e^{x y} + 2 x e^{x y})+(- 3 y z e^{- 3 y z} + e^{- 3 y z})+(2 y z \left(x + y z\right) + \left(x + y z\right)^{2}) \\ & =x^{2} y e^{x y} + x^{2} + 4 x y z + 2 x e^{x y} + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}.\end{aligned}
$$

## Generated — hard

Template: `product_exp`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨- 2 x^{2} e^{2 x y},\,y e^{- 3 y z},\,z \left(x + y z\right)^{2}⟩.$ Find $\text{div}\,F.$

$\text{div}\,F=$ {{field-1}}

- $- 4 x^{2} y e^{2 x y} + x^{2} + 4 x y z - 4 x e^{2 x y} + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x^{2} e^{2 x y})+\frac{∂}{∂y}(y e^{- 3 y z})+\frac{∂}{∂z}(z \left(x + y z\right)^{2}) \\ & =(- 4 x^{2} y e^{2 x y} - 4 x e^{2 x y})+(- 3 y z e^{- 3 y z} + e^{- 3 y z})+(2 y z \left(x + y z\right) + \left(x + y z\right)^{2}) \\ & =- 4 x^{2} y e^{2 x y} + x^{2} + 4 x y z - 4 x e^{2 x y} + 3 y^{2} z^{2} - 3 y z e^{- 3 y z} + e^{- 3 y z}.\end{aligned}
$$

## Generated — hard

Template: `product_log`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨x^{2} \sin{\left(x y \right)},\,y e^{- 3 y z},\,z \ln{\left(x z + 2 \right)}⟩.$ Find $\text{div}\,F.$ Assume $2+xz>0.$

- $x^{2} y \cos{\left(x y \right)} + \frac{x z}{x z + 2} + 2 x \sin{\left(x y \right)} + \ln{\left(x z + 2 \right)}$
- $\frac{x z}{x z + 2} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}$
- $x^{2} y \cos{\left(x y \right)} + \frac{x z}{x z + 2} + 2 x \sin{\left(x y \right)} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}$ **Correct**
- $- x^{2} y \cos{\left(x y \right)} - \frac{x z}{x z + 2} - 2 x \sin{\left(x y \right)} + 3 y z e^{- 3 y z} - \ln{\left(x z + 2 \right)} - e^{- 3 y z}$
- $x^{2} y \cos{\left(x y \right)} + 2 x \sin{\left(x y \right)} - 3 y z e^{- 3 y z} + e^{- 3 y z}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x^{2} \sin{\left(x y \right)})+\frac{∂}{∂y}(y e^{- 3 y z})+\frac{∂}{∂z}(z \ln{\left(x z + 2 \right)}) \\ & =(x^{2} y \cos{\left(x y \right)} + 2 x \sin{\left(x y \right)})+(- 3 y z e^{- 3 y z} + e^{- 3 y z})+(\frac{x z}{x z + 2} + \ln{\left(x z + 2 \right)}) \\ & =x^{2} y \cos{\left(x y \right)} + \frac{x z}{x z + 2} + 2 x \sin{\left(x y \right)} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}.\end{aligned}
$$

## Generated — hard

Template: `product_log`; profile: `authored_omission_sign`; authored eligible

Consider the vector field $F=⟨- 2 x^{2} \sin{\left(2 x y \right)},\,y e^{- 3 y z},\,z \ln{\left(x z + 2 \right)}⟩.$ Find $\text{div}\,F.$ Assume $2+xz>0.$

- $- 4 x^{2} y \cos{\left(2 x y \right)} + \frac{x z}{x z + 2} - 4 x \sin{\left(2 x y \right)} + \ln{\left(x z + 2 \right)}$
- $- 4 x^{2} y \cos{\left(2 x y \right)} - 4 x \sin{\left(2 x y \right)} - 3 y z e^{- 3 y z} + e^{- 3 y z}$
- $4 x^{2} y \cos{\left(2 x y \right)} - \frac{x z}{x z + 2} + 4 x \sin{\left(2 x y \right)} + 3 y z e^{- 3 y z} - \ln{\left(x z + 2 \right)} - e^{- 3 y z}$
- $- 4 x^{2} y \cos{\left(2 x y \right)} + \frac{x z}{x z + 2} - 4 x \sin{\left(2 x y \right)} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}$ **Correct**
- $\frac{x z}{x z + 2} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}$

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x^{2} \sin{\left(2 x y \right)})+\frac{∂}{∂y}(y e^{- 3 y z})+\frac{∂}{∂z}(z \ln{\left(x z + 2 \right)}) \\ & =(- 4 x^{2} y \cos{\left(2 x y \right)} - 4 x \sin{\left(2 x y \right)})+(- 3 y z e^{- 3 y z} + e^{- 3 y z})+(\frac{x z}{x z + 2} + \ln{\left(x z + 2 \right)}) \\ & =- 4 x^{2} y \cos{\left(2 x y \right)} + \frac{x z}{x z + 2} - 4 x \sin{\left(2 x y \right)} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}.\end{aligned}
$$

## Generated — hard

Template: `product_log`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨x^{2} \sin{\left(x y \right)},\,y e^{- 3 y z},\,z \ln{\left(x z + 2 \right)}⟩.$ Find $\text{div}\,F.$ Assume $2+xz>0.$

$\text{div}\,F=$ {{field-1}}

- $x^{2} y \cos{\left(x y \right)} + \frac{x z}{x z + 2} + 2 x \sin{\left(x y \right)} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(x^{2} \sin{\left(x y \right)})+\frac{∂}{∂y}(y e^{- 3 y z})+\frac{∂}{∂z}(z \ln{\left(x z + 2 \right)}) \\ & =(x^{2} y \cos{\left(x y \right)} + 2 x \sin{\left(x y \right)})+(- 3 y z e^{- 3 y z} + e^{- 3 y z})+(\frac{x z}{x z + 2} + \ln{\left(x z + 2 \right)}) \\ & =x^{2} y \cos{\left(x y \right)} + \frac{x z}{x z + 2} + 2 x \sin{\left(x y \right)} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}.\end{aligned}
$$

## Generated — hard

Template: `product_log`; profile: `authored_blank`; authored eligible

Consider the vector field $F=⟨- 2 x^{2} \sin{\left(2 x y \right)},\,y e^{- 3 y z},\,z \ln{\left(x z + 2 \right)}⟩.$ Find $\text{div}\,F.$ Assume $2+xz>0.$

$\text{div}\,F=$ {{field-1}}

- $- 4 x^{2} y \cos{\left(2 x y \right)} + \frac{x z}{x z + 2} - 4 x \sin{\left(2 x y \right)} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}∇\cdot F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\ & =\frac{∂}{∂x}(- 2 x^{2} \sin{\left(2 x y \right)})+\frac{∂}{∂y}(y e^{- 3 y z})+\frac{∂}{∂z}(z \ln{\left(x z + 2 \right)}) \\ & =(- 4 x^{2} y \cos{\left(2 x y \right)} - 4 x \sin{\left(2 x y \right)})+(- 3 y z e^{- 3 y z} + e^{- 3 y z})+(\frac{x z}{x z + 2} + \ln{\left(x z + 2 \right)}) \\ & =- 4 x^{2} y \cos{\left(2 x y \right)} + \frac{x z}{x z + 2} - 4 x \sin{\left(2 x y \right)} - 3 y z e^{- 3 y z} + \ln{\left(x z + 2 \right)} + e^{- 3 y z}.\end{aligned}
$$

## Generated — easy

Template: `zero_terms`; profile: `supported_blank_q-168615`; authored eligible

Consider the vector field $F=⟨(-3)\left({z}^{2}\right),\,(-3)\left(2xy\right),\,(-3)\left(x{y}^{2}\right)⟩.$

$\text{div}\,F\,=$

                            
                                    
                            
                                        {{field-1}}

- $(-3)\left(2x\right)$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}\text{div}F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((-3)\left({z}^{2}\right))+\frac{∂}{∂y}((-3)\left(2xy\right))+\frac{∂}{∂z}((-3)\left(x{y}^{2}\right)) \\  & =(-3)\left(0+2x+0\right) \\  & =(-3)\left(2x\right).\end{aligned}
$$

## Generated — easy

Template: `zero_terms`; profile: `supported_blank_q-168615`; authored eligible

Consider the vector field $F=⟨(-1)\left({z}^{2}\right),\,(-1)\left(2xy\right),\,(-1)\left(x{y}^{2}\right)⟩.$

$\text{div}\,F\,=$

                            
                                    
                            
                                        {{field-1}}

- $(-1)\left(2x\right)$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}\text{div}F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((-1)\left({z}^{2}\right))+\frac{∂}{∂y}((-1)\left(2xy\right))+\frac{∂}{∂z}((-1)\left(x{y}^{2}\right)) \\  & =(-1)\left(0+2x+0\right) \\  & =(-1)\left(2x\right).\end{aligned}
$$

## Generated — easy

Template: `zero_terms`; profile: `supported_blank_q-168615`; authored eligible

Consider the vector field $F=⟨{z}^{2},\,2xy,\,x{y}^{2}⟩.$

$\text{div}\,F\,=$

                            
                                    
                            
                                        {{field-1}}

- $2x$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}\text{div}F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}({z}^{2})+\frac{∂}{∂y}(2xy)+\frac{∂}{∂z}(x{y}^{2}) \\  & =0+2x+0 \\  & =2x.\end{aligned}
$$

## Generated — easy

Template: `zero_terms`; profile: `supported_blank_q-168615`; authored eligible

Consider the vector field $F=⟨2\left({z}^{2}\right),\,2\left(2xy\right),\,2\left(x{y}^{2}\right)⟩.$

$\text{div}\,F\,=$

                            
                                    
                            
                                        {{field-1}}

- $2\left(2x\right)$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}\text{div}F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left({z}^{2}\right))+\frac{∂}{∂y}(2\left(2xy\right))+\frac{∂}{∂z}(2\left(x{y}^{2}\right)) \\  & =2\left(0+2x+0\right) \\  & =2\left(2x\right).\end{aligned}
$$

## Generated — easy

Template: `zero_terms`; profile: `supported_blank_q-168615`; authored eligible

Consider the vector field $F=⟨3\left({z}^{2}\right),\,3\left(2xy\right),\,3\left(x{y}^{2}\right)⟩.$

$\text{div}\,F\,=$

                            
                                    
                            
                                        {{field-1}}

- $3\left(2x\right)$ **Correct**

**Worked solution**

If $F=P\,i+Q\,j+R\,k$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=∇\cdot F=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

  

Therefore, we have

$$
\begin{aligned}\text{div}F & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(3\left({z}^{2}\right))+\frac{∂}{∂y}(3\left(2xy\right))+\frac{∂}{∂z}(3\left(x{y}^{2}\right)) \\  & =3\left(0+2x+0\right) \\  & =3\left(2x\right).\end{aligned}
$$

## Generated — easy

Template: `axial`; profile: `supported_blank_q-168624`; authored eligible

Consider the vector field $G=⟨(-3)\left(0\right),\,(-3)\left(0\right),\,(-3)\left(-xy-2{z}^{2}\right)⟩.$

$∇\cdot G=\,$

                            
                                    
                            
                                        {{field-1}}

- $(-3)\left(-4z\right)$ **Correct**

**Worked solution**

If $G=P\,\text{i}+Q\,\text{j}+R\,\text{k}$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $G$ all exist, then the divergence of $G$ is the scalar field given by

$$
∇\cdot G=\text{div}\,G=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

Therefore, we have

$$
\begin{aligned}∇\cdot G & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((-3)\left(0\right))+\frac{∂}{∂y}((-3)\left(0\right))+\frac{∂}{∂z}((-3)\left(-xy-2{z}^{2}\right)) \\  & =(-3)\left(-4z\right).\end{aligned}
$$

## Generated — easy

Template: `axial`; profile: `supported_blank_q-168624`; authored eligible

Consider the vector field $G=⟨(-1)\left(0\right),\,(-1)\left(0\right),\,(-1)\left(-xy-2{z}^{2}\right)⟩.$

$∇\cdot G=\,$

                            
                                    
                            
                                        {{field-1}}

- $(-1)\left(-4z\right)$ **Correct**

**Worked solution**

If $G=P\,\text{i}+Q\,\text{j}+R\,\text{k}$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $G$ all exist, then the divergence of $G$ is the scalar field given by

$$
∇\cdot G=\text{div}\,G=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

Therefore, we have

$$
\begin{aligned}∇\cdot G & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}((-1)\left(0\right))+\frac{∂}{∂y}((-1)\left(0\right))+\frac{∂}{∂z}((-1)\left(-xy-2{z}^{2}\right)) \\  & =(-1)\left(-4z\right).\end{aligned}
$$

## Generated — easy

Template: `axial`; profile: `supported_blank_q-168624`; authored eligible

Consider the vector field $G=⟨0,\,0,\,-xy-2{z}^{2}⟩.$

$∇\cdot G=\,$

                            
                                    
                            
                                        {{field-1}}

- $-4z$ **Correct**

**Worked solution**

If $G=P\,\text{i}+Q\,\text{j}+R\,\text{k}$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $G$ all exist, then the divergence of $G$ is the scalar field given by

$$
∇\cdot G=\text{div}\,G=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

Therefore, we have

$$
\begin{aligned}∇\cdot G & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(0)+\frac{∂}{∂y}(0)+\frac{∂}{∂z}(-xy-2{z}^{2}) \\  & =-4z.\end{aligned}
$$

## Generated — easy

Template: `axial`; profile: `supported_blank_q-168624`; authored eligible

Consider the vector field $G=⟨2\left(0\right),\,2\left(0\right),\,2\left(-xy-2{z}^{2}\right)⟩.$

$∇\cdot G=\,$

                            
                                    
                            
                                        {{field-1}}

- $2\left(-4z\right)$ **Correct**

**Worked solution**

If $G=P\,\text{i}+Q\,\text{j}+R\,\text{k}$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $G$ all exist, then the divergence of $G$ is the scalar field given by

$$
∇\cdot G=\text{div}\,G=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

Therefore, we have

$$
\begin{aligned}∇\cdot G & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(2\left(0\right))+\frac{∂}{∂y}(2\left(0\right))+\frac{∂}{∂z}(2\left(-xy-2{z}^{2}\right)) \\  & =2\left(-4z\right).\end{aligned}
$$

## Generated — easy

Template: `axial`; profile: `supported_blank_q-168624`; authored eligible

Consider the vector field $G=⟨3\left(0\right),\,3\left(0\right),\,3\left(-xy-2{z}^{2}\right)⟩.$

$∇\cdot G=\,$

                            
                                    
                            
                                        {{field-1}}

- $3\left(-4z\right)$ **Correct**

**Worked solution**

If $G=P\,\text{i}+Q\,\text{j}+R\,\text{k}$ is a vector field on ${R}^{3}$ and the partial derivatives of the components of $G$ all exist, then the divergence of $G$ is the scalar field given by

$$
∇\cdot G=\text{div}\,G=\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}.
$$

Therefore, we have

$$
\begin{aligned}∇\cdot G & =\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z} \\  & =\frac{∂}{∂x}(3\left(0\right))+\frac{∂}{∂y}(3\left(0\right))+\frac{∂}{∂z}(3\left(-xy-2{z}^{2}\right)) \\  & =3\left(-4z\right).\end{aligned}
$$
