# Original and generated review

Each original is a public parameterized raw replay; source errors remain visibly documented. Generated examples use eligible method banks.

## Original replay: sqrt_product

Given $f(x,y,z)=\sqrt{xyz}$, find $∇f(x,y,z).$

1. $\frac{\sqrt{xyz}}{2}(\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k)$
2. $\frac{xyz}{2}(\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k)$
3. $\sqrt{xyz}(x\text{ }i+y\text{ }j+z\text{ }k)$
4. $\sqrt{xyz}(\frac{1}{yz}\text{ }i+\frac{1}{xz}\text{ }j+\frac{1}{xz}\text{ }k)$
5. $\frac{\sqrt{xyz}}{2}(x\text{ }i+y\text{ }j+z\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{xyz}) \\  & =\frac{1}{2\sqrt{xyz}}\cdot (yz) \\  & =\frac{\sqrt{xyz}}{2x} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{xyz}) \\  & =\frac{1}{2\sqrt{xyz}}\cdot (xz) \\  & =\frac{\sqrt{xyz}}{2y} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{xyz}) \\  & =\frac{1}{2\sqrt{xyz}}\cdot (xy) \\  & =\frac{\sqrt{xyz}}{2z}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{\sqrt{xyz}}{2x}\text{ }i+\frac{\sqrt{xyz}}{2y}\text{ }j+\frac{\sqrt{xyz}}{2z}\text{ }k \\  & =\frac{\sqrt{xyz}}{2}(\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k)\end{aligned}
$$

## Original replay: root_log

Find $∇g(x,y,z)$ given that  $g(x,y,z)=\sqrt{x+2}+\operatorname{ln}⁡(\sqrt{yz}).$

1. $\frac{1}{2\sqrt{x+2}}i+\frac{1}{2\sqrt{y}}\text{ }j+\frac{1}{2\sqrt{z}}\text{ }k$
2. $\frac{1}{\sqrt{x+2}}i+\frac{1}{yz}\text{ }j+\frac{1}{yz}\text{ }k$
3. $\frac{1}{2\sqrt{x+2}}i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k$
4. $\frac{1}{\sqrt{x+2}}i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k$
5. $\frac{1}{2\sqrt{x+2}}i+\frac{1}{2yz}\text{ }j+\frac{1}{2yz}\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{x+2}+\operatorname{ln}⁡(\sqrt{yz})) \\  & =\frac{1}{2\sqrt{x+2}}+0 \\  & =\frac{1}{2\sqrt{x+2}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{x+2}+\operatorname{ln}⁡(\sqrt{yz})) \\  & =0+\frac{1}{\sqrt{yz}}\cdot \frac{1}{2\sqrt{yz}}\cdot z \\  & =\frac{1}{2y} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{x+2}+\operatorname{ln}⁡(\sqrt{yz})) \\  & =0+\frac{1}{\sqrt{yz}}\cdot \frac{1}{2\sqrt{yz}}\cdot y \\  & =\frac{1}{2z}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =\frac{1}{2\sqrt{x+2}}i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k\end{aligned}
$$

## Original replay: log_point

Evaluate $∇f(x,y,z)$ at the point $(2,3,1)$ if $f(x,y,z)=\operatorname{ln}⁡(\sqrt{xyz}).$

1. $\frac{1}{4}\text{ }i+\frac{1}{6}\text{ }j+\frac{1}{2}\text{ }k$
2. $\frac{1}{2}\text{ }i+\frac{\sqrt{6}}{6}\text{ }j-\frac{\sqrt{2}}{2}\text{ }k$
3. $\frac{1}{2}\text{ }i+\frac{1}{3}\text{ }j+k$
4. $\frac{1}{2}\text{ }i+\frac{1}{3}\text{ }j-k$
5. $4\text{ }i+6\text{ }j-2\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot yz \\  & =\frac{1}{2x} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xz \\  & =\frac{1}{2y} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xy \\  & =\frac{1}{2z}\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{x}(x,y,z)\text{ }j+{f}_{x}(x,y,z)\text{ }k \\  & =\frac{1}{2x}\text{ }i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k \\ ∇f(2,3,1) & =\frac{1}{2\cdot 2}\text{ }i+\frac{1}{2\cdot 3}\text{ }j+\frac{1}{2\cdot 1}\text{ }k \\  & =\frac{1}{4}\text{ }i+\frac{1}{6}\text{ }j+\frac{1}{2}\text{ }k.\end{aligned}
$$

## Original replay: product_log

Given $h(x,y,z)=xy\operatorname{ln}⁡(z)$, find $∇h(x,y,z).$

1. $y\operatorname{ln}⁡(z)\text{ }i+xy\text{ }j+\frac{xy}{z}\text{ }k$
2. $x\operatorname{ln}⁡(z)\text{ }i+y\operatorname{ln}⁡(z)\text{ }j+xy\operatorname{ln}⁡(z)\text{ }k$
3. $y\operatorname{ln}⁡(yz+zx)\text{ }i+y\operatorname{ln}⁡(yz+zx)\text{ }j+\frac{xy}{z}\text{ }k$
4. $y\operatorname{ln}⁡(z)\text{ }i+x\operatorname{ln}⁡(z)\text{ }j+\frac{xy}{z}\text{ }k$
5. $xy\operatorname{ln}⁡(z)\text{ }i+xy\operatorname{ln}⁡(z)\text{ }j+\frac{xy}{z}\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(xy\operatorname{ln}⁡(z)) \\  & =y\operatorname{ln}⁡(z) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(xy\operatorname{ln}⁡(z)) \\  & =x\operatorname{ln}⁡(z) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(xy\operatorname{ln}⁡(z)) \\  & =xy\cdot \frac{1}{z} \\  & =\frac{xy}{z}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & =y\operatorname{ln}⁡(z)\text{ }i+x\operatorname{ln}⁡(z)\text{ }j+\frac{xy}{z}\text{ }k\end{aligned}
$$

## Original replay: power_exp

Find $∇g(x,y,z)$ given that  $g(x,y,z)={x}^{2}{y}^{2}{z}^{2}+{e}^{xyz}.$

1. $(2x{y}^{2}{z}^{2}+yz{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+xz{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+xy{e}^{xyz})\text{ }k$
2. $(2x+yz{e}^{xyz})\text{ }i+(2y+xz{e}^{xyz})\text{ }j+(2z+xy{e}^{xyz})\text{ }k$
3. $(2x{y}^{2}{z}^{2}+{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+{e}^{xyz})\text{ }k$
4. $(2x{y}^{2}{z}^{2}+x{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+y{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+z{e}^{xyz})\text{ }k$
5. $(x{y}^{2}{z}^{2}+yz{e}^{xyz-1})\text{ }i+({x}^{2}y{z}^{2}+xz{e}^{xyz-1})\text{ }j+({x}^{2}{y}^{2}z+xy{e}^{xyz-1})\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({x}^{2}{y}^{2}{z}^{2}+{e}^{xyz}) \\  & =2x{y}^{2}{z}^{2}+yz{e}^{xyz} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({x}^{2}{y}^{2}{z}^{2}+{e}^{xyz}) \\  & =2{x}^{2}y{z}^{2}+xz{e}^{xyz} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({x}^{2}{y}^{2}{z}^{2}+{e}^{xyz}) \\  & =2{x}^{2}{y}^{2}z+xy{e}^{xyz}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =(2x{y}^{2}{z}^{2}+yz{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+xz{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+xy{e}^{xyz})\text{ }k\end{aligned}
$$

## Original replay: variable_power

If $f(x,y,z)={x}^{y}+{y}^{z},$ find $∇f(x,y,z).$

1. ${x}^{y}\operatorname{ln}⁡y\,i+{x}^{y}\operatorname{ln}⁡x\,j+({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})k$
2. $y{x}^{y-1}\,i+z{y}^{z-1}\,j+{y}^{z}\operatorname{ln}⁡y\,k$
3. $y{x}^{y-1}\,i+({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})j+{y}^{z}\operatorname{ln}⁡y\,k$
4. $y{x}^{y-1}\,i+z{y}^{z-1}\,j+z{y}^{z-1}\,k$
5. $({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})i+{x}^{y}\operatorname{ln}⁡y\,j+{y}^{z}\operatorname{ln}⁡z\,k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}({x}^{y}+{y}^{z}) \\  & =y{x}^{y-1} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}({x}^{y}+{y}^{z}) \\  & ={x}^{y}\operatorname{ln}⁡x+z{y}^{z-1} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}({x}^{y}+{y}^{z}) \\  & ={y}^{z}\operatorname{ln}⁡y\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\,j+{f}_{z}(x,y,z)\,k \\  & =y{x}^{y-1}\,i+({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})j+{y}^{z}\operatorname{ln}⁡y\,k.\end{aligned}
$$

## Original replay: expcos_point

Evaluate $∇h(x,y,z)$ at the point $(\frac{1}{2},1,\pi )$ if $h(x,y,z)={e}^{xy}\operatorname{cos}⁡(yz).$

1. $\sqrt{e}(-i+\pi \,j-k)$
2. $e(i-\frac{1}{2}\,j+k)$
3. $e(i-\frac{1}{2}\,j)$
4. $-\sqrt{e}(i+\frac{1}{2}\,j)$
5. $-\sqrt{e}(i+\pi \,j-k)$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =y{e}^{xy}\operatorname{cos}⁡(yz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =x{e}^{xy}\operatorname{cos}⁡(yz)+{e}^{xy}(-\operatorname{sin}⁡(yz))(z) \\  & ={e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz)) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =-y{e}^{xy}\operatorname{sin}⁡(yz)\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\,i+{h}_{x}(x,y,z)\,j+{h}_{x}(x,y,z)\,k \\  & =y{e}^{xy}\operatorname{cos}⁡(yz)\,i+{e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y{e}^{xy}\operatorname{sin}⁡(yz)\,k \\  & ={e}^{xy}(y\operatorname{cos}⁡(yz)\,i+(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y\operatorname{sin}⁡(yz)\,k) \\ ∇h(\frac{1}{2},1,\pi ) & ={e}^{(1/2)(1)}(1\operatorname{cos}⁡(1\pi )\,i+(\frac{1}{2}\operatorname{cos}⁡(1\pi )-\pi \operatorname{sin}⁡(1\pi ))\,j-1\operatorname{sin}⁡(1\pi )\,k) \\  & =\sqrt{e}(-i-\frac{1}{2}\,j-0\,k) \\  & =-\sqrt{e}(i+\frac{1}{2}\,j).\end{aligned}
$$

## Original replay: exp_sin

Given  $g(x,y,z)={e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)$, find $∇g(x,y,z).$

1. $z\operatorname{sin}⁡({y}^{2}-1)i+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\operatorname{sin}⁡({y}^{2}-1)\text{ }k$
2. $2{e}^{2xz}\text{ }(zi+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\text{ }k)$
3. $2{e}^{2xz}\text{ }(z\operatorname{sin}⁡({y}^{2}-1)i+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\operatorname{sin}⁡({y}^{2}-1)\text{ }k)$
4. $2{e}^{2xz}\text{ }(zi+y\text{ }j+x\text{ }k)$
5. $2{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)\text{ }(zi+y\text{ }j+x\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)) \\  & =2z{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1) \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)) \\  & =2y{e}^{2xz}\operatorname{cos}⁡({y}^{2}-1) \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)) \\  & =2x{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1).\end{aligned}
$$

Hence, the gradient is: 

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =2z{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)\text{ }i+2y{e}^{2xz}\operatorname{cos}⁡({y}^{2}-1)\text{ }j+2x{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)\text{ }k \\  & =2{e}^{2xz}\text{ }(z\operatorname{sin}⁡({y}^{2}-1)i+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\operatorname{sin}⁡({y}^{2}-1)\text{ }k)\end{aligned}
$$

## Original replay: composite_log

Given $h(x,y,z)=xyz\operatorname{ln}⁡(xyz)$, find  $∇h(x,y,z).$

1. $(\operatorname{ln}⁡(xyz)+1)(x\text{ }i+y\text{ }j+z\text{ }k)$
2. $(\operatorname{ln}⁡(xyz)+1)(yz\text{ }i+xz\text{ }j+xy\text{ }k)$
3. $yz\text{ }i+xz\text{ }j+xy\text{ }k$
4. $(\operatorname{ln}⁡(xyz)+1)(\text{ }i+\text{ }j+\text{ }k)$
5. $\operatorname{ln}⁡(xyz)(yz\text{ }i+xz\text{ }j+xy\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(xyz\operatorname{ln}⁡(xyz)) \\  & =yz\operatorname{ln}⁡(xyz)+xyz\frac{yz}{xyz} \\  & =yz(\operatorname{ln}⁡(xyz)+1) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(xyz\operatorname{ln}⁡(xyz)) \\  & =xz\operatorname{ln}⁡(xyz)+xyz\frac{xz}{xyz} \\  & =xz(\operatorname{ln}⁡(xyz)+1) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(xyz\operatorname{ln}⁡(xyz)) \\  & =xy\operatorname{ln}⁡(xyz)+xyz\frac{xy}{xyz} \\  & =xy(\operatorname{ln}⁡(xyz)+1)\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & =yz(\operatorname{ln}⁡(xyz)+1)\text{ }i+xz(\operatorname{ln}⁡(xyz)+1)\text{ }j+xy(\operatorname{ln}⁡(xyz)+1)\text{ }k \\  & =(\operatorname{ln}⁡(xyz)+1)(yz\text{ }i+xz\text{ }j+xy\text{ }k).\end{aligned}
$$

## Original replay: sine_point

Evaluate $∇h(x,y,z)$ at the point $(1,-1,\pi )$ if $h(x,y,z)=\operatorname{sin}⁡(xyz).$

1. $\pi \text{ }i+\pi \text{ }j+\text{ }k$
2. $\pi \text{ }i+\pi \text{ }j+\pi \text{ }k$
3. $\pi \text{ }i-\pi \text{ }j+\text{ }k$
4. $-\pi \text{ }i+\pi \text{ }j+\text{ }k$
5. $\text{ }i-\pi \text{ }j+\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{sin}⁡(xyz)) \\  & =yz\operatorname{cos}⁡(xyz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{sin}⁡(xyz)) \\  & =xz\operatorname{cos}⁡(xyz) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{sin}⁡(xyz)) \\  & =xy\operatorname{cos}⁡(xyz)\end{aligned}
$$

 
Hence, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{x}(x,y,z)\text{ }j+{h}_{x}(x,y,z)\text{ }k \\  & =yz\operatorname{cos}⁡(xyz)\text{ }i+xz\operatorname{cos}⁡(xyz)\text{ }j+xy\operatorname{cos}⁡(xyz)\text{ }k \\ ∇h(1,-1,\pi ) & =(-1)(\pi )\operatorname{cos}⁡(-\pi )\text{ }i+(1)(\pi )\operatorname{cos}⁡(-\pi )\text{ }j+(1)(-1)\operatorname{cos}⁡(-\pi )\text{ }k \\  & =(-\pi )(-1)\text{ }i+\pi (-1)\text{ }j-(-1)\text{ }k \\  & =\pi \text{ }i-\pi \text{ }j+\text{ }k\end{aligned}
$$

## Generated easy: polynomial

Find $∇g(x,y,z)$ given that $g(x,y,z)=x^{2} + 4 y^{3} + 5 z^{2}.$

1. $(2 x)\,\mathbf i+(12 y^{2})\,\mathbf j+(- 10 z)\,\mathbf k$
2. $(2 x)\,\mathbf i+(- 12 y^{2})\,\mathbf j+(10 z)\,\mathbf k$
3. $(2 x)\,\mathbf i+(12 y^{2})\,\mathbf j+(10 z)\,\mathbf k$
4. $(- 2 x)\,\mathbf i+(12 y^{2})\,\mathbf j+(10 z)\,\mathbf k$
5. $(x)\,\mathbf i+(4 y^{2})\,\mathbf j+(5 z)\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(x^{2} + 4 y^{3} + 5 z^{2}) \\  & =(2 x)+(0)+(0) \\  & =2 x \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(x^{2} + 4 y^{3} + 5 z^{2}) \\  & =(0)+(12 y^{2})+(0) \\  & =12 y^{2} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(x^{2} + 4 y^{3} + 5 z^{2}) \\  & =(0)+(0)+(10 z) \\  & =10 z\end{aligned}
$$

Therefore, the gradient is

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\,\mathbf i+{g}_{y}(x,y,z)\,\mathbf j+{g}_{z}(x,y,z)\,\mathbf k \\  & =(2 x)\,\mathbf i+(12 y^{2})\,\mathbf j+(10 z)\,\mathbf k\end{aligned}
$$

## Generated easy: polynomial

Find $∇g(x,y,z)$ given that $g(x,y,z)=- 4 x^{3} + 5 y^{3} - 3 z^{3}.$

1. $(- 12 x^{2})\,\mathbf i+(15 y^{2})\,\mathbf j+(- 9 z^{2})\,\mathbf k$
2. $(- 12 x^{2})\,\mathbf i+(- 15 y^{2})\,\mathbf j+(- 9 z^{2})\,\mathbf k$
3. $(12 x^{2})\,\mathbf i+(15 y^{2})\,\mathbf j+(- 9 z^{2})\,\mathbf k$
4. $(- 4 x^{2})\,\mathbf i+(5 y^{2})\,\mathbf j+(- 3 z^{2})\,\mathbf k$
5. $(- 12 x^{2})\,\mathbf i+(15 y^{2})\,\mathbf j+(9 z^{2})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(- 4 x^{3} + 5 y^{3} - 3 z^{3}) \\  & =(- 12 x^{2})+(0)+(0) \\  & =- 12 x^{2} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(- 4 x^{3} + 5 y^{3} - 3 z^{3}) \\  & =(0)+(15 y^{2})+(0) \\  & =15 y^{2} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(- 4 x^{3} + 5 y^{3} - 3 z^{3}) \\  & =(0)+(0)+(- 9 z^{2}) \\  & =- 9 z^{2}\end{aligned}
$$

Therefore, the gradient is

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\,\mathbf i+{g}_{y}(x,y,z)\,\mathbf j+{g}_{z}(x,y,z)\,\mathbf k \\  & =(- 12 x^{2})\,\mathbf i+(15 y^{2})\,\mathbf j+(- 9 z^{2})\,\mathbf k\end{aligned}
$$

## Generated moderate: sqrt_product

Given $f(x,y,z)=\sqrt{{(x-1)}{(y+1)}{(z+1)}}$, find $∇f(x,y,z).$

1. $(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}}{x - 1})\,\mathbf i+(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}}{y + 1})\,\mathbf j+(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}}{z + 1})\,\mathbf k$
2. $(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)} \left(x - 1\right)}{2})\,\mathbf i+(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)} \left(y + 1\right)}{2})\,\mathbf j+(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)} \left(z + 1\right)}{2})\,\mathbf k$
3. $(\frac{1}{2 \sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}})\,\mathbf i+(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}}{2 y + 2})\,\mathbf j+(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}}{2 z + 2})\,\mathbf k$
4. $(\frac{\left(y + 1\right) \left(z + 1\right)}{2})\,\mathbf i+(\frac{\left(x - 1\right) \left(z + 1\right)}{2})\,\mathbf j+(\frac{\left(x - 1\right) \left(y + 1\right)}{2})\,\mathbf k$
5. $(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}}{2 \left(x - 1\right)})\,\mathbf i+(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}}{2 \left(y + 1\right)})\,\mathbf j+(\frac{\sqrt{\left(x - 1\right) \left(y + 1\right) \left(z + 1\right)}}{2 \left(z + 1\right)})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{{(x-1)}{(y+1)}{(z+1)}}) \\  & =\frac{1}{2\sqrt{{(x-1)}{(y+1)}{(z+1)}}}\cdot ({(y+1)}{(z+1)}) \\  & =\frac{\sqrt{{(x-1)}{(y+1)}{(z+1)}}}{2{(x-1)}} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{{(x-1)}{(y+1)}{(z+1)}}) \\  & =\frac{1}{2\sqrt{{(x-1)}{(y+1)}{(z+1)}}}\cdot ({(x-1)}{(z+1)}) \\  & =\frac{\sqrt{{(x-1)}{(y+1)}{(z+1)}}}{2{(y+1)}} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{{(x-1)}{(y+1)}{(z+1)}}) \\  & =\frac{1}{2\sqrt{{(x-1)}{(y+1)}{(z+1)}}}\cdot ({(x-1)}{(y+1)}) \\  & =\frac{\sqrt{{(x-1)}{(y+1)}{(z+1)}}}{2{(z+1)}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{\sqrt{{(x-1)}{(y+1)}{(z+1)}}}{2{(x-1)}}\text{ }i+\frac{\sqrt{{(x-1)}{(y+1)}{(z+1)}}}{2{(y+1)}}\text{ }j+\frac{\sqrt{{(x-1)}{(y+1)}{(z+1)}}}{2{(z+1)}}\text{ }k \\  & =\frac{\sqrt{{(x-1)}{(y+1)}{(z+1)}}}{2}(\frac{1}{{(x-1)}}\text{ }i+\frac{1}{{(y+1)}}\text{ }j+\frac{1}{{(z+1)}}\text{ }k)\end{aligned}
$$

## Generated moderate: sqrt_product

Given $f(x,y,z)=\sqrt{{(x-3)}{(y+3)}{(z+1)}}$, find $∇f(x,y,z).$

1. $(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}}{2 \left(x - 3\right)})\,\mathbf i+(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}}{2 \left(y + 3\right)})\,\mathbf j+(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}}{2 \left(z + 1\right)})\,\mathbf k$
2. $(\frac{1}{2 \sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}})\,\mathbf i+(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}}{2 y + 6})\,\mathbf j+(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}}{2 z + 2})\,\mathbf k$
3. $(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)} \left(x - 3\right)}{2})\,\mathbf i+(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)} \left(y + 3\right)}{2})\,\mathbf j+(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)} \left(z + 1\right)}{2})\,\mathbf k$
4. $(\frac{\left(y + 3\right) \left(z + 1\right)}{2})\,\mathbf i+(\frac{\left(x - 3\right) \left(z + 1\right)}{2})\,\mathbf j+(\frac{\left(x - 3\right) \left(y + 3\right)}{2})\,\mathbf k$
5. $(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}}{x - 3})\,\mathbf i+(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}}{y + 3})\,\mathbf j+(\frac{\sqrt{\left(x - 3\right) \left(y + 3\right) \left(z + 1\right)}}{z + 1})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{{(x-3)}{(y+3)}{(z+1)}}) \\  & =\frac{1}{2\sqrt{{(x-3)}{(y+3)}{(z+1)}}}\cdot ({(y+3)}{(z+1)}) \\  & =\frac{\sqrt{{(x-3)}{(y+3)}{(z+1)}}}{2{(x-3)}} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{{(x-3)}{(y+3)}{(z+1)}}) \\  & =\frac{1}{2\sqrt{{(x-3)}{(y+3)}{(z+1)}}}\cdot ({(x-3)}{(z+1)}) \\  & =\frac{\sqrt{{(x-3)}{(y+3)}{(z+1)}}}{2{(y+3)}} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{{(x-3)}{(y+3)}{(z+1)}}) \\  & =\frac{1}{2\sqrt{{(x-3)}{(y+3)}{(z+1)}}}\cdot ({(x-3)}{(y+3)}) \\  & =\frac{\sqrt{{(x-3)}{(y+3)}{(z+1)}}}{2{(z+1)}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{\sqrt{{(x-3)}{(y+3)}{(z+1)}}}{2{(x-3)}}\text{ }i+\frac{\sqrt{{(x-3)}{(y+3)}{(z+1)}}}{2{(y+3)}}\text{ }j+\frac{\sqrt{{(x-3)}{(y+3)}{(z+1)}}}{2{(z+1)}}\text{ }k \\  & =\frac{\sqrt{{(x-3)}{(y+3)}{(z+1)}}}{2}(\frac{1}{{(x-3)}}\text{ }i+\frac{1}{{(y+3)}}\text{ }j+\frac{1}{{(z+1)}}\text{ }k)\end{aligned}
$$

## Generated historical bank evidence only: sqrt_product

Given $f(x,y,z)=\sqrt{{(x+2)}{(y-1)}{(z+3)}}$, find $∇f(x,y,z).$

1. $\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2}(\frac{1}{{(x+2)}}\text{ }i+\frac{1}{{(y-1)}}\text{ }j+\frac{1}{{(z+3)}}\text{ }k)$
2. $\frac{{(x+2)}{(y-1)}{(z+3)}}{2}(\frac{1}{{(x+2)}}\text{ }i+\frac{1}{{(y-1)}}\text{ }j+\frac{1}{{(z+3)}}\text{ }k)$
3. $\sqrt{{(x+2)}{(y-1)}{(z+3)}}({(x+2)}\text{ }i+{(y-1)}\text{ }j+{(z+3)}\text{ }k)$
4. $\sqrt{{(x+2)}{(y-1)}{(z+3)}}(\frac{1}{{(y-1)}{(z+3)}}\text{ }i+\frac{1}{{(x+2)}{(z+3)}}\text{ }j+\frac{1}{{(x+2)}{(z+3)}}\text{ }k)$
5. $\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2}({(x+2)}\text{ }i+{(y-1)}\text{ }j+{(z+3)}\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{{(x+2)}{(y-1)}{(z+3)}}) \\  & =\frac{1}{2\sqrt{{(x+2)}{(y-1)}{(z+3)}}}\cdot ({(y-1)}{(z+3)}) \\  & =\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2{(x+2)}} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{{(x+2)}{(y-1)}{(z+3)}}) \\  & =\frac{1}{2\sqrt{{(x+2)}{(y-1)}{(z+3)}}}\cdot ({(x+2)}{(z+3)}) \\  & =\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2{(y-1)}} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{{(x+2)}{(y-1)}{(z+3)}}) \\  & =\frac{1}{2\sqrt{{(x+2)}{(y-1)}{(z+3)}}}\cdot ({(x+2)}{(y-1)}) \\  & =\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2{(z+3)}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2{(x+2)}}\text{ }i+\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2{(y-1)}}\text{ }j+\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2{(z+3)}}\text{ }k \\  & =\frac{\sqrt{{(x+2)}{(y-1)}{(z+3)}}}{2}(\frac{1}{{(x+2)}}\text{ }i+\frac{1}{{(y-1)}}\text{ }j+\frac{1}{{(z+3)}}\text{ }k)\end{aligned}
$$

## Generated moderate: root_log

Find $∇g(x,y,z)$ given that  $g(x,y,z)=\sqrt{{(x-1)}+2}+\operatorname{ln}⁡(\sqrt{{(y+1)}{(z+1)}}).$

1. $\frac{1}{\sqrt{{(x-1)}+2}}i+\frac{1}{{(y+1)}{(z+1)}}\text{ }j+\frac{1}{{(y+1)}{(z+1)}}\text{ }k$
2. $\frac{1}{2\sqrt{{(x-1)}+2}}i+\frac{1}{2{(y+1)}{(z+1)}}\text{ }j+\frac{1}{2{(y+1)}{(z+1)}}\text{ }k$
3. $\frac{1}{\sqrt{{(x-1)}+2}}i+\frac{1}{{(y+1)}}\text{ }j+\frac{1}{{(z+1)}}\text{ }k$
4. $\frac{1}{2\sqrt{{(x-1)}+2}}i+\frac{1}{2\sqrt{{(y+1)}}}\text{ }j+\frac{1}{2\sqrt{{(z+1)}}}\text{ }k$
5. $\frac{1}{2\sqrt{{(x-1)}+2}}i+\frac{1}{2{(y+1)}}\text{ }j+\frac{1}{2{(z+1)}}\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{{(x-1)}+2}+\operatorname{ln}⁡(\sqrt{{(y+1)}{(z+1)}})) \\  & =\frac{1}{2\sqrt{{(x-1)}+2}}+0 \\  & =\frac{1}{2\sqrt{{(x-1)}+2}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{{(x-1)}+2}+\operatorname{ln}⁡(\sqrt{{(y+1)}{(z+1)}})) \\  & =0+\frac{1}{\sqrt{{(y+1)}{(z+1)}}}\cdot \frac{1}{2\sqrt{{(y+1)}{(z+1)}}}\cdot {(z+1)} \\  & =\frac{1}{2{(y+1)}} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{{(x-1)}+2}+\operatorname{ln}⁡(\sqrt{{(y+1)}{(z+1)}})) \\  & =0+\frac{1}{\sqrt{{(y+1)}{(z+1)}}}\cdot \frac{1}{2\sqrt{{(y+1)}{(z+1)}}}\cdot {(y+1)} \\  & =\frac{1}{2{(z+1)}}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =\frac{1}{2\sqrt{{(x-1)}+2}}i+\frac{1}{2{(y+1)}}\text{ }j+\frac{1}{2{(z+1)}}\text{ }k\end{aligned}
$$

## Generated moderate: root_log

Find $∇g(x,y,z)$ given that  $g(x,y,z)=\sqrt{{(x-3)}+2}+\operatorname{ln}⁡(\sqrt{{(y+3)}{(z+1)}}).$

1. $\frac{1}{2\sqrt{{(x-3)}+2}}i+\frac{1}{2{(y+3)}}\text{ }j+\frac{1}{2{(z+1)}}\text{ }k$
2. $\frac{1}{\sqrt{{(x-3)}+2}}i+\frac{1}{{(y+3)}}\text{ }j+\frac{1}{{(z+1)}}\text{ }k$
3. $\frac{1}{2\sqrt{{(x-3)}+2}}i+\frac{1}{2{(y+3)}{(z+1)}}\text{ }j+\frac{1}{2{(y+3)}{(z+1)}}\text{ }k$
4. $\frac{1}{2\sqrt{{(x-3)}+2}}i+\frac{1}{2\sqrt{{(y+3)}}}\text{ }j+\frac{1}{2\sqrt{{(z+1)}}}\text{ }k$
5. $\frac{1}{\sqrt{{(x-3)}+2}}i+\frac{1}{{(y+3)}{(z+1)}}\text{ }j+\frac{1}{{(y+3)}{(z+1)}}\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{{(x-3)}+2}+\operatorname{ln}⁡(\sqrt{{(y+3)}{(z+1)}})) \\  & =\frac{1}{2\sqrt{{(x-3)}+2}}+0 \\  & =\frac{1}{2\sqrt{{(x-3)}+2}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{{(x-3)}+2}+\operatorname{ln}⁡(\sqrt{{(y+3)}{(z+1)}})) \\  & =0+\frac{1}{\sqrt{{(y+3)}{(z+1)}}}\cdot \frac{1}{2\sqrt{{(y+3)}{(z+1)}}}\cdot {(z+1)} \\  & =\frac{1}{2{(y+3)}} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{{(x-3)}+2}+\operatorname{ln}⁡(\sqrt{{(y+3)}{(z+1)}})) \\  & =0+\frac{1}{\sqrt{{(y+3)}{(z+1)}}}\cdot \frac{1}{2\sqrt{{(y+3)}{(z+1)}}}\cdot {(y+3)} \\  & =\frac{1}{2{(z+1)}}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =\frac{1}{2\sqrt{{(x-3)}+2}}i+\frac{1}{2{(y+3)}}\text{ }j+\frac{1}{2{(z+1)}}\text{ }k\end{aligned}
$$

## Generated historical bank evidence only: root_log

Find $∇g(x,y,z)$ given that  $g(x,y,z)=\sqrt{{(x+2)}+2}+\operatorname{ln}⁡(\sqrt{{(y-1)}{(z+3)}}).$

1. $\frac{1}{2\sqrt{{(x+2)}+2}}i+\frac{1}{2\sqrt{{(y-1)}}}\text{ }j+\frac{1}{2\sqrt{{(z+3)}}}\text{ }k$
2. $\frac{1}{\sqrt{{(x+2)}+2}}i+\frac{1}{{(y-1)}{(z+3)}}\text{ }j+\frac{1}{{(y-1)}{(z+3)}}\text{ }k$
3. $\frac{1}{2\sqrt{{(x+2)}+2}}i+\frac{1}{2{(y-1)}}\text{ }j+\frac{1}{2{(z+3)}}\text{ }k$
4. $\frac{1}{\sqrt{{(x+2)}+2}}i+\frac{1}{{(y-1)}}\text{ }j+\frac{1}{{(z+3)}}\text{ }k$
5. $\frac{1}{2\sqrt{{(x+2)}+2}}i+\frac{1}{2{(y-1)}{(z+3)}}\text{ }j+\frac{1}{2{(y-1)}{(z+3)}}\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{{(x+2)}+2}+\operatorname{ln}⁡(\sqrt{{(y-1)}{(z+3)}})) \\  & =\frac{1}{2\sqrt{{(x+2)}+2}}+0 \\  & =\frac{1}{2\sqrt{{(x+2)}+2}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{{(x+2)}+2}+\operatorname{ln}⁡(\sqrt{{(y-1)}{(z+3)}})) \\  & =0+\frac{1}{\sqrt{{(y-1)}{(z+3)}}}\cdot \frac{1}{2\sqrt{{(y-1)}{(z+3)}}}\cdot {(z+3)} \\  & =\frac{1}{2{(y-1)}} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{{(x+2)}+2}+\operatorname{ln}⁡(\sqrt{{(y-1)}{(z+3)}})) \\  & =0+\frac{1}{\sqrt{{(y-1)}{(z+3)}}}\cdot \frac{1}{2\sqrt{{(y-1)}{(z+3)}}}\cdot {(y-1)} \\  & =\frac{1}{2{(z+3)}}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =\frac{1}{2\sqrt{{(x+2)}+2}}i+\frac{1}{2{(y-1)}}\text{ }j+\frac{1}{2{(z+3)}}\text{ }k\end{aligned}
$$

## Generated moderate: log_point

Evaluate $∇f(x,y,z)$ at the point $(3,5,5)$ if $f(x,y,z)=\operatorname{ln}⁡(\sqrt{xyz}).$

1. $(\frac{1}{3})\,\mathbf i+(\frac{1}{5})\,\mathbf j+(\frac{1}{5})\,\mathbf k$
2. $(\frac{1}{6})\,\mathbf i+(- \frac{1}{10})\,\mathbf j+(\frac{1}{10})\,\mathbf k$
3. $(\frac{1}{6})\,\mathbf i+(\frac{1}{10})\,\mathbf j+(- \frac{1}{10})\,\mathbf k$
4. $(- \frac{1}{6})\,\mathbf i+(\frac{1}{10})\,\mathbf j+(\frac{1}{10})\,\mathbf k$
5. $(\frac{1}{6})\,\mathbf i+(\frac{1}{10})\,\mathbf j+(\frac{1}{10})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot yz \\  & =\frac{1}{2x} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xz \\  & =\frac{1}{2y} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xy \\  & =\frac{1}{2z}\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{1}{2x}\text{ }i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k \\ ∇f(3,5,5) & =\frac{1}{2\cdot 3}\text{ }i+\frac{1}{2\cdot 5}\text{ }j+\frac{1}{2\cdot 5}\text{ }k \\  & =\frac{1}{6}\text{ }i+\frac{1}{10}\text{ }j+\frac{1}{10}\text{ }k.\end{aligned}
$$

## Generated moderate: log_point

Evaluate $∇f(x,y,z)$ at the point $(1,5,6)$ if $f(x,y,z)=\operatorname{ln}⁡(\sqrt{xyz}).$

1. $(\frac{1}{2})\,\mathbf i+(\frac{1}{10})\,\mathbf j+(\frac{1}{12})\,\mathbf k$
2. $(\frac{1}{2})\,\mathbf i+(\frac{1}{10})\,\mathbf j+(- \frac{1}{12})\,\mathbf k$
3. $(\frac{1}{2})\,\mathbf i+(- \frac{1}{10})\,\mathbf j+(\frac{1}{12})\,\mathbf k$
4. $(- \frac{1}{2})\,\mathbf i+(\frac{1}{10})\,\mathbf j+(\frac{1}{12})\,\mathbf k$
5. $(1)\,\mathbf i+(\frac{1}{5})\,\mathbf j+(\frac{1}{6})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot yz \\  & =\frac{1}{2x} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xz \\  & =\frac{1}{2y} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xy \\  & =\frac{1}{2z}\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{1}{2x}\text{ }i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k \\ ∇f(1,5,6) & =\frac{1}{2\cdot 1}\text{ }i+\frac{1}{2\cdot 5}\text{ }j+\frac{1}{2\cdot 6}\text{ }k \\  & =\frac{1}{2}\text{ }i+\frac{1}{10}\text{ }j+\frac{1}{12}\text{ }k.\end{aligned}
$$

## Generated historical bank evidence only: log_point

Evaluate $∇f(x,y,z)$ at the point $(4,2,3)$ if $f(x,y,z)=\operatorname{ln}⁡(\sqrt{xyz}).$

1. $\frac{1}{8}\text{ }i+\frac{1}{4}\text{ }j+\frac{1}{6}\text{ }k$
2. $\frac{1}{4}\text{ }i+\frac{\sqrt{2}}{4}\text{ }j-\frac{1}{6}\text{ }k$
3. $\frac{1}{4}\text{ }i+\frac{1}{2}\text{ }j+\frac{1}{3}\text{ }k$
4. $\frac{1}{4}\text{ }i+\frac{1}{2}\text{ }j-\frac{1}{3}\text{ }k$
5. $8\text{ }i+4\text{ }j-6\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot yz \\  & =\frac{1}{2x} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xz \\  & =\frac{1}{2y} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xy \\  & =\frac{1}{2z}\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{x}(x,y,z)\text{ }j+{f}_{x}(x,y,z)\text{ }k \\  & =\frac{1}{2x}\text{ }i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k \\ ∇f(4,2,3) & =\frac{1}{2\cdot 4}\text{ }i+\frac{1}{2\cdot 2}\text{ }j+\frac{1}{2\cdot 3}\text{ }k \\  & =\frac{1}{8}\text{ }i+\frac{1}{4}\text{ }j+\frac{1}{6}\text{ }k.\end{aligned}
$$

## Generated moderate: product_log

Given $h(x,y,z)={(x-1)}{(y+1)}\operatorname{ln}⁡({(z+1)})$, find $∇h(x,y,z).$

1. $(\left(x - 1\right) \left(y + 1\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(x - 1\right) \left(y + 1\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\frac{\left(x - 1\right) \left(y + 1\right)}{z + 1})\,\mathbf k$
2. $(\left(y + 1\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(x - 1\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\left(x - 1\right) \left(y + 1\right) \ln{\left(z + 1 \right)})\,\mathbf k$
3. $(\left(x - 1\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(y + 1\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\frac{\left(x - 1\right) \left(y + 1\right)}{z + 1})\,\mathbf k$
4. $(\left(y + 1\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(x - 1\right) \left(y + 1\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\frac{\left(x - 1\right) \left(y + 1\right)}{z + 1})\,\mathbf k$
5. $(\left(y + 1\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(x - 1\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\frac{\left(x - 1\right) \left(y + 1\right)}{z + 1})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({(x-1)}{(y+1)}\operatorname{ln}⁡({(z+1)})) \\  & ={(y+1)}\operatorname{ln}⁡({(z+1)}) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({(x-1)}{(y+1)}\operatorname{ln}⁡({(z+1)})) \\  & ={(x-1)}\operatorname{ln}⁡({(z+1)}) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({(x-1)}{(y+1)}\operatorname{ln}⁡({(z+1)})) \\  & ={(x-1)}{(y+1)}\cdot \frac{1}{{(z+1)}} \\  & =\frac{{(x-1)}{(y+1)}}{{(z+1)}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & ={(y+1)}\operatorname{ln}⁡({(z+1)})\text{ }i+{(x-1)}\operatorname{ln}⁡({(z+1)})\text{ }j+\frac{{(x-1)}{(y+1)}}{{(z+1)}}\text{ }k\end{aligned}
$$

## Generated moderate: product_log

Given $h(x,y,z)={(x-3)}{(y+3)}\operatorname{ln}⁡({(z+1)})$, find $∇h(x,y,z).$

1. $(\left(y + 3\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(x - 3\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\frac{\left(x - 3\right) \left(y + 3\right)}{z + 1})\,\mathbf k$
2. $(\left(x - 3\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(y + 3\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\frac{\left(x - 3\right) \left(y + 3\right)}{z + 1})\,\mathbf k$
3. $(\left(y + 3\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(x - 3\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\left(x - 3\right) \left(y + 3\right) \ln{\left(z + 1 \right)})\,\mathbf k$
4. $(\left(y + 3\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(x - 3\right) \left(y + 3\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\frac{\left(x - 3\right) \left(y + 3\right)}{z + 1})\,\mathbf k$
5. $(\left(x - 3\right) \left(y + 3\right) \ln{\left(z + 1 \right)})\,\mathbf i+(\left(x - 3\right) \left(y + 3\right) \ln{\left(z + 1 \right)})\,\mathbf j+(\frac{\left(x - 3\right) \left(y + 3\right)}{z + 1})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({(x-3)}{(y+3)}\operatorname{ln}⁡({(z+1)})) \\  & ={(y+3)}\operatorname{ln}⁡({(z+1)}) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({(x-3)}{(y+3)}\operatorname{ln}⁡({(z+1)})) \\  & ={(x-3)}\operatorname{ln}⁡({(z+1)}) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({(x-3)}{(y+3)}\operatorname{ln}⁡({(z+1)})) \\  & ={(x-3)}{(y+3)}\cdot \frac{1}{{(z+1)}} \\  & =\frac{{(x-3)}{(y+3)}}{{(z+1)}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & ={(y+3)}\operatorname{ln}⁡({(z+1)})\text{ }i+{(x-3)}\operatorname{ln}⁡({(z+1)})\text{ }j+\frac{{(x-3)}{(y+3)}}{{(z+1)}}\text{ }k\end{aligned}
$$

## Generated historical bank evidence only: product_log

Given $h(x,y,z)={(x+2)}{(y-1)}\operatorname{ln}⁡({(z+3)})$, find $∇h(x,y,z).$

1. ${(y-1)}\operatorname{ln}⁡({(z+3)})\text{ }i+{(x+2)}{(y-1)}\text{ }j+\frac{{(x+2)}{(y-1)}}{{(z+3)}}\text{ }k$
2. ${(x+2)}\operatorname{ln}⁡({(z+3)})\text{ }i+{(y-1)}\operatorname{ln}⁡({(z+3)})\text{ }j+{(x+2)}{(y-1)}\operatorname{ln}⁡({(z+3)})\text{ }k$
3. ${(y-1)}\operatorname{ln}⁡({(y-1)}{(z+3)}+{(z+3)}{(x+2)})\text{ }i+{(y-1)}\operatorname{ln}⁡({(y-1)}{(z+3)}+{(z+3)}{(x+2)})\text{ }j+\frac{{(x+2)}{(y-1)}}{{(z+3)}}\text{ }k$
4. ${(y-1)}\operatorname{ln}⁡({(z+3)})\text{ }i+{(x+2)}\operatorname{ln}⁡({(z+3)})\text{ }j+\frac{{(x+2)}{(y-1)}}{{(z+3)}}\text{ }k$
5. ${(x+2)}{(y-1)}\operatorname{ln}⁡({(z+3)})\text{ }i+{(x+2)}{(y-1)}\operatorname{ln}⁡({(z+3)})\text{ }j+\frac{{(x+2)}{(y-1)}}{{(z+3)}}\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({(x+2)}{(y-1)}\operatorname{ln}⁡({(z+3)})) \\  & ={(y-1)}\operatorname{ln}⁡({(z+3)}) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({(x+2)}{(y-1)}\operatorname{ln}⁡({(z+3)})) \\  & ={(x+2)}\operatorname{ln}⁡({(z+3)}) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({(x+2)}{(y-1)}\operatorname{ln}⁡({(z+3)})) \\  & ={(x+2)}{(y-1)}\cdot \frac{1}{{(z+3)}} \\  & =\frac{{(x+2)}{(y-1)}}{{(z+3)}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & ={(y-1)}\operatorname{ln}⁡({(z+3)})\text{ }i+{(x+2)}\operatorname{ln}⁡({(z+3)})\text{ }j+\frac{{(x+2)}{(y-1)}}{{(z+3)}}\text{ }k\end{aligned}
$$

## Generated moderate: power_exp

Find $∇g(x,y,z)$ given that  $g(x,y,z)={{(x-1)}}^{2}{{(y+1)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-1)}{(y+1)}{(z+1)}}.$

1. $(2{(x-1)}+{(y+1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }i+(2{(y+1)}+{(x-1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }j+(2{(z+1)}+{(x-1)}{(y+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }k$
2. $({(x-1)}{{(y+1)}}^{2}{{(z+1)}}^{2}+{(y+1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}-1})\text{ }i+({{(x-1)}}^{2}{(y+1)}{{(z+1)}}^{2}+{(x-1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}-1})\text{ }j+({{(x-1)}}^{2}{{(y+1)}}^{2}{(z+1)}+{(x-1)}{(y+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}-1})\text{ }k$
3. $(2{(x-1)}{{(y+1)}}^{2}{{(z+1)}}^{2}+{(x-1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }i+(2{{(x-1)}}^{2}{(y+1)}{{(z+1)}}^{2}+{(y+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }j+(2{{(x-1)}}^{2}{{(y+1)}}^{2}{(z+1)}+{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }k$
4. $(2{(x-1)}{{(y+1)}}^{2}{{(z+1)}}^{2}+{(y+1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }i+(2{{(x-1)}}^{2}{(y+1)}{{(z+1)}}^{2}+{(x-1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }j+(2{{(x-1)}}^{2}{{(y+1)}}^{2}{(z+1)}+{(x-1)}{(y+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }k$
5. $(2{(x-1)}{{(y+1)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }i+(2{{(x-1)}}^{2}{(y+1)}{{(z+1)}}^{2}+{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }j+(2{{(x-1)}}^{2}{{(y+1)}}^{2}{(z+1)}+{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({{(x-1)}}^{2}{{(y+1)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-1)}{(y+1)}{(z+1)}}) \\  & =2{(x-1)}{{(y+1)}}^{2}{{(z+1)}}^{2}+{(y+1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({{(x-1)}}^{2}{{(y+1)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-1)}{(y+1)}{(z+1)}}) \\  & =2{{(x-1)}}^{2}{(y+1)}{{(z+1)}}^{2}+{(x-1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({{(x-1)}}^{2}{{(y+1)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-1)}{(y+1)}{(z+1)}}) \\  & =2{{(x-1)}}^{2}{{(y+1)}}^{2}{(z+1)}+{(x-1)}{(y+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =(2{(x-1)}{{(y+1)}}^{2}{{(z+1)}}^{2}+{(y+1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }i+(2{{(x-1)}}^{2}{(y+1)}{{(z+1)}}^{2}+{(x-1)}{(z+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }j+(2{{(x-1)}}^{2}{{(y+1)}}^{2}{(z+1)}+{(x-1)}{(y+1)}{e}^{{(x-1)}{(y+1)}{(z+1)}})\text{ }k\end{aligned}
$$

## Generated moderate: power_exp

Find $∇g(x,y,z)$ given that  $g(x,y,z)={{(x-3)}}^{2}{{(y+3)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-3)}{(y+3)}{(z+1)}}.$

1. $(2{(x-3)}{{(y+3)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }i+(2{{(x-3)}}^{2}{(y+3)}{{(z+1)}}^{2}+{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }j+(2{{(x-3)}}^{2}{{(y+3)}}^{2}{(z+1)}+{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }k$
2. $(2{(x-3)}{{(y+3)}}^{2}{{(z+1)}}^{2}+{(x-3)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }i+(2{{(x-3)}}^{2}{(y+3)}{{(z+1)}}^{2}+{(y+3)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }j+(2{{(x-3)}}^{2}{{(y+3)}}^{2}{(z+1)}+{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }k$
3. $({(x-3)}{{(y+3)}}^{2}{{(z+1)}}^{2}+{(y+3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}-1})\text{ }i+({{(x-3)}}^{2}{(y+3)}{{(z+1)}}^{2}+{(x-3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}-1})\text{ }j+({{(x-3)}}^{2}{{(y+3)}}^{2}{(z+1)}+{(x-3)}{(y+3)}{e}^{{(x-3)}{(y+3)}{(z+1)}-1})\text{ }k$
4. $(2{(x-3)}{{(y+3)}}^{2}{{(z+1)}}^{2}+{(y+3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }i+(2{{(x-3)}}^{2}{(y+3)}{{(z+1)}}^{2}+{(x-3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }j+(2{{(x-3)}}^{2}{{(y+3)}}^{2}{(z+1)}+{(x-3)}{(y+3)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }k$
5. $(2{(x-3)}+{(y+3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }i+(2{(y+3)}+{(x-3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }j+(2{(z+1)}+{(x-3)}{(y+3)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({{(x-3)}}^{2}{{(y+3)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-3)}{(y+3)}{(z+1)}}) \\  & =2{(x-3)}{{(y+3)}}^{2}{{(z+1)}}^{2}+{(y+3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({{(x-3)}}^{2}{{(y+3)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-3)}{(y+3)}{(z+1)}}) \\  & =2{{(x-3)}}^{2}{(y+3)}{{(z+1)}}^{2}+{(x-3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({{(x-3)}}^{2}{{(y+3)}}^{2}{{(z+1)}}^{2}+{e}^{{(x-3)}{(y+3)}{(z+1)}}) \\  & =2{{(x-3)}}^{2}{{(y+3)}}^{2}{(z+1)}+{(x-3)}{(y+3)}{e}^{{(x-3)}{(y+3)}{(z+1)}}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =(2{(x-3)}{{(y+3)}}^{2}{{(z+1)}}^{2}+{(y+3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }i+(2{{(x-3)}}^{2}{(y+3)}{{(z+1)}}^{2}+{(x-3)}{(z+1)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }j+(2{{(x-3)}}^{2}{{(y+3)}}^{2}{(z+1)}+{(x-3)}{(y+3)}{e}^{{(x-3)}{(y+3)}{(z+1)}})\text{ }k\end{aligned}
$$

## Generated historical bank evidence only: power_exp

Find $∇g(x,y,z)$ given that  $g(x,y,z)={{(x+2)}}^{2}{{(y-1)}}^{2}{{(z+3)}}^{2}+{e}^{{(x+2)}{(y-1)}{(z+3)}}.$

1. $(2{(x+2)}{{(y-1)}}^{2}{{(z+3)}}^{2}+{(y-1)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }i+(2{{(x+2)}}^{2}{(y-1)}{{(z+3)}}^{2}+{(x+2)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }j+(2{{(x+2)}}^{2}{{(y-1)}}^{2}{(z+3)}+{(x+2)}{(y-1)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }k$
2. $(2{(x+2)}+{(y-1)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }i+(2{(y-1)}+{(x+2)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }j+(2{(z+3)}+{(x+2)}{(y-1)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }k$
3. $(2{(x+2)}{{(y-1)}}^{2}{{(z+3)}}^{2}+{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }i+(2{{(x+2)}}^{2}{(y-1)}{{(z+3)}}^{2}+{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }j+(2{{(x+2)}}^{2}{{(y-1)}}^{2}{(z+3)}+{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }k$
4. $(2{(x+2)}{{(y-1)}}^{2}{{(z+3)}}^{2}+{(x+2)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }i+(2{{(x+2)}}^{2}{(y-1)}{{(z+3)}}^{2}+{(y-1)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }j+(2{{(x+2)}}^{2}{{(y-1)}}^{2}{(z+3)}+{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }k$
5. $({(x+2)}{{(y-1)}}^{2}{{(z+3)}}^{2}+{(y-1)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}-1})\text{ }i+({{(x+2)}}^{2}{(y-1)}{{(z+3)}}^{2}+{(x+2)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}-1})\text{ }j+({{(x+2)}}^{2}{{(y-1)}}^{2}{(z+3)}+{(x+2)}{(y-1)}{e}^{{(x+2)}{(y-1)}{(z+3)}-1})\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({{(x+2)}}^{2}{{(y-1)}}^{2}{{(z+3)}}^{2}+{e}^{{(x+2)}{(y-1)}{(z+3)}}) \\  & =2{(x+2)}{{(y-1)}}^{2}{{(z+3)}}^{2}+{(y-1)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({{(x+2)}}^{2}{{(y-1)}}^{2}{{(z+3)}}^{2}+{e}^{{(x+2)}{(y-1)}{(z+3)}}) \\  & =2{{(x+2)}}^{2}{(y-1)}{{(z+3)}}^{2}+{(x+2)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({{(x+2)}}^{2}{{(y-1)}}^{2}{{(z+3)}}^{2}+{e}^{{(x+2)}{(y-1)}{(z+3)}}) \\  & =2{{(x+2)}}^{2}{{(y-1)}}^{2}{(z+3)}+{(x+2)}{(y-1)}{e}^{{(x+2)}{(y-1)}{(z+3)}}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =(2{(x+2)}{{(y-1)}}^{2}{{(z+3)}}^{2}+{(y-1)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }i+(2{{(x+2)}}^{2}{(y-1)}{{(z+3)}}^{2}+{(x+2)}{(z+3)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }j+(2{{(x+2)}}^{2}{{(y-1)}}^{2}{(z+3)}+{(x+2)}{(y-1)}{e}^{{(x+2)}{(y-1)}{(z+3)}})\text{ }k\end{aligned}
$$

## Generated moderate: variable_power

If $f(x,y,z)={{(x-1)}}^{{(y+1)}}+{{(y+1)}}^{{(z+1)}},$ find $∇f(x,y,z).$

1. ${(y+1)}{{(x-1)}}^{{(y+1)}-1}\,i+{(z+1)}{{(y+1)}}^{{(z+1)}-1}\,j+{{(y+1)}}^{{(z+1)}}\operatorname{ln}⁡{(y+1)}\,k$
2. $({{(x-1)}}^{{(y+1)}}\operatorname{ln}⁡{(x-1)}+{(z+1)}{{(y+1)}}^{{(z+1)}-1})i+{{(x-1)}}^{{(y+1)}}\operatorname{ln}⁡{(y+1)}\,j+{{(y+1)}}^{{(z+1)}}\operatorname{ln}⁡{(z+1)}\,k$
3. ${(y+1)}{{(x-1)}}^{{(y+1)}-1}\,i+{(z+1)}{{(y+1)}}^{{(z+1)}-1}\,j+{(z+1)}{{(y+1)}}^{{(z+1)}-1}\,k$
4. ${{(x-1)}}^{{(y+1)}}\operatorname{ln}⁡{(y+1)}\,i+{{(x-1)}}^{{(y+1)}}\operatorname{ln}⁡{(x-1)}\,j+({{(x-1)}}^{{(y+1)}}\operatorname{ln}⁡{(x-1)}+{(z+1)}{{(y+1)}}^{{(z+1)}-1})k$
5. ${(y+1)}{{(x-1)}}^{{(y+1)}-1}\,i+({{(x-1)}}^{{(y+1)}}\operatorname{ln}⁡{(x-1)}+{(z+1)}{{(y+1)}}^{{(z+1)}-1})j+{{(y+1)}}^{{(z+1)}}\operatorname{ln}⁡{(y+1)}\,k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}({{(x-1)}}^{{(y+1)}}+{{(y+1)}}^{{(z+1)}}) \\  & ={(y+1)}{{(x-1)}}^{{(y+1)}-1} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}({{(x-1)}}^{{(y+1)}}+{{(y+1)}}^{{(z+1)}}) \\  & ={{(x-1)}}^{{(y+1)}}\operatorname{ln}⁡{(x-1)}+{(z+1)}{{(y+1)}}^{{(z+1)}-1} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}({{(x-1)}}^{{(y+1)}}+{{(y+1)}}^{{(z+1)}}) \\  & ={{(y+1)}}^{{(z+1)}}\operatorname{ln}⁡{(y+1)}\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\,j+{f}_{z}(x,y,z)\,k \\  & ={(y+1)}{{(x-1)}}^{{(y+1)}-1}\,i+({{(x-1)}}^{{(y+1)}}\operatorname{ln}⁡{(x-1)}+{(z+1)}{{(y+1)}}^{{(z+1)}-1})j+{{(y+1)}}^{{(z+1)}}\operatorname{ln}⁡{(y+1)}\,k.\end{aligned}
$$

## Generated moderate: variable_power

If $f(x,y,z)={{(x-3)}}^{{(y+3)}}+{{(y+3)}}^{{(z+1)}},$ find $∇f(x,y,z).$

1. ${(y+3)}{{(x-3)}}^{{(y+3)}-1}\,i+({{(x-3)}}^{{(y+3)}}\operatorname{ln}⁡{(x-3)}+{(z+1)}{{(y+3)}}^{{(z+1)}-1})j+{{(y+3)}}^{{(z+1)}}\operatorname{ln}⁡{(y+3)}\,k$
2. ${(y+3)}{{(x-3)}}^{{(y+3)}-1}\,i+{(z+1)}{{(y+3)}}^{{(z+1)}-1}\,j+{(z+1)}{{(y+3)}}^{{(z+1)}-1}\,k$
3. $({{(x-3)}}^{{(y+3)}}\operatorname{ln}⁡{(x-3)}+{(z+1)}{{(y+3)}}^{{(z+1)}-1})i+{{(x-3)}}^{{(y+3)}}\operatorname{ln}⁡{(y+3)}\,j+{{(y+3)}}^{{(z+1)}}\operatorname{ln}⁡{(z+1)}\,k$
4. ${{(x-3)}}^{{(y+3)}}\operatorname{ln}⁡{(y+3)}\,i+{{(x-3)}}^{{(y+3)}}\operatorname{ln}⁡{(x-3)}\,j+({{(x-3)}}^{{(y+3)}}\operatorname{ln}⁡{(x-3)}+{(z+1)}{{(y+3)}}^{{(z+1)}-1})k$
5. ${(y+3)}{{(x-3)}}^{{(y+3)}-1}\,i+{(z+1)}{{(y+3)}}^{{(z+1)}-1}\,j+{{(y+3)}}^{{(z+1)}}\operatorname{ln}⁡{(y+3)}\,k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}({{(x-3)}}^{{(y+3)}}+{{(y+3)}}^{{(z+1)}}) \\  & ={(y+3)}{{(x-3)}}^{{(y+3)}-1} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}({{(x-3)}}^{{(y+3)}}+{{(y+3)}}^{{(z+1)}}) \\  & ={{(x-3)}}^{{(y+3)}}\operatorname{ln}⁡{(x-3)}+{(z+1)}{{(y+3)}}^{{(z+1)}-1} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}({{(x-3)}}^{{(y+3)}}+{{(y+3)}}^{{(z+1)}}) \\  & ={{(y+3)}}^{{(z+1)}}\operatorname{ln}⁡{(y+3)}\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\,j+{f}_{z}(x,y,z)\,k \\  & ={(y+3)}{{(x-3)}}^{{(y+3)}-1}\,i+({{(x-3)}}^{{(y+3)}}\operatorname{ln}⁡{(x-3)}+{(z+1)}{{(y+3)}}^{{(z+1)}-1})j+{{(y+3)}}^{{(z+1)}}\operatorname{ln}⁡{(y+3)}\,k.\end{aligned}
$$

## Generated historical bank evidence only: variable_power

If $f(x,y,z)={{(x+2)}}^{{(y-1)}}+{{(y-1)}}^{{(z+3)}},$ find $∇f(x,y,z).$

1. ${{(x+2)}}^{{(y-1)}}\operatorname{ln}⁡{(y-1)}\,i+{{(x+2)}}^{{(y-1)}}\operatorname{ln}⁡{(x+2)}\,j+({{(x+2)}}^{{(y-1)}}\operatorname{ln}⁡{(x+2)}+{(z+3)}{{(y-1)}}^{{(z+3)}-1})k$
2. ${(y-1)}{{(x+2)}}^{{(y-1)}-1}\,i+{(z+3)}{{(y-1)}}^{{(z+3)}-1}\,j+{{(y-1)}}^{{(z+3)}}\operatorname{ln}⁡{(y-1)}\,k$
3. ${(y-1)}{{(x+2)}}^{{(y-1)}-1}\,i+({{(x+2)}}^{{(y-1)}}\operatorname{ln}⁡{(x+2)}+{(z+3)}{{(y-1)}}^{{(z+3)}-1})j+{{(y-1)}}^{{(z+3)}}\operatorname{ln}⁡{(y-1)}\,k$
4. ${(y-1)}{{(x+2)}}^{{(y-1)}-1}\,i+{(z+3)}{{(y-1)}}^{{(z+3)}-1}\,j+{(z+3)}{{(y-1)}}^{{(z+3)}-1}\,k$
5. $({{(x+2)}}^{{(y-1)}}\operatorname{ln}⁡{(x+2)}+{(z+3)}{{(y-1)}}^{{(z+3)}-1})i+{{(x+2)}}^{{(y-1)}}\operatorname{ln}⁡{(y-1)}\,j+{{(y-1)}}^{{(z+3)}}\operatorname{ln}⁡{(z+3)}\,k$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}({{(x+2)}}^{{(y-1)}}+{{(y-1)}}^{{(z+3)}}) \\  & ={(y-1)}{{(x+2)}}^{{(y-1)}-1} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}({{(x+2)}}^{{(y-1)}}+{{(y-1)}}^{{(z+3)}}) \\  & ={{(x+2)}}^{{(y-1)}}\operatorname{ln}⁡{(x+2)}+{(z+3)}{{(y-1)}}^{{(z+3)}-1} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}({{(x+2)}}^{{(y-1)}}+{{(y-1)}}^{{(z+3)}}) \\  & ={{(y-1)}}^{{(z+3)}}\operatorname{ln}⁡{(y-1)}\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\,j+{f}_{z}(x,y,z)\,k \\  & ={(y-1)}{{(x+2)}}^{{(y-1)}-1}\,i+({{(x+2)}}^{{(y-1)}}\operatorname{ln}⁡{(x+2)}+{(z+3)}{{(y-1)}}^{{(z+3)}-1})j+{{(y-1)}}^{{(z+3)}}\operatorname{ln}⁡{(y-1)}\,k.\end{aligned}
$$

## Generated moderate: expcos_point

Evaluate $∇h(x,y,z)$ at the point $(1,3,- \frac{2 \pi}{3} )$ if $h(x,y,z)={e}^{xy}\operatorname{cos}⁡(yz).$

1. $(3 e^{3})\,\mathbf i+(3 e^{3})\,\mathbf j+(0)\,\mathbf k$
2. $(- 3 e^{3})\,\mathbf i+(- e^{3})\,\mathbf j+(0)\,\mathbf k$
3. $(3 e^{3})\,\mathbf i+(e^{3})\,\mathbf j+(0)\,\mathbf k$
4. $(3)\,\mathbf i+(1)\,\mathbf j+(0)\,\mathbf k$
5. $(3 e^{6})\,\mathbf i+(e^{6})\,\mathbf j+(0)\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =y{e}^{xy}\operatorname{cos}⁡(yz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =x{e}^{xy}\operatorname{cos}⁡(yz)+{e}^{xy}(-\operatorname{sin}⁡(yz))(z) \\  & ={e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz)) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =-y{e}^{xy}\operatorname{sin}⁡(yz)\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\,i+{h}_{y}(x,y,z)\,j+{h}_{z}(x,y,z)\,k \\  & =y{e}^{xy}\operatorname{cos}⁡(yz)\,i+{e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y{e}^{xy}\operatorname{sin}⁡(yz)\,k \\  & ={e}^{xy}(y\operatorname{cos}⁡(yz)\,i+(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y\operatorname{sin}⁡(yz)\,k) \\ ∇h(1,3,- \frac{2 \pi}{3} ) & ={e}^{(1)(3)}(3\operatorname{cos}⁡((3)(-\frac{2 \pi}{3}))\,i+(1\operatorname{cos}⁡((3)(-\frac{2 \pi}{3}))-(-\frac{2 \pi}{3})\operatorname{sin}⁡((3)(-\frac{2 \pi}{3})))\,j-3\operatorname{sin}⁡((3)(-\frac{2 \pi}{3}))\,k) \\  & =e^{3}(3i+\,j-0\,k) \\  & =e^{3}(3i+1\,j).\end{aligned}
$$

## Generated moderate: expcos_point

Evaluate $∇h(x,y,z)$ at the point $(\frac{1}{2},3,- \frac{\pi}{3} )$ if $h(x,y,z)={e}^{xy}\operatorname{cos}⁡(yz).$

1. $(3 e^{\frac{3}{2}})\,\mathbf i+(\frac{e^{\frac{3}{2}}}{2})\,\mathbf j+(0)\,\mathbf k$
2. $(- 3 e^{\frac{3}{2}})\,\mathbf i+(- \frac{e^{\frac{3}{2}}}{2})\,\mathbf j+(0)\,\mathbf k$
3. $(-3)\,\mathbf i+(- \frac{1}{2})\,\mathbf j+(0)\,\mathbf k$
4. $(- 3 e^{\frac{3}{2}})\,\mathbf i+(- 3 e^{\frac{3}{2}})\,\mathbf j+(0)\,\mathbf k$
5. $(- 3 e^{3})\,\mathbf i+(- \frac{e^{3}}{2})\,\mathbf j+(0)\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =y{e}^{xy}\operatorname{cos}⁡(yz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =x{e}^{xy}\operatorname{cos}⁡(yz)+{e}^{xy}(-\operatorname{sin}⁡(yz))(z) \\  & ={e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz)) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =-y{e}^{xy}\operatorname{sin}⁡(yz)\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\,i+{h}_{y}(x,y,z)\,j+{h}_{z}(x,y,z)\,k \\  & =y{e}^{xy}\operatorname{cos}⁡(yz)\,i+{e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y{e}^{xy}\operatorname{sin}⁡(yz)\,k \\  & ={e}^{xy}(y\operatorname{cos}⁡(yz)\,i+(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y\operatorname{sin}⁡(yz)\,k) \\ ∇h(\frac{1}{2},3,- \frac{\pi}{3} ) & ={e}^{(1/2)(3)}(3\operatorname{cos}⁡((3)(-\frac{\pi}{3}))\,i+(\frac{1}{2}\operatorname{cos}⁡((3)(-\frac{\pi}{3}))-(-\frac{\pi}{3})\operatorname{sin}⁡((3)(-\frac{\pi}{3})))\,j-3\operatorname{sin}⁡((3)(-\frac{\pi}{3}))\,k) \\  & =e^{\frac{3}{2}}(-3i-\frac{1}{2}\,j-0\,k) \\  & =-e^{\frac{3}{2}}(3i+\frac{1}{2}\,j).\end{aligned}
$$

## Generated historical bank evidence only: expcos_point

Evaluate $∇h(x,y,z)$ at the point $(\frac{1}{3},2,\frac{\pi}{2} )$ if $h(x,y,z)={e}^{xy}\operatorname{cos}⁡(yz).$

1. $e^{\frac{2}{3}}(-2i+\frac{\pi}{2} \,j-k)$
2. $e^{\frac{4}{3}}(2i-\frac{1}{3}\,j+k)$
3. $e^{\frac{4}{3}}(2i-\frac{1}{3}\,j)$
4. $-e^{\frac{2}{3}}(2i+\frac{1}{3}\,j)$
5. $-e^{\frac{2}{3}}(2i+\frac{\pi}{2} \,j-k)$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =y{e}^{xy}\operatorname{cos}⁡(yz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =x{e}^{xy}\operatorname{cos}⁡(yz)+{e}^{xy}(-\operatorname{sin}⁡(yz))(z) \\  & ={e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz)) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =-y{e}^{xy}\operatorname{sin}⁡(yz)\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\,i+{h}_{x}(x,y,z)\,j+{h}_{x}(x,y,z)\,k \\  & =y{e}^{xy}\operatorname{cos}⁡(yz)\,i+{e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y{e}^{xy}\operatorname{sin}⁡(yz)\,k \\  & ={e}^{xy}(y\operatorname{cos}⁡(yz)\,i+(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y\operatorname{sin}⁡(yz)\,k) \\ ∇h(\frac{1}{3},2,\frac{\pi}{2} ) & ={e}^{(1/3)(2)}(2\operatorname{cos}⁡((2)(\frac{\pi}{2}))\,i+(\frac{1}{3}\operatorname{cos}⁡((2)(\frac{\pi}{2}))-\frac{\pi}{2}\operatorname{sin}⁡((2)(\frac{\pi}{2})))\,j-2\operatorname{sin}⁡((2)(\frac{\pi}{2}))\,k) \\  & =e^{\frac{2}{3}}(-2i-\frac{1}{3}\,j-0\,k) \\  & =-e^{\frac{2}{3}}(2i+\frac{1}{3}\,j).\end{aligned}
$$

## Generated moderate: exp_sin

Given  $g(x,y,z)={e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1)$, find $∇g(x,y,z).$

1. $2{e}^{2{(x-1)}{(z+1)}}\text{ }({(z+1)}i+{(y+1)}\operatorname{cos}⁡({{(y+1)}}^{2}-1)\text{ }j+{(x-1)}\text{ }k)$
2. $2{e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1)\text{ }({(z+1)}i+{(y+1)}\text{ }j+{(x-1)}\text{ }k)$
3. $2{e}^{2{(x-1)}{(z+1)}}\text{ }({(z+1)}i+{(y+1)}\text{ }j+{(x-1)}\text{ }k)$
4. ${(z+1)}\operatorname{sin}⁡({{(y+1)}}^{2}-1)i+{(y+1)}\operatorname{cos}⁡({{(y+1)}}^{2}-1)\text{ }j+{(x-1)}\operatorname{sin}⁡({{(y+1)}}^{2}-1)\text{ }k$
5. $2{e}^{2{(x-1)}{(z+1)}}\text{ }({(z+1)}\operatorname{sin}⁡({{(y+1)}}^{2}-1)i+{(y+1)}\operatorname{cos}⁡({{(y+1)}}^{2}-1)\text{ }j+{(x-1)}\operatorname{sin}⁡({{(y+1)}}^{2}-1)\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1)) \\  & =2{(z+1)}{e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1) \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1)) \\  & =2{(y+1)}{e}^{2{(x-1)}{(z+1)}}\operatorname{cos}⁡({{(y+1)}}^{2}-1) \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1)) \\  & =2{(x-1)}{e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1).\end{aligned}
$$

Hence, the gradient is: 

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =2{(z+1)}{e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1)\text{ }i+2{(y+1)}{e}^{2{(x-1)}{(z+1)}}\operatorname{cos}⁡({{(y+1)}}^{2}-1)\text{ }j+2{(x-1)}{e}^{2{(x-1)}{(z+1)}}\operatorname{sin}⁡({{(y+1)}}^{2}-1)\text{ }k \\  & =2{e}^{2{(x-1)}{(z+1)}}\text{ }({(z+1)}\operatorname{sin}⁡({{(y+1)}}^{2}-1)i+{(y+1)}\operatorname{cos}⁡({{(y+1)}}^{2}-1)\text{ }j+{(x-1)}\operatorname{sin}⁡({{(y+1)}}^{2}-1)\text{ }k)\end{aligned}
$$

## Generated moderate: exp_sin

Given  $g(x,y,z)={e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1)$, find $∇g(x,y,z).$

1. $2{e}^{2{(x-3)}{(z+1)}}\text{ }({(z+1)}\operatorname{sin}⁡({{(y+3)}}^{2}-1)i+{(y+3)}\operatorname{cos}⁡({{(y+3)}}^{2}-1)\text{ }j+{(x-3)}\operatorname{sin}⁡({{(y+3)}}^{2}-1)\text{ }k)$
2. $2{e}^{2{(x-3)}{(z+1)}}\text{ }({(z+1)}i+{(y+3)}\text{ }j+{(x-3)}\text{ }k)$
3. $2{e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1)\text{ }({(z+1)}i+{(y+3)}\text{ }j+{(x-3)}\text{ }k)$
4. ${(z+1)}\operatorname{sin}⁡({{(y+3)}}^{2}-1)i+{(y+3)}\operatorname{cos}⁡({{(y+3)}}^{2}-1)\text{ }j+{(x-3)}\operatorname{sin}⁡({{(y+3)}}^{2}-1)\text{ }k$
5. $2{e}^{2{(x-3)}{(z+1)}}\text{ }({(z+1)}i+{(y+3)}\operatorname{cos}⁡({{(y+3)}}^{2}-1)\text{ }j+{(x-3)}\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1)) \\  & =2{(z+1)}{e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1) \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1)) \\  & =2{(y+3)}{e}^{2{(x-3)}{(z+1)}}\operatorname{cos}⁡({{(y+3)}}^{2}-1) \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1)) \\  & =2{(x-3)}{e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1).\end{aligned}
$$

Hence, the gradient is: 

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =2{(z+1)}{e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1)\text{ }i+2{(y+3)}{e}^{2{(x-3)}{(z+1)}}\operatorname{cos}⁡({{(y+3)}}^{2}-1)\text{ }j+2{(x-3)}{e}^{2{(x-3)}{(z+1)}}\operatorname{sin}⁡({{(y+3)}}^{2}-1)\text{ }k \\  & =2{e}^{2{(x-3)}{(z+1)}}\text{ }({(z+1)}\operatorname{sin}⁡({{(y+3)}}^{2}-1)i+{(y+3)}\operatorname{cos}⁡({{(y+3)}}^{2}-1)\text{ }j+{(x-3)}\operatorname{sin}⁡({{(y+3)}}^{2}-1)\text{ }k)\end{aligned}
$$

## Generated historical bank evidence only: exp_sin

Given  $g(x,y,z)={e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1)$, find $∇g(x,y,z).$

1. ${(z+3)}\operatorname{sin}⁡({{(y-1)}}^{2}-1)i+{(y-1)}\operatorname{cos}⁡({{(y-1)}}^{2}-1)\text{ }j+{(x+2)}\operatorname{sin}⁡({{(y-1)}}^{2}-1)\text{ }k$
2. $2{e}^{2{(x+2)}{(z+3)}}\text{ }({(z+3)}i+{(y-1)}\operatorname{cos}⁡({{(y-1)}}^{2}-1)\text{ }j+{(x+2)}\text{ }k)$
3. $2{e}^{2{(x+2)}{(z+3)}}\text{ }({(z+3)}\operatorname{sin}⁡({{(y-1)}}^{2}-1)i+{(y-1)}\operatorname{cos}⁡({{(y-1)}}^{2}-1)\text{ }j+{(x+2)}\operatorname{sin}⁡({{(y-1)}}^{2}-1)\text{ }k)$
4. $2{e}^{2{(x+2)}{(z+3)}}\text{ }({(z+3)}i+{(y-1)}\text{ }j+{(x+2)}\text{ }k)$
5. $2{e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1)\text{ }({(z+3)}i+{(y-1)}\text{ }j+{(x+2)}\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1)) \\  & =2{(z+3)}{e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1) \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1)) \\  & =2{(y-1)}{e}^{2{(x+2)}{(z+3)}}\operatorname{cos}⁡({{(y-1)}}^{2}-1) \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1)) \\  & =2{(x+2)}{e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1).\end{aligned}
$$

Hence, the gradient is: 

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =2{(z+3)}{e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1)\text{ }i+2{(y-1)}{e}^{2{(x+2)}{(z+3)}}\operatorname{cos}⁡({{(y-1)}}^{2}-1)\text{ }j+2{(x+2)}{e}^{2{(x+2)}{(z+3)}}\operatorname{sin}⁡({{(y-1)}}^{2}-1)\text{ }k \\  & =2{e}^{2{(x+2)}{(z+3)}}\text{ }({(z+3)}\operatorname{sin}⁡({{(y-1)}}^{2}-1)i+{(y-1)}\operatorname{cos}⁡({{(y-1)}}^{2}-1)\text{ }j+{(x+2)}\operatorname{sin}⁡({{(y-1)}}^{2}-1)\text{ }k)\end{aligned}
$$

## Generated moderate: composite_log

Given $h(x,y,z)={(x-1)}{(y+1)}{(z+1)}\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})$, find  $∇h(x,y,z).$

1. $(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1)({(y+1)}{(z+1)}\text{ }i+{(x-1)}{(z+1)}\text{ }j+{(x-1)}{(y+1)}\text{ }k)$
2. $\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})({(y+1)}{(z+1)}\text{ }i+{(x-1)}{(z+1)}\text{ }j+{(x-1)}{(y+1)}\text{ }k)$
3. $(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1)(\text{ }i+\text{ }j+\text{ }k)$
4. $(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1)({(x-1)}\text{ }i+{(y+1)}\text{ }j+{(z+1)}\text{ }k)$
5. ${(y+1)}{(z+1)}\text{ }i+{(x-1)}{(z+1)}\text{ }j+{(x-1)}{(y+1)}\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({(x-1)}{(y+1)}{(z+1)}\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})) \\  & ={(y+1)}{(z+1)}\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+{(x-1)}{(y+1)}{(z+1)}\frac{{(y+1)}{(z+1)}}{{(x-1)}{(y+1)}{(z+1)}} \\  & ={(y+1)}{(z+1)}(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({(x-1)}{(y+1)}{(z+1)}\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})) \\  & ={(x-1)}{(z+1)}\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+{(x-1)}{(y+1)}{(z+1)}\frac{{(x-1)}{(z+1)}}{{(x-1)}{(y+1)}{(z+1)}} \\  & ={(x-1)}{(z+1)}(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({(x-1)}{(y+1)}{(z+1)}\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})) \\  & ={(x-1)}{(y+1)}\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+{(x-1)}{(y+1)}{(z+1)}\frac{{(x-1)}{(y+1)}}{{(x-1)}{(y+1)}{(z+1)}} \\  & ={(x-1)}{(y+1)}(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1)\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & ={(y+1)}{(z+1)}(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1)\text{ }i+{(x-1)}{(z+1)}(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1)\text{ }j+{(x-1)}{(y+1)}(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1)\text{ }k \\  & =(\operatorname{ln}⁡({(x-1)}{(y+1)}{(z+1)})+1)({(y+1)}{(z+1)}\text{ }i+{(x-1)}{(z+1)}\text{ }j+{(x-1)}{(y+1)}\text{ }k).\end{aligned}
$$

## Generated moderate: composite_log

Given $h(x,y,z)={(x-3)}{(y+3)}{(z+1)}\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})$, find  $∇h(x,y,z).$

1. ${(y+3)}{(z+1)}\text{ }i+{(x-3)}{(z+1)}\text{ }j+{(x-3)}{(y+3)}\text{ }k$
2. $(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1)(\text{ }i+\text{ }j+\text{ }k)$
3. $\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})({(y+3)}{(z+1)}\text{ }i+{(x-3)}{(z+1)}\text{ }j+{(x-3)}{(y+3)}\text{ }k)$
4. $(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1)({(x-3)}\text{ }i+{(y+3)}\text{ }j+{(z+1)}\text{ }k)$
5. $(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1)({(y+3)}{(z+1)}\text{ }i+{(x-3)}{(z+1)}\text{ }j+{(x-3)}{(y+3)}\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({(x-3)}{(y+3)}{(z+1)}\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})) \\  & ={(y+3)}{(z+1)}\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+{(x-3)}{(y+3)}{(z+1)}\frac{{(y+3)}{(z+1)}}{{(x-3)}{(y+3)}{(z+1)}} \\  & ={(y+3)}{(z+1)}(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({(x-3)}{(y+3)}{(z+1)}\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})) \\  & ={(x-3)}{(z+1)}\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+{(x-3)}{(y+3)}{(z+1)}\frac{{(x-3)}{(z+1)}}{{(x-3)}{(y+3)}{(z+1)}} \\  & ={(x-3)}{(z+1)}(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({(x-3)}{(y+3)}{(z+1)}\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})) \\  & ={(x-3)}{(y+3)}\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+{(x-3)}{(y+3)}{(z+1)}\frac{{(x-3)}{(y+3)}}{{(x-3)}{(y+3)}{(z+1)}} \\  & ={(x-3)}{(y+3)}(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1)\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & ={(y+3)}{(z+1)}(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1)\text{ }i+{(x-3)}{(z+1)}(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1)\text{ }j+{(x-3)}{(y+3)}(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1)\text{ }k \\  & =(\operatorname{ln}⁡({(x-3)}{(y+3)}{(z+1)})+1)({(y+3)}{(z+1)}\text{ }i+{(x-3)}{(z+1)}\text{ }j+{(x-3)}{(y+3)}\text{ }k).\end{aligned}
$$

## Generated historical bank evidence only: composite_log

Given $h(x,y,z)={(x+2)}{(y-1)}{(z+3)}\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})$, find  $∇h(x,y,z).$

1. $(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1)({(x+2)}\text{ }i+{(y-1)}\text{ }j+{(z+3)}\text{ }k)$
2. $(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1)({(y-1)}{(z+3)}\text{ }i+{(x+2)}{(z+3)}\text{ }j+{(x+2)}{(y-1)}\text{ }k)$
3. ${(y-1)}{(z+3)}\text{ }i+{(x+2)}{(z+3)}\text{ }j+{(x+2)}{(y-1)}\text{ }k$
4. $(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1)(\text{ }i+\text{ }j+\text{ }k)$
5. $\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})({(y-1)}{(z+3)}\text{ }i+{(x+2)}{(z+3)}\text{ }j+{(x+2)}{(y-1)}\text{ }k)$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({(x+2)}{(y-1)}{(z+3)}\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})) \\  & ={(y-1)}{(z+3)}\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+{(x+2)}{(y-1)}{(z+3)}\frac{{(y-1)}{(z+3)}}{{(x+2)}{(y-1)}{(z+3)}} \\  & ={(y-1)}{(z+3)}(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({(x+2)}{(y-1)}{(z+3)}\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})) \\  & ={(x+2)}{(z+3)}\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+{(x+2)}{(y-1)}{(z+3)}\frac{{(x+2)}{(z+3)}}{{(x+2)}{(y-1)}{(z+3)}} \\  & ={(x+2)}{(z+3)}(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({(x+2)}{(y-1)}{(z+3)}\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})) \\  & ={(x+2)}{(y-1)}\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+{(x+2)}{(y-1)}{(z+3)}\frac{{(x+2)}{(y-1)}}{{(x+2)}{(y-1)}{(z+3)}} \\  & ={(x+2)}{(y-1)}(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1)\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & ={(y-1)}{(z+3)}(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1)\text{ }i+{(x+2)}{(z+3)}(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1)\text{ }j+{(x+2)}{(y-1)}(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1)\text{ }k \\  & =(\operatorname{ln}⁡({(x+2)}{(y-1)}{(z+3)})+1)({(y-1)}{(z+3)}\text{ }i+{(x+2)}{(z+3)}\text{ }j+{(x+2)}{(y-1)}\text{ }k).\end{aligned}
$$

## Generated moderate: sine_point

Evaluate $∇h(x,y,z)$ at the point $(1,-2,- \frac{\pi}{2} )$ if $h(x,y,z)=\operatorname{sin}⁡(xyz).$

1. $(- \pi)\,\mathbf i+(- \frac{\pi}{2})\,\mathbf j+(2)\,\mathbf k$
2. $(- \pi)\,\mathbf i+(\frac{\pi}{2})\,\mathbf j+(2)\,\mathbf k$
3. $(- \pi)\,\mathbf i+(\frac{\pi}{2})\,\mathbf j+(-2)\,\mathbf k$
4. $(\pi)\,\mathbf i+(- \frac{\pi}{2})\,\mathbf j+(-2)\,\mathbf k$
5. $(\pi)\,\mathbf i+(\frac{\pi}{2})\,\mathbf j+(2)\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{sin}⁡(xyz)) \\  & =yz\operatorname{cos}⁡(xyz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{sin}⁡(xyz)) \\  & =xz\operatorname{cos}⁡(xyz) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{sin}⁡(xyz)) \\  & =xy\operatorname{cos}⁡(xyz)\end{aligned}
$$

 
Hence, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & =yz\operatorname{cos}⁡(xyz)\text{ }i+xz\operatorname{cos}⁡(xyz)\text{ }j+xy\operatorname{cos}⁡(xyz)\text{ }k \\ ∇h(1,-2,- \frac{\pi}{2} ) & =(-2)(-\frac{\pi}{2})\operatorname{cos}⁡(\pi )\text{ }i+(1)(-\frac{\pi}{2})\operatorname{cos}⁡(\pi )\text{ }j+(1)(-2)\operatorname{cos}⁡(\pi )\text{ }k \\  & =\pi (-1)\text{ }i+(-\frac{\pi}{2})(-1)\text{ }j+(-2)(-1)\text{ }k \\  & =-\pi \text{ }i+\frac{\pi}{2}\text{ }j+2\text{ }k\end{aligned}
$$

## Generated moderate: sine_point

Evaluate $∇h(x,y,z)$ at the point $(-2,-1,\frac{\pi}{2} )$ if $h(x,y,z)=\operatorname{sin}⁡(xyz).$

1. $(\frac{\pi}{2})\,\mathbf i+(\pi)\,\mathbf j+(2)\,\mathbf k$
2. $(\frac{\pi}{2})\,\mathbf i+(\pi)\,\mathbf j+(-2)\,\mathbf k$
3. $(- \frac{\pi}{2})\,\mathbf i+(\pi)\,\mathbf j+(-2)\,\mathbf k$
4. $(\frac{\pi}{2})\,\mathbf i+(- \pi)\,\mathbf j+(-2)\,\mathbf k$
5. $(- \frac{\pi}{2})\,\mathbf i+(- \pi)\,\mathbf j+(2)\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{sin}⁡(xyz)) \\  & =yz\operatorname{cos}⁡(xyz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{sin}⁡(xyz)) \\  & =xz\operatorname{cos}⁡(xyz) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{sin}⁡(xyz)) \\  & =xy\operatorname{cos}⁡(xyz)\end{aligned}
$$

 
Hence, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & =yz\operatorname{cos}⁡(xyz)\text{ }i+xz\operatorname{cos}⁡(xyz)\text{ }j+xy\operatorname{cos}⁡(xyz)\text{ }k \\ ∇h(-2,-1,\frac{\pi}{2} ) & =(-1)(\frac{\pi}{2})\operatorname{cos}⁡(\pi )\text{ }i+(-2)(\frac{\pi}{2})\operatorname{cos}⁡(\pi )\text{ }j+(-2)(-1)\operatorname{cos}⁡(\pi )\text{ }k \\  & =(-\frac{\pi}{2})(-1)\text{ }i+(-\pi )(-1)\text{ }j+2(-1)\text{ }k \\  & =\frac{\pi}{2}\text{ }i+\pi \text{ }j-2\text{ }k\end{aligned}
$$

## Generated historical bank evidence only: sine_point

Evaluate $∇h(x,y,z)$ at the point $(2,-1,\frac{\pi}{2} )$ if $h(x,y,z)=\operatorname{sin}⁡(xyz).$

1. $\frac{\pi}{2}\text{ }i+\frac{\pi}{2}\text{ }j+\text{ }k$
2. $\frac{\pi}{2}\text{ }i+\frac{\pi}{2}\text{ }j+\frac{\pi}{2}\text{ }k$
3. $\frac{\pi}{2}\text{ }i-\pi \text{ }j+2\text{ }k$
4. $-\frac{\pi}{2}\text{ }i+\frac{\pi}{2}\text{ }j+\text{ }k$
5. $\text{ }i-\frac{\pi}{2}\text{ }j+\text{ }k$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{sin}⁡(xyz)) \\  & =yz\operatorname{cos}⁡(xyz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{sin}⁡(xyz)) \\  & =xz\operatorname{cos}⁡(xyz) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{sin}⁡(xyz)) \\  & =xy\operatorname{cos}⁡(xyz)\end{aligned}
$$

 
Hence, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{x}(x,y,z)\text{ }j+{h}_{x}(x,y,z)\text{ }k \\  & =yz\operatorname{cos}⁡(xyz)\text{ }i+xz\operatorname{cos}⁡(xyz)\text{ }j+xy\operatorname{cos}⁡(xyz)\text{ }k \\ ∇h(2,-1,\frac{\pi}{2} ) & =(-1)(\frac{\pi}{2})\operatorname{cos}⁡(-\pi )\text{ }i+(2)(\frac{\pi}{2})\operatorname{cos}⁡(-\pi )\text{ }j+(2)(-1)\operatorname{cos}⁡(-\pi )\text{ }k \\  & =(-\frac{\pi}{2})(-1)\text{ }i+\pi (-1)\text{ }j+(-2)(-1)\text{ }k \\  & =\frac{\pi}{2}\text{ }i-\pi \text{ }j+2\text{ }k\end{aligned}
$$

## Generated hard: quotient

Evaluate $∇g(x,y,z)$ at the point $(-3,-1,-2)$ if $g(x,y,z)=- \frac{x y z}{2 x + 2 y + z}.$

1. $(\frac{1}{5})\,\mathbf i+(\frac{3}{5})\,\mathbf j+(\frac{3}{10})\,\mathbf k$
2. $(- \frac{3}{25})\,\mathbf i+(- \frac{3}{25})\,\mathbf j+(- \frac{3}{50})\,\mathbf k$
3. $(\frac{2}{25})\,\mathbf i+(\frac{12}{25})\,\mathbf j+(\frac{6}{25})\,\mathbf k$
4. $(8)\,\mathbf i+(48)\,\mathbf j+(24)\,\mathbf k$
5. $(\frac{8}{25})\,\mathbf i+(\frac{18}{25})\,\mathbf j+(\frac{9}{25})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(- \frac{x y z}{2 x + 2 y + z}) \\  & =\frac{(2 x + 2 y + z)(- y z)-(- x y z)(2)}{(2 x + 2 y + z)^2} \\  & =- \frac{y z \left(2 y + z\right)}{\left(2 x + 2 y + z\right)^{2}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(- \frac{x y z}{2 x + 2 y + z}) \\  & =\frac{(2 x + 2 y + z)(- x z)-(- x y z)(2)}{(2 x + 2 y + z)^2} \\  & =- \frac{x z \left(2 x + z\right)}{\left(2 x + 2 y + z\right)^{2}} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(- \frac{x y z}{2 x + 2 y + z}) \\  & =\frac{(2 x + 2 y + z)(- x y)-(- x y z)(1)}{(2 x + 2 y + z)^2} \\  & =- \frac{2 x y \left(x + y\right)}{\left(2 x + 2 y + z\right)^{2}}\end{aligned}
$$

Therefore, the gradient is

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\,\mathbf i+{g}_{y}(x,y,z)\,\mathbf j+{g}_{z}(x,y,z)\,\mathbf k \\  & =(\frac{2 x y z}{\left(2 x + 2 y + z\right)^{2}} - \frac{y z}{2 x + 2 y + z})\,\mathbf i+(\frac{2 x y z}{\left(2 x + 2 y + z\right)^{2}} - \frac{x z}{2 x + 2 y + z})\,\mathbf j+(\frac{x y z}{\left(2 x + 2 y + z\right)^{2}} - \frac{x y}{2 x + 2 y + z})\,\mathbf k \\ ∇g(-3,-1,-2) & =(\frac{(-10)(-2)-(6)(2)}{(-10)^2})\,\mathbf i+(\frac{(-10)(-6)-(6)(2)}{(-10)^2})\,\mathbf j+(\frac{(-10)(-3)-(6)(1)}{(-10)^2})\,\mathbf k \\  & =(\frac{2}{25})\,\mathbf i+(\frac{12}{25})\,\mathbf j+(\frac{6}{25})\,\mathbf k \\  & =(\frac{2}{25})\,\mathbf i+(\frac{12}{25})\,\mathbf j+(\frac{6}{25})\,\mathbf k\end{aligned}
$$

## Generated hard: quotient

Evaluate $∇g(x,y,z)$ at the point $(3,-3,3)$ if $g(x,y,z)=- \frac{2 x y z}{x - 2 y + z}.$

1. $(162)\,\mathbf i+(-108)\,\mathbf j+(162)\,\mathbf k$
2. $(\frac{3}{2})\,\mathbf i+(- \frac{3}{2})\,\mathbf j+(\frac{3}{2})\,\mathbf k$
3. $(\frac{9}{8})\,\mathbf i+(- \frac{3}{4})\,\mathbf j+(\frac{9}{8})\,\mathbf k$
4. $(- \frac{3}{8})\,\mathbf i+(\frac{3}{4})\,\mathbf j+(- \frac{3}{8})\,\mathbf k$
5. $(\frac{15}{8})\,\mathbf i+(- \frac{9}{4})\,\mathbf j+(\frac{15}{8})\,\mathbf k$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(- \frac{2 x y z}{x - 2 y + z}) \\  & =\frac{(x - 2 y + z)(- 2 y z)-(- 2 x y z)(1)}{(x - 2 y + z)^2} \\  & =\frac{2 y z \left(2 y - z\right)}{\left(x - 2 y + z\right)^{2}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(- \frac{2 x y z}{x - 2 y + z}) \\  & =\frac{(x - 2 y + z)(- 2 x z)-(- 2 x y z)(-2)}{(x - 2 y + z)^2} \\  & =- \frac{2 x z \left(x + z\right)}{\left(x - 2 y + z\right)^{2}} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(- \frac{2 x y z}{x - 2 y + z}) \\  & =\frac{(x - 2 y + z)(- 2 x y)-(- 2 x y z)(1)}{(x - 2 y + z)^2} \\  & =- \frac{2 x y \left(x - 2 y\right)}{\left(x - 2 y + z\right)^{2}}\end{aligned}
$$

Therefore, the gradient is

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\,\mathbf i+{g}_{y}(x,y,z)\,\mathbf j+{g}_{z}(x,y,z)\,\mathbf k \\  & =(\frac{2 x y z}{\left(x - 2 y + z\right)^{2}} - \frac{2 y z}{x - 2 y + z})\,\mathbf i+(- \frac{4 x y z}{\left(x - 2 y + z\right)^{2}} - \frac{2 x z}{x - 2 y + z})\,\mathbf j+(\frac{2 x y z}{\left(x - 2 y + z\right)^{2}} - \frac{2 x y}{x - 2 y + z})\,\mathbf k \\ ∇g(3,-3,3) & =(\frac{(12)(18)-(54)(1)}{(12)^2})\,\mathbf i+(\frac{(12)(-18)-(54)(-2)}{(12)^2})\,\mathbf j+(\frac{(12)(18)-(54)(1)}{(12)^2})\,\mathbf k \\  & =(\frac{9}{8})\,\mathbf i+(- \frac{3}{4})\,\mathbf j+(\frac{9}{8})\,\mathbf k \\  & =(\frac{9}{8})\,\mathbf i+(- \frac{3}{4})\,\mathbf j+(\frac{9}{8})\,\mathbf k\end{aligned}
$$
