# 17592186049731 Invertible Functions

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125752 — Introduction

A function is **invertible** on an interval if and only if it's one-to-one. In other words, it must pass the horizontal line test.

Not all functions have inverses! For example, consider the function $f(x)=x^2-1$ whose graph is shown below. 

![](images/e9/e99832fa1867a8314dda20f392d0c897ebb2942ac91a652ab1cf474b5d2d9612.png)

Notice that $f(x)$ is not a one-to-one since it does not satisfy the horizontal line test.

To find the graph of a function's inverse, we usually reflect it over the line $y=x.$ However, if we reflect $f(x)$ over the line $y=x,$ the result is not a function since it will not satisfy the vertical line test.

![](images/7a/7a5a95f1cc3e2c8b40e865a24d22f4529e47c3c0137a6cb8d0369059f4a89a56.png)

Therefore, $f(x)$ is *not* invertible.

If a function is not invertible, we can sometimes make it invertible by restricting its domain.

Here, if we take $f(x)=x^2-1$ over the restricted interval $x \in (0,\infty),$ then it passes the horizontal line test and we can find the corresponding inverse function by reflecting the graph of $y=f(x)$ over the line $y=x.$

![](images/0a/0a7f98c2dce4599ee74cc13dc53c3a693b9c3716ffe54c708811f4c011f18b6d.png)

To determine if a function is invertible over a particular domain, we need to use the horizontal line test to check if it's a one-to-one function.



### example 17592186124283 — Identifying an Invertible Function From Its Graph

Which of the graphs below correspond to an invertible function?

![](images/6f/6fbded3e0a3faefda0e1f2c8418f5e271fb116cde4082487096378f89511b695.png)

A function is invertible if and only if it's a one-to-one function. To determine which of the functions are one-to-one, we use the horizontal line test.  

![](images/50/5036479a948abee5644cd3b96632f6aaf8ee370f7473ba27e11d25bb84ddb781.png)

From the above, we see that: 

- In graph IV, any horizontal line will intersect the curve at most once, no matter where we draw the line. Therefore, graph IV  shows a one-to-one function. This means that the function is invertible.

- For graphs I, II, and III, some horizontal lines intersect the curve more than once. So, these are not one-to-one functions. As a result, they are not invertible.

Therefore, the correct answer is "IV only".

### example 17592186124284 — Identifying the Intervals on Which a Function is Invertible Given Its Graph

![](images/d9/d965e0b1087ad45206dd9259c963609f556bf5803af47ab18006bf40dffb2557.png)

     

On which of the following intervals is the function $f(x)$ (shown above) invertible?

I. $(-3,-1]$

II. $(0,4]$

III. $[-2,2)$

A function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test.   

- The given function is invertible on the interval $x\in (-3,-1].$  Indeed, any horizontal line will intersect the curve at most once, no matter where we draw the line.

![](images/24/245484a6a77160a5f5892738a7e1f8e488f6df8e4ba990bbc94ae964c3305525.png)

- The given function is **not** invertible on the intervals $(0,4]$ and $[-2,2)$ because some horizontal lines will intersect the curve more than once.

![](images/47/4737a1460e1abd4edc200404407fef10761f038d9a29e52ba0f8c3e8c69bb93f.png)

          

Therefore, the correct answer is "I  only".

### example 17592186124285 — Identifying the Intervals on Which a Function is Invertible Given a Description

Given that $f(x)=|x-2|-2,$ on which of the following intervals is $f(x)$ invertible?

I. $x \in (-\infty, 2]$

II. $x \in (0, \infty)$

III. $x \in (-1,4]$

First, let's graph the given function. The graph of the function $f(x)=|x-2|-2$ can be obtained in the following way:  

1\. Take the curve $y=|x|.$

2\. Translate it by $2$ units to the right,  to get $y= |x-2|.$

3\. Finally, translate $y= |x-2|$ by $2$ units down to get $f(x)=|x-2|-2.$

![](images/60/60c2601abfd3c4034991408f47b75c8cf70a1bccb72f73b2f9624a52d0ed7b42.png)

Now, remember that a function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test. 

- The function $f(x)$ is invertible on the interval $x\in(-\infty,2].$  Indeed, on this interval, any horizontal line will intersect the curve at most once, no matter where we draw the line.

![](images/45/45b0cdd26280d9379a449af41edbc9e69dd9d76f3b4116d938fbe708c21f6f29.png)

- The function $f(x)$ is not invertible on any of the intervals $x\in(0,\infty)$ and $x \in (-1,4].$ On these intervals, some horizontal lines will intersect the curve more than once.

![](images/55/55b8483c59362d3a59dfd269db74f2c5f17a97cee1f25c896ece16890d80bd42.png)

  

Therefore, the correct answer is "I only".

## Representative practice (first three per skill; full bank in practice.json)

### Identifying an Invertible Function From Its Graph (26 captured questions)

Question 17592186124945 — None

Which of the graphs below correspond to an invertible function?

Select all that apply.

Solution: Graphs I and II are strictly monotone and pass the horizontal line test. Graphs III and IV each meet some horizontal line twice. There are four graphs, so all four labels are represented.

Answer ![Graph III](images/f1/f1b632f3a7dd97a4fea48833028cef766b001beba6966f8ab6aa8523859e353a.svg): false

Answer ![Graph II](images/7c/7c0ab470aa65066b1f0cb7dd0f4649885e7bf3c01b3f58c59681c16d59e39c8f.svg): true

Answer ![Graph IV](images/6e/6e612e0d248bca692e1cd90d665dac0b81a22dd698d31dc47d02a8dd861d0dd1.svg): false

Answer ![Graph I](images/ca/ca3114048dd78effaad82921c0448062ab788ff336a9b072e4565a2e2fc1ce35.svg): true

Question 17592186125018 — None

Which of the graphs below correspond to an invertible function?

Select all that apply.

Solution: Graph I is strictly increasing. Graph II has a local minimum and maximum, graph III first decreases to a visible local minimum and then increases, and graph IV is a downward parabola. Thus II, III, and IV fail the horizontal line test; only I is invertible.

Answer ![Graph III](images/3c/3c01cf271870556b9e6870ac7c814c05496c010a7b7e8ebb7b16905188af5df2.svg): false

Answer ![Graph II](images/b6/b64560a9c02ce12767fa06b42e2dfc9bd9e8ba6bb9392ff21cfa78507997df6e.svg): false

Answer ![Graph IV](images/46/4651b8b75b33ee763d138713d25e4255b607851f1fd53cdbbf2de2e89a82f590.svg): false

Answer ![Graph I](images/1f/1f40de0e90c070042f23318ca1d53475b95b9cd1e1e45da6571bca5b5e939d5c.svg): true

Answer None of the above: false

Question 17592186244143 — question.difficulty/moderate

Which of the graphs below correspond to an invertible function?

Select all that apply.

Solution: A function is invertible if and only if it's a one-to-one function. To determine which of the functions are one-to-one, we use the horizontal line test.

![](images/cf/cfb095836b7498c91a5cbd9d2cb694715a0d89a12a5e6ea5ff417342c4bde798.png)

From the above, we see that:

- For graph III, any horizontal line will intersect the curve at most once, no matter where we draw the line. Therefore, graph III shows a one-to-one function. As a result, this function is invertible.

- For graphs I, II, and IV, some horizontal lines intersect the curve more than once. These are not one-to-one functions. As a result, they are not invertible.

Answer ![Graph III](images/45/45c8195e54ab766f50439d63146e299f0602766b6c3d7c37942282db6e578185.svg): true

Answer ![Graph II](images/86/86abd8cebd946cacb0f6e6b5c36cf9292a3c5d99e471822307b0638377949b95.svg): false

Answer ![Graph IV](images/26/26893dd5faa2990bc8bfd53602863ee15fbad8008c52c59a3abd19b960904c70.svg): false

Answer ![Graph I](images/74/749427225b10ed6998d384640273a2583f58ec596bb8ac9f006f53662e62850a.svg): false

### Identifying the Intervals on Which a Function is Invertible Given Its Graph (30 captured questions)

Question 17592186124951 — question.difficulty/moderate

![](images/93/936cea1e20ef7bbc1eb66acf9dd564c61476f5bb68ee05e553b00aaf3f970dc3.png)

On which of the following intervals is the function $f(x)$ (shown above) invertible?

Select all that apply.

Solution: A function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test.  

- The given function is invertible on each of the intervals $x\in [-4,0]$ and $x\in (-4,-2].$ Indeed, any horizontal line will intersect the curve at most once, no matter where we draw the line.

![](images/a4/a4499c2d4995c09b9ab6f8852cc2982f415f1650d65429c86df83800344106f4.png)

- The given function is **not** invertible on the interval $x\in (-3,1]$  because some lines will intersect the curve at more than one point.

![](images/cb/cb0a462b3af10d15bb586f127baac45a74eecd5dc19848bda23664e75de968a4.png)

Therefore, the correct answer is $x\in [-4,0]$; $x\in (-4,-2]$ only.

Answer $x\in (-3,1)$: false

Answer $x\in (-4,-2]$: true

Answer $x\in [-4,0]$: true

Question 17592186125021 — question.difficulty/hard

![](images/3c/3cbdac583a4cdf1b5eb761892934516a0b4edd1487bd402ae0014859c4a0ad53.png)

On which of the following intervals is the function $f(x)$ (shown above) invertible?

Select all that apply.

Solution: A function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test.

- The given function is invertible on the interval $x\in (-2,0].$ Indeed, a horizontal line will intersect the curve at most once, no matter where we draw the line.

![](images/d7/d7c6e8d314483ad67e89ce5d4675b7af27fa08c88a4ed9d95eed9ad2a4da51cc.png)

- The given function is **not** invertible on the intervals $x\in (-2,2]$ and $x\in [-4,-2]\cup [2,4]$ because some horizontal lines will intersect the curve more than once.

![](images/ce/cee829f7e3d5f32b0acb54cb5c40406d8391d2a2967c68df0c1f5e1cae87d729.png)

Therefore, the correct answer is $x\in (-2,0]$ only.

Answer $x\in (-2,0]$: true

Answer $x\in (-2,2]$: false

Answer $x\in [-4,-2]\cup [2,4]$: false

Question 17592186244150 — question.difficulty/hard

![](images/81/811ead4928d2f245235736dce473d121261ea358ca4ff3a0cc8b01bb2e9f3b31.png)

On which of the following intervals is the function $f(x)$ (shown above) invertible?

Select all that apply.

Solution: A function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test.

- The given function is invertible on the interval $x\in (-\infty ,-3].$ Indeed, any horizontal line will intersect the curve at most once, no matter where we draw the line.

![](images/32/32f1ad5bdec30951900a1c30c2996ea040e65880f859c43769faf374db06a2f0.png)

- The given function is **not** invertible on the intervals $x\in (-3,3)$ and $x\in [1,4]$ because some horizontal lines will intersect the curve more than once.

![](images/8e/8ed451b24fa83de513f4a1b5c79d39f94add784c6b7265e765a3381e7b03363a.png)

Therefore, the correct answer is $x\in (-\infty ,-3]$ only.

Answer $x\in (-3,3)$: false

Answer $x\in (-\infty ,-3]$: true

Answer $x\in [1,4]$: false

### Identifying the Intervals on Which a Function is Invertible Given a Description (28 captured questions)

Question 17592186125195 — question.difficulty/moderate

Given that $f(x)={x}^{2}+2,$ on which of the following intervals is $f(x)$ invertible?

Select all that apply.

Solution: The graph of the function $f(x)={x}^{2}+2$ can be obtained in the following way:

- Take the curve $y={x}^{2}.$

- Translate it by $2$ units up to get $f(x)={x}^{2}+2.$

![](images/ff/ff3d1ac7500d83574b8671b23e99d4a0f1dbd6ab9cebc906aa06ff2c21f95345.png)

A function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test.

- The function $f(x)$ is not invertible on the interval $x\in (-2,2).$ On this interval, some horizontal lines will intersect the curve more than once.

![](images/a7/a71ce036adc5dc0b15fce9e367a0c8512699dc6a7814f4e9a1886696d2abad6e.png)

- The function $f(x)$ is invertible on the intervals $x\in [0,\infty )$ and  $x\in (-\infty ,0].$ On these intervals, any horizontal line will intersect the curve at most once, no matter where we draw the line.

![](images/68/6858bd1fab8d9659c84fa941cd63ee9f509c8364dce0e753706c640ecfe6e9ec.png)

Therefore, the correct answer is $x\in [0,\infty )$; $x\in (-\infty ,0]$ only.

Answer $x\in (-2,2)$: false

Answer $x\in (-\infty ,0]$: true

Answer $x\in [0,\infty )$: true

Question 17592186125196 — question.difficulty/easy

Given that $f(x)=x+1,$ on which of the following intervals is $f(x)$ invertible?

Select all that apply.

Solution: The function $f(x)$ is a linear function with slope $1$ and $y$-intercept $1,$ as shown below.

![](images/00/00d6394343d441ee10fa20ee029b8f89b52ff1e6ded8e7fdbe0756118212f1a8.png)

A function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test.

- The given function is invertible on the interval $x\in (-\infty ,\infty ).$ On this interval, a horizontal line will intersect the curve at most once, no matter where we draw the line.

- Since the function is invertible on $x\in (-\infty ,\infty ),$ it is also invertible on  $x\in (-1,\infty )$ and $x\in (-10,5).$

Therefore, the correct answer is $x\in (-\infty ,\infty )$; $x\in (-1,\infty )$; $x\in (-10,5)$.

Answer $x\in (-1,\infty )$: true

Answer $x\in (-10,5)$: true

Answer $x\in (-\infty ,\infty )$: true

Question 17592186234209 — question.difficulty/moderate

Given that $f(x)=|x-4|+2,$ on which of the following intervals is $f(x)$ invertible?

Select all that apply.

Solution: The graph of the function $f(x)=|x-4|+2$ can be obtained in the following way:

- Take the curve $y=|x|.$

- Translate it by $4$ units to the right,  to get $y=|x-4|.$

- Finally, translate $y=|x-4|$ by $2$ units up to get $f(x)=|x-4|+2.$

![](images/56/56956d0f23ae6828098507712fd00525dc4f114a195716dc16e63d8475e9c143.png)

A function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test. 

- The function $f(x)$ is invertible on the interval $x\in (-\infty ,3).$  Indeed, on this interval, any horizontal line will intersect the curve at most once, no matter where we draw the line.

- The function $f(x)$ is not invertible on any of the intervals $x\in (1,\infty )$  and $(-\infty ,5].$ On each of these intervals, some horizontal lines will intersect the curve more than once.

Therefore, the correct answer is $x\in (-\infty ,3)$ only.

Answer $x\in (-\infty ,3)$: true

Answer $x\in (-\infty ,5]$: false

Answer $x\in (1,\infty )$: false
