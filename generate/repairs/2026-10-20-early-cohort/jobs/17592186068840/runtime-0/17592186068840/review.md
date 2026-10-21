# Explicit separable solutions review

Original records and observed anomaly banks are evidence replay; generated records use authored complete operation banks.

## Original replay — linear_sin

Profile: `observed_linear_sin` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{sin}⁡x$ for $y\ne 0.$

- $y={e}^{-\operatorname{sin}⁡x}+K$
- $y=\operatorname{ln}⁡\operatorname{cos}⁡x+K$
- $y=K{e}^{-\operatorname{cos}⁡x}$ (correct)
- $y=\operatorname{cos}⁡x+K$
- $y={e}^{-\operatorname{cos}⁡x}+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{sin}⁡x \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{sin}⁡x \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sin}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=-\operatorname{cos}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-\operatorname{cos}⁡x+C} \\ |y| & ={e}^{-\operatorname{cos}⁡x+C} \\ |y| & ={e}^{-\operatorname{cos}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{-\operatorname{cos}⁡x},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{-\operatorname{cos}⁡x}.
$$

## Generated variant — linear_sin

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{sin}⁡(x+4)$ for $y\ne 0.$

- $y=K + e^{- \cos{\left(x + 4 \right)}}$
- $y=C - \cos{\left(x + 4 \right)}$
- $y=K e^{- \cos{\left(x + 4 \right)}}$ (correct)
- $y=K e^{\sin{\left(x + 4 \right)}}$
- $y=K e^{\cos{\left(x + 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{sin}⁡(x+4) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{sin}⁡(x+4) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(x+4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(x+4)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡(x+4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sin}⁡(x+4)\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\operatorname{cos}⁡(x+4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=-\operatorname{cos}⁡(x+4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-\operatorname{cos}⁡(x+4)+C} \\ |y| & ={e}^{-\operatorname{cos}⁡(x+4)+C} \\ |y| & ={e}^{-\operatorname{cos}⁡(x+4)}\cdot {e}^{C} \\ |y| & =K{e}^{-\operatorname{cos}⁡(x+4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{-\operatorname{cos}⁡(x+4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_sin

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{sin}⁡(x-4)$ for $y\ne 0.$

- $y=C - \cos{\left(x - 4 \right)}$
- $y=K e^{\cos{\left(x - 4 \right)}}$
- $y=K + e^{- \cos{\left(x - 4 \right)}}$
- $y=K e^{- \cos{\left(x - 4 \right)}}$ (correct)
- $y=K e^{\sin{\left(x - 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{sin}⁡(x-4) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{sin}⁡(x-4) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(x-4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(x-4)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡(x-4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sin}⁡(x-4)\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\operatorname{cos}⁡(x-4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=-\operatorname{cos}⁡(x-4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-\operatorname{cos}⁡(x-4)+C} \\ |y| & ={e}^{-\operatorname{cos}⁡(x-4)+C} \\ |y| & ={e}^{-\operatorname{cos}⁡(x-4)}\cdot {e}^{C} \\ |y| & =K{e}^{-\operatorname{cos}⁡(x-4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{-\operatorname{cos}⁡(x-4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_sin

Profile: `observed_linear_sin` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{sin}⁡(x+2)$ for $y\ne 0.$

- $y={e}^{-\operatorname{cos}⁡(x+2)}+K$
- $y=K{e}^{-\operatorname{cos}⁡(x+2)}$ (correct)
- $y={e}^{-\operatorname{sin}⁡(x+2)}+K$
- $y=\operatorname{cos}⁡(x+2)+K$
- $y=\operatorname{ln}⁡\operatorname{cos}⁡(x+2)+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{sin}⁡(x+2) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{sin}⁡(x+2) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡(x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡(x+2)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡(x+2)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sin}⁡(x+2)\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\operatorname{cos}⁡(x+2)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=-\operatorname{cos}⁡(x+2)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{-\operatorname{cos}⁡(x+2)+C} \\ |y| & ={e}^{-\operatorname{cos}⁡(x+2)+C} \\ |y| & ={e}^{-\operatorname{cos}⁡(x+2)}\cdot {e}^{C} \\ |y| & =K{e}^{-\operatorname{cos}⁡(x+2)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{-\operatorname{cos}⁡(x+2)}.
$$

## Original replay — autonomous_tan

Profile: `observed_autonomous_tan` (observed expression-shape bank; wrong-option intent unresolved).

{"a": 1}

Find the general solution to the differential equation ${y}^{′}={y}^{2}+1.$

- $y=\frac{{y}^{3}}{3}+y+C$
- $y=\operatorname{cot}⁡(x+C)$
- $y=\operatorname{sec}⁡(x)+C$
- $y=\operatorname{tan}⁡(x+C)$ (correct)
- $y=\operatorname{tan}⁡(x+1)+C$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & ={y}^{2}+1 \\ \frac{\text{d}y}{\text{d}x} & ={y}^{2}+1 \\ \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int \,\text{d}x \\ \operatorname{arctan}⁡(y) & =x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arctan}⁡(y)=x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\operatorname{tan}⁡(x+C).
$$

## Generated variant — autonomous_tan

Profile: `operation_errors` (authored complete operation bank).

{"a": 4}

Find the general solution to the differential equation ${y}^{′}=4({y}^{2}+1).$

- $y=C + \tan{\left(4 x \right)}$
- $y=C + 4 x$
- $y=\tan{\left(C + 4 x \right)}$ (correct)
- $y=\tan{\left(C + 4 \right)}$
- $y=\tan{\left(C - 4 x \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =4({y}^{2}+1) \\ \frac{\text{d}y}{\text{d}x} & =4({y}^{2}+1) \\ \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\text{d}x} & =4\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 4\,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 4\,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int 4\,\text{d}x \\ \operatorname{arctan}⁡(y) & =(4x)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arctan}⁡(y)=(4x)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\operatorname{tan}⁡((4x)+C).
$$

Use intervals avoiding tangent poles.

## Generated variant — autonomous_tan

Profile: `operation_errors` (authored complete operation bank).

{"a": 2}

Find the general solution to the differential equation ${y}^{′}=2({y}^{2}+1).$

- $y=C + 2 x$
- $y=\tan{\left(C - 2 x \right)}$
- $y=C + \tan{\left(2 x \right)}$
- $y=\tan{\left(C + 2 x \right)}$ (correct)
- $y=\tan{\left(C + 2 \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =2({y}^{2}+1) \\ \frac{\text{d}y}{\text{d}x} & =2({y}^{2}+1) \\ \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\text{d}x} & =2\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2\,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2\,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int 2\,\text{d}x \\ \operatorname{arctan}⁡(y) & =(2x)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arctan}⁡(y)=(2x)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\operatorname{tan}⁡((2x)+C).
$$

Use intervals avoiding tangent poles.

## Generated variant — autonomous_tan

Profile: `observed_autonomous_tan` (observed expression-shape bank; wrong-option intent unresolved).

{"a": 3}

Find the general solution to the differential equation ${y}^{′}=3({y}^{2}+1).$

- $y=\operatorname{tan}⁡((3x)+1)+C$
- $y=\operatorname{sec}⁡((3x))+C$
- $y=\frac{{y}^{3}}{3}+y+C$
- $y=\operatorname{tan}⁡((3x)+C)$ (correct)
- $y=\operatorname{cot}⁡((3x)+C)$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =3({y}^{2}+1) \\ \frac{\text{d}y}{\text{d}x} & =3({y}^{2}+1) \\ \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\text{d}x} & =3\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 3\,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 3\,\text{d}x \\ \int \frac{1}{{y}^{2}+1}\,\text{d}y & =\int 3\,\text{d}x \\ \operatorname{arctan}⁡(y) & =(3x)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arctan}⁡(y)=(3x)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\operatorname{tan}⁡((3x)+C).
$$

## Original replay — temperature_blank

Profile: `observed_temperature_blank` (observed expression-shape bank; wrong-option intent unresolved).

{"rate": "0.03", "ambient": 25}

Find the general solution to the differential equation in part 1 for $T\ne 25.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $T\,=\,25+K\cdot \,$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$\,\,$where $K$ is an arbitrary constant.

- ${e}^{-0.03t}$ (correct)

To find the general solution, we separate variables and integrate both sides with respect to $t,$ as follows:

$$
\begin{aligned}\frac{\text{d}T}{\text{d}t} & =-0.03(T-25) \\ \frac{1}{T-25}\cdot \frac{\text{d}T}{\text{d}t} & =-0.03 \\ \int \frac{1}{T-25}\cdot \frac{\text{d}T}{\text{d}t}\,\text{d}t & =\int -0.03\,\text{d}t \\ \int \frac{\text{d}T}{T-25} & =-0.03\int \,\text{d}t \\ \operatorname{ln}⁡|T-25| & =-0.03t+C\end{aligned}
$$

This is a perfectly valid general solution. However, if we want to write $T=T(t)$ explicitly, then we can solve for $T.$ This gives

$$
\begin{aligned}\operatorname{ln}⁡|T-25| & =-0.03t+C \\ |T-25| & ={e}^{-0.03t+C} \\ |T-25| & =K\,{e}^{-0.03t}\end{aligned}
$$

where $K={e}^{C}$ is an arbitrary positive constant.

We can drop the absolute value bars by allowing $K$ to be both positive and negative. Therefore, the most general solution is

$$
\begin{aligned}T & =25+K\,{e}^{-0.03t}.\end{aligned}
$$

## Generated variant — temperature_blank

Profile: `operation_errors` (authored complete operation bank).

{"rate": "0.05", "ambient": 25}

Find the general solution to $\frac{\mathrm{d}T}{\mathrm{d}t}=-0.05(T-25)$ for $T\ne 25.$

$T=25+K\cdot$ {{field-1}}, where $K$ is an arbitrary nonzero constant. Write the factor as a single exponential with leading coefficient 1.

- $e^{- \frac{t}{20}}$ (correct)

To find the general solution, we separate variables and integrate both sides with respect to $t,$ as follows:

$$
\begin{aligned}\frac{\text{d}T}{\text{d}t} & =-0.05(T-25) \\ \frac{1}{T-25}\cdot \frac{\text{d}T}{\text{d}t} & =-0.05 \\ \int \frac{1}{T-25}\cdot \frac{\text{d}T}{\text{d}t}\,\text{d}t & =\int -0.05\,\text{d}t \\ \int \frac{\text{d}T}{T-25} & =-0.05\int \,\text{d}t \\ \operatorname{ln}⁡|T-25| & =-0.05t+C\end{aligned}
$$

This is a perfectly valid general solution. However, if we want to write $T=T(t)$ explicitly, then we can solve for $T.$ This gives

$$
\begin{aligned}\operatorname{ln}⁡|T-25| & =-0.05t+C \\ |T-25| & ={e}^{-0.05t+C} \\ |T-25| & =K\,{e}^{-0.05t}\end{aligned}
$$

where $K={e}^{C}$ is an arbitrary positive constant.

We can drop the absolute value bars by allowing $K$ to be both positive and negative. Therefore, the most general solution is

$$
\begin{aligned}T & =25+K\,{e}^{-0.05t}.\end{aligned}
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — temperature_blank

Profile: `operation_errors` (authored complete operation bank).

{"rate": "0.03", "ambient": 20}

Find the general solution to $\frac{\mathrm{d}T}{\mathrm{d}t}=-0.03(T-20)$ for $T\ne 20.$

$T=20+K\cdot$ {{field-1}}, where $K$ is an arbitrary nonzero constant. Write the factor as a single exponential with leading coefficient 1.

- $e^{- \frac{3 t}{100}}$ (correct)

To find the general solution, we separate variables and integrate both sides with respect to $t,$ as follows:

$$
\begin{aligned}\frac{\text{d}T}{\text{d}t} & =-0.03(T-20) \\ \frac{1}{T-20}\cdot \frac{\text{d}T}{\text{d}t} & =-0.03 \\ \int \frac{1}{T-20}\cdot \frac{\text{d}T}{\text{d}t}\,\text{d}t & =\int -0.03\,\text{d}t \\ \int \frac{\text{d}T}{T-20} & =-0.03\int \,\text{d}t \\ \operatorname{ln}⁡|T-20| & =-0.03t+C\end{aligned}
$$

This is a perfectly valid general solution. However, if we want to write $T=T(t)$ explicitly, then we can solve for $T.$ This gives

$$
\begin{aligned}\operatorname{ln}⁡|T-20| & =-0.03t+C \\ |T-20| & ={e}^{-0.03t+C} \\ |T-20| & =K\,{e}^{-0.03t}\end{aligned}
$$

where $K={e}^{C}$ is an arbitrary positive constant.

We can drop the absolute value bars by allowing $K$ to be both positive and negative. Therefore, the most general solution is

$$
\begin{aligned}T & =20+K\,{e}^{-0.03t}.\end{aligned}
$$

Here $K$ is arbitrary and nonzero.

## Original replay — reciprocal_cube

Profile: `observed_reciprocal_cube` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2x}{3{y}^{2}}.$

- $y=\sqrt[3]{{x}^{2}+C}$ (correct)
- $y=\frac{2}{3}x+C$
- $y=({x}^{2}+C)^{3}$
- $y=\sqrt[3]{2x+C}$
- $y=(\sqrt[3]{x}+C)^{2}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2x}{3{y}^{2}} \\ 3{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 3{y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int 3{y}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2x\,\text{d}x \\ \int 3{y}^{2}\,\text{d}y & =\int 2x\,\text{d}x \\ {y}^{3} & ={x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{3}={x}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt[3]{{x}^{2}+C}.
$$

## Generated variant — reciprocal_cube

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2(x+4)}{3{y}^{2}}.$ Assume $x+4>0.$

- $y=C + \left|{x + 4}\right|^{\frac{2}{3}}$
- $y=C + \left(x + 4\right)^{2}$
- $y=\sqrt[3]{C + \left(x + 4\right)^{2}}$ (correct)
- $y=\sqrt[3]{C + 2 x + 8}$
- $y=\sqrt[3]{C - \left(x + 4\right)^{2}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2(x+4)}{3{y}^{2}} \\ 3{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2(x+4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 3{y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2(x+4)\,\text{d}x \\ \int 3{y}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2(x+4)\,\text{d}x \\ \int 3{y}^{2}\,\text{d}y & =\int 2(x+4)\,\text{d}x \\ {y}^{3} & ={(x+4)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{3}={(x+4)}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt[3]{{(x+4)}^{2}+C}.
$$

Use the real cube root, on intervals where $y\ne 0.$

## Generated variant — reciprocal_cube

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2(x-4)}{3{y}^{2}}.$ Assume $x-4>0.$

- $y=C + \left(x - 4\right)^{2}$
- $y=\sqrt[3]{C - \left(x - 4\right)^{2}}$
- $y=C + \left|{x - 4}\right|^{\frac{2}{3}}$
- $y=\sqrt[3]{C + \left(x - 4\right)^{2}}$ (correct)
- $y=\sqrt[3]{C + 2 x - 8}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2(x-4)}{3{y}^{2}} \\ 3{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2(x-4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 3{y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2(x-4)\,\text{d}x \\ \int 3{y}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2(x-4)\,\text{d}x \\ \int 3{y}^{2}\,\text{d}y & =\int 2(x-4)\,\text{d}x \\ {y}^{3} & ={(x-4)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{3}={(x-4)}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt[3]{{(x-4)}^{2}+C}.
$$

Use the real cube root, on intervals where $y\ne 0.$

## Generated variant — reciprocal_cube

Profile: `observed_reciprocal_cube` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2(x+2)}{3{y}^{2}}.$

- $y=(\sqrt[3]{(x+2)}+C)^{2}$
- $y=({(x+2)}^{2}+C)^{3}$
- $y=\sqrt[3]{{(x+2)}^{2}+C}$ (correct)
- $y=\sqrt[3]{2(x+2)+C}$
- $y=\frac{2}{3}(x+2)+C$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2(x+2)}{3{y}^{2}} \\ 3{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2(x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 3{y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2(x+2)\,\text{d}x \\ \int 3{y}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2(x+2)\,\text{d}x \\ \int 3{y}^{2}\,\text{d}y & =\int 2(x+2)\,\text{d}x \\ {y}^{3} & ={(x+2)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{3}={(x+2)}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt[3]{{(x+2)}^{2}+C}.
$$

## Original replay — linear_sec2

Profile: `observed_linear_sec2` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation ${y}^{′}=\frac{y}{{cos}^{2}⁡x}$ for $y\ne 0$ and $-\frac{\pi }{2}<x<\frac{\pi }{2}.$

- $y=K{e}^{\operatorname{cos}⁡x}$
- $y=\operatorname{ln}⁡(\operatorname{cos}⁡x)+K$
- $y={e}^{\operatorname{tan}⁡x}+K$
- $y=K{e}^{\operatorname{tan}⁡x}$ (correct)
- $y=K\operatorname{ln}⁡(\operatorname{tan}⁡x)$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =\frac{y}{{cos}^{2}⁡x} \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{cos}^{2}⁡x} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{{cos}^{2}⁡x} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {sec}^{2}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {sec}^{2}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {sec}^{2}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{tan}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{tan}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{tan}⁡x+C} \\ |y| & ={e}^{\operatorname{tan}⁡x+C} \\ |y| & ={e}^{\operatorname{tan}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{tan}⁡x},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{tan}⁡x}.
$$

## Generated variant — linear_sec2

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation ${y}^{′}=\frac{y}{{cos}^{2}⁡(x+4)}$ for $y\ne 0$ and $-\frac{\pi }{2}<(x+4)<\frac{\pi }{2}.$

- $y=K + e^{\tan{\left(x + 4 \right)}}$
- $y=C + \tan{\left(x + 4 \right)}$
- $y=K e^{\tan{\left(x + 4 \right)}}$ (correct)
- $y=K e^{\sec^{2}{\left(x + 4 \right)}}$
- $y=K e^{- \tan{\left(x + 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =\frac{y}{{cos}^{2}⁡(x+4)} \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{cos}^{2}⁡(x+4)} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{{cos}^{2}⁡(x+4)} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(x+4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {sec}^{2}⁡(x+4)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {sec}^{2}⁡(x+4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {sec}^{2}⁡(x+4)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{tan}⁡(x+4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{tan}⁡(x+4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{tan}⁡(x+4)+C} \\ |y| & ={e}^{\operatorname{tan}⁡(x+4)+C} \\ |y| & ={e}^{\operatorname{tan}⁡(x+4)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{tan}⁡(x+4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{tan}⁡(x+4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_sec2

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation ${y}^{′}=\frac{y}{{cos}^{2}⁡(x-4)}$ for $y\ne 0$ and $-\frac{\pi }{2}<(x-4)<\frac{\pi }{2}.$

- $y=C + \tan{\left(x - 4 \right)}$
- $y=K e^{- \tan{\left(x - 4 \right)}}$
- $y=K + e^{\tan{\left(x - 4 \right)}}$
- $y=K e^{\tan{\left(x - 4 \right)}}$ (correct)
- $y=K e^{\sec^{2}{\left(x - 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =\frac{y}{{cos}^{2}⁡(x-4)} \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{cos}^{2}⁡(x-4)} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{{cos}^{2}⁡(x-4)} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(x-4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {sec}^{2}⁡(x-4)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {sec}^{2}⁡(x-4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {sec}^{2}⁡(x-4)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{tan}⁡(x-4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{tan}⁡(x-4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{tan}⁡(x-4)+C} \\ |y| & ={e}^{\operatorname{tan}⁡(x-4)+C} \\ |y| & ={e}^{\operatorname{tan}⁡(x-4)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{tan}⁡(x-4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{tan}⁡(x-4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_sec2

Profile: `observed_linear_sec2` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation ${y}^{′}=\frac{y}{{cos}^{2}⁡(x+2)}$ for $y\ne 0$ and $-\frac{\pi }{2}<(x+2)<\frac{\pi }{2}.$

- $y=K\operatorname{ln}⁡(\operatorname{tan}⁡(x+2))$
- $y={e}^{\operatorname{tan}⁡(x+2)}+K$
- $y=K{e}^{\operatorname{cos}⁡(x+2)}$
- $y=K{e}^{\operatorname{tan}⁡(x+2)}$ (correct)
- $y=\operatorname{ln}⁡(\operatorname{cos}⁡(x+2))+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =\frac{y}{{cos}^{2}⁡(x+2)} \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{{cos}^{2}⁡(x+2)} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{{cos}^{2}⁡(x+2)} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & ={sec}^{2}⁡(x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {sec}^{2}⁡(x+2)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {sec}^{2}⁡(x+2)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {sec}^{2}⁡(x+2)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{tan}⁡(x+2)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{tan}⁡(x+2)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{tan}⁡(x+2)+C} \\ |y| & ={e}^{\operatorname{tan}⁡(x+2)+C} \\ |y| & ={e}^{\operatorname{tan}⁡(x+2)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{tan}⁡(x+2)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{tan}⁡(x+2)}.
$$

## Original replay — linear_cos

Profile: `observed_linear_cos` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{cos}⁡x$ for $y\ne 0.$

- $y=K{e}^{\operatorname{sin}⁡x}$ (correct)
- $y={e}^{-\operatorname{cos}⁡x}+K$
- $y=K{e}^{\operatorname{cos}⁡x}$
- $y=K{e}^{-2\operatorname{sin}⁡x}$
- $y={e}^{\operatorname{sin}⁡x}+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{cos}⁡x \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{cos}⁡x \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{cos}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{cos}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{cos}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{sin}⁡x+C} \\ |y| & ={e}^{\operatorname{sin}⁡x+C} \\ |y| & ={e}^{\operatorname{sin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sin}⁡x},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sin}⁡x}.
$$

## Generated variant — linear_cos

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{cos}⁡(x+4)$ for $y\ne 0.$

- $y=K + e^{\sin{\left(x + 4 \right)}}$
- $y=C + \sin{\left(x + 4 \right)}$
- $y=K e^{\sin{\left(x + 4 \right)}}$ (correct)
- $y=K e^{\cos{\left(x + 4 \right)}}$
- $y=K e^{- \sin{\left(x + 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{cos}⁡(x+4) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{cos}⁡(x+4) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡(x+4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{cos}⁡(x+4)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{cos}⁡(x+4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{cos}⁡(x+4)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sin}⁡(x+4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sin}⁡(x+4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{sin}⁡(x+4)+C} \\ |y| & ={e}^{\operatorname{sin}⁡(x+4)+C} \\ |y| & ={e}^{\operatorname{sin}⁡(x+4)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sin}⁡(x+4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sin}⁡(x+4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_cos

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{cos}⁡(x-4)$ for $y\ne 0.$

- $y=C + \sin{\left(x - 4 \right)}$
- $y=K e^{- \sin{\left(x - 4 \right)}}$
- $y=K + e^{\sin{\left(x - 4 \right)}}$
- $y=K e^{\sin{\left(x - 4 \right)}}$ (correct)
- $y=K e^{\cos{\left(x - 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{cos}⁡(x-4) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{cos}⁡(x-4) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡(x-4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{cos}⁡(x-4)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{cos}⁡(x-4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{cos}⁡(x-4)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sin}⁡(x-4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sin}⁡(x-4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{sin}⁡(x-4)+C} \\ |y| & ={e}^{\operatorname{sin}⁡(x-4)+C} \\ |y| & ={e}^{\operatorname{sin}⁡(x-4)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sin}⁡(x-4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sin}⁡(x-4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_cos

Profile: `observed_linear_cos` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{cos}⁡(x+2)$ for $y\ne 0.$

- $y={e}^{\operatorname{sin}⁡(x+2)}+K$
- $y=K{e}^{\operatorname{cos}⁡(x+2)}$
- $y=K{e}^{\operatorname{sin}⁡(x+2)}$ (correct)
- $y=K{e}^{-2\operatorname{sin}⁡(x+2)}$
- $y={e}^{-\operatorname{cos}⁡(x+2)}+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{cos}⁡(x+2) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{cos}⁡(x+2) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡(x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{cos}⁡(x+2)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{cos}⁡(x+2)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{cos}⁡(x+2)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sin}⁡(x+2)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sin}⁡(x+2)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{sin}⁡(x+2)+C} \\ |y| & ={e}^{\operatorname{sin}⁡(x+2)+C} \\ |y| & ={e}^{\operatorname{sin}⁡(x+2)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sin}⁡(x+2)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sin}⁡(x+2)}.
$$

## Original replay — linear_power

Profile: `observed_linear_power` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation ${y}^{′}={x}^{2}y$ for $y\ne 0.$

- $y=K{e}^{{x}^{3}/3}$ (correct)
- $y={e}^{{x}^{2}/2}+K$
- $y={e}^{{x}^{3}/3}+K$
- $y=K{e}^{{x}^{2}/2}$
- $y=K{e}^{3x}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & ={x}^{2}y \\ \frac{\text{d}y}{\text{d}x} & ={x}^{2}y \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & ={x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {x}^{2}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{3}\,{x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\frac{1}{3}\,{x}^{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{x}^{3}/3+C} \\ |y| & ={e}^{{x}^{3}/3+C} \\ |y| & ={e}^{{x}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{{x}^{3}/3},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{x}^{3}/3}.
$$

## Generated variant — linear_power

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation ${y}^{′}={(x+4)}^{2}y$ for $y\ne 0.$

- $y=K + e^{\frac{\left(x + 4\right)^{3}}{3}}$
- $y=C + \frac{\left(x + 4\right)^{3}}{3}$
- $y=K e^{\frac{\left(x + 4\right)^{3}}{3}}$ (correct)
- $y=K e^{\left(x + 4\right)^{2}}$
- $y=K e^{- \frac{\left(x + 4\right)^{3}}{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & ={(x+4)}^{2}y \\ \frac{\text{d}y}{\text{d}x} & ={(x+4)}^{2}y \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & ={(x+4)}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {(x+4)}^{2}\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {(x+4)}^{2}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {(x+4)}^{2}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{3}\,{(x+4)}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\frac{1}{3}\,{(x+4)}^{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{(x+4)}^{3}/3+C} \\ |y| & ={e}^{{(x+4)}^{3}/3+C} \\ |y| & ={e}^{{(x+4)}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{{(x+4)}^{3}/3},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{(x+4)}^{3}/3}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_power

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation ${y}^{′}={(x-4)}^{2}y$ for $y\ne 0.$

- $y=C + \frac{\left(x - 4\right)^{3}}{3}$
- $y=K e^{- \frac{\left(x - 4\right)^{3}}{3}}$
- $y=K + e^{\frac{\left(x - 4\right)^{3}}{3}}$
- $y=K e^{\frac{\left(x - 4\right)^{3}}{3}}$ (correct)
- $y=K e^{\left(x - 4\right)^{2}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & ={(x-4)}^{2}y \\ \frac{\text{d}y}{\text{d}x} & ={(x-4)}^{2}y \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & ={(x-4)}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {(x-4)}^{2}\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {(x-4)}^{2}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {(x-4)}^{2}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{3}\,{(x-4)}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\frac{1}{3}\,{(x-4)}^{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{(x-4)}^{3}/3+C} \\ |y| & ={e}^{{(x-4)}^{3}/3+C} \\ |y| & ={e}^{{(x-4)}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{{(x-4)}^{3}/3},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{(x-4)}^{3}/3}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_power

Profile: `observed_linear_power` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation ${y}^{′}={(x+2)}^{2}y$ for $y\ne 0.$

- $y=K{e}^{3(x+2)}$
- $y={e}^{{(x+2)}^{3}/3}+K$
- $y=K{e}^{{(x+2)}^{3}/3}$ (correct)
- $y=K{e}^{{(x+2)}^{2}/2}$
- $y={e}^{{(x+2)}^{2}/2}+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & ={(x+2)}^{2}y \\ \frac{\text{d}y}{\text{d}x} & ={(x+2)}^{2}y \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & ={(x+2)}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {(x+2)}^{2}\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {(x+2)}^{2}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {(x+2)}^{2}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\frac{1}{3}\,{(x+2)}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\frac{1}{3}\,{(x+2)}^{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{{(x+2)}^{3}/3+C} \\ |y| & ={e}^{{(x+2)}^{3}/3+C} \\ |y| & ={e}^{{(x+2)}^{3}/3}\cdot {e}^{C} \\ |y| & =K{e}^{{(x+2)}^{3}/3},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{{(x+2)}^{3}/3}.
$$

## Original replay — linear_arcsin

Profile: `observed_linear_arcsin` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation ${y}^{′}=\frac{y}{\sqrt{1-{x}^{2}}}$ for $y\ne 0$ and $|x|<1.$

- $y=\sqrt{1-{x}^{2}}+K$
- $y=K{e}^{1/\sqrt{1-{x}^{2}}}$
- $y=K{e}^{\operatorname{arcsin}⁡x}$ (correct)
- $y=K{e}^{\sqrt{1-{x}^{2}}}$
- $y={e}^{\operatorname{arcsin}⁡x}+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =\frac{y}{\sqrt{1-{x}^{2}}} \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{1-{x}^{2}}} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{1-{x}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{1}{\sqrt{1-{x}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{arcsin}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{arcsin}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{arcsin}⁡x+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡x+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{arcsin}⁡x},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{arcsin}⁡x}.
$$

## Generated variant — linear_arcsin

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation ${y}^{′}=\frac{y}{\sqrt{1-{(x+4)}^{2}}}$ for $y\ne 0$ and $|(x+4)|<1.$

- $y=K + e^{\arcsin{\left(x + 4 \right)}}$
- $y=C + \arcsin{\left(x + 4 \right)}$
- $y=K e^{\arcsin{\left(x + 4 \right)}}$ (correct)
- $y=K e^{\frac{1}{\sqrt{1 - \left(x + 4\right)^{2}}}}$
- $y=K e^{- \arcsin{\left(x + 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =\frac{y}{\sqrt{1-{(x+4)}^{2}}} \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{1-{(x+4)}^{2}}} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{1-{(x+4)}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\sqrt{1-{(x+4)}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{\sqrt{1-{(x+4)}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{1}{\sqrt{1-{(x+4)}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{arcsin}⁡(x+4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{arcsin}⁡(x+4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{arcsin}⁡(x+4)+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡(x+4)+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡(x+4)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{arcsin}⁡(x+4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{arcsin}⁡(x+4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_arcsin

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation ${y}^{′}=\frac{y}{\sqrt{1-{(x-4)}^{2}}}$ for $y\ne 0$ and $|(x-4)|<1.$

- $y=C + \arcsin{\left(x - 4 \right)}$
- $y=K e^{- \arcsin{\left(x - 4 \right)}}$
- $y=K + e^{\arcsin{\left(x - 4 \right)}}$
- $y=K e^{\arcsin{\left(x - 4 \right)}}$ (correct)
- $y=K e^{\frac{1}{\sqrt{1 - \left(x - 4\right)^{2}}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =\frac{y}{\sqrt{1-{(x-4)}^{2}}} \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{1-{(x-4)}^{2}}} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{1-{(x-4)}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\sqrt{1-{(x-4)}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{\sqrt{1-{(x-4)}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{1}{\sqrt{1-{(x-4)}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{arcsin}⁡(x-4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{arcsin}⁡(x-4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{arcsin}⁡(x-4)+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡(x-4)+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡(x-4)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{arcsin}⁡(x-4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{arcsin}⁡(x-4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_arcsin

Profile: `observed_linear_arcsin` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation ${y}^{′}=\frac{y}{\sqrt{1-{(x+2)}^{2}}}$ for $y\ne 0$ and $|(x+2)|<1.$

- $y={e}^{\operatorname{arcsin}⁡(x+2)}+K$
- $y=K{e}^{\operatorname{arcsin}⁡(x+2)}$ (correct)
- $y=\sqrt{1-{(x+2)}^{2}}+K$
- $y=K{e}^{\sqrt{1-{(x+2)}^{2}}}$
- $y=K{e}^{1/\sqrt{1-{(x+2)}^{2}}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =\frac{y}{\sqrt{1-{(x+2)}^{2}}} \\ \frac{\text{d}y}{\text{d}x} & =\frac{y}{\sqrt{1-{(x+2)}^{2}}} \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{\sqrt{1-{(x+2)}^{2}}}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{\sqrt{1-{(x+2)}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{\sqrt{1-{(x+2)}^{2}}}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \frac{1}{\sqrt{1-{(x+2)}^{2}}}\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{arcsin}⁡(x+2)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{arcsin}⁡(x+2)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{arcsin}⁡(x+2)+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡(x+2)+C} \\ |y| & ={e}^{\operatorname{arcsin}⁡(x+2)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{arcsin}⁡(x+2)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{arcsin}⁡(x+2)}.
$$

## Original replay — linear_sectan

Profile: `observed_linear_sectan` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{sec}⁡x\operatorname{tan}⁡x$ for $y\ne 0$ and $-\frac{\pi }{2}<x<\frac{\pi }{2}.$

- $y={e}^{\operatorname{sec}⁡x}+K$
- $y=K{e}^{\operatorname{sec}⁡x}$ (correct)
- $y=K{e}^{\operatorname{cos}⁡x}$
- $y=K{e}^{\operatorname{tan}⁡x}$
- $y={e}^{\operatorname{tan}⁡x}+K$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{sec}⁡x\operatorname{tan}⁡x \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{sec}⁡x\operatorname{tan}⁡x \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{sec}⁡x\operatorname{tan}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sec}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sec}⁡x+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{sec}⁡x+C} \\ |y| & ={e}^{\operatorname{sec}⁡x+C} \\ |y| & ={e}^{\operatorname{sec}⁡x}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sec}⁡x},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sec}⁡x}.
$$

## Generated variant — linear_sectan

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{sec}⁡(x+4)\operatorname{tan}⁡(x+4)$ for $y\ne 0$ and $-\frac{\pi }{2}<(x+4)<\frac{\pi }{2}.$

- $y=K + e^{\sec{\left(x + 4 \right)}}$
- $y=C + \sec{\left(x + 4 \right)}$
- $y=K e^{\sec{\left(x + 4 \right)}}$ (correct)
- $y=K e^{\tan{\left(x + 4 \right)} \sec{\left(x + 4 \right)}}$
- $y=K e^{- \sec{\left(x + 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{sec}⁡(x+4)\operatorname{tan}⁡(x+4) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{sec}⁡(x+4)\operatorname{tan}⁡(x+4) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{sec}⁡(x+4)\operatorname{tan}⁡(x+4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sec}⁡(x+4)\operatorname{tan}⁡(x+4)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sec}⁡(x+4)\operatorname{tan}⁡(x+4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sec}⁡(x+4)\operatorname{tan}⁡(x+4)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sec}⁡(x+4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sec}⁡(x+4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{sec}⁡(x+4)+C} \\ |y| & ={e}^{\operatorname{sec}⁡(x+4)+C} \\ |y| & ={e}^{\operatorname{sec}⁡(x+4)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sec}⁡(x+4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sec}⁡(x+4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_sectan

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{sec}⁡(x-4)\operatorname{tan}⁡(x-4)$ for $y\ne 0$ and $-\frac{\pi }{2}<(x-4)<\frac{\pi }{2}.$

- $y=C + \sec{\left(x - 4 \right)}$
- $y=K e^{- \sec{\left(x - 4 \right)}}$
- $y=K + e^{\sec{\left(x - 4 \right)}}$
- $y=K e^{\sec{\left(x - 4 \right)}}$ (correct)
- $y=K e^{\tan{\left(x - 4 \right)} \sec{\left(x - 4 \right)}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{sec}⁡(x-4)\operatorname{tan}⁡(x-4) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{sec}⁡(x-4)\operatorname{tan}⁡(x-4) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{sec}⁡(x-4)\operatorname{tan}⁡(x-4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sec}⁡(x-4)\operatorname{tan}⁡(x-4)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sec}⁡(x-4)\operatorname{tan}⁡(x-4)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sec}⁡(x-4)\operatorname{tan}⁡(x-4)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sec}⁡(x-4)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sec}⁡(x-4)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{sec}⁡(x-4)+C} \\ |y| & ={e}^{\operatorname{sec}⁡(x-4)+C} \\ |y| & ={e}^{\operatorname{sec}⁡(x-4)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sec}⁡(x-4)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sec}⁡(x-4)}.
$$

Here $K$ is arbitrary and nonzero.

## Generated variant — linear_sectan

Profile: `observed_linear_sectan` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation ${y}^{′}=y\operatorname{sec}⁡(x+2)\operatorname{tan}⁡(x+2)$ for $y\ne 0$ and $-\frac{\pi }{2}<(x+2)<\frac{\pi }{2}.$

- $y={e}^{\operatorname{tan}⁡(x+2)}+K$
- $y=K{e}^{\operatorname{cos}⁡(x+2)}$
- $y={e}^{\operatorname{sec}⁡(x+2)}+K$
- $y=K{e}^{\operatorname{tan}⁡(x+2)}$
- $y=K{e}^{\operatorname{sec}⁡(x+2)}$ (correct)

To find the general solution, we first separate the variables:

$$
\begin{aligned}{y}^{′} & =y\operatorname{sec}⁡(x+2)\operatorname{tan}⁡(x+2) \\ \frac{\text{d}y}{\text{d}x} & =y\operatorname{sec}⁡(x+2)\operatorname{tan}⁡(x+2) \\ \frac{1}{y}\,\frac{\text{d}y}{\text{d}x} & =\operatorname{sec}⁡(x+2)\operatorname{tan}⁡(x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sec}⁡(x+2)\operatorname{tan}⁡(x+2)\,\text{d}x \\ \int \frac{1}{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sec}⁡(x+2)\operatorname{tan}⁡(x+2)\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sec}⁡(x+2)\operatorname{tan}⁡(x+2)\,\text{d}x \\ \operatorname{ln}⁡|y| & =\operatorname{sec}⁡(x+2)+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=\operatorname{sec}⁡(x+2)+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}{e}^{\operatorname{ln}⁡|y|} & ={e}^{\operatorname{sec}⁡(x+2)+C} \\ |y| & ={e}^{\operatorname{sec}⁡(x+2)+C} \\ |y| & ={e}^{\operatorname{sec}⁡(x+2)}\cdot {e}^{C} \\ |y| & =K{e}^{\operatorname{sec}⁡(x+2)},\end{aligned}
$$

where $K={e}^{C}$ and $K>0.$

We can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is

$$
y=K{e}^{\operatorname{sec}⁡(x+2)}.
$$

## Original replay — negative_exp

Profile: `observed_negative_exp` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=x{e}^{-y}.$

- $y=\frac{\operatorname{ln}⁡({x}^{2})}{2}+C$
- $y=\operatorname{ln}⁡(\frac{{x}^{2}}{2}+C)$ (correct)
- $y=\operatorname{ln}⁡(\frac{x}{2})+C$
- $y=\operatorname{ln}⁡(\frac{{x}^{2}}{2})+C$
- $y=\frac{{x}^{2}}{2}+C$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =x{e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =\frac{x}{{e}^{y}} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & =x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int x\,\text{d}x \\ \int {e}^{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int x\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int x\,\text{d}x \\ {e}^{y} & =\frac{{x}^{2}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{y}=\frac{{x}^{2}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\operatorname{ln}⁡(\frac{{x}^{2}}{2}+C).
$$

## Generated variant — negative_exp

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=(x+4){e}^{-y}.$ Assume $x+4>0.$

- $y=C + \ln{\left(\frac{\left(x + 4\right)^{2}}{2} \right)}$
- $y=C + \frac{\left(x + 4\right)^{2}}{2}$
- $y=\ln{\left(C + \frac{\left(x + 4\right)^{2}}{2} \right)}$ (correct)
- $y=\ln{\left(C + x + 4 \right)}$
- $y=\ln{\left(C - \frac{\left(x + 4\right)^{2}}{2} \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =(x+4){e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =\frac{(x+4)}{{e}^{y}} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & =(x+4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (x+4)\,\text{d}x \\ \int {e}^{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (x+4)\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (x+4)\,\text{d}x \\ {e}^{y} & =\frac{{(x+4)}^{2}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{y}=\frac{{(x+4)}^{2}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\operatorname{ln}⁡(\frac{{(x+4)}^{2}}{2}+C).
$$

Use intervals where the logarithm argument is positive.

## Generated variant — negative_exp

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=(x-4){e}^{-y}.$ Assume $x-4>0.$

- $y=C + \frac{\left(x - 4\right)^{2}}{2}$
- $y=\ln{\left(C - \frac{\left(x - 4\right)^{2}}{2} \right)}$
- $y=C + \ln{\left(\frac{\left(x - 4\right)^{2}}{2} \right)}$
- $y=\ln{\left(C + \frac{\left(x - 4\right)^{2}}{2} \right)}$ (correct)
- $y=\ln{\left(C + x - 4 \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =(x-4){e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =\frac{(x-4)}{{e}^{y}} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & =(x-4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (x-4)\,\text{d}x \\ \int {e}^{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (x-4)\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (x-4)\,\text{d}x \\ {e}^{y} & =\frac{{(x-4)}^{2}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{y}=\frac{{(x-4)}^{2}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\operatorname{ln}⁡(\frac{{(x-4)}^{2}}{2}+C).
$$

Use intervals where the logarithm argument is positive.

## Generated variant — negative_exp

Profile: `observed_negative_exp` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=(x+2){e}^{-y}.$

- $y=\frac{{(x+2)}^{2}}{2}+C$
- $y=\operatorname{ln}⁡(\frac{(x+2)}{2})+C$
- $y=\frac{\operatorname{ln}⁡({(x+2)}^{2})}{2}+C$
- $y=\operatorname{ln}⁡(\frac{{(x+2)}^{2}}{2})+C$
- $y=\operatorname{ln}⁡(\frac{{(x+2)}^{2}}{2}+C)$ (correct)

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =(x+2){e}^{-y} \\ \frac{\text{d}y}{\text{d}x} & =\frac{(x+2)}{{e}^{y}} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & =(x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (x+2)\,\text{d}x \\ \int {e}^{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int (x+2)\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int (x+2)\,\text{d}x \\ {e}^{y} & =\frac{{(x+2)}^{2}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{y}=\frac{{(x+2)}^{2}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\operatorname{ln}⁡(\frac{{(x+2)}^{2}}{2}+C).
$$

## Original replay — cube_power

Profile: `observed_cube_power` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 0}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=6x\sqrt[3]{{y}^{2}}$ for $y\ne 0.$

- $y=({x}^{2}+C)^{3}$ (correct)
- $y=\sqrt[3]{6x+C}$
- $y=(6x+C)^{3}$
- $y={x}^{6}+C$
- $y=\sqrt[3]{{x}^{2}+C}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =6x\sqrt[3]{{y}^{2}} \\ \frac{\text{d}y}{\text{d}x} & =2x\cdot 3\sqrt[3]{{y}^{2}} \\ \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2x\,\text{d}x \\ \int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \text{d}y & =\int 2x\,\text{d}x \\ \frac{1}{3}\int {y}^{-2/3}\,\text{d}y & =\int 2x\,\text{d}x \\ {y}^{1/3} & ={x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{1/3}={x}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=({x}^{2}+C)^{3}.
$$

## Generated variant — cube_power

Profile: `operation_errors` (authored complete operation bank).

{"h": 4}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=6(x+4)\sqrt[3]{{y}^{2}}$ for $y\ne 0.$

- $y=C + \left(x + 4\right)^{6}$
- $y=C + \left(x + 4\right)^{2}$
- $y=\left(C + \left(x + 4\right)^{2}\right)^{3}$ (correct)
- $y=\left(C + 2 x + 8\right)^{3}$
- $y=\left(C - \left(x + 4\right)^{2}\right)^{3}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =6(x+4)\sqrt[3]{{y}^{2}} \\ \frac{\text{d}y}{\text{d}x} & =2(x+4)\cdot 3\sqrt[3]{{y}^{2}} \\ \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =2(x+4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2(x+4)\,\text{d}x \\ \int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2(x+4)\,\text{d}x \\ \int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \text{d}y & =\int 2(x+4)\,\text{d}x \\ \frac{1}{3}\int {y}^{-2/3}\,\text{d}y & =\int 2(x+4)\,\text{d}x \\ {y}^{1/3} & ={(x+4)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{1/3}={(x+4)}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=({(x+4)}^{2}+C)^{3}.
$$

Use the real cube root during separation, on intervals where $y\ne 0.$

## Generated variant — cube_power

Profile: `operation_errors` (authored complete operation bank).

{"h": -4}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=6(x-4)\sqrt[3]{{y}^{2}}$ for $y\ne 0.$

- $y=C + \left(x - 4\right)^{2}$
- $y=\left(C - \left(x - 4\right)^{2}\right)^{3}$
- $y=C + \left(x - 4\right)^{6}$
- $y=\left(C + \left(x - 4\right)^{2}\right)^{3}$ (correct)
- $y=\left(C + 2 x - 8\right)^{3}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =6(x-4)\sqrt[3]{{y}^{2}} \\ \frac{\text{d}y}{\text{d}x} & =2(x-4)\cdot 3\sqrt[3]{{y}^{2}} \\ \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =2(x-4)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2(x-4)\,\text{d}x \\ \int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2(x-4)\,\text{d}x \\ \int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \text{d}y & =\int 2(x-4)\,\text{d}x \\ \frac{1}{3}\int {y}^{-2/3}\,\text{d}y & =\int 2(x-4)\,\text{d}x \\ {y}^{1/3} & ={(x-4)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{1/3}={(x-4)}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=({(x-4)}^{2}+C)^{3}.
$$

Use the real cube root during separation, on intervals where $y\ne 0.$

## Generated variant — cube_power

Profile: `observed_cube_power` (observed expression-shape bank; wrong-option intent unresolved).

{"h": 2}

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=6(x+2)\sqrt[3]{{y}^{2}}$ for $y\ne 0.$

- $y=\sqrt[3]{{(x+2)}^{2}+C}$
- $y=(6(x+2)+C)^{3}$
- $y=({(x+2)}^{2}+C)^{3}$ (correct)
- $y={(x+2)}^{6}+C$
- $y=\sqrt[3]{6(x+2)+C}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =6(x+2)\sqrt[3]{{y}^{2}} \\ \frac{\text{d}y}{\text{d}x} & =2(x+2)\cdot 3\sqrt[3]{{y}^{2}} \\ \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =2(x+2)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2(x+2)\,\text{d}x \\ \int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2(x+2)\,\text{d}x \\ \int \frac{1}{3\sqrt[3]{{y}^{2}}}\cdot \text{d}y & =\int 2(x+2)\,\text{d}x \\ \frac{1}{3}\int {y}^{-2/3}\,\text{d}y & =\int 2(x+2)\,\text{d}x \\ {y}^{1/3} & ={(x+2)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{1/3}={(x+2)}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=({(x+2)}^{2}+C)^{3}.
$$

## Generated variant — canonical_root

Profile: `operation_errors` (authored complete operation bank).

{"h": 4, "a": 2, "n": 3}

Find the general solution to the differential equation $y′=\frac{2 \left(x + 4\right)^{3}}{y}.$ Assume $x+4>0.$ Take both sign branches on intervals where the radicand is positive and $y\ne 0.$

- $y=\pm \sqrt{C + 4 \left(x + 4\right)^{3}}$
- $y=\pm \sqrt{C + \left(x + 4\right)^{4}}$ (correct)
- $y=C + \frac{\left(x + 4\right)^{4}}{2}$
- $y=C + \left(x + 4\right)^{2}$
- $y=\pm \sqrt{C - \left(x + 4\right)^{4}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =\frac{2 \left(x + 4\right)^{3}}{y} \\ y\,\frac{\mathrm{d}y}{\mathrm{d}x} & =2 \left(x + 4\right)^{3}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int y\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int 2 \left(x + 4\right)^{3}\,\mathrm{d}x \\ \int y\,\mathrm{d}y & =\int 2 \left(x + 4\right)^{3}\,\mathrm{d}x \\ \frac{y^{2}}{2} & =\frac{\left(x + 4\right)^{4}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{2}}{2}=\frac{\left(x + 4\right)^{4}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y^2 & =\left(x + 4\right)^{4}+2C \\ y & =\pm\sqrt{\left(x + 4\right)^{4}+2C} \\ y & =\pm\sqrt{\left(x + 4\right)^{4}+K}\end{aligned}
$$

where $K=2C$ is an arbitrary real constant. Use either sign consistently on each interval where the radicand is positive.

## Generated variant — canonical_root

Profile: `operation_errors` (authored complete operation bank).

{"h": 4, "a": 1, "n": 4}

Find the general solution to the differential equation $y′=\frac{\left(x + 4\right)^{4}}{y}.$ Assume $x+4>0.$ Take both sign branches on intervals where the radicand is positive and $y\ne 0.$

- $y=\pm \sqrt{C + 2 \left(x + 4\right)^{4}}$
- $y=\pm \sqrt{C + \frac{2 \left(x + 4\right)^{5}}{5}}$ (correct)
- $y=C + \frac{\sqrt{10} \sqrt{\left(x + 4\right)^{5}}}{5}$
- $y=C + \frac{\left(x + 4\right)^{5}}{5}$
- $y=\pm \sqrt{C - \frac{2 \left(x + 4\right)^{5}}{5}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =\frac{\left(x + 4\right)^{4}}{y} \\ y\,\frac{\mathrm{d}y}{\mathrm{d}x} & =\left(x + 4\right)^{4}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int y\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int \left(x + 4\right)^{4}\,\mathrm{d}x \\ \int y\,\mathrm{d}y & =\int \left(x + 4\right)^{4}\,\mathrm{d}x \\ \frac{y^{2}}{2} & =\frac{\left(x + 4\right)^{5}}{5}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{2}}{2}=\frac{\left(x + 4\right)^{5}}{5}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y^2 & =\frac{2 \left(x + 4\right)^{5}}{5}+2C \\ y & =\pm\sqrt{\frac{2 \left(x + 4\right)^{5}}{5}+2C} \\ y & =\pm\sqrt{\frac{2 \left(x + 4\right)^{5}}{5}+K}\end{aligned}
$$

where $K=2C$ is an arbitrary real constant. Use either sign consistently on each interval where the radicand is positive.

## Generated variant — canonical_root

Profile: `operation_errors` (authored complete operation bank).

{"h": 3, "a": 3, "n": 4}

Find the general solution to the differential equation $y′=\frac{3 \left(x + 3\right)^{4}}{y}.$ Assume $x+3>0.$ Take both sign branches on intervals where the radicand is positive and $y\ne 0.$

- $y=\pm \sqrt{C - \frac{6 \left(x + 3\right)^{5}}{5}}$
- $y=\pm \sqrt{C + \frac{6 \left(x + 3\right)^{5}}{5}}$ (correct)
- $y=\pm \sqrt{C + 6 \left(x + 3\right)^{4}}$
- $y=C + \frac{3 \left(x + 3\right)^{5}}{5}$
- $y=C + \frac{\sqrt{30} \sqrt{\left(x + 3\right)^{5}}}{5}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =\frac{3 \left(x + 3\right)^{4}}{y} \\ y\,\frac{\mathrm{d}y}{\mathrm{d}x} & =3 \left(x + 3\right)^{4}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int y\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int 3 \left(x + 3\right)^{4}\,\mathrm{d}x \\ \int y\,\mathrm{d}y & =\int 3 \left(x + 3\right)^{4}\,\mathrm{d}x \\ \frac{y^{2}}{2} & =\frac{3 \left(x + 3\right)^{5}}{5}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{2}}{2}=\frac{3 \left(x + 3\right)^{5}}{5}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y^2 & =\frac{6 \left(x + 3\right)^{5}}{5}+2C \\ y & =\pm\sqrt{\frac{6 \left(x + 3\right)^{5}}{5}+2C} \\ y & =\pm\sqrt{\frac{6 \left(x + 3\right)^{5}}{5}+K}\end{aligned}
$$

where $K=2C$ is an arbitrary real constant. Use either sign consistently on each interval where the radicand is positive.

## Generated variant — intro_log

Profile: `operation_errors` (authored complete operation bank).

{"a": -5, "b": -2}

Find the general solution to the differential equation $y′=- 5 e^{- 2 x - y}.$ Work on intervals where the logarithm argument is positive.

- $y=C + \frac{5 e^{- 2 x}}{2}$
- $y=\ln{\left(C + \frac{5 e^{- 2 x}}{2} \right)}$ (correct)
- $y=\ln{\left(C - 5 e^{- 2 x} \right)}$
- $y=C + \ln{\left(\frac{5 e^{- 2 x}}{2} \right)}$
- $y=\ln{\left(C - \frac{5 e^{- 2 x}}{2} \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =- 5 e^{- 2 x - y} \\ e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x} & =- 5 e^{- 2 x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int - 5 e^{- 2 x}\,\mathrm{d}x \\ \int e^{y}\,\mathrm{d}y & =\int - 5 e^{- 2 x}\,\mathrm{d}x \\ e^{y} & =\frac{5 e^{- 2 x}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
e^{y}=\frac{5 e^{- 2 x}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\ln{\left(C + \frac{5 e^{- 2 x}}{2} \right)}.
$$

The logarithm argument must be positive on the solution interval; $C$ is an arbitrary real constant.

## Generated variant — intro_log

Profile: `operation_errors` (authored complete operation bank).

{"a": -5, "b": -5}

Find the general solution to the differential equation $y′=- 5 e^{- 5 x - y}.$ Work on intervals where the logarithm argument is positive.

- $y=\ln{\left(C - 5 e^{- 5 x} \right)}$
- $y=\ln{\left(C + e^{- 5 x} \right)}$ (correct)
- $y=C - 5 x$
- $y=C + e^{- 5 x}$
- $y=\ln{\left(C - e^{- 5 x} \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =- 5 e^{- 5 x - y} \\ e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x} & =- 5 e^{- 5 x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int - 5 e^{- 5 x}\,\mathrm{d}x \\ \int e^{y}\,\mathrm{d}y & =\int - 5 e^{- 5 x}\,\mathrm{d}x \\ e^{y} & =e^{- 5 x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
e^{y}=e^{- 5 x}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\ln{\left(C + e^{- 5 x} \right)}.
$$

The logarithm argument must be positive on the solution interval; $C$ is an arbitrary real constant.

## Generated variant — intro_log

Profile: `operation_errors` (authored complete operation bank).

{"a": 4, "b": 3}

Find the general solution to the differential equation $y′=4 e^{3 x - y}.$ Work on intervals where the logarithm argument is positive.

- $y=\ln{\left(C - \frac{4 e^{3 x}}{3} \right)}$
- $y=\ln{\left(C + \frac{4 e^{3 x}}{3} \right)}$ (correct)
- $y=\ln{\left(C + 4 e^{3 x} \right)}$
- $y=C + \frac{4 e^{3 x}}{3}$
- $y=C + \ln{\left(\frac{4 e^{3 x}}{3} \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =4 e^{3 x - y} \\ e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x} & =4 e^{3 x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int 4 e^{3 x}\,\mathrm{d}x \\ \int e^{y}\,\mathrm{d}y & =\int 4 e^{3 x}\,\mathrm{d}x \\ e^{y} & =\frac{4 e^{3 x}}{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
e^{y}=\frac{4 e^{3 x}}{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\ln{\left(C + \frac{4 e^{3 x}}{3} \right)}.
$$

The logarithm argument must be positive on the solution interval; $C$ is an arbitrary real constant.
