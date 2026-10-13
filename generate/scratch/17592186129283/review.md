# Original source and generated review

Sources: math basis 1356. Source profiles are observed; default variants are authored operation banks. Easy/hard labels are authored scope claims.

## Original q-160341

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}-2{v}^{2} \\ u-v\end{aligned}],
$$

is (locally) orientation-reversing?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/09/09f7f36ecc2197cc95e1878fa22ac22367978809a5241f09886a7eb2fab071f3.png)

![](/media/jake/SSD/EDB/math/images/15/154f70201a5a00737d8df61952f5600ff91a2373df07b0b54680fe84e048402c.png)

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

![](/media/jake/SSD/EDB/math/images/30/3033f0ae73e3f484fc5d3d65e388062feba1824fb3da9971d560cf2f518f49bb.png)

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-2{(v + 1)}^{2} \\ (u - 1)-(v + 1)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d19bc87bd47faf335f6b.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7da76c461943cd65bb14.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a368c5ffeacd23bcd509.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-2{(v + 1)}^{2} \\ (u - 1)-(v + 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & -4(v + 1) \\ 1 & -1\end{aligned}| \\  & =2(u - 1)\cdot (-1)-(-4(v + 1))\cdot 1 \\  & =-2(u - 1)+4(v + 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-2(u - 1)+4(v + 1) & <0 \\ 4(v + 1) & <2(u - 1) \\ (v + 1) & <\frac{1}{2}(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)=\frac{1}{2}(u - 1)
$$

defines a straight line, and the coordinates of, say, $(2,-2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a368c5ffeacd23bcd509.png)

Original worked solution

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}-2{v}^{2} \\ u-v\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2u & -4v \\ 1 & -1\end{aligned}| \\  & =2u\cdot (-1)-(-4v)\cdot 1 \\  & =-2u+4v.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-2u+4v & <0 \\ 4v & <2u \\ v & <\frac{1}{2}u\end{aligned}
$$

 

Notice that the equation 

$$
v=\frac{1}{2}u
$$

defines a straight line, and the coordinates of, say, $(1,-1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/media/jake/SSD/EDB/math/images/09/09f7f36ecc2197cc95e1878fa22ac22367978809a5241f09886a7eb2fab071f3.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}-2{(v - 2)}^{2} \\ (u + 1)-(v - 2)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d0306dd5b56ab990c5cf.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-511287c72fe6f589bf3f.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f5cc28213f4ae50bbef6.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-76d8eddaa23fca03849f.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-580f687d068f4a7cee0b.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}-2{(v - 2)}^{2} \\ (u + 1)-(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u + 1) & -4(v - 2) \\ 1 & -1\end{aligned}| \\  & =2(u + 1)\cdot (-1)-(-4(v - 2))\cdot 1 \\  & =-2(u + 1)+4(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-2(u + 1)+4(v - 2) & <0 \\ 4(v - 2) & <2(u + 1) \\ (v - 2) & <\frac{1}{2}(u + 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=\frac{1}{2}(u + 1)
$$

defines a straight line, and the coordinates of, say, $(0,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-580f687d068f4a7cee0b.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-2{(v - 2)}^{2} \\ (u - 1)-(v - 2)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8bf4a535626be22eba26.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e349d2ae5485468806b3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c2489f7565526e2a3874.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-141276b1a8f26e66b8d2.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-b911e93c591f646d064a.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-2{(v - 2)}^{2} \\ (u - 1)-(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & -4(v - 2) \\ 1 & -1\end{aligned}| \\  & =2(u - 1)\cdot (-1)-(-4(v - 2))\cdot 1 \\  & =-2(u - 1)+4(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-2(u - 1)+4(v - 2) & <0 \\ 4(v - 2) & <2(u - 1) \\ (v - 2) & <\frac{1}{2}(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=\frac{1}{2}(u - 1)
$$

defines a straight line, and the coordinates of, say, $(2,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c2489f7565526e2a3874.png)

## Original q-160601

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}-v \\ 4u-{v}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/13/1368ee41963c1abcc320d2cd35449c08599582f37c7d68f750e137fcdcd2e57b.png)

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

![](/media/jake/SSD/EDB/math/images/09/090bab0ac1c6356010d83a6ad54c59b53b7dd12062fb5e331a936ce3f3a1b411.png)

![](/media/jake/SSD/EDB/math/images/15/154f70201a5a00737d8df61952f5600ff91a2373df07b0b54680fe84e048402c.png)

Original raw bank 1

![](/media/jake/SSD/EDB/math/images/13/1368ee41963c1abcc320d2cd35449c08599582f37c7d68f750e137fcdcd2e57b.png)

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/15/154f70201a5a00737d8df61952f5600ff91a2373df07b0b54680fe84e048402c.png)

![](/media/jake/SSD/EDB/math/images/09/090bab0ac1c6356010d83a6ad54c59b53b7dd12062fb5e331a936ce3f3a1b411.png)

### Generated explicit observed bank variant: observed_legacy

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v + 1) \\ 4(u - 1)-{(v + 1)}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8f4100dc9b543c613f18.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3979213a5676761da39d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d19bc87bd47faf335f6b.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v + 1) \\ 4(u - 1)-{(v + 1)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & -1 \\ 4 & -2(v + 1)\end{aligned}| \\  & =2(u - 1)\cdot (-2(v + 1))-4\cdot (-1) \\  & =-4(u - 1)(v + 1)+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4(u - 1)(v + 1)+4 & >0 \\ -4(u - 1)(v + 1) & >-4 \\ (u - 1)(v + 1) & <1\end{aligned}
$$

 

This gives the solution $(v + 1)<\frac{1}{(u - 1)}$ for $(u - 1)>0$ and $(v + 1)>\frac{1}{(u - 1)}$ for $(u - 1)<0.$

Notice that the equation 

$$
(v + 1)=\frac{1}{(u - 1)}
$$

defines a hyperbola, and the coordinates of, say, $(2,-2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v + 1) \\ 4(u - 1)-{(v + 1)}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d19bc87bd47faf335f6b.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3979213a5676761da39d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8f4100dc9b543c613f18.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v + 1) \\ 4(u - 1)-{(v + 1)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & -1 \\ 4 & -2(v + 1)\end{aligned}| \\  & =2(u - 1)\cdot (-2(v + 1))-4\cdot (-1) \\  & =-4(u - 1)(v + 1)+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4(u - 1)(v + 1)+4 & >0 \\ -4(u - 1)(v + 1) & >-4 \\ (u - 1)(v + 1) & <1\end{aligned}
$$

 

This gives the solution $(v + 1)<\frac{1}{(u - 1)}$ for $(u - 1)>0$ and $(v + 1)>\frac{1}{(u - 1)}$ for $(u - 1)<0.$

Notice that the equation 

$$
(v + 1)=\frac{1}{(u - 1)}
$$

defines a hyperbola, and the coordinates of, say, $(2,-2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

Original worked solution

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}-v \\ 4u-{v}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2u & -1 \\ 4 & -2v\end{aligned}| \\  & =2u\cdot (-2v)-4\cdot (-1) \\  & =-4uv+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4uv+4 & >0 \\ -4uv & >-4 \\ uv & <1\end{aligned}
$$

 

This gives the solution $v<\frac{1}{u}$ for $u>0$ and $v>\frac{1}{u}$ for $u<0.$

Notice that the equation 

$$
v=\frac{1}{u}
$$

defines a hyperbola, and the coordinates of, say, $(1,-1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}-(v - 2) \\ 4(u + 1)-{(v - 2)}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-cfa4311efaa7d6903ff4.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3379269052602b004b7c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ff53fde06c10853cf930.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-553da6c26d2926fb384d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4955dad6870f7850adc2.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}-(v - 2) \\ 4(u + 1)-{(v - 2)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u + 1) & -1 \\ 4 & -2(v - 2)\end{aligned}| \\  & =2(u + 1)\cdot (-2(v - 2))-4\cdot (-1) \\  & =-4(u + 1)(v - 2)+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4(u + 1)(v - 2)+4 & >0 \\ -4(u + 1)(v - 2) & >-4 \\ (u + 1)(v - 2) & <1\end{aligned}
$$

 

This gives the solution $(v - 2)<\frac{1}{(u + 1)}$ for $(u + 1)>0$ and $(v - 2)>\frac{1}{(u + 1)}$ for $(u + 1)<0.$

Notice that the equation 

$$
(v - 2)=\frac{1}{(u + 1)}
$$

defines a hyperbola, and the coordinates of, say, $(0,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4955dad6870f7850adc2.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v - 2) \\ 4(u - 1)-{(v - 2)}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4390cfb0897ae8dc4afd.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d2b73dba7d0828d97099.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-0ebca27a59cf7a57ccbc.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c0b5d651811fd14dd142.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c660cdb49b8026b6c555.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v - 2) \\ 4(u - 1)-{(v - 2)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & -1 \\ 4 & -2(v - 2)\end{aligned}| \\  & =2(u - 1)\cdot (-2(v - 2))-4\cdot (-1) \\  & =-4(u - 1)(v - 2)+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4(u - 1)(v - 2)+4 & >0 \\ -4(u - 1)(v - 2) & >-4 \\ (u - 1)(v - 2) & <1\end{aligned}
$$

 

This gives the solution $(v - 2)<\frac{1}{(u - 1)}$ for $(u - 1)>0$ and $(v - 2)>\frac{1}{(u - 1)}$ for $(u - 1)<0.$

Notice that the equation 

$$
(v - 2)=\frac{1}{(u - 1)}
$$

defines a hyperbola, and the coordinates of, say, $(2,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-0ebca27a59cf7a57ccbc.png)

## Original q-161838

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}u+v \\ {u}^{2}+{v}^{2}\end{aligned}],
$$

is (locally) orientation-reversing?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/30/3033f0ae73e3f484fc5d3d65e388062feba1824fb3da9971d560cf2f518f49bb.png)

![](/media/jake/SSD/EDB/math/images/83/8382e54c1f91ff0e07910c1250c046413814748d9e7ef8968984b7223b43afcc.png)

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/7f/7f214af0b5d71689ec7f21fff043e1779f1d3244c13fdbaf7b8df7f408d66298.png)

![](/media/jake/SSD/EDB/math/images/14/14015cadab7d5dc8a9c33d0c1a57a44a79506bd01ba9b1cfe8ec1d280eb3fbb6.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u - 1)+(v + 1) \\ {(u - 1)}^{2}+{(v + 1)}^{2}\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c0e7397a50b442c9ec00.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7ca5a3c978e65cb3f9c3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-366d7bfabb1f0c8cfe57.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7da76c461943cd65bb14.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u - 1)+(v + 1) \\ {(u - 1)}^{2}+{(v + 1)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 2(u - 1) & 2(v + 1)\end{aligned}| \\  & =1\cdot (2(v + 1))-(2(u - 1))\cdot 1 \\  & =2(v + 1)-2(u - 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2(v + 1)-2(u - 1) & <0 \\ 2(v + 1) & <2(u - 1) \\ (v + 1) & <(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)=(u - 1)
$$

defines a straight line, and the coordinates of, say, $(2,-2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c0e7397a50b442c9ec00.png)

Original worked solution

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}u+v \\ {u}^{2}+{v}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 2u & 2v\end{aligned}| \\  & =1\cdot (2v)-(2u)\cdot 1 \\  & =2v-2u.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2v-2u & <0 \\ 2v & <2u \\ v & <u\end{aligned}
$$

 

Notice that the equation 

$$
v=u
$$

defines a straight line, and the coordinates of, say, $(1,-1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/media/jake/SSD/EDB/math/images/83/8382e54c1f91ff0e07910c1250c046413814748d9e7ef8968984b7223b43afcc.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u + 1)+(v - 2) \\ {(u + 1)}^{2}+{(v - 2)}^{2}\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2850f37ec994c18eec0c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f5cc28213f4ae50bbef6.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-518515168bf12d4ad69d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ab65afa46303c25674f1.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d0306dd5b56ab990c5cf.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u + 1)+(v - 2) \\ {(u + 1)}^{2}+{(v - 2)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 2(u + 1) & 2(v - 2)\end{aligned}| \\  & =1\cdot (2(v - 2))-(2(u + 1))\cdot 1 \\  & =2(v - 2)-2(u + 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2(v - 2)-2(u + 1) & <0 \\ 2(v - 2) & <2(u + 1) \\ (v - 2) & <(u + 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=(u + 1)
$$

defines a straight line, and the coordinates of, say, $(0,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d0306dd5b56ab990c5cf.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u - 1)+(v - 2) \\ {(u - 1)}^{2}+{(v - 2)}^{2}\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-141276b1a8f26e66b8d2.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-dfe19b5312fbc4090423.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e349d2ae5485468806b3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-506f81e71e5ae858692d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-877e0095838696bb6e08.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u - 1)+(v - 2) \\ {(u - 1)}^{2}+{(v - 2)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 2(u - 1) & 2(v - 2)\end{aligned}| \\  & =1\cdot (2(v - 2))-(2(u - 1))\cdot 1 \\  & =2(v - 2)-2(u - 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2(v - 2)-2(u - 1) & <0 \\ 2(v - 2) & <2(u - 1) \\ (v - 2) & <(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=(u - 1)
$$

defines a straight line, and the coordinates of, say, $(2,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e349d2ae5485468806b3.png)

## Original q-161842

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{3}-\frac{1}{2}{v}^{2} \\ u-\frac{1}{3}v\end{aligned}],
$$

is (locally) orientation-reversing?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/30/3033f0ae73e3f484fc5d3d65e388062feba1824fb3da9971d560cf2f518f49bb.png)

![](/media/jake/SSD/EDB/math/images/cb/cb5b22ff46569b231d122c2ed11bd412907f36271a033d86769435adf9fe48c7.png)

![](/media/jake/SSD/EDB/math/images/13/1368ee41963c1abcc320d2cd35449c08599582f37c7d68f750e137fcdcd2e57b.png)

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{3}-\frac{1}{2}{(v + 1)}^{2} \\ (u - 1)-\frac{1}{3}(v + 1)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-cb2513c5410e5c23a741.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7da76c461943cd65bb14.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8f4100dc9b543c613f18.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{3}-\frac{1}{2}{(v + 1)}^{2} \\ (u - 1)-\frac{1}{3}(v + 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}3{(u - 1)}^{2} & -(v + 1) \\ 1 & -\frac{1}{3}\end{aligned}| \\  & =(3{(u - 1)}^{2})\cdot (-\frac{1}{3})-(1)\cdot (-(v + 1)) \\  & =(v + 1)-{(u - 1)}^{2}.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}(v + 1)-{(u - 1)}^{2} & <0 \\ (v + 1) & <{(u - 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)={(u - 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(2,-2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8f4100dc9b543c613f18.png)

Original worked solution

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{3}-\frac{1}{2}{v}^{2} \\ u-\frac{1}{3}v\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}3{u}^{2} & -v \\ 1 & -\frac{1}{3}\end{aligned}| \\  & =(3{u}^{2})\cdot (-\frac{1}{3})-(1)\cdot (-v) \\  & =v-{u}^{2}.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}v-{u}^{2} & <0 \\ v & <{u}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
v={u}^{2}
$$

defines a parabola, and the coordinates of, say, $(1,-1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/media/jake/SSD/EDB/math/images/13/1368ee41963c1abcc320d2cd35449c08599582f37c7d68f750e137fcdcd2e57b.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{3}-\frac{1}{2}{(v - 2)}^{2} \\ (u + 1)-\frac{1}{3}(v - 2)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ba1400051583712bb99e.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-fa98e5173b824a7e8d95.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-863018907e01b16deee0.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-cd1dc1a2f433077ea151.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ec91559083e4fdbe0d8f.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{3}-\frac{1}{2}{(v - 2)}^{2} \\ (u + 1)-\frac{1}{3}(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}3{(u + 1)}^{2} & -(v - 2) \\ 1 & -\frac{1}{3}\end{aligned}| \\  & =(3{(u + 1)}^{2})\cdot (-\frac{1}{3})-(1)\cdot (-(v - 2)) \\  & =(v - 2)-{(u + 1)}^{2}.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}(v - 2)-{(u + 1)}^{2} & <0 \\ (v - 2) & <{(u + 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)={(u + 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(0,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ec91559083e4fdbe0d8f.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{3}-\frac{1}{2}{(v - 2)}^{2} \\ (u - 1)-\frac{1}{3}(v - 2)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8c5aa38a4536a60303c5.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-86b3cc3b9a3b945791e6.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-006aace0527798817722.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-26f65bf0f9b34f7a5ca0.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a7af09fc117b0b097e81.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{3}-\frac{1}{2}{(v - 2)}^{2} \\ (u - 1)-\frac{1}{3}(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}3{(u - 1)}^{2} & -(v - 2) \\ 1 & -\frac{1}{3}\end{aligned}| \\  & =(3{(u - 1)}^{2})\cdot (-\frac{1}{3})-(1)\cdot (-(v - 2)) \\  & =(v - 2)-{(u - 1)}^{2}.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}(v - 2)-{(u - 1)}^{2} & <0 \\ (v - 2) & <{(u - 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)={(u - 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(2,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-006aace0527798817722.png)

## Original q-161843

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}4u+{v}^{2} \\ v-{u}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/c2/c244350524a52123e2e97db4cd8eb4f57737b8b15746eb72a8d54eac32a4f3cf.png)

![](/media/jake/SSD/EDB/math/images/c5/c501e7e341af57e86f18d73871314800d453f79572e16ccf2477335352d4dcdc.png)

![](/media/jake/SSD/EDB/math/images/9c/9cd254ac65dedfa4c720b18afd4f5c3c7676b4f21170930f78e9adac276317ee.png)

![](/media/jake/SSD/EDB/math/images/13/1368ee41963c1abcc320d2cd35449c08599582f37c7d68f750e137fcdcd2e57b.png)

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}4(u - 1)+{(v + 1)}^{2} \\ (v + 1)-{(u - 1)}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-bb688f71d9a2046ac3f5.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-38ebdfeb2d9fc32af272.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8f4100dc9b543c613f18.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ee2e459c6acbc544f2ba.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}4(u - 1)+{(v + 1)}^{2} \\ (v + 1)-{(u - 1)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}4 & 2(v + 1) \\ -2(u - 1) & 1\end{aligned}| \\  & =4\cdot 1-(-2(u - 1))\cdot (2(v + 1)) \\  & =4+4(u - 1)(v + 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}4+4(u - 1)(v + 1) & >0 \\ 4(u - 1)(v + 1) & >-4 \\ (u - 1)(v + 1) & >-1\end{aligned}
$$

 

This gives the solution $(v + 1)>-\frac{1}{(u - 1)}$ for $(u - 1)>0$ and $(v + 1)<-\frac{1}{(u - 1)}$ for $(u - 1)<0.$

Notice that the equation 

$$
(v + 1)=-\frac{1}{(u - 1)}
$$

defines a hyperbola, and the coordinates of, say, $(2,0)$ and $(0,-2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

  

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-38ebdfeb2d9fc32af272.png)

Original worked solution

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}4u+{v}^{2} \\ v-{u}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}4 & 2v \\ -2u & 1\end{aligned}| \\  & =4\cdot 1-(-2u)\cdot (2v) \\  & =4+4uv.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}4+4uv & >0 \\ 4uv & >-4 \\ uv & >-1\end{aligned}
$$

 

This gives the solution $v>-\frac{1}{u}$ for $u>0$ and $v<-\frac{1}{u}$ for $u<0.$

Notice that the equation 

$$
v=-\frac{1}{u}
$$

defines a hyperbola, and the coordinates of, say, $(1,1)$ and $(-1,-1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

  

![](/media/jake/SSD/EDB/math/images/c5/c501e7e341af57e86f18d73871314800d453f79572e16ccf2477335352d4dcdc.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}4(u + 1)+{(v - 2)}^{2} \\ (v - 2)-{(u + 1)}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2c8a1c6a585d6be13d29.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-553da6c26d2926fb384d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-fc8cfb31ac3962ee11f5.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3379269052602b004b7c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a7ab2e04b93fd0c54df2.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}4(u + 1)+{(v - 2)}^{2} \\ (v - 2)-{(u + 1)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}4 & 2(v - 2) \\ -2(u + 1) & 1\end{aligned}| \\  & =4\cdot 1-(-2(u + 1))\cdot (2(v - 2)) \\  & =4+4(u + 1)(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}4+4(u + 1)(v - 2) & >0 \\ 4(u + 1)(v - 2) & >-4 \\ (u + 1)(v - 2) & >-1\end{aligned}
$$

 

This gives the solution $(v - 2)>-\frac{1}{(u + 1)}$ for $(u + 1)>0$ and $(v - 2)<-\frac{1}{(u + 1)}$ for $(u + 1)<0.$

Notice that the equation 

$$
(v - 2)=-\frac{1}{(u + 1)}
$$

defines a hyperbola, and the coordinates of, say, $(0,3)$ and $(-2,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

  

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a7ab2e04b93fd0c54df2.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}4(u - 1)+{(v - 2)}^{2} \\ (v - 2)-{(u - 1)}^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c660cdb49b8026b6c555.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-cf1679bea7c2cee81cc4.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ff3ff3f79973165ccc0a.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-85a47083a8042bf12bee.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4390cfb0897ae8dc4afd.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}4(u - 1)+{(v - 2)}^{2} \\ (v - 2)-{(u - 1)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}4 & 2(v - 2) \\ -2(u - 1) & 1\end{aligned}| \\  & =4\cdot 1-(-2(u - 1))\cdot (2(v - 2)) \\  & =4+4(u - 1)(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}4+4(u - 1)(v - 2) & >0 \\ 4(u - 1)(v - 2) & >-4 \\ (u - 1)(v - 2) & >-1\end{aligned}
$$

 

This gives the solution $(v - 2)>-\frac{1}{(u - 1)}$ for $(u - 1)>0$ and $(v - 2)<-\frac{1}{(u - 1)}$ for $(u - 1)<0.$

Notice that the equation 

$$
(v - 2)=-\frac{1}{(u - 1)}
$$

defines a hyperbola, and the coordinates of, say, $(2,3)$ and $(0,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

  

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ff3ff3f79973165ccc0a.png)

## Original q-161855

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{uv} \\ {u}^{2}+v\end{aligned}],
$$

is (locally) orientation-preserving?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/61/613e83ce5ad6154905ec9001ece078309e396561e251e85455ff261bb4cd61a0.png)

![](/media/jake/SSD/EDB/math/images/9e/9ecab1b0f048e83b57d04a60c1cf20ee5ed0e61257577cf42c1a091976c04473.png)

![](/media/jake/SSD/EDB/math/images/7f/7fc8ce1e1eaa3eb4e4acbbc167bdc4a479591bea21d2acdeaf799bd99d6b1150.png)

![](/media/jake/SSD/EDB/math/images/13/1368ee41963c1abcc320d2cd35449c08599582f37c7d68f750e137fcdcd2e57b.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u - 1)(v + 1)} \\ {(u - 1)}^{2}+(v + 1)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3a8b4a84721fc559c740.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-adcc252110a0dfe48796.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-de53b97e811ff4ad5539.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8f4100dc9b543c613f18.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u - 1)(v + 1)} \\ {(u - 1)}^{2}+(v + 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}(v + 1){e}^{(u - 1)(v + 1)} & (u - 1){e}^{(u - 1)(v + 1)} \\ 2(u - 1) & 1\end{aligned}| \\  & =(v + 1){e}^{(u - 1)(v + 1)}\cdot (1)-(2(u - 1))\cdot (u - 1){e}^{(u - 1)(v + 1)} \\  & ={e}^{(u - 1)(v + 1)}((v + 1)-2{(u - 1)}^{2}).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{e}^{(u - 1)(v + 1)}((v + 1)-2{(u - 1)}^{2}) & >0 \\ (v + 1)-2{(u - 1)}^{2} & >0 \\ (v + 1) & >2{(u - 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)=2{(u - 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(1,0)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-adcc252110a0dfe48796.png)

Original worked solution

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{uv} \\ {u}^{2}+v\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}v{e}^{uv} & u{e}^{uv} \\ 2u & 1\end{aligned}| \\  & =v{e}^{uv}\cdot (1)-(2u)\cdot u{e}^{uv} \\  & ={e}^{uv}(v-2{u}^{2}).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{e}^{uv}(v-2{u}^{2}) & >0 \\ v-2{u}^{2} & >0 \\ v & >2{u}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
v=2{u}^{2}
$$

defines a parabola, and the coordinates of, say, $(0,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/media/jake/SSD/EDB/math/images/61/613e83ce5ad6154905ec9001ece078309e396561e251e85455ff261bb4cd61a0.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u + 1)(v - 2)} \\ {(u + 1)}^{2}+(v - 2)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3c75a0256f68eda4213e.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ea01ec3b3980dc6177fc.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a620694862ea281286d4.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a04f9c2ad359b98cf36c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-76c284fe1199349ba684.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u + 1)(v - 2)} \\ {(u + 1)}^{2}+(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}(v - 2){e}^{(u + 1)(v - 2)} & (u + 1){e}^{(u + 1)(v - 2)} \\ 2(u + 1) & 1\end{aligned}| \\  & =(v - 2){e}^{(u + 1)(v - 2)}\cdot (1)-(2(u + 1))\cdot (u + 1){e}^{(u + 1)(v - 2)} \\  & ={e}^{(u + 1)(v - 2)}((v - 2)-2{(u + 1)}^{2}).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{e}^{(u + 1)(v - 2)}((v - 2)-2{(u + 1)}^{2}) & >0 \\ (v - 2)-2{(u + 1)}^{2} & >0 \\ (v - 2) & >2{(u + 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=2{(u + 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(-1,3)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-76c284fe1199349ba684.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u - 1)(v - 2)} \\ {(u - 1)}^{2}+(v - 2)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-5d9e43cf0ca60082100f.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-9ef7b63e7d01e765a48b.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f4f646fadfdb8d103ac1.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-b4a247d49d2d52840f59.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-70c25559b47886d7ae95.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u - 1)(v - 2)} \\ {(u - 1)}^{2}+(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}(v - 2){e}^{(u - 1)(v - 2)} & (u - 1){e}^{(u - 1)(v - 2)} \\ 2(u - 1) & 1\end{aligned}| \\  & =(v - 2){e}^{(u - 1)(v - 2)}\cdot (1)-(2(u - 1))\cdot (u - 1){e}^{(u - 1)(v - 2)} \\  & ={e}^{(u - 1)(v - 2)}((v - 2)-2{(u - 1)}^{2}).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{e}^{(u - 1)(v - 2)}((v - 2)-2{(u - 1)}^{2}) & >0 \\ (v - 2)-2{(u - 1)}^{2} & >0 \\ (v - 2) & >2{(u - 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=2{(u - 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(1,3)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f4f646fadfdb8d103ac1.png)

## Original q-161835

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}uv \\ u+v\end{aligned}],
$$

is (locally) orientation-preserving?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/42/427cb4b8e6497f75aecfe809aa084b0bf6f4ad167f3a0838aa40b1a50d115e1d.png)

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/30/3033f0ae73e3f484fc5d3d65e388062feba1824fb3da9971d560cf2f518f49bb.png)

![](/media/jake/SSD/EDB/math/images/0b/0b764651dbc7999e7af13214685796b5045fab89f101bbc72bf413112df3c51f.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u - 1)(v + 1) \\ (u - 1)+(v + 1)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7da76c461943cd65bb14.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c0e7397a50b442c9ec00.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-366d7bfabb1f0c8cfe57.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u - 1)(v + 1) \\ (u - 1)+(v + 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}(v + 1) & (u - 1) \\ 1 & 1\end{aligned}| \\  & =(v + 1)\cdot 1-1\cdot (u - 1) \\  & =(v + 1)-(u - 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}(v + 1)-(u - 1) & >0 \\ (v + 1) & >(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)=(u - 1)
$$

defines a line, and the coordinates of, say, $(2,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-366d7bfabb1f0c8cfe57.png)

Original worked solution

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}uv \\ u+v\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}v & u \\ 1 & 1\end{aligned}| \\  & =v\cdot 1-1\cdot u \\  & =v-u.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}v-u & >0 \\ v & >u\end{aligned}
$$

 

Notice that the equation 

$$
v=u
$$

defines a line, and the coordinates of, say, $(1,2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/media/jake/SSD/EDB/math/images/42/427cb4b8e6497f75aecfe809aa084b0bf6f4ad167f3a0838aa40b1a50d115e1d.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u + 1)(v - 2) \\ (u + 1)+(v - 2)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-518515168bf12d4ad69d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d0306dd5b56ab990c5cf.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2850f37ec994c18eec0c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d31b891d105ad9e65cf9.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f5cc28213f4ae50bbef6.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u + 1)(v - 2) \\ (u + 1)+(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}(v - 2) & (u + 1) \\ 1 & 1\end{aligned}| \\  & =(v - 2)\cdot 1-1\cdot (u + 1) \\  & =(v - 2)-(u + 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}(v - 2)-(u + 1) & >0 \\ (v - 2) & >(u + 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=(u + 1)
$$

defines a line, and the coordinates of, say, $(0,4)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f5cc28213f4ae50bbef6.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u - 1)(v - 2) \\ (u - 1)+(v - 2)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e349d2ae5485468806b3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-506f81e71e5ae858692d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-141276b1a8f26e66b8d2.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-dfe19b5312fbc4090423.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3c8c6102de94d89edfd5.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}(u - 1)(v - 2) \\ (u - 1)+(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}(v - 2) & (u - 1) \\ 1 & 1\end{aligned}| \\  & =(v - 2)\cdot 1-1\cdot (u - 1) \\  & =(v - 2)-(u - 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}(v - 2)-(u - 1) & >0 \\ (v - 2) & >(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=(u - 1)
$$

defines a line, and the coordinates of, say, $(2,4)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-141276b1a8f26e66b8d2.png)

## Original q-161837

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{3}{u}^{3}+v \\ uv\end{aligned}],
$$

is (locally) orientation-reversing?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

![](/media/jake/SSD/EDB/math/images/30/3033f0ae73e3f484fc5d3d65e388062feba1824fb3da9971d560cf2f518f49bb.png)

![](/media/jake/SSD/EDB/math/images/d5/d5889bd5e8d537757de25a7b1a868ff8a903da14c9088c5f8de5a70d8b078552.png)

![](/media/jake/SSD/EDB/math/images/cb/cb5b22ff46569b231d122c2ed11bd412907f36271a033d86769435adf9fe48c7.png)

![](/media/jake/SSD/EDB/math/images/b0/b0171dfd42295e39cd45186e8edba3a5105fbd1bd02a1621223091de75815f61.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{3}{(u - 1)}^{3}+(v + 1) \\ (u - 1)(v + 1)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-763da57bbd850d157a53.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7da76c461943cd65bb14.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-cb2513c5410e5c23a741.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-cf1050d8029ade21dca3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{3}{(u - 1)}^{3}+(v + 1) \\ (u - 1)(v + 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{(u - 1)}^{2} & 1 \\ (v + 1) & (u - 1)\end{aligned}| \\  & ={(u - 1)}^{2}\cdot (u - 1)-(v + 1)\cdot 1 \\  & ={(u - 1)}^{3}-(v + 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{(u - 1)}^{3}-(v + 1) & <0 \\ (v + 1) & >{(u - 1)}^{3}\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)={(u - 1)}^{3}
$$

defines a cubic function, and the coordinates of, say, $(0,0)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-cb2513c5410e5c23a741.png)

Original worked solution

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{3}{u}^{3}+v \\ uv\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{u}^{2} & 1 \\ v & u\end{aligned}| \\  & ={u}^{2}\cdot u-v\cdot 1 \\  & ={u}^{3}-v.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{u}^{3}-v & <0 \\ v & >{u}^{3}\end{aligned}
$$

 

Notice that the equation 

$$
v={u}^{3}
$$

defines a cubic function, and the coordinates of, say, $(-1,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/media/jake/SSD/EDB/math/images/cb/cb5b22ff46569b231d122c2ed11bd412907f36271a033d86769435adf9fe48c7.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{3}{(u + 1)}^{3}+(v - 2) \\ (u + 1)(v - 2)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-bec6fa2dfcfa322e8b9b.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2126fd76c940032949e7.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-88c9704699bbfcda31eb.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-db4b7932eb5cd38cc422.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-6ac58622cfe099f62032.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{3}{(u + 1)}^{3}+(v - 2) \\ (u + 1)(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{(u + 1)}^{2} & 1 \\ (v - 2) & (u + 1)\end{aligned}| \\  & ={(u + 1)}^{2}\cdot (u + 1)-(v - 2)\cdot 1 \\  & ={(u + 1)}^{3}-(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{(u + 1)}^{3}-(v - 2) & <0 \\ (v - 2) & >{(u + 1)}^{3}\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)={(u + 1)}^{3}
$$

defines a cubic function, and the coordinates of, say, $(-2,3)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-6ac58622cfe099f62032.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{3}{(u - 1)}^{3}+(v - 2) \\ (u - 1)(v - 2)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-701dccb76a764263659f.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-960d9d85e0c4eb206b83.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-29a7325baad234d4719f.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-1eee9ca0db143a758209.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-83180666f407d7901f9f.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{3}{(u - 1)}^{3}+(v - 2) \\ (u - 1)(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{(u - 1)}^{2} & 1 \\ (v - 2) & (u - 1)\end{aligned}| \\  & ={(u - 1)}^{2}\cdot (u - 1)-(v - 2)\cdot 1 \\  & ={(u - 1)}^{3}-(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{(u - 1)}^{3}-(v - 2) & <0 \\ (v - 2) & >{(u - 1)}^{3}\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)={(u - 1)}^{3}
$$

defines a cubic function, and the coordinates of, say, $(0,3)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-29a7325baad234d4719f.png)

## Original q-161839

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}-v \\ uv+1\end{aligned}],
$$

is (locally) orientation-preserving?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

![](/media/jake/SSD/EDB/math/images/8b/8b35fbafaf8d121bceef7a0763253df075fe4fe85eb3c992f95c59d05f986c67.png)

![](/media/jake/SSD/EDB/math/images/09/09f7f36ecc2197cc95e1878fa22ac22367978809a5241f09886a7eb2fab071f3.png)

![](/media/jake/SSD/EDB/math/images/10/105e6e8a010b7b9001f75cf17e11cbbc1e031d83cbc2ddfafc3595c745106f3f.png)

![](/media/jake/SSD/EDB/math/images/09/090bab0ac1c6356010d83a6ad54c59b53b7dd12062fb5e331a936ce3f3a1b411.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v + 1) \\ (u - 1)(v + 1)+1\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a368c5ffeacd23bcd509.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-b2838ae2dea04fb76fd1.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-adcc252110a0dfe48796.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3979213a5676761da39d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v + 1) \\ (u - 1)(v + 1)+1\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & -1 \\ (v + 1) & (u - 1)\end{aligned}| \\  & =2(u - 1)\cdot (u - 1)-(v + 1)\cdot (-1) \\  & =2{(u - 1)}^{2}+(v + 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2{(u - 1)}^{2}+(v + 1) & >0 \\ (v + 1) & >-2{(u - 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)=-2{(u - 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(2,0)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-b2838ae2dea04fb76fd1.png)

Original worked solution

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}-v \\ uv+1\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2u & -1 \\ v & u\end{aligned}| \\  & =2u\cdot u-v\cdot (-1) \\  & =2{u}^{2}+v.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2{u}^{2}+v & >0 \\ v & >-2{u}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
v=-2{u}^{2}
$$

defines a parabola, and the coordinates of, say, $(1,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/media/jake/SSD/EDB/math/images/8b/8b35fbafaf8d121bceef7a0763253df075fe4fe85eb3c992f95c59d05f986c67.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}-(v - 2) \\ (u + 1)(v - 2)+1\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c702ed6605f89f4f46ea.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-6316231e29e7046db7e7.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-37e6bea3b38ee3c1bfb1.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-76c284fe1199349ba684.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a04f9c2ad359b98cf36c.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}-(v - 2) \\ (u + 1)(v - 2)+1\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u + 1) & -1 \\ (v - 2) & (u + 1)\end{aligned}| \\  & =2(u + 1)\cdot (u + 1)-(v - 2)\cdot (-1) \\  & =2{(u + 1)}^{2}+(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2{(u + 1)}^{2}+(v - 2) & >0 \\ (v - 2) & >-2{(u + 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=-2{(u + 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(0,3)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a04f9c2ad359b98cf36c.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v - 2) \\ (u - 1)(v - 2)+1\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-b5cc8b72f3c4238aec83.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4014b5ad768fb1a454c8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-70c25559b47886d7ae95.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a8afeac449e380422d41.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f4f646fadfdb8d103ac1.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}-(v - 2) \\ (u - 1)(v - 2)+1\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & -1 \\ (v - 2) & (u - 1)\end{aligned}| \\  & =2(u - 1)\cdot (u - 1)-(v - 2)\cdot (-1) \\  & =2{(u - 1)}^{2}+(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2{(u - 1)}^{2}+(v - 2) & >0 \\ (v - 2) & >-2{(u - 1)}^{2}\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=-2{(u - 1)}^{2}
$$

defines a parabola, and the coordinates of, say, $(2,3)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-70c25559b47886d7ae95.png)

## Original q-161840

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}+{v}^{2} \\ v-u\end{aligned}],
$$

is (locally) orientation-reversing?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/c2/c244350524a52123e2e97db4cd8eb4f57737b8b15746eb72a8d54eac32a4f3cf.png)

![](/media/jake/SSD/EDB/math/images/13/1368ee41963c1abcc320d2cd35449c08599582f37c7d68f750e137fcdcd2e57b.png)

![](/media/jake/SSD/EDB/math/images/fd/fd2a51ca3a1654c2e857018268bf251366472a2c5d7f90009d5ccfbf1b1edd9d.png)

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/95/95bf5e059fda0fc1ba8423b35fffa57d9cae0cc2a2a7e40b0c2539b6a7ae7678.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}+{(v + 1)}^{2} \\ (v + 1)-(u - 1)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7ca5a3c978e65cb3f9c3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-8f4100dc9b543c613f18.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-96dea2820ffaeb290234.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ee2e459c6acbc544f2ba.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}+{(v + 1)}^{2} \\ (v + 1)-(u - 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & 2(v + 1) \\ -1 & 1\end{aligned}| \\  & =2(u - 1)\cdot 1-(-1)\cdot (2(v + 1)) \\  & =2(u - 1)+2(v + 1).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2(u - 1)+2(v + 1) & <0 \\ 2(v + 1) & <-2(u - 1) \\ (v + 1) & <-(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)=-(u - 1)
$$

defines a straight line, and the coordinates of, say, $(0,-2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ee2e459c6acbc544f2ba.png)

Original worked solution

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}+{v}^{2} \\ v-u\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2u & 2v \\ -1 & 1\end{aligned}| \\  & =2u\cdot 1-(-1)\cdot (2v) \\  & =2u+2v.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2u+2v & <0 \\ 2v & <-2u \\ v & <-u\end{aligned}
$$

 

Notice that the equation 

$$
v=-u
$$

defines a straight line, and the coordinates of, say, $(-1,-1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/media/jake/SSD/EDB/math/images/c2/c244350524a52123e2e97db4cd8eb4f57737b8b15746eb72a8d54eac32a4f3cf.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}+{(v - 2)}^{2} \\ (v - 2)-(u + 1)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7e86241e9217c2175da1.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d31b891d105ad9e65cf9.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a9cc359cca1b5fc6ed26.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d0306dd5b56ab990c5cf.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ab65afa46303c25674f1.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}+{(v - 2)}^{2} \\ (v - 2)-(u + 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u + 1) & 2(v - 2) \\ -1 & 1\end{aligned}| \\  & =2(u + 1)\cdot 1-(-1)\cdot (2(v - 2)) \\  & =2(u + 1)+2(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2(u + 1)+2(v - 2) & <0 \\ 2(v - 2) & <-2(u + 1) \\ (v - 2) & <-(u + 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=-(u + 1)
$$

defines a straight line, and the coordinates of, say, $(-2,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ab65afa46303c25674f1.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}+{(v - 2)}^{2} \\ (v - 2)-(u - 1)\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3c8c6102de94d89edfd5.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d4b5896cdb596cf77dd9.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-877e0095838696bb6e08.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-1087820b9d06d8fca977.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e349d2ae5485468806b3.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}+{(v - 2)}^{2} \\ (v - 2)-(u - 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & 2(v - 2) \\ -1 & 1\end{aligned}| \\  & =2(u - 1)\cdot 1-(-1)\cdot (2(v - 2)) \\  & =2(u - 1)+2(v - 2).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}2(u - 1)+2(v - 2) & <0 \\ 2(v - 2) & <-2(u - 1) \\ (v - 2) & <-(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=-(u - 1)
$$

defines a straight line, and the coordinates of, say, $(0,1)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-877e0095838696bb6e08.png)

## Original q-161841

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{u+v} \\ -uv\end{aligned}],
$$

is (locally) orientation-preserving?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/c2/c244350524a52123e2e97db4cd8eb4f57737b8b15746eb72a8d54eac32a4f3cf.png)

![](/media/jake/SSD/EDB/math/images/8b/8bec16b8ed5083071e21761e6b2e649e136ce0662f7e5ab764161491094c0609.png)

![](/media/jake/SSD/EDB/math/images/fd/fd2a51ca3a1654c2e857018268bf251366472a2c5d7f90009d5ccfbf1b1edd9d.png)

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/0b/0b764651dbc7999e7af13214685796b5045fab89f101bbc72bf413112df3c51f.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u - 1)+(v + 1)} \\ -(u - 1)(v + 1)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7ca5a3c978e65cb3f9c3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-366d7bfabb1f0c8cfe57.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c0e7397a50b442c9ec00.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ee2e459c6acbc544f2ba.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u - 1)+(v + 1)} \\ -(u - 1)(v + 1)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{(u - 1)+(v + 1)} & {e}^{(u - 1)+(v + 1)} \\ -(v + 1) & -(u - 1)\end{aligned}| \\  & ={e}^{(u - 1)+(v + 1)}\cdot (-(u - 1))-(-(v + 1))\cdot {e}^{(u - 1)+(v + 1)} \\  & ={e}^{(u - 1)+(v + 1)}((v + 1)-(u - 1)).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{e}^{(u - 1)+(v + 1)}((v + 1)-(u - 1)) & >0 \\ (v + 1)-(u - 1) & >0 \\ (v + 1) & >(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v + 1)=(u - 1)
$$

defines a straight line, and the coordinates of, say, $(3,2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-366d7bfabb1f0c8cfe57.png)

Original worked solution

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{u+v} \\ -uv\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{u+v} & {e}^{u+v} \\ -v & -u\end{aligned}| \\  & ={e}^{u+v}\cdot (-u)-(-v)\cdot {e}^{u+v} \\  & ={e}^{u+v}(v-u).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{e}^{u+v}(v-u) & >0 \\ v-u & >0 \\ v & >u\end{aligned}
$$

 

Notice that the equation 

$$
v=u
$$

defines a straight line, and the coordinates of, say, $(2,3)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/media/jake/SSD/EDB/math/images/8b/8bec16b8ed5083071e21761e6b2e649e136ce0662f7e5ab764161491094c0609.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u + 1)+(v - 2)} \\ -(u + 1)(v - 2)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-518515168bf12d4ad69d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d0306dd5b56ab990c5cf.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2850f37ec994c18eec0c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d31b891d105ad9e65cf9.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f5cc28213f4ae50bbef6.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u + 1)+(v - 2)} \\ -(u + 1)(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{(u + 1)+(v - 2)} & {e}^{(u + 1)+(v - 2)} \\ -(v - 2) & -(u + 1)\end{aligned}| \\  & ={e}^{(u + 1)+(v - 2)}\cdot (-(u + 1))-(-(v - 2))\cdot {e}^{(u + 1)+(v - 2)} \\  & ={e}^{(u + 1)+(v - 2)}((v - 2)-(u + 1)).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{e}^{(u + 1)+(v - 2)}((v - 2)-(u + 1)) & >0 \\ (v - 2)-(u + 1) & >0 \\ (v - 2) & >(u + 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=(u + 1)
$$

defines a straight line, and the coordinates of, say, $(1,5)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-f5cc28213f4ae50bbef6.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u - 1)+(v - 2)} \\ -(u - 1)(v - 2)\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e349d2ae5485468806b3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-506f81e71e5ae858692d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-141276b1a8f26e66b8d2.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-dfe19b5312fbc4090423.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3c8c6102de94d89edfd5.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0.
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{(u - 1)+(v - 2)} \\ -(u - 1)(v - 2)\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{(u - 1)+(v - 2)} & {e}^{(u - 1)+(v - 2)} \\ -(v - 2) & -(u - 1)\end{aligned}| \\  & ={e}^{(u - 1)+(v - 2)}\cdot (-(u - 1))-(-(v - 2))\cdot {e}^{(u - 1)+(v - 2)} \\  & ={e}^{(u - 1)+(v - 2)}((v - 2)-(u - 1)).\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}{e}^{(u - 1)+(v - 2)}((v - 2)-(u - 1)) & >0 \\ (v - 2)-(u - 1) & >0 \\ (v - 2) & >(u - 1)\end{aligned}
$$

 

Notice that the equation 

$$
(v - 2)=(u - 1)
$$

defines a straight line, and the coordinates of, say, $(3,5)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-141276b1a8f26e66b8d2.png)

## Original q-161856

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}+2v \\ -2u-{v}^{2}\end{aligned}],
$$

is (locally) orientation-reversing?

Original raw bank 0

![](/media/jake/SSD/EDB/math/images/c2/c244350524a52123e2e97db4cd8eb4f57737b8b15746eb72a8d54eac32a4f3cf.png)

![](/media/jake/SSD/EDB/math/images/4d/4d944eb13437b86c0cf6ae4fa8bca09031ed0f2f85a9f20bcb0050a6de9f8ebb.png)

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

![](/media/jake/SSD/EDB/math/images/fe/fe7bb422a3f992ea88a900e63b2c55df99bce3a785929901c248abadfadf23f1.png)

![](/media/jake/SSD/EDB/math/images/f7/f7bc22ac4dfd2d7015952144ece63f91ecccef2a992649aece60dc8a70f1d018.png)

### Generated explicit observed bank variant: observed

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}+2(v + 1) \\ -2(u - 1)-{(v + 1)}^{2}\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-240f1e253b60dead14fa.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-39defdf4275c4be4e16c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-bb688f71d9a2046ac3f5.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ee2e459c6acbc544f2ba.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}+2(v + 1) \\ -2(u - 1)-{(v + 1)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & 2 \\ -2 & -2(v + 1)\end{aligned}| \\  & =2(u - 1)\cdot (-2(v + 1))-(-2)\cdot 2 \\  & =-4(u - 1)(v + 1)+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4(u - 1)(v + 1)+4 & <0 \\ -4(u - 1)(v + 1) & <-4 \\ (u - 1)(v + 1) & >1\end{aligned}
$$

 

This gives the solution $(v + 1)>\frac{1}{(u - 1)}$ for $(u - 1)>0$ and $(v + 1)<\frac{1}{(u - 1)}$ for $(u - 1)<0.$

Notice that the equation 

$$
(v + 1)=\frac{1}{(u - 1)}
$$

defines a hyperbola, and the coordinates of, say, $(2,1)$ and $(0,-3)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

   

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e9ca1df2e689a6e664a8.png)

Original worked solution

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}+2v \\ -2u-{v}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2u & 2 \\ -2 & -2v\end{aligned}| \\  & =2u\cdot (-2v)-(-2)\cdot 2 \\  & =-4uv+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4uv+4 & <0 \\ -4uv & <-4 \\ uv & >1\end{aligned}
$$

 

This gives the solution $v>\frac{1}{u}$ for $u>0$ and $v<\frac{1}{u}$ for $u<0.$

Notice that the equation 

$$
v=\frac{1}{u}
$$

defines a hyperbola, and the coordinates of, say, $(1,2)$ and $(-1,-2)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

   

![](/media/jake/SSD/EDB/math/images/d4/d477a9f312fc2fb0a5a4c2d13164c96118aa70b53cf23db80be9ec698151e6fd.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}+2(v - 2) \\ -2(u + 1)-{(v - 2)}^{2}\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ff53fde06c10853cf930.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4955dad6870f7850adc2.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-cfa4311efaa7d6903ff4.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a7ab2e04b93fd0c54df2.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3379269052602b004b7c.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u + 1)}^{2}+2(v - 2) \\ -2(u + 1)-{(v - 2)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u + 1) & 2 \\ -2 & -2(v - 2)\end{aligned}| \\  & =2(u + 1)\cdot (-2(v - 2))-(-2)\cdot 2 \\  & =-4(u + 1)(v - 2)+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4(u + 1)(v - 2)+4 & <0 \\ -4(u + 1)(v - 2) & <-4 \\ (u + 1)(v - 2) & >1\end{aligned}
$$

 

This gives the solution $(v - 2)>\frac{1}{(u + 1)}$ for $(u + 1)>0$ and $(v - 2)<\frac{1}{(u + 1)}$ for $(u + 1)<0.$

Notice that the equation 

$$
(v - 2)=\frac{1}{(u + 1)}
$$

defines a hyperbola, and the coordinates of, say, $(0,4)$ and $(-2,0)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

   

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-3379269052602b004b7c.png)

### Generated authored default variant

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}+2(v - 2) \\ -2(u - 1)-{(v - 2)}^{2}\end{aligned}],
$$

is (locally) orientation-reversing?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-0ebca27a59cf7a57ccbc.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c0b5d651811fd14dd142.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4390cfb0897ae8dc4afd.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d2b73dba7d0828d97099.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ff3ff3f79973165ccc0a.png)

Worked solution:

Recall that a transformation is (locally) orientation-reversing at the points where the Jacobian determinant is negative:

$$
\frac{∂(x,y)}{∂(u,v)}<0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{(u - 1)}^{2}+2(v - 2) \\ -2(u - 1)-{(v - 2)}^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2(u - 1) & 2 \\ -2 & -2(v - 2)\end{aligned}| \\  & =2(u - 1)\cdot (-2(v - 2))-(-2)\cdot 2 \\  & =-4(u - 1)(v - 2)+4.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}-4(u - 1)(v - 2)+4 & <0 \\ -4(u - 1)(v - 2) & <-4 \\ (u - 1)(v - 2) & >1\end{aligned}
$$

 

This gives the solution $(v - 2)>\frac{1}{(u - 1)}$ for $(u - 1)>0$ and $(v - 2)<\frac{1}{(u - 1)}$ for $(u - 1)<0.$

Notice that the equation 

$$
(v - 2)=\frac{1}{(u - 1)}
$$

defines a hyperbola, and the coordinates of, say, $(2,4)$ and $(0,0)$ satisfy the inequality. 

Therefore, the region where the transformation is (locally) orientation-reversing must be the following:

   

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4390cfb0897ae8dc4afd.png)

## Generated authored easy

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\left(u + 2\right)^{2} \\ 3 v - 6\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-5bd1df48180fb99d9508.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-126ed4a574a85b2f2b41.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e0cf807a64aed2da341d.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-36971fd0a07b8c008768.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2e1d17216704e46f7306.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\left(u + 2\right)^{2} \\ 3 v - 6\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} &=\begin{vmatrix}2 u + 4 & 0 \\ 0 & 3\end{vmatrix} \\ &=(2 u + 4)\cdot (3)-(0)\cdot (0) \\ &=6 u + 12.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}6 u + 12 &>0 \\ u > -2\end{aligned}
$$

Notice that the equation

$$
u = -2
$$

defines a vertical line.

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-5bd1df48180fb99d9508.png)

## Generated authored easy

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3 \left(u - 1\right)^{2} \\ 3 v - 6\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-0532f80712ef65ec2bd8.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-62344757bdd2492eea5a.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-231ec3ace564781761c1.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c9db071323b90cf34003.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-44e5c3b380b2a7bc22c5.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3 \left(u - 1\right)^{2} \\ 3 v - 6\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} &=\begin{vmatrix}6 u - 6 & 0 \\ 0 & 3\end{vmatrix} \\ &=(6 u - 6)\cdot (3)-(0)\cdot (0) \\ &=18 u - 18.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}18 u - 18 &>0 \\ u > 1\end{aligned}
$$

Notice that the equation

$$
u = 1
$$

defines a vertical line.

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-c9db071323b90cf34003.png)

## Generated authored easy

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}u + 2 \\ 3 \left(v - 2\right)^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e33a7b416045989e1f3b.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-a77f7c28407e8d087e49.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2e2049a43410a26f0512.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2e1fed097209149c8460.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ea4e26c4d04ec1eb3c1d.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}u + 2 \\ 3 \left(v - 2\right)^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} &=\begin{vmatrix}1 & 0 \\ 0 & 6 v - 12\end{vmatrix} \\ &=(1)\cdot (6 v - 12)-(0)\cdot (0) \\ &=6 v - 12.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}6 v - 12 &>0 \\ v > 2\end{aligned}
$$

Notice that the equation

$$
v = 2
$$

defines a horizontal line.

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-e33a7b416045989e1f3b.png)

## Generated authored easy

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3 u - 3 \\ 3 \left(v - 2\right)^{2}\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-d076a5f02051d561d6c9.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-9af37e1d161768010bd0.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-9fa993332b42da9cf5fd.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4d2957abd621c9899134.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-5f8f001c13df2fc8b9d8.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3 u - 3 \\ 3 \left(v - 2\right)^{2}\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} &=\begin{vmatrix}3 & 0 \\ 0 & 6 v - 12\end{vmatrix} \\ &=(3)\cdot (6 v - 12)-(0)\cdot (0) \\ &=18 v - 36.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}18 v - 36 &>0 \\ v > 2\end{aligned}
$$

Notice that the equation

$$
v = 2
$$

defines a horizontal line.

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4d2957abd621c9899134.png)

## Generated authored hard

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3 v + \left(u + 2\right)^{2} - 6 \\ - u - \left(v - 2\right)^{2} - 2\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-9b09f7ef79dafffb852c.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-6b5ee05fccbebe5631d3.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ccbc8b7227c0cef49948.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-b9d4c9f06a88808ceb1b.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-210b51bace244ff29caa.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3 v + \left(u + 2\right)^{2} - 6 \\ - u - \left(v - 2\right)^{2} - 2\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} &=\begin{vmatrix}2 u + 4 & 3 \\ -1 & 4 - 2 v\end{vmatrix} \\ &=(2 u + 4)\cdot (4 - 2 v)-(3)\cdot (-1) \\ &=- 4 u v + 8 u - 8 v + 19.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}- 4 u v + 8 u - 8 v + 19 &>0 \\ \left(u + 2\right) \left(v - 2\right) < \frac{3}{4}\end{aligned}
$$

This gives the solution $v < 2 + \frac{3}{4 \left(u + 2\right)}$ for $u>-2$ and $v > 2 + \frac{3}{4 \left(u + 2\right)}$ for $u<-2.$ At $u=-2,$ the Jacobian is positive, so this line belongs to the required region.

Notice that the equation

$$
v = 2 + \frac{3}{4 \left(u + 2\right)}
$$

defines a hyperbola.

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-9b09f7ef79dafffb852c.png)

## Generated authored hard

Which of the following shows the region in the $uv$-plane where the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}2 v + \left(u - 1\right)^{2} - 4 \\ - u - \left(v - 2\right)^{2} + 1\end{aligned}],
$$

is (locally) orientation-preserving?

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-4390cfb0897ae8dc4afd.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-2362d21944af09512c0f.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-0ebca27a59cf7a57ccbc.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-ebf89e0d09da31f89a5f.png)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7c8c19da63af34f6f7eb.png)

Worked solution:

Recall that a transformation is (locally) orientation-preserving at the points where the Jacobian determinant is positive:

$$
\frac{∂(x,y)}{∂(u,v)}>0
$$

We have

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}2 v + \left(u - 1\right)^{2} - 4 \\ - u - \left(v - 2\right)^{2} + 1\end{aligned}].
$$

Computing the corresponding Jacobian determinant, we obtain

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} &=\begin{vmatrix}2 u - 2 & 2 \\ -1 & 4 - 2 v\end{vmatrix} \\ &=(2 u - 2)\cdot (4 - 2 v)-(2)\cdot (-1) \\ &=- 4 u v + 8 u + 4 v - 6.\end{aligned}
$$

To find the required regions, we solve the following inequality:

$$
\begin{aligned}- 4 u v + 8 u + 4 v - 6 &>0 \\ \left(u - 1\right) \left(v - 2\right) < \frac{1}{2}\end{aligned}
$$

This gives the solution $v < 2 + \frac{1}{2 \left(u - 1\right)}$ for $u>1$ and $v > 2 + \frac{1}{2 \left(u - 1\right)}$ for $u<1.$ At $u=1,$ the Jacobian is positive, so this line belongs to the required region.

Notice that the equation

$$
v = 2 + \frac{1}{2 \left(u - 1\right)}
$$

defines a hyperbola.

Therefore, the region where the transformation is (locally) orientation-preserving must be the following:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129283/plots/plot-7c8c19da63af34f6f7eb.png)
