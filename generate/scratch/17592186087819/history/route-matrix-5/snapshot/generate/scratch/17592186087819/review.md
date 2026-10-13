# Matrices for Route Planning: source and generated review

Basis 1356; raw capture in source.json. Source figure paths alone are localized. Observed scalar windows are catalogs with unresolved author intent, not inferred errors. Generated counts are independently read from arrow sidecars and displayed ordered tables.

## Original replay q-138940

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/cb/cbdf5c2470229ae3ba10ee18bccd2dc764407897397466b157474bf2b819f5d9.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$a$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$c$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 3, 2, 1, 5, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Original replay q-139685

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/ab/abbc0e5ce20a52263ba067d1563708f803e33def4f931a3d3badedd1c8ff4908.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$a$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$b$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$c$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 2, 1 ✓, 0, 5, 3

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $a=0.$

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from $B$ to $A,$ and so $b=0.$

- There is $1$ arrow starting at Station C and ending at Station B. So, there is only one route from $C$ to $B,$ and so $c=1.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 0+0+1 = 1.
$$

## Original replay q-139689

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/6c/6c52f315d079b82fb729c4ab47f210ec4bf2683d0dfe1adfe79c94db9fbc5f63.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$a$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$c$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 2 ✓, 1, 0, 4, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are no arrows starting at Station C and ending at Station A. So, there are no routes from $C$ to $A,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=1+1+0=2.
$$

## Original replay q-139719

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/0e/0ed581569bdc7c4f269f4cdf48d3ae20205627312641ff5b06daa2dca5a0e168.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$a$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$b$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$c$</td><td>$1$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 2, 1, 0, 4, 3 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station D. So, there are two routes from $A$ to $D,$ and so $a=2.$

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $b=1.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=2+1+0=3.
$$

## Original replay q-319346

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/f5/f5297b339026b8b2ec9666a37bcb59a73297bf8a691690999ca41f5313cb3c93.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>{{field-1}}</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>{{field-2}}</td><td>$0$</td><td>{{field-3}}</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 2 ✓

**field-2 (blank):** 1 ✓

**field-3 (blank):** 3 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are $2$ routes from A to B.

- There is $1$ arrow starting at Station B and ending at Station A. So, there is $1$ route from B to A.

- There are $3$ arrows starting at Station B and ending at Station C. So, there is $3$ route from B to C.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$3$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Original replay q-319412

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/e7/e7c2810c5ccfa768d356e19e69cf9a54d21fcf608ed4863bd3da0b672313403e.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>{{field-1}}</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>{{field-2}}</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>{{field-3}}</td><td>$2$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$1$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 2 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station C. So, there are $2$ routes from A to C.

- There are $2$ arrows starting at Station B and ending at Station A. So, there are $2$ routes from B to A.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from C to C.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$2$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$1$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Original replay q-319429

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/76/76cff940632cac02300b538a4ef063cfe3e8a699b2d406c998725a6c6fa1eee6.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>{{field-1}}</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>{{field-2}}</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>{{field-3}}</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 3 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are $3$ arrows starting at Station A and ending at Station C. So, there are $3$ routes from A to C.

- There are $2$ arrows starting at Station B and ending at Station B. So, there are $2$ routes from B to B.

- There is $1$ arrow starting at Station C and ending at Station B. So, there is $1$ route from C to B.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$3$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$2$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

## Raw observed prose q-319429 (direction error retained as evidence)

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/76/76cff940632cac02300b538a4ef063cfe3e8a699b2d406c998725a6c6fa1eee6.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>{{field-1}}</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>{{field-2}}</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>{{field-3}}</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 3 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are $3$ arrows starting at Station A and ending at Station C. So, there are $3$ routes from A to C.

- There are $2$ arrows starting at Station B and ending at Station C. So, there are $2$ routes from B to C.

- There is $1$ arrow starting at Station C and ending at Station B. So, there is $1$ route from C to B.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$3$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$2$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy sum_138940 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/0f7d2f1cd3c52b3a94cd81a649e9118e2853a7f782a685bf552d917bd93a23a6.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$a$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$c$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 5, 1, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Generated variant easy sum_138940 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/b017ac82a9353caea52bb54b4f4d0bd549665ac2bec68f31af790f285b38a022.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$a$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$c$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 4 ✓, 5, 3, 2, 1

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $a=2.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $c=1.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$2$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 2+1+1 = 4.
$$

## Generated variant easy sum_139685 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/4e8c65fa473bb4e4f34c455fcb64007172da3f9e4df184aa94ed52e6195f5666.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$a$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$b$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$c$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 5, 0 ✓, 2, 1, 3

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $a=0.$

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from $B$ to $A,$ and so $b=0.$

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from $C$ to $B,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 0+0+0 = 0.
$$

## Generated variant easy sum_139685 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/a811180d736b3df4bcf8c8d368b9fb5494eb714007a401591a556483c06ffd7f.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$a$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$b$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$c$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 3, 5, 2 ✓, 1, 0

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $a=0.$

- There are $2$ arrows starting at Station B and ending at Station A. So, there are two routes from $B$ to $A,$ and so $b=2.$

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from $C$ to $B,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$2$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 0+2+0 = 2.
$$

## Generated variant moderate sum_139689 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/d847d0ab6983ad7195429ebef54bb05e72fe23422b959138832ca3ac9c145561.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$a$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$c$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 4 ✓, 0, 2, 1, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station C and ending at Station A. So, there are two routes from $C$ to $A,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=1+1+2=4.
$$

## Generated variant moderate sum_139689 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/f5592396df1f4e84d0fa08446edcdb22987f51b584965fa989bf65b803aeeca8.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$a$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$c$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 3, 4, 2, 1, 0 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station B. So, there are no routes from $A$ to $B,$ and so $a=0.$

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $b=0.$

- There are no arrows starting at Station C and ending at Station A. So, there are no routes from $C$ to $A,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+0+0=0.
$$

## Generated variant easy sum_139719 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/fef7fa2fec8a10e56c98b234240ed64fc96fa96c91912db81737bfa14a1f21f1.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$2$</td><td>$0$</td><td>$a$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$b$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$c$</td><td>$1$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 4, 0, 2 ✓, 1, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station D. So, there is only one route from $A$ to $D,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $b=1.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$2$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=1+1+0=2.
$$

## Generated variant easy sum_139719 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/ecd6423ea03b71f42598948e87402a00074b67dceb17f3ec238dae2d3fe23415.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$a$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$b$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$c$</td><td>$2$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 3, 4, 2 ✓, 1, 0

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station D. So, there are no routes from $A$ to $D,$ and so $a=0.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $b=2.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+2+0=2.
$$

## Generated variant easy blanks_319346 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/a92d0c37e52a7cfb7ea7563841e498b59b6599020b8216e11e5c01c623b04f16.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>{{field-1}}</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>{{field-2}}</td><td>$0$</td><td>{{field-3}}</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 2 ✓

**field-2 (blank):** 1 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are $2$ routes from A to B.

- There is $1$ arrow starting at Station B and ending at Station A. So, there is $1$ route from B to A.

- There is $1$ arrow starting at Station B and ending at Station C. So, there is $1$ route from B to C.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319346 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/d683fe5a2614ae8d20e96353af0d4145a3ff51fe7e67e9d8e6295887dd0c44af.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>{{field-1}}</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>{{field-2}}</td><td>$0$</td><td>{{field-3}}</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 1 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 2 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is $1$ route from A to B.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

- There are $2$ arrows starting at Station B and ending at Station C. So, there are $2$ routes from B to C.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319412 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/e8a02bd2c112471fa20bdd80d38a7f58f52cab74085251693397cbcd2930cf11.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>{{field-1}}</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>{{field-2}}</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>{{field-3}}</td><td>$2$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$1$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 0 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

- There is $1$ arrow starting at Station C and ending at Station C. So, there is $1$ route from C to C.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$1$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319412 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/adb83039b37b5e5f3a278a21f5d7422722ee5e1d56a3eabbdcdc9c3c8873260d.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>{{field-1}}</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>{{field-2}}</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>{{field-3}}</td><td>$1$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$1$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 0 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from C to C.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$1$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319429 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/9960cc380ab39e6f81a31863b2187e77b16635197eb4aacd1a6b0639a82e3bc8.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>{{field-1}}</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>{{field-2}}</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>{{field-3}}</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 1 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station C. So, there is $1$ route from A to C.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from B to B.

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from C to B.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319429 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/d53622756a2cc362df818ed6cde029ea74990d6c30fb0d1f80cddc08855d23dd.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>{{field-1}}</td></tr>
      <tr><th scope="row">B</th><td>$2$</td><td>{{field-2}}</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>{{field-3}}</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 0 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from B to B.

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from C to B.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$2$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant hard sum_permuted_four 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/b07ccfd20a9ce506d81e9ccd50e4af331a1d310d2d947ae82ac4ad955acaeda0.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">D</th><th scope="col">C</th><th scope="col">B</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">D</th><td>$c$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$b$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">A</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$a$</td><td>$2$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 6, 2, 4 ✓, 3, 5

Let's examine our diagram.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $a=0.$

- There are $2$ arrows starting at Station B and ending at Station A. So, there are two routes from $B$ to $A,$ and so $b=2.$

- There are $2$ arrows starting at Station D and ending at Station A. So, there are two routes from $D$ to $A,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">D</th><th scope="col">C</th><th scope="col">B</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">D</th><td>$2$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$2$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">A</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td><td>$2$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+2+2=4.
$$

## Generated variant hard sum_permuted_four 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/513dbfb6898f810f9a92cd11cc58a9da3eaf1bb085815b2a9d4fd4e85c4fc27a.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">D</th><th scope="col">C</th><th scope="col">B</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$a$</td></tr>
      <tr><th scope="row">A</th><td>$1$</td><td>$c$</td><td>$b$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 4, 5, 3 ✓, 2, 1

Let's examine our diagram.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $a=0.$

- There is $1$ arrow starting at Station A and ending at Station C. So, there is only one route from $A$ to $C,$ and so $b=1.$

- There are $2$ arrows starting at Station A and ending at Station D. So, there are two routes from $A$ to $D,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">D</th><th scope="col">C</th><th scope="col">B</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">A</th><td>$1$</td><td>$2$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+1+2=3.
$$

## Optional authored omission bank easy 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/images/cb/cbdf5c2470229ae3ba10ee18bccd2dc764407897397466b157474bf2b819f5d9.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$a$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$c$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 1, 6, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Optional authored omission bank easy 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/5f412f96abefe3ddc07b5769723d86d2e3d29091812691c82d37b15f9aed9722.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$a$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$c$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 1, 8, 2, 3, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station B and ending at Station C. So, there are two routes from $B$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Optional authored omission bank moderate 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/286678f8cf07cfb7a28e332f97a4e7e16367a4f5dc6ad9bab08c5a4242aba916.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$a$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$c$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 1, 8, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station C and ending at Station A. So, there are two routes from $C$ to $A,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=1+1+2=4.
$$

## Optional authored omission bank moderate 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/d847d0ab6983ad7195429ebef54bb05e72fe23422b959138832ca3ac9c145561.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$a$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$b$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$c$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 1, 8, 2, 3, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station B. So, there is only one route from $A$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $b=1.$

- There are $2$ arrows starting at Station C and ending at Station A. So, there are two routes from $C$ to $A,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=1+1+2=4.
$$
