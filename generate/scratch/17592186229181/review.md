## ORIGINAL PROFILE REPLAY: source_17592186229724
A wastewater basin initially holds $750L$ of water containing $6kg$ of dissolved pollutant.
A solution containing $0.03kg/L$ of dissolved pollutant is pumped into the basin at a rate of $30L/min$, while the completely mixed liquid is drained out at a rate of $30L/min$. Which expression gives the amount of pollutant $Q(t)$, in kilograms, in the basin $t$ minutes after pumping begins?

- $Q(t) = 22.5 - 16.5e^{t/25}$
- $Q(t) = 22.5 - 16.5e^{-t/20}$
- $Q(t) = 22.5 - 16.5e^{-t/25}$
- $Q(t) = 22.5 + 16.5e^{-t/25}$
- $Q(t) = 6 - 22.5e^{-t/25}$

[Original worked solution omitted.]

**Evidence only; ineligible for learning.**

## ORIGINAL PROFILE REPLAY: source_17592186229725
A fish hatchery tank initially holds $900L$ of water containing $10kg$ of dissolved salt.
A feed solution containing $0.02kg/L$ of the salt is pumped into the tank at a rate of $30L/min$, while the completely mixed liquid is drained out at a rate of $30L/min$.
Find, rounded to two decimal places, the amount of salt in the tank $6$ minutes after pumping begins.

- $12.11kg$
- $11.02kg$
- $11.83kg$
- $10.76kg$
- $11.45kg$

[Original worked solution omitted.]

**Evidence only; ineligible for learning.**

## ORIGINAL PROFILE REPLAY: source_17592186377242
A nutrient-mixing tank initially holds $720\,\text{L}$ of solution containing $3\,\text{kg}$ of dissolved supplement.
A feed solution containing $0.03\,\text{kg/L}$ of the supplement is pumped into the tank at a rate of $12\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $12\,\text{L/min}.$
Find, rounded to two decimal places, the amount of supplement in the tank $5$ minutes after pumping begins.

- $4.49\,\text{kg}$ [correct]
- $3.96\,\text{kg}$
- $4.17\,\text{kg}$
- $4.83\,\text{kg}$
- $5.02\,\text{kg}$

Let $Q$ be the amount of supplement in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which supplements enter the tank minus the rate at which supplements leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which supplements enter the tank.

Note that a feed solution containing $0.03\,\text{kg/L}$ of the supplement enters the tank at a rate of $12\,\text{L/min}.$ So, the rate at which the *supplement* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.03\,\frac{\text{kg}}{\text{L}})\cdot (12\,\frac{\text{L}}{\text{min}}) \\  & =(0.03\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (12\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.36\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which supplements exit the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $720\,\text{L}.$ Then, since $Q$ is the amount of supplement in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{720}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $12\,\text{L/min},$ *supplement* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(12\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{720}\,\frac{\text{kg}}{\text{L}}) \\  & =(12\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{720}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{12Q}{720}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{60}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.36-\frac{Q}{60}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{60}Q=0.36.
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
0+\frac{1}{60}\alpha =0.36\,⟹\,\alpha =21.6.
$$

Therefore, the particular solution is ${Q}_{p}(t)=21.6.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/60}+21.6.
$$

We're told that the tank initially contains $3\,\text{kg}$ of dissolved supplement. So, we can apply the initial condition $Q(0)=3,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =3 \\ A{e}^{-0/60}+21.6 & =3 \\ A & =-18.6\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=21.6-18.6{e}^{-t/60}
$$

Finally,  the amount of supplement in the tank $5$ minutes after pumping begins is

$$
Q(5)=21.6-18.6{e}^{-5/60}≈4.49\,\text{kg},
$$

rounded to two decimal places.

**Evidence only; ineligible for learning.**

## ORIGINAL PROFILE REPLAY: source_17592186377256
A coolant tank initially holds $500\,\text{L}$ of liquid containing $7\,\text{kg}$ of dissolved anti-corrosion additive.
A solution containing $0.02\,\text{kg/L}$ of dissolved additive is pumped into the tank at a rate of $25\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $25\,\text{L/min}.$ Which expression gives the amount of additive $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins?

- $Q(t)=10-3{e}^{-t/20}$ [correct]
- $Q(t)=8-{e}^{-t/20}$
- $Q(t)=12-5{e}^{t/20}$
- $Q(t)=9-2{e}^{-t/20}$
- $Q(t)=-9+16{e}^{-t/20}$

Let $Q$ be the amount of additive in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which additives enter the tank minus the rate at which additives leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additives enter the tank.

Note that a feed solution containing $0.02\,\text{kg/L}$ of the additive enters the tank at a rate of $25\,\text{L/min}.$ So, the rate at which the *additive* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.02\,\frac{\text{kg}}{\text{L}})\cdot (25\,\frac{\text{L}}{\text{min}}) \\  & =(0.02\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (25\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.5\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additives exit the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $500\,\text{L}.$ Then, since $Q$ is the amount of additive in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{500}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $25\,\text{L/min},$ *additive* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(25\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{500}\,\frac{\text{kg}}{\text{L}}) \\  & =(25\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{500}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{25Q}{500}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{20}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.5-\frac{Q}{20}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{20}Q=\frac{1}{2}.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{20}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/20},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{20}\alpha =\frac{1}{2}\,⟹\,\alpha =10.
$$

Therefore, the particular solution is ${Q}_{p}(t)=10.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/20}+10.
$$

We're told that the tank initially contains $7\,\text{kg}$ of dissolved additive. So, we can apply the initial condition $Q(0)=7,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =7 \\ A{e}^{-0/20}+10 & =7 \\ A & =-3\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=10-3{e}^{-t/20}.
$$

**Evidence only; ineligible for learning.**

## ORIGINAL PROFILE REPLAY: source_17592186377263
A storage tank initially holds $400\,\text{L}$ of liquid containing $3\,\text{kg}$ of dissolved disinfectant.
A solution containing $0.03\,\text{kg/L}$ of dissolved disinfectant is pumped into the tank at a rate of $20\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $20\,\text{L/min}.$ Which expression gives the amount of disinfectant $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins?

- $Q(t)=-1+4{e}^{t/20}$
- $Q(t)=12-9{e}^{-t/20}$ [correct]
- $Q(t)=10-7{e}^{t/20}$
- $Q(t)=-9+12{e}^{-t/20}$
- $Q(t)=4-{e}^{-t/20}$

Let $Q$ be the amount of disinfectant in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which disinfectant enters the tank minus the rate at which disinfectant leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additives enter the tank.

Note that a feed solution containing $0.03\,\text{kg/L}$ of the disinfectant enters the tank at a rate of $20\,\text{L/min}.$ So, the rate at which the *disinfectant* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.03\,\frac{\text{kg}}{\text{L}})\cdot (20\,\frac{\text{L}}{\text{min}}) \\  & =(0.03\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (20\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.6\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additives exit the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $400\,\text{L}.$ Then, since $Q$ is the amount of disinfectant in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{400}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $20\,\text{L/min},$ *disinfectant* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{400}\,\frac{\text{kg}}{\text{L}}) \\  & =(20\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{400}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{20Q}{400}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{20}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.6-\frac{Q}{20}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{20}Q=0.6.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{20}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/20},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{20}\alpha =0.6\,⟹\,\alpha =12.
$$

Therefore, the particular solution is ${Q}_{p}(t)=12.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/20}+12.
$$

We're told that the tank initially contains $3\,\text{kg}$ of dissolved disinfectant. So, we can apply the initial condition $Q(0)=3,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =3 \\ A{e}^{-0/20}+12 & =3 \\ A & =-9\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=12-9{e}^{-t/20}.
$$

**Evidence only; ineligible for learning.**

## ORIGINAL PROFILE REPLAY: source_17592186377279
A dye vat initially holds $450\,\text{L}$ of liquid containing $2\,\text{kg}$ of dissolved dye.
A solution containing $0.02\,\text{kg/L}$ of dissolved dye is pumped into the vat at a rate of $30\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $30\,\text{L/min}.$ Which expression gives the amount of dye $Q(t),$ in kilograms, in the vat $t$ minutes after pumping begins?

- $Q(t)=2-9{e}^{-t/15}$
- $Q(t)=9-7{e}^{-t/20}$
- $Q(t)=9-7{e}^{t/15}$
- $Q(t)=9+7{e}^{-t/15}$
- $Q(t)=9-7{e}^{-t/15}$ [correct]

Let $Q$ be the amount of dye in the vat at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which dye enters the vat minus the rate at which dye leaves the vat.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additives enter the vat.

Note that a feed solution containing $0.02\,\text{kg/L}$ of the dye enters the vat at a rate of $30\,\text{L/min}.$ So, the rate at which the *dye* enters the vat is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.02\,\frac{\text{kg}}{\text{L}})\cdot (30\,\frac{\text{L}}{\text{min}}) \\  & =(0.02\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (30\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.6\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additives exit the vat.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the vat remains $450\,\text{L}.$ Then, since $Q$ is the amount of dye in the vat, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{450}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $30\,\text{L/min},$ *dye* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(30\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{450}\,\frac{\text{kg}}{\text{L}}) \\  & =(30\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{450}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{30Q}{450}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{15}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.6-\frac{Q}{15}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{15}Q=0.6.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{15}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/15},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{15}\alpha =0.6\,⟹\,\alpha =9.
$$

Therefore, the particular solution is ${Q}_{p}(t)=9.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/15}+9.
$$

We're told that the vat initially contains $2\,\text{kg}$ of dissolved dye. So, we can apply the initial condition $Q(0)=2,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =2 \\ A{e}^{-0/15}+9 & =2 \\ A & =-7\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=9-7{e}^{-t/15}.
$$

**Evidence only; ineligible for learning.**

## ORIGINAL PROFILE REPLAY: source_17592186377286
A brewing tank initially holds $350\,\text{L}$ of liquid containing $8\,\text{kg}$ of dissolved sugar.
A feed solution containing $0.02\,\text{kg/L}$ of the sugar is pumped into the tank at a rate of $25\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $25\,\text{L/min}.$
Find, rounded to two decimal places, the amount of sugar in the tank $4$ minutes after pumping begins.

- $7.98\,\text{kg}$
- $8.21\,\text{kg}$
- $7.32\,\text{kg}$
- $7.75\,\text{kg}$ [correct]
- $7.54\,\text{kg}$

Let $Q$ be the amount of sugar in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which additives enter the tank minus the rate at which additives leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additives enter the tank.

Note that a feed solution containing $0.02\,\text{kg/L}$ of the sugar enters the tank at a rate of $25\,\text{L/min}.$ So, the rate at which the *sugar* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.02\,\frac{\text{kg}}{\text{L}})\cdot (25\,\frac{\text{L}}{\text{min}}) \\  & =(0.02\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (25\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.5\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additives exit the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $350\,\text{L}.$ Then, since $Q$ is the amount of sugar in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{350}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $25\,\text{L/min},$ *sugar* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(25\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{350}\,\frac{\text{kg}}{\text{L}}) \\  & =(25\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{350}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{25Q}{350}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{14}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.5-\frac{Q}{14}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{14}Q=\frac{1}{2}.
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
0+\frac{1}{14}\alpha =\frac{1}{2}\,⟹\,\alpha =7.
$$

Therefore, the particular solution is ${Q}_{p}(t)=7.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/14}+7.
$$

We're told that the tank initially contains $8\,\text{kg}$ of dissolved sugar. So, we can apply the initial condition $Q(0)=8,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =8 \\ A{e}^{-0/14}+7 & =8 \\ A & =1\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=7+{e}^{-t/14}
$$

Finally,  the amount of sugar in the tank $4$ minutes after pumping begins is

$$
Q(4)=7+{e}^{-4/14}≈7.75\,\text{kg},
$$

rounded to two decimal places.

**Evidence only; ineligible for learning.**

## GENERATED VARIANT — OBSERVED EVIDENCE BANK: source_17592186229724
A wastewater basin initially holds $1500L$ of water containing $12kg$ of dissolved pollutant.
A solution containing $0.03kg/L$ of dissolved pollutant is pumped into the basin at a rate of $60L/min$, while the completely mixed liquid is drained out at a rate of $60L/min$. Which expression gives the amount of pollutant $Q(t)$, in kilograms, in the basin $t$ minutes after pumping begins?

- $Q(t) = 45 + 33e^{-t/25}$
- $Q(t) = 12 - 45e^{-t/25}$
- $Q(t) = 45 - 33e^{-t/20}$
- $Q(t) = 45 - 33e^{-t/25}$
- $Q(t) = 45 - 33e^{t/25}$

[Original worked solution omitted.]

**Evidence only; ineligible for learning.**

## GENERATED VARIANT — OBSERVED EVIDENCE BANK: source_17592186229725
A fish hatchery tank initially holds $1800L$ of water containing $20kg$ of dissolved salt.
A feed solution containing $0.02kg/L$ of the salt is pumped into the tank at a rate of $60L/min$, while the completely mixed liquid is drained out at a rate of $60L/min$.
Find, rounded to two decimal places, the amount of salt in the tank $6$ minutes after pumping begins.

- $21.52kg$
- $22.90kg$
- $22.04kg$
- $23.66kg$
- $24.22kg$

[Original worked solution omitted.]

**Evidence only; ineligible for learning.**

## GENERATED VARIANT — OBSERVED EVIDENCE BANK: source_17592186377242
A nutrient-mixing tank initially holds $1440\,\text{L}$ of solution containing $6\,\text{kg}$ of dissolved supplement.
A feed solution containing $0.03\,\text{kg/L}$ of the supplement is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $24\,\text{L/min}.$
Find, rounded to two decimal places, the amount of supplement in the tank $5$ minutes after pumping begins.

- $9.66\,\text{kg}$
- $10.04\,\text{kg}$
- $7.92\,\text{kg}$
- $8.34\,\text{kg}$
- $8.97\,\text{kg}$ [correct]

Let $Q$ be the amount of supplement in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which supplements enter the tank minus the rate at which supplements leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which supplements enter the tank.

Note that a feed solution containing $0.03\,\text{kg/L}$ of the supplement enters the tank at a rate of $24\,\text{L/min}.$ So, the rate at which the *supplement* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.03\,\frac{\text{kg}}{\text{L}})\cdot (24\,\frac{\text{L}}{\text{min}}) \\  & =(0.03\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (24\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.72\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which supplements exit the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $1440\,\text{L}.$ Then, since $Q$ is the amount of supplement in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{1440}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $24\,\text{L/min},$ *supplement* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(24\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{1440}\,\frac{\text{kg}}{\text{L}}) \\  & =(24\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{1440}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{24Q}{1440}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{60}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.72-\frac{Q}{60}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{60}Q=0.72.
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
0+\frac{1}{60}\alpha =0.72\,⟹\,\alpha =43.2.
$$

Therefore, the particular solution is ${Q}_{p}(t)=43.2.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/60}+43.2.
$$

We're told that the tank initially contains $6\,\text{kg}$ of dissolved supplement. So, we can apply the initial condition $Q(0)=6,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =6 \\ A{e}^{-0/60}+43.2 & =6 \\ A & =-37.2\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=43.2-37.2{e}^{-t/60}
$$

Finally,  the amount of supplement in the tank $5$ minutes after pumping begins is

$$
Q(5)=43.2-37.2{e}^{-5/60}≈8.97\,\text{kg},
$$

rounded to two decimal places.

**Evidence only; ineligible for learning.**

## GENERATED VARIANT — OBSERVED EVIDENCE BANK: source_17592186377256
A coolant tank initially holds $1000\,\text{L}$ of liquid containing $14\,\text{kg}$ of dissolved anti-corrosion additive.
A solution containing $0.02\,\text{kg/L}$ of dissolved additive is pumped into the tank at a rate of $50\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $50\,\text{L/min}.$ Which expression gives the amount of additive $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins?

- $Q(t)=18-4{e}^{-t/20}$
- $Q(t)=-18+32{e}^{-t/20}$
- $Q(t)=16-{e}^{-t/20}$
- $Q(t)=24-10{e}^{t/20}$
- $Q(t)=20-6{e}^{-t/20}$ [correct]

Let $Q$ be the amount of additive in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which additives enter the tank minus the rate at which additives leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additives enter the tank.

Note that a feed solution containing $0.02\,\text{kg/L}$ of the additive enters the tank at a rate of $50\,\text{L/min}.$ So, the rate at which the *additive* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.02\,\frac{\text{kg}}{\text{L}})\cdot (50\,\frac{\text{L}}{\text{min}}) \\  & =(0.02\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (50\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additives exit the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $1000\,\text{L}.$ Then, since $Q$ is the amount of additive in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{1000}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $50\,\text{L/min},$ *additive* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(50\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{1000}\,\frac{\text{kg}}{\text{L}}) \\  & =(50\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{1000}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{50Q}{1000}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{20}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1-\frac{Q}{20}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{20}Q=1.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{20}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/20},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{20}\alpha =1\,⟹\,\alpha =20.
$$

Therefore, the particular solution is ${Q}_{p}(t)=20.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/20}+20.
$$

We're told that the tank initially contains $14\,\text{kg}$ of dissolved additive. So, we can apply the initial condition $Q(0)=14,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =14 \\ A{e}^{-0/20}+20 & =14 \\ A & =-6\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=20-6{e}^{-t/20}.
$$

**Evidence only; ineligible for learning.**

## GENERATED VARIANT — OBSERVED EVIDENCE BANK: source_17592186377263
A storage tank initially holds $800\,\text{L}$ of liquid containing $6\,\text{kg}$ of dissolved disinfectant.
A solution containing $0.03\,\text{kg/L}$ of dissolved disinfectant is pumped into the tank at a rate of $40\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $40\,\text{L/min}.$ Which expression gives the amount of disinfectant $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins?

- $Q(t)=-18+24{e}^{-t/20}$
- $Q(t)=8-{e}^{-t/20}$
- $Q(t)=24-18{e}^{-t/20}$ [correct]
- $Q(t)=20-14{e}^{t/20}$
- $Q(t)=-2+8{e}^{t/20}$

Let $Q$ be the amount of disinfectant in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which disinfectant enters the tank minus the rate at which disinfectant leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additives enter the tank.

Note that a feed solution containing $0.03\,\text{kg/L}$ of the disinfectant enters the tank at a rate of $40\,\text{L/min}.$ So, the rate at which the *disinfectant* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.03\,\frac{\text{kg}}{\text{L}})\cdot (40\,\frac{\text{L}}{\text{min}}) \\  & =(0.03\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (40\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1.2\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additives exit the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $800\,\text{L}.$ Then, since $Q$ is the amount of disinfectant in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{800}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $40\,\text{L/min},$ *disinfectant* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(40\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{800}\,\frac{\text{kg}}{\text{L}}) \\  & =(40\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{800}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{40Q}{800}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{20}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1.2-\frac{Q}{20}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{20}Q=1.2.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{20}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/20},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{20}\alpha =1.2\,⟹\,\alpha =24.
$$

Therefore, the particular solution is ${Q}_{p}(t)=24.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/20}+24.
$$

We're told that the tank initially contains $6\,\text{kg}$ of dissolved disinfectant. So, we can apply the initial condition $Q(0)=6,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =6 \\ A{e}^{-0/20}+24 & =6 \\ A & =-18\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=24-18{e}^{-t/20}.
$$

**Evidence only; ineligible for learning.**

## GENERATED VARIANT — OBSERVED EVIDENCE BANK: source_17592186377279
A dye vat initially holds $900\,\text{L}$ of liquid containing $4\,\text{kg}$ of dissolved dye.
A solution containing $0.02\,\text{kg/L}$ of dissolved dye is pumped into the vat at a rate of $60\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $60\,\text{L/min}.$ Which expression gives the amount of dye $Q(t),$ in kilograms, in the vat $t$ minutes after pumping begins?

- $Q(t)=18+14{e}^{-t/15}$
- $Q(t)=18-14{e}^{-t/15}$ [correct]
- $Q(t)=18-14{e}^{-t/20}$
- $Q(t)=18-14{e}^{t/15}$
- $Q(t)=4-18{e}^{-t/15}$

Let $Q$ be the amount of dye in the vat at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which dye enters the vat minus the rate at which dye leaves the vat.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additives enter the vat.

Note that a feed solution containing $0.02\,\text{kg/L}$ of the dye enters the vat at a rate of $60\,\text{L/min}.$ So, the rate at which the *dye* enters the vat is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.02\,\frac{\text{kg}}{\text{L}})\cdot (60\,\frac{\text{L}}{\text{min}}) \\  & =(0.02\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (60\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1.2\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additives exit the vat.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the vat remains $900\,\text{L}.$ Then, since $Q$ is the amount of dye in the vat, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{900}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $60\,\text{L/min},$ *dye* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(60\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{900}\,\frac{\text{kg}}{\text{L}}) \\  & =(60\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{900}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{60Q}{900}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{15}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1.2-\frac{Q}{15}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{15}Q=1.2.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{15}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/15},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{15}\alpha =1.2\,⟹\,\alpha =18.
$$

Therefore, the particular solution is ${Q}_{p}(t)=18.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/15}+18.
$$

We're told that the vat initially contains $4\,\text{kg}$ of dissolved dye. So, we can apply the initial condition $Q(0)=4,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =4 \\ A{e}^{-0/15}+18 & =4 \\ A & =-14\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=18-14{e}^{-t/15}.
$$

**Evidence only; ineligible for learning.**

## GENERATED VARIANT — OBSERVED EVIDENCE BANK: source_17592186377286
A brewing tank initially holds $700\,\text{L}$ of liquid containing $16\,\text{kg}$ of dissolved sugar.
A feed solution containing $0.02\,\text{kg/L}$ of the sugar is pumped into the tank at a rate of $50\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $50\,\text{L/min}.$
Find, rounded to two decimal places, the amount of sugar in the tank $4$ minutes after pumping begins.

- $15.50\,\text{kg}$ [correct]
- $15.08\,\text{kg}$
- $16.42\,\text{kg}$
- $14.64\,\text{kg}$
- $15.96\,\text{kg}$

Let $Q$ be the amount of sugar in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which additives enter the tank minus the rate at which additives leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which additives enter the tank.

Note that a feed solution containing $0.02\,\text{kg/L}$ of the sugar enters the tank at a rate of $50\,\text{L/min}.$ So, the rate at which the *sugar* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.02\,\frac{\text{kg}}{\text{L}})\cdot (50\,\frac{\text{L}}{\text{min}}) \\  & =(0.02\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (50\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additives exit the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $700\,\text{L}.$ Then, since $Q$ is the amount of sugar in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{700}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $50\,\text{L/min},$ *sugar* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(50\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{700}\,\frac{\text{kg}}{\text{L}}) \\  & =(50\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{700}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{50Q}{700}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{14}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1-\frac{Q}{14}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{14}Q=1.
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
0+\frac{1}{14}\alpha =1\,⟹\,\alpha =14.
$$

Therefore, the particular solution is ${Q}_{p}(t)=14.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/14}+14.
$$

We're told that the tank initially contains $16\,\text{kg}$ of dissolved sugar. So, we can apply the initial condition $Q(0)=16,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =16 \\ A{e}^{-0/14}+14 & =16 \\ A & =2\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=14+2{e}^{-t/14}
$$

Finally,  the amount of sugar in the tank $4$ minutes after pumping begins is

$$
Q(4)=14+2{e}^{-4/14}≈15.50\,\text{kg},
$$

rounded to two decimal places.

**Evidence only; ineligible for learning.**

## GENERATED VARIANT — OBSERVED LAYOUT, AUTHORED COMPLETE BANK: expression
A storage tank initially holds $600\,\text{L}$ of liquid containing $10\,\text{kg}$ of dissolved disinfectant.
A feed solution containing $0.02\,\text{kg/L}$ of the disinfectant is pumped into the tank at a rate of $20\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $20\,\text{L/min}.$ Which expression gives the amount of disinfectant $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins?

- $Q(t)=24-14e^{-t/60}$
- $Q(t)=6+4e^{-t/15}$
- $Q(t)=12-2e^{-t/30}$ [correct]
- $Q(t)=12+2e^{-t/30}$
- $Q(t)=0.4+9.6e^{-t/30}$

Let $Q$ be the amount of disinfectant in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which disinfectant enters the tank minus the rate at which disinfectant leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which disinfectant enters the tank.

Note that a feed solution containing $0.02\,\text{kg/L}$ of the disinfectant enters the tank at a rate of $20\,\text{L/min}.$ So, the rate at which the *disinfectant* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.02\,\frac{\text{kg}}{\text{L}})\cdot (20\,\frac{\text{L}}{\text{min}}) \\  & =(0.02\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (20\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.4\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which disinfectant exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $600\,\text{L}.$ Then, since $Q$ is the amount of disinfectant in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{600}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $20\,\text{L/min},$ *disinfectant* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{600}\,\frac{\text{kg}}{\text{L}}) \\  & =(20\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{600}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{20Q}{600}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{30}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.4-\frac{Q}{30}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{30}Q=0.4.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{30}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/30},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{30}\alpha =0.4\,⟹\,\alpha =12.
$$

Therefore, the particular solution is ${Q}_{p}(t)=12.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/30}+12.
$$

We're told that the tank initially contains $10\,\text{kg}$ of dissolved disinfectant. So, we can apply the initial condition $Q(0)=10,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =10 \\ A{e}^{-0/30}+12 & =10 \\ A & =-2\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=12-2{e}^{-t/30}.
$$

## GENERATED VARIANT — OBSERVED LAYOUT, AUTHORED COMPLETE BANK: expression
A coolant tank initially holds $525\,\text{L}$ of liquid containing $9\,\text{kg}$ of dissolved additive.
A feed solution containing $0.01\,\text{kg/L}$ of the additive is pumped into the tank at a rate of $15\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$ Which expression gives the amount of additive $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins?

- $Q(t)=10.5-1.5e^{-t/70}$
- $Q(t)=0.15+8.85e^{-t/35}$
- $Q(t)=5.25-3.75e^{-t/35}$
- $Q(t)=5.25+3.75e^{-t/35}$ [correct]
- $Q(t)=2.625+6.375e^{-t/17.5}$

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

Note that a feed solution containing $0.01\,\text{kg/L}$ of the additive enters the tank at a rate of $15\,\text{L/min}.$ So, the rate at which the *additive* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.01\,\frac{\text{kg}}{\text{L}})\cdot (15\,\frac{\text{L}}{\text{min}}) \\  & =(0.01\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (15\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.15\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additive exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $525\,\text{L}.$ Then, since $Q$ is the amount of additive in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{525}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $15\,\text{L/min},$ *additive* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(15\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{525}\,\frac{\text{kg}}{\text{L}}) \\  & =(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{525}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{15Q}{525}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{35}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.15-\frac{Q}{35}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{35}Q=0.15.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{35}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/35},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{35}\alpha =0.15\,⟹\,\alpha =5.25.
$$

Therefore, the particular solution is ${Q}_{p}(t)=5.25.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/35}+5.25.
$$

We're told that the tank initially contains $9\,\text{kg}$ of dissolved additive. So, we can apply the initial condition $Q(0)=9,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =9 \\ A{e}^{-0/35}+5.25 & =9 \\ A & =3.75\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=5.25+3.75{e}^{-t/35}.
$$

## GENERATED VARIANT — OBSERVED LAYOUT, AUTHORED COMPLETE BANK: amount
A fish hatchery tank initially holds $625\,\text{L}$ of water containing $22\,\text{kg}$ of dissolved salt.
A feed solution containing $0.04\,\text{kg/L}$ of the salt is pumped into the tank at a rate of $25\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $25\,\text{L/min}.$
Find, rounded to two decimal places, the amount of salt in the tank $7$ minutes after pumping begins.

- $25.66\,\text{kg}$
- $17.93\,\text{kg}$
- $22.73\,\text{kg}$ [correct]
- $27.27\,\text{kg}$
- $16.87\,\text{kg}$

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

Note that a feed solution containing $0.04\,\text{kg/L}$ of the salt enters the tank at a rate of $25\,\text{L/min}.$ So, the rate at which the *salt* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.04\,\frac{\text{kg}}{\text{L}})\cdot (25\,\frac{\text{L}}{\text{min}}) \\  & =(0.04\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (25\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $625\,\text{L}.$ Then, since $Q$ is the amount of salt in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{625}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $25\,\text{L/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(25\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{625}\,\frac{\text{kg}}{\text{L}}) \\  & =(25\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{625}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{25Q}{625}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{25}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1-\frac{Q}{25}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{25}Q=1.
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
0+\frac{1}{25}\alpha =1\,⟹\,\alpha =25.
$$

Therefore, the particular solution is ${Q}_{p}(t)=25.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/25}+25.
$$

We're told that the tank initially contains $22\,\text{kg}$ of dissolved salt. So, we can apply the initial condition $Q(0)=22,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =22 \\ A{e}^{-0/25}+25 & =22 \\ A & =-3\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=25-3{e}^{-t/25}
$$

Finally,  the amount of salt in the tank $7$ minutes after pumping begins is

$$
Q(7)=25-3{e}^{-7/25}≈22.73\,\text{kg},
$$

rounded to two decimal places.

## GENERATED VARIANT — OBSERVED LAYOUT, AUTHORED COMPLETE BANK: amount
A coolant tank initially holds $525\,\text{L}$ of liquid containing $9\,\text{kg}$ of dissolved additive.
A feed solution containing $0.01\,\text{kg/L}$ of the additive is pumped into the tank at a rate of $15\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$
Find, rounded to two decimal places, the amount of additive in the tank $9$ minutes after pumping begins.

- $9.18\,\text{kg}$
- $6.99\,\text{kg}$
- $2.35\,\text{kg}$
- $8.15\,\text{kg}$ [correct]
- $6.44\,\text{kg}$

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

Note that a feed solution containing $0.01\,\text{kg/L}$ of the additive enters the tank at a rate of $15\,\text{L/min}.$ So, the rate at which the *additive* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.01\,\frac{\text{kg}}{\text{L}})\cdot (15\,\frac{\text{L}}{\text{min}}) \\  & =(0.01\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (15\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.15\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additive exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $525\,\text{L}.$ Then, since $Q$ is the amount of additive in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{525}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $15\,\text{L/min},$ *additive* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(15\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{525}\,\frac{\text{kg}}{\text{L}}) \\  & =(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{525}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{15Q}{525}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{35}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.15-\frac{Q}{35}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{35}Q=\frac{3}{20}.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{35}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/35},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{35}\alpha =\frac{3}{20}\,⟹\,\alpha =5.25.
$$

Therefore, the particular solution is ${Q}_{p}(t)=5.25.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/35}+5.25.
$$

We're told that the tank initially contains $9\,\text{kg}$ of dissolved additive. So, we can apply the initial condition $Q(0)=9,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =9 \\ A{e}^{-0/35}+5.25 & =9 \\ A & =3.75\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=5.25+3.75{e}^{-t/35}
$$

Finally,  the amount of additive in the tank $9$ minutes after pumping begins is

$$
Q(9)=5.25+3.75{e}^{-9/35}≈8.15\,\text{kg},
$$

rounded to two decimal places.

## GENERATED VARIANT — AUTHORED MISSING-LEVEL EXTENSION: amount_unit_conversion
A fish hatchery tank initially holds $625\,\text{L}$ of water containing $22\,\text{kg}$ of dissolved salt.
A feed solution containing $40\,\text{g/L}$ of the salt is pumped into the tank at a rate of $25\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $25\,\text{L/min}.$
Find, rounded to two decimal places, the amount of salt in the tank $7$ minutes after pumping begins.

- $25.66\,\text{kg}$
- $17.93\,\text{kg}$
- $22.73\,\text{kg}$ [correct]
- $27.27\,\text{kg}$
- $16.87\,\text{kg}$

The feed concentration must use kilograms: $40\,\text{g/L}\cdot\frac{1\,\text{kg}}{1000\,\text{g}}=0.04\,\text{kg/L}.$

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

Note that a feed solution containing $0.04\,\text{kg/L}$ of the salt enters the tank at a rate of $25\,\text{L/min}.$ So, the rate at which the *salt* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.04\,\frac{\text{kg}}{\text{L}})\cdot (25\,\frac{\text{L}}{\text{min}}) \\  & =(0.04\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (25\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $625\,\text{L}.$ Then, since $Q$ is the amount of salt in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{625}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $25\,\text{L/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(25\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{625}\,\frac{\text{kg}}{\text{L}}) \\  & =(25\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{625}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{25Q}{625}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{25}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1-\frac{Q}{25}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{25}Q=1.
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
0+\frac{1}{25}\alpha =1\,⟹\,\alpha =25.
$$

Therefore, the particular solution is ${Q}_{p}(t)=25.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/25}+25.
$$

We're told that the tank initially contains $22\,\text{kg}$ of dissolved salt. So, we can apply the initial condition $Q(0)=22,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =22 \\ A{e}^{-0/25}+25 & =22 \\ A & =-3\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=25-3{e}^{-t/25}
$$

Finally,  the amount of salt in the tank $7$ minutes after pumping begins is

$$
Q(7)=25-3{e}^{-7/25}≈22.73\,\text{kg},
$$

rounded to two decimal places.

## GENERATED VARIANT — AUTHORED MISSING-LEVEL EXTENSION: amount_unit_conversion
A coolant tank initially holds $525\,\text{L}$ of liquid containing $9\,\text{kg}$ of dissolved additive.
A feed solution containing $10\,\text{g/L}$ of the additive is pumped into the tank at a rate of $15\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$
Find, rounded to two decimal places, the amount of additive in the tank $9$ minutes after pumping begins.

- $9.18\,\text{kg}$
- $6.99\,\text{kg}$
- $2.35\,\text{kg}$
- $8.15\,\text{kg}$ [correct]
- $6.44\,\text{kg}$

The feed concentration must use kilograms: $10\,\text{g/L}\cdot\frac{1\,\text{kg}}{1000\,\text{g}}=0.01\,\text{kg/L}.$

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

Note that a feed solution containing $0.01\,\text{kg/L}$ of the additive enters the tank at a rate of $15\,\text{L/min}.$ So, the rate at which the *additive* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.01\,\frac{\text{kg}}{\text{L}})\cdot (15\,\frac{\text{L}}{\text{min}}) \\  & =(0.01\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (15\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.15\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which additive exits the tank.

Next, note that the rate of flow in equals the rate of flow out, so the volume in the tank remains $525\,\text{L}.$ Then, since $Q$ is the amount of additive in the tank, the *concentration* of the solution at time $t$ is

$$
\frac{Q}{525}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $15\,\text{L/min},$ *additive* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(15\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{525}\,\frac{\text{kg}}{\text{L}}) \\  & =(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{525}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{15Q}{525}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{35}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.15-\frac{Q}{35}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1}{35}Q=\frac{3}{20}.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with constant coefficients. To find the general solution, we must sum the complementary and particular solutions.

- To find the complementary solution ${Q}_{c},$ we solve the corresponding homogeneous equation, given by

$$
\frac{d{Q}_{c}}{dt}+\frac{1}{35}{Q}_{c}=0.
$$

Solving using an integration technique, such as separation of variables, we obtain the complementary solution

$$
{Q}_{c}(t)=A{e}^{-t/35},
$$

where $A$ is a constant of integration.

- Next, we find the particular solution. Note that the right-hand side of the inhomogeneous equation is a polynomial of degree $0.$ So, we assume that the particular solution is also a polynomial of degree $0,$ i.e.,

$$
{Q}_{p}(t)=\alpha .
$$

To find the value of $\alpha ,$ we substitute ${Q}_{p}=\alpha $ and $\frac{d{Q}_{p}}{dt}=(\alpha )^{′}=0$ into the inhomogeneous equation:

$$
0+\frac{1}{35}\alpha =\frac{3}{20}\,⟹\,\alpha =5.25.
$$

Therefore, the particular solution is ${Q}_{p}(t)=5.25.$

Now, since the general solution is given by the sum of the complementary solution and the particular solution, the general solution in our case is

$$
Q(t)={Q}_{c}(t)+{Q}_{p}(t)=A{e}^{-t/35}+5.25.
$$

We're told that the tank initially contains $9\,\text{kg}$ of dissolved additive. So, we can apply the initial condition $Q(0)=9,$ and solve for $A:$

$$
\begin{aligned}Q(0) & =9 \\ A{e}^{-0/35}+5.25 & =9 \\ A & =3.75\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
Q(t)=5.25+3.75{e}^{-t/35}
$$

Finally,  the amount of additive in the tank $9$ minutes after pumping begins is

$$
Q(9)=5.25+3.75{e}^{-9/35}≈8.15\,\text{kg},
$$

rounded to two decimal places.
