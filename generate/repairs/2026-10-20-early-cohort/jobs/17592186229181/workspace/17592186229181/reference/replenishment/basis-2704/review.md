## GENERATED VARIANT: amount
A fish hatchery tank initially holds $560\,\text{L}$ of water containing $16\,\text{kg}$ of dissolved salt.
A feed solution containing $0.06\,\text{kg/L}$ of the salt is pumped into the tank at a rate of $40\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $40\,\text{L/min}.$
Find, rounded to two decimal places, the amount of salt in the tank $2$ minutes after pumping begins.

- $18.34\,\text{kg}$ [correct]
- $48.86\,\text{kg}$
- $19.53\,\text{kg}$
- $16.20\,\text{kg}$
- $14.19\,\text{kg}$

Let $Q$ be the amount of salt in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which salt enters the tank minus the rate at which salt leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enters the tank.

Note that a feed solution containing $0.06\,\text{kg/L}$ of the salt enters the tank at a rate of $40\,\text{L/min}.$ So, the rate at which the *salt* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.06\,\frac{\text{kg}}{\text{L}})\cdot (40\,\frac{\text{L}}{\text{min}}) \\  & =(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (40\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =2.4\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $560\,\text{L}.$ Then, since $Q$ is the amount of salt in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{560}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $40\,\text{L/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(40\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{560}\,\frac{\text{kg}}{\text{L}}) \\  & =(40\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{560}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{40Q}{560}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{14}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =2.4-\frac{Q}{14}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{14}Q=2.4.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{14}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/14},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{14}\alpha =2.4\,⟹\,\alpha =33.6.
$$

Therefore, the particular solution is ${Q}_{p}(t)=33.6.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/14}+33.6.
$$

We're told that the tank initially contains $16\,\text{kg}$ of dissolved salt. So, we can apply the initial condition $Q(0)=16,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =16 \\ A{e}^{-0/14}+33.6 & =16 \\ A & =-17.6\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=33.6-17.6{e}^{-t/14}
$$

Finally,  the amount of salt in the tank $2$ minutes after pumping begins is

$$
Q(2)=33.6-17.6{e}^{-2/14}≈18.34\,\text{kg},
$$

rounded to two decimal places.

---

## GENERATED VARIANT: amount
A dye vat initially holds $900\,\text{L}$ of liquid containing $15\,\text{kg}$ of dissolved dye.
A feed solution containing $0.06\,\text{kg/L}$ of the dye is pumped into the vat at a rate of $15\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$
Find, rounded to two decimal places, the amount of dye in the vat $5$ minutes after pumping begins.

- $18.80\,\text{kg}$
- $13.87\,\text{kg}$
- $16.84\,\text{kg}$
- $18.12\,\text{kg}$ [correct]
- $89.88\,\text{kg}$

Let $Q$ be the amount of dye in the vat at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which dye enters the vat minus the rate at which dye leaves the vat.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which dye enters the vat.

Note that a feed solution containing $0.06\,\text{kg/L}$ of the dye enters the vat at a rate of $15\,\text{L/min}.$ So, the rate at which the *dye* enters the vat is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.06\,\frac{\text{kg}}{\text{L}})\cdot (15\,\frac{\text{L}}{\text{min}}) \\  & =(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (15\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.9\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which dye exits the vat.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the vat remains $900\,\text{L}.$ Then, since $Q$ is the amount of dye in the vat, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{900}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $15\,\text{L/min},$ *dye* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(15\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{900}\,\frac{\text{kg}}{\text{L}}) \\  & =(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{900}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{15Q}{900}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{60}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.9-\frac{Q}{60}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{60}Q=0.9.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{60}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/60},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{60}\alpha =0.9\,⟹\,\alpha =54.
$$

Therefore, the particular solution is ${Q}_{p}(t)=54.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/60}+54.
$$

We're told that the vat initially contains $15\,\text{kg}$ of dissolved dye. So, we can apply the initial condition $Q(0)=15,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =15 \\ A{e}^{-0/60}+54 & =15 \\ A & =-39\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=54-39{e}^{-t/60}
$$

Finally,  the amount of dye in the vat $5$ minutes after pumping begins is

$$
Q(5)=54-39{e}^{-5/60}≈18.12\,\text{kg},
$$

rounded to two decimal places.

---

## GENERATED VARIANT: amount_unit_conversion
A fish hatchery tank initially holds $560\,\text{L}$ of water containing $16\,\text{kg}$ of dissolved salt.
A feed solution containing $60\,\text{g/L}$ of the salt is pumped into the tank at a rate of $40\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $40\,\text{L/min}.$
Find, rounded to two decimal places, the amount of salt in the tank $2$ minutes after pumping begins.

- $18.34\,\text{kg}$ [correct]
- $48.86\,\text{kg}$
- $19.53\,\text{kg}$
- $16.20\,\text{kg}$
- $14.19\,\text{kg}$

The feed concentration must use kilograms: $60\,\text{g/L}\cdot\frac{1\,\text{kg}}{1000\,\text{g}}=0.06\,\text{kg/L}.$

Let $Q$ be the amount of salt in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which salt enters the tank minus the rate at which salt leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enters the tank.

Note that a feed solution containing $0.06\,\text{kg/L}$ of the salt enters the tank at a rate of $40\,\text{L/min}.$ So, the rate at which the *salt* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.06\,\frac{\text{kg}}{\text{L}})\cdot (40\,\frac{\text{L}}{\text{min}}) \\  & =(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (40\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =2.4\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $560\,\text{L}.$ Then, since $Q$ is the amount of salt in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{560}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $40\,\text{L/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(40\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{560}\,\frac{\text{kg}}{\text{L}}) \\  & =(40\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{560}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{40Q}{560}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{14}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =2.4-\frac{Q}{14}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{14}Q=2.4.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{14}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/14},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{14}\alpha =2.4\,⟹\,\alpha =33.6.
$$

Therefore, the particular solution is ${Q}_{p}(t)=33.6.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/14}+33.6.
$$

We're told that the tank initially contains $16\,\text{kg}$ of dissolved salt. So, we can apply the initial condition $Q(0)=16,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =16 \\ A{e}^{-0/14}+33.6 & =16 \\ A & =-17.6\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=33.6-17.6{e}^{-t/14}
$$

Finally,  the amount of salt in the tank $2$ minutes after pumping begins is

$$
Q(2)=33.6-17.6{e}^{-2/14}≈18.34\,\text{kg},
$$

rounded to two decimal places.

---

## GENERATED VARIANT: amount_unit_conversion
A dye vat initially holds $900\,\text{L}$ of liquid containing $15\,\text{kg}$ of dissolved dye.
A feed solution containing $60\,\text{g/L}$ of the dye is pumped into the vat at a rate of $15\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$
Find, rounded to two decimal places, the amount of dye in the vat $5$ minutes after pumping begins.

- $18.80\,\text{kg}$
- $13.87\,\text{kg}$
- $16.84\,\text{kg}$
- $18.12\,\text{kg}$ [correct]
- $89.88\,\text{kg}$

The feed concentration must use kilograms: $60\,\text{g/L}\cdot\frac{1\,\text{kg}}{1000\,\text{g}}=0.06\,\text{kg/L}.$

Let $Q$ be the amount of dye in the vat at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which dye enters the vat minus the rate at which dye leaves the vat.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which dye enters the vat.

Note that a feed solution containing $0.06\,\text{kg/L}$ of the dye enters the vat at a rate of $15\,\text{L/min}.$ So, the rate at which the *dye* enters the vat is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.06\,\frac{\text{kg}}{\text{L}})\cdot (15\,\frac{\text{L}}{\text{min}}) \\  & =(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (15\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.9\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which dye exits the vat.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the vat remains $900\,\text{L}.$ Then, since $Q$ is the amount of dye in the vat, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{900}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $15\,\text{L/min},$ *dye* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(15\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{900}\,\frac{\text{kg}}{\text{L}}) \\  & =(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{900}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{15Q}{900}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{60}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.9-\frac{Q}{60}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{60}Q=0.9.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{60}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/60},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{60}\alpha =0.9\,⟹\,\alpha =54.
$$

Therefore, the particular solution is ${Q}_{p}(t)=54.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/60}+54.
$$

We're told that the vat initially contains $15\,\text{kg}$ of dissolved dye. So, we can apply the initial condition $Q(0)=15,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =15 \\ A{e}^{-0/60}+54 & =15 \\ A & =-39\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=54-39{e}^{-t/60}
$$

Finally,  the amount of dye in the vat $5$ minutes after pumping begins is

$$
Q(5)=54-39{e}^{-5/60}≈18.12\,\text{kg},
$$

rounded to two decimal places.

---

## GENERATED VARIANT: amount_unit_conversion
A coolant tank initially holds $625\,\text{L}$ of liquid containing $13\,\text{kg}$ of dissolved additive.
A feed solution containing $30\,\text{g/L}$ of the additive is pumped into the tank at a rate of $25\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $25\,\text{L/min}.$
Find, rounded to two decimal places, the amount of additive in the tank $6$ minutes after pumping begins.

- $14.23\,\text{kg}$ [correct]
- $15.77\,\text{kg}$
- $11.62\,\text{kg}$
- $10.39\,\text{kg}$
- $23.27\,\text{kg}$

The feed concentration must use kilograms: $30\,\text{g/L}\cdot\frac{1\,\text{kg}}{1000\,\text{g}}=0.03\,\text{kg/L}.$

Let $Q$ be the amount of additive in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which additive enters the tank minus the rate at which additive leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additive enters the tank.

Note that a feed solution containing $0.03\,\text{kg/L}$ of the additive enters the tank at a rate of $25\,\text{L/min}.$ So, the rate at which the *additive* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.03\,\frac{\text{kg}}{\text{L}})\cdot (25\,\frac{\text{L}}{\text{min}}) \\  & =(0.03\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (25\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.75\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additive exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $625\,\text{L}.$ Then, since $Q$ is the amount of additive in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{625}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $25\,\text{L/min},$ *additive* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(25\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{625}\,\frac{\text{kg}}{\text{L}}) \\  & =(25\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{625}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{25Q}{625}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{25}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.75-\frac{Q}{25}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{25}Q=0.75.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{25}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/25},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{25}\alpha =0.75\,⟹\,\alpha =18.75.
$$

Therefore, the particular solution is ${Q}_{p}(t)=18.75.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/25}+18.75.
$$

We're told that the tank initially contains $13\,\text{kg}$ of dissolved additive. So, we can apply the initial condition $Q(0)=13,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =13 \\ A{e}^{-0/25}+18.75 & =13 \\ A & =-5.75\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=18.75-5.75{e}^{-t/25}
$$

Finally,  the amount of additive in the tank $6$ minutes after pumping begins is

$$
Q(6)=18.75-5.75{e}^{-6/25}≈14.23\,\text{kg},
$$

rounded to two decimal places.

---

## GENERATED VARIANT: amount_unit_conversion
A coolant tank initially holds $720\,\text{L}$ of liquid containing $24\,\text{kg}$ of dissolved additive.
A feed solution containing $30\,\text{g/L}$ of the additive is pumped into the tank at a rate of $30\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $30\,\text{L/min}.$
Find, rounded to two decimal places, the amount of additive in the tank $3$ minutes after pumping begins.

- $21.08\,\text{kg}$
- $21.29\,\text{kg}$
- $23.72\,\text{kg}$ [correct]
- $19.48\,\text{kg}$
- $25.16\,\text{kg}$

The feed concentration must use kilograms: $30\,\text{g/L}\cdot\frac{1\,\text{kg}}{1000\,\text{g}}=0.03\,\text{kg/L}.$

Let $Q$ be the amount of additive in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which additive enters the tank minus the rate at which additives leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additive enters the tank.

Note that a feed solution containing $0.03\,\text{kg/L}$ of the additive enters the tank at a rate of $30\,\text{L/min}.$ So, the rate at which the *additive* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.03\,\frac{\text{kg}}{\text{L}})\cdot (30\,\frac{\text{L}}{\text{min}}) \\  & =(0.03\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (30\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.9\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additive exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $720\,\text{L}.$ Then, since $Q$ is the amount of additive in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{720}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $30\,\text{L/min},$ *additive* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(30\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{720}\,\frac{\text{kg}}{\text{L}}) \\  & =(30\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{720}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{30Q}{720}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{24}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.9-\frac{Q}{24}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{24}Q=\frac{9}{10}.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{24}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/24},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{24}\alpha =\frac{9}{10}\,⟹\,\alpha =21.6.
$$

Therefore, the particular solution is ${Q}_{p}(t)=21.6.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/24}+21.6.
$$

We're told that the tank initially contains $24\,\text{kg}$ of dissolved additive. So, we can apply the initial condition $Q(0)=24,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =24 \\ A{e}^{-0/24}+21.6 & =24 \\ A & =2.4\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=21.6+2.4{e}^{-t/24}
$$

Finally,  the amount of additive in the tank $3$ minutes after pumping begins is

$$
Q(3)=21.6+2.4{e}^{-3/24}≈23.72\,\text{kg},
$$

rounded to two decimal places.

---

## GENERATED VARIANT: amount_unit_conversion
A dye vat initially holds $900\,\text{L}$ of liquid containing $25\,\text{kg}$ of dissolved dye.
A feed solution containing $40\,\text{g/L}$ of the dye is pumped into the vat at a rate of $15\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$
Find, rounded to two decimal places, the amount of dye in the vat $6$ minutes after pumping begins.

- $26.05\,\text{kg}$ [correct]
- $22.68\,\text{kg}$
- $45.95\,\text{kg}$
- $27.29\,\text{kg}$
- $23.73\,\text{kg}$

The feed concentration must use kilograms: $40\,\text{g/L}\cdot\frac{1\,\text{kg}}{1000\,\text{g}}=0.04\,\text{kg/L}.$

Let $Q$ be the amount of dye in the vat at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which dye enters the vat minus the rate at which dye leaves the vat.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which dye enters the vat.

Note that a feed solution containing $0.04\,\text{kg/L}$ of the dye enters the vat at a rate of $15\,\text{L/min}.$ So, the rate at which the *dye* enters the vat is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.04\,\frac{\text{kg}}{\text{L}})\cdot (15\,\frac{\text{L}}{\text{min}}) \\  & =(0.04\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (15\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.6\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which dye exits the vat.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the vat remains $900\,\text{L}.$ Then, since $Q$ is the amount of dye in the vat, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{900}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $15\,\text{L/min},$ *dye* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(15\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{900}\,\frac{\text{kg}}{\text{L}}) \\  & =(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{900}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{15Q}{900}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{60}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.6-\frac{Q}{60}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{60}Q=0.6.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{60}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/60},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{60}\alpha =0.6\,⟹\,\alpha =36.
$$

Therefore, the particular solution is ${Q}_{p}(t)=36.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/60}+36.
$$

We're told that the vat initially contains $25\,\text{kg}$ of dissolved dye. So, we can apply the initial condition $Q(0)=25,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =25 \\ A{e}^{-0/60}+36 & =25 \\ A & =-11\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=36-11{e}^{-t/60}
$$

Finally,  the amount of dye in the vat $6$ minutes after pumping begins is

$$
Q(6)=36-11{e}^{-6/60}≈26.05\,\text{kg},
$$

rounded to two decimal places.
