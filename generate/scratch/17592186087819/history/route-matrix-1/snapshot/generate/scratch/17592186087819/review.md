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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/54a7fc9fc1fd70afe9c4a0ec378dd0d1c41ae08b417aff08353416d341f1bc5a.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $2$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $3$ | $0$ | $0$ |  |

**selection (radio):** 5, 1 ✓, 3, 2, 4

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $b=0.$

- There are no arrows starting at Station B and ending at Station C. So, there are no routes from $B$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $2$ |
| **B** | $0$ | $0$ | $0$ |  |
| **C** | $3$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 1+0+0 = 1.
$$

## Generated variant easy sum_138940 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/bb31e2917652541de13835df438214ebc02a4ac8f2b2e39935f284fc6e65f709.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $1$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $2$ | $0$ | $0$ |  |

**selection (radio):** 4, 5, 3 ✓, 2, 1

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $a=2.$

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $b=0.$

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $c=1.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $2$ | $1$ |
| **B** | $0$ | $0$ | $1$ |  |
| **C** | $2$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 2+0+1 = 3.
$$

## Generated variant easy sum_139685 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/ec63c2259a808809bbc33c0242cd4b1390c909a50cea2a1e971454f420564398.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $a$ | $3$ | $2$ |
| **B** | $b$ | $0$ | $3$ |  |
| **C** | $3$ | $c$ | $0$ |  |

**selection (radio):** 5, 0, 2, 1 ✓, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station A. So, there is only one route from $A$ to $A,$ and so $a=1.$

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from $B$ to $A,$ and so $b=0.$

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from $C$ to $B,$ and so $c=0.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $3$ | $2$ |
| **B** | $0$ | $0$ | $3$ |  |
| **C** | $3$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 1+0+0 = 1.
$$

## Generated variant easy sum_139685 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/f0a950b3601ee29da5aeccfcd26ad3198e2212711e701169e6188bc915c5aaa2.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $a$ | $1$ | $1$ |
| **B** | $b$ | $0$ | $3$ |  |
| **C** | $1$ | $c$ | $0$ |  |

**selection (radio):** 3 ✓, 5, 2, 1, 0

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station A. So, there are two routes from $A$ to $A,$ and so $a=2.$

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from $B$ to $A,$ and so $b=0.$

- There is $1$ arrow starting at Station C and ending at Station B. So, there is only one route from $C$ to $B,$ and so $c=1.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $2$ | $1$ | $1$ |
| **B** | $0$ | $0$ | $3$ |  |
| **C** | $1$ | $1$ | $0$ |  |

Therefore, 

$$
a + b + c = 2+0+1 = 3.
$$

## Generated variant moderate sum_139689 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/c360ca8c4870967f28d8639944bf6471f9efb4dfdebd40fdbdd37f218b557ce9.png)

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
<td align="center">$3$</td>
<td align="center">$a$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$b$</td>
<td align="center">$3$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$c$</td>
<td align="center">$3$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

**selection (radio):** 4, 0, 2, 1 ✓, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

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
<td align="center">$3$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$0$</td>
<td align="center">$3$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$0$</td>
<td align="center">$3$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

Therefore, 

$$
a+b+c=1+0+0=1.
$$

## Generated variant moderate sum_139689 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/8fed10484a2c5c052272bba4bf456dc7ca2220d9215385ae4ca2e8b0619a75ba.png)

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

**selection (radio):** 3 ✓, 4, 2, 1, 0

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $a=2.$

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $b=0.$

- There is $1$ arrow starting at Station C and ending at Station A. So, there is only one route from $C$ to $A,$ and so $c=1.$

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
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$0$</td>
<td align="center">$1$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$1$</td>
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

Therefore, 

$$
a+b+c=2+0+1=3.
$$

## Generated variant easy sum_139719 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/c591c499cfc6559119b7b28305fa385729354562c5f31afd3c0950e73932203f.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $3$ | $0$ | $a$ |
| **B** | $0$ | $0$ | $b$ | $0$ |  |
| **C** | $0$ | $0$ | $c$ | $3$ |  |
| **D** | $0$ | $0$ | $3$ | $0$ |  |

**selection (radio):** 4, 0, 2, 1 ✓, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station D. So, there is only one route from $A$ to $D,$ and so $a=1.$

- There are no arrows starting at Station B and ending at Station C. So, there are no routes from $B$ to $C,$ and so $b=0.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $3$ | $0$ | $1$ |
| **B** | $0$ | $0$ | $0$ | $0$ |  |
| **C** | $0$ | $0$ | $0$ | $3$ |  |
| **D** | $0$ | $0$ | $3$ | $0$ |  |

Therefore, 

$$
a+b+c=1+0+0=1.
$$

## Generated variant easy sum_139719 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/0f8f60111059ade78bcd33f235ddda6862035d4453b329306cf69260d09e3b3b.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $0$ | $a$ |
| **B** | $0$ | $0$ | $b$ | $0$ |  |
| **C** | $0$ | $0$ | $c$ | $1$ |  |
| **D** | $0$ | $0$ | $2$ | $0$ |  |

**selection (radio):** 3 ✓, 4, 2, 1, 0

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station D. So, there are two routes from $A$ to $D,$ and so $a=2.$

- There are no arrows starting at Station B and ending at Station C. So, there are no routes from $B$ to $C,$ and so $b=0.$

- There is $1$ arrow starting at Station C and ending at Station C. So, there is only one route from $C$ to $C,$ and so $c=1.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $0$ | $2$ |
| **B** | $0$ | $0$ | $0$ | $0$ |  |
| **C** | $0$ | $0$ | $1$ | $1$ |  |
| **D** | $0$ | $0$ | $2$ | $0$ |  |

Therefore, 

$$
a+b+c=2+0+1=3.
$$

## Generated variant easy blanks_319346 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/738a13583b7e8198f74f67f0e09f4a9dc1fccd3935296a472bb54dfc96739bab.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | {{field-3}} |  |
| **C** | $3$ | $0$ | $0$ |  |

**field-1 (blank):** 1 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is $1$ route from A to B.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

- There are no arrows starting at Station B and ending at Station C. So, there are no routes from B to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $0$ |
| **B** | $0$ | $0$ | $0$ |  |
| **C** | $3$ | $0$ | $0$ |  |

## Generated variant easy blanks_319346 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/3bfc6f6f22210199e445be3363233b026da3821875db46b7d5bd22748eef9f7a.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | {{field-3}} |  |
| **C** | $1$ | $0$ | $0$ |  |

**field-1 (blank):** 3 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are $3$ arrows starting at Station A and ending at Station B. So, there are $3$ routes from A to B.

- There are $2$ arrows starting at Station B and ending at Station A. So, there are $2$ routes from B to A.

- There are no arrows starting at Station B and ending at Station C. So, there are no routes from B to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $3$ | $0$ |
| **B** | $2$ | $0$ | $0$ |  |
| **C** | $1$ | $0$ | $0$ |  |

## Generated variant easy blanks_319412 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/f001541fd0be2bfd8912099440fda96c047e6bf419b2e7071d355fd6c807b35b.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $2$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | $2$ | $0$ |  |
| **C** | $1$ | $0$ | {{field-3}} | $1$ |  |
| **D** | $0$ | $1$ | $3$ | $0$ |  |

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
| From: | **A** | $0$ | $2$ | $0$ | $0$ |
| **B** | $0$ | $0$ | $2$ | $0$ |  |
| **C** | $1$ | $0$ | $1$ | $1$ |  |
| **D** | $0$ | $1$ | $3$ | $0$ |  |

## Generated variant easy blanks_319412 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/d00a949a9c685a040326775a27e171c8a349ad83b7819c78fdb053e1a6b2b541.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | {{field-1}} | $0$ |
| **B** | {{field-2}} | $0$ | $1$ | $0$ |  |
| **C** | $2$ | $0$ | {{field-3}} | $2$ |  |
| **D** | $0$ | $1$ | $3$ | $0$ |  |

**field-1 (blank):** 1 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station C. So, there is $1$ route from A to C.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

- There is $1$ arrow starting at Station C and ending at Station C. So, there is $1$ route from C to C.

Therefore, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** | **D** |
| From: | **A** | $0$ | $1$ | $1$ | $0$ |
| **B** | $0$ | $0$ | $1$ | $0$ |  |
| **C** | $2$ | $0$ | $1$ | $2$ |  |
| **D** | $0$ | $1$ | $3$ | $0$ |  |

## Generated variant easy blanks_319429 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/443d3156c7ffd0e616dc153a5c01bad790855af6d880f84299461dbbd7c51220.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $3$ | $2$ | {{field-1}} |
| **B** | $3$ | {{field-2}} | $1$ |  |
| **C** | $0$ | {{field-3}} | $1$ |  |

**field-1 (blank):** 0 ✓

**field-2 (blank):** 3 ✓

**field-3 (blank):** 3 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

- There are $3$ arrows starting at Station B and ending at Station B. So, there are $3$ routes from B to B.

- There are $3$ arrows starting at Station C and ending at Station B. So, there are $3$ routes from C to B.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $3$ | $2$ | $0$ |
| **B** | $3$ | $3$ | $1$ |  |
| **C** | $0$ | $3$ | $1$ |  |

## Generated variant easy blanks_319429 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/bbc1c5e56adf5b86ac169df93437cf09fee138399c438b811a3000750d8e5538.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | {{field-1}} |
| **B** | $1$ | {{field-2}} | $2$ |  |
| **C** | $0$ | {{field-3}} | $3$ |  |

**field-1 (blank):** 1 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station C. So, there is $1$ route from A to C.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from B to B.

- There is $1$ arrow starting at Station C and ending at Station B. So, there is $1$ route from C to B.

Therefore, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $1$ | $1$ | $1$ |
| **B** | $1$ | $0$ | $2$ |  |
| **C** | $0$ | $1$ | $3$ |  |

## Generated variant hard sum_permuted_four 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/3076645f4956fa47a133fb2edb2e357e85b974adc7de4dcb263654bc7e57ea54.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **C** | **A** | **D** | **B** |
| From: | **D** | $0$ | $0$ | $0$ | $0$ |
| **B** | $3$ | $2$ | $1$ | $0$ |  |
| **A** | $0$ | $a$ | $0$ | $b$ |  |
| **C** | $0$ | $1$ | $c$ | $1$ |  |

**selection (radio):** 13, 5 ✓, 2, 4, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station A. So, there is only one route from $A$ to $A,$ and so $a=1.$

- There are $3$ arrows starting at Station A and ending at Station B. So, there are three routes from $A$ to $B,$ and so $b=3.$

- There is $1$ arrow starting at Station C and ending at Station D. So, there is only one route from $C$ to $D,$ and so $c=1.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **C** | **A** | **D** | **B** |
| From: | **D** | $0$ | $0$ | $0$ | $0$ |
| **B** | $3$ | $2$ | $1$ | $0$ |  |
| **A** | $0$ | $1$ | $0$ | $3$ |  |
| **C** | $0$ | $1$ | $1$ | $1$ |  |

Therefore, 

$$
a+b+c=1+3+1=5.
$$

## Generated variant hard sum_permuted_four 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/c51e16d11c124810c425fa8eb8066445c866dfb47d64c70cd05e70ed3ad05ebf.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **C** | **A** | **B** | **D** |
| From: | **C** | $0$ | $0$ | $0$ | $1$ |
| **B** | $1$ | $0$ | $1$ | $0$ |  |
| **D** | $1$ | $0$ | $c$ | $0$ |  |
| **A** | $b$ | $a$ | $0$ | $1$ |  |

**selection (radio):** 1, 11, 4, 3, 6 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station A. So, there is only one route from $A$ to $A,$ and so $a=1.$

- There are $2$ arrows starting at Station A and ending at Station C. So, there are two routes from $A$ to $C,$ and so $b=2.$

- There are $3$ arrows starting at Station D and ending at Station B. So, there are three routes from $D$ to $B,$ and so $c=3.$

As a result, our route matrix is the following:

|  |  | To: |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | **C** | **A** | **B** | **D** |
| From: | **C** | $0$ | $0$ | $0$ | $1$ |
| **B** | $1$ | $0$ | $1$ | $0$ |  |
| **D** | $1$ | $0$ | $3$ | $0$ |  |
| **A** | $2$ | $1$ | $0$ | $1$ |  |

Therefore, 

$$
a+b+c=1+2+3=6.
$$

## Authored bank easy 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/f07ebbdb5d4d13f782053d6e8e75ebbd25991f8dae0d26802a0475961cdc8506.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $3$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $1$ | $0$ | $0$ |  |

**selection (radio):** 1, 8, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $1$ | $3$ |
| **B** | $0$ | $1$ | $2$ |  |
| **C** | $1$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Authored bank easy 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/b1c14900a5dc302dd26e961019a6dac862893831ed7922d296a4045eb519e97e.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

|  |  | To: |  |  |
| --- | ---: | ---: | ---: | ---: |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $a$ | $3$ |
| **B** | $0$ | $b$ | $c$ |  |
| **C** | $1$ | $0$ | $0$ |  |

**selection (radio):** 2, 11, 4, 5, 7 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $a=2.$

- There are $2$ arrows starting at Station B and ending at Station B. So, there are two routes from $B$ to $B,$ and so $b=2.$

- There are $3$ arrows starting at Station B and ending at Station C. So, there are three routes from $B$ to $C,$ and so $c=3.$

As a result, our route matrix is the following:

|  |  | To: |  |  |
| --- | --- | --- | --- | --- |
|  |  | **A** | **B** | **C** |
| From: | **A** | $0$ | $2$ | $3$ |
| **B** | $0$ | $2$ | $3$ |  |
| **C** | $1$ | $0$ | $0$ |  |

Therefore, 

$$
a + b + c = 2+2+3 = 7.
$$

## Authored bank moderate 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/c0cd2c79b98a22e5f7b8d612994e23d63ef0f1f33693ca503042464925243785.png)

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
<td align="center">$3$</td>
<td align="center">$a$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$b$</td>
<td align="center">$3$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$c$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

**selection (radio):** 1, 11, 3, 2, 4 ✓

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
<td align="center">$3$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$1$</td>
<td align="center">$3$</td>
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

## Authored bank moderate 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/72f087cbdd78d1c11d1f890637ecfb58e2554383a63e5a6882c062c834af6ca4.png)

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

**selection (radio):** 2, 11, 4, 5, 7 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $a=2.$

- There are $2$ arrows starting at Station B and ending at Station B. So, there are two routes from $B$ to $B,$ and so $b=2.$

- There are $3$ arrows starting at Station C and ending at Station A. So, there are three routes from $C$ to $A,$ and so $c=3.$

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
<td align="center">$2$</td>
<td align="center">$0$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>B</b></td>
<td align="center">$0$</td>
<td align="center">$2$</td>
<td align="center">$2$</td>
</tr>
<tr>
<td align="center" bgcolor="#D6EAF8" width="30"><b>C</b></td>
<td align="center">$3$</td>
<td align="center">$1$</td>
<td align="center">$0$</td>
</tr>
</tbody></table>

Therefore, 

$$
a+b+c=2+2+3=7.
$$
