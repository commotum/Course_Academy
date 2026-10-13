# Second-order direct-integration review

Raw originals and public generated replays preserve their attribute presence. Completed examples normalize presentation and remove legacy duplicate fields. Authored E/M/H variants are separate. No database writes.

## Easy — q-50139 — Original / exact parameter replay

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=-10.$

Field 1 (selection)
- $y = Cx^{2} + 10x + D$
- $y =-5x^{2} + Cx + D$
- $y =-5x^{2} + Cx$
- $y = 5x^{2} + Cx + D$
- $y =-5x^{2} + D$
Field 2 (selection)
- $y=-5{x}^{2}+Cx+D$ **correct**
- $y=5{x}^{2}+Cx+D$
- $y=-5{x}^{2}+Cx$
- $y=-5{x}^{2}+D$
- $y=C{x}^{2}+10x+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =-10\int \,\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =-10x+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-10x+C)\text{d}x \\ y & =-10\cdot \frac{{x}^{2}}{2}+Cx+D \\  & =-5{x}^{2}+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-50139 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=-2\left(10\right).$

Field 1 (selection)
- $y= Cx^{2} +2\left( 10x \right)+ D$
- $y=-2\left(5x^{2} \right)+ Cx + D$
- $y=-2\left(5x^{2} \right)+ Cx$
- $y=2\left( 5x^{2} \right)+ Cx + D$
- $y=-2\left(5x^{2} \right)+ D$
Field 2 (selection)
- $y=-2\left(5{x}^{2}\right)+Cx+D$ **correct**
- $y=2\left(5{x}^{2}\right)+Cx+D$
- $y=-2\left(5{x}^{2}\right)+Cx$
- $y=-2\left(5{x}^{2}\right)+D$
- $y=C{x}^{2}+2\left(10x\right)+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =-2\left(10\int \,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =-2\left(10x\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-2\left(10x\right)+C)\text{d}x \\ y & =-2\left(10\cdot \frac{{x}^{2}}{2}\right)+Cx+D \\  & =-2\left(5{x}^{2}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-50139 — Generated completed profile at scale=1/2

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=-\frac{1}{2}\left(10\right).$

Field 1 (selection)
- $y=-\frac{1}{2}\left(5{x}^{2}\right)+Cx+D$ **correct**
- $y=-\frac{1}{2}\left(5{x}^{2}\right)+D$
- $y=C{x}^{2}+\frac{1}{2}\left(10x\right)+D$
- $y=-\frac{1}{2}\left(5{x}^{2}\right)+Cx$
- $y=\frac{1}{2}\left(5{x}^{2}\right)+Cx+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =-\frac{1}{2}\left(10\int \,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =-\frac{1}{2}\left(10x\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-\frac{1}{2}\left(10x\right)+C)\text{d}x \\ y & =-\frac{1}{2}\left(10\cdot \frac{{x}^{2}}{2}\right)+Cx+D \\  & =-\frac{1}{2}\left(5{x}^{2}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-50148 — Original / exact parameter replay

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-{e}^{3x}=0.
$$

Field 1 (selection)
- $y = \frac{1}{9}e^{3x} + Cx^{2} + D$
- $y = \frac{1}{9}e^{3x} + Cx + D$
- $y = \frac{1}{3}e^{3x} + Cx + D$
- $y =-\frac{1}{3}e^{3x} + Cx + D$
- $y =-\frac{1}{9}e^{3x} + Cx^{2} + D$
Field 2 (selection)
- $y=-\frac{1}{3}{e}^{3x}+Cx+D$
- $y=\frac{1}{3}{e}^{3x}+Cx+D$
- $y=\frac{1}{9}{e}^{3x}+C{x}^{2}+D$
- $y=\frac{1}{9}{e}^{3x}+Cx+D$ **correct**
- $y=-\frac{1}{9}{e}^{3x}+C{x}^{2}+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}={e}^{3x}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int {e}^{3x}\,\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{3}{e}^{3x}+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{3}{e}^{3x}+C)\text{d}x \\ y & =\frac{1}{3}\int {e}^{3x}\,\text{d}x+C\int \text{d}x \\  & =\frac{1}{3}(\frac{1}{3}\,{e}^{3x})+Cx+D \\  & =\frac{1}{9}{e}^{3x}+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-50148 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-2\left({e}^{3x}\right)=2\left(0\right).
$$

Field 1 (selection)
- $y=2\left( \frac{1}{9}e^{3x} \right)+ Cx^{2} + D$
- $y=2\left( \frac{1}{9}e^{3x} \right)+ Cx + D$
- $y=2\left( \frac{1}{3}e^{3x} \right)+ Cx + D$
- $y=-2\left(\frac{1}{3}e^{3x} \right)+ Cx + D$
- $y=-2\left(\frac{1}{9}e^{3x} \right)+ Cx^{2} + D$
Field 2 (selection)
- $y=-2\left(\frac{1}{3}{e}^{3x}\right)+Cx+D$
- $y=2\left(\frac{1}{3}{e}^{3x}\right)+Cx+D$
- $y=2\left(\frac{1}{9}{e}^{3x}\right)+C{x}^{2}+D$
- $y=2\left(\frac{1}{9}{e}^{3x}\right)+Cx+D$ **correct**
- $y=-2\left(\frac{1}{9}{e}^{3x}\right)+C{x}^{2}+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left({e}^{3x}\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(\int {e}^{3x}\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(\frac{1}{3}{e}^{3x}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left(\frac{1}{3}{e}^{3x}\right)+C)\text{d}x \\ y & =2\left(\frac{1}{3}\int {e}^{3x}\,\text{d}x\right)+C\int \text{d}x \\  & =2\left(\frac{1}{3}(\frac{1}{3}\,{e}^{3x})\right)+Cx+D \\  & =2\left(\frac{1}{9}{e}^{3x}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-50148 — Generated completed profile at scale=1/2

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-\frac{1}{2}\left({e}^{3x}\right)=\frac{1}{2}\left(0\right).
$$

Field 1 (selection)
- $y=-\frac{1}{2}\left(\frac{1}{3}{e}^{3x}\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{1}{9}{e}^{3x}\right)+Cx+D$ **correct**
- $y=-\frac{1}{2}\left(\frac{1}{9}{e}^{3x}\right)+C{x}^{2}+D$
- $y=\frac{1}{2}\left(\frac{1}{9}{e}^{3x}\right)+C{x}^{2}+D$
- $y=\frac{1}{2}\left(\frac{1}{3}{e}^{3x}\right)+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left({e}^{3x}\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(\int {e}^{3x}\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(\frac{1}{3}{e}^{3x}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left(\frac{1}{3}{e}^{3x}\right)+C)\text{d}x \\ y & =\frac{1}{2}\left(\frac{1}{3}\int {e}^{3x}\,\text{d}x\right)+C\int \text{d}x \\  & =\frac{1}{2}\left(\frac{1}{3}(\frac{1}{3}\,{e}^{3x})\right)+Cx+D \\  & =\frac{1}{2}\left(\frac{1}{9}{e}^{3x}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119038 — Original / exact parameter replay

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=8{e}^{-2x}.$

Field 1 (selection)
- $y=2{e}^{-2x}+Cx+D$ **correct**
- $y={e}^{-2x}+C{x}^{2}+Dx$
- $y=-4{e}^{-2x}+Cx+D$
- $y=-{e}^{-2x}+C{e}^{-x}+Dx$
- $y=2{e}^{-2x}+C{e}^{-x}+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =8\int {e}^{-2x}\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =8(-\frac{1}{2}{e}^{-2x})+C \\  & =-4{e}^{-2x}+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-4{e}^{-2x}+C)\text{d}x \\ y & =-4(-\frac{1}{2}{e}^{-2x})+Cx+D \\  & =2{e}^{-2x}+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119038 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(8{e}^{-2x}\right).$

Field 1 (selection)
- $y=2\left(2{e}^{-2x}\right)+Cx+D$ **correct**
- $y=2\left({e}^{-2x}\right)+C{x}^{2}+Dx$
- $y=-2\left(4{e}^{-2x}\right)+Cx+D$
- $y=-2\left({e}^{-2x}\right)+C{e}^{-x}+Dx$
- $y=2\left(2{e}^{-2x}\right)+C{e}^{-x}+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(8\int {e}^{-2x}\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(8(-\frac{1}{2}{e}^{-2x})\right)+C \\  & =-2\left(4{e}^{-2x}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-2\left(4{e}^{-2x}\right)+C)\text{d}x \\ y & =-2\left(4(-\frac{1}{2}{e}^{-2x})\right)+Cx+D \\  & =2\left(2{e}^{-2x}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119038 — Generated completed profile at scale=1/2

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(8{e}^{-2x}\right).$

Field 1 (selection)
- $y=\frac{1}{2}\left(2{e}^{-2x}\right)+Cx+D$ **correct**
- $y=\frac{1}{2}\left({e}^{-2x}\right)+C{x}^{2}+Dx$
- $y=-\frac{1}{2}\left(4{e}^{-2x}\right)+Cx+D$
- $y=-\frac{1}{2}\left({e}^{-2x}\right)+C{e}^{-x}+Dx$
- $y=\frac{1}{2}\left(2{e}^{-2x}\right)+C{e}^{-x}+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(8\int {e}^{-2x}\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(8(-\frac{1}{2}{e}^{-2x})\right)+C \\  & =-\frac{1}{2}\left(4{e}^{-2x}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-\frac{1}{2}\left(4{e}^{-2x}\right)+C)\text{d}x \\ y & =-\frac{1}{2}\left(4(-\frac{1}{2}{e}^{-2x})\right)+Cx+D \\  & =\frac{1}{2}\left(2{e}^{-2x}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119041 — Original / exact parameter replay

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=-8\operatorname{sin}⁡2x.$

Field 1 (selection)
- $y=-\operatorname{cos}⁡2x+C{x}^{2}+D$
- $y=\operatorname{sin}⁡2x+Cx+D$
- $y=-2\operatorname{sin}⁡2x+C{x}^{2}+D$
- $y=2\operatorname{sin}⁡2x+Cx+D$ **correct**
- $y=2\operatorname{cos}⁡2x+Cx+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =-8\int \operatorname{sin}⁡2x\,\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =-8(-\frac{1}{2}\operatorname{cos}⁡2x) \\  & =4\operatorname{cos}⁡2x+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (4\operatorname{cos}⁡2x+C)\text{d}x \\ y & =4\int \operatorname{cos}⁡2x\,\text{d}x+C\int \text{d}x \\  & =4(\frac{1}{2}\operatorname{sin}⁡2x)+Cx+D \\  & =2\operatorname{sin}⁡2x+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119041 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=-2\left(8\operatorname{sin}⁡2x\right).$

Field 1 (selection)
- $y=-2\left(\operatorname{cos}⁡2x\right)+C{x}^{2}+D$
- $y=2\left(\operatorname{sin}⁡2x\right)+Cx+D$
- $y=-2\left(2\operatorname{sin}⁡2x\right)+C{x}^{2}+D$
- $y=2\left(2\operatorname{sin}⁡2x\right)+Cx+D$ **correct**
- $y=2\left(2\operatorname{cos}⁡2x\right)+Cx+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =-2\left(8\int \operatorname{sin}⁡2x\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =-2\left(8(-\frac{1}{2}\operatorname{cos}⁡2x)\right) \\  & =2\left(4\operatorname{cos}⁡2x\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left(4\operatorname{cos}⁡2x\right)+C)\text{d}x \\ y & =2\left(4\int \operatorname{cos}⁡2x\,\text{d}x\right)+C\int \text{d}x \\  & =2\left(4(\frac{1}{2}\operatorname{sin}⁡2x)\right)+Cx+D \\  & =2\left(2\operatorname{sin}⁡2x\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119041 — Generated completed profile at scale=1/2

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=-\frac{1}{2}\left(8\operatorname{sin}⁡2x\right).$

Field 1 (selection)
- $y=-\frac{1}{2}\left(\operatorname{cos}⁡2x\right)+C{x}^{2}+D$
- $y=\frac{1}{2}\left(\operatorname{sin}⁡2x\right)+Cx+D$
- $y=-\frac{1}{2}\left(2\operatorname{sin}⁡2x\right)+C{x}^{2}+D$
- $y=\frac{1}{2}\left(2\operatorname{sin}⁡2x\right)+Cx+D$ **correct**
- $y=\frac{1}{2}\left(2\operatorname{cos}⁡2x\right)+Cx+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =-\frac{1}{2}\left(8\int \operatorname{sin}⁡2x\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =-\frac{1}{2}\left(8(-\frac{1}{2}\operatorname{cos}⁡2x)\right)+C  \\  & =\frac{1}{2}\left(4\operatorname{cos}⁡2x\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left(4\operatorname{cos}⁡2x\right)+C)\text{d}x \\ y & =\frac{1}{2}\left(4\int \operatorname{cos}⁡2x\,\text{d}x\right)+C\int \text{d}x \\  & =\frac{1}{2}\left(4(\frac{1}{2}\operatorname{sin}⁡2x)\right)+Cx+D \\  & =\frac{1}{2}\left(2\operatorname{sin}⁡2x\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119042 — Original / exact parameter replay

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+6x=8{e}^{x/2}.
$$

Field 1 (selection)
- $y=16{e}^{x/2}-3{x}^{3}+Cx+D$
- $y=8{e}^{x/2}-{x}^{3}+Cx+D$
- $y=32{e}^{x/2}-\frac{1}{2}{x}^{3}+Cx+D$
- $y=16{e}^{x/2}+{x}^{3}+Cx+D$
- $y=32{e}^{x/2}-{x}^{3}+Cx+D$ **correct**

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=8{e}^{x/2}-6x.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int (8{e}^{x/2}-6x)\text{d}x \\  & =8\int {e}^{x/2}\,\text{d}x-6\int x\,\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =8(2{e}^{x/2})-6(\frac{1}{2}{x}^{2})+C \\  & =16{e}^{x/2}-3{x}^{2}+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (16{e}^{x/2}-3{x}^{2}+C)\text{d}x \\ y & =16\int {e}^{x/2}\,\text{d}x-3\int {x}^{2}\,\text{d}x+C\int \text{d}x \\  & =16(2{e}^{x/2})-3(\frac{1}{3}{x}^{3})+Cx+D \\  & =32{e}^{x/2}-{x}^{3}+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119042 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+2\left(6x\right)=2\left(8{e}^{x/2}\right).
$$

Field 1 (selection)
- $y=2\left(16{e}^{x/2}\right)-2\left(3{x}^{3}\right)+Cx+D$
- $y=2\left(8{e}^{x/2}\right)-2\left({x}^{3}\right)+Cx+D$
- $y=2\left(32{e}^{x/2}\right)-2\left(\frac{1}{2}{x}^{3}\right)+Cx+D$
- $y=2\left(16{e}^{x/2}\right)+2\left({x}^{3}\right)+Cx+D$
- $y=2\left(32{e}^{x/2}\right)-2\left({x}^{3}\right)+Cx+D$ **correct**

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(8{e}^{x/2}\right)-2\left(6x\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(\int (8{e}^{x/2}-6x)\text{d}x\right) \\  & =2\left(8\int {e}^{x/2}\,\text{d}x\right)-2\left(6\int x\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(8(2{e}^{x/2})\right)-2\left(6(\frac{1}{2}{x}^{2})\right)+C \\  & =2\left(16{e}^{x/2}\right)-2\left(3{x}^{2}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left(16{e}^{x/2}\right)-2\left(3{x}^{2}\right)+C)\text{d}x \\ y & =2\left(16\int {e}^{x/2}\,\text{d}x\right)-2\left(3\int {x}^{2}\,\text{d}x\right)+C\int \text{d}x \\  & =2\left(16(2{e}^{x/2})\right)-2\left(3(\frac{1}{3}{x}^{3})\right)+Cx+D \\  & =2\left(32{e}^{x/2}\right)-2\left({x}^{3}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119042 — Generated completed profile at scale=1/2

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+\frac{1}{2}\left(6x\right)=\frac{1}{2}\left(8{e}^{x/2}\right).
$$

Field 1 (selection)
- $y=\frac{1}{2}\left(16{e}^{x/2}\right)-\frac{1}{2}\left(3{x}^{3}\right)+Cx+D$
- $y=\frac{1}{2}\left(8{e}^{x/2}\right)-\frac{1}{2}\left({x}^{3}\right)+Cx+D$
- $y=\frac{1}{2}\left(32{e}^{x/2}\right)-\frac{1}{2}\left(\frac{1}{2}{x}^{3}\right)+Cx+D$
- $y=\frac{1}{2}\left(16{e}^{x/2}\right)+\frac{1}{2}\left({x}^{3}\right)+Cx+D$
- $y=\frac{1}{2}\left(32{e}^{x/2}\right)-\frac{1}{2}\left({x}^{3}\right)+Cx+D$ **correct**

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(8{e}^{x/2}\right)-\frac{1}{2}\left(6x\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(\int (8{e}^{x/2}-6x)\text{d}x\right) \\  & =\frac{1}{2}\left(8\int {e}^{x/2}\,\text{d}x\right)-\frac{1}{2}\left(6\int x\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(8(2{e}^{x/2})\right)-\frac{1}{2}\left(6(\frac{1}{2}{x}^{2})\right)+C \\  & =\frac{1}{2}\left(16{e}^{x/2}\right)-\frac{1}{2}\left(3{x}^{2}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left(16{e}^{x/2}\right)-\frac{1}{2}\left(3{x}^{2}\right)+C)\text{d}x \\ y & =\frac{1}{2}\left(16\int {e}^{x/2}\,\text{d}x\right)-\frac{1}{2}\left(3\int {x}^{2}\,\text{d}x\right)+C\int \text{d}x \\  & =\frac{1}{2}\left(16(2{e}^{x/2})\right)-\frac{1}{2}\left(3(\frac{1}{3}{x}^{3})\right)+Cx+D \\  & =\frac{1}{2}\left(32{e}^{x/2}\right)-\frac{1}{2}\left({x}^{3}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119043 — Original / exact parameter replay

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+5=6{x}^{2}.
$$

Field 1 (selection)
- $y=\frac{{x}^{4}}{4}+\frac{5{x}^{2}}{4}+Cx+D$
- $y=3{x}^{4}-5{x}^{2}+Cx+D$
- $y=\frac{{x}^{4}}{2}-4{x}^{2}+Cx+D$
- $y=3{x}^{4}+4{x}^{2}+Cx+D$
- $y=\frac{{x}^{4}}{2}-\frac{5{x}^{2}}{2}+Cx+D$ **correct**

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6{x}^{2}-5.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int (6{x}^{2}-5)\text{d}x \\  & =6\int {x}^{2}\,\text{d}x-5\int \text{d}x \\ \frac{\text{d}y}{\text{d}x} & =6(\frac{{x}^{3}}{3})-5x+C \\  & =2{x}^{3}-5x+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2{x}^{3}-5x+C)\text{d}x \\ y & =2\int {x}^{3}\,\text{d}x-5\int x\,\text{d}x+C\int \text{d}x \\  & =2(\frac{{x}^{4}}{4})-5(\frac{{x}^{2}}{2})+Cx+D \\  & =\frac{{x}^{4}}{2}-\frac{5{x}^{2}}{2}+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119043 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+2\left(5\right)=2\left(6{x}^{2}\right).
$$

Field 1 (selection)
- $y=2\left(\frac{{x}^{4}}{4}\right)+2\left(\frac{5{x}^{2}}{4}\right)+Cx+D$
- $y=2\left(3{x}^{4}\right)-2\left(5{x}^{2}\right)+Cx+D$
- $y=2\left(\frac{{x}^{4}}{2}\right)-2\left(4{x}^{2}\right)+Cx+D$
- $y=2\left(3{x}^{4}\right)+2\left(4{x}^{2}\right)+Cx+D$
- $y=2\left(\frac{{x}^{4}}{2}\right)-2\left(\frac{5{x}^{2}}{2}\right)+Cx+D$ **correct**

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(6{x}^{2}\right)-2\left(5\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(\int (6{x}^{2}-5)\text{d}x\right) \\  & =2\left(6\int {x}^{2}\,\text{d}x\right)-2\left(5\int \text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(6(\frac{{x}^{3}}{3})\right)-2\left(5x\right)+C \\  & =2\left(2{x}^{3}\right)-2\left(5x\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left(2{x}^{3}\right)-2\left(5x\right)+C)\text{d}x \\ y & =2\left(2\int {x}^{3}\,\text{d}x\right)-2\left(5\int x\,\text{d}x\right)+C\int \text{d}x \\  & =2\left(2(\frac{{x}^{4}}{4})\right)-2\left(5(\frac{{x}^{2}}{2})\right)+Cx+D \\  & =2\left(\frac{{x}^{4}}{2}\right)-2\left(\frac{5{x}^{2}}{2}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119043 — Generated completed profile at scale=1/2

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+\frac{1}{2}\left(5\right)=\frac{1}{2}\left(6{x}^{2}\right).
$$

Field 1 (selection)
- $y=\frac{1}{2}\left(\frac{{x}^{4}}{4}\right)+\frac{1}{2}\left(\frac{5{x}^{2}}{4}\right)+Cx+D$
- $y=\frac{1}{2}\left(3{x}^{4}\right)-\frac{1}{2}\left(5{x}^{2}\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{{x}^{4}}{2}\right)-\frac{1}{2}\left(4{x}^{2}\right)+Cx+D$
- $y=\frac{1}{2}\left(3{x}^{4}\right)+\frac{1}{2}\left(4{x}^{2}\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{{x}^{4}}{2}\right)-\frac{1}{2}\left(\frac{5{x}^{2}}{2}\right)+Cx+D$ **correct**

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(6{x}^{2}\right)-\frac{1}{2}\left(5\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(\int (6{x}^{2}-5)\text{d}x\right) \\  & =\frac{1}{2}\left(6\int {x}^{2}\,\text{d}x\right)-\frac{1}{2}\left(5\int \text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(6(\frac{{x}^{3}}{3})\right)-\frac{1}{2}\left(5x\right)+C \\  & =\frac{1}{2}\left(2{x}^{3}\right)-\frac{1}{2}\left(5x\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left(2{x}^{3}\right)-\frac{1}{2}\left(5x\right)+C)\text{d}x \\ y & =\frac{1}{2}\left(2\int {x}^{3}\,\text{d}x\right)-\frac{1}{2}\left(5\int x\,\text{d}x\right)+C\int \text{d}x \\  & =\frac{1}{2}\left(2(\frac{{x}^{4}}{4})\right)-\frac{1}{2}\left(5(\frac{{x}^{2}}{2})\right)+Cx+D \\  & =\frac{1}{2}\left(\frac{{x}^{4}}{2}\right)-\frac{1}{2}\left(\frac{5{x}^{2}}{2}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119044 — Original / exact parameter replay

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-{2}^{x}=\operatorname{cos}⁡x.
$$

Field 1 (selection)
- $y={2}^{x}{ln}^{2}⁡2-\operatorname{sin}⁡x+Cx+D$
- $y=\frac{{2}^{x}}{\operatorname{ln}⁡2}+\operatorname{cos}⁡x+Cx+D$
- $y=\frac{{2}^{x}}{{ln}^{2}⁡2}+\operatorname{sin}⁡x+Cx+D$
- $y=\frac{{2}^{x}}{{ln}^{2}⁡2}-\operatorname{cos}⁡x+Cx+D$ **correct**
- $y={2}^{x}\operatorname{ln}⁡2-\operatorname{cos}⁡x+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\operatorname{cos}⁡x+{2}^{x}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int (\operatorname{cos}⁡x+{2}^{x})\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =\int \operatorname{cos}⁡x\,\text{d}x+\int {2}^{x}\,\text{d}x \\  & =\operatorname{sin}⁡x+\frac{{2}^{x}}{\operatorname{ln}⁡2}+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\operatorname{sin}⁡x+\frac{{2}^{x}}{\operatorname{ln}⁡2}+C)\text{d}x \\ y & =\int \operatorname{sin}⁡x\,\text{d}x+\frac{1}{\operatorname{ln}⁡2}\int {2}^{x}\,\text{d}x+C\int \text{d}x \\  & =-\operatorname{cos}⁡x+\frac{1}{\operatorname{ln}⁡2}(\frac{{2}^{x}}{\operatorname{ln}⁡2})+Cx+D \\  & =\frac{{2}^{x}}{{ln}^{2}⁡2}-\operatorname{cos}⁡x+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119044 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-2\left({2}^{x}\right)=2\left(\operatorname{cos}⁡x\right).
$$

Field 1 (selection)
- $y=2\left({2}^{x}{ln}^{2}⁡2\right)-2\left(\operatorname{sin}⁡x\right)+Cx+D$
- $y=2\left(\frac{{2}^{x}}{\operatorname{ln}⁡2}\right)+2\left(\operatorname{cos}⁡x\right)+Cx+D$
- $y=2\left(\frac{{2}^{x}}{{ln}^{2}⁡2}\right)+2\left(\operatorname{sin}⁡x\right)+Cx+D$
- $y=2\left(\frac{{2}^{x}}{{ln}^{2}⁡2}\right)-2\left(\operatorname{cos}⁡x\right)+Cx+D$ **correct**
- $y=2\left({2}^{x}\operatorname{ln}⁡2\right)-2\left(\operatorname{cos}⁡x\right)+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(\operatorname{cos}⁡x\right)+2\left({2}^{x}\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(\int (\operatorname{cos}⁡x+{2}^{x})\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(\int \operatorname{cos}⁡x\,\text{d}x\right)+2\left(\int {2}^{x}\,\text{d}x\right) \\  & =2\left(\operatorname{sin}⁡x\right)+2\left(\frac{{2}^{x}}{\operatorname{ln}⁡2}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left(\operatorname{sin}⁡x\right)+2\left(\frac{{2}^{x}}{\operatorname{ln}⁡2}\right)+C)\text{d}x \\ y & =2\left(\int \operatorname{sin}⁡x\,\text{d}x\right)+2\left(\frac{1}{\operatorname{ln}⁡2}\int {2}^{x}\,\text{d}x\right)+C\int \text{d}x \\  & =-2\left(\operatorname{cos}⁡x\right)+2\left(\frac{1}{\operatorname{ln}⁡2}(\frac{{2}^{x}}{\operatorname{ln}⁡2})\right)+Cx+D \\  & =2\left(\frac{{2}^{x}}{{ln}^{2}⁡2}\right)-2\left(\operatorname{cos}⁡x\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-119044 — Generated completed profile at scale=1/2

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-\frac{1}{2}\left({2}^{x}\right)=\frac{1}{2}\left(\operatorname{cos}⁡x\right).
$$

Field 1 (selection)
- $y=\frac{1}{2}\left({2}^{x}\ln^{2}2\right)-\frac{1}{2}\left(\operatorname{sin}⁡x\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{{2}^{x}}{\operatorname{ln}⁡2}\right)+\frac{1}{2}\left(\operatorname{cos}⁡x\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{{2}^{x}}{\ln^{2}2}\right)+\frac{1}{2}\left(\operatorname{sin}⁡x\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{{2}^{x}}{\ln^{2}2}\right)-\frac{1}{2}\left(\operatorname{cos}⁡x\right)+Cx+D$ **correct**
- $y=\frac{1}{2}\left({2}^{x}\operatorname{ln}⁡2\right)-\frac{1}{2}\left(\operatorname{cos}⁡x\right)+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(\operatorname{cos}⁡x\right)+\frac{1}{2}\left({2}^{x}\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(\int (\operatorname{cos}⁡x+{2}^{x})\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(\int \operatorname{cos}⁡x\,\text{d}x\right)+\frac{1}{2}\left(\int {2}^{x}\,\text{d}x\right) \\  & =\frac{1}{2}\left(\operatorname{sin}⁡x\right)+\frac{1}{2}\left(\frac{{2}^{x}}{\operatorname{ln}⁡2}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left(\operatorname{sin}⁡x\right)+\frac{1}{2}\left(\frac{{2}^{x}}{\operatorname{ln}⁡2}\right)+C)\text{d}x \\ y & =\frac{1}{2}\left(\int \operatorname{sin}⁡x\,\text{d}x\right)+\frac{1}{2}\left(\frac{1}{\operatorname{ln}⁡2}\int {2}^{x}\,\text{d}x\right)+C\int \text{d}x \\  & =-\frac{1}{2}\left(\operatorname{cos}⁡x\right)+\frac{1}{2}\left(\frac{1}{\operatorname{ln}⁡2}(\frac{{2}^{x}}{\operatorname{ln}⁡2})\right)+Cx+D \\  & =\frac{1}{2}\left(\frac{{2}^{x}}{\ln^{2}2}\right)-\frac{1}{2}\left(\operatorname{cos}⁡x\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-50146 — Original / exact parameter replay

Solve the differential equation $x\cdot \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6{x}^{3}-4{x}^{2}.$

Field 1 (selection)
- $y=\frac{{x}^{4}}{2}-\frac{2{x}^{3}}{3}+Cx+D$ **correct**
- $y=\frac{{x}^{4}}{2}-\frac{{x}^{3}}{3}+Cx+D$
- $y={x}^{4}-\frac{{x}^{3}}{3}+C{x}^{2}+D$
- $y=\frac{{x}^{4}}{4}-\frac{{x}^{3}}{6}+Cx+D$
- $y={x}^{4}-\frac{2{x}^{3}}{3}+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6{x}^{2}-4x.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int (6{x}^{2}-4x)\,\text{d}x \\  & =6\int {x}^{2}\,\text{d}x-4\int x\,\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =6(\frac{{x}^{3}}{3})-4(\frac{{x}^{2}}{2})+C \\  & =2{x}^{3}-2{x}^{2}+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2{x}^{3}-2{x}^{2}+C)\,\text{d}x \\ y & =2\int {x}^{3}\,\text{d}x-2\int {x}^{2}\,\text{d}x+C\int \text{d}x \\  & =2(\frac{{x}^{4}}{4})-2(\frac{{x}^{3}}{3})+Cx+D \\  & =\frac{{x}^{4}}{2}-\frac{2{x}^{3}}{3}+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-50146 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation $x\cdot \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(6{x}^{3}\right)-2\left(4{x}^{2}\right).$

Field 1 (selection)
- $y=2\left(\frac{{x}^{4}}{2}\right)-2\left(\frac{2{x}^{3}}{3}\right)+Cx+D$ **correct**
- $y=2\left(\frac{{x}^{4}}{2}\right)-2\left(\frac{{x}^{3}}{3}\right)+Cx+D$
- $y=2\left({x}^{4}\right)-2\left(\frac{{x}^{3}}{3}\right)+C{x}^{2}+D$
- $y=2\left(\frac{{x}^{4}}{4}\right)-2\left(\frac{{x}^{3}}{6}\right)+Cx+D$
- $y=2\left({x}^{4}\right)-2\left(\frac{2{x}^{3}}{3}\right)+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(6{x}^{2}\right)-2\left(4x\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(\int (6{x}^{2}-4x)\,\text{d}x\right) \\  & =2\left(6\int {x}^{2}\,\text{d}x\right)-2\left(4\int x\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(6(\frac{{x}^{3}}{3})\right)-2\left(4(\frac{{x}^{2}}{2})\right)+C \\  & =2\left(2{x}^{3}\right)-2\left(2{x}^{2}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left(2{x}^{3}\right)-2\left(2{x}^{2}\right)+C)\,\text{d}x \\ y & =2\left(2\int {x}^{3}\,\text{d}x\right)-2\left(2\int {x}^{2}\,\text{d}x\right)+C\int \text{d}x \\  & =2\left(2(\frac{{x}^{4}}{4})\right)-2\left(2(\frac{{x}^{3}}{3})\right)+Cx+D \\  & =2\left(\frac{{x}^{4}}{2}\right)-2\left(\frac{2{x}^{3}}{3}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-50146 — Generated completed profile at scale=1/2

Solve the differential equation $x\cdot \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(6{x}^{3}\right)-\frac{1}{2}\left(4{x}^{2}\right).$

Field 1 (selection)
- $y=\frac{1}{2}\left(\frac{{x}^{4}}{2}\right)-\frac{1}{2}\left(\frac{2{x}^{3}}{3}\right)+Cx+D$ **correct**
- $y=\frac{1}{2}\left(\frac{{x}^{4}}{2}\right)-\frac{1}{2}\left(\frac{{x}^{3}}{3}\right)+Cx+D$
- $y=\frac{1}{2}\left({x}^{4}\right)-\frac{1}{2}\left(\frac{{x}^{3}}{3}\right)+C{x}^{2}+D$
- $y=\frac{1}{2}\left(\frac{{x}^{4}}{4}\right)-\frac{1}{2}\left(\frac{{x}^{3}}{6}\right)+Cx+D$
- $y=\frac{1}{2}\left({x}^{4}\right)-\frac{1}{2}\left(\frac{2{x}^{3}}{3}\right)+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(6{x}^{2}\right)-\frac{1}{2}\left(4x\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(\int (6{x}^{2}-4x)\,\text{d}x\right) \\  & =\frac{1}{2}\left(6\int {x}^{2}\,\text{d}x\right)-\frac{1}{2}\left(4\int x\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(6(\frac{{x}^{3}}{3})\right)-\frac{1}{2}\left(4(\frac{{x}^{2}}{2})\right)+C \\  & =\frac{1}{2}\left(2{x}^{3}\right)-\frac{1}{2}\left(2{x}^{2}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left(2{x}^{3}\right)-\frac{1}{2}\left(2{x}^{2}\right)+C)\,\text{d}x \\ y & =\frac{1}{2}\left(2\int {x}^{3}\,\text{d}x\right)-\frac{1}{2}\left(2\int {x}^{2}\,\text{d}x\right)+C\int \text{d}x \\  & =\frac{1}{2}\left(2(\frac{{x}^{4}}{4})\right)-\frac{1}{2}\left(2(\frac{{x}^{3}}{3})\right)+Cx+D \\  & =\frac{1}{2}\left(\frac{{x}^{4}}{2}\right)-\frac{1}{2}\left(\frac{2{x}^{3}}{3}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-79554 — Original / exact parameter replay

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-\sqrt{x}=0.
$$

Field 1 (selection)
- $y=\frac{4}{15}\,{x}^{5/2}+Cx+D$ **correct**
- $y=\frac{2}{15}\,{x}^{5/2}+C{x}^{2}+D$
- $y=\frac{2}{3}\,{x}^{3/2}+Cx+D$
- $y=\frac{4}{5}\,{x}^{3/2}+C{x}^{2}+D$
- $y=\frac{2}{15}\,{x}^{5/2}+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\sqrt{x}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \sqrt{x}\,\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =\frac{2}{3}{x}^{3/2}+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{2}{3}{x}^{3/2}+C)\text{d}x \\ y & =\frac{2}{3}\int {x}^{3/2}\,\text{d}x+C\int \text{d}x \\  & =\frac{2}{3}(\frac{2}{5}\,{x}^{5/2})+Cx+D \\  & =\frac{4}{15}\,{x}^{5/2}+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-79554 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-2\left(\sqrt{x}\right)=2\left(0\right).
$$

Field 1 (selection)
- $y=2\left(\frac{4}{15}\,{x}^{5/2}\right)+Cx+D$ **correct**
- $y=2\left(\frac{2}{15}\,{x}^{5/2}\right)+C{x}^{2}+D$
- $y=2\left(\frac{2}{3}\,{x}^{3/2}\right)+Cx+D$
- $y=2\left(\frac{4}{5}\,{x}^{3/2}\right)+C{x}^{2}+D$
- $y=2\left(\frac{2}{15}\,{x}^{5/2}\right)+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(\sqrt{x}\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(\int \sqrt{x}\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(\frac{2}{3}{x}^{3/2}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left(\frac{2}{3}{x}^{3/2}\right)+C)\text{d}x \\ y & =2\left(\frac{2}{3}\int {x}^{3/2}\,\text{d}x\right)+C\int \text{d}x \\  & =2\left(\frac{2}{3}(\frac{2}{5}\,{x}^{5/2})\right)+Cx+D \\  & =2\left(\frac{4}{15}\,{x}^{5/2}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-79554 — Generated completed profile at scale=1/2

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-\frac{1}{2}\left(\sqrt{x}\right)=\frac{1}{2}\left(0\right).
$$

Field 1 (selection)
- $y=\frac{1}{2}\left(\frac{4}{15}\,{x}^{5/2}\right)+Cx+D$ **correct**
- $y=\frac{1}{2}\left(\frac{2}{15}\,{x}^{5/2}\right)+C{x}^{2}+D$
- $y=\frac{1}{2}\left(\frac{2}{3}\,{x}^{3/2}\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{4}{5}\,{x}^{3/2}\right)+C{x}^{2}+D$
- $y=\frac{1}{2}\left(\frac{2}{15}\,{x}^{5/2}\right)+Cx+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(\sqrt{x}\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(\int \sqrt{x}\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(\frac{2}{3}{x}^{3/2}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left(\frac{2}{3}{x}^{3/2}\right)+C)\text{d}x \\ y & =\frac{1}{2}\left(\frac{2}{3}\int {x}^{3/2}\,\text{d}x\right)+C\int \text{d}x \\  & =\frac{1}{2}\left(\frac{2}{3}(\frac{2}{5}\,{x}^{5/2})\right)+Cx+D \\  & =\frac{1}{2}\left(\frac{4}{15}\,{x}^{5/2}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119039 — Original / exact parameter replay

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=20{x}^{3}.$

Field 1 (selection)
- $y=4{x}^{4}+C{x}^{2}+Dx$
- $y={x}^{5}+Cx+D$ **correct**
- $y=5{x}^{4}+Cx+D$
- $y={x}^{5}+C{x}^{2}+Dx$
- $y=4{x}^{5}+Cx+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =20\int {x}^{3}\,\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =20\cdot \frac{1}{4}{x}^{4}+C \\  & =5{x}^{4}+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (5{x}^{4}+C)\text{d}x \\ y & =5\cdot \frac{1}{5}{x}^{5}+Cx+D \\  & ={x}^{5}+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119039 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(20{x}^{3}\right).$

Field 1 (selection)
- $y=2\left(4{x}^{4}\right)+C{x}^{2}+Dx$
- $y=2\left({x}^{5}\right)+Cx+D$ **correct**
- $y=2\left(5{x}^{4}\right)+Cx+D$
- $y=2\left({x}^{5}\right)+C{x}^{2}+Dx$
- $y=2\left(4{x}^{5}\right)+Cx+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(20\int {x}^{3}\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(20\cdot \frac{1}{4}{x}^{4}\right)+C \\  & =2\left(5{x}^{4}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left(5{x}^{4}\right)+C)\text{d}x \\ y & =2\left(5\cdot \frac{1}{5}{x}^{5}\right)+Cx+D \\  & =2\left({x}^{5}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Easy — q-119039 — Generated completed profile at scale=1/2

Solve the differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(20{x}^{3}\right).$

Field 1 (selection)
- $y=\frac{1}{2}\left(4{x}^{4}\right)+C{x}^{2}+Dx$
- $y=\frac{1}{2}\left({x}^{5}\right)+Cx+D$ **correct**
- $y=\frac{1}{2}\left(5{x}^{4}\right)+Cx+D$
- $y=\frac{1}{2}\left({x}^{5}\right)+C{x}^{2}+Dx$
- $y=\frac{1}{2}\left(4{x}^{5}\right)+Cx+D$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(20\int {x}^{3}\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(20\cdot \frac{1}{4}{x}^{4}\right)+C \\  & =\frac{1}{2}\left(5{x}^{4}\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left(5{x}^{4}\right)+C)\text{d}x \\ y & =\frac{1}{2}\left(5\cdot \frac{1}{5}{x}^{5}\right)+Cx+D \\  & =\frac{1}{2}\left({x}^{5}\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-99009 — Original / exact parameter replay

Solve the differential equation $2\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-\operatorname{sin}⁡x=4x.$

Field 1 (selection)
- $y={x}^{3}-2\operatorname{cos}⁡x+C+D$
- $y={x}^{3}-\operatorname{sin}⁡x+Cx+D$
- $y=\frac{{x}^{3}}{3}-\operatorname{sin}⁡x+Cx+D$
- $y=\frac{{x}^{3}}{3}-\frac{1}{2}\operatorname{sin}⁡x+Cx+D$ **correct**
- $y=\frac{{x}^{3}}{3}-\operatorname{cos}⁡x+C+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2x+\frac{1}{2}\operatorname{sin}⁡x.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int (2x+\frac{1}{2}\operatorname{sin}⁡x)\text{d}x \\  & =2\int x\,\text{d}x+\frac{1}{2}\int \operatorname{sin}⁡x\,\text{d}x \\ \frac{\text{d}y}{\text{d}x} & =2(\frac{{x}^{2}}{2})+\frac{1}{2}(-\operatorname{cos}⁡x)+C \\  & ={x}^{2}-\frac{1}{2}\operatorname{cos}⁡x+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int ({x}^{2}-\frac{1}{2}\operatorname{cos}⁡x+C)\,\text{d}x \\ y & =\int {x}^{2}\,\text{d}x-\frac{1}{2}\int \operatorname{cos}⁡x\,\text{d}x+C\int \text{d}x \\  & =(\frac{{x}^{3}}{3})-\frac{1}{2}(\operatorname{sin}⁡x)+Cx+D \\  & =\frac{{x}^{3}}{3}-\frac{1}{2}\operatorname{sin}⁡x+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-99009 — Generated observed profile at scale=2 (raw evidence)

Solve the differential equation $2\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-2\left(\operatorname{sin}⁡x\right)=2\left(4x\right).$

Field 1 (selection)
- $y=2\left({x}^{3}\right)-2\left(2\operatorname{cos}⁡x\right)+C+D$
- $y=2\left({x}^{3}\right)-2\left(\operatorname{sin}⁡x\right)+Cx+D$
- $y=2\left(\frac{{x}^{3}}{3}\right)-2\left(\operatorname{sin}⁡x\right)+Cx+D$
- $y=2\left(\frac{{x}^{3}}{3}\right)-2\left(\frac{1}{2}\operatorname{sin}⁡x\right)+Cx+D$ **correct**
- $y=2\left(\frac{{x}^{3}}{3}\right)-2\left(\operatorname{cos}⁡x\right)+C+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=2\left(2x\right)+2\left(\frac{1}{2}\operatorname{sin}⁡x\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =2\left(\int (2x+\frac{1}{2}\operatorname{sin}⁡x)\text{d}x\right) \\  & =2\left(2\int x\,\text{d}x\right)+2\left(\frac{1}{2}\int \operatorname{sin}⁡x\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =2\left(2(\frac{{x}^{2}}{2})\right)+2\left(\frac{1}{2}(-\operatorname{cos}⁡x)\right)+C \\  & =2\left({x}^{2}\right)-2\left(\frac{1}{2}\operatorname{cos}⁡x\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (2\left({x}^{2}\right)-2\left(\frac{1}{2}\operatorname{cos}⁡x\right)+C)\,\text{d}x \\ y & =2\left(\int {x}^{2}\,\text{d}x\right)-2\left(\frac{1}{2}\int \operatorname{cos}⁡x\,\text{d}x\right)+C\int \text{d}x \\  & =2\left((\frac{{x}^{3}}{3})\right)-2\left(\frac{1}{2}(\operatorname{sin}⁡x)\right)+Cx+D \\  & =2\left(\frac{{x}^{3}}{3}\right)-2\left(\frac{1}{2}\operatorname{sin}⁡x\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Moderate — q-99009 — Generated completed profile at scale=1/2

Solve the differential equation $2\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}-\frac{1}{2}\left(\operatorname{sin}⁡x\right)=\frac{1}{2}\left(4x\right).$

Field 1 (selection)
- $y=\frac{1}{2}\left({x}^{3}\right)-\frac{1}{2}\left(2\operatorname{cos}⁡x\right)+C+D$
- $y=\frac{1}{2}\left({x}^{3}\right)-\frac{1}{2}\left(\operatorname{sin}⁡x\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{{x}^{3}}{3}\right)-\frac{1}{2}\left(\operatorname{sin}⁡x\right)+Cx+D$
- $y=\frac{1}{2}\left(\frac{{x}^{3}}{3}\right)-\frac{1}{2}\left(\frac{1}{2}\operatorname{sin}⁡x\right)+Cx+D$ **correct**
- $y=\frac{1}{2}\left(\frac{{x}^{3}}{3}\right)-\frac{1}{2}\left(\operatorname{cos}⁡x\right)+C+D$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=\frac{1}{2}\left(2x\right)+\frac{1}{2}\left(\frac{1}{2}\operatorname{sin}⁡x\right).
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\frac{1}{2}\left(\int (2x+\frac{1}{2}\operatorname{sin}⁡x)\text{d}x\right) \\  & =\frac{1}{2}\left(2\int x\,\text{d}x\right)+\frac{1}{2}\left(\frac{1}{2}\int \operatorname{sin}⁡x\,\text{d}x\right) \\ \frac{\text{d}y}{\text{d}x} & =\frac{1}{2}\left(2(\frac{{x}^{2}}{2})\right)+\frac{1}{2}\left(\frac{1}{2}(-\operatorname{cos}⁡x)\right)+C \\  & =\frac{1}{2}\left({x}^{2}\right)-\frac{1}{2}\left(\frac{1}{2}\operatorname{cos}⁡x\right)+C.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (\frac{1}{2}\left({x}^{2}\right)-\frac{1}{2}\left(\frac{1}{2}\operatorname{cos}⁡x\right)+C)\,\text{d}x \\ y & =\frac{1}{2}\left(\int {x}^{2}\,\text{d}x\right)-\frac{1}{2}\left(\frac{1}{2}\int \operatorname{cos}⁡x\,\text{d}x\right)+C\int \text{d}x \\  & =\frac{1}{2}\left((\frac{{x}^{3}}{3})\right)-\frac{1}{2}\left(\frac{1}{2}(\operatorname{sin}⁡x)\right)+Cx+D \\  & =\frac{1}{2}\left(\frac{{x}^{3}}{3}\right)-\frac{1}{2}\left(\frac{1}{2}\operatorname{sin}⁡x\right)+Cx+D.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored easy — single_power — seed 21

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 3 x^{2}.
$$

Field 1 (selection)
- $y=C x + D - \frac{x^{4}}{4}$ **correct**
- $y=D - \frac{x^{4}}{4}$
- $y=C x - \frac{x^{4}}{4}$
- $y=C x + D + \frac{x^{4}}{4}$
- $y=C x + D - x^{3}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 3 x^{2}\right)\,\text{d}x \\  & =((-3)\int \left(x^{2}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{x^{3}}{3}\right))+C \\  & =C - x^{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - x^{3}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{3}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{4}}{4}\right))+Cx+D \\  & =C x + D - \frac{x^{4}}{4}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored easy — single_power — seed 54

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 4 x^{3}.
$$

Field 1 (selection)
- $y=D - \frac{x^{5}}{5}$
- $y=C x + D - x^{4}$
- $y=C x - \frac{x^{5}}{5}$
- $y=C x + D - \frac{x^{5}}{5}$ **correct**
- $y=C x + D + \frac{x^{5}}{5}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 4 x^{3}\right)\,\text{d}x \\  & =((-4)\int \left(x^{3}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{x^{4}}{4}\right))+C \\  & =C - x^{4}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - x^{4}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{4}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{5}}{5}\right))+Cx+D \\  & =C x + D - \frac{x^{5}}{5}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored easy — single_exp — seed 21

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 3 e^{3 x}.
$$

Field 1 (selection)
- $y=C x + D - \frac{e^{3 x}}{3}$ **correct**
- $y=D - \frac{e^{3 x}}{3}$
- $y=C x - \frac{e^{3 x}}{3}$
- $y=C x + D + \frac{e^{3 x}}{3}$
- $y=C x + D - e^{3 x}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 3 e^{3 x}\right)\,\text{d}x \\  & =((-3)\int \left(e^{3 x}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{e^{3 x}}{3}\right))+C \\  & =C - e^{3 x}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - e^{3 x}\right)\,\text{d}x \\ y & =((-1)\int \left(e^{3 x}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{e^{3 x}}{3}\right))+Cx+D \\  & =C x + D - \frac{e^{3 x}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored easy — single_exp — seed 54

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 4 e^{3 x}.
$$

Field 1 (selection)
- $y=D - \frac{4 e^{3 x}}{9}$
- $y=C x + D - \frac{4 e^{3 x}}{3}$
- $y=C x - \frac{4 e^{3 x}}{9}$
- $y=C x + D - \frac{4 e^{3 x}}{9}$ **correct**
- $y=C x + D + \frac{4 e^{3 x}}{9}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 4 e^{3 x}\right)\,\text{d}x \\  & =((-4)\int \left(e^{3 x}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{e^{3 x}}{3}\right))+C \\  & =C - \frac{4 e^{3 x}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - \frac{4 e^{3 x}}{3}\right)\,\text{d}x \\ y & =((- \frac{4}{3})\int \left(e^{3 x}\right)\,\text{d}x)+C\int \text{d}x \\  & =((- \frac{4}{3})\left(\frac{e^{3 x}}{3}\right))+Cx+D \\  & =C x + D - \frac{4 e^{3 x}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored easy — single_sin — seed 21

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 3 \sin{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=C x + D + \frac{\sin{\left(3 x \right)}}{3}$ **correct**
- $y=D + \frac{\sin{\left(3 x \right)}}{3}$
- $y=C x + \frac{\sin{\left(3 x \right)}}{3}$
- $y=C x + D - \frac{\sin{\left(3 x \right)}}{3}$
- $y=C x + D + \cos{\left(3 x \right)}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 3 \sin{\left(3 x \right)}\right)\,\text{d}x \\  & =((-3)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+C \\  & =C + \cos{\left(3 x \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C + \cos{\left(3 x \right)}\right)\,\text{d}x \\ y & =((1)\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((1)\left(\frac{\sin{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D + \frac{\sin{\left(3 x \right)}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored easy — single_sin — seed 54

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 4 \sin{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=D + \frac{4 \sin{\left(3 x \right)}}{9}$
- $y=C x + D + \frac{4 \cos{\left(3 x \right)}}{3}$
- $y=C x + \frac{4 \sin{\left(3 x \right)}}{9}$
- $y=C x + D + \frac{4 \sin{\left(3 x \right)}}{9}$ **correct**
- $y=C x + D - \frac{4 \sin{\left(3 x \right)}}{9}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 4 \sin{\left(3 x \right)}\right)\,\text{d}x \\  & =((-4)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+C \\  & =C + \frac{4 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C + \frac{4 \cos{\left(3 x \right)}}{3}\right)\,\text{d}x \\ y & =((\frac{4}{3})\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((\frac{4}{3})\left(\frac{\sin{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D + \frac{4 \sin{\left(3 x \right)}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored easy — single_cos — seed 21

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 3 \cos{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=C x + D + \frac{\cos{\left(3 x \right)}}{3}$ **correct**
- $y=D + \frac{\cos{\left(3 x \right)}}{3}$
- $y=C x + \frac{\cos{\left(3 x \right)}}{3}$
- $y=C x + D - \frac{\cos{\left(3 x \right)}}{3}$
- $y=C x + D - \sin{\left(3 x \right)}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 3 \cos{\left(3 x \right)}\right)\,\text{d}x \\  & =((-3)\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{\sin{\left(3 x \right)}}{3}\right))+C \\  & =C - \sin{\left(3 x \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - \sin{\left(3 x \right)}\right)\,\text{d}x \\ y & =((-1)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D + \frac{\cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored easy — single_cos — seed 54

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 4 \cos{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=D + \frac{4 \cos{\left(3 x \right)}}{9}$
- $y=C x + D - \frac{4 \sin{\left(3 x \right)}}{3}$
- $y=C x + \frac{4 \cos{\left(3 x \right)}}{9}$
- $y=C x + D + \frac{4 \cos{\left(3 x \right)}}{9}$ **correct**
- $y=C x + D - \frac{4 \cos{\left(3 x \right)}}{9}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 4 \cos{\left(3 x \right)}\right)\,\text{d}x \\  & =((-4)\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{\sin{\left(3 x \right)}}{3}\right))+C \\  & =C - \frac{4 \sin{\left(3 x \right)}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - \frac{4 \sin{\left(3 x \right)}}{3}\right)\,\text{d}x \\ y & =((- \frac{4}{3})\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((- \frac{4}{3})\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D + \frac{4 \cos{\left(3 x \right)}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored moderate — power_exp — seed 21

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 12 x^{2} + 24 e^{3 x}.
$$

Field 1 (selection)
- $y=C x + D - \frac{x^{4}}{4} + \frac{2 e^{3 x}}{3}$ **correct**
- $y=D - \frac{x^{4}}{4} + \frac{2 e^{3 x}}{3}$
- $y=C x - \frac{x^{4}}{4} + \frac{2 e^{3 x}}{3}$
- $y=C x + D + \frac{x^{4}}{4} - \frac{2 e^{3 x}}{3}$
- $y=C x + D - x^{3} + 2 e^{3 x}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 3 x^{2} + 6 e^{3 x}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 3 x^{2} + 6 e^{3 x}\right)\,\text{d}x \\  & =((-3)\int \left(x^{2}\right)\,\text{d}x) + ((6)\int \left(e^{3 x}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{x^{3}}{3}\right)) + ((6)\left(\frac{e^{3 x}}{3}\right))+C \\  & =C - x^{3} + 2 e^{3 x}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - x^{3} + 2 e^{3 x}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{3}\right)\,\text{d}x) + ((2)\int \left(e^{3 x}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{4}}{4}\right)) + ((2)\left(\frac{e^{3 x}}{3}\right))+Cx+D \\  & =C x + D - \frac{x^{4}}{4} + \frac{2 e^{3 x}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored moderate — power_exp — seed 54

Solve the differential equation

$$
3\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 12 x^{3} + 21 e^{3 x}.
$$

Field 1 (selection)
- $y=D - \frac{x^{5}}{5} + \frac{7 e^{3 x}}{9}$
- $y=C x + D - x^{4} + \frac{7 e^{3 x}}{3}$
- $y=C x - \frac{x^{5}}{5} + \frac{7 e^{3 x}}{9}$
- $y=C x + D - \frac{x^{5}}{5} + \frac{7 e^{3 x}}{9}$ **correct**
- $y=C x + D + \frac{x^{5}}{5} - \frac{7 e^{3 x}}{9}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 4 x^{3} + 7 e^{3 x}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 4 x^{3} + 7 e^{3 x}\right)\,\text{d}x \\  & =((-4)\int \left(x^{3}\right)\,\text{d}x) + ((7)\int \left(e^{3 x}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{x^{4}}{4}\right)) + ((7)\left(\frac{e^{3 x}}{3}\right))+C \\  & =C - x^{4} + \frac{7 e^{3 x}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - x^{4} + \frac{7 e^{3 x}}{3}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{4}\right)\,\text{d}x) + ((\frac{7}{3})\int \left(e^{3 x}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{5}}{5}\right)) + ((\frac{7}{3})\left(\frac{e^{3 x}}{3}\right))+Cx+D \\  & =C x + D - \frac{x^{5}}{5} + \frac{7 e^{3 x}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored moderate — power_trig — seed 21

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 12 x^{2} + 24 \cos{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=C x + D - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$ **correct**
- $y=D - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x + D + \frac{x^{4}}{4} + \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x + D - x^{3} + 2 \sin{\left(3 x \right)}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 3 x^{2} + 6 \cos{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 3 x^{2} + 6 \cos{\left(3 x \right)}\right)\,\text{d}x \\  & =((-3)\int \left(x^{2}\right)\,\text{d}x) + ((6)\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{x^{3}}{3}\right)) + ((6)\left(\frac{\sin{\left(3 x \right)}}{3}\right))+C \\  & =C - x^{3} + 2 \sin{\left(3 x \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - x^{3} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{3}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{4}}{4}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored moderate — power_trig — seed 54

Solve the differential equation

$$
3\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 12 x^{3} + 6 \sin{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=D - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=C x + D - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=C x + D - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$ **correct**
- $y=C x + D + \frac{x^{5}}{5} + \frac{2 \sin{\left(3 x \right)}}{9}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 4 x^{3} + 2 \sin{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 4 x^{3} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\  & =((-4)\int \left(x^{3}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{x^{4}}{4}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+C \\  & =C - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{4}\right)\,\text{d}x) + ((- \frac{2}{3})\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{5}}{5}\right)) + ((- \frac{2}{3})\left(\frac{\sin{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored moderate — two_powers — seed 21

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=24 x^{3} - 12 x^{2}.
$$

Field 1 (selection)
- $y=C x + D + \frac{3 x^{5}}{10} - \frac{x^{4}}{4}$ **correct**
- $y=D + \frac{3 x^{5}}{10} - \frac{x^{4}}{4}$
- $y=C x + \frac{3 x^{5}}{10} - \frac{x^{4}}{4}$
- $y=C x + D - \frac{3 x^{5}}{10} + \frac{x^{4}}{4}$
- $y=C x + D + \frac{3 x^{4}}{2} - x^{3}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6 x^{3} - 3 x^{2}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(6 x^{3} - 3 x^{2}\right)\,\text{d}x \\  & =((-3)\int \left(x^{2}\right)\,\text{d}x) + ((6)\int \left(x^{3}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{x^{3}}{3}\right)) + ((6)\left(\frac{x^{4}}{4}\right))+C \\  & =C + \frac{3 x^{4}}{2} - x^{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C + \frac{3 x^{4}}{2} - x^{3}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{3}\right)\,\text{d}x) + ((\frac{3}{2})\int \left(x^{4}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{4}}{4}\right)) + ((\frac{3}{2})\left(\frac{x^{5}}{5}\right))+Cx+D \\  & =C x + D + \frac{3 x^{5}}{10} - \frac{x^{4}}{4}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored moderate — two_powers — seed 54

Solve the differential equation

$$
3\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=21 x^{4} - 12 x^{3}.
$$

Field 1 (selection)
- $y=D + \frac{7 x^{6}}{30} - \frac{x^{5}}{5}$
- $y=C x + D + \frac{7 x^{5}}{5} - x^{4}$
- $y=C x + \frac{7 x^{6}}{30} - \frac{x^{5}}{5}$
- $y=C x + D + \frac{7 x^{6}}{30} - \frac{x^{5}}{5}$ **correct**
- $y=C x + D - \frac{7 x^{6}}{30} + \frac{x^{5}}{5}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=7 x^{4} - 4 x^{3}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(7 x^{4} - 4 x^{3}\right)\,\text{d}x \\  & =((-4)\int \left(x^{3}\right)\,\text{d}x) + ((7)\int \left(x^{4}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{x^{4}}{4}\right)) + ((7)\left(\frac{x^{5}}{5}\right))+C \\  & =C + \frac{7 x^{5}}{5} - x^{4}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C + \frac{7 x^{5}}{5} - x^{4}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{4}\right)\,\text{d}x) + ((\frac{7}{5})\int \left(x^{5}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{5}}{5}\right)) + ((\frac{7}{5})\left(\frac{x^{6}}{6}\right))+Cx+D \\  & =C x + D + \frac{7 x^{6}}{30} - \frac{x^{5}}{5}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored moderate — base_trig — seed 21

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=24 \cdot 2^{x} + 24 \cos{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D - \frac{2 \cos{\left(3 x \right)}}{3}$ **correct**
- $y=\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + D - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=- \frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D + \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}} + C x + D + 2 \sin{\left(3 x \right)}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6 \cdot 2^{x} + 6 \cos{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(6 \cdot 2^{x} + 6 \cos{\left(3 x \right)}\right)\,\text{d}x \\  & =((6)\int \left(2^{x}\right)\,\text{d}x) + ((6)\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((6)\left(\frac{2^{x}}{\ln{\left(2 \right)}}\right)) + ((6)\left(\frac{\sin{\left(3 x \right)}}{3}\right))+C \\  & =\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}} + C + 2 \sin{\left(3 x \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}} + C + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\ y & =((\frac{6}{\ln{\left(2 \right)}})\int \left(2^{x}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((\frac{6}{\ln{\left(2 \right)}})\left(\frac{2^{x}}{\ln{\left(2 \right)}}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+Cx+D \\  & =\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored moderate — base_trig — seed 54

Solve the differential equation

$$
3\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=21 \cdot 3^{x} + 6 \sin{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + D - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}} + C x + D - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + C x - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + C x + D - \frac{2 \sin{\left(3 x \right)}}{9}$ **correct**
- $y=- \frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + C x + D + \frac{2 \sin{\left(3 x \right)}}{9}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=7 \cdot 3^{x} + 2 \sin{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(7 \cdot 3^{x} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\  & =((7)\int \left(3^{x}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((7)\left(\frac{3^{x}}{\ln{\left(3 \right)}}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+C \\  & =\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}} + C - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}} + C - \frac{2 \cos{\left(3 x \right)}}{3}\right)\,\text{d}x \\ y & =((\frac{7}{\ln{\left(3 \right)}})\int \left(3^{x}\right)\,\text{d}x) + ((- \frac{2}{3})\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((\frac{7}{\ln{\left(3 \right)}})\left(\frac{3^{x}}{\ln{\left(3 \right)}}\right)) + ((- \frac{2}{3})\left(\frac{\sin{\left(3 x \right)}}{3}\right))+Cx+D \\  & =\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + C x + D - \frac{2 \sin{\left(3 x \right)}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored hard — power_exp_trig — seed 21

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 12 x^{2} + 24 e^{3 x} + 24 \cos{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=C x + D - \frac{x^{4}}{4} + \frac{2 e^{3 x}}{3} - \frac{2 \cos{\left(3 x \right)}}{3}$ **correct**
- $y=D - \frac{x^{4}}{4} + \frac{2 e^{3 x}}{3} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x - \frac{x^{4}}{4} + \frac{2 e^{3 x}}{3} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x + D + \frac{x^{4}}{4} - \frac{2 e^{3 x}}{3} + \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x + D - x^{3} + 2 e^{3 x} + 2 \sin{\left(3 x \right)}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 3 x^{2} + 6 e^{3 x} + 6 \cos{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 3 x^{2} + 6 e^{3 x} + 6 \cos{\left(3 x \right)}\right)\,\text{d}x \\  & =((-3)\int \left(x^{2}\right)\,\text{d}x) + ((6)\int \left(e^{3 x}\right)\,\text{d}x) + ((6)\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{x^{3}}{3}\right)) + ((6)\left(\frac{e^{3 x}}{3}\right)) + ((6)\left(\frac{\sin{\left(3 x \right)}}{3}\right))+C \\  & =C - x^{3} + 2 e^{3 x} + 2 \sin{\left(3 x \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - x^{3} + 2 e^{3 x} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{3}\right)\,\text{d}x) + ((2)\int \left(e^{3 x}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{4}}{4}\right)) + ((2)\left(\frac{e^{3 x}}{3}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D - \frac{x^{4}}{4} + \frac{2 e^{3 x}}{3} - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored hard — power_exp_trig — seed 54

Solve the differential equation

$$
3\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 12 x^{3} + 21 e^{3 x} + 6 \sin{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=D - \frac{x^{5}}{5} + \frac{7 e^{3 x}}{9} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=C x + D - x^{4} + \frac{7 e^{3 x}}{3} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x - \frac{x^{5}}{5} + \frac{7 e^{3 x}}{9} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=C x + D - \frac{x^{5}}{5} + \frac{7 e^{3 x}}{9} - \frac{2 \sin{\left(3 x \right)}}{9}$ **correct**
- $y=C x + D + \frac{x^{5}}{5} - \frac{7 e^{3 x}}{9} + \frac{2 \sin{\left(3 x \right)}}{9}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 4 x^{3} + 7 e^{3 x} + 2 \sin{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 4 x^{3} + 7 e^{3 x} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\  & =((-4)\int \left(x^{3}\right)\,\text{d}x) + ((7)\int \left(e^{3 x}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{x^{4}}{4}\right)) + ((7)\left(\frac{e^{3 x}}{3}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+C \\  & =C - x^{4} + \frac{7 e^{3 x}}{3} - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - x^{4} + \frac{7 e^{3 x}}{3} - \frac{2 \cos{\left(3 x \right)}}{3}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{4}\right)\,\text{d}x) + ((\frac{7}{3})\int \left(e^{3 x}\right)\,\text{d}x) + ((- \frac{2}{3})\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{5}}{5}\right)) + ((\frac{7}{3})\left(\frac{e^{3 x}}{3}\right)) + ((- \frac{2}{3})\left(\frac{\sin{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D - \frac{x^{5}}{5} + \frac{7 e^{3 x}}{9} - \frac{2 \sin{\left(3 x \right)}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored hard — two_powers_trig — seed 21

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=24 x^{3} - 12 x^{2} + 24 \cos{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=C x + D + \frac{3 x^{5}}{10} - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$ **correct**
- $y=D + \frac{3 x^{5}}{10} - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x + \frac{3 x^{5}}{10} - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x + D - \frac{3 x^{5}}{10} + \frac{x^{4}}{4} + \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x + D + \frac{3 x^{4}}{2} - x^{3} + 2 \sin{\left(3 x \right)}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6 x^{3} - 3 x^{2} + 6 \cos{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(6 x^{3} - 3 x^{2} + 6 \cos{\left(3 x \right)}\right)\,\text{d}x \\  & =((-3)\int \left(x^{2}\right)\,\text{d}x) + ((6)\int \left(x^{3}\right)\,\text{d}x) + ((6)\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{x^{3}}{3}\right)) + ((6)\left(\frac{x^{4}}{4}\right)) + ((6)\left(\frac{\sin{\left(3 x \right)}}{3}\right))+C \\  & =C + \frac{3 x^{4}}{2} - x^{3} + 2 \sin{\left(3 x \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C + \frac{3 x^{4}}{2} - x^{3} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{3}\right)\,\text{d}x) + ((\frac{3}{2})\int \left(x^{4}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{4}}{4}\right)) + ((\frac{3}{2})\left(\frac{x^{5}}{5}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D + \frac{3 x^{5}}{10} - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored hard — two_powers_trig — seed 54

Solve the differential equation

$$
3\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=21 x^{4} - 12 x^{3} + 6 \sin{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=D + \frac{7 x^{6}}{30} - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=C x + D + \frac{7 x^{5}}{5} - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x + \frac{7 x^{6}}{30} - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=C x + D + \frac{7 x^{6}}{30} - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$ **correct**
- $y=C x + D - \frac{7 x^{6}}{30} + \frac{x^{5}}{5} + \frac{2 \sin{\left(3 x \right)}}{9}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=7 x^{4} - 4 x^{3} + 2 \sin{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(7 x^{4} - 4 x^{3} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\  & =((-4)\int \left(x^{3}\right)\,\text{d}x) + ((7)\int \left(x^{4}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{x^{4}}{4}\right)) + ((7)\left(\frac{x^{5}}{5}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+C \\  & =C + \frac{7 x^{5}}{5} - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C + \frac{7 x^{5}}{5} - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{4}\right)\,\text{d}x) + ((\frac{7}{5})\int \left(x^{5}\right)\,\text{d}x) + ((- \frac{2}{3})\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{5}}{5}\right)) + ((\frac{7}{5})\left(\frac{x^{6}}{6}\right)) + ((- \frac{2}{3})\left(\frac{\sin{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D + \frac{7 x^{6}}{30} - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored hard — power_base_trig — seed 21

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=24 \cdot 2^{x} - 12 x^{2} + 24 \cos{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$ **correct**
- $y=\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + D - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=- \frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D + \frac{x^{4}}{4} + \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}} + C x + D - x^{3} + 2 \sin{\left(3 x \right)}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6 \cdot 2^{x} - 3 x^{2} + 6 \cos{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(6 \cdot 2^{x} - 3 x^{2} + 6 \cos{\left(3 x \right)}\right)\,\text{d}x \\  & =((-3)\int \left(x^{2}\right)\,\text{d}x) + ((6)\int \left(2^{x}\right)\,\text{d}x) + ((6)\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-3)\left(\frac{x^{3}}{3}\right)) + ((6)\left(\frac{2^{x}}{\ln{\left(2 \right)}}\right)) + ((6)\left(\frac{\sin{\left(3 x \right)}}{3}\right))+C \\  & =\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}} + C - x^{3} + 2 \sin{\left(3 x \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}} + C - x^{3} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{3}\right)\,\text{d}x) + ((\frac{6}{\ln{\left(2 \right)}})\int \left(2^{x}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{4}}{4}\right)) + ((\frac{6}{\ln{\left(2 \right)}})\left(\frac{2^{x}}{\ln{\left(2 \right)}}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+Cx+D \\  & =\frac{6 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D - \frac{x^{4}}{4} - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

## Authored hard — power_base_trig — seed 54

Solve the differential equation

$$
3\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=21 \cdot 3^{x} - 12 x^{3} + 6 \sin{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + D - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}} + C x + D - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + C x - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + C x + D - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$ **correct**
- $y=- \frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + C x + D + \frac{x^{5}}{5} + \frac{2 \sin{\left(3 x \right)}}{9}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=7 \cdot 3^{x} - 4 x^{3} + 2 \sin{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(7 \cdot 3^{x} - 4 x^{3} + 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\  & =((-4)\int \left(x^{3}\right)\,\text{d}x) + ((7)\int \left(3^{x}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-4)\left(\frac{x^{4}}{4}\right)) + ((7)\left(\frac{3^{x}}{\ln{\left(3 \right)}}\right)) + ((2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+C \\  & =\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}} + C - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}} + C - x^{4} - \frac{2 \cos{\left(3 x \right)}}{3}\right)\,\text{d}x \\ y & =((-1)\int \left(x^{4}\right)\,\text{d}x) + ((\frac{7}{\ln{\left(3 \right)}})\int \left(3^{x}\right)\,\text{d}x) + ((- \frac{2}{3})\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-1)\left(\frac{x^{5}}{5}\right)) + ((\frac{7}{\ln{\left(3 \right)}})\left(\frac{3^{x}}{\ln{\left(3 \right)}}\right)) + ((- \frac{2}{3})\left(\frac{\sin{\left(3 x \right)}}{3}\right))+Cx+D \\  & =\frac{7 \cdot 3^{x}}{\ln{\left(3 \right)}^{2}} + C x + D - \frac{x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$
