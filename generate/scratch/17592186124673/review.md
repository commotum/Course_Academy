# Original and generated review

Raw source evidence, supported completions and authored variants are labeled separately. Correct choices are marked only where a designation exists.

## ORIGINAL q-106661 — unrated

Given that $y < 150$ and $t \ge 0$, which of the following is an inhibited growth equation?

- $\frac{dy}{dt} = 150(y - 0.5)$
- $\frac{dy}{dt} = 150(y + 0.5)$
- $\frac{dy}{dt} =-0.5(y + 150)$
- $\frac{dy}{dt} = 0.5(y - 150)$
- $\frac{dy}{dt} = 0.5(150 - y)$

## ORIGINAL q-106662 — moderate

Given that $y<80$ and $t\ge 0,$ which of the following is an inhibited growth equation?

- $\frac{dy}{dt} = 400 - 5y$
- $\frac{dy}{dt} = 5 - 400y$
- $\frac{dy}{dt} = 5y^{2} - 400$
- $\frac{dy}{dt} = 400 - 5y^{2}$
- $\frac{dy}{dt} = 5y - 400$

- $\frac{dy}{dt}=5-400y$
- $\frac{dy}{dt}=400-5y$ **Correct**
- $\frac{dy}{dt}=5y-400$
- $\frac{dy}{dt}=5{y}^{2}-400$
- $\frac{dy}{dt}=400-5{y}^{2}$

Worked solution:
An inhibited growth equation has the form

$$
\frac{dy}{dt}=k(a-y),
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth equation is

$$
\frac{dy}{dt}=400-5y.
$$

To see this, let's factor the right-hand side of the equation. This gives

$$
\frac{dy}{dt}=5(80-y).
$$

In this case, the constant of proportionality is $k=5,$ and $a=80.$ Note that for inhibited growth, we must have $y<80$ for all $t\ge 0.$

## ORIGINAL q-106663 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dy}{dt}=3(250-y),\,y(0)=150$ **Correct**
- $\frac{dy}{dt}=3(250-y),\,y(0)=400$
- $\frac{dy}{dt}=3(y-250),\,y(0)=200$
- $\frac{dy}{dt}=-3(y+250),\,y(0)=100$
- $\frac{dy}{dt}=3y(y-250),\,y(0)=50$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dy}{dt}=3(250-y),\,y(0)=150.
$$

In this case, $k=3,a=250,$ and ${y}_{0}=150.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problem

$$
\frac{dy}{dt}=3(250-y),\,y(0)=400,
$$

does *not* represent inhibited growth model because ${y}_{0}=400>a=250.$

## ORIGINAL q-37176 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=22P-19\,734,\,P(0)=20\,000$
- $\frac{dP}{dt}=0.02P-875,\,P(0)=47\,500$
- $\frac{dP}{dt}=5\,700-0.8P,\,P(0)=7\,200$
- $\frac{dP}{dt}=1\,250-0.005P,\,P(0)=270\,000$
- $\frac{dP}{dt}=690-0.003P,\,P(0)=200\,000$ **Correct**

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=690-0.003P,\,P(0)=200\,000,
$$

since

$$
\frac{dP}{dt}=690-0.003P=0.003(230\,000-P).
$$

In this case, $k=0.003,a=230\,000,$ and ${y}_{0}=200\,000.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=1\,250-0.005P=0.005(250\,000-P),\,P(0)=270\,000,
$$

and

$$
\frac{dP}{dt}=5\,700-0.8P=0.8(7\,125-P),\,P(0)=7\,200
$$

do *not* represent an inhibited growth model because ${y}_{0}=270\,000>a=250\,000,$ and ${y}_{0}=7\,200>a=7\,125.$

## ORIGINAL q-37177 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=3P-321,\,P(0)=120$
- $\frac{dP}{dt}=8\,200-40P,\,P(0)=210$
- $\frac{dP}{dt}=7-0.000\,2P,\,P(0)=38\,000$
- $\frac{dP}{dt}=830-0.8P,\,P(0)=1\,000$ **Correct**
- $\frac{dP}{dt}=450-0.03P,\,P(0)=16\,000$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=830-0.8P,\,P(0)=1\,000,
$$

since

$$
\frac{dP}{dt}=830-0.8P=0.8(1\,037.5-P).
$$

In this case, $k=0.8,a=1\,037.5,$ and ${y}_{0}=1\,000.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=7-0.000\,2P=0.000\,2(35\,000-P),\,P(0)=38\,000,
$$

$$
\frac{dP}{dt}=450-0.03P=0.03(15\,000-P),\,P(0)=16\,000,
$$

and

$$
\frac{dP}{dt}=8\,200-40P=40(205-P),\,P(0)=210
$$

do *not* represent an inhibited growth model because ${y}_{0}=38\,000>a=35\,000,$ ${y}_{0}=16\,000>a=15\,000,$ and ${y}_{0}=210>a=205.$

## ORIGINAL q-37180 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=9P-6\,066,\,P(0)=680$
- $\frac{dP}{dt}=0.5P-1\,23,\,P(0)=2\,500$
- $\frac{dP}{dt}=12\,510-18P,\,P(0)=690$ **Correct**
- $\frac{dP}{dt}=16\,256-4P,\,P(0)=4\,070$
- $\frac{dP}{dt}=2\,580-0.6P,\,P(0)=4\,400$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=12\,510-18P,\,P(0)=690,
$$

since

$$
\frac{dP}{dt}=12\,510-18P=18(695-P).
$$

In this case, $k=18,a=695,$ and ${y}_{0}=690.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=16\,256-4P=4(4\,064-P),\,P(0)=4\,070,
$$

and

$$
\frac{dP}{dt}=2\,580-0.6P=0.6(4\,300-P),\,P(0)=4\,400
$$

do *not* represent an inhibited growth model because ${y}_{0}=4\,070>a=4\,064,$ and ${y}_{0}=4\,400>a=4\,300.$

## GENERATED observed_106661 — unrated

Given that $y < 410$ and $t \ge 0$, which of the following is an inhibited growth equation?

- $\frac{dy}{dt} = 410(y + 0.5)$
- $\frac{dy}{dt} = 0.5(410 - y)$
- $\frac{dy}{dt} = 0.5(y - 410)$
- $\frac{dy}{dt} = 410(y - 0.5)$
- $\frac{dy}{dt} =-0.5(y + 410)$

## GENERATED observed_106661 — unrated

Given that $y < 180$ and $t \ge 0$, which of the following is an inhibited growth equation?

- $\frac{dy}{dt} = 180(y + 0.5)$
- $\frac{dy}{dt} =-0.5(y + 180)$
- $\frac{dy}{dt} = 180(y - 0.5)$
- $\frac{dy}{dt} = 0.5(180 - y)$
- $\frac{dy}{dt} = 0.5(y - 180)$

## GENERATED observed_106662 — moderate

Given that $y<40$ and $t\ge 0,$ which of the following is an inhibited growth equation?

- $\frac{dy}{dt} = 2y - 80$
- $\frac{dy}{dt} = 80 - 2y^{2}$
- $\frac{dy}{dt} = 2y^{2} - 80$
- $\frac{dy}{dt} = 2 - 80y$
- $\frac{dy}{dt} = 80 - 2y$

- $\frac{dy}{dt}=2{y}^{2}-80$
- $\frac{dy}{dt}=2y-80$
- $\frac{dy}{dt}=80-2y$ **Correct**
- $\frac{dy}{dt}=80-2{y}^{2}$
- $\frac{dy}{dt}=2-80y$

Worked solution:
An inhibited growth equation has the form

$$
\frac{dy}{dt}=k(a-y),
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth equation is

$$
\frac{dy}{dt}=80-2y.
$$

To see this, let's factor the right-hand side of the equation. This gives

$$
\frac{dy}{dt}=2(40-y).
$$

In this case, the constant of proportionality is $k=2,$ and $a=40.$ Note that for inhibited growth, we must have $y<40$ for all $t\ge 0.$

## GENERATED observed_106662 — moderate

Given that $y<90$ and $t\ge 0,$ which of the following is an inhibited growth equation?

- $\frac{dy}{dt} = 3 - 270y$
- $\frac{dy}{dt} = 3y^{2} - 270$
- $\frac{dy}{dt} = 270 - 3y$
- $\frac{dy}{dt} = 3y - 270$
- $\frac{dy}{dt} = 270 - 3y^{2}$

- $\frac{dy}{dt}=3y-270$
- $\frac{dy}{dt}=3-270y$
- $\frac{dy}{dt}=270-3{y}^{2}$
- $\frac{dy}{dt}=270-3y$ **Correct**
- $\frac{dy}{dt}=3{y}^{2}-270$

Worked solution:
An inhibited growth equation has the form

$$
\frac{dy}{dt}=k(a-y),
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth equation is

$$
\frac{dy}{dt}=270-3y.
$$

To see this, let's factor the right-hand side of the equation. This gives

$$
\frac{dy}{dt}=3(90-y).
$$

In this case, the constant of proportionality is $k=3,$ and $a=90.$ Note that for inhibited growth, we must have $y<90$ for all $t\ge 0.$

## GENERATED observed_106663 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dy}{dt}=1y(y-100),\,y(0)=20$
- $\frac{dy}{dt}=-1(y+100),\,y(0)=40$
- $\frac{dy}{dt}=1(y-100),\,y(0)=80$
- $\frac{dy}{dt}=1(100-y),\,y(0)=160$
- $\frac{dy}{dt}=1(100-y),\,y(0)=60$ **Correct**

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dy}{dt}=1(100-y),\,y(0)=60.
$$

In this case, $k=1,a=100,$ and ${y}_{0}=60.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problem

$$
\frac{dy}{dt}=1(100-y),\,y(0)=160,
$$

does *not* represent inhibited growth model because ${y}_{0}=160>a=100.$

## GENERATED observed_106663 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dy}{dt}=2(250-y),\,y(0)=400$
- $\frac{dy}{dt}=2(y-250),\,y(0)=200$
- $\frac{dy}{dt}=2(250-y),\,y(0)=150$ **Correct**
- $\frac{dy}{dt}=2y(y-250),\,y(0)=50$
- $\frac{dy}{dt}=-2(y+250),\,y(0)=100$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dy}{dt}=2(250-y),\,y(0)=150.
$$

In this case, $k=2,a=250,$ and ${y}_{0}=150.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problem

$$
\frac{dy}{dt}=2(250-y),\,y(0)=400,
$$

does *not* represent inhibited growth model because ${y}_{0}=400>a=250.$

## GENERATED observed_37176 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=54.01-0.02P,\,P(0)=2\,720.5$
- $\frac{dP}{dt}=0.005P-303.002\,5,\,P(0)=60\,605.5$
- $\frac{dP}{dt}=11.52-0.000\,2P,\,P(0)=57\,645$
- $\frac{dP}{dt}=0.6P-8\,640,\,P(0)=14\,445$
- $\frac{dP}{dt}=1.94-0.000\,2P,\,P(0)=9\,680$ **Correct**

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=1.94-0.000\,2P,\,P(0)=9\,680,
$$

since

$$
\frac{dP}{dt}=1.94-0.000\,2P=0.000\,2(9\,700-P).
$$

In this case, $k=0.000\,2,a=9\,700,$ and ${y}_{0}=9\,680.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=11.52-0.000\,2P=0.000\,2(57\,600-P),\,P(0)=57\,645,
$$

and

$$
\frac{dP}{dt}=54.01-0.02P=0.02(2\,700.5-P),\,P(0)=2\,720.5
$$

do *not* represent an inhibited growth model because ${y}_{0}=57\,645>a=57\,600,$ and ${y}_{0}=2\,720.5>a=2\,700.5.$

## GENERATED observed_37176 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=10\,160.4-0.8P,\,P(0)=12\,750.5$
- $\frac{dP}{dt}=33\,840-0.8P,\,P(0)=42\,335$
- $\frac{dP}{dt}=0.1P-4\,740.05,\,P(0)=47\,450.5$
- $\frac{dP}{dt}=23\,150-0.5P,\,P(0)=46\,295$ **Correct**
- $\frac{dP}{dt}=0.005P-250.002\,5,\,P(0)=50\,045.5$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=23\,150-0.5P,\,P(0)=46\,295,
$$

since

$$
\frac{dP}{dt}=23\,150-0.5P=0.5(46\,300-P).
$$

In this case, $k=0.5,a=46\,300,$ and ${y}_{0}=46\,295.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=33\,840-0.8P=0.8(42\,300-P),\,P(0)=42\,335,
$$

and

$$
\frac{dP}{dt}=10\,160.4-0.8P=0.8(12\,700.5-P),\,P(0)=12\,750.5
$$

do *not* represent an inhibited growth model because ${y}_{0}=42\,335>a=42\,300,$ and ${y}_{0}=12\,750.5>a=12\,700.5.$

## GENERATED observed_37177 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=54.01-0.02P,\,P(0)=2\,720.5$
- $\frac{dP}{dt}=0.005P-303.002\,5,\,P(0)=60\,605.5$
- $\frac{dP}{dt}=11.52-0.000\,2P,\,P(0)=57\,555$ **Correct**
- $\frac{dP}{dt}=8\,640-0.6P,\,P(0)=14\,445$
- $\frac{dP}{dt}=1.94-0.000\,2P,\,P(0)=9\,720$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=11.52-0.000\,2P,\,P(0)=57\,555,
$$

since

$$
\frac{dP}{dt}=11.52-0.000\,2P=0.000\,2(57\,600-P).
$$

In this case, $k=0.000\,2,a=57\,600,$ and ${y}_{0}=57\,555.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=54.01-0.02P=0.02(2\,700.5-P),\,P(0)=2\,720.5,
$$

$$
\frac{dP}{dt}=1.94-0.000\,2P=0.000\,2(9\,700-P),\,P(0)=9\,720,
$$

and

$$
\frac{dP}{dt}=8\,640-0.6P=0.6(14\,400-P),\,P(0)=14\,445
$$

do *not* represent an inhibited growth model because ${y}_{0}=2\,720.5>a=2\,700.5,$ ${y}_{0}=9\,720>a=9\,700,$ and ${y}_{0}=14\,445>a=14\,400.$

## GENERATED observed_37177 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=10\,160.4-0.8P,\,P(0)=12\,750.5$
- $\frac{dP}{dt}=33\,840-0.8P,\,P(0)=42\,265$ **Correct**
- $\frac{dP}{dt}=4\,740.05-0.1P,\,P(0)=47\,450.5$
- $\frac{dP}{dt}=23\,150-0.5P,\,P(0)=46\,305$
- $\frac{dP}{dt}=0.005P-250.002\,5,\,P(0)=50\,045.5$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=33\,840-0.8P,\,P(0)=42\,265,
$$

since

$$
\frac{dP}{dt}=33\,840-0.8P=0.8(42\,300-P).
$$

In this case, $k=0.8,a=42\,300,$ and ${y}_{0}=42\,265.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=10\,160.4-0.8P=0.8(12\,700.5-P),\,P(0)=12\,750.5,
$$

$$
\frac{dP}{dt}=23\,150-0.5P=0.5(46\,300-P),\,P(0)=46\,305,
$$

and

$$
\frac{dP}{dt}=4\,740.05-0.1P=0.1(47\,400.5-P),\,P(0)=47\,450.5
$$

do *not* represent an inhibited growth model because ${y}_{0}=12\,750.5>a=12\,700.5,$ ${y}_{0}=46\,305>a=46\,300,$ and ${y}_{0}=47\,450.5>a=47\,400.5.$

## GENERATED observed_37180 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=54.01-0.02P,\,P(0)=2\,680.5$ **Correct**
- $\frac{dP}{dt}=0.005P-303.002\,5,\,P(0)=60\,605.5$
- $\frac{dP}{dt}=11.52-0.000\,2P,\,P(0)=57\,645$
- $\frac{dP}{dt}=0.6P-8\,640,\,P(0)=14\,445$
- $\frac{dP}{dt}=1.94-0.000\,2P,\,P(0)=9\,720$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=54.01-0.02P,\,P(0)=2\,680.5,
$$

since

$$
\frac{dP}{dt}=54.01-0.02P=0.02(2\,700.5-P).
$$

In this case, $k=0.02,a=2\,700.5,$ and ${y}_{0}=2\,680.5.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=11.52-0.000\,2P=0.000\,2(57\,600-P),\,P(0)=57\,645,
$$

and

$$
\frac{dP}{dt}=1.94-0.000\,2P=0.000\,2(9\,700-P),\,P(0)=9\,720
$$

do *not* represent an inhibited growth model because ${y}_{0}=57\,645>a=57\,600,$ and ${y}_{0}=9\,720>a=9\,700.$

## GENERATED observed_37180 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=10\,160.4-0.8P,\,P(0)=12\,650.5$ **Correct**
- $\frac{dP}{dt}=33\,840-0.8P,\,P(0)=42\,335$
- $\frac{dP}{dt}=0.1P-4\,740.05,\,P(0)=47\,450.5$
- $\frac{dP}{dt}=23\,150-0.5P,\,P(0)=46\,305$
- $\frac{dP}{dt}=0.005P-250.002\,5,\,P(0)=50\,045.5$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=10\,160.4-0.8P,\,P(0)=12\,650.5,
$$

since

$$
\frac{dP}{dt}=10\,160.4-0.8P=0.8(12\,700.5-P).
$$

In this case, $k=0.8,a=12\,700.5,$ and ${y}_{0}=12\,650.5.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=33\,840-0.8P=0.8(42\,300-P),\,P(0)=42\,335,
$$

and

$$
\frac{dP}{dt}=23\,150-0.5P=0.5(46\,300-P),\,P(0)=46\,305
$$

do *not* represent an inhibited growth model because ${y}_{0}=42\,335>a=42\,300,$ and ${y}_{0}=46\,305>a=46\,300.$

## GENERATED authored_factored — easy

Given that $y < 410$ and $t \ge 0$, which of the following is an inhibited growth equation?

- $\frac{dy}{dt} = 410(y + 0.5)$
- $\frac{dy}{dt} = 0.5(410 - y)$ **Correct**
- $\frac{dy}{dt} = 0.5(y - 410)$
- $\frac{dy}{dt} = 410(y - 0.5)$
- $\frac{dy}{dt} =-0.5(y + 410)$

Worked solution:
An inhibited growth equation has the form

$$
\frac{dy}{dt}=k(a-y),
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth equation is

$$
\frac{dy}{dt} = 0.5(410 - y).
$$

In this case, the constant of proportionality is $k=0.5,$ and $a=410.$ Note that for inhibited growth, we must have $y<410$ for all $t\ge 0.$

## GENERATED authored_factored — easy

Given that $y < 180$ and $t \ge 0$, which of the following is an inhibited growth equation?

- $\frac{dy}{dt} = 180(y + 0.5)$
- $\frac{dy}{dt} =-0.5(y + 180)$
- $\frac{dy}{dt} = 180(y - 0.5)$
- $\frac{dy}{dt} = 0.5(180 - y)$ **Correct**
- $\frac{dy}{dt} = 0.5(y - 180)$

Worked solution:
An inhibited growth equation has the form

$$
\frac{dy}{dt}=k(a-y),
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth equation is

$$
\frac{dy}{dt} = 0.5(180 - y).
$$

In this case, the constant of proportionality is $k=0.5,$ and $a=180.$ Note that for inhibited growth, we must have $y<180$ for all $t\ge 0.$

## GENERATED authored_expanded — moderate

Given that $y<40$ and $t\ge 0,$ which of the following is an inhibited growth equation?

- $\frac{dy}{dt}=2{y}^{2}-80$
- $\frac{dy}{dt}=80-2{y}^{2}$
- $\frac{dy}{dt}=2-80y$
- $\frac{dy}{dt}=2y-80$
- $\frac{dy}{dt}=80-2y$ **Correct**

Worked solution:
An inhibited growth equation has the form

$$
\frac{dy}{dt}=k(a-y),
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth equation is

$$
\frac{dy}{dt}=80-2y.
$$

To see this, let's factor the right-hand side of the equation. This gives

$$
\frac{dy}{dt}=2(40-y).
$$

In this case, the constant of proportionality is $k=2,$ and $a=40.$ Note that for inhibited growth, we must have $y<40$ for all $t\ge 0.$

## GENERATED authored_expanded — moderate

Given that $y<90$ and $t\ge 0,$ which of the following is an inhibited growth equation?

- $\frac{dy}{dt}=3y-270$
- $\frac{dy}{dt}=3-270y$
- $\frac{dy}{dt}=270-3y$ **Correct**
- $\frac{dy}{dt}=3{y}^{2}-270$
- $\frac{dy}{dt}=270-3{y}^{2}$

Worked solution:
An inhibited growth equation has the form

$$
\frac{dy}{dt}=k(a-y),
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth equation is

$$
\frac{dy}{dt}=270-3y.
$$

To see this, let's factor the right-hand side of the equation. This gives

$$
\frac{dy}{dt}=3(90-y).
$$

In this case, the constant of proportionality is $k=3,$ and $a=90.$ Note that for inhibited growth, we must have $y<90$ for all $t\ge 0.$

## GENERATED authored_ivp — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dy}{dt}=1y(y-100),\,y(0)=20$
- $\frac{dy}{dt}=-1(y+100),\,y(0)=40$
- $\frac{dy}{dt}=1(y-100),\,y(0)=80$
- $\frac{dy}{dt}=1(100-y),\,y(0)=160$
- $\frac{dy}{dt}=1(100-y),\,y(0)=60$ **Correct**

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dy}{dt}=1(100-y),\,y(0)=60.
$$

In this case, $k=1,a=100,$ and ${y}_{0}=60.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problem

$$
\frac{dy}{dt}=1(100-y),\,y(0)=160,
$$

does *not* represent inhibited growth model because ${y}_{0}=160>a=100.$

## GENERATED authored_ivp — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dy}{dt}=2(250-y),\,y(0)=400$
- $\frac{dy}{dt}=2(y-250),\,y(0)=200$
- $\frac{dy}{dt}=2(250-y),\,y(0)=150$ **Correct**
- $\frac{dy}{dt}=2y(y-250),\,y(0)=50$
- $\frac{dy}{dt}=-2(y+250),\,y(0)=100$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dy}{dt}=2(250-y),\,y(0)=150.
$$

In this case, $k=2,a=250,$ and ${y}_{0}=150.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problem

$$
\frac{dy}{dt}=2(250-y),\,y(0)=400,
$$

does *not* represent inhibited growth model because ${y}_{0}=400>a=250.$

## GENERATED authored_heterogeneous_2 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=54.01-0.02P,\,P(0)=2\,720.5$
- $\frac{dP}{dt}=0.005P-303.002\,5,\,P(0)=60\,605.5$
- $\frac{dP}{dt}=11.52-0.000\,2P,\,P(0)=57\,645$
- $\frac{dP}{dt}=0.6P-8\,640,\,P(0)=14\,445$
- $\frac{dP}{dt}=1.94-0.000\,2P,\,P(0)=9\,680$ **Correct**

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dP}{dt}=k(a-P),\,P(0)={P}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>P$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=1.94-0.000\,2P,\,P(0)=9\,680,
$$

since

$$
\frac{dP}{dt}=1.94-0.000\,2P=0.000\,2(9\,700-P).
$$

In this case, $k=0.000\,2,a=9\,700,$ and ${P}_{0}=9\,680.$ Notice that $a>{P}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=11.52-0.000\,2P=0.000\,2(57\,600-P),\,P(0)=57\,645,
$$

and

$$
\frac{dP}{dt}=54.01-0.02P=0.02(2\,700.5-P),\,P(0)=2\,720.5
$$

do *not* represent an inhibited growth model because ${P}_{0}=57\,645>a=57\,600,$ and ${P}_{0}=2\,720.5>a=2\,700.5.$

## GENERATED authored_heterogeneous_2 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=10\,160.4-0.8P,\,P(0)=12\,750.5$
- $\frac{dP}{dt}=33\,840-0.8P,\,P(0)=42\,335$
- $\frac{dP}{dt}=0.1P-4\,740.05,\,P(0)=47\,450.5$
- $\frac{dP}{dt}=23\,150-0.5P,\,P(0)=46\,295$ **Correct**
- $\frac{dP}{dt}=0.005P-250.002\,5,\,P(0)=50\,045.5$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dP}{dt}=k(a-P),\,P(0)={P}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>P$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=23\,150-0.5P,\,P(0)=46\,295,
$$

since

$$
\frac{dP}{dt}=23\,150-0.5P=0.5(46\,300-P).
$$

In this case, $k=0.5,a=46\,300,$ and ${P}_{0}=46\,295.$ Notice that $a>{P}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=33\,840-0.8P=0.8(42\,300-P),\,P(0)=42\,335,
$$

and

$$
\frac{dP}{dt}=10\,160.4-0.8P=0.8(12\,700.5-P),\,P(0)=12\,750.5
$$

do *not* represent an inhibited growth model because ${P}_{0}=42\,335>a=42\,300,$ and ${P}_{0}=12\,750.5>a=12\,700.5.$

## GENERATED authored_heterogeneous_3 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=54.01-0.02P,\,P(0)=2\,680.5$ **Correct**
- $\frac{dP}{dt}=0.005P-303.002\,5,\,P(0)=60\,605.5$
- $\frac{dP}{dt}=11.52-0.000\,2P,\,P(0)=57\,645$
- $\frac{dP}{dt}=8\,640-0.6P,\,P(0)=14\,445$
- $\frac{dP}{dt}=1.94-0.000\,2P,\,P(0)=9\,720$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dP}{dt}=k(a-P),\,P(0)={P}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>P$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=54.01-0.02P,\,P(0)=2\,680.5,
$$

since

$$
\frac{dP}{dt}=54.01-0.02P=0.02(2\,700.5-P).
$$

In this case, $k=0.02,a=2\,700.5,$ and ${P}_{0}=2\,680.5.$ Notice that $a>{P}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=8\,640-0.6P=0.6(14\,400-P),\,P(0)=14\,445,
$$

$$
\frac{dP}{dt}=1.94-0.000\,2P=0.000\,2(9\,700-P),\,P(0)=9\,720,
$$

and

$$
\frac{dP}{dt}=11.52-0.000\,2P=0.000\,2(57\,600-P),\,P(0)=57\,645
$$

do *not* represent an inhibited growth model because ${P}_{0}=14\,445>a=14\,400,$ ${P}_{0}=9\,720>a=9\,700,$ and ${P}_{0}=57\,645>a=57\,600.$

## GENERATED authored_heterogeneous_3 — hard

Which of the following initial value problems is an inhibited growth problem?

- $\frac{dP}{dt}=10\,160.4-0.8P,\,P(0)=12\,650.5$ **Correct**
- $\frac{dP}{dt}=33\,840-0.8P,\,P(0)=42\,335$
- $\frac{dP}{dt}=4\,740.05-0.1P,\,P(0)=47\,450.5$
- $\frac{dP}{dt}=23\,150-0.5P,\,P(0)=46\,305$
- $\frac{dP}{dt}=0.005P-250.002\,5,\,P(0)=50\,045.5$

Worked solution:
An inhibited growth initial value problem has the form

$$
\frac{dP}{dt}=k(a-P),\,P(0)={P}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>P$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=10\,160.4-0.8P,\,P(0)=12\,650.5,
$$

since

$$
\frac{dP}{dt}=10\,160.4-0.8P=0.8(12\,700.5-P).
$$

In this case, $k=0.8,a=12\,700.5,$ and ${P}_{0}=12\,650.5.$ Notice that $a>{P}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=4\,740.05-0.1P=0.1(47\,400.5-P),\,P(0)=47\,450.5,
$$

$$
\frac{dP}{dt}=23\,150-0.5P=0.5(46\,300-P),\,P(0)=46\,305,
$$

and

$$
\frac{dP}{dt}=33\,840-0.8P=0.8(42\,300-P),\,P(0)=42\,335
$$

do *not* represent an inhibited growth model because ${P}_{0}=47\,450.5>a=47\,400.5,$ ${P}_{0}=46\,305>a=46\,300,$ and ${P}_{0}=42\,335>a=42\,300.$
