# Source fidelity and generated peer review

Captured math basis 1356. Originals below are evidence; repaired and authored learner records are labeled.

## Original q-48707

Susan, the new receptionist of the Smithsonian Museum in Washington DC, uses the following three functions to model the daily number of visitors to the museum $t$ minutes after the museum has opened.

- $N(t)$ - the number of people inside the museum
- $E(t)$ - the rate at which people enter the museum
- $L(t)$ - the rate at which people leave the museum

What is the relationship between the three functions above?

### Original complete bank

- $N(t) = E(t) + L(t)$
- $N^{′}(t) = E(t) - L(t)$
- $N^{′}(t) = E(t) \cdot L(t)$
- $N^{′}(t) = E(t) + L(t)$
- $N(t) = E(t) - L(t)$

### Original solution

(Solution missing in capture.)

### Generated peer variant — source-template prose, documented repairs

## moderate — q_48707 (museum_net)

Susan, the new receptionist of the Smithsonian Museum in Washington DC, uses the following three functions to model the daily number of visitors to the museum $u$ minutes after the museum has opened.

- $W(u)$ - the number of people inside the museum
- $H(u)$ - the rate at which people enter the museum
- $V(u)$ - the rate at which people leave the museum

What is the relationship between the three functions above?

- $W^{′}(u) = H(u) - V(u)$ **Correct**
- $W(u) = H(u) - V(u)$
- $W^{′}(u) = H(u) \cdot V(u)$
- $W(u) = H(u) + V(u)$
- $W^{′}(u) = H(u) + V(u)$

**Worked solution**

The function $W(u)$ gives the number of people inside the museum $u$ minutes after opening. Then,

$$
W'(u) = \dfrac{\textrm{d}W(u)}{\textrm{d}u} = \dfrac{\textrm{Change in }W}{\textrm{Change in }u}.
$$

Thus, $W'(u)$ gives the rate at which the number of people inside the museum changes $u$ minutes after opening.

In addition, we can compute the rate of change of the number of people inside the museum at time $u$ by finding the difference between the entry and exit rates at time $u.$ That is,

$$
W'(u) = H(u) - V(u).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## moderate — q_48707 (museum_net)

Susan, the new receptionist of the Smithsonian Museum in Washington DC, uses the following three functions to model the daily number of visitors to the museum $s$ minutes after the museum has opened.

- $V(s)$ - the number of people inside the museum
- $A(s)$ - the rate at which people enter the museum
- $G(s)$ - the rate at which people leave the museum

What is the relationship between the three functions above?

- $V^{′}(s) = A(s) - G(s)$ **Correct**
- $V^{′}(s) = A(s) + G(s)$
- $V(s) = A(s) - G(s)$
- $V(s) = A(s) + G(s)$
- $V^{′}(s) = A(s) \cdot G(s)$

**Worked solution**

The function $V(s)$ gives the number of people inside the museum $s$ minutes after opening. Then,

$$
V'(s) = \dfrac{\textrm{d}V(s)}{\textrm{d}s} = \dfrac{\textrm{Change in }V}{\textrm{Change in }s}.
$$

Thus, $V'(s)$ gives the rate at which the number of people inside the museum changes $s$ minutes after opening.

In addition, we can compute the rate of change of the number of people inside the museum at time $s$ by finding the difference between the entry and exit rates at time $s.$ That is,

$$
V'(s) = A(s) - G(s).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

## Original q-72004

Jason, a biologist, is measuring the growth of bacteria in a Petri dish by recording the following two numbers for different values of $t,$ where $t$ is the time, in hours, since he started his observations:

- $N(t)$ - the number of bacteria in the dish.

- $r(t)$ - the rate at which the number of bacteria in the dish is increasing.

What is the relationship between $N(t)$ and $r(t)?$

### Original complete bank

- $N(t)=r(t)$
- $N(t)={r}^{′}(t)$
- ${N}^{′}(t)=r(t)$
- $N(t)=-{r}^{′}(t)$
- ${N}^{′}(t)=-r(t)$

### Original solution

The function $N(t)$ gives the number of bacteria inside the dish after $t$ hours. Then,

$$
{N}^{′}(t)=\frac{\text{d}N(t)}{\text{d}t}=\frac{\text{Change in }N}{\text{Change in }t}.
$$

Thus, ${N}^{′}(t)$ gives the rate at which the number of bacteria is increasing at time $t$, which is the same as $r(t).$ Therefore, the relationship between $N(t)$ and $r(t)$ is ${N}^{′}(t)=r(t).$

### Generated peer variant — source-template prose, documented repairs

## easy — q_72004 (single_sign)

Jason, a biologist, is measuring the growth of bacteria in a Petri dish by recording the following two numbers for different values of $u,$ where $u$ is the time, in hours, since he started his observations:

- $W(u)$ - the number of bacteria in the dish.

- $h(u)$ - the rate at which the number of bacteria in the dish is increasing.

What is the relationship between $W(u)$ and $h(u)?$

- $W(u)={h}^{′}(u)$
- ${W}^{′}(u)=-h(u)$
- ${W}^{′}(u)=h(u)$ **Correct**
- $W(u)=h(u)$
- $W(u)=-{h}^{′}(u)$

**Worked solution**

The function $W(u)$ gives the number of bacteria inside the dish after $u$ hours. Then,

$$
{W}^{′}(u)=\frac{\text{d}W(u)}{\text{d}u}=\frac{\text{Change in }W}{\text{Change in }u}.
$$

Thus, ${W}^{′}(u)$ gives the rate at which the number of bacteria is increasing at time $u$, which is the same as $h(u).$ Therefore, the relationship between $W(u)$ and $h(u)$ is ${W}^{′}(u)=h(u).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## easy — q_72004 (single_sign)

Jason, a biologist, is measuring the growth of bacteria in a Petri dish by recording the following two numbers for different values of $s,$ where $s$ is the time, in hours, since he started his observations:

- $V(s)$ - the number of bacteria in the dish.

- $a(s)$ - the rate at which the number of bacteria in the dish is increasing.

What is the relationship between $V(s)$ and $a(s)?$

- $V(s)={a}^{′}(s)$
- $V(s)=-{a}^{′}(s)$
- ${V}^{′}(s)=-a(s)$
- $V(s)=a(s)$
- ${V}^{′}(s)=a(s)$ **Correct**

**Worked solution**

The function $V(s)$ gives the number of bacteria inside the dish after $s$ hours. Then,

$$
{V}^{′}(s)=\frac{\text{d}V(s)}{\text{d}s}=\frac{\text{Change in }V}{\text{Change in }s}.
$$

Thus, ${V}^{′}(s)$ gives the rate at which the number of bacteria is increasing at time $s$, which is the same as $a(s).$ Therefore, the relationship between $V(s)$ and $a(s)$ is ${V}^{′}(s)=a(s).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

## Original q-112509

Joseph is measuring the height reached by his lime tree by recording the following two numbers for different values of $t,$ where $t$ is the time, in years, since he planted the tree:

- $H(t)$ - The tree's height, in centimeters

- $r(t)$ - the rate at which the tree's height is increasing.

What is the relationship between $H(t)$ and $r(t)?$

### Original complete bank

(Field missing in capture.)

### Original solution

The function $H(t)$ gives the tree's height after $t$ years. Then,

$$
{H}^{'}(t)=\frac{\text{d}H(t)}{\text{d}t}=\frac{\text{Change in }H}{\text{Change in }t}.
$$

Thus, ${H}^{'}(t)$ gives the rate at which the height of the tree increases at time $t$, which is the same as $r(t).$ Therefore, the relationship between $H(t)$ and $r(t)$ is ${H}^{'}(t)=r(t).$

### Generated peer variant — source-template prose, documented repairs

## easy — q_112509 (single_sign)

Joseph is measuring the height reached by his lime tree by recording the following two numbers for different values of $u,$ where $u$ is the time, in years, since he planted the tree:

- $W(u)$ - The tree's height, in centimeters

- $h(u)$ - the rate at which the tree's height is increasing.

What is the relationship between $W(u)$ and $h(u)?$

- $W(u)={h}^{′}(u)$
- ${W}^{′}(u)=-h(u)$
- ${W}^{′}(u)=h(u)$ **Correct**
- $W(u)=h(u)$
- $W(u)=-{h}^{′}(u)$

**Worked solution**

The function $W(u)$ gives the tree's height after $u$ years. Then,

$$
{W}^{'}(u)=\frac{\text{d}W(u)}{\text{d}u}=\frac{\text{Change in }W}{\text{Change in }u}.
$$

Thus, ${W}^{'}(u)$ gives the rate at which the height of the tree increases at time $u$, which is the same as $h(u).$ Therefore, the relationship between $W(u)$ and $h(u)$ is ${W}^{'}(u)=h(u).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## easy — q_112509 (single_sign)

Joseph is measuring the height reached by his lime tree by recording the following two numbers for different values of $s,$ where $s$ is the time, in years, since he planted the tree:

- $V(s)$ - The tree's height, in centimeters

- $a(s)$ - the rate at which the tree's height is increasing.

What is the relationship between $V(s)$ and $a(s)?$

- $V(s)={a}^{′}(s)$
- $V(s)=-{a}^{′}(s)$
- ${V}^{′}(s)=-a(s)$
- $V(s)=a(s)$
- ${V}^{′}(s)=a(s)$ **Correct**

**Worked solution**

The function $V(s)$ gives the tree's height after $s$ years. Then,

$$
{V}^{'}(s)=\frac{\text{d}V(s)}{\text{d}s}=\frac{\text{Change in }V}{\text{Change in }s}.
$$

Thus, ${V}^{'}(s)$ gives the rate at which the height of the tree increases at time $s$, which is the same as $a(s).$ Therefore, the relationship between $V(s)$ and $a(s)$ is ${V}^{'}(s)=a(s).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

## Original q-48923

To measure the success of an amusement park, Ed uses the following three functions that model the daily number of visitors to the park $t$ minutes after the park is opened to the public.

- $N(t)$ - the number of people inside the park

- $E(t)$ - the rate at which people enter the park

- $L(t)$ - the rate at which people leave the park

What is the relationship between the functions above?

### Original complete bank

(Field missing in capture.)

### Original solution

The function $N(t)$ gives the number of people inside the park $t$ minutes after opening. Then,

$$
{N}^{'}(t)=\frac{\text{d}N(t)}{\text{d}t}=\frac{\text{Change in }N}{\text{Change in }t}.
$$

Thus, ${N}^{'}(t)$ gives the rate at which the number of people inside the park changes $t$ minutes after opening.

In addition, we can compute the rate of change of the number of people inside the park at time $t$ by finding the difference between the entry and exit rates at time $t.$ That is,

$$
{N}^{'}(t)=E(t)-L(t).
$$

### Generated peer variant — source-template prose, documented repairs

## moderate — q_48923 (net_standard)

To measure the success of an amusement park, Ed uses the following three functions that model the daily number of visitors to the park $u$ minutes after the park is opened to the public.

- $W(u)$ - the number of people inside the park

- $H(u)$ - the rate at which people enter the park

- $V(u)$ - the rate at which people leave the park

What is the relationship between the functions above?

- ${W}^{′}(u)=H(u)-V(u)$ **Correct**
- ${W}^{′}(u)=H(u)\cdot V(u)$
- $W(u)=H(u)+V(u)$
- ${W}^{′}(u)=H(u)+V(u)$
- $W(u)=H(u)-V(u)$

**Worked solution**

The function $W(u)$ gives the number of people inside the park $u$ minutes after opening. Then,

$$
{W}^{'}(u)=\frac{\text{d}W(u)}{\text{d}u}=\frac{\text{Change in }W}{\text{Change in }u}.
$$

Thus, ${W}^{'}(u)$ gives the rate at which the number of people inside the park changes $u$ minutes after opening.

In addition, we can compute the rate of change of the number of people inside the park at time $u$ by finding the difference between the entry and exit rates at time $u.$ That is,

$$
{W}^{'}(u)=H(u)-V(u).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## moderate — q_48923 (net_standard)

To measure the success of an amusement park, Ed uses the following three functions that model the daily number of visitors to the park $s$ minutes after the park is opened to the public.

- $V(s)$ - the number of people inside the park

- $A(s)$ - the rate at which people enter the park

- $G(s)$ - the rate at which people leave the park

What is the relationship between the functions above?

- ${V}^{′}(s)=A(s)-G(s)$ **Correct**
- $V(s)=A(s)-G(s)$
- ${V}^{′}(s)=A(s)\cdot G(s)$
- ${V}^{′}(s)=A(s)+G(s)$
- $V(s)=A(s)+G(s)$

**Worked solution**

The function $V(s)$ gives the number of people inside the park $s$ minutes after opening. Then,

$$
{V}^{'}(s)=\frac{\text{d}V(s)}{\text{d}s}=\frac{\text{Change in }V}{\text{Change in }s}.
$$

Thus, ${V}^{'}(s)$ gives the rate at which the number of people inside the park changes $s$ minutes after opening.

In addition, we can compute the rate of change of the number of people inside the park at time $s$ by finding the difference between the entry and exit rates at time $s.$ That is,

$$
{V}^{'}(s)=A(s)-G(s).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

## Original q-72109

Ramin, a bricklayer, is monitoring the construction of a wall by recording the following two numbers for different values of $t,$ where $t$ is the time, in hours, since he started his observations:

- $B(t)$ - the number of bricks in the wall.

- $r(t)$ - the rate at which the number of bricks in the wall is increasing.

What is the relationship between $B(t)$ and $r(t)?$

### Original complete bank

(Field missing in capture.)

### Original solution

The function $B(t)$ gives the number of bricks inside the wall after $t$ hours. Then,

$$
{B}^{'}(t)=\frac{\text{d}B(t)}{\text{d}t}=\frac{\text{Change in }B}{\text{Change in }t}.
$$

Thus, ${B}^{'}(t)$ gives the rate at which the number of bricks increases at time $t$, which is the same as $r(t).$ Therefore, the relationship between $B(t)$ and $r(t)$ is ${B}^{'}(t)=r(t).$

### Generated peer variant — source-template prose, documented repairs

## easy — q_72109 (single_sign)

Ramin, a bricklayer, is monitoring the construction of a wall by recording the following two numbers for different values of $u,$ where $u$ is the time, in hours, since he started his observations:

- $W(u)$ - the number of bricks in the wall.

- $h(u)$ - the rate at which the number of bricks in the wall is increasing.

What is the relationship between $W(u)$ and $h(u)?$

- $W(u)={h}^{′}(u)$
- ${W}^{′}(u)=-h(u)$
- ${W}^{′}(u)=h(u)$ **Correct**
- $W(u)=h(u)$
- $W(u)=-{h}^{′}(u)$

**Worked solution**

The function $W(u)$ gives the number of bricks inside the wall after $u$ hours. Then,

$$
{W}^{'}(u)=\frac{\text{d}W(u)}{\text{d}u}=\frac{\text{Change in }W}{\text{Change in }u}.
$$

Thus, ${W}^{'}(u)$ gives the rate at which the number of bricks increases at time $u$, which is the same as $h(u).$ Therefore, the relationship between $W(u)$ and $h(u)$ is ${W}^{'}(u)=h(u).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## easy — q_72109 (single_sign)

Ramin, a bricklayer, is monitoring the construction of a wall by recording the following two numbers for different values of $s,$ where $s$ is the time, in hours, since he started his observations:

- $V(s)$ - the number of bricks in the wall.

- $a(s)$ - the rate at which the number of bricks in the wall is increasing.

What is the relationship between $V(s)$ and $a(s)?$

- $V(s)={a}^{′}(s)$
- $V(s)=-{a}^{′}(s)$
- ${V}^{′}(s)=-a(s)$
- $V(s)=a(s)$
- ${V}^{′}(s)=a(s)$ **Correct**

**Worked solution**

The function $V(s)$ gives the number of bricks inside the wall after $s$ hours. Then,

$$
{V}^{'}(s)=\frac{\text{d}V(s)}{\text{d}s}=\frac{\text{Change in }V}{\text{Change in }s}.
$$

Thus, ${V}^{'}(s)$ gives the rate at which the number of bricks increases at time $s$, which is the same as $a(s).$ Therefore, the relationship between $V(s)$ and $a(s)$ is ${V}^{'}(s)=a(s).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

## Original q-112518

Liam, a farmer, is monitoring the construction of a fence by recording the following two numbers for different values of $t,$ where $t$ is the time, in hours, since he started his observations:

- $P(t)$ - the number of panels in the fence.

- $r(t)$ - the rate at which the number of panels in the fence increases.

What is the relationship between $P(t)$ and $r(t)?$

### Original complete bank

- ${P}^{′}(t)=\frac{1}{r(t)}$
- $P(t)={r}^{2}(t)$
- ${P}^{′}(t)=r(t)$
- $P(t)={r}^{′}(t)$
- ${P}^{′}(t)=1-r(t)$

### Original solution

The function $P(t)$ gives the number of panels in the fence after $t$ hours. Then,

$$
{P}^{′}(t)=\frac{\text{d}P(t)}{\text{d}t}=\frac{\text{Change in }P}{\text{Change in }t}.
$$

Thus, ${P}^{′}(t)$ gives the rate at which the number of panels increases at time $t$, which is the same as $r(t).$ Therefore, the relationship between $P(t)$ and $r(t)$ is ${P}^{′}(t)=r(t).$

### Generated peer variant — source-template prose, documented repairs

## easy — q_112518 (single_reciprocal)

Liam, a farmer, is monitoring the construction of a fence by recording the following two numbers for different values of $u,$ where $u$ is the time, in hours, since he started his observations:

- $W(u)$ - the number of panels in the fence.

- $h(u)$ - the rate at which the number of panels in the fence increases.

What is the relationship between $W(u)$ and $h(u)?$

- $W(u)={h}^{2}(u)$
- ${W}^{′}(u)=1-h(u)$
- ${W}^{′}(u)=h(u)$ **Correct**
- ${W}^{′}(u)=\frac{1}{h(u)}$
- $W(u)={h}^{′}(u)$

**Worked solution**

The function $W(u)$ gives the number of panels in the fence after $u$ hours. Then,

$$
{W}^{′}(u)=\frac{\text{d}W(u)}{\text{d}u}=\frac{\text{Change in }W}{\text{Change in }u}.
$$

Thus, ${W}^{′}(u)$ gives the rate at which the number of panels increases at time $u$, which is the same as $h(u).$ Therefore, the relationship between $W(u)$ and $h(u)$ is ${W}^{′}(u)=h(u).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## easy — q_112518 (single_reciprocal)

Liam, a farmer, is monitoring the construction of a fence by recording the following two numbers for different values of $s,$ where $s$ is the time, in hours, since he started his observations:

- $V(s)$ - the number of panels in the fence.

- $a(s)$ - the rate at which the number of panels in the fence increases.

What is the relationship between $V(s)$ and $a(s)?$

- $V(s)={a}^{2}(s)$
- $V(s)={a}^{′}(s)$
- ${V}^{′}(s)=1-a(s)$
- ${V}^{′}(s)=\frac{1}{a(s)}$
- ${V}^{′}(s)=a(s)$ **Correct**

**Worked solution**

The function $V(s)$ gives the number of panels in the fence after $s$ hours. Then,

$$
{V}^{′}(s)=\frac{\text{d}V(s)}{\text{d}s}=\frac{\text{Change in }V}{\text{Change in }s}.
$$

Thus, ${V}^{′}(s)$ gives the rate at which the number of panels increases at time $s$, which is the same as $a(s).$ Therefore, the relationship between $V(s)$ and $a(s)$ is ${V}^{′}(s)=a(s).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

## Original q-112519

To measure the number of children visiting a playground, Noah uses the following three functions that model the hourly number of visitors to the playground $t$ hours after the playground is opened to the public.

- $N(t)$ - the number of children inside the playground

- $E(t)$ - the rate at which children enter the playground

- $L(t)$ - the rate at which children leave the playground

What is the relationship between the functions above?

### Original complete bank

- ${N}^{′}(t)=E(t)+L(t)$
- ${N}^{′}(t)=E(t)-L(t)$
- $N(t)=E(t)+L(t)$
- $N(t)=E(t)-L(t)$
- ${N}^{′}(t)=E(t)\cdot L(t)$

### Original solution

The function $N(t)$ gives the number of children inside the park $t$ minutes after opening. Then,

$$
{N}^{′}(t)=\frac{\text{d}N(t)}{\text{d}t}=\frac{\text{Change in }N}{\text{Change in }t}.
$$

Thus, ${N}^{′}(t)$ gives the rate at which the number of children inside the playground changes $t$ hours after opening.

In addition, we can compute the rate of change of the number of children inside the playground at time $t$ by finding the difference between the entry and exit rates at time $t.$ That is,

$$
{N}^{′}(t)=E(t)-L(t).
$$

### Generated peer variant — source-template prose, documented repairs

## easy — q_112519 (net_standard)

To measure the number of children visiting a playground, Noah uses the following three functions that model the hourly number of visitors to the playground $u$ hours after the playground is opened to the public.

- $W(u)$ - the number of children inside the playground

- $H(u)$ - the rate at which children enter the playground

- $V(u)$ - the rate at which children leave the playground

What is the relationship between the functions above?

- ${W}^{′}(u)=H(u)-V(u)$ **Correct**
- ${W}^{′}(u)=H(u)\cdot V(u)$
- $W(u)=H(u)+V(u)$
- ${W}^{′}(u)=H(u)+V(u)$
- $W(u)=H(u)-V(u)$

**Worked solution**

The function $W(u)$ gives the number of children inside the playground $u$ hours after opening. Then,

$$
{W}^{′}(u)=\frac{\text{d}W(u)}{\text{d}u}=\frac{\text{Change in }W}{\text{Change in }u}.
$$

Thus, ${W}^{′}(u)$ gives the rate at which the number of children inside the playground changes $u$ hours after opening.

In addition, we can compute the rate of change of the number of children inside the playground at time $u$ by finding the difference between the entry and exit rates at time $u.$ That is,

$$
{W}^{′}(u)=H(u)-V(u).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## easy — q_112519 (net_standard)

To measure the number of children visiting a playground, Noah uses the following three functions that model the hourly number of visitors to the playground $s$ hours after the playground is opened to the public.

- $V(s)$ - the number of children inside the playground

- $A(s)$ - the rate at which children enter the playground

- $G(s)$ - the rate at which children leave the playground

What is the relationship between the functions above?

- ${V}^{′}(s)=A(s)-G(s)$ **Correct**
- $V(s)=A(s)-G(s)$
- ${V}^{′}(s)=A(s)\cdot G(s)$
- ${V}^{′}(s)=A(s)+G(s)$
- $V(s)=A(s)+G(s)$

**Worked solution**

The function $V(s)$ gives the number of children inside the playground $s$ hours after opening. Then,

$$
{V}^{′}(s)=\frac{\text{d}V(s)}{\text{d}s}=\frac{\text{Change in }V}{\text{Change in }s}.
$$

Thus, ${V}^{′}(s)$ gives the rate at which the number of children inside the playground changes $s$ hours after opening.

In addition, we can compute the rate of change of the number of children inside the playground at time $s$ by finding the difference between the entry and exit rates at time $s.$ That is,

$$
{V}^{′}(s)=A(s)-G(s).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

## Original q-112522

Oliver, the owner of a platform for chess players, uses the following three functions to model the daily number of users of the platform $t$ days after it was launched.

- $N(t)$ - the number of users with an account

- $O(t)$ - the rate at which new users open an account

- $C(t)$ - the rate at which users cancel their account

What is the relationship between the three functions above?

### Original complete bank

- $N(t)=-O(t)-C(t)$
- $N(t)=O(t)+C(t)$
- ${N}^{′}(t)=O(t)+C(t)$
- ${N}^{′}(t)=O(t)-C(t)$
- $N(t)=O(t)-C(t)$

### Original solution

The function $N(t)$ gives the number of users $t$ days after the platform is set up. Then,

$$
{N}^{′}(t)=\frac{\text{d}N(t)}{\text{d}t}=\frac{\text{Change in }N}{\text{Change in }t}.
$$

Thus, ${N}^{′}(t)$ gives the rate at which the number of users with an account changes $t$ days after opening.

In addition, we can compute the rate of change of the number of users at time $t$ by finding the difference between the open and cancel rates at time $t.$ That is,

$$
{N}^{′}(t)=O(t)-C(t).
$$

### Generated peer variant — source-template prose, documented repairs

## easy — q_112522 (net_accounts)

Oliver, the owner of a platform for chess players, uses the following three functions to model the daily number of users of the platform $u$ days after it was launched.

- $W(u)$ - the number of users with an account

- $H(u)$ - the rate at which new users open an account

- $V(u)$ - the rate at which users cancel their account

What is the relationship between the three functions above?

- $W(u)=H(u)+V(u)$
- $W(u)=H(u)-V(u)$
- ${W}^{′}(u)=H(u)+V(u)$
- $W(u)=-H(u)-V(u)$
- ${W}^{′}(u)=H(u)-V(u)$ **Correct**

**Worked solution**

The function $W(u)$ gives the number of users $u$ days after the platform is set up. Then,

$$
{W}^{′}(u)=\frac{\text{d}W(u)}{\text{d}u}=\frac{\text{Change in }W}{\text{Change in }u}.
$$

Thus, ${W}^{′}(u)$ gives the rate at which the number of users with an account changes $u$ days after opening.

In addition, we can compute the rate of change of the number of users at time $u$ by finding the difference between the open and cancel rates at time $u.$ That is,

$$
{W}^{′}(u)=H(u)-V(u).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## easy — q_112522 (net_accounts)

Oliver, the owner of a platform for chess players, uses the following three functions to model the daily number of users of the platform $s$ days after it was launched.

- $V(s)$ - the number of users with an account

- $A(s)$ - the rate at which new users open an account

- $G(s)$ - the rate at which users cancel their account

What is the relationship between the three functions above?

- $V(s)=A(s)+G(s)$
- ${V}^{′}(s)=A(s)-G(s)$ **Correct**
- $V(s)=A(s)-G(s)$
- $V(s)=-A(s)-G(s)$
- ${V}^{′}(s)=A(s)+G(s)$

**Worked solution**

The function $V(s)$ gives the number of users $s$ days after the platform is set up. Then,

$$
{V}^{′}(s)=\frac{\text{d}V(s)}{\text{d}s}=\frac{\text{Change in }V}{\text{Change in }s}.
$$

Thus, ${V}^{′}(s)$ gives the rate at which the number of users with an account changes $s$ days after opening.

In addition, we can compute the rate of change of the number of users at time $s$ by finding the difference between the open and cancel rates at time $s.$ That is,

$$
{V}^{′}(s)=A(s)-G(s).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

## Original q-72105

Douglas, a pilot, is flying a plane. The plane's control systems record two measurements for different values of $t,$ where $t$ is the time, in minutes, since take off. The two measurements are:

- $A(t)$ - the altitude (height) of the plane

- $r(t)$ the rate at which the altitude is increasing

What is the relationship between $A(t)$ and $r(t)?$

### Original complete bank

- ${A}^{′}(t)=r(t)$
- $A(t)=-{r}^{′}(t)$
- ${A}^{′}(t)=-r(t)$
- $A(t)={r}^{′}(t)$
- $A(t)=r(t)$

### Original solution

The function $A(t)$ gives the altitude of the plane after $t$ hours. Then,

$$
{A}^{′}(t)=\frac{\text{d}A(t)}{\text{d}t}=\frac{\text{Change in }A}{\text{Change in }t}.
$$

Thus, ${A}^{′}(t)$ gives the rate at which the altitude is increasing at time $t$, which is the same as $r(t).$ Therefore, the relationship between $A(t)$ and $r(t)$ is ${A}^{′}(t)=r(t).$

### Generated peer variant — source-template prose, documented repairs

## easy — q_72105 (single_sign)

Douglas, a pilot, is flying a plane. The plane's control systems record two measurements for different values of $u,$ where $u$ is the time, in minutes, since take off. The two measurements are:

- $W(u)$ - the altitude (height) of the plane

- $h(u)$ the rate at which the altitude is increasing

What is the relationship between $W(u)$ and $h(u)?$

- $W(u)={h}^{′}(u)$
- ${W}^{′}(u)=-h(u)$
- ${W}^{′}(u)=h(u)$ **Correct**
- $W(u)=h(u)$
- $W(u)=-{h}^{′}(u)$

**Worked solution**

The function $W(u)$ gives the altitude of the plane after $u$ minutes. Then,

$$
{W}^{′}(u)=\frac{\text{d}W(u)}{\text{d}u}=\frac{\text{Change in }W}{\text{Change in }u}.
$$

Thus, ${W}^{′}(u)$ gives the rate at which the altitude is increasing at time $u$, which is the same as $h(u).$ Therefore, the relationship between $W(u)$ and $h(u)$ is ${W}^{′}(u)=h(u).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Generated peer variant — source-template prose, documented repairs

## easy — q_72105 (single_sign)

Douglas, a pilot, is flying a plane. The plane's control systems record two measurements for different values of $s,$ where $s$ is the time, in minutes, since take off. The two measurements are:

- $V(s)$ - the altitude (height) of the plane

- $a(s)$ the rate at which the altitude is increasing

What is the relationship between $V(s)$ and $a(s)?$

- $V(s)={a}^{′}(s)$
- $V(s)=-{a}^{′}(s)$
- ${V}^{′}(s)=-a(s)$
- $V(s)=a(s)$
- ${V}^{′}(s)=a(s)$ **Correct**

**Worked solution**

The function $V(s)$ gives the altitude of the plane after $s$ minutes. Then,

$$
{V}^{′}(s)=\frac{\text{d}V(s)}{\text{d}s}=\frac{\text{Change in }V}{\text{Change in }s}.
$$

Thus, ${V}^{′}(s)$ gives the rate at which the altitude is increasing at time $s$, which is the same as $a(s).$ Therefore, the relationship between $V(s)$ and $a(s)$ is ${V}^{′}(s)=a(s).$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## easy — single_growth (single_sign)

A model records the volume of water in a tank at time $t$, measured in minutes after observations begin.

- $V(t)$ - the volume of water in a tank, in liters.

- $r(t)$ - the positive rate at which that amount is increasing, in liters per minute.

What is the relationship between $V(t)$ and $r(t)$?

- ${V}^{′}(t)=r(t)$ **Correct**
- $V(t)={r}^{′}(t)$
- $V(t)=r(t)$
- ${V}^{′}(t)=-r(t)$
- $V(t)=-{r}^{′}(t)$

**Worked solution**

The function $V(t)$ gives the volume of water in a tank after $t$ minutes. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate of change of that amount. This is the same as $r(t)$. Therefore, the relationship is $V'(t)=r(t)$.

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## easy — single_growth (single_sign)

A model records the mass of grain in a silo at time $t$, measured in hours after observations begin.

- $V(t)$ - the mass of grain in a silo, in kilograms.

- $r(t)$ - the positive rate at which that amount is increasing, in kilograms per hour.

What is the relationship between $V(t)$ and $r(t)$?

- ${V}^{′}(t)=r(t)$ **Correct**
- $V(t)=-{r}^{′}(t)$
- ${V}^{′}(t)=-r(t)$
- $V(t)=r(t)$
- $V(t)={r}^{′}(t)$

**Worked solution**

The function $V(t)$ gives the mass of grain in a silo after $t$ hours. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate of change of that amount. This is the same as $r(t)$. Therefore, the relationship is $V'(t)=r(t)$.

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## easy — single_growth (single_sign)

A model records the volume of fuel in a reservoir at time $t$, measured in seconds after observations begin.

- $V(t)$ - the volume of fuel in a reservoir, in liters.

- $r(t)$ - the positive rate at which that amount is increasing, in liters per second.

What is the relationship between $V(t)$ and $r(t)$?

- ${V}^{′}(t)=r(t)$ **Correct**
- $V(t)={r}^{′}(t)$
- $V(t)=-{r}^{′}(t)$
- ${V}^{′}(t)=-r(t)$
- $V(t)=r(t)$

**Worked solution**

The function $V(t)$ gives the volume of fuel in a reservoir after $t$ seconds. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate of change of that amount. This is the same as $r(t)$. Therefore, the relationship is $V'(t)=r(t)$.

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## easy — single_growth (single_sign)

A model records the number of items in a store at time $t$, measured in days after observations begin.

- $V(t)$ - the number of items in a store, in items.

- $r(t)$ - the positive rate at which that amount is increasing, in items per day.

What is the relationship between $V(t)$ and $r(t)$?

- $V(t)=r(t)$
- ${V}^{′}(t)=r(t)$ **Correct**
- $V(t)=-{r}^{′}(t)$
- ${V}^{′}(t)=-r(t)$
- $V(t)={r}^{′}(t)$

**Worked solution**

The function $V(t)$ gives the number of items in a store after $t$ days. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate of change of that amount. This is the same as $r(t)$. Therefore, the relationship is $V'(t)=r(t)$.

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## easy — single_loss (single_loss)

A model records the volume of water in a tank at time $t$, measured in minutes after observations begin.

- $V(t)$ - the volume of water in a tank, in liters.

- $r(t)$ - the positive rate at which that amount is decreasing, in liters per minute.

What is the relationship between $V(t)$ and $r(t)$?

- ${V}^{′}(t)=-r(t)$ **Correct**
- $V(t)={r}^{′}(t)$
- $V(t)=r(t)$
- $V(t)=-r(t)$
- ${V}^{′}(t)=r(t)$

**Worked solution**

The function $V(t)$ gives the volume of water in a tank after $t$ minutes. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate of change of that amount. The amount is decreasing, so the derivative is the negative of the positive loss rate $r(t)$. Therefore, the relationship is $V'(t)=-r(t)$.

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## easy — single_loss (single_loss)

A model records the mass of grain in a silo at time $t$, measured in hours after observations begin.

- $V(t)$ - the mass of grain in a silo, in kilograms.

- $r(t)$ - the positive rate at which that amount is decreasing, in kilograms per hour.

What is the relationship between $V(t)$ and $r(t)$?

- ${V}^{′}(t)=-r(t)$ **Correct**
- ${V}^{′}(t)=r(t)$
- $V(t)=-r(t)$
- $V(t)=r(t)$
- $V(t)={r}^{′}(t)$

**Worked solution**

The function $V(t)$ gives the mass of grain in a silo after $t$ hours. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate of change of that amount. The amount is decreasing, so the derivative is the negative of the positive loss rate $r(t)$. Therefore, the relationship is $V'(t)=-r(t)$.

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## easy — single_loss (single_loss)

A model records the volume of fuel in a reservoir at time $t$, measured in seconds after observations begin.

- $V(t)$ - the volume of fuel in a reservoir, in liters.

- $r(t)$ - the positive rate at which that amount is decreasing, in liters per second.

What is the relationship between $V(t)$ and $r(t)$?

- ${V}^{′}(t)=-r(t)$ **Correct**
- $V(t)={r}^{′}(t)$
- ${V}^{′}(t)=r(t)$
- $V(t)=-r(t)$
- $V(t)=r(t)$

**Worked solution**

The function $V(t)$ gives the volume of fuel in a reservoir after $t$ seconds. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate of change of that amount. The amount is decreasing, so the derivative is the negative of the positive loss rate $r(t)$. Therefore, the relationship is $V'(t)=-r(t)$.

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## easy — single_loss (single_loss)

A model records the number of items in a store at time $t$, measured in days after observations begin.

- $V(t)$ - the number of items in a store, in items.

- $r(t)$ - the positive rate at which that amount is decreasing, in items per day.

What is the relationship between $V(t)$ and $r(t)$?

- $V(t)=r(t)$
- ${V}^{′}(t)=-r(t)$ **Correct**
- ${V}^{′}(t)=r(t)$
- $V(t)=-r(t)$
- $V(t)={r}^{′}(t)$

**Worked solution**

The function $V(t)$ gives the number of items in a store after $t$ days. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate of change of that amount. The amount is decreasing, so the derivative is the negative of the positive loss rate $r(t)$. Therefore, the relationship is $V'(t)=-r(t)$.

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## moderate — net_magnitudes (net_standard)

A model records the volume of water in a tank at time $t$, measured in minutes after observations begin.

- $V(t)$ - the volume of water in a tank, in liters.

- $E(t)$ - the positive rate at which the amount is added, in liters per minute.

- $L(t)$ - the positive rate at which the amount is removed, in liters per minute.

What is the relationship between the three functions above?

- $V(t)=E(t)+L(t)$
- ${V}^{′}(t)=E(t)-L(t)$ **Correct**
- ${V}^{′}(t)=E(t)+L(t)$
- ${V}^{′}(t)=E(t)\cdot L(t)$
- $V(t)=E(t)-L(t)$

**Worked solution**

The function $V(t)$ gives the volume of water in a tank after $t$ minutes. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate at which the amount changes at time $t$.

In addition, we can compute this rate by finding the difference between the addition and removal rates at time $t$. That is,

$$
V'(t)=E(t)-L(t).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## moderate — net_magnitudes (net_standard)

A model records the mass of grain in a silo at time $t$, measured in hours after observations begin.

- $V(t)$ - the mass of grain in a silo, in kilograms.

- $E(t)$ - the positive rate at which the amount is added, in kilograms per hour.

- $L(t)$ - the positive rate at which the amount is removed, in kilograms per hour.

What is the relationship between the three functions above?

- $V(t)=E(t)+L(t)$
- $V(t)=E(t)-L(t)$
- ${V}^{′}(t)=E(t)\cdot L(t)$
- ${V}^{′}(t)=E(t)+L(t)$
- ${V}^{′}(t)=E(t)-L(t)$ **Correct**

**Worked solution**

The function $V(t)$ gives the mass of grain in a silo after $t$ hours. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate at which the amount changes at time $t$.

In addition, we can compute this rate by finding the difference between the addition and removal rates at time $t$. That is,

$$
V'(t)=E(t)-L(t).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## moderate — net_magnitudes (net_standard)

A model records the volume of fuel in a reservoir at time $t$, measured in seconds after observations begin.

- $V(t)$ - the volume of fuel in a reservoir, in liters.

- $E(t)$ - the positive rate at which the amount is added, in liters per second.

- $L(t)$ - the positive rate at which the amount is removed, in liters per second.

What is the relationship between the three functions above?

- $V(t)=E(t)+L(t)$
- ${V}^{′}(t)=E(t)-L(t)$ **Correct**
- $V(t)=E(t)-L(t)$
- ${V}^{′}(t)=E(t)\cdot L(t)$
- ${V}^{′}(t)=E(t)+L(t)$

**Worked solution**

The function $V(t)$ gives the volume of fuel in a reservoir after $t$ seconds. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate at which the amount changes at time $t$.

In addition, we can compute this rate by finding the difference between the addition and removal rates at time $t$. That is,

$$
V'(t)=E(t)-L(t).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## moderate — net_magnitudes (net_standard)

A model records the number of items in a store at time $t$, measured in days after observations begin.

- $V(t)$ - the number of items in a store, in items.

- $E(t)$ - the positive rate at which the amount is added, in items per day.

- $L(t)$ - the positive rate at which the amount is removed, in items per day.

What is the relationship between the three functions above?

- ${V}^{′}(t)=E(t)+L(t)$
- $V(t)=E(t)+L(t)$
- $V(t)=E(t)-L(t)$
- ${V}^{′}(t)=E(t)\cdot L(t)$
- ${V}^{′}(t)=E(t)-L(t)$ **Correct**

**Worked solution**

The function $V(t)$ gives the number of items in a store after $t$ days. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate at which the amount changes at time $t$.

In addition, we can compute this rate by finding the difference between the addition and removal rates at time $t$. That is,

$$
V'(t)=E(t)-L(t).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## hard — signed_net (signed_net)

A model records the volume of water in a tank at time $t$, measured in minutes after observations begin.

- $V(t)$ - the volume of water in a tank, in liters.

- $E(t)$ - the positive rate at which the amount is added, in liters per minute.

- $L(t)$ - the signed contribution of removal to the rate of change, in liters per minute; $L(t)<0$ when removal occurs.

What is the relationship between the three functions above?

- ${V}^{′}(t)=-E(t)-L(t)$
- ${V}^{′}(t)=E(t)+L(t)$ **Correct**
- ${V}^{′}(t)=E(t)-L(t)$
- ${V}^{′}(t)=E(t)\cdot L(t)$
- $V(t)=E(t)+L(t)$

**Worked solution**

The function $V(t)$ gives the volume of water in a tank after $t$ minutes. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate at which the amount changes at time $t$.

In addition, $L(t)$ already includes the negative sign of removal. We add the two signed contributions at time $t$. That is,

$$
V'(t)=E(t)+L(t).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## hard — signed_net (signed_net)

A model records the mass of grain in a silo at time $t$, measured in hours after observations begin.

- $V(t)$ - the mass of grain in a silo, in kilograms.

- $E(t)$ - the positive rate at which the amount is added, in kilograms per hour.

- $L(t)$ - the signed contribution of removal to the rate of change, in kilograms per hour; $L(t)<0$ when removal occurs.

What is the relationship between the three functions above?

- ${V}^{′}(t)=-E(t)-L(t)$
- $V(t)=E(t)+L(t)$
- ${V}^{′}(t)=E(t)\cdot L(t)$
- ${V}^{′}(t)=E(t)-L(t)$
- ${V}^{′}(t)=E(t)+L(t)$ **Correct**

**Worked solution**

The function $V(t)$ gives the mass of grain in a silo after $t$ hours. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate at which the amount changes at time $t$.

In addition, $L(t)$ already includes the negative sign of removal. We add the two signed contributions at time $t$. That is,

$$
V'(t)=E(t)+L(t).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## hard — signed_net (signed_net)

A model records the volume of fuel in a reservoir at time $t$, measured in seconds after observations begin.

- $V(t)$ - the volume of fuel in a reservoir, in liters.

- $E(t)$ - the positive rate at which the amount is added, in liters per second.

- $L(t)$ - the signed contribution of removal to the rate of change, in liters per second; $L(t)<0$ when removal occurs.

What is the relationship between the three functions above?

- ${V}^{′}(t)=-E(t)-L(t)$
- ${V}^{′}(t)=E(t)+L(t)$ **Correct**
- $V(t)=E(t)+L(t)$
- ${V}^{′}(t)=E(t)\cdot L(t)$
- ${V}^{′}(t)=E(t)-L(t)$

**Worked solution**

The function $V(t)$ gives the volume of fuel in a reservoir after $t$ seconds. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate at which the amount changes at time $t$.

In addition, $L(t)$ already includes the negative sign of removal. We add the two signed contributions at time $t$. That is,

$$
V'(t)=E(t)+L(t).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.

### Authored level extension — not observed

## hard — signed_net (signed_net)

A model records the number of items in a store at time $t$, measured in days after observations begin.

- $V(t)$ - the number of items in a store, in items.

- $E(t)$ - the positive rate at which the amount is added, in items per day.

- $L(t)$ - the signed contribution of removal to the rate of change, in items per day; $L(t)<0$ when removal occurs.

What is the relationship between the three functions above?

- ${V}^{′}(t)=E(t)-L(t)$
- ${V}^{′}(t)=-E(t)-L(t)$
- $V(t)=E(t)+L(t)$
- ${V}^{′}(t)=E(t)\cdot L(t)$
- ${V}^{′}(t)=E(t)+L(t)$ **Correct**

**Worked solution**

The function $V(t)$ gives the number of items in a store after $t$ days. Then,

$$
V'(t)=\frac{\text{d}V(t)}{\text{d}t}=\frac{\text{Change in }V}{\text{Change in }t}.
$$

Thus, $V'(t)$ gives the instantaneous rate at which the amount changes at time $t$.

In addition, $L(t)$ already includes the negative sign of removal. We add the two signed contributions at time $t$. That is,

$$
V'(t)=E(t)+L(t).
$$

The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.
