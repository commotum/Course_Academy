# Variable queried cells: moderate 3×3 examples

All nine cells are queried across these three examples. Each question still counts one loop and two other directed relations.

## Seed 0

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/a3a7ca325e30aafc5bb76848d7a0b00005d73051c890bb079677ba3f5bccd5fb.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$b$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$a$</td><td>$c$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Let's examine our diagram.

- There is $1$ arrow starting at Station B and ending at Station B. So, there is only one route from $B$ to $B,$ and so $a=1.$

- There are no arrows starting at Station A and ending at Station B. So, there are no routes from $A$ to $B,$ and so $b=0.$

- There are no arrows starting at Station B and ending at Station C. So, there are no routes from $B$ to $C,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$0$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$1$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">C</th><td>$2$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=1+0+0=1.
$$

## Seed 3

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/4e59f8020793245cd931d2b8497c7944bd0b8b4fe6b7009e590ede82047461cc.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$c$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$b$</td><td>$a$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Let's examine our diagram.

- There are $2$ arrows starting at Station C and ending at Station B. So, there are two routes from $C$ to $B,$ and so $a=2.$

- There are no arrows starting at Station C and ending at Station A. So, there are no routes from $C$ to $A,$ and so $b=0.$

- There are no arrows starting at Station A and ending at Station A. So, there are no routes from $A$ to $A,$ and so $c=0.$

As a result, our route matrix is the following:

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$2$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$0$</td><td>$1$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$0$</td><td>$2$</td><td>$0$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=2+0+0=2.
$$

## Seed 48

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186087819/plots/6ba3ef7af263a4c8dbfe82a59e534fe6a6aaa8984cead0869785ed22a5e7b281.png)

The diagram above shows train routes between three stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the three stations. Find the value of $a+b+c.$

<div class="route-matrix">
  <span class="matrix-to">To</span>
  <span class="matrix-from">From</span>
  <table aria-label="Route matrix: rows are From stations; columns are To stations">
    <thead>
      <tr><td class="matrix-corner"></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$c$</td></tr>
      <tr><th scope="row">B</th><td>$b$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$a$</td></tr>
    </tbody>
  </table>
</div>

Let's examine our diagram.

- There is $1$ arrow starting at Station C and ending at Station C. So, there is only one route from $C$ to $C,$ and so $a=1.$

- There are $2$ arrows starting at Station B and ending at Station A. So, there are two routes from $B$ to $A,$ and so $b=2.$

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
      <tr><th scope="row">A</th><td>$0$</td><td>$1$</td><td>$0$</td></tr>
      <tr><th scope="row">B</th><td>$2$</td><td>$0$</td><td>$1$</td></tr>
      <tr><th scope="row">C</th><td>$1$</td><td>$0$</td><td>$1$</td></tr>
    </tbody>
  </table>
</div>

Therefore, 

$$
a+b+c=1+2+0=3.
$$
