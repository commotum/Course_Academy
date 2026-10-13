# Review: two independent variables

Original replay banks are evidence-only. Normal variants retain every source solution stage and use authored complete method banks. Easy variants are explicitly authored.

## Original complete raw replay q-37205

Let $f(x,y)=2x+xy,$ where $x=s{e}^{s}$ and $y=t{e}^{s}.$ Calculate $\frac{∂f}{∂t}.$

- $s{e}^{st}$
- $st{e}^{s}$
- $t{e}^{2s}$
- $s{e}^{2s}$ **correct**
- $t{e}^{st}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2+y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2+t{e}^{s}, \\ \frac{∂f}{∂y} & =s{e}^{s}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =0, \\ \frac{∂y}{∂t} & ={e}^{s}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(2+t{e}^{s})(0)+(s{e}^{s})({e}^{s}) \\  & =s{e}^{2s}.\end{aligned}
$$

## Generated source-shaped normal zero_exponential {'h': -2, 'k': 1}

Let $f(x,y)=2x+xy,$ where $x=\left(s-2\right){e}^{\left(s-2\right)}$ and $y=\left(t+1\right){e}^{\left(s-2\right)}.$ Calculate $\frac{∂f}{∂t}.$

- $\left(s - 2\right) e^{s - 2}$
- $2 \left(s - 2\right) \left(t + 1\right) e^{2 s - 4} + 2 \left(s - 2\right) e^{s - 2} + \left(t + 1\right) e^{2 s - 4} + 2 e^{s - 2}$
- $\left(s - 2\right) e^{2 s - 4}$ **correct**
- $\left(t + 1\right) e^{2 s - 4}$
- $\left(s - 2\right) \left(t + 1\right) e^{2 s - 4}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2+y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2+\left(t+1\right){e}^{\left(s-2\right)}, \\ \frac{∂f}{∂y} & =\left(s-2\right){e}^{\left(s-2\right)}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =0, \\ \frac{∂y}{∂t} & ={e}^{\left(s-2\right)}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(2+\left(t+1\right){e}^{\left(s-2\right)})(0)+(\left(s-2\right){e}^{\left(s-2\right)})({e}^{\left(s-2\right)}) \\  & =\left(s-2\right){e}^{2\left(s-2\right)}.\end{aligned}
$$

## Generated source-shaped normal zero_exponential {'h': 1, 'k': -2}

Let $f(x,y)=2x+xy,$ where $x=\left(s+1\right){e}^{\left(s+1\right)}$ and $y=\left(t-2\right){e}^{\left(s+1\right)}.$ Calculate $\frac{∂f}{∂t}.$

- $\left(s + 1\right) e^{s + 1}$
- $2 \left(s + 1\right) \left(t - 2\right) e^{2 s + 2} + 2 \left(s + 1\right) e^{s + 1} + \left(t - 2\right) e^{2 s + 2} + 2 e^{s + 1}$
- $\left(s + 1\right) e^{2 s + 2}$ **correct**
- $\left(t - 2\right) e^{2 s + 2}$
- $\left(s + 1\right) \left(t - 2\right) e^{2 s + 2}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2+y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2+\left(t-2\right){e}^{\left(s+1\right)}, \\ \frac{∂f}{∂y} & =\left(s+1\right){e}^{\left(s+1\right)}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =0, \\ \frac{∂y}{∂t} & ={e}^{\left(s+1\right)}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(2+\left(t-2\right){e}^{\left(s+1\right)})(0)+(\left(s+1\right){e}^{\left(s+1\right)})({e}^{\left(s+1\right)}) \\  & =\left(s+1\right){e}^{2\left(s+1\right)}.\end{aligned}
$$

## Original complete raw replay q-94448

Let $f(x,y)={x}^{2}-4y,$ where $x=2st$ and $y={s}^{2}t.$ Calculate $\frac{∂f}{∂s}.$

- $4{s}^{2}(s-t)$
- $2{s}^{2}t(s-t)$
- $4{s}^{2}(2t-1)$
- $8st(t-1)$ **correct**
- $8st(s-1)$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=-4\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2(2st)=4st, \\ \frac{∂f}{∂y} & =-4.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =2t, \\ \frac{∂y}{∂s} & =2st.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(4st)(2t)+(-4)(2st) \\  & =8s{t}^{2}-8st \\  & =8st(t-1).\end{aligned}
$$

## Generated source-shaped normal quadratic_linear {'h': -2, 'k': 1}

Let $f(x,y)={x}^{2}-4y,$ where $x=2\left(s-2\right)\left(t+1\right)$ and $y={\left(s-2\right)}^{2}\left(t+1\right).$ Calculate $\frac{∂f}{∂s}.$

- $- 4 \left(2 s - 4\right) \left(t + 1\right)$
- $4 \left(s - 2\right) \left(t + 1\right) \left(2 t + 2\right)$
- $4 \left(s - 2\right) \left(t + 1\right) \left(2 t + 2\right) - 4 \left(2 s - 4\right) \left(t + 1\right)$ **correct**
- $4 \left(s - 2\right) \left(t + 1\right) - 4$
- $4 \left(s - 2\right) \left(t + 1\right) \left(2 t + 2\right) + 4 \left(2 s - 4\right) \left(t + 1\right)$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=-4\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2(2\left(s-2\right)\left(t+1\right))=4\left(s-2\right)\left(t+1\right), \\ \frac{∂f}{∂y} & =-4.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =2\left(t+1\right), \\ \frac{∂y}{∂s} & =2\left(s-2\right)\left(t+1\right).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(4\left(s-2\right)\left(t+1\right))(2\left(t+1\right))+(-4)(2\left(s-2\right)\left(t+1\right)) \\  & =8\left(s-2\right){\left(t+1\right)}^{2}-8\left(s-2\right)\left(t+1\right) \\  & =8\left(s-2\right)\left(t+1\right)(\left(t+1\right)-1).\end{aligned}
$$

## Generated source-shaped normal quadratic_linear {'h': 1, 'k': -2}

Let $f(x,y)={x}^{2}-4y,$ where $x=2\left(s+1\right)\left(t-2\right)$ and $y={\left(s+1\right)}^{2}\left(t-2\right).$ Calculate $\frac{∂f}{∂s}.$

- $- 4 \left(2 s + 2\right) \left(t - 2\right)$
- $4 \left(s + 1\right) \left(t - 2\right) \left(2 t - 4\right)$
- $4 \left(s + 1\right) \left(t - 2\right) \left(2 t - 4\right) - 4 \left(2 s + 2\right) \left(t - 2\right)$ **correct**
- $4 \left(s + 1\right) \left(t - 2\right) - 4$
- $4 \left(s + 1\right) \left(t - 2\right) \left(2 t - 4\right) + 4 \left(2 s + 2\right) \left(t - 2\right)$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=-4\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2(2\left(s+1\right)\left(t-2\right))=4\left(s+1\right)\left(t-2\right), \\ \frac{∂f}{∂y} & =-4.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =2\left(t-2\right), \\ \frac{∂y}{∂s} & =2\left(s+1\right)\left(t-2\right).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(4\left(s+1\right)\left(t-2\right))(2\left(t-2\right))+(-4)(2\left(s+1\right)\left(t-2\right)) \\  & =8\left(s+1\right){\left(t-2\right)}^{2}-8\left(s+1\right)\left(t-2\right) \\  & =8\left(s+1\right)\left(t-2\right)(\left(t-2\right)-1).\end{aligned}
$$

## Original complete raw replay q-170672

Let $f(x,y)=xy,$ where $x=\operatorname{cos}⁡t+\operatorname{sin}⁡s$ and $y=\operatorname{sin}⁡t.$ Calculate $\frac{∂f}{∂t}.$

- ${cos}^{2}⁡t-{sin}^{2}⁡t+\operatorname{cos}⁡s\operatorname{cos}⁡t$
- $1+\operatorname{sin}⁡s\operatorname{sin}⁡t$
- $1+\operatorname{cos}⁡s\operatorname{cos}⁡t$
- ${cos}^{2}⁡t-{sin}^{2}⁡t+\operatorname{sin}⁡s\operatorname{cos}⁡t$ **correct**
- ${cos}^{2}⁡t-{sin}^{2}⁡t+\operatorname{cos}⁡s\operatorname{sin}⁡t$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{sin}⁡t, \\ \frac{∂f}{∂y} & =\operatorname{cos}⁡t+\operatorname{sin}⁡s.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =-\operatorname{sin}⁡t, \\ \frac{∂y}{∂t} & =\operatorname{cos}⁡t.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =\operatorname{sin}⁡t(-\operatorname{sin}⁡t)+(\operatorname{cos}⁡t+\operatorname{sin}⁡s)\cdot \operatorname{cos}⁡t \\  & =-{sin}^{2}⁡t+{cos}^{2}⁡t+\operatorname{sin}⁡s\operatorname{cos}⁡t.\end{aligned}
$$

## Generated source-shaped normal trig_sum_product {'h': -2, 'k': 1}

Let $f(x,y)=xy,$ where $x=\operatorname{cos}⁡\left(t+1\right)+\operatorname{sin}⁡\left(s-2\right)$ and $y=\operatorname{sin}⁡\left(t+1\right).$ Calculate $\frac{∂f}{∂t}.$

- $\left(\sin{\left(s - 2 \right)} + \cos{\left(t + 1 \right)}\right) \cos{\left(t + 1 \right)}$
- $- \sin^{2}{\left(t + 1 \right)}$
- $\left(\sin{\left(s - 2 \right)} + \cos{\left(t + 1 \right)}\right) \cos{\left(t + 1 \right)} - \sin^{2}{\left(t + 1 \right)}$ **correct**
- $\sin{\left(s - 2 \right)} + \sin{\left(t + 1 \right)} + \cos{\left(t + 1 \right)}$
- $- \left(\sin{\left(s - 2 \right)} + \cos{\left(t + 1 \right)}\right) \cos{\left(t + 1 \right)} - \sin^{2}{\left(t + 1 \right)}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{sin}⁡\left(t+1\right), \\ \frac{∂f}{∂y} & =\operatorname{cos}⁡\left(t+1\right)+\operatorname{sin}⁡\left(s-2\right).\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =-\operatorname{sin}⁡\left(t+1\right), \\ \frac{∂y}{∂t} & =\operatorname{cos}⁡\left(t+1\right).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =\operatorname{sin}⁡\left(t+1\right)(-\operatorname{sin}⁡\left(t+1\right))+(\operatorname{cos}⁡\left(t+1\right)+\operatorname{sin}⁡\left(s-2\right))\cdot \operatorname{cos}⁡\left(t+1\right) \\  & =-{sin}^{2}⁡\left(t+1\right)+{cos}^{2}⁡\left(t+1\right)+\operatorname{sin}⁡\left(s-2\right)\operatorname{cos}⁡\left(t+1\right).\end{aligned}
$$

## Generated source-shaped normal trig_sum_product {'h': 1, 'k': -2}

Let $f(x,y)=xy,$ where $x=\operatorname{cos}⁡\left(t-2\right)+\operatorname{sin}⁡\left(s+1\right)$ and $y=\operatorname{sin}⁡\left(t-2\right).$ Calculate $\frac{∂f}{∂t}.$

- $\left(\sin{\left(s + 1 \right)} + \cos{\left(t - 2 \right)}\right) \cos{\left(t - 2 \right)}$
- $- \sin^{2}{\left(t - 2 \right)}$
- $\left(\sin{\left(s + 1 \right)} + \cos{\left(t - 2 \right)}\right) \cos{\left(t - 2 \right)} - \sin^{2}{\left(t - 2 \right)}$ **correct**
- $\sin{\left(s + 1 \right)} + \sin{\left(t - 2 \right)} + \cos{\left(t - 2 \right)}$
- $- \left(\sin{\left(s + 1 \right)} + \cos{\left(t - 2 \right)}\right) \cos{\left(t - 2 \right)} - \sin^{2}{\left(t - 2 \right)}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{sin}⁡\left(t-2\right), \\ \frac{∂f}{∂y} & =\operatorname{cos}⁡\left(t-2\right)+\operatorname{sin}⁡\left(s+1\right).\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =-\operatorname{sin}⁡\left(t-2\right), \\ \frac{∂y}{∂t} & =\operatorname{cos}⁡\left(t-2\right).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =\operatorname{sin}⁡\left(t-2\right)(-\operatorname{sin}⁡\left(t-2\right))+(\operatorname{cos}⁡\left(t-2\right)+\operatorname{sin}⁡\left(s+1\right))\cdot \operatorname{cos}⁡\left(t-2\right) \\  & =-{sin}^{2}⁡\left(t-2\right)+{cos}^{2}⁡\left(t-2\right)+\operatorname{sin}⁡\left(s+1\right)\operatorname{cos}⁡\left(t-2\right).\end{aligned}
$$

## Original complete raw replay q-170673

Let $f(x,y)=y{e}^{x},$ where $x=t+s$ and $y=ts.$ Calculate $\frac{∂f}{∂s}.$

- $t{e}^{t+s}(s+1)$ **correct**
- $t{e}^{t+s}(s-t)$
- ${e}^{t+s}(s+t)$
- $s{e}^{t+s}(t+1)$
- $s{e}^{t+s}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y{e}^{x},\,\frac{∂f}{∂y}={e}^{x}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =ts{e}^{t+s}, \\ \frac{∂f}{∂y} & ={e}^{t+s}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =1, \\ \frac{∂y}{∂s} & =t.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(ts{e}^{t+s})(1)+({e}^{t+s})(t) \\  & =t{e}^{t+s}(s+1).\end{aligned}
$$

## Generated source-shaped normal exponential_product {'h': -2, 'k': 1}

Let $f(x,y)=y{e}^{x},$ where $x=\left(t+1\right)+\left(s-2\right)$ and $y=\left(t+1\right)\left(s-2\right).$ Calculate $\frac{∂f}{∂s}.$

- $\left(t + 1\right) e^{s + t - 1}$
- $\left(s - 2\right) \left(t + 1\right) e^{s + t - 1}$
- $\left(s - 2\right) \left(t + 1\right) e^{s + t - 1} + \left(t + 1\right) e^{s + t - 1}$ **correct**
- $\left(s - 2\right) \left(t + 1\right) e^{s + t - 1} + e^{s + t - 1}$
- $\left(s - 2\right) \left(t + 1\right) e^{s + t - 1} - \left(t + 1\right) e^{s + t - 1}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y{e}^{x},\,\frac{∂f}{∂y}={e}^{x}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\left(t+1\right)\left(s-2\right){e}^{\left(t+1\right)+\left(s-2\right)}, \\ \frac{∂f}{∂y} & ={e}^{\left(t+1\right)+\left(s-2\right)}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =1, \\ \frac{∂y}{∂s} & =\left(t+1\right).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(\left(t+1\right)\left(s-2\right){e}^{\left(t+1\right)+\left(s-2\right)})(1)+({e}^{\left(t+1\right)+\left(s-2\right)})(\left(t+1\right)) \\  & =\left(t+1\right){e}^{\left(t+1\right)+\left(s-2\right)}(\left(s-2\right)+1).\end{aligned}
$$

## Generated source-shaped normal exponential_product {'h': 1, 'k': -2}

Let $f(x,y)=y{e}^{x},$ where $x=\left(t-2\right)+\left(s+1\right)$ and $y=\left(t-2\right)\left(s+1\right).$ Calculate $\frac{∂f}{∂s}.$

- $\left(t - 2\right) e^{s + t - 1}$
- $\left(s + 1\right) \left(t - 2\right) e^{s + t - 1}$
- $\left(s + 1\right) \left(t - 2\right) e^{s + t - 1} + \left(t - 2\right) e^{s + t - 1}$ **correct**
- $\left(s + 1\right) \left(t - 2\right) e^{s + t - 1} + e^{s + t - 1}$
- $\left(s + 1\right) \left(t - 2\right) e^{s + t - 1} - \left(t - 2\right) e^{s + t - 1}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y{e}^{x},\,\frac{∂f}{∂y}={e}^{x}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\left(t-2\right)\left(s+1\right){e}^{\left(t-2\right)+\left(s+1\right)}, \\ \frac{∂f}{∂y} & ={e}^{\left(t-2\right)+\left(s+1\right)}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =1, \\ \frac{∂y}{∂s} & =\left(t-2\right).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(\left(t-2\right)\left(s+1\right){e}^{\left(t-2\right)+\left(s+1\right)})(1)+({e}^{\left(t-2\right)+\left(s+1\right)})(\left(t-2\right)) \\  & =\left(t-2\right){e}^{\left(t-2\right)+\left(s+1\right)}(\left(s+1\right)+1).\end{aligned}
$$

## Original complete raw replay q-37138

Let $f(x,y)=x{y}^{2}-2y,$ where $x=s{t}^{2}$ and $y={s}^{3}-t.$ Calculate $\frac{∂f}{∂s}.$

- $7{s}^{5}{t}^{2}+2{s}^{3}{t}^{3}-6{s}^{2}+4{t}^{2}$
- $7{s}^{6}{t}^{2}-8{s}^{3}{t}^{3}-6{s}^{2}+{t}^{4}$ **correct**
- $3{s}^{6}{t}^{2}-6{s}^{2}+{t}^{4}$
- $4{s}^{3}{t}^{3}-5{s}^{2}+2{t}^{4}$
- $7{s}^{3}{t}^{2}-4{s}^{3}{t}^{3}-6s$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}={y}^{2},\,\frac{∂f}{∂y}=2xy-2\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =({s}^{3}-t)^{2}={s}^{6}-2{s}^{3}t+{t}^{2}, \\ \frac{∂f}{∂y} & =2(s{t}^{2})({s}^{3}-t)-2=2{s}^{4}{t}^{2}-2s{t}^{3}-2.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & ={t}^{2}, \\ \frac{∂y}{∂s} & =3{s}^{2}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =({s}^{6}-2{s}^{3}t+{t}^{2})({t}^{2})+(2{s}^{4}{t}^{2}-2s{t}^{3}-2)(3{s}^{2}) \\  & ={s}^{6}{t}^{2}-2{s}^{3}{t}^{3}+{t}^{4}+6{s}^{6}{t}^{2}-6{s}^{3}{t}^{3}-6{s}^{2} \\  & =7{s}^{6}{t}^{2}-8{s}^{3}{t}^{3}-6{s}^{2}+{t}^{4}.\end{aligned}
$$

## Generated source-shaped normal expanded_polynomial {'h': -2, 'k': 1}

Let $f(x,y)=x{y}^{2}-2y,$ where $x=\left(s-2\right){\left(t+1\right)}^{2}$ and $y={\left(s-2\right)}^{3}-\left(t+1\right).$ Calculate $\frac{∂f}{∂s}.$

- $3 \left(s - 2\right)^{2} \left(2 \left(s - 2\right) \left(t + 1\right)^{2} \left(- t + \left(s - 2\right)^{3} - 1\right) - 2\right)$
- $\left(t + 1\right)^{2} \left(- t + \left(s - 2\right)^{3} - 1\right)^{2}$
- $3 \left(s - 2\right)^{2} \left(2 \left(s - 2\right) \left(t + 1\right)^{2} \left(- t + \left(s - 2\right)^{3} - 1\right) - 2\right) + \left(t + 1\right)^{2} \left(- t + \left(s - 2\right)^{3} - 1\right)^{2}$ **correct**
- $2 \left(s - 2\right) \left(t + 1\right)^{2} \left(- t + \left(s - 2\right)^{3} - 1\right) + \left(- t + \left(s - 2\right)^{3} - 1\right)^{2} - 2$
- $- 3 \left(s - 2\right)^{2} \left(2 \left(s - 2\right) \left(t + 1\right)^{2} \left(- t + \left(s - 2\right)^{3} - 1\right) - 2\right) + \left(t + 1\right)^{2} \left(- t + \left(s - 2\right)^{3} - 1\right)^{2}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}={y}^{2},\,\frac{∂f}{∂y}=2xy-2\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =({\left(s-2\right)}^{3}-\left(t+1\right))^{2}={\left(s-2\right)}^{6}-2{\left(s-2\right)}^{3}\left(t+1\right)+{\left(t+1\right)}^{2}, \\ \frac{∂f}{∂y} & =2(\left(s-2\right){\left(t+1\right)}^{2})({\left(s-2\right)}^{3}-\left(t+1\right))-2=2{\left(s-2\right)}^{4}{\left(t+1\right)}^{2}-2\left(s-2\right){\left(t+1\right)}^{3}-2.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & ={\left(t+1\right)}^{2}, \\ \frac{∂y}{∂s} & =3{\left(s-2\right)}^{2}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =({\left(s-2\right)}^{6}-2{\left(s-2\right)}^{3}\left(t+1\right)+{\left(t+1\right)}^{2})({\left(t+1\right)}^{2})+(2{\left(s-2\right)}^{4}{\left(t+1\right)}^{2}-2\left(s-2\right){\left(t+1\right)}^{3}-2)(3{\left(s-2\right)}^{2}) \\  & ={\left(s-2\right)}^{6}{\left(t+1\right)}^{2}-2{\left(s-2\right)}^{3}{\left(t+1\right)}^{3}+{\left(t+1\right)}^{4}+6{\left(s-2\right)}^{6}{\left(t+1\right)}^{2}-6{\left(s-2\right)}^{3}{\left(t+1\right)}^{3}-6{\left(s-2\right)}^{2} \\  & =7{\left(s-2\right)}^{6}{\left(t+1\right)}^{2}-8{\left(s-2\right)}^{3}{\left(t+1\right)}^{3}-6{\left(s-2\right)}^{2}+{\left(t+1\right)}^{4}.\end{aligned}
$$

## Generated source-shaped normal expanded_polynomial {'h': 1, 'k': -2}

Let $f(x,y)=x{y}^{2}-2y,$ where $x=\left(s+1\right){\left(t-2\right)}^{2}$ and $y={\left(s+1\right)}^{3}-\left(t-2\right).$ Calculate $\frac{∂f}{∂s}.$

- $3 \left(s + 1\right)^{2} \left(2 \left(s + 1\right) \left(t - 2\right)^{2} \left(- t + \left(s + 1\right)^{3} + 2\right) - 2\right)$
- $\left(t - 2\right)^{2} \left(- t + \left(s + 1\right)^{3} + 2\right)^{2}$
- $3 \left(s + 1\right)^{2} \left(2 \left(s + 1\right) \left(t - 2\right)^{2} \left(- t + \left(s + 1\right)^{3} + 2\right) - 2\right) + \left(t - 2\right)^{2} \left(- t + \left(s + 1\right)^{3} + 2\right)^{2}$ **correct**
- $2 \left(s + 1\right) \left(t - 2\right)^{2} \left(- t + \left(s + 1\right)^{3} + 2\right) + \left(- t + \left(s + 1\right)^{3} + 2\right)^{2} - 2$
- $- 3 \left(s + 1\right)^{2} \left(2 \left(s + 1\right) \left(t - 2\right)^{2} \left(- t + \left(s + 1\right)^{3} + 2\right) - 2\right) + \left(t - 2\right)^{2} \left(- t + \left(s + 1\right)^{3} + 2\right)^{2}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}={y}^{2},\,\frac{∂f}{∂y}=2xy-2\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =({\left(s+1\right)}^{3}-\left(t-2\right))^{2}={\left(s+1\right)}^{6}-2{\left(s+1\right)}^{3}\left(t-2\right)+{\left(t-2\right)}^{2}, \\ \frac{∂f}{∂y} & =2(\left(s+1\right){\left(t-2\right)}^{2})({\left(s+1\right)}^{3}-\left(t-2\right))-2=2{\left(s+1\right)}^{4}{\left(t-2\right)}^{2}-2\left(s+1\right){\left(t-2\right)}^{3}-2.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & ={\left(t-2\right)}^{2}, \\ \frac{∂y}{∂s} & =3{\left(s+1\right)}^{2}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =({\left(s+1\right)}^{6}-2{\left(s+1\right)}^{3}\left(t-2\right)+{\left(t-2\right)}^{2})({\left(t-2\right)}^{2})+(2{\left(s+1\right)}^{4}{\left(t-2\right)}^{2}-2\left(s+1\right){\left(t-2\right)}^{3}-2)(3{\left(s+1\right)}^{2}) \\  & ={\left(s+1\right)}^{6}{\left(t-2\right)}^{2}-2{\left(s+1\right)}^{3}{\left(t-2\right)}^{3}+{\left(t-2\right)}^{4}+6{\left(s+1\right)}^{6}{\left(t-2\right)}^{2}-6{\left(s+1\right)}^{3}{\left(t-2\right)}^{3}-6{\left(s+1\right)}^{2} \\  & =7{\left(s+1\right)}^{6}{\left(t-2\right)}^{2}-8{\left(s+1\right)}^{3}{\left(t-2\right)}^{3}-6{\left(s+1\right)}^{2}+{\left(t-2\right)}^{4}.\end{aligned}
$$

## Original complete raw replay q-94747

Let $f(x,y)=\frac{1}{x}+\frac{1}{y},$ where $x={e}^{st}$ and $y={e}^{-st}.$ Calculate $\frac{∂f}{∂s}.$

- $2t$
- $2t{e}^{st}$
- $2t{e}^{-st}$
- $t({e}^{2st}+{e}^{-2st})$
- $t({e}^{st}-{e}^{-st})$ **correct**

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-\frac{1}{{x}^{2}},\,\frac{∂f}{∂y}=-\frac{1}{{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-\frac{1}{({e}^{st})^{2}}=-{e}^{-2st}, \\ \frac{∂f}{∂y} & =-\frac{1}{({e}^{-st})^{2}}=-{e}^{2st}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =t{e}^{st}, \\ \frac{∂y}{∂s} & =-t{e}^{-st}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(-{e}^{-2st})(t{e}^{st})+(-{e}^{2st})(-t{e}^{-st}) \\  & =t{e}^{st}-t{e}^{-st} \\  & =t({e}^{st}-{e}^{-st}).\end{aligned}
$$

## Generated source-shaped normal reciprocal_exponential {'h': -2, 'k': 1}

Let $f(x,y)=\frac{1}{x}+\frac{1}{y},$ where $x={e}^{\left(s-2\right)\left(t+1\right)}$ and $y={e}^{-\left(s-2\right)\left(t+1\right)}.$ Calculate $\frac{∂f}{∂s}.$

- $- \left(- t - 1\right) e^{\left(s - 2\right) \left(t + 1\right)}$
- $- \left(t + 1\right) e^{- \left(s - 2\right) \left(t + 1\right)}$
- $- \left(- t - 1\right) e^{\left(s - 2\right) \left(t + 1\right)} - \left(t + 1\right) e^{- \left(s - 2\right) \left(t + 1\right)}$ **correct**
- $- e^{2 \left(s - 2\right) \left(t + 1\right)} - e^{- 2 \left(s - 2\right) \left(t + 1\right)}$
- $\left(- t - 1\right) e^{\left(s - 2\right) \left(t + 1\right)} - \left(t + 1\right) e^{- \left(s - 2\right) \left(t + 1\right)}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-\frac{1}{{x}^{2}},\,\frac{∂f}{∂y}=-\frac{1}{{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-\frac{1}{({e}^{\left(s-2\right)\left(t+1\right)})^{2}}=-{e}^{-2\left(s-2\right)\left(t+1\right)}, \\ \frac{∂f}{∂y} & =-\frac{1}{({e}^{-\left(s-2\right)\left(t+1\right)})^{2}}=-{e}^{2\left(s-2\right)\left(t+1\right)}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =\left(t+1\right){e}^{\left(s-2\right)\left(t+1\right)}, \\ \frac{∂y}{∂s} & =-\left(t+1\right){e}^{-\left(s-2\right)\left(t+1\right)}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(-{e}^{-2\left(s-2\right)\left(t+1\right)})(\left(t+1\right){e}^{\left(s-2\right)\left(t+1\right)})+(-{e}^{2\left(s-2\right)\left(t+1\right)})(-\left(t+1\right){e}^{-\left(s-2\right)\left(t+1\right)}) \\  & =\left(t+1\right){e}^{\left(s-2\right)\left(t+1\right)}-\left(t+1\right){e}^{-\left(s-2\right)\left(t+1\right)} \\  & =\left(t+1\right)({e}^{\left(s-2\right)\left(t+1\right)}-{e}^{-\left(s-2\right)\left(t+1\right)}).\end{aligned}
$$

## Generated source-shaped normal reciprocal_exponential {'h': 1, 'k': -2}

Let $f(x,y)=\frac{1}{x}+\frac{1}{y},$ where $x={e}^{\left(s+1\right)\left(t-2\right)}$ and $y={e}^{-\left(s+1\right)\left(t-2\right)}.$ Calculate $\frac{∂f}{∂s}.$

- $- \left(2 - t\right) e^{\left(s + 1\right) \left(t - 2\right)}$
- $- \left(t - 2\right) e^{- \left(s + 1\right) \left(t - 2\right)}$
- $- \left(2 - t\right) e^{\left(s + 1\right) \left(t - 2\right)} - \left(t - 2\right) e^{- \left(s + 1\right) \left(t - 2\right)}$ **correct**
- $- e^{2 \left(s + 1\right) \left(t - 2\right)} - e^{- 2 \left(s + 1\right) \left(t - 2\right)}$
- $\left(2 - t\right) e^{\left(s + 1\right) \left(t - 2\right)} - \left(t - 2\right) e^{- \left(s + 1\right) \left(t - 2\right)}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-\frac{1}{{x}^{2}},\,\frac{∂f}{∂y}=-\frac{1}{{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-\frac{1}{({e}^{\left(s+1\right)\left(t-2\right)})^{2}}=-{e}^{-2\left(s+1\right)\left(t-2\right)}, \\ \frac{∂f}{∂y} & =-\frac{1}{({e}^{-\left(s+1\right)\left(t-2\right)})^{2}}=-{e}^{2\left(s+1\right)\left(t-2\right)}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =\left(t-2\right){e}^{\left(s+1\right)\left(t-2\right)}, \\ \frac{∂y}{∂s} & =-\left(t-2\right){e}^{-\left(s+1\right)\left(t-2\right)}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(-{e}^{-2\left(s+1\right)\left(t-2\right)})(\left(t-2\right){e}^{\left(s+1\right)\left(t-2\right)})+(-{e}^{2\left(s+1\right)\left(t-2\right)})(-\left(t-2\right){e}^{-\left(s+1\right)\left(t-2\right)}) \\  & =\left(t-2\right){e}^{\left(s+1\right)\left(t-2\right)}-\left(t-2\right){e}^{-\left(s+1\right)\left(t-2\right)} \\  & =\left(t-2\right)({e}^{\left(s+1\right)\left(t-2\right)}-{e}^{-\left(s+1\right)\left(t-2\right)}).\end{aligned}
$$

## Original complete raw replay q-94749

Let $f(x,y)=xy,$ where $x=\operatorname{sin}⁡(st)$ and $y=\operatorname{cos}⁡(st).$ Calculate $\frac{∂f}{∂t}.$

- ${s}^{2}\operatorname{sin}⁡(2st)$
- $s\operatorname{cos}⁡(2st)$ **correct**
- $t\operatorname{sin}⁡(2st)$
- ${t}^{2}\operatorname{cos}⁡(2st)$
- $s\operatorname{sin}⁡(2st)$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{cos}⁡(st), \\ \frac{∂f}{∂y} & =\operatorname{sin}⁡(st).\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =s\operatorname{cos}⁡(st), \\ \frac{∂y}{∂t} & =-s\operatorname{sin}⁡(st).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(\operatorname{cos}⁡(st))(s\operatorname{cos}⁡(st))+(\operatorname{sin}⁡(st))(-s\operatorname{sin}⁡(st)) \\  & =s{cos}^{2}⁡(st)-s{sin}^{2}⁡(st) \\  & =s({cos}^{2}⁡(st)-{sin}^{2}⁡(st)) \\  & =s\operatorname{cos}⁡(2st).\end{aligned}
$$

## Generated source-shaped normal trig_product {'h': -2, 'k': 1}

Let $f(x,y)=xy,$ where $x=\operatorname{sin}⁡(\left(s-2\right)\left(t+1\right))$ and $y=\operatorname{cos}⁡(\left(s-2\right)\left(t+1\right)).$ Calculate $\frac{∂f}{∂t}.$

- $- \left(s - 2\right) \sin^{2}{\left(\left(s - 2\right) \left(t + 1\right) \right)}$
- $\left(s - 2\right) \cos^{2}{\left(\left(s - 2\right) \left(t + 1\right) \right)}$
- $- \left(s - 2\right) \sin^{2}{\left(\left(s - 2\right) \left(t + 1\right) \right)} + \left(s - 2\right) \cos^{2}{\left(\left(s - 2\right) \left(t + 1\right) \right)}$ **correct**
- $\sin{\left(\left(s - 2\right) \left(t + 1\right) \right)} + \cos{\left(\left(s - 2\right) \left(t + 1\right) \right)}$
- $\left(s - 2\right) \sin^{2}{\left(\left(s - 2\right) \left(t + 1\right) \right)} + \left(s - 2\right) \cos^{2}{\left(\left(s - 2\right) \left(t + 1\right) \right)}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{cos}⁡(\left(s-2\right)\left(t+1\right)), \\ \frac{∂f}{∂y} & =\operatorname{sin}⁡(\left(s-2\right)\left(t+1\right)).\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =\left(s-2\right)\operatorname{cos}⁡(\left(s-2\right)\left(t+1\right)), \\ \frac{∂y}{∂t} & =-\left(s-2\right)\operatorname{sin}⁡(\left(s-2\right)\left(t+1\right)).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(\operatorname{cos}⁡(\left(s-2\right)\left(t+1\right)))(\left(s-2\right)\operatorname{cos}⁡(\left(s-2\right)\left(t+1\right)))+(\operatorname{sin}⁡(\left(s-2\right)\left(t+1\right)))(-\left(s-2\right)\operatorname{sin}⁡(\left(s-2\right)\left(t+1\right))) \\  & =\left(s-2\right){cos}^{2}⁡(\left(s-2\right)\left(t+1\right))-\left(s-2\right){sin}^{2}⁡(\left(s-2\right)\left(t+1\right)) \\  & =\left(s-2\right)({cos}^{2}⁡(\left(s-2\right)\left(t+1\right))-{sin}^{2}⁡(\left(s-2\right)\left(t+1\right))) \\  & =\left(s-2\right)\operatorname{cos}⁡(2\left(s-2\right)\left(t+1\right)).\end{aligned}
$$

## Generated source-shaped normal trig_product {'h': 1, 'k': -2}

Let $f(x,y)=xy,$ where $x=\operatorname{sin}⁡(\left(s+1\right)\left(t-2\right))$ and $y=\operatorname{cos}⁡(\left(s+1\right)\left(t-2\right)).$ Calculate $\frac{∂f}{∂t}.$

- $- \left(s + 1\right) \sin^{2}{\left(\left(s + 1\right) \left(t - 2\right) \right)}$
- $\left(s + 1\right) \cos^{2}{\left(\left(s + 1\right) \left(t - 2\right) \right)}$
- $- \left(s + 1\right) \sin^{2}{\left(\left(s + 1\right) \left(t - 2\right) \right)} + \left(s + 1\right) \cos^{2}{\left(\left(s + 1\right) \left(t - 2\right) \right)}$ **correct**
- $\sin{\left(\left(s + 1\right) \left(t - 2\right) \right)} + \cos{\left(\left(s + 1\right) \left(t - 2\right) \right)}$
- $\left(s + 1\right) \sin^{2}{\left(\left(s + 1\right) \left(t - 2\right) \right)} + \left(s + 1\right) \cos^{2}{\left(\left(s + 1\right) \left(t - 2\right) \right)}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{cos}⁡(\left(s+1\right)\left(t-2\right)), \\ \frac{∂f}{∂y} & =\operatorname{sin}⁡(\left(s+1\right)\left(t-2\right)).\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =\left(s+1\right)\operatorname{cos}⁡(\left(s+1\right)\left(t-2\right)), \\ \frac{∂y}{∂t} & =-\left(s+1\right)\operatorname{sin}⁡(\left(s+1\right)\left(t-2\right)).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(\operatorname{cos}⁡(\left(s+1\right)\left(t-2\right)))(\left(s+1\right)\operatorname{cos}⁡(\left(s+1\right)\left(t-2\right)))+(\operatorname{sin}⁡(\left(s+1\right)\left(t-2\right)))(-\left(s+1\right)\operatorname{sin}⁡(\left(s+1\right)\left(t-2\right))) \\  & =\left(s+1\right){cos}^{2}⁡(\left(s+1\right)\left(t-2\right))-\left(s+1\right){sin}^{2}⁡(\left(s+1\right)\left(t-2\right)) \\  & =\left(s+1\right)({cos}^{2}⁡(\left(s+1\right)\left(t-2\right))-{sin}^{2}⁡(\left(s+1\right)\left(t-2\right))) \\  & =\left(s+1\right)\operatorname{cos}⁡(2\left(s+1\right)\left(t-2\right)).\end{aligned}
$$

## Original complete raw replay q-94751

Let $f(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}),$ where $x=t{e}^{s}$ and $y=t{e}^{-s}.$ Calculate $\frac{∂f}{∂t}.$

- $\frac{2({e}^{2s}-{e}^{-2s})}{{e}^{2s}+{e}^{-2s}}$
- $\frac{1}{{t}^{2}}$
- $\frac{2}{t}$ **correct**
- $1-\frac{4}{{t}^{2}}$
- $\frac{{e}^{2s}+{e}^{-2s}}{2({e}^{2s}-{e}^{-2s})}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{∂f}{∂y}=\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{2(t{e}^{s})}{(t{e}^{s})^{2}+(t{e}^{-s})^{2}}=\frac{2{e}^{s}}{t({e}^{2s}+{e}^{-2s})}, \\ \frac{∂f}{∂y} & =\frac{2(t{e}^{-s})}{(t{e}^{s})^{2}+(t{e}^{-s})^{2}}=\frac{2{e}^{-s}}{t({e}^{2s}+{e}^{-2s})}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & ={e}^{s}, \\ \frac{∂y}{∂t} & ={e}^{-s}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =\frac{2{e}^{s}}{t({e}^{2s}+{e}^{-2s})}\cdot {e}^{s}+\frac{2{e}^{-s}}{t({e}^{2s}+{e}^{-2s})}\cdot {e}^{-s} \\  & =\frac{2{e}^{2s}}{t({e}^{2s}+{e}^{-2s})}+\frac{2{e}^{-2s}}{t({e}^{2s}+{e}^{-2s})} \\  & =\frac{2({e}^{2s}+{e}^{-2s})}{t({e}^{2s}+{e}^{-2s})} \\  & =\frac{2}{t}.\end{aligned}
$$

## Generated source-shaped normal log_norm {'h': -2, 'k': 1}

Let $f(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}),$ where $x=\left(t+1\right){e}^{\left(s-2\right)}$ and $y=\left(t+1\right){e}^{-\left(s-2\right)}.$ Calculate $\frac{∂f}{∂t}.$

- $\frac{2 \left(t + 1\right) e^{4 - 2 s}}{\left(t + 1\right)^{2} e^{4 - 2 s} + \left(t + 1\right)^{2} e^{2 s - 4}}$
- $\frac{2 \left(t + 1\right) e^{2 s - 4}}{\left(t + 1\right)^{2} e^{4 - 2 s} + \left(t + 1\right)^{2} e^{2 s - 4}}$
- $\frac{2 \left(t + 1\right) e^{4 - 2 s}}{\left(t + 1\right)^{2} e^{4 - 2 s} + \left(t + 1\right)^{2} e^{2 s - 4}} + \frac{2 \left(t + 1\right) e^{2 s - 4}}{\left(t + 1\right)^{2} e^{4 - 2 s} + \left(t + 1\right)^{2} e^{2 s - 4}}$ **correct**
- $\frac{2 \left(t + 1\right) e^{2 - s}}{\left(t + 1\right)^{2} e^{4 - 2 s} + \left(t + 1\right)^{2} e^{2 s - 4}} + \frac{2 \left(t + 1\right) e^{s - 2}}{\left(t + 1\right)^{2} e^{4 - 2 s} + \left(t + 1\right)^{2} e^{2 s - 4}}$
- $- \frac{2 \left(t + 1\right) e^{4 - 2 s}}{\left(t + 1\right)^{2} e^{4 - 2 s} + \left(t + 1\right)^{2} e^{2 s - 4}} + \frac{2 \left(t + 1\right) e^{2 s - 4}}{\left(t + 1\right)^{2} e^{4 - 2 s} + \left(t + 1\right)^{2} e^{2 s - 4}}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{∂f}{∂y}=\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{2(\left(t+1\right){e}^{\left(s-2\right)})}{(\left(t+1\right){e}^{\left(s-2\right)})^{2}+(\left(t+1\right){e}^{-\left(s-2\right)})^{2}}=\frac{2{e}^{\left(s-2\right)}}{\left(t+1\right)({e}^{2\left(s-2\right)}+{e}^{-2\left(s-2\right)})}, \\ \frac{∂f}{∂y} & =\frac{2(\left(t+1\right){e}^{-\left(s-2\right)})}{(\left(t+1\right){e}^{\left(s-2\right)})^{2}+(\left(t+1\right){e}^{-\left(s-2\right)})^{2}}=\frac{2{e}^{-\left(s-2\right)}}{\left(t+1\right)({e}^{2\left(s-2\right)}+{e}^{-2\left(s-2\right)})}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & ={e}^{\left(s-2\right)}, \\ \frac{∂y}{∂t} & ={e}^{-\left(s-2\right)}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =\frac{2{e}^{\left(s-2\right)}}{\left(t+1\right)({e}^{2\left(s-2\right)}+{e}^{-2\left(s-2\right)})}\cdot {e}^{\left(s-2\right)}+\frac{2{e}^{-\left(s-2\right)}}{\left(t+1\right)({e}^{2\left(s-2\right)}+{e}^{-2\left(s-2\right)})}\cdot {e}^{-\left(s-2\right)} \\  & =\frac{2{e}^{2\left(s-2\right)}}{\left(t+1\right)({e}^{2\left(s-2\right)}+{e}^{-2\left(s-2\right)})}+\frac{2{e}^{-2\left(s-2\right)}}{\left(t+1\right)({e}^{2\left(s-2\right)}+{e}^{-2\left(s-2\right)})} \\  & =\frac{2({e}^{2\left(s-2\right)}+{e}^{-2\left(s-2\right)})}{\left(t+1\right)({e}^{2\left(s-2\right)}+{e}^{-2\left(s-2\right)})} \\  & =\frac{2}{\left(t+1\right)}.\end{aligned}
$$

## Generated source-shaped normal log_norm {'h': 1, 'k': -2}

Let $f(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}),$ where $x=\left(t-2\right){e}^{\left(s+1\right)}$ and $y=\left(t-2\right){e}^{-\left(s+1\right)}.$ Calculate $\frac{∂f}{∂t}.$

- $\frac{2 \left(t - 2\right) e^{- 2 s - 2}}{\left(t - 2\right)^{2} e^{- 2 s - 2} + \left(t - 2\right)^{2} e^{2 s + 2}}$
- $\frac{2 \left(t - 2\right) e^{2 s + 2}}{\left(t - 2\right)^{2} e^{- 2 s - 2} + \left(t - 2\right)^{2} e^{2 s + 2}}$
- $\frac{2 \left(t - 2\right) e^{- 2 s - 2}}{\left(t - 2\right)^{2} e^{- 2 s - 2} + \left(t - 2\right)^{2} e^{2 s + 2}} + \frac{2 \left(t - 2\right) e^{2 s + 2}}{\left(t - 2\right)^{2} e^{- 2 s - 2} + \left(t - 2\right)^{2} e^{2 s + 2}}$ **correct**
- $\frac{2 \left(t - 2\right) e^{- s - 1}}{\left(t - 2\right)^{2} e^{- 2 s - 2} + \left(t - 2\right)^{2} e^{2 s + 2}} + \frac{2 \left(t - 2\right) e^{s + 1}}{\left(t - 2\right)^{2} e^{- 2 s - 2} + \left(t - 2\right)^{2} e^{2 s + 2}}$
- $- \frac{2 \left(t - 2\right) e^{- 2 s - 2}}{\left(t - 2\right)^{2} e^{- 2 s - 2} + \left(t - 2\right)^{2} e^{2 s + 2}} + \frac{2 \left(t - 2\right) e^{2 s + 2}}{\left(t - 2\right)^{2} e^{- 2 s - 2} + \left(t - 2\right)^{2} e^{2 s + 2}}$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{∂f}{∂y}=\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{2(\left(t-2\right){e}^{\left(s+1\right)})}{(\left(t-2\right){e}^{\left(s+1\right)})^{2}+(\left(t-2\right){e}^{-\left(s+1\right)})^{2}}=\frac{2{e}^{\left(s+1\right)}}{\left(t-2\right)({e}^{2\left(s+1\right)}+{e}^{-2\left(s+1\right)})}, \\ \frac{∂f}{∂y} & =\frac{2(\left(t-2\right){e}^{-\left(s+1\right)})}{(\left(t-2\right){e}^{\left(s+1\right)})^{2}+(\left(t-2\right){e}^{-\left(s+1\right)})^{2}}=\frac{2{e}^{-\left(s+1\right)}}{\left(t-2\right)({e}^{2\left(s+1\right)}+{e}^{-2\left(s+1\right)})}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & ={e}^{\left(s+1\right)}, \\ \frac{∂y}{∂t} & ={e}^{-\left(s+1\right)}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =\frac{2{e}^{\left(s+1\right)}}{\left(t-2\right)({e}^{2\left(s+1\right)}+{e}^{-2\left(s+1\right)})}\cdot {e}^{\left(s+1\right)}+\frac{2{e}^{-\left(s+1\right)}}{\left(t-2\right)({e}^{2\left(s+1\right)}+{e}^{-2\left(s+1\right)})}\cdot {e}^{-\left(s+1\right)} \\  & =\frac{2{e}^{2\left(s+1\right)}}{\left(t-2\right)({e}^{2\left(s+1\right)}+{e}^{-2\left(s+1\right)})}+\frac{2{e}^{-2\left(s+1\right)}}{\left(t-2\right)({e}^{2\left(s+1\right)}+{e}^{-2\left(s+1\right)})} \\  & =\frac{2({e}^{2\left(s+1\right)}+{e}^{-2\left(s+1\right)})}{\left(t-2\right)({e}^{2\left(s+1\right)}+{e}^{-2\left(s+1\right)})} \\  & =\frac{2}{\left(t-2\right)}.\end{aligned}
$$

## Original complete raw replay q-37201

Let $f(x,y)={x}^{2}-2{y}^{2},$ where $x=s\operatorname{sin}⁡t$ and $y=t\operatorname{sin}⁡s.$ Calculate $\frac{∂f}{∂s}.$

- ${s}^{2}\operatorname{sin}⁡2t+4t{sin}^{2}⁡s$
- $2s{sin}^{2}⁡t-2{t}^{2}\operatorname{sin}⁡2s$ **correct**
- $2s{cos}^{2}⁡t-2t\operatorname{sin}⁡2s$
- $s\operatorname{sin}⁡2t-4{t}^{2}{sin}^{2}⁡s$
- $2{s}^{2}{sin}^{2}⁡t+2t\operatorname{sin}⁡2s$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=-4y\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2s\operatorname{sin}⁡t, \\ \frac{∂f}{∂y} & =-4t\operatorname{sin}⁡s.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =\operatorname{sin}⁡t, \\ \frac{∂y}{∂s} & =t\operatorname{cos}⁡s.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(2s\operatorname{sin}⁡t)(\operatorname{sin}⁡t)+(-4t\operatorname{sin}⁡s)(t\operatorname{cos}⁡s) \\  & =2s{sin}^{2}⁡t-4{t}^{2}\operatorname{sin}⁡s\operatorname{cos}⁡s \\  & =2s{sin}^{2}⁡t-2{t}^{2}\operatorname{sin}⁡2s.\end{aligned}
$$

## Generated source-shaped normal quadratic_trig {'h': -2, 'k': 1}

Let $f(x,y)={x}^{2}-2{y}^{2},$ where $x=\left(s-2\right)\operatorname{sin}⁡\left(t+1\right)$ and $y=\left(t+1\right)\operatorname{sin}⁡\left(s-2\right).$ Calculate $\frac{∂f}{∂s}.$

- $- 4 \left(t + 1\right)^{2} \sin{\left(s - 2 \right)} \cos{\left(s - 2 \right)}$
- $2 \left(s - 2\right) \sin^{2}{\left(t + 1 \right)}$
- $2 \left(s - 2\right) \sin^{2}{\left(t + 1 \right)} - 4 \left(t + 1\right)^{2} \sin{\left(s - 2 \right)} \cos{\left(s - 2 \right)}$ **correct**
- $2 \left(s - 2\right) \sin{\left(t + 1 \right)} - 4 \left(t + 1\right) \sin{\left(s - 2 \right)}$
- $2 \left(s - 2\right) \sin^{2}{\left(t + 1 \right)} + 4 \left(t + 1\right)^{2} \sin{\left(s - 2 \right)} \cos{\left(s - 2 \right)}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=-4y\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\left(s-2\right)\operatorname{sin}⁡\left(t+1\right), \\ \frac{∂f}{∂y} & =-4\left(t+1\right)\operatorname{sin}⁡\left(s-2\right).\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =\operatorname{sin}⁡\left(t+1\right), \\ \frac{∂y}{∂s} & =\left(t+1\right)\operatorname{cos}⁡\left(s-2\right).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(2\left(s-2\right)\operatorname{sin}⁡\left(t+1\right))(\operatorname{sin}⁡\left(t+1\right))+(-4\left(t+1\right)\operatorname{sin}⁡\left(s-2\right))(\left(t+1\right)\operatorname{cos}⁡\left(s-2\right)) \\  & =2\left(s-2\right){sin}^{2}⁡\left(t+1\right)-4{\left(t+1\right)}^{2}\operatorname{sin}⁡\left(s-2\right)\operatorname{cos}⁡\left(s-2\right) \\  & =2\left(s-2\right){sin}^{2}⁡\left(t+1\right)-2{\left(t+1\right)}^{2}\operatorname{sin}⁡2\left(s-2\right).\end{aligned}
$$

## Generated source-shaped normal quadratic_trig {'h': 1, 'k': -2}

Let $f(x,y)={x}^{2}-2{y}^{2},$ where $x=\left(s+1\right)\operatorname{sin}⁡\left(t-2\right)$ and $y=\left(t-2\right)\operatorname{sin}⁡\left(s+1\right).$ Calculate $\frac{∂f}{∂s}.$

- $- 4 \left(t - 2\right)^{2} \sin{\left(s + 1 \right)} \cos{\left(s + 1 \right)}$
- $2 \left(s + 1\right) \sin^{2}{\left(t - 2 \right)}$
- $2 \left(s + 1\right) \sin^{2}{\left(t - 2 \right)} - 4 \left(t - 2\right)^{2} \sin{\left(s + 1 \right)} \cos{\left(s + 1 \right)}$ **correct**
- $2 \left(s + 1\right) \sin{\left(t - 2 \right)} - 4 \left(t - 2\right) \sin{\left(s + 1 \right)}$
- $2 \left(s + 1\right) \sin^{2}{\left(t - 2 \right)} + 4 \left(t - 2\right)^{2} \sin{\left(s + 1 \right)} \cos{\left(s + 1 \right)}$

![](images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂s}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=-4y\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2\left(s+1\right)\operatorname{sin}⁡\left(t-2\right), \\ \frac{∂f}{∂y} & =-4\left(t-2\right)\operatorname{sin}⁡\left(s+1\right).\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $s,$ and we get

$$
\begin{aligned}\frac{∂x}{∂s} & =\operatorname{sin}⁡\left(t-2\right), \\ \frac{∂y}{∂s} & =\left(t-2\right)\operatorname{cos}⁡\left(s+1\right).\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂s} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂s}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂s} \\  & =(2\left(s+1\right)\operatorname{sin}⁡\left(t-2\right))(\operatorname{sin}⁡\left(t-2\right))+(-4\left(t-2\right)\operatorname{sin}⁡\left(s+1\right))(\left(t-2\right)\operatorname{cos}⁡\left(s+1\right)) \\  & =2\left(s+1\right){sin}^{2}⁡\left(t-2\right)-4{\left(t-2\right)}^{2}\operatorname{sin}⁡\left(s+1\right)\operatorname{cos}⁡\left(s+1\right) \\  & =2\left(s+1\right){sin}^{2}⁡\left(t-2\right)-2{\left(t-2\right)}^{2}\operatorname{sin}⁡2\left(s+1\right).\end{aligned}
$$

## Original complete raw replay q-94748

Let $f(x,y)=y{x}^{2},$ where $x=ts$ and $y=s-t.$ Calculate $\frac{∂f}{∂t}.$

- $t({s}^{2}+s+1)$
- $s{t}^{2}(s-2t)$
- $ts({t}^{2}-3ts+2{s}^{2})$
- $t{s}^{2}(2s-3t)$ **correct**
- $ts(1+ts)(1-st)$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2xy,\,\frac{∂f}{∂y}={x}^{2}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2(ts)(s-t)=2t{s}^{2}-2s{t}^{2}, \\ \frac{∂f}{∂y} & =(ts)^{2}={t}^{2}{s}^{2}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =s, \\ \frac{∂y}{∂t} & =-1.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(2t{s}^{2}-2s{t}^{2})(s)+({t}^{2}{s}^{2})(-1) \\  & =2t{s}^{3}-2{s}^{2}{t}^{2}-{t}^{2}{s}^{2} \\  & =2t{s}^{3}-3{t}^{2}{s}^{2} \\  & =t{s}^{2}(2s-3t).\end{aligned}
$$

## Generated source-shaped normal cubic_product {'h': -2, 'k': 1}

Let $f(x,y)=y{x}^{2},$ where $x=\left(t+1\right)\left(s-2\right)$ and $y=\left(s-2\right)-\left(t+1\right).$ Calculate $\frac{∂f}{∂t}.$

- $- \left(s - 2\right)^{2} \left(t + 1\right)^{2}$
- $2 \left(s - 2\right)^{2} \left(t + 1\right) \left(s - t - 3\right)$
- $- \left(s - 2\right)^{2} \left(t + 1\right)^{2} + 2 \left(s - 2\right)^{2} \left(t + 1\right) \left(s - t - 3\right)$ **correct**
- $\left(s - 2\right)^{2} \left(t + 1\right)^{2} + 2 \left(s - 2\right) \left(t + 1\right) \left(s - t - 3\right)$
- $\left(s - 2\right)^{2} \left(t + 1\right)^{2} + 2 \left(s - 2\right)^{2} \left(t + 1\right) \left(s - t - 3\right)$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2xy,\,\frac{∂f}{∂y}={x}^{2}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2(\left(t+1\right)\left(s-2\right))(\left(s-2\right)-\left(t+1\right))=2\left(t+1\right){\left(s-2\right)}^{2}-2\left(s-2\right){\left(t+1\right)}^{2}, \\ \frac{∂f}{∂y} & =(\left(t+1\right)\left(s-2\right))^{2}={\left(t+1\right)}^{2}{\left(s-2\right)}^{2}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =\left(s-2\right), \\ \frac{∂y}{∂t} & =-1.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(2\left(t+1\right){\left(s-2\right)}^{2}-2\left(s-2\right){\left(t+1\right)}^{2})(\left(s-2\right))+({\left(t+1\right)}^{2}{\left(s-2\right)}^{2})(-1) \\  & =2\left(t+1\right){\left(s-2\right)}^{3}-2{\left(s-2\right)}^{2}{\left(t+1\right)}^{2}-{\left(t+1\right)}^{2}{\left(s-2\right)}^{2} \\  & =2\left(t+1\right){\left(s-2\right)}^{3}-3{\left(t+1\right)}^{2}{\left(s-2\right)}^{2} \\  & =\left(t+1\right){\left(s-2\right)}^{2}(2\left(s-2\right)-3\left(t+1\right)).\end{aligned}
$$

## Generated source-shaped normal cubic_product {'h': 1, 'k': -2}

Let $f(x,y)=y{x}^{2},$ where $x=\left(t-2\right)\left(s+1\right)$ and $y=\left(s+1\right)-\left(t-2\right).$ Calculate $\frac{∂f}{∂t}.$

- $- \left(s + 1\right)^{2} \left(t - 2\right)^{2}$
- $2 \left(s + 1\right)^{2} \left(t - 2\right) \left(s - t + 3\right)$
- $- \left(s + 1\right)^{2} \left(t - 2\right)^{2} + 2 \left(s + 1\right)^{2} \left(t - 2\right) \left(s - t + 3\right)$ **correct**
- $\left(s + 1\right)^{2} \left(t - 2\right)^{2} + 2 \left(s + 1\right) \left(t - 2\right) \left(s - t + 3\right)$
- $\left(s + 1\right)^{2} \left(t - 2\right)^{2} + 2 \left(s + 1\right)^{2} \left(t - 2\right) \left(s - t + 3\right)$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2xy,\,\frac{∂f}{∂y}={x}^{2}\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2(\left(t-2\right)\left(s+1\right))(\left(s+1\right)-\left(t-2\right))=2\left(t-2\right){\left(s+1\right)}^{2}-2\left(s+1\right){\left(t-2\right)}^{2}, \\ \frac{∂f}{∂y} & =(\left(t-2\right)\left(s+1\right))^{2}={\left(t-2\right)}^{2}{\left(s+1\right)}^{2}.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =\left(s+1\right), \\ \frac{∂y}{∂t} & =-1.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(2\left(t-2\right){\left(s+1\right)}^{2}-2\left(s+1\right){\left(t-2\right)}^{2})(\left(s+1\right))+({\left(t-2\right)}^{2}{\left(s+1\right)}^{2})(-1) \\  & =2\left(t-2\right){\left(s+1\right)}^{3}-2{\left(s+1\right)}^{2}{\left(t-2\right)}^{2}-{\left(t-2\right)}^{2}{\left(s+1\right)}^{2} \\  & =2\left(t-2\right){\left(s+1\right)}^{3}-3{\left(t-2\right)}^{2}{\left(s+1\right)}^{2} \\  & =\left(t-2\right){\left(s+1\right)}^{2}(2\left(s+1\right)-3\left(t-2\right)).\end{aligned}
$$

## Authored missing-level easy 0

Let $f(x,y)=x - 3 y,$ where $x=- s + 2 t$ and $y=s + t.$ Calculate $\frac{∂f}{∂t}.$

- $-4$
- $-1$ **correct**
- $-3$
- $5$
- $2$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=1,\,\frac{∂f}{∂y}=-3\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =1, \\ \frac{∂f}{∂y} & =-3.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =2, \\ \frac{∂y}{∂t} & =1.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(1)\cdot (2)+(-3)\cdot (1) \\  & =(2)+(-3) \\  & =-1.\end{aligned}
$$

## Authored missing-level easy 1

Let $f(x,y)=3 x + y,$ where $x=- 2 s - 3 t$ and $y=s - 3 t.$ Calculate $\frac{∂f}{∂t}.$

- $-3$
- $-5$
- $-6$
- $-12$ **correct**
- $-9$

![](images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png)

The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:

$$
\frac{∂f}{∂t}=\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=3,\,\frac{∂f}{∂y}=1\end{aligned}
$$

Writing the above results in terms of $s$ and $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =3, \\ \frac{∂f}{∂y} & =1.\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{∂x}{∂t} & =-3, \\ \frac{∂y}{∂t} & =-3.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{∂f}{∂t} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂t}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂t} \\  & =(3)\cdot (-3)+(1)\cdot (-3) \\  & =(-9)+(-3) \\  & =-12.\end{aligned}
$$
