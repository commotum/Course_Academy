Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6 e^{- \frac{x}{2}}.
$$

Field 1 (selection)
- $y=C x + D + 24 e^{- \frac{x}{2}}$ **correct**
- $y=D + 24 e^{- \frac{x}{2}}$
- $y=C x + 24 e^{- \frac{x}{2}}$
- $y=C x + D - 24 e^{- \frac{x}{2}}$
- $y=C x + D - 12 e^{- \frac{x}{2}}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(6 e^{- \frac{x}{2}}\right)\,\text{d}x \\  & =((6)\int \left(e^{- \frac{x}{2}}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((6)\left(- 2 e^{- \frac{x}{2}}\right))+C \\  & =C - 12 e^{- \frac{x}{2}}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - 12 e^{- \frac{x}{2}}\right)\,\text{d}x \\ y & =((-12)\int \left(e^{- \frac{x}{2}}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-12)\left(- 2 e^{- \frac{x}{2}}\right))+Cx+D \\  & =C x + D + 24 e^{- \frac{x}{2}}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

---

Solve the differential equation

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- e^{- 2 x}.
$$

Field 1 (selection)
- $y=C x + D - \frac{e^{- 2 x}}{4}$ **correct**
- $y=C x - \frac{e^{- 2 x}}{4}$
- $y=D - \frac{e^{- 2 x}}{4}$
- $y=C x + D + \frac{e^{- 2 x}}{4}$
- $y=C x + D + \frac{e^{- 2 x}}{2}$

Integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- e^{- 2 x}\right)\,\text{d}x \\  & =((-1)\int \left(e^{- 2 x}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-1)\left(- \frac{e^{- 2 x}}{2}\right))+C \\  & =C + \frac{e^{- 2 x}}{2}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C + \frac{e^{- 2 x}}{2}\right)\,\text{d}x \\ y & =((\frac{1}{2})\int \left(e^{- 2 x}\right)\,\text{d}x)+C\int \text{d}x \\  & =((\frac{1}{2})\left(- \frac{e^{- 2 x}}{2}\right))+Cx+D \\  & =C x + D - \frac{e^{- 2 x}}{4}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

---

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=24 x^{3} - 8 \sin{\left(\frac{x}{2} \right)} + 24 e^{- \frac{x}{2}}.
$$

Field 1 (selection)
- $y=C x + D + \frac{3 x^{5}}{10} + 8 \sin{\left(\frac{x}{2} \right)} + 24 e^{- \frac{x}{2}}$ **correct**
- $y=D + \frac{3 x^{5}}{10} + 8 \sin{\left(\frac{x}{2} \right)} + 24 e^{- \frac{x}{2}}$
- $y=C x + \frac{3 x^{5}}{10} + 8 \sin{\left(\frac{x}{2} \right)} + 24 e^{- \frac{x}{2}}$
- $y=C x + D - \frac{3 x^{5}}{10} - 8 \sin{\left(\frac{x}{2} \right)} - 24 e^{- \frac{x}{2}}$
- $y=C x + D + \frac{3 x^{4}}{2} + 4 \cos{\left(\frac{x}{2} \right)} - 12 e^{- \frac{x}{2}}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=6 x^{3} - 2 \sin{\left(\frac{x}{2} \right)} + 6 e^{- \frac{x}{2}}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(6 x^{3} - 2 \sin{\left(\frac{x}{2} \right)} + 6 e^{- \frac{x}{2}}\right)\,\text{d}x \\  & =((6)\int \left(x^{3}\right)\,\text{d}x) + ((6)\int \left(e^{- \frac{x}{2}}\right)\,\text{d}x) + ((-2)\int \left(\sin{\left(\frac{x}{2} \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((6)\left(\frac{x^{4}}{4}\right)) + ((6)\left(- 2 e^{- \frac{x}{2}}\right)) + ((-2)\left(- 2 \cos{\left(\frac{x}{2} \right)}\right))+C \\  & =C + \frac{3 x^{4}}{2} + 4 \cos{\left(\frac{x}{2} \right)} - 12 e^{- \frac{x}{2}}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C + \frac{3 x^{4}}{2} + 4 \cos{\left(\frac{x}{2} \right)} - 12 e^{- \frac{x}{2}}\right)\,\text{d}x \\ y & =((\frac{3}{2})\int \left(x^{4}\right)\,\text{d}x) + ((-12)\int \left(e^{- \frac{x}{2}}\right)\,\text{d}x) + ((4)\int \left(\cos{\left(\frac{x}{2} \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((\frac{3}{2})\left(\frac{x^{5}}{5}\right)) + ((-12)\left(- 2 e^{- \frac{x}{2}}\right)) + ((4)\left(2 \sin{\left(\frac{x}{2} \right)}\right))+Cx+D \\  & =C x + D + \frac{3 x^{5}}{10} + 8 \sin{\left(\frac{x}{2} \right)} + 24 e^{- \frac{x}{2}}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

---

Solve the differential equation

$$
2\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 2 x + 14 \cos{\left(2 x \right)} - 16 e^{- 2 x}.
$$

Field 1 (selection)
- $y=C x + D - \frac{x^{3}}{6} - \frac{7 \cos{\left(2 x \right)}}{4} - 2 e^{- 2 x}$ **correct**
- $y=C x - \frac{x^{3}}{6} - \frac{7 \cos{\left(2 x \right)}}{4} - 2 e^{- 2 x}$
- $y=D - \frac{x^{3}}{6} - \frac{7 \cos{\left(2 x \right)}}{4} - 2 e^{- 2 x}$
- $y=C x + D + \frac{x^{3}}{6} + \frac{7 \cos{\left(2 x \right)}}{4} + 2 e^{- 2 x}$
- $y=C x + D - \frac{x^{2}}{2} + \frac{7 \sin{\left(2 x \right)}}{2} + 4 e^{- 2 x}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- x + 7 \cos{\left(2 x \right)} - 8 e^{- 2 x}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- x + 7 \cos{\left(2 x \right)} - 8 e^{- 2 x}\right)\,\text{d}x \\  & =((-1)\int \left(x\right)\,\text{d}x) + ((-8)\int \left(e^{- 2 x}\right)\,\text{d}x) + ((7)\int \left(\cos{\left(2 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-1)\left(\frac{x^{2}}{2}\right)) + ((-8)\left(- \frac{e^{- 2 x}}{2}\right)) + ((7)\left(\frac{\sin{\left(2 x \right)}}{2}\right))+C \\  & =C - \frac{x^{2}}{2} + \frac{7 \sin{\left(2 x \right)}}{2} + 4 e^{- 2 x}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - \frac{x^{2}}{2} + \frac{7 \sin{\left(2 x \right)}}{2} + 4 e^{- 2 x}\right)\,\text{d}x \\ y & =((- \frac{1}{2})\int \left(x^{2}\right)\,\text{d}x) + ((4)\int \left(e^{- 2 x}\right)\,\text{d}x) + ((\frac{7}{2})\int \left(\sin{\left(2 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((- \frac{1}{2})\left(\frac{x^{3}}{3}\right)) + ((4)\left(- \frac{e^{- 2 x}}{2}\right)) + ((\frac{7}{2})\left(- \frac{\cos{\left(2 x \right)}}{2}\right))+Cx+D \\  & =C x + D - \frac{x^{3}}{6} - \frac{7 \cos{\left(2 x \right)}}{4} - 2 e^{- 2 x}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

---

Solve the differential equation

$$
2\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 16 x^{4} - 12 x^{3} + 4 \cos{\left(2 x \right)}.
$$

Field 1 (selection)
- $y=C x + D + \frac{4 x^{6}}{15} + \frac{3 x^{5}}{10} + \frac{\cos{\left(2 x \right)}}{2}$
- $y=C x - \frac{4 x^{6}}{15} - \frac{3 x^{5}}{10} - \frac{\cos{\left(2 x \right)}}{2}$
- $y=C x + D - \frac{8 x^{5}}{5} - \frac{3 x^{4}}{2} + \sin{\left(2 x \right)}$
- $y=C x + D - \frac{4 x^{6}}{15} - \frac{3 x^{5}}{10} - \frac{\cos{\left(2 x \right)}}{2}$ **correct**
- $y=D - \frac{4 x^{6}}{15} - \frac{3 x^{5}}{10} - \frac{\cos{\left(2 x \right)}}{2}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 8 x^{4} - 6 x^{3} + 2 \cos{\left(2 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 8 x^{4} - 6 x^{3} + 2 \cos{\left(2 x \right)}\right)\,\text{d}x \\  & =((-6)\int \left(x^{3}\right)\,\text{d}x) + ((-8)\int \left(x^{4}\right)\,\text{d}x) + ((2)\int \left(\cos{\left(2 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-6)\left(\frac{x^{4}}{4}\right)) + ((-8)\left(\frac{x^{5}}{5}\right)) + ((2)\left(\frac{\sin{\left(2 x \right)}}{2}\right))+C \\  & =C - \frac{8 x^{5}}{5} - \frac{3 x^{4}}{2} + \sin{\left(2 x \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - \frac{8 x^{5}}{5} - \frac{3 x^{4}}{2} + \sin{\left(2 x \right)}\right)\,\text{d}x \\ y & =((- \frac{3}{2})\int \left(x^{4}\right)\,\text{d}x) + ((- \frac{8}{5})\int \left(x^{5}\right)\,\text{d}x) + ((1)\int \left(\sin{\left(2 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((- \frac{3}{2})\left(\frac{x^{5}}{5}\right)) + ((- \frac{8}{5})\left(\frac{x^{6}}{6}\right)) + ((1)\left(- \frac{\cos{\left(2 x \right)}}{2}\right))+Cx+D \\  & =C x + D - \frac{4 x^{6}}{15} - \frac{3 x^{5}}{10} - \frac{\cos{\left(2 x \right)}}{2}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

---

Solve the differential equation

$$
4\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 12 \cdot 2^{x} + 20 x + 8 \sin{\left(\frac{x}{2} \right)}.
$$

Field 1 (selection)
- $y=- \frac{3 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + D + \frac{5 x^{3}}{6} - 8 \sin{\left(\frac{x}{2} \right)}$
- $y=- \frac{3 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D + \frac{5 x^{3}}{6} - 8 \sin{\left(\frac{x}{2} \right)}$ **correct**
- $y=- \frac{3 \cdot 2^{x}}{\ln{\left(2 \right)}} + C x + D + \frac{5 x^{2}}{2} - 4 \cos{\left(\frac{x}{2} \right)}$
- $y=\frac{3 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D - \frac{5 x^{3}}{6} + 8 \sin{\left(\frac{x}{2} \right)}$
- $y=- \frac{3 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + \frac{5 x^{3}}{6} - 8 \sin{\left(\frac{x}{2} \right)}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 3 \cdot 2^{x} + 5 x + 2 \sin{\left(\frac{x}{2} \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 3 \cdot 2^{x} + 5 x + 2 \sin{\left(\frac{x}{2} \right)}\right)\,\text{d}x \\  & =((5)\int \left(x\right)\,\text{d}x) + ((-3)\int \left(2^{x}\right)\,\text{d}x) + ((2)\int \left(\sin{\left(\frac{x}{2} \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((5)\left(\frac{x^{2}}{2}\right)) + ((-3)\left(\frac{2^{x}}{\ln{\left(2 \right)}}\right)) + ((2)\left(- 2 \cos{\left(\frac{x}{2} \right)}\right))+C \\  & =- \frac{3 \cdot 2^{x}}{\ln{\left(2 \right)}} + C + \frac{5 x^{2}}{2} - 4 \cos{\left(\frac{x}{2} \right)}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(- \frac{3 \cdot 2^{x}}{\ln{\left(2 \right)}} + C + \frac{5 x^{2}}{2} - 4 \cos{\left(\frac{x}{2} \right)}\right)\,\text{d}x \\ y & =((\frac{5}{2})\int \left(x^{2}\right)\,\text{d}x) + ((- \frac{3}{\ln{\left(2 \right)}})\int \left(2^{x}\right)\,\text{d}x) + ((-4)\int \left(\cos{\left(\frac{x}{2} \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((\frac{5}{2})\left(\frac{x^{3}}{3}\right)) + ((- \frac{3}{\ln{\left(2 \right)}})\left(\frac{2^{x}}{\ln{\left(2 \right)}}\right)) + ((-4)\left(2 \sin{\left(\frac{x}{2} \right)}\right))+Cx+D \\  & =- \frac{3 \cdot 2^{x}}{\ln{\left(2 \right)}^{2}} + C x + D + \frac{5 x^{3}}{6} - 8 \sin{\left(\frac{x}{2} \right)}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$

---

Solve the differential equation

$$
3\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 6 x^{4} - 24 x^{3} - 6 \sin{\left(3 x \right)}.
$$

Field 1 (selection)
- $y=C x + D - \frac{x^{6}}{15} - \frac{2 x^{5}}{5} + \frac{2 \sin{\left(3 x \right)}}{9}$ **correct**
- $y=D - \frac{x^{6}}{15} - \frac{2 x^{5}}{5} + \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=C x + D + \frac{x^{6}}{15} + \frac{2 x^{5}}{5} - \frac{2 \sin{\left(3 x \right)}}{9}$
- $y=C x + D - \frac{2 x^{5}}{5} - 2 x^{4} + \frac{2 \cos{\left(3 x \right)}}{3}$
- $y=C x - \frac{x^{6}}{15} - \frac{2 x^{5}}{5} + \frac{2 \sin{\left(3 x \right)}}{9}$

First, we rearrange the equation to give

$$
\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}=- 2 x^{4} - 8 x^{3} - 2 \sin{\left(3 x \right)}.
$$

Now, integrating the equation once, we get

$$
\begin{aligned}\int \frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}\,\text{d}x & =\int \left(- 2 x^{4} - 8 x^{3} - 2 \sin{\left(3 x \right)}\right)\,\text{d}x \\  & =((-8)\int \left(x^{3}\right)\,\text{d}x) + ((-2)\int \left(x^{4}\right)\,\text{d}x) + ((-2)\int \left(\sin{\left(3 x \right)}\right)\,\text{d}x) \\ \frac{\text{d}y}{\text{d}x} & =((-8)\left(\frac{x^{4}}{4}\right)) + ((-2)\left(\frac{x^{5}}{5}\right)) + ((-2)\left(- \frac{\cos{\left(3 x \right)}}{3}\right))+C \\  & =C - \frac{2 x^{5}}{5} - 2 x^{4} + \frac{2 \cos{\left(3 x \right)}}{3}.\end{aligned}
$$

Integrating a second time, we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \left(C - \frac{2 x^{5}}{5} - 2 x^{4} + \frac{2 \cos{\left(3 x \right)}}{3}\right)\,\text{d}x \\ y & =((-2)\int \left(x^{4}\right)\,\text{d}x) + ((- \frac{2}{5})\int \left(x^{5}\right)\,\text{d}x) + ((\frac{2}{3})\int \left(\cos{\left(3 x \right)}\right)\,\text{d}x)+C\int \text{d}x \\  & =((-2)\left(\frac{x^{5}}{5}\right)) + ((- \frac{2}{5})\left(\frac{x^{6}}{6}\right)) + ((\frac{2}{3})\left(\frac{\sin{\left(3 x \right)}}{3}\right))+Cx+D \\  & =C x + D - \frac{x^{6}}{15} - \frac{2 x^{5}}{5} + \frac{2 \sin{\left(3 x \right)}}{9}.\end{aligned}
$$

Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$
