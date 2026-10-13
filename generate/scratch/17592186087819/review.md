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

## Same graph, original cells

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/a888a13fe85d39835045ab1ab8206e0b3c29735ccb30e853492c1b9f13d1052f.png)

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
      <tr><th scope="row">B</th><td>$1$</td><td>$b$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$c$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 2 ✓, 1, 0, 4, 3

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $a=2.$

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
      <tr><th scope="row">A</th><td>$1$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=2+0+0=2.
$$

## Same graph, moved cells including C->C

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/a888a13fe85d39835045ab1ab8206e0b3c29735ccb30e853492c1b9f13d1052f.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$b$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$c$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$a$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 2, 1, 0, 4, 3 ✓

Let's examine our diagram.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $a=0.$

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $b=2.$

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
      <tr><th scope="row">A</th><td>$1$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+2+1=3.
$$

## Generated variant easy sum_138940 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/44dfeece00c923d5344cdbf3bba891dd0458c040bf64b92a5010e6098f1610cd.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$0$</td><td>$c$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$a$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$b$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 5, 1, 3, 2 ✓, 4

Let's examine our diagram.

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $a=1.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $b=0.$

- There is $1$ arrow starting at Station A and ending at Station C. So, there is only one route from $A$ to $C,$ and so $c=1.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+0+1 = 2.
$$

## Generated variant easy sum_138940 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/687cc3a814dd0ae4aefe58d8739c466099ca4f965cff78b3b1c5b3eda11425bc.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$b$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$a$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$c$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 4, 5, 3 ✓, 2, 1

Let's examine our diagram.

- There is $1$ arrow starting at Station B and ending at Station A. So, there is only one route from $B$ to $A,$ and so $a=1.$

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $b=0.$

- There are $2$ arrows starting at Station C and ending at Station B. So, there are two routes from $C$ to $B,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+0+2 = 3.
$$

## Generated variant easy sum_139685 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/c2f463aee0b7ff2a4c3b33ab6c1bc17461d2459dfe4540c95d84684762936c22.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$c$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$a$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$b$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 5, 0, 2 ✓, 1, 3

Let's examine our diagram.

- There are no arrows starting at Station B and ending at Station C. So, there are no routes from $B$ to $C,$ and so $a=0.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $b=0.$

- There are $2$ arrows starting at Station A and ending at Station C. So, there are two routes from $A$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 0+0+2 = 2.
$$

## Generated variant easy sum_139685 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/4a7c1d76beaf7162182e26dea14ce7412615d03907aa648976e156a9887488ed.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$a$</td><td>$0$</td><td>$c$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$b$</td><td>$2$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 3 ✓, 5, 2, 1, 0

Let's examine our diagram.

- There is $1$ arrow starting at Station A and ending at Station A. So, there is only one route from $A$ to $A,$ and so $a=1.$

- There are $2$ arrows starting at Station C and ending at Station A. So, there are two routes from $C$ to $A,$ and so $b=2.$

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from $A$ to $C,$ and so $c=0.$

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
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$2$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+2+0 = 3.
$$

## Generated variant moderate sum_139689 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/75b2fd576dcb3d3d217ea1adb80849216a8c0f66586affb26016711b9765b8c5.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$0$</td><td>$c$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$a$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$b$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 4, 0, 2, 1 ✓, 3

Let's examine our diagram.

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $a=1.$

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $b=0.$

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from $A$ to $C,$ and so $c=0.$

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
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=1+0+0=1.
$$

## Generated variant moderate sum_139689 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/c22172897d2c22af5f51c27c8e7cc2f49d527e7f438b63f92ce8014fccf4f12c.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$a$</td><td>$1$</td><td>$c$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$b$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 3, 4, 2 ✓, 1, 0

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $a=0.$

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from $C$ to $B,$ and so $b=0.$

- There are $2$ arrows starting at Station A and ending at Station C. So, there are two routes from $A$ to $C,$ and so $c=2.$

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
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+0+2=2.
$$

## Generated variant easy sum_139719 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/056fddeef16f89b5f6054584630161bf65d8e935c5cae61877db370cccdebd64.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$2$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$c$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$2$</td><td>$0$</td><td>$a$</td><td>$b$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 4, 0, 2, 1, 3 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station D and ending at Station C. So, there are two routes from $D$ to $C,$ and so $a=2.$

- There are no arrows starting at Station D and ending at Station D. So, there are no routes from $D$ to $D,$ and so $b=0.$

- There is $1$ arrow starting at Station B and ending at Station A. So, there is only one route from $B$ to $A,$ and so $c=1.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$2$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$2$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=2+0+1=3.
$$

## Generated variant easy sum_139719 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/a31c2c8673da47a553bcf17a3241ca7a3b4da647160f7e19336262faf8fd2b0d.png)

The diagram above shows bus routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$a$</td><td>$1$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$c$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$1$</td><td>$b$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 3, 4, 2, 1, 0 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $a=0.$

- There are no arrows starting at Station D and ending at Station C. So, there are no routes from $D$ to $C,$ and so $b=0.$

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from $B$ to $A,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+0+0=0.
$$

## Generated variant easy blanks_319346 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/11043e9e2db1cf6f774ad4e920ef17e0cc6e59f7871ffbcddb7a072cfa0114dd.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$0$</td><td>{{field-3}}</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>{{field-1}}</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>{{field-2}}</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 2 ✓

**field-2 (blank):** 1 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station B and ending at Station C. So, there are $2$ routes from B to C.

- There is $1$ arrow starting at Station C and ending at Station B. So, there is $1$ route from C to B.

- There is $1$ arrow starting at Station A and ending at Station C. So, there is $1$ route from A to C.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319346 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/f884ab72785f93ec538369e2fb89cb3f4b689077977524147bf29cf6929ad9b9.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>{{field-2}}</td><td>{{field-1}}</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>{{field-3}}</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 0 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

- There are $2$ arrows starting at Station A and ending at Station B. So, there are $2$ routes from A to B.

- There is $1$ arrow starting at Station C and ending at Station A. So, there is $1$ route from C to A.

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
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319412 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/c29b04585e3f8dccd8c858ef21a82673ffb0997d574d3654896b7b46f1484ca9.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>{{field-3}}</td><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$2$</td><td>$0$</td><td>{{field-1}}</td><td>{{field-2}}</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 0 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are no arrows starting at Station D and ending at Station C. So, there are no routes from D to C.

- There are no arrows starting at Station D and ending at Station D. So, there are no routes from D to D.

- There are no arrows starting at Station B and ending at Station A. So, there are no routes from B to A.

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
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$2$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319412 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/e00d410ea7b9470a1308575363484cba734a1a7e44b79f3bd3b148578564fc81.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>{{field-1}}</td><td>$1$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>{{field-3}}</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$2$</td><td>$1$</td><td>{{field-2}}</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 0 ✓

**field-2 (blank):** 2 ✓

**field-3 (blank):** 1 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from A to A.

- There are $2$ arrows starting at Station D and ending at Station C. So, there are $2$ routes from D to C.

- There is $1$ arrow starting at Station B and ending at Station A. So, there is $1$ route from B to A.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$2$</td><td>$1$</td><td>$2$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319429 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/8902d10d7c7ea3929fe6c92282c8bd6c8e9ff7b3d556fd854f1f57af346655fa.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>{{field-3}}</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>{{field-1}}</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>{{field-2}}</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 2 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 0 ✓

Let's examine our diagram.

- There are $2$ arrows starting at Station B and ending at Station C. So, there are $2$ routes from B to C.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from C to C.

- There are no arrows starting at Station A and ending at Station C. So, there are no routes from A to C.

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
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant easy blanks_319429 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/1039662605302587c0b70f4830ed1271439b63989128946c4e77307a90730987.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Fill in the missing elements of the table.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>{{field-1}}</td><td>$1$</td><td>{{field-3}}</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>{{field-2}}</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**field-1 (blank):** 0 ✓

**field-2 (blank):** 0 ✓

**field-3 (blank):** 2 ✓

Let's examine our diagram.

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from A to A.

- There are no arrows starting at Station C and ending at Station B. So, there are no routes from C to B.

- There are $2$ arrows starting at Station A and ending at Station C. So, there are $2$ routes from A to C.

Therefore, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

## Generated variant hard sum_permuted_four 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/0c28093b2b2c2b7ba782a13e8419d1ed248821311b867587117d095dd57ae15c.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">C</th><th scope="col">D</th><th scope="col">B</th><th scope="col">A</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$1$</td><td>$0$</td><td>$0$</td><td>$b$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$c$</td><td>$a$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 7, 3, 5 ✓, 4, 6

Let's examine our diagram.

- There are $2$ arrows starting at Station B and ending at Station A. So, there are two routes from $B$ to $A,$ and so $a=2.$

- There are $2$ arrows starting at Station D and ending at Station A. So, there are two routes from $D$ to $A,$ and so $b=2.$

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $c=1.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">C</th><th scope="col">D</th><th scope="col">B</th><th scope="col">A</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">D</th><td>$1$</td><td>$0$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$1$</td><td>$2$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=2+2+1=5.
$$

## Generated variant hard sum_permuted_four 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/513dbfb6898f810f9a92cd11cc58a9da3eaf1bb085815b2a9d4fd4e85c4fc27a.png)

The diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">C</th><th scope="col">A</th><th scope="col">B</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$c$</td><td>$1$</td><td>$0$</td><td>$a$</td></tr>
      <tr><th scope="row">D</th><td>$1$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$b$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 4, 5, 3 ✓, 2, 1

Let's examine our diagram.

- There are $2$ arrows starting at Station A and ending at Station D. So, there are two routes from $A$ to $D,$ and so $a=2.$

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $b=0.$

- There is $1$ arrow starting at Station A and ending at Station C. So, there is only one route from $A$ to $C,$ and so $c=1.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">C</th><th scope="col">A</th><th scope="col">B</th><th scope="col">D</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">D</th><td>$1$</td><td>$0$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$0$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=2+0+1=3.
$$

## Optional authored omission bank easy 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/8a54e97873c326e4f5073c513ab0a341b84eae431a08479446b9bf6f150f7265.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$c$</td><td>$b$</td><td>$a$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 1, 6, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station C and ending at Station C. So, there is only one route from $C$ to $C,$ and so $a=1.$

- There is $1$ arrow starting at Station C and ending at Station B. So, there is only one route from $C$ to $B,$ and so $b=1.$

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
      <tr><th scope="row">A</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$1$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Optional authored omission bank easy 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/6334cd97060a86b9fa21fc1030c74e3b0cf38f6943997371614f83cb520f16e9.png)

The diagram above shows bus routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$b$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$a$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$c$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 1, 6, 2, 3, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station B and ending at Station A. So, there is only one route from $B$ to $A,$ and so $a=1.$

- There is $1$ arrow starting at Station A and ending at Station A. So, there is only one route from $A$ to $A,$ and so $b=1.$

- There are $2$ arrows starting at Station C and ending at Station B. So, there are two routes from $C$ to $B,$ and so $c=2.$

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
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$2$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Optional authored omission bank easy 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/0e9318e53709a238d3965f98014338086437ae49370ad2dbdc358ffe7ede7001.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$c$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$a$</td><td>$b$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 1, 8, 3, 2, 4 ✓

Let's examine our diagram.

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $a=1.$

- There is $1$ arrow starting at Station B and ending at Station C. So, there is only one route from $B$ to $C,$ and so $b=1.$

- There are $2$ arrows starting at Station A and ending at Station C. So, there are two routes from $A$ to $C,$ and so $c=2.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 1+1+2 = 4.
$$

## Optional authored omission bank easy 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/682f297a19e86bdc59c478bda8204641ec97e3c49ff36c88db319ea6cfb9f19e.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed lines between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a + b + c$.

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$b$</td></tr>
      <tr><th scope="row">B</th><td>$2$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$c$</td><td>$a$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 0, 8, 2, 1, 3 ✓

Let's examine our diagram.

- There are no arrows starting at Station C and ending at Station C. So, there are no routes from $C$ to $C,$ and so $a=0.$

- There are $2$ arrows starting at Station A and ending at Station C. So, there are two routes from $A$ to $C,$ and so $b=2.$

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
      <tr><th scope="row">A</th><td>$1$</td><td>$1$</td><td>$2$</td></tr>
      <tr><th scope="row">B</th><td>$2$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a + b + c = 0+2+1 = 3.
$$

## Optional authored omission bank moderate 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/a0bc4b805f1e2b137496a30b2d921391dd2820603c7accb69d0a8ce7ce52c2c0.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$a$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$c$</td><td>$b$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 0, 6, 2, 1, 3 ✓

Let's examine our diagram.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $a=0.$

- There is $1$ arrow starting at Station C and ending at Station B. So, there is only one route from $C$ to $B,$ and so $b=1.$

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
      <tr><th scope="row">A</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$1$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+1+2=3.
$$

## Optional authored omission bank moderate 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/5b95dff91bed0129c9798314d79b4065c46f00b239057062457e8e936c1b2868.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$b$</td><td>$c$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$a$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$2$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

**selection (radio):** 0, 8, 2, 1, 3 ✓

Let's examine our diagram.

- There are no arrows starting at Station B and ending at Station B. So, there are no routes from $B$ to $B,$ and so $a=0.$

- There are $2$ arrows starting at Station A and ending at Station B. So, there are two routes from $A$ to $B,$ and so $b=2.$

- There is $1$ arrow starting at Station A and ending at Station C. So, there is only one route from $A$ to $C,$ and so $c=1.$

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
      <tr><th scope="row">B</th><td>$0$</td><td>$0$</td><td>$2$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$2$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=0+2+1=3.
$$
