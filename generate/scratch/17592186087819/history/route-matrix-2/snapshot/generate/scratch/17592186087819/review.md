# Matrices for Route Planning: source and generated review

Basis 1356; raw capture in source.json. Source figure paths alone are localized. Observed scalar windows are catalogs with unresolved author intent, not inferred errors. Generated counts are independently read from arrow sidecars and displayed ordered tables.

## Original replay q-138940

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/cb/cbdf5c2470229ae3ba10ee18bccd2dc764407897397466b157474bf2b819f5d9.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $1$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $1$ | $0$ | $0$ |  |

**selection (radio):** 3, 2, 1, 5, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $1$ |
| **B** | $0$ | $1$ | $2$ |  |
| **C** | $1$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Original replay q-139685

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/ab/abbc0e5ce20a52263ba067d1563708f803e33def4f931a3d3badedd1c8ff4908.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $a$ | $1$ | $1$ |
| **B** | $b$ | $0$ | $1$ |  |
| **C** | $1$ | $c$ | $0$ |  |

**selection (radio):** 2, 1 ✓, 0, 5, 3

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $a=0.$

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from $B$ to $A,$ and so $b=0.$

- There is $1$ arrow starting at Station C and ending at Station B. So, there is only one route from $C$ to $B,$ and so $c=1.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $1$ |
| **B** | $0$ | $0$ | $1$ |  |
| **C** | $1$ | $1$ | $0$ |  |

Therefore, 

$$
a + b + c = 0+0+1 = 1.
$$

## Original replay q-139689

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/6c/6c52f315d079b82fb729c4ab47f210ec4bf2683d0dfe1adfe79c94db9fbc5f63.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$a$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$b$</td>
<td align="center">$2$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$c$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

**selection (radio):** 2 ✓, 1, 0, 4, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are no arrows starting at Station C and ending at Station A. So, there are no routes from $C$ to $A,$ and so $c=0.$

As a result, our route matrix is the following:

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$1$</td>
<td align="center">$2$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$0$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

Therefore, 

$$
a+b+c=1+1+0=2.
$$

## Original replay q-139719

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/0e/0ed581569bdc7c4f269f4cdf48d3ae20205627312641ff5b06daa2dca5a0e168.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $0$ | $a$ |
| **B** | $0$ | $0$ | $b$ | $0$ |  |
| **C** | $0$ | $0$ | $c$ | $1$ |  |
| **D** | $0$ | $0$ | $1$ | $0$ |  |

**selection (radio):** 2, 1, 0, 4, 3 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station D. So, there are two routes from $A$ to $D,$ and so $a=2.$

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $b=1.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $0$ | $2$ |
| **B** | $0$ | $0$ | $1$ | $0$ |  |
| **C** | $0$ | $0$ | $0$ | $1$ |  |
| **D** | $0$ | $0$ | $1$ | $0$ |  |

Therefore, 

$$
a+b+c=2+1+0=3.
$$

## Original replay q-319346

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/f5/f5297b339026b8b2ec9666a37bcb59a73297bf8a691690999ca41f5313cb3c93.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | {{field-3}} |  |
| **C** | $2$ | $0$ | $0$ |  |

**field-1 (blank):** 2 ✓

**field-2 (blank):** 1 ✓

**field-3 (blank):** 3 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are $2$ routes from A to B.

- There is $1$ arrow starting at Station B and ending at Station A. So, there is $1$ route from B to A.

- There are $3$ arrows starting at Station B and ending at Station C. So, there is $3$ route from B to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $2$ | $0$ |
| **B** | $1$ | $0$ | $3$ |  |
| **C** | $2$ | $0$ | $0$ |  |

## Original replay q-319412

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/e7/e7c2810c5ccfa768d356e19e69cf9a54d21fcf608ed4863bd3da0b672313403e.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | $1$ | $0$ |  |
| **C** | $1$ | $0$ | {{field-3}} | $2$ |  |
| **D** | $0$ | $1$ | $1$ | $0$ |  |

**field-1 (blank):** 2 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station C. So, there are $2$ routes from A to C.

- There are $2$ arrows starting at Station B and ending at Station A. So, there are $2$ routes from B to A.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from C to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $2$ | $0$ |
| **B** | $2$ | $0$ | $1$ | $0$ |  |
| **C** | $1$ | $0$ | $0$ | $2$ |  |
| **D** | $0$ | $1$ | $1$ | $0$ |  |

## Original replay q-319429

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/76/76cff940632cac02300b538a4ef063cfe3e8a699b2d406c998725a6c6fa1eee6.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | {{field-1}} |
| **B** | $1$ | {{field-2}} | $2$ |  |
| **C** | $0$ | {{field-3}} | $1$ |  |

**field-1 (blank):** 3 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are $3$ arrows starting at Station A and ending at Station C. So, there are $3$ routes from A to C.

- There are $2$ arrows starting at Station B and ending at Station B. So, there are $2$ routes from B to B.

- There is $1$ arrow starting at Station C and ending at Station B. So, there is $1$ route from C to B.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | $3$ |
| **B** | $1$ | $2$ | $2$ |  |
| **C** | $0$ | $1$ | $1$ |  |

## Raw observed prose q-319429 (direction error retained as evidence)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/76/76cff940632cac02300b538a4ef063cfe3e8a699b2d406c998725a6c6fa1eee6.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | {{field-1}} |
| **B** | $1$ | {{field-2}} | $2$ |  |
| **C** | $0$ | {{field-3}} | $1$ |  |

**field-1 (blank):** 3 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are $3$ arrows starting at Station A and ending at Station C. So, there are $3$ routes from A to C.

- There are $2$ arrows starting at Station B and ending at Station C. So, there are $2$ routes from B to C.

- There is $1$ arrow starting at Station C and ending at Station B. So, there is $1$ route from C to B.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | $3$ |
| **B** | $1$ | $2$ | $2$ |  |
| **C** | $0$ | $1$ | $1$ |  |

## Generated variant easy sum_138940 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/c21eb50e0ed5949d5255c5f128aaea0d45968625322478643faee023f656c675.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $1$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $2$ | $0$ | $0$ |  |

**selection (radio):** 5, 1, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $1$ |
| **B** | $0$ | $1$ | $2$ |  |
| **C** | $2$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Generated variant easy sum_138940 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/5ebdcd17735c0fcf90e9d8e55de5d38120dfbba02c98d8343dcc66c8e021a395.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $1$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $1$ | $0$ | $0$ |  |

**selection (radio):** 4 ✓, 5, 3, 2, 1

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $a=2.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $c=1.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $2$ | $1$ |
| **B** | $0$ | $1$ | $1$ |  |
| **C** | $1$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 2+1+1 = 4.
$$

## Generated variant easy sum_139685 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/d8b9324e3595e97f12f0fefb32d74e1d6c5ae97cc917bb3e5e7bff193aed27ca.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $a$ | $1$ | $2$ |
| **B** | $b$ | $0$ | $1$ |  |
| **C** | $1$ | $c$ | $0$ |  |

**selection (radio):** 5, 0 ✓, 2, 1, 3

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $a=0.$

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from $B$ to $A,$ and so $b=0.$

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from $C$ to $B,$ and so $c=0.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $2$ |
| **B** | $0$ | $0$ | $1$ |  |
| **C** | $1$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 0+0+0 = 0.
$$

## Generated variant easy sum_139685 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/f8143111b0fe8a3532ea14a350a65ab94e1ba51e1dde484506c4c557f6b63590.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $a$ | $1$ | $1$ |
| **B** | $b$ | $0$ | $1$ |  |
| **C** | $2$ | $c$ | $0$ |  |

**selection (radio):** 3, 5, 2 ✓, 1, 0

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $a=0.$

- There are $2$ arrows starting at Station B and ending at Station A. So, there are two routes from $B$ to $A,$ and so $b=2.$

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from $C$ to $B,$ and so $c=0.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $1$ |
| **B** | $2$ | $0$ | $1$ |  |
| **C** | $2$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 0+2+0 = 2.
$$

## Generated variant moderate sum_139689 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/cef1270bc46e537afa7fbf4ba456cea729349f0ad7196b3b891d950572e1e8ed.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$a$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$b$</td>
<td align="center">$1$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$c$</td>
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

**selection (radio):** 4 ✓, 0, 2, 1, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station C and ending at Station A. So, there are two routes from $C$ to $A,$ and so $c=2.$

As a result, our route matrix is the following:

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$1$</td>
<td align="center">$1$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$2$</td>
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

Therefore, 

$$
a+b+c=1+1+2=4.
$$

## Generated variant moderate sum_139689 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/f9420cf5ddf4929ab4ee45235b0e922a7c4a008e272efe4659fb4a58bd87be8e.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$a$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$b$</td>
<td align="center">$2$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$c$</td>
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

**selection (radio):** 3, 4, 2, 1, 0 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station B. So, there are no routes from $A$ to $B,$ and so $a=0.$

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $b=0.$

- There are no arrows starting at Station C and ending at Station A. So, there are no routes from $C$ to $A,$ and so $c=0.$

As a result, our route matrix is the following:

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$0$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$0$</td>
<td align="center">$2$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$0$</td>
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

Therefore, 

$$
a+b+c=0+0+0=0.
$$

## Generated variant easy sum_139719 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/9cf9cf3e3bedcaefc942214169e322d7d0336a24cc4274dadc22692b1d0a1552.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $2$ | $0$ | $a$ |
| **B** | $0$ | $0$ | $b$ | $0$ |  |
| **C** | $0$ | $0$ | $c$ | $1$ |  |
| **D** | $0$ | $0$ | $2$ | $0$ |  |

**selection (radio):** 4, 0, 2 ✓, 1, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station D. So, there is only one route from $A$ to $D,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $b=1.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $2$ | $0$ | $1$ |
| **B** | $0$ | $0$ | $1$ | $0$ |  |
| **C** | $0$ | $0$ | $0$ | $1$ |  |
| **D** | $0$ | $0$ | $2$ | $0$ |  |

Therefore, 

$$
a+b+c=1+1+0=2.
$$

## Generated variant easy sum_139719 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/08932a6ae802dd2fa1e015c0a936b9f6e6cd43890a28936ebcaded445570f941.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $0$ | $a$ |
| **B** | $0$ | $0$ | $b$ | $0$ |  |
| **C** | $0$ | $0$ | $c$ | $2$ |  |
| **D** | $0$ | $0$ | $2$ | $0$ |  |

**selection (radio):** 3, 4, 2 ✓, 1, 0

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station D. So, there are no routes from $A$ to $D,$ and so $a=0.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $b=2.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $0$ | $0$ |
| **B** | $0$ | $0$ | $2$ | $0$ |  |
| **C** | $0$ | $0$ | $0$ | $2$ |  |
| **D** | $0$ | $0$ | $2$ | $0$ |  |

Therefore, 

$$
a+b+c=0+2+0=2.
$$

## Generated variant easy blanks_319346 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/dbaa8c8550566a5a636c79333613092b00506c510353a9524119be089b7d8e74.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | {{field-3}} |  |
| **C** | $1$ | $0$ | $0$ |  |

**field-1 (blank):** 2 ✓

**field-2 (blank):** 1 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are $2$ routes from A to B.

- There is $1$ arrow starting at Station B and ending at Station A. So, there is $1$ route from B to A.

- There is $1$ arrow starting at Station B and ending at Station C. So, there is $1$ route from B to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $2$ | $0$ |
| **B** | $1$ | $0$ | $1$ |  |
| **C** | $1$ | $0$ | $0$ |  |

## Generated variant easy blanks_319346 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/0322af921cae754fe7b71ebe7e2b6ac9da76d27920c6a03988ed9ba584809329.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | {{field-3}} |  |
| **C** | $2$ | $0$ | $0$ |  |

**field-1 (blank):** 1 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 2 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is $1$ route from A to B.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

- There are $2$ arrows starting at Station B and ending at Station C. So, there are $2$ routes from B to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $0$ |
| **B** | $0$ | $0$ | $2$ |  |
| **C** | $2$ | $0$ | $0$ |  |

## Generated variant easy blanks_319412 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/341ece398edb42bdfddb298e01ec26293bca8f0199808454a6e80efc6785e22e.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | $1$ | $0$ |  |
| **C** | $1$ | $0$ | {{field-3}} | $2$ |  |
| **D** | $0$ | $1$ | $2$ | $0$ |  |

**field-1 (blank):** 0 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

- There is $1$ arrow starting at Station C and ending at Station C. So, there is $1$ route from C to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $0$ | $0$ |
| **B** | $0$ | $0$ | $1$ | $0$ |  |
| **C** | $1$ | $0$ | $1$ | $2$ |  |
| **D** | $0$ | $1$ | $2$ | $0$ |  |

## Generated variant easy blanks_319412 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/9ecff1779e458c96aa99661bcbf154fd3348d547240fb9a715bdeb4dbb4180bd.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | $2$ | $0$ |  |
| **C** | $2$ | $0$ | {{field-3}} | $1$ |  |
| **D** | $0$ | $1$ | $1$ | $0$ |  |

**field-1 (blank):** 0 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from C to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $0$ | $0$ |
| **B** | $0$ | $0$ | $2$ | $0$ |  |
| **C** | $2$ | $0$ | $0$ | $1$ |  |
| **D** | $0$ | $1$ | $1$ | $0$ |  |

## Generated variant easy blanks_319429 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/dccfe567c7f4d5c6bf2def399a78eccd49b165bd0315de418d04e8c5466ce175.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | {{field-1}} |
| **B** | $1$ | {{field-2}} | $2$ |  |
| **C** | $0$ | {{field-3}} | $1$ |  |

**field-1 (blank):** 1 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station C. So, there is $1$ route from A to C.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from B to B.

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from C to B.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | $1$ |
| **B** | $1$ | $0$ | $2$ |  |
| **C** | $0$ | $0$ | $1$ |  |

## Generated variant easy blanks_319429 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/ce8542c6db73b8ed57c68e73f43ef34183393f8e57a35ace8495e12fe77ba3b9.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | {{field-1}} |
| **B** | $2$ | {{field-2}} | $1$ |  |
| **C** | $0$ | {{field-3}} | $1$ |  |

**field-1 (blank):** 0 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from B to B.

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from C to B.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | $0$ |
| **B** | $2$ | $0$ | $1$ |  |
| **C** | $0$ | $0$ | $1$ |  |

## Generated variant hard sum_permuted_four 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/351846a93f8b3c0515f366c8bb0be989c8f317295ed87caef2df5f2e2356a17e.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **D** | **C** | **B** |
| From: | **D** | $c$ | $1$ | $0$ | $0$ |
| **B** | $b$ | $0$ | $0$ | $0$ |  |
| **A** | $0$ | $0$ | $1$ | $0$ |  |
| **C** | $1$ | $0$ | $a$ | $2$ |  |

**selection (radio):** 6, 2, 4 ✓, 3, 5

Let's examine our diagram.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $a=0.$

- There are $2$ arrows starting at Station B and ending at Station A. So, there are two routes from $B$ to $A,$ and so $b=2.$

- There are $2$ arrows starting at Station D and ending at Station A. So, there are two routes from $D$ to $A,$ and so $c=2.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **D** | **C** | **B** |
| From: | **D** | $2$ | $1$ | $0$ | $0$ |
| **B** | $2$ | $0$ | $0$ | $0$ |  |
| **A** | $0$ | $0$ | $1$ | $0$ |  |
| **C** | $1$ | $0$ | $0$ | $2$ |  |

Therefore, 

$$
a+b+c=0+2+2=4.
$$

## Generated variant hard sum_permuted_four 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/ddc2e3ce4729057b1dd7c3bf7065e3d66b475722d63be5fd79ae54ecbda354ca.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **D** | **C** | **B** |
| From: | **B** | $0$ | $0$ | $0$ | $a$ |
| **A** | $1$ | $c$ | $b$ | $0$ |  |
| **D** | $0$ | $0$ | $1$ | $2$ |  |
| **C** | $0$ | $1$ | $0$ | $0$ |  |

**selection (radio):** 4, 5, 3 ✓, 2, 1

Let's examine our diagram.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $a=0.$

- There is $1$ arrow starting at Station A and ending at Station C. So, there is only one route from $A$ to $C,$ and so $b=1.$

- There are $2$ arrows starting at Station A and ending at Station D. So, there are two routes from $A$ to $D,$ and so $c=2.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **D** | **C** | **B** |
| From: | **B** | $0$ | $0$ | $0$ | $0$ |
| **A** | $1$ | $2$ | $1$ | $0$ |  |
| **D** | $0$ | $0$ | $1$ | $2$ |  |
| **C** | $0$ | $1$ | $0$ | $0$ |  |

Therefore, 

$$
a+b+c=0+1+2=3.
$$

## Optional authored omission bank easy 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/cb/cbdf5c2470229ae3ba10ee18bccd2dc764407897397466b157474bf2b819f5d9.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $1$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $1$ | $0$ | $0$ |  |

**selection (radio):** 1, 6, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $1$ |
| **B** | $0$ | $1$ | $2$ |  |
| **C** | $1$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Optional authored omission bank easy 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/474088c8d8d42100ae476b17e3f5a4a7bf9aa59f2a48dc1ae176fd9e0b1892f1.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $2$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $2$ | $0$ | $0$ |  |

**selection (radio):** 1, 8, 2, 3, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $2$ |
| **B** | $0$ | $1$ | $2$ |  |
| **C** | $2$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Optional authored omission bank moderate 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/f51d55290d3834b57f1bb7e885fd0b87519dc500c17343457f95e348f8f4d7d9.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$a$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$b$</td>
<td align="center">$2$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$c$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

**selection (radio):** 1, 8, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station C and ending at Station A. So, there are two routes from $C$ to $A,$ and so $c=2.$

As a result, our route matrix is the following:

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$1$</td>
<td align="center">$2$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$2$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

Therefore, 

$$
a+b+c=1+1+2=4.
$$

## Optional authored omission bank moderate 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/cef1270bc46e537afa7fbf4ba456cea729349f0ad7196b3b891d950572e1e8ed.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$a$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$b$</td>
<td align="center">$1$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$c$</td>
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

**selection (radio):** 1, 8, 2, 3, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station C and ending at Station A. So, there are two routes from $C$ to $A,$ and so $c=2.$

As a result, our route matrix is the following:

<table align="center" cellpadding="10" rules="all">
<tbody><tr>
<td></td>
<td></td>
<td align="center" colspan="3">To:</td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
</tr>
<tr>
<td align="center" rowspan="3">From:</td>
<td align="center" bgcolor="#D6EAF8" width="30"><b>A</b></td>
<td align="center">$1$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$1$</td>
<td align="center">$1$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$2$</td>
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

Therefore, 

$$
a+b+c=1+1+2=4.
$$
