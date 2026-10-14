# Current source and template extraction

Basis 2267. All source choices, response contracts, and operative stages are preserved below. Historical details are retained in reference/legacy-basis-1356/template-extraction.md.

## q-36219 / 491a90b9-f33c-5937-8491-8e8447d7cf82

Moderate, radio `selection`, five choices, plot rating none. Point: `['1', '2', '4']`; fixed plane: `x`; supplied partial: `\frac{3x+y}{\sqrt{6xy+{y}^{2}}}`; exact slope: `5/4`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=1.$ Given that the point $P(1,2,4)$ lies on $C$, and that ${f}_{y}=\frac{3x+y}{\sqrt{6xy+{y}^{2}}}$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=1.$ Hence, the slope of the tangent to the curve at the point $P(1,2,4)$ will be given by the partial derivative $\frac{∂z}{∂y}{|}_{(1,2)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂y}$ at $(1,2):$

$$
\begin{aligned}{f}_{y}(1,2) & =\frac{3(1)+(2)}{\sqrt{6(1)(2)+(2)^{2}}} \\  & =\frac{5}{\sqrt{16}} \\  & =\frac{5}{4}\end{aligned}
$$

 

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(1,2)} & =\frac{∂z}{∂y}{|}_{(1,2)}(y-2) \\ z-4 & =\frac{5}{4}(y-2) \\ z & =\frac{5}{4}y+\frac{3}{2}\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(1,2,4)$ can be given as the intersection of two planes, as follows:

$$
{\begin{aligned}x=1 \\ z=\frac{5}{4}y+\frac{3}{2}\end{aligned}
$$

Complete observed bank, profile `raw_q-36219`:

- `{\begin{aligned}x=1 \\ z=\frac{4}{5}y-\frac{3}{2}\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=1 \\ z=\frac{5}{4}y+\frac{3}{2}\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=1 \\ z=-\frac{5}{4}y+\frac{2}{3}\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=2 \\ z=-\frac{5}{4}y+\frac{3}{2}\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=1 \\ z=\frac{5}{2}y-\frac{3}{2}\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-36369 / faf15e19-a012-50bb-842f-791131393cd4

Moderate, radio `selection`, five choices, plot rating none. Point: `['1', '1', '0']`; fixed plane: `y`; supplied partial: `3x+6x\operatorname{ln}⁡(xy)`; exact slope: `3`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=1.$ Given that the point $P(1,1,0)$ lies on $C$, and that ${f}_{x}=3x+6x\operatorname{ln}⁡(xy)$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=1.$ Hence, the slope of the tangent to the curve at the point $P(1,1,0)$ will be given by the partial derivative $\frac{∂z}{∂x}{|}_{(1,1)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂x}$ at $(1,1):$

$$
\begin{aligned}\frac{∂z}{∂x}{|}_{(1,1)} & =3(1)+6(1)\operatorname{ln}⁡(1\cdot 1) \\  & =3+6\operatorname{ln}⁡1 \\  & =3\end{aligned}
$$

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(1,1)} & =\frac{∂z}{∂x}{|}_{(1,1)}(x-1) \\ z-0 & =3(x-1) \\ z & =3x-3\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(1,1,0)$ can be given as the intersection of two planes, as follows:

$$
\{\begin{aligned}y=1 \\ z=3x-3\end{aligned}
$$

Complete observed bank, profile `raw_q-36369`:

- `\{\begin{aligned}y=1 \\ z=2-2x\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=1 \\ z=3x\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=1 \\ z=3x-3\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=1 \\ z=2x-2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=1, \\ z=4x-4\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-132585 / 484f8b36-97b4-5e4f-a875-d05f61c48bf6

Moderate, radio `selection`, five choices, plot rating none. Point: `['4', '-2', '5']`; fixed plane: `y`; supplied partial: `y\sqrt{x}`; exact slope: `-4`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=-2.$ Given that the point $P(4,-2,5)$ lies on $C$, and that ${f}_{x}=y\sqrt{x}$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-2.$ Hence, the slope of the tangent to the curve at the point $P(4,-2,5)$ will be given by the partial derivative $\frac{∂z}{∂x}{|}_{(4,-2)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂x}$ at $(4,-2):$

$$
\begin{aligned}\frac{∂z}{∂x}{|}_{(4,-2)} & =(-2)\sqrt{4} \\  & =-2(2) \\  & =-4\end{aligned}
$$

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(4,-2)} & =\frac{∂z}{∂x}{|}_{(4,-2)}(x-4) \\ z-5 & =-4(x-4) \\ z & =-4x+21\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(4,-2,5)$ can be given as the intersection of two planes, as follows:

$$
{\begin{aligned}y=-2 \\ z=-4x+21\end{aligned}
$$

Complete observed bank, profile `raw_q-132585`:

- `{\begin{aligned}y=-2 \\ z=-4x+9\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=-2 \\ z=-4x+21\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=-2 \\ z=2x+9\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=-2 \\ z=-2x+15\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=-2 \\ z=2x+21\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-132587 / 1c434702-618c-5a71-8a4a-aadc6bd7fee6

Moderate, radio `selection`, five choices, plot rating none. Point: `['1', '2', '1']`; fixed plane: `y`; supplied partial: `2xy+2`; exact slope: `6`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=2.$ Given that the point $P(1,2,1)$ lies on $C$, and that ${f}_{x}=2xy+2$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve at the point $P(1,2,1)$ will be given by the partial derivative $\frac{∂z}{∂x}{|}_{(1,2)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂x}$ at $(1,2):$

$$
\begin{aligned}\frac{∂z}{∂x}{|}_{(1,2)} & =2(1)(2)+2 \\  & =4+2 \\  & =6\end{aligned}
$$

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(1,2)} & =\frac{∂z}{∂x}{|}_{(1,2)}(x-1) \\ z-1 & =6(x-1) \\ z & =6x-5\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(1,2,1)$ can be given as the intersection of two planes, as follows:

$$
{\begin{aligned}y=2 \\ z=6x-5\end{aligned}
$$

Complete observed bank, profile `raw_q-132587`:

- `{\begin{aligned}y=2 \\ z=6x-5\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=3x-2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=6x+3\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=3x-5\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=4x+3\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-132589 / 5c5dd738-1c94-548e-aa53-3b5d32dc4abc

Moderate, radio `selection`, five choices, plot rating none. Point: `['e', '2', '3']`; fixed plane: `x`; supplied partial: `2\operatorname{ln}⁡x-\frac{{e}^{y}}{{x}^{2}}`; exact slope: `1`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=e.$ Given that the point $P(e,2,3)$ lies on $C$, and that ${f}_{y}=2\operatorname{ln}⁡x-\frac{{e}^{y}}{{x}^{2}}$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=e.$ Hence, the slope of the tangent to the curve at the point $P(e,2,3)$ will be given by the partial derivative $\frac{∂z}{∂y}{|}_{(e,2)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂y}$ at $(e,2):$

$$
\begin{aligned}{f}_{y}(e,2) & =2\operatorname{ln}⁡e-\frac{{e}^{2}}{{e}^{2}} \\  & =2-1 \\  & =1\end{aligned}
$$

 

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(e,2)} & =\frac{∂z}{∂y}{|}_{(e,2)}(y-2) \\ z-3 & =1(y-2) \\ z & =y+1\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(e,2,3)$ can be given as the intersection of two planes, as follows:

$$
\{\begin{aligned}x=e \\ z=y+1\end{aligned}
$$

Complete observed bank, profile `raw_q-132589`:

- `\{\begin{aligned}x=e \\ z=2y-3\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=e \\ z=y+3\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=e \\ z=2y-1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=e \\ z=y-2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=e \\ z=y+1\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-132590 / 90718d28-70a4-5587-a36e-fa57ec8d26d4

Moderate, radio `selection`, five choices, plot rating none. Point: `['-\\frac{\\pi }{2}', '2', '2\\pi ']`; fixed plane: `y`; supplied partial: `\operatorname{sin}⁡x+\frac{xy}{\pi }`; exact slope: `-2`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=2.$ Given that the point $P(-\frac{\pi }{2},2,2\pi )$ lies on $C$, and that ${f}_{x}=\operatorname{sin}⁡x+\frac{xy}{\pi }$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve at the point $P(-\frac{\pi }{2},2,2\pi )$ will be given by the partial derivative $\frac{∂z}{∂x}{|}_{(-\pi /2,2)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂x}$ at $(-\frac{\pi }{2},2):$

$$
\begin{aligned}\frac{∂z}{∂x}{|}_{(-\pi /2,2)} & =\operatorname{sin}⁡(-\frac{\pi }{2})+\frac{(-\frac{\pi }{2})(2)}{\pi } \\  & =-1-1 \\  & =-2\end{aligned}
$$

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(-\pi /2,2)} & =\frac{∂z}{∂x}{|}_{(-\pi /2,2)}(x-(-\frac{\pi }{2})) \\ z-2\pi  & =-2(x+\frac{\pi }{2}) \\ z & =-2x+\pi \end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(-\frac{\pi }{2},2,2\pi )$ can be given as the intersection of two planes, as follows:

$$
{\begin{aligned}y=2 \\ z=-2x+\pi \end{aligned}
$$

Complete observed bank, profile `raw_q-132590`:

- `{\begin{aligned}y=2 \\ z=x+2\pi \end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=2x-2\pi \end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=-2x+\pi \end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=x-\pi \end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=-2x-\frac{\pi }{2}\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-132593 / 22a41e65-3d40-52de-a0eb-a4c7353c0c15

Moderate, radio `selection`, five choices, plot rating none. Point: `['2', '\\frac{\\pi }{4}', '0']`; fixed plane: `x`; supplied partial: `4\operatorname{sin}⁡(xy)`; exact slope: `4`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=2.$ Given that the point $P(2,\frac{\pi }{4},0)$ lies on $C$, and that ${f}_{y}=4\operatorname{sin}⁡(xy)$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=2.$ Hence, the slope of the tangent to the curve at the point $P(2,\frac{\pi }{4},0)$ will be given by the partial derivative $\frac{∂z}{∂y}{|}_{(2,\pi /4)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂y}$ at $(2,\frac{\pi }{4}):$

$$
\begin{aligned}{f}_{y}(2,\frac{\pi }{4}) & =4\cdot \operatorname{sin}⁡(2\cdot \frac{\pi }{4}) \\  & =4\operatorname{sin}⁡(\frac{\pi }{2}) \\  & =4\cdot 1 \\  & =4\end{aligned}
$$

 

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(2,\pi /4)} & =\frac{∂z}{∂y}{|}_{(2,\pi /4)}(y-\frac{\pi }{4}) \\ z-0 & =4(y-\frac{\pi }{4}) \\ z & =4y-\pi \end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(2,\frac{\pi }{4},0)$ can be given as the intersection of two planes, as follows:

$$
\{\begin{aligned}x=2 \\ z=4y-\pi \end{aligned}
$$

Complete observed bank, profile `raw_q-132593`:

- `\{\begin{aligned}x=2 \\ z=4y-\pi \end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=2 \\ z=2y-\frac{\pi }{2}\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=2 \\ z=2y+\pi \end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=2 \\ z=4y-\frac{\pi }{2}\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=2 \\ z=4y\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-132595 / ac300975-45c9-5a2c-a8b5-5d2addf48a83

Moderate, radio `selection`, five choices, plot rating none. Point: `['\\sqrt{2}', '2', '\\frac{1}{2}']`; fixed plane: `x`; supplied partial: `-\frac{2{x}^{2}+y}{{y}^{3}}`; exact slope: `-3/4`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=\sqrt{2}.$ Given that the point $P(\sqrt{2},2,\frac{1}{2})$ lies on $C$, and that ${f}_{y}=-\frac{2{x}^{2}+y}{{y}^{3}}$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=\sqrt{2}.$ Hence, the slope of the tangent to the curve at the point $P(\sqrt{2},2,\frac{1}{2})$ will be given by the partial derivative $\frac{∂z}{∂y}{|}_{(\sqrt{2},2)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂y}$ at $(\sqrt{2},2):$

$$
\begin{aligned}{f}_{y}(\sqrt{2},2) & =-\frac{2(\sqrt{2})^{2}+2}{{2}^{3}} \\  & =-\frac{4+2}{8} \\  & =-\frac{3}{4}\end{aligned}
$$

 

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(\sqrt{2},2)} & =\frac{∂z}{∂y}{|}_{(\sqrt{2},2)}(y-2) \\ z-\frac{1}{2} & =-\frac{3}{4}(y-2) \\ z & =-\frac{3}{4}y+2\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(\sqrt{2},2,\frac{1}{2})$ can be given as the intersection of two planes, as follows:

$$
\{\begin{aligned}x=\sqrt{2} \\ z=-\frac{3}{4}y+2\end{aligned}
$$

Complete observed bank, profile `raw_q-132595`:

- `\{\begin{aligned}x=\sqrt{2} \\ z=\frac{3}{2}y-1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=\sqrt{2} \\ z=-\frac{3}{4}y+2\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=\sqrt{2} \\ z=-\frac{1}{4}y-2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=\sqrt{2} \\ z=\frac{1}{2}y+2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=\sqrt{2} \\ z=-\frac{3}{2}y+1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-36301 / daecb367-4754-591f-93db-eaa083b20ffe

Moderate, radio `selection`, five choices, plot rating none. Point: `['-2', '0', '8']`; fixed plane: `x`; supplied partial: `x\operatorname{cos}⁡y+4y+x`; exact slope: `-4`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=-2.$ Given that the point $P(-2,0,8)$ lies on $C$, and that ${f}_{y}=x\operatorname{cos}⁡y+4y+x$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=-2.$ Hence, the slope of the tangent to the curve at the point $P(-2,0,8)$ will be given by the partial derivative $\frac{∂z}{∂y}{|}_{(-2,0)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂y}$ at $(-2,0):$

$$
\begin{aligned}\frac{∂z}{∂y}{|}_{(-2,0)} & =(-2)\operatorname{cos}⁡0+4(0)+(-2) \\  & =-2-2 \\  & =-4\end{aligned}
$$

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(-2,0)} & =\frac{∂z}{∂y}{|}_{(-2,0)}(y-0) \\ z-8 & =-4(y-0) \\ z & =-4y+8\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(-2,0,8)$ can be given as the intersection of two planes, as follows:

$$
{\begin{aligned}x=-2 \\ z=-4y+8\end{aligned}
$$

Complete observed bank, profile `raw_q-36301`:

- `{\begin{aligned}x=-2 \\ z=4y+8\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=-2 \\ z=-4x\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=-2 \\ z=-4y+8\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=-2 \\ z=4x+8\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=-2 \\ z=4y-8\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-36441 / 12d0b28e-9c11-5054-bcb2-feb86bd6fc4d

Moderate, radio `selection`, five choices, plot rating none. Point: `['0.5', '2', '4']`; fixed plane: `x`; supplied partial: `y+2y\operatorname{ln}⁡(xy)+\frac{1}{x}`; exact slope: `4`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=0.5.$ Given that the point $P(0.5,2,4)$ lies on $C$, and that ${f}_{y}=y+2y\operatorname{ln}⁡(xy)+\frac{1}{x}$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=0.5.$ Hence, the slope of the tangent to the curve at the point $P(0.5,2,4)$ will be given by the partial derivative $\frac{∂z}{∂y}{|}_{(0.5,2)}.$ 

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂y}$ at $(0.5,2):$

$$
\begin{aligned}\frac{∂z}{∂y}{|}_{(0.5,2)} & =2+2(2)\operatorname{ln}⁡((0.5)(2))+\frac{1}{0.5} \\  & =2+4\operatorname{ln}⁡1+2 \\  & =4\end{aligned}
$$

Now, we use the point-slope form of a straight line: 

$$
\begin{aligned}z-z{|}_{(0.5,2)} & =\frac{∂z}{∂y}{|}_{(0.5,2)}(y-2) \\ z-4 & =4(y-2) \\ z & =4y-4\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(0.5,2,4)$ can be given as the intersection of two planes, as follows:

$$
{\begin{aligned}x=0.5 \\ z=4y-4\end{aligned}
$$

Complete observed bank, profile `raw_q-36441`:

- `{\begin{aligned}x=0.5 \\ z=4x+2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=2 \\ z=4x+2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=0.5 \\ z=4y-12\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=0.5 \\ z=-4y+12\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=0.5 \\ z=4y-4\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-71209 / 3868b943-72a6-5a73-9952-d94521bce0ce

Moderate, radio `selection`, five choices, plot rating none. Point: `['-2', '2', '1']`; fixed plane: `x`; supplied partial: `{x}^{2}y+2x-y`; exact slope: `2`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=-2.$ Given that the point $P(-2,2,1)$ lies on $C$, and that ${f}_{y}={x}^{2}y+2x-y$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=-2.$ Hence, the slope of the tangent to the curve at the point $P(-2,2,1)$ will be given by the partial derivative $\frac{∂z}{∂y}{|}_{(-2,2)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂y}$ at $(-2,2):$

$$
\begin{aligned}{f}_{y}(-2,2) & =(-2)^{2}(2)+2(-2)-(2) \\  & =8-4-2 \\  & =2\end{aligned}
$$

 

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(-2,2)} & =\frac{∂z}{∂y}{|}_{(-2,2)}(y-2) \\ z-1 & =2(y-2) \\ z & =2y-3\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(-2,2,1)$ can be given as the intersection of two planes, as follows:

$$
\{\begin{aligned}x=-2 \\ z=2y-3\end{aligned}
$$

Complete observed bank, profile `raw_q-71209`:

- `\{\begin{aligned}x=-2 \\ z=6y-3\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=-2 \\ z=4y-5\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=-2 \\ z=2y-3\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=-2 \\ z=4y-3\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=-2 \\ z=2y-5\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-71218 / ceda561f-8269-5197-b05a-efc41af9a9a2

Moderate, radio `selection`, five choices, plot rating none. Point: `['0', '1', '2']`; fixed plane: `y`; supplied partial: `{x}^{2}+{y}^{2}-\operatorname{ln}⁡(x+y)`; exact slope: `1`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=1.$ Given that the point $P(0,1,2)$ lies on $C$, and that ${f}_{x}={x}^{2}+{y}^{2}-\operatorname{ln}⁡(x+y)$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=1.$ Hence, the slope of the tangent to the curve at the point $P(0,1,2)$ will be given by the partial derivative $\frac{∂z}{∂x}{|}_{(0,1)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂x}$ at $(0,1):$

$$
\begin{aligned}\frac{∂z}{∂x}{|}_{(0,1)} & =(0)^{2}+(1)^{2}-\operatorname{ln}⁡(0+1) \\  & =1-\operatorname{ln}⁡1 \\  & =1-0 \\  & =1\end{aligned}
$$

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(0,1)} & =\frac{∂z}{∂x}{|}_{(0,1)}(x-0) \\ z-2 & =1(x) \\ z & =x+2\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(0,1,2)$ can be given as the intersection of two planes, as follows:

$$
{\begin{aligned}y=1 \\ z=x+2\end{aligned}
$$

Complete observed bank, profile `raw_q-71218`:

- `{\begin{aligned}y=1 \\ z=x-2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=1 \\ z=x+2\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=1 \\ z=2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=1 \\ z=-x+2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}y=1 \\ z=-2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-36372 / 376329be-a379-553e-b714-516f831f127f

Moderate, radio `selection`, five choices, plot rating none. Point: `['2', '0', '4']`; fixed plane: `y`; supplied partial: `{e}^{y}+2x\operatorname{cos}⁡y`; exact slope: `5`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=0.$ Given that the point $P(2,0,4)$ lies on $C$, and that ${f}_{x}={e}^{y}+2x\operatorname{cos}⁡y$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=0.$ Hence, the slope of the tangent to the curve at the point $P(2,0,4)$ will be given by the partial derivative $\frac{∂z}{∂x}{|}_{(2,0)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂x}$ at $(2,0):$

$$
\begin{aligned}{f}_{x}(2,0) & ={e}^{(0)}+2(2)\operatorname{cos}⁡(0) \\  & =1+4 \\  & =5\end{aligned}
$$

 

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(2,0)} & =\frac{∂z}{∂x}{|}_{(2,0)}(x-2) \\ z-4 & =5(x-2) \\ z & =5x-6\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(2,0,4)$ can be given as the intersection of two planes, as follows:

$$
\{\begin{aligned}y=0 \\ z=5x-6\end{aligned}
$$

Complete observed bank, profile `raw_q-36372`:

- `\{\begin{aligned}x=2 \\ z=5y+4\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=0 \\ z=5x-14\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=0 \\ z=5x+6\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}x=2 \\ z=-5x-6\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=0 \\ z=5x-6\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-71216 / 05b78370-0b37-5800-aa28-6b6b17964b90

Moderate, radio `selection`, five choices, plot rating none. Point: `['1', '0', '-1']`; fixed plane: `x`; supplied partial: `x{e}^{xy}-2\operatorname{cos}⁡y`; exact slope: `-1`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $x=1.$ Given that the point $P(1,0,-1)$ lies on $C$, and that ${f}_{y}=x{e}^{xy}-2\operatorname{cos}⁡y$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=1.$ Hence, the slope of the tangent to the curve at the point $P(1,0,-1)$ will be given by the partial derivative $\frac{∂z}{∂y}{|}_{(1,0)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂y}$ at $(1,0):$

$$
\begin{aligned}{f}_{y}(1,0) & =1\cdot {e}^{1\cdot 0}-2\operatorname{cos}⁡0 \\  & =1\cdot 1-2\cdot 1 \\  & =-1\end{aligned}
$$

 

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(1,0)} & =\frac{∂z}{∂y}{|}_{(1,0)}(y-0) \\ z-(-1) & =(-1)y \\ z & =-y-1\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(1,0,-1)$ can be given as the intersection of two planes, as follows:

$$
{\begin{aligned}x=1 \\ z=-y-1\end{aligned}
$$

Complete observed bank, profile `raw_q-71216`:

- `{\begin{aligned}x=1 \\ z=-y+1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=1 \\ z=-2y-1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=1 \\ z=y-1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=1 \\ z=-2y+1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `{\begin{aligned}x=1 \\ z=-y-1\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-71204 / ac629eca-77ed-5bb7-99e7-49845bdc5d9a

Moderate, radio `selection`, five choices, plot rating none. Point: `['\\frac{1}{2}', '0', '1']`; fixed plane: `y`; supplied partial: `(y+1)\operatorname{cos}⁡(\pi x)+2x\operatorname{cos}⁡(\pi y)\operatorname{sin}⁡(\pi x)`; exact slope: `1`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=0.$ Given that the point $P(\frac{1}{2},0,1)$ lies on $C$, and that ${f}_{x}=(y+1)\operatorname{cos}⁡(\pi x)+2x\operatorname{cos}⁡(\pi y)\operatorname{sin}⁡(\pi x)$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=0.$ Hence, the slope of the tangent to the curve at the point $P(\frac{1}{2},0,1)$ will be given by the partial derivative $\frac{∂z}{∂x}{|}_{(\frac{1}{2},0)}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂x}$ at $(\frac{1}{2},0)\,:$

$$
\begin{aligned}\frac{∂z}{∂x}{|}_{(\frac{1}{2},0)} & =(0+1)\operatorname{cos}⁡(\pi \cdot \frac{1}{2})+2\cdot \frac{1}{2}\cdot \operatorname{cos}⁡(\pi \cdot 0)\operatorname{sin}⁡(\pi \cdot \frac{1}{2}) \\  & =1\cdot 0+2\cdot \frac{1}{2}\cdot 1\cdot 1 \\  & =0+1 \\  & =1\end{aligned}
$$

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(\frac{1}{2},0)} & =\frac{∂z}{∂x}{|}_{(\frac{1}{2},0)}(x-\frac{1}{2}) \\ z-1 & =1(x-\frac{1}{2}) \\ z-1 & =x-\frac{1}{2} \\ z & =x+\frac{1}{2}\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(\frac{1}{2},0,1)$ can be given as the intersection of two planes, as follows:

$$
\{\begin{aligned}y=0 \\ z=x+\frac{1}{2}\end{aligned}
$$

Complete observed bank, profile `raw_q-71204`:

- `\{\begin{aligned}y=0 \\ z=2x\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=0 \\ z=2x+\frac{1}{2}\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=0 \\ z=x+\frac{1}{2}\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=0 \\ z=3x-2\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=0 \\ z=2x+1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

## q-132594 / ae3534f1-44d3-55be-bcdb-7634e16c97c5

Moderate, radio `selection`, five choices, plot rating none. Point: `['\\frac{1}{2}', '\\pi ', '1']`; fixed plane: `y`; supplied partial: `2x{e}^{\operatorname{cos}⁡(xy)}+\operatorname{sin}⁡(xy)`; exact slope: `2`.

The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $y=\pi .$ Given that the point $P(\frac{1}{2},\pi ,1)$ lies on $C$, and that ${f}_{x}=2x{e}^{\operatorname{cos}⁡(xy)}+\operatorname{sin}⁡(xy)$, find the equations of the tangent line to $C$ at $P.$

Source worked solution:

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=\pi .$ Hence, the slope of the tangent to the curve at the point $P(\frac{1}{2},\pi ,1)$ will be given by the partial derivative $\frac{∂z}{∂x}{|}_{(1/2,\pi )}.$

To get the slope, we evaluate the partial derivative $\frac{∂z}{∂x}$ at $(\frac{1}{2},\pi ):$

$$
\begin{aligned}\frac{∂z}{∂x}{|}_{(1/2,\pi )} & =2(\frac{1}{2}){e}^{\operatorname{cos}⁡(\pi /2)}+\operatorname{sin}⁡(\frac{\pi }{2}) \\  & ={e}^{0}+1 \\  & =2\end{aligned}
$$

Now, we use the point-slope form of a straight line:

$$
\begin{aligned}z-z{|}_{(1/2,\pi )} & =\frac{∂z}{∂x}{|}_{(1/2,\pi )}(x-\frac{1}{2}) \\ z-1 & =2(x-\frac{1}{2}) \\ z & =2x\end{aligned}
$$

Finally, the tangent line to the curve $C$ at $P(\frac{1}{2},\pi ,1)$ can be given as the intersection of two planes, as follows:

$$
\{\begin{aligned}y=\pi  \\ z=2x\end{aligned}
$$

Complete observed bank, profile `raw_q-132594`:

- `\{\begin{aligned}y=\pi  \\ z=3x+1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=\pi  \\ z=x-1\end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=\pi  \\ z=x-\pi \end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=\pi  \\ z=2x+\pi \end{aligned}`. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.

- `\{\begin{aligned}y=\pi  \\ z=2x\end{aligned}` — correct. Recipe: preserve the fixed-plane row; transform the entire z right-hand side E to `c(E-h_source)+h_new`. This reproduces the complete source value at `c=1, h_new=h_source`.


## Backbone and parameter slots

Supplied surface notation z=f(x,y), supplied one partial derivative, a point P(a,b,h), and a fixed-coordinate plane. Evaluate the supplied partial at (a,b); use its value m in z-h=m(u-u0); rearrange to an affine z equation; pair it with the unchanged fixed-coordinate plane. The answer is one whole two-plane relation, never a vector or one equation fragment. Each source preserves its full derivative-stage count and interior expressions. q-71204's extra simplification equality remains an extra equality.

Observed source coordinates and partials are replay anchors. Moderate normal generalization replaces the supplied derivative D with cD, c in {-3,-2,-1,1,2,3}; each evaluation stage is c times the original stage; sampled heights are nonzero integers -12 through 12. Explicit same-method heights also permit half-integers and pi multiples within the documented bounds. The point, all prose references, each point-slope left side, each point-slope right side, conclusion, correct answer, and every profile option depend on these parameters. Fixed xy coordinates preserve the source's perfect-square, logarithm, exponential, and familiar-angle arithmetic; moving them without family-specific guards is outside this conservative generator. Scale and altitude both change assessed arithmetic; seed and answer order do not.

Raw profiles transform every complete source option as recorded above. Distinct profiles are never pooled. Normal `authored_operations` is separately labeled: correct m(u-u0)+h; negated slope -m(u-u0)+h; erroneous offset m(u+u0)+h; omitted altitude m(u-u0); swapped fixed/variable coordinates with m(v-v0)+h. For zero u0, replace the coincident offset recipe with m u-h and retain the omitted-altitude recipe m u. Compare whole affine row spaces and reject any bank with equivalent options, including accidental correct distractors.

Easy: a,b,k are signed nonzero integers of magnitude at most 4 and h is a nonzero integer of magnitude at most 12. Supplied partial is kx and fixed plane is y=b. Hard: a is a signed nonzero integer of magnitude at most 4, k is a signed nonzero integer of magnitude at most 3, h is a nonzero integer of magnitude at most 12, fixed y=k pi, supplied partial y cos(xy)+cos(y). Slope is k pi (-1)^(a k)+(-1)^k. Easy and hard retain constant workloads within their own band.

Every generated answer is delimiter-free mathematical content with a field-owned identity. UUIDs depend on rendered content; mathematical duplicate checking independently ignores seed, choice order, bank profile, identity, prose, and difficulty. The original canonical task is included in exclusion checks. No images or distractor feedback are introduced.
