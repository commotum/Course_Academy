# Substitution review

Source originals are raw captured evidence. Generated replays repair presentation only; missing solutions and answers are independently authored. Context defaults additionally supply the missing first equation.

## Original q-171690

```text
Consider the following system of equations:
${x + 5y = 13; y = x + 5$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$$,
{{field-2}}
$)$
```

Captured fields: [{"key": "field-2", "type": ":answer-field.type/blank", "values": [], "correct_value": null}, {"key": "field-1", "type": ":answer-field.type/blank", "values": [], "correct_value": null}]

```text
No captured worked solution.
```

## Presentation-normalized replay q-171690

Consider the following system of equations:
$\{x+5y=13; y=x+5$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$, $
{{field-2}}
$)$

field-1: $-2$ (correct)
field-2: $3$ (correct)

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the second equation is already solved for $y:$

$$
y=x+5
$$

So, we replace $y$ in the first equation and solve for $x:$

$$
\begin{aligned}x+5y & =13 \\ x+5(x+5) & =13 \\ x+5x+25 & =13 \\ 6x+25 & =13 \\ 6x & =-12 \\ x & =-2\end{aligned}
$$

If we now substitute $x=-2$ into $y=x+5,$ we can then find the value of $y:$

$$
\begin{aligned}y & =(-2)+5 \\ y & =3\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-2,\,y=3.$

## Original q-4133

```text
Given the system of equations below, what is the value of $a - b$?

${3a + 2b = 4; - 4a + b = 2$
```

Captured fields: [{"key": "selection", "type": ":answer-field.type/radio", "values": ["-1", "2", "1", "3", "-2"], "correct_value": null}]

```text
No captured worked solution.
```

## Presentation-normalized replay q-4133

Given the system of equations below, what is the value of $a - b$?

$\{3a+2b=4; -4a+b=2$

selection: $1$, $-2$ (correct), $-1$, $2$, $3$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}-4a+b & =2 \\ b & =2+4a\end{aligned}
$$

Then, we substitute $b=2+4a$ into the first equation and solve for $a:$

$$
\begin{aligned}3a+2b & =4 \\ 3a+2(2+4a) & =4 \\ 3a+4+8a & =4 \\ 11a+4 & =4 \\ 11a & =0 \\ a & =0\end{aligned}
$$

If we now substitute $a=0$ into $b=2+4a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =2+4(0) \\ b & =2\end{aligned}
$$

Therefore, $a-b=0-(2)=-2.$

## Original q-5179

```text
Given the system of equations below, what is the value of $p - q$?

${3p = 15; p + 2q = 9$
```

Captured fields: [{"key": "selection", "type": ":answer-field.type/radio", "values": ["3", "-4", "-3", "2", "5"], "correct_value": null}]

```text
No captured worked solution.
```

## Presentation-normalized replay q-5179

Given the system of equations below, what is the value of $p - q$?

$\{3p=15; p+2q=9$

selection: $-3$, $5$, $3$ (correct), $-4$, $2$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the first equation, we can isolate $p$ by dividing both sides by $3:$

$$
\begin{aligned}3p & =15 \\ p & =5\end{aligned}
$$

Then, we substitute $p=5$ into the second equation and solve for $q:$

$$
\begin{aligned}p+2q & =9 \\ (5)+2q & =9 \\ 2q & =4 \\ q & =2\end{aligned}
$$

Therefore, $p-q=5-(2)=3.$

## Original q-167194

```text
The coefficients $a$ and $b$ also satisfy the equation $20b+400a=7\,200.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}
```

Captured fields: [{"key": "field-1", "type": ":answer-field.type/blank", "values": ["-12"], "correct_value": "-12"}, {"key": "field-2", "type": ":answer-field.type/blank", "values": ["600"], "correct_value": "600"}]

```text
We have the following system of linear equations:

$$
{\begin{aligned}b=480-10a \\ 20b+400a=7\,200\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=480-10a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}20b+400a & =7\,200 \\ 20(480-10a)+400a & =7\,200 \\ 9\,600-200a+400a & =7\,200 \\ 9\,600+200a & =7\,200 \\ 200a & =-2\,400 \\ a & =-12\end{aligned}
$$

If we now substitute $a=-12$ into $b=480-10a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =480-10(-12) \\ b & =600\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-12,\,b=600.$
```

## Presentation-normalized replay q-167194

The coefficients $a$ and $b$ also satisfy the equation $20b+400a=7\,200.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-12$ (correct)
field-2: $600$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=480-10a \\ 20b+400a=7\,200\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=480-10a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}20b+400a & =7\,200 \\ 20(480-10a)+400a & =7\,200 \\ 9\,600-200a+400a & =7\,200 \\ 9\,600+200a & =7\,200 \\ 200a & =-2\,400 \\ a & =-12\end{aligned}
$$

If we now substitute $a=-12$ into $b=480-10a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =480-10(-12) \\ b & =600\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-12,\,b=600.$

## Original q-167210

```text
The coefficients $a$ and $b$ also satisfy the equation $30b+900a=6\,000.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}
```

Captured fields: [{"key": "field-1", "type": ":answer-field.type/blank", "values": ["-4"], "correct_value": "-4"}, {"key": "field-2", "type": ":answer-field.type/blank", "values": ["320"], "correct_value": "320"}]

```text
We have the following system of linear equations:

$$
{\begin{aligned}b=240-20a \\ 30b+900a=6\,000\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=240-20a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}30b+900a & =6\,000 \\ 30(240-20a)+900a & =6\,000 \\ 7\,200-600a+900a & =6\,000 \\ 7\,200+300a & =6\,000 \\ 300a & =-1\,200 \\ a & =-4\end{aligned}
$$

If we now substitute $a=-4$ into $b=240-20a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =240-20(-4) \\ b & =320\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-4,\,b=320.$
```

## Presentation-normalized replay q-167210

The coefficients $a$ and $b$ also satisfy the equation $30b+900a=6\,000.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-4$ (correct)
field-2: $320$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=240-20a \\ 30b+900a=6\,000\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=240-20a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}30b+900a & =6\,000 \\ 30(240-20a)+900a & =6\,000 \\ 7\,200-600a+900a & =6\,000 \\ 7\,200+300a & =6\,000 \\ 300a & =-1\,200 \\ a & =-4\end{aligned}
$$

If we now substitute $a=-4$ into $b=240-20a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =240-20(-4) \\ b & =320\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-4,\,b=320.$

## Original q-167226

```text
The coefficients $a$ and $b$ also satisfy the equation $70a+9b=600.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}
```

Captured fields: [{"key": "field-1", "type": ":answer-field.type/blank", "values": ["-3"], "correct_value": "-3"}, {"key": "field-2", "type": ":answer-field.type/blank", "values": ["90"], "correct_value": "90"}]

```text
We have the following system of linear equations:

$$
{\begin{aligned}b=75-5a \\ 70a+9b=600\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=75-5a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}70a+9b & =600 \\ 70a+9(75-5a) & =600 \\ 70a+675-45a & =600 \\ 25a+675 & =600 \\ 25a & =-75 \\ a & =-3\end{aligned}
$$

If we now substitute $a=-3$ into $b=75-5a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =75-5(-3) \\ b & =90\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-3,\,b=90.$
```

## Presentation-normalized replay q-167226

The coefficients $a$ and $b$ also satisfy the equation $70a+9b=600.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-3$ (correct)
field-2: $90$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=75-5a \\ 70a+9b=600\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=75-5a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}70a+9b & =600 \\ 70a+9(75-5a) & =600 \\ 70a+675-45a & =600 \\ 25a+675 & =600 \\ 25a & =-75 \\ a & =-3\end{aligned}
$$

If we now substitute $a=-3$ into $b=75-5a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =75-5(-3) \\ b & =90\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-3,\,b=90.$

## Generated observed-profile variant for q-171690

Consider the following system of equations:
$\{x+4y=-10; y=x-5$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$, $
{{field-2}}
$)$

field-1: $2$ (correct)
field-2: $-3$ (correct)

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the second equation is already solved for $y:$

$$
y=x-5
$$

So, we replace $y$ in the first equation and solve for $x:$

$$
\begin{aligned}x+4y & =-10 \\ x+4(x-5) & =-10 \\ x+4x-20 & =-10 \\ 5x-20 & =-10 \\ 5x & =10 \\ x & =2\end{aligned}
$$

If we now substitute $x=2$ into $y=x-5,$ we can then find the value of $y:$

$$
\begin{aligned}y & =(2)-5 \\ y & =-3\end{aligned}
$$

Therefore, the solution to the system of equations is $x=2,\,y=-3.$

## Generated observed-profile variant for q-4133

Given the system of equations below, what is the value of $a - b$?

$\{-5a-2b=7; 2a+b=-1$

selection: $14$, $-7$, $21$, $7$, $-14$ (correct)

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}2a+b & =-1 \\ b & =-1-2a\end{aligned}
$$

Then, we substitute $b=-1-2a$ into the first equation and solve for $a:$

$$
\begin{aligned}-5a-2b & =7 \\ -5a-2(-1-2a) & =7 \\ -5a+2+4a & =7 \\ -a+2 & =7 \\ -a & =5 \\ a & =-5\end{aligned}
$$

If we now substitute $a=-5$ into $b=-1-2a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =-1-2(-5) \\ b & =9\end{aligned}
$$

Therefore, $a-b=-5-(9)=-14.$

## Generated observed-profile variant for q-5179

Given the system of equations below, what is the value of $p - q$?

$\{3p=3; p+3q=10$

selection: $-6$, $-2$ (correct), $3$, $2$, $1$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the first equation, we can isolate $p$ by dividing both sides by $3:$

$$
\begin{aligned}3p & =3 \\ p & =1\end{aligned}
$$

Then, we substitute $p=1$ into the second equation and solve for $q:$

$$
\begin{aligned}p+3q & =10 \\ (1)+3q & =10 \\ 3q & =9 \\ q & =3\end{aligned}
$$

Therefore, $p-q=1-(3)=-2.$

## Generated observed-profile variant for q-167194

The coefficients $a$ and $b$ also satisfy the equation $8b+141a=940.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-4$ (correct)
field-2: $188$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=140-12a \\ 8b+141a=940\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=140-12a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}8b+141a & =940 \\ 8(140-12a)+141a & =940 \\ 1\,120-96a+141a & =940 \\ 1\,120+45a & =940 \\ 45a & =-180 \\ a & =-4\end{aligned}
$$

If we now substitute $a=-4$ into $b=140-12a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =140-12(-4) \\ b & =188\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-4,\,b=188.$

## Generated observed-profile variant for q-167210

The coefficients $a$ and $b$ also satisfy the equation $8b+141a=940.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-4$ (correct)
field-2: $188$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=140-12a \\ 8b+141a=940\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=140-12a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}8b+141a & =940 \\ 8(140-12a)+141a & =940 \\ 1\,120-96a+141a & =940 \\ 1\,120+45a & =940 \\ 45a & =-180 \\ a & =-4\end{aligned}
$$

If we now substitute $a=-4$ into $b=140-12a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =140-12(-4) \\ b & =188\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-4,\,b=188.$

## Generated observed-profile variant for q-167226

The coefficients $a$ and $b$ also satisfy the equation $141a+8b=940.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-4$ (correct)
field-2: $188$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=140-12a \\ 141a+8b=940\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=140-12a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}141a+8b & =940 \\ 141a+8(140-12a) & =940 \\ 141a+1\,120-96a & =940 \\ 45a+1\,120 & =940 \\ 45a & =-180 \\ a & =-4\end{aligned}
$$

If we now substitute $a=-4$ into $b=140-12a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =140-12(-4) \\ b & =188\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-4,\,b=188.$

## Authored default easy coefficient_b_first

The coefficients $a$ and $b$ satisfy $b=180-15a.$

The coefficients $a$ and $b$ also satisfy the equation $3b+95a=90.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-9$ (correct)
field-2: $315$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=180-15a \\ 3b+95a=90\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=180-15a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}3b+95a & =90 \\ 3(180-15a)+95a & =90 \\ 540-45a+95a & =90 \\ 540+50a & =90 \\ 50a & =-450 \\ a & =-9\end{aligned}
$$

If we now substitute $a=-9$ into $b=180-15a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =180-15(-9) \\ b & =315\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-9,\,b=315.$

## Authored default easy coefficient_b_first

The coefficients $a$ and $b$ satisfy $b=100-20a.$

The coefficients $a$ and $b$ also satisfy the equation $29b+600a=2\,800.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-5$ (correct)
field-2: $200$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=100-20a \\ 29b+600a=2\,800\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=100-20a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}29b+600a & =2\,800 \\ 29(100-20a)+600a & =2\,800 \\ 2\,900-580a+600a & =2\,800 \\ 2\,900+20a & =2\,800 \\ 20a & =-100 \\ a & =-5\end{aligned}
$$

If we now substitute $a=-5$ into $b=100-20a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =100-20(-5) \\ b & =200\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-5,\,b=200.$

## Authored default easy coefficient_a_first

The coefficients $a$ and $b$ satisfy $b=180-15a.$

The coefficients $a$ and $b$ also satisfy the equation $95a+3b=90.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-9$ (correct)
field-2: $315$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=180-15a \\ 95a+3b=90\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=180-15a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}95a+3b & =90 \\ 95a+3(180-15a) & =90 \\ 95a+540-45a & =90 \\ 50a+540 & =90 \\ 50a & =-450 \\ a & =-9\end{aligned}
$$

If we now substitute $a=-9$ into $b=180-15a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =180-15(-9) \\ b & =315\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-9,\,b=315.$

## Authored default easy coefficient_a_first

The coefficients $a$ and $b$ satisfy $b=100-20a.$

The coefficients $a$ and $b$ also satisfy the equation $600a+29b=2\,800.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

field-1: $-5$ (correct)
field-2: $200$ (correct)

We have the following system of linear equations:

$$
\{\begin{aligned}b=100-20a \\ 600a+29b=2\,800\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=100-20a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}600a+29b & =2\,800 \\ 600a+29(100-20a) & =2\,800 \\ 600a+2\,900-580a & =2\,800 \\ 20a+2\,900 & =2\,800 \\ 20a & =-100 \\ a & =-5\end{aligned}
$$

If we now substitute $a=-5$ into $b=100-20a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =100-20(-5) \\ b & =200\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-5,\,b=200.$

## Authored default easy tuple_xy

Consider the following system of equations:
$\{x+5y=-10; y=x-8$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$, $
{{field-2}}
$)$

field-1: $5$ (correct)
field-2: $-3$ (correct)

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the second equation is already solved for $y:$

$$
y=x-8
$$

So, we replace $y$ in the first equation and solve for $x:$

$$
\begin{aligned}x+5y & =-10 \\ x+5(x-8) & =-10 \\ x+5x-40 & =-10 \\ 6x-40 & =-10 \\ 6x & =30 \\ x & =5\end{aligned}
$$

If we now substitute $x=5$ into $y=x-8,$ we can then find the value of $y:$

$$
\begin{aligned}y & =(5)-8 \\ y & =-3\end{aligned}
$$

Therefore, the solution to the system of equations is $x=5,\,y=-3.$

## Authored default easy tuple_xy

Consider the following system of equations:
$\{x+3y=-33; y=x-3$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$, $
{{field-2}}
$)$

field-1: $-6$ (correct)
field-2: $-9$ (correct)

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the second equation is already solved for $y:$

$$
y=x-3
$$

So, we replace $y$ in the first equation and solve for $x:$

$$
\begin{aligned}x+3y & =-33 \\ x+3(x-3) & =-33 \\ x+3x-9 & =-33 \\ 4x-9 & =-33 \\ 4x & =-24 \\ x & =-6\end{aligned}
$$

If we now substitute $x=-6$ into $y=x-3,$ we can then find the value of $y:$

$$
\begin{aligned}y & =(-6)-3 \\ y & =-9\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-6,\,y=-9.$

## Authored default easy direct_pq

Given the system of equations below, what is the value of $p - q$?

$\{2p=10; p+4q=29$

selection: $-1$ (correct), $1$, $5$, $11$, $6$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the first equation, we can isolate $p$ by dividing both sides by $2:$

$$
\begin{aligned}2p & =10 \\ p & =5\end{aligned}
$$

Then, we substitute $p=5$ into the second equation and solve for $q:$

$$
\begin{aligned}p+4q & =29 \\ (5)+4q & =29 \\ 4q & =24 \\ q & =6\end{aligned}
$$

Therefore, $p-q=5-(6)=-1.$

## Authored default easy direct_pq

Given the system of equations below, what is the value of $p - q$?

$\{4p=-16; p+2q=-16$

selection: $-2$, $2$ (correct), $-4$, $-10$, $-6$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the first equation, we can isolate $p$ by dividing both sides by $4:$

$$
\begin{aligned}4p & =-16 \\ p & =-4\end{aligned}
$$

Then, we substitute $p=-4$ into the second equation and solve for $q:$

$$
\begin{aligned}p+2q & =-16 \\ (-4)+2q & =-16 \\ 2q & =-12 \\ q & =-6\end{aligned}
$$

Therefore, $p-q=-4-(-6)=2.$

## Authored default moderate difference_ab

Given the system of equations below, what is the value of $a - b$?

$\{2a+2b=22; -4a+b=1$

selection: $-7$ (correct), $7$, $2$, $11$, $9$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}-4a+b & =1 \\ b & =1+4a\end{aligned}
$$

Then, we substitute $b=1+4a$ into the first equation and solve for $a:$

$$
\begin{aligned}2a+2b & =22 \\ 2a+2(1+4a) & =22 \\ 2a+2+8a & =22 \\ 10a+2 & =22 \\ 10a & =20 \\ a & =2\end{aligned}
$$

If we now substitute $a=2$ into $b=1+4a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =1+4(2) \\ b & =9\end{aligned}
$$

Therefore, $a-b=2-(9)=-7.$

## Authored default moderate difference_ab

Given the system of equations below, what is the value of $a - b$?

$\{2a+2b=-2; 2a+b=5$

selection: $-13$, $13$ (correct), $6$, $-1$, $-7$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}2a+b & =5 \\ b & =5-2a\end{aligned}
$$

Then, we substitute $b=5-2a$ into the first equation and solve for $a:$

$$
\begin{aligned}2a+2b & =-2 \\ 2a+2(5-2a) & =-2 \\ 2a+10-4a & =-2 \\ -2a+10 & =-2 \\ -2a & =-12 \\ a & =6\end{aligned}
$$

If we now substitute $a=6$ into $b=5-2a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =5-2(6) \\ b & =-7\end{aligned}
$$

Therefore, $a-b=6-(-7)=13.$

## Authored default hard unit_pair

Find the solution $(x,y)$ to this system using the method of substitution.

$\{-2x+3y=-6; 4x+y=-4$

The solution is $($ {{field-1}} $, $ {{field-2}} $)$

field-1: $-\frac{3}{7}$ (correct)
field-2: $-\frac{16}{7}$ (correct)

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $y$:

$$
\begin{aligned}4x+y & =-4 \\ y & =-4-4x\end{aligned}
$$

Then, we substitute $y=-4-4x$ into the first equation and solve for $x:$

$$
\begin{aligned}-2x+3y & =-6 \\ -2x+3(-4-4x) & =-6 \\ -2x-12-12x & =-6 \\ -14x-12 & =-6 \\ -14x & =6 \\ x & =-\frac{3}{7}\end{aligned}
$$

If we now substitute $x=-\frac{3}{7}$ into $y=-4-4x,$ we can then find the value of $y:$

$$
\begin{aligned}y & =-4-4(-\frac{3}{7}) \\ y & =-\frac{16}{7}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-\frac{3}{7},\,y=-\frac{16}{7}.$

## Authored default hard unit_pair

Find the solution $(x,y)$ to this system using the method of substitution.

$\{-3x+3y=-12; -4x+y=1$

The solution is $($ {{field-1}} $, $ {{field-2}} $)$

field-1: $-\frac{5}{3}$ (correct)
field-2: $-\frac{17}{3}$ (correct)

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $y$:

$$
\begin{aligned}-4x+y & =1 \\ y & =1+4x\end{aligned}
$$

Then, we substitute $y=1+4x$ into the first equation and solve for $x:$

$$
\begin{aligned}-3x+3y & =-12 \\ -3x+3(1+4x) & =-12 \\ -3x+3+12x & =-12 \\ 9x+3 & =-12 \\ 9x & =-15 \\ x & =-\frac{5}{3}\end{aligned}
$$

If we now substitute $x=-\frac{5}{3}$ into $y=1+4x,$ we can then find the value of $y:$

$$
\begin{aligned}y & =1+4(-\frac{5}{3}) \\ y & =-\frac{17}{3}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-\frac{5}{3},\,y=-\frac{17}{3}.$
