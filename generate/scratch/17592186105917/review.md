# Scalar projection review

Original banks are evidence-only; the unrated original intentionally has no designation/solution. Changed source-bank variants retain opaque ratio profiles. Normal authored banks derive specific component-method errors. Hard examples are authored.

## Original replay — unrated
Template `q-126501`, profile `observed:q-126501`, seed 17.

Let $c = ⟨2, 1, 2⟩$ and $d = ⟨ - 1, 2, 2⟩$. Find $comp_{d}c + comp_{c}d$.

- A. $8$
- B. $\frac{1}{3}$
- C. $-6$
- D. $0$
- E. $\frac{8}{3}$

Correct: absent in raw source evidence

Worked solution:
Absent in raw source evidence.

---

## Original replay — easy
Template `q-18374`, profile `observed:q-18374`, seed 17.

Let $p=⟨\sqrt{2},1,-1⟩$ and $q=⟨\sqrt{8},-\sqrt{3},1⟩.$ Find the scalar projection of $p$ onto $q.$

- A. $2$
- B. $\frac{\sqrt{3}-1}{2\sqrt{3}}$
- C. $0$
- D. $2\sqrt{3}$
- E. $\frac{\sqrt{3}-1}{2}$

Correct: \frac{\sqrt{3}-1}{2}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{\sqrt{2}\cdot \sqrt{8}+1\cdot (-\sqrt{3})+(-1)\cdot 1}{\sqrt{(\sqrt{8})^{2}+(-\sqrt{3})^{2}+{1}^{2}}} \\  & =\frac{3-\sqrt{3}}{\sqrt{12}} \\  & =\frac{3-\sqrt{3}}{2\sqrt{3}} \\  & =\frac{\sqrt{3}-1}{2}.\end{aligned}
$$

---

## Original replay — easy
Template `q-101526`, profile `observed:q-101526`, seed 17.

Let $a=⟨3,-1,-1⟩$ and $b=⟨4,4,2⟩.$ Find the scalar projection of $a$ onto $b.$

- A. $2$
- B. $\frac{1}{\sqrt{6}}$
- C. $1$
- D. $\frac{1}{6}$
- E. $6$

Correct: 1

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{3\cdot 4+(-1)\cdot 4+(-1)\cdot 2}{\sqrt{{4}^{2}+{4}^{2}+{2}^{2}}} \\  & =\frac{6}{\sqrt{36}} \\  & =1.\end{aligned}
$$

---

## Original replay — easy
Template `q-101527`, profile `observed:q-101527`, seed 17.

Let $p=⟨3,2,1⟩$ and $q=⟨1,-1,1⟩.$ Find the scalar projection of $p$ onto $q.$

- A. $\frac{1}{4\sqrt{3}}$
- B. $\frac{1}{\sqrt{3}}$
- C. $\frac{3}{\sqrt{3}}$
- D. $\frac{1}{2\sqrt{3}}$
- E. $\frac{2}{\sqrt{3}}$

Correct: \frac{2}{\sqrt{3}}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{3\cdot 1+2\cdot (-1)+1\cdot 1}{\sqrt{{1}^{2}+(-1)^{2}+{1}^{2}}} \\  & =\frac{2}{\sqrt{3}}.\end{aligned}
$$

---

## Original replay — moderate
Template `q-101528`, profile `observed:q-101528`, seed 17.

Let $a=⟨2,-1,2⟩$ and $b=⟨6,2,-3⟩.$ Find ${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b.$

- A. $-\frac{4}{3}$
- B. $-\frac{2}{7}$
- C. $-\frac{16}{21}$
- D. $-\frac{4}{7}$
- E. $-1$

Correct: -\frac{16}{21}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{2\cdot 6+(-1)\cdot 2+2\cdot (-3)}{\sqrt{{6}^{2}+{2}^{2}+(-3)^{2}}} \\  & =\frac{4}{\sqrt{49}} \\  & =\frac{4}{7}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{4}{\sqrt{{2}^{2}+(-1)^{2}+{2}^{2}}} \\  & =\frac{4}{\sqrt{9}} \\  & =\frac{4}{3}.\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b & =\frac{4}{7}-\frac{4}{3} \\  & =4(\frac{1}{7}-\frac{1}{3}) \\  & =4(\frac{3}{21}-\frac{7}{21}) \\  & =-\frac{16}{21}.\end{aligned}
$$

---

## Original replay — moderate
Template `q-101529`, profile `observed:q-101529`, seed 17.

Let $p=⟨1,\sqrt{6},3⟩$ and $q=⟨-7,\sqrt{6},3⟩.$ Find ${\text{comp}}_{q}\,p+{\text{comp}}_{p}\,q.$

- A. $1$
- B. $3$
- C. $\frac{3}{2}$
- D. $\frac{1}{2}$
- E. $2$

Correct: 3

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{1\cdot (-7)+\sqrt{6}\cdot \sqrt{6}+3\cdot 3}{\sqrt{(-7)^{2}+{\sqrt{6}}^{2}+{3}^{2}}} \\  & =\frac{8}{\sqrt{64}} \\  & =1\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{p}\,q & =\frac{p\cdot q}{|\,p\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{p}_{x}^{2}+{p}_{y}^{2}+{p}_{z}^{2}}} \\  & =\frac{8}{\sqrt{{1}^{2}+{\sqrt{6}}^{2}+{3}^{2}}} \\  & =\frac{8}{\sqrt{16}} \\  & =2.\end{aligned}
$$

Therefore

$$
\begin{aligned}{\text{comp}}_{q}\,p+{\text{comp}}_{p}\,q & =1+2 \\  & =3.\end{aligned}
$$

---

## Original replay — easy
Template `q-126502`, profile `observed:q-126502`, seed 17.

Let $p=⟨6,-4,1⟩$ and $q=⟨2\sqrt{2},\sqrt{2},-2\sqrt{2}⟩.$ Find the scalar projection of $p$ onto $q.$

- A. $\frac{2\sqrt{2}}{3}$
- B. $2$
- C. $\frac{2}{3}$
- D. $\frac{\sqrt{2}}{3}$
- E. $2\sqrt{2}$

Correct: 2

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{6\cdot 2\sqrt{2}+(-4)\cdot \sqrt{2}+1\cdot (-2\sqrt{2})}{\sqrt{(2\sqrt{2})^{2}+(\sqrt{2})^{2}+(-2\sqrt{2})^{2}}} \\  & =\frac{6\sqrt{2}}{\sqrt{18}} \\  & =\frac{6\sqrt{2}}{3\sqrt{2}} \\  & =2.\end{aligned}
$$

---

## Original replay — easy
Template `q-18372`, profile `observed:q-18372`, seed 17.

Let $c=⟨-2,0,0⟩$ and $d=⟨4,-1,0⟩.$ Find the scalar projection of $c$ onto $d.$

- A. $-4$
- B. $0$
- C. $-\frac{8}{\sqrt{17}}$
- D. $\sqrt{17}$
- E. $-2$

Correct: -\frac{8}{\sqrt{17}}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{d}\,c & =\frac{c\cdot d}{|\,d\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}} \\  & =\frac{-2\cdot 4+0\cdot (-1)+0\cdot 0}{\sqrt{{4}^{2}+(-1)^{2}+{0}^{2}}} \\  & =-\frac{8}{\sqrt{17}}.\end{aligned}
$$

---

## Original replay — easy
Template `q-19139`, profile `observed:q-19139`, seed 17.

Let $a=⟨3,2,1⟩$ and $b=⟨3,4,1⟩.$ Find the scalar projection of $a$ onto $b.$

- A. $\frac{19}{\sqrt{14}}$
- B. $\frac{18}{\sqrt{14}}$
- C. $\frac{19}{\sqrt{26}}$
- D. $\frac{10}{\sqrt{26}}$
- E. $\frac{18}{\sqrt{26}}$

Correct: \frac{18}{\sqrt{26}}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{3\cdot 3+2\cdot 4+1\cdot 1}{\sqrt{{3}^{2}+{4}^{2}+{1}^{2}}} \\  & =\frac{18}{\sqrt{26}}.\end{aligned}
$$

---

## Original replay — easy
Template `q-19142`, profile `observed:q-19142`, seed 17.

Let $p=⟨4,1,4⟩$ and $q=⟨2,3,3⟩.$ Find the scalar projection of $p$ onto $q.$

- A. $\frac{23}{3\sqrt{11}}$
- B. $\frac{23}{\sqrt{33}}$
- C. $\frac{23}{2\sqrt{11}}$
- D. $\frac{23}{\sqrt{22}}$
- E. $\frac{22}{\sqrt{23}}$

Correct: \frac{23}{\sqrt{22}}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{4\cdot 2+1\cdot 3+4\cdot 3}{\sqrt{{2}^{2}+{3}^{2}+{3}^{2}}} \\  & =\frac{23}{\sqrt{22}}.\end{aligned}
$$

---

## Original replay — moderate
Template `q-19143`, profile `observed:q-19143`, seed 17.

Let $a=⟨2,1,-1⟩$ and $b=⟨1,4,2⟩.$ Find ${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b.$

- A. $0$
- B. $\frac{\sqrt{6}-\sqrt{21}}{\sqrt{126}}$
- C. $\frac{4\sqrt{6}-4\sqrt{21}}{\sqrt{126}}$
- D. $\frac{\sqrt{6}-4\sqrt{21}}{\sqrt{126}}$
- E. $\frac{4\sqrt{6}-\sqrt{21}}{\sqrt{126}}$

Correct: \frac{4\sqrt{6}-4\sqrt{21}}{\sqrt{126}}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{2\cdot 1+1\cdot 4+(-1)\cdot 2}{\sqrt{{1}^{2}+{4}^{2}+{2}^{2}}} \\  & =\frac{4}{\sqrt{21}}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{4}{\sqrt{{2}^{2}+{1}^{2}+(-1)^{2}}} \\  & =\frac{4}{\sqrt{6}}.\end{aligned}
$$

Therefore

$$
\begin{aligned}{\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b & =\frac{4}{\sqrt{21}}-\frac{4}{\sqrt{6}} \\  & =\frac{4\sqrt{6}-4\sqrt{21}}{\sqrt{126}}.\end{aligned}
$$

---

## Original replay — moderate
Template `q-19145`, profile `observed:q-19145`, seed 17.

Let $c=⟨4,3,0⟩$ and $d=⟨2,1,2⟩.$ Find ${\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d.$

- A. $\frac{55}{3}$
- B. $0$
- C. $\frac{33}{5}$
- D. $\frac{33}{15}$
- E. $\frac{22}{15}$

Correct: \frac{22}{15}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{d}\,c & =\frac{c\cdot d}{|\,d\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}} \\  & =\frac{4\cdot 2+3\cdot 1+0\cdot 2}{\sqrt{{2}^{2}+{1}^{2}+{2}^{2}}} \\  & =\frac{11}{\sqrt{9}} \\  & =\frac{11}{3}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{c}\,d & =\frac{c\cdot d}{|\,c\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{c}_{x}^{2}+{c}_{y}^{2}+{c}_{z}^{2}}} \\  & =\frac{11}{\sqrt{{4}^{2}+{3}^{2}+{0}^{2}}} \\  & =\frac{11}{\sqrt{25}} \\  & =\frac{11}{5}.\end{aligned}
$$

Therefore

$$
\begin{aligned}{\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d & =\frac{11}{3}-\frac{11}{5} \\  & =11(\frac{1}{3}-\frac{1}{5}) \\  & =11(\frac{5}{15}-\frac{3}{15}) \\  & =\frac{22}{15}.\end{aligned}
$$

---

## Original replay — moderate
Template `q-19146`, profile `observed:q-19146`, seed 17.

Let $a=⟨-1,2,\sqrt{11}⟩$ and $b=⟨4,3,\sqrt{11}⟩.$ Find ${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b.$

- A. $\frac{12}{13}$
- B. $-\frac{12}{13}$
- C. $\frac{13}{12}$
- D. $-\frac{13}{12}$
- E. $0$

Correct: -\frac{13}{12}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(-1)\cdot 4+2\cdot 3+\sqrt{11}\cdot \sqrt{11}}{\sqrt{{4}^{2}+{3}^{2}+(\sqrt{11})^{2}}} \\  & =\frac{13}{\sqrt{36}} \\  & =\frac{13}{6}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{13}{\sqrt{(-1)^{2}+{2}^{2}+(\sqrt{11})^{2}}} \\  & =\frac{13}{\sqrt{16}} \\  & =\frac{13}{4}.\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b & =\frac{13}{6}-\frac{13}{4} \\  & =13(\frac{1}{6}-\frac{1}{4}) \\  & =13(\frac{2}{12}-\frac{3}{12}) \\  & =-\frac{13}{12}.\end{aligned}
$$

---

## Original replay — moderate
Template `q-19147`, profile `observed:q-19147`, seed 17.

Let $p=⟨1,4,2\sqrt{2}⟩$ and $q=⟨1,1,\sqrt{2}⟩.$ Find ${\text{comp}}_{q}\,p+{\text{comp}}_{p}\,q.$

- A. $\frac{27}{10}$
- B. $\frac{63}{10}$
- C. $-\frac{29}{5}$
- D. $\frac{29}{5}$
- E. $\frac{32}{5}$

Correct: \frac{63}{10}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{1\cdot 1+4\cdot 1+2\sqrt{2}\cdot \sqrt{2}}{\sqrt{{1}^{2}+{1}^{2}+(\sqrt{2})^{2}}} \\  & =\frac{9}{\sqrt{4}} \\  & =\frac{9}{2}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{p}\,q & =\frac{p\cdot q}{|\,p\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{p}_{x}^{2}+{p}_{y}^{2}+{p}_{z}^{2}}} \\  & =\frac{9}{\sqrt{{1}^{2}+{4}^{2}+(2\sqrt{2})^{2}}} \\  & =\frac{9}{\sqrt{25}} \\  & =\frac{9}{5}.\end{aligned}
$$

Therefore

$$
\begin{aligned}{\text{comp}}_{q}\,p+{\text{comp}}_{p}\,q & =\frac{9}{2}+\frac{9}{5} \\  & =9(\frac{1}{2}+\frac{1}{5}) \\  & =9(\frac{5}{10}+\frac{2}{10}) \\  & =\frac{63}{10}.\end{aligned}
$$

---

## Original replay — easy
Template `q-275244`, profile `observed:q-275244`, seed 17.

Let $p=⟨2,1,-2⟩$ and $q=⟨3,2,0⟩.$ Find the exact value of the scalar projection of $p$ onto $q.$

${\text{comp}}_{q}\,p=$
{{field-1}}

- A. $\frac{8}{\sqrt{13}}$

Correct: \frac{8}{\sqrt{13}}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{2\cdot 3+1\cdot 2+(-2)\cdot 0}{\sqrt{{3}^{2}+{2}^{2}+{0}^{2}}} \\  & =\frac{8}{\sqrt{13}}.\end{aligned}
$$

---

## Original replay — easy
Template `q-275245`, profile `observed:q-275245`, seed 17.

Let $c=⟨1,2,-3⟩$ and $d=⟨2,1,2⟩.$ Find the scalar projection of $c$ onto $d.$

${\text{comp}}_{d}\,c=$
{{field-1}}

- A. $-\frac{2}{3}$

Correct: -\frac{2}{3}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{d}\,c & =\frac{c\cdot d}{|\,d\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}} \\  & =\frac{1\cdot 2+2\cdot 1+(-3)\cdot 2}{\sqrt{{2}^{2}+{1}^{2}+{2}^{2}}} \\  & =-\frac{2}{\sqrt{9}} \\  & =-\frac{2}{3}.\end{aligned}
$$

---

## Original replay — moderate
Template `q-275247`, profile `observed:q-275247`, seed 17.

Let $c=⟨4,-3,0⟩$ and $d=⟨2,1,-2⟩.$ Find, ${\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d.$

${\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d=$
{{field-1}}

- A. $\frac{2}{3}$

Correct: \frac{2}{3}

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{d}\,c & =\frac{c\cdot d}{|\,d\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}} \\  & =\frac{4\cdot 2+(-3)\cdot 1+0\cdot (-2)}{\sqrt{{2}^{2}+{1}^{2}+(-2)^{2}}} \\  & =\frac{5}{\sqrt{9}} \\  & =\frac{5}{3}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{c}\,d & =\frac{c\cdot d}{|\,c\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{c}_{x}^{2}+{c}_{y}^{2}+{c}_{z}^{2}}} \\  & =\frac{5}{\sqrt{{4}^{2}+(-3)^{2}+{0}^{2}}} \\  & =\frac{5}{\sqrt{25}} \\  & =\frac{5}{5} \\  & =1.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d & =\frac{5}{3}-1 \\  & =\frac{2}{3}.\end{aligned}
$$

---

## Original replay — easy
Template `q-318977`, profile `observed:q-318977`, seed 17.

Let $p=⟨4,-1,1⟩$ and $q=⟨1,2,2⟩.$ Find the scalar projection of $p$ onto $q.$

${\text{comp}}_{q}\,p=$
{{field-1}}

- A. $\frac{4}{3}$

Correct: \frac{4}{3}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{(4)(1)+(-1)(2)+(1)(2)}{\sqrt{{1}^{2}+{2}^{2}+{2}^{2}}} \\  & =\frac{4-2+2}{\sqrt{9}} \\  & =\frac{4}{3}.\end{aligned}
$$

---

## Original replay — easy
Template `q-318979`, profile `observed:q-318979`, seed 17.

Let $a=⟨3,-2,1⟩$ and $b=⟨2,1,-2⟩.$ Find the scalar projection of $a$ onto $b.$

${\text{comp}}_{b}\,a=$
{{field-1}}

- A. $\frac{2}{3}$

Correct: \frac{2}{3}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(3)(2)+(-2)(1)+(1)(-2)}{\sqrt{{2}^{2}+{1}^{2}+(-2)^{2}}} \\  & =\frac{6-2-2}{\sqrt{9}} \\  & =\frac{2}{3}.\end{aligned}
$$

---

## Original replay — easy
Template `q-318981`, profile `observed:q-318981`, seed 17.

Let $r=⟨-1,2,3⟩$ and $s=⟨2,0,0⟩.$ Find the scalar projection of $r$ onto $s.$

${\text{comp}}_{s}\,r=$
{{field-1}}

- A. $-1$

Correct: -1

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{s}\,r & =\frac{r\cdot s}{|\,s\,|} \\  & =\frac{{r}_{x}{s}_{x}+{r}_{y}{s}_{y}+{r}_{z}{s}_{z}}{\sqrt{{s}_{x}^{2}+{s}_{y}^{2}+{s}_{z}^{2}}} \\  & =\frac{(-1)(2)+(2)(0)+(3)(0)}{\sqrt{{2}^{2}+{0}^{2}+{0}^{2}}} \\  & =\frac{-2}{\sqrt{4}} \\  & =-1.\end{aligned}
$$

---

## Original replay — moderate
Template `q-318987`, profile `observed:q-318987`, seed 17.

Let $m=⟨6,8,0⟩$ and $n=⟨0,5,12⟩.$ Find ${\text{comp}}_{n}\,m-{\text{comp}}_{m}\,n.$

${\text{comp}}_{n}\,m-{\text{comp}}_{m}\,n=$
{{field-1}}

- A. $-\frac{12}{13}$

Correct: -\frac{12}{13}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{n}\,m & =\frac{m\cdot n}{|\,n\,|} \\  & =\frac{{m}_{x}{n}_{x}+{m}_{y}{n}_{y}+{m}_{z}{n}_{z}}{\sqrt{{n}_{x}^{2}+{n}_{y}^{2}+{n}_{z}^{2}}} \\  & =\frac{(6)(0)+(8)(5)+(0)(12)}{\sqrt{{0}^{2}+{5}^{2}+{12}^{2}}} \\  & =\frac{40}{\sqrt{169}} \\  & =\frac{40}{13}.\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{m}\,n & =\frac{m\cdot n}{|\,m\,|} \\  & =\frac{{m}_{x}{n}_{x}+{m}_{y}{n}_{y}+{m}_{z}{n}_{z}}{\sqrt{{m}_{x}^{2}+{m}_{y}^{2}+{m}_{z}^{2}}} \\  & =\frac{40}{\sqrt{{6}^{2}+{8}^{2}+{0}^{2}}} \\  & =\frac{40}{\sqrt{100}} \\  & =4.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{n}\,m-{\text{comp}}_{m}\,n & =\frac{40}{13}-4 \\  & =\frac{40-52}{13} \\  & =-\frac{12}{13}.\end{aligned}
$$

---

## Original replay — moderate
Template `q-318988`, profile `observed:q-318988`, seed 17.

Let $p=⟨9,12,0⟩$ and $q=⟨0,3,4⟩.$ Find ${\text{comp}}_{q}\,p-{\text{comp}}_{p}\,q.$

${\text{comp}}_{q}\,p-{\text{comp}}_{p}\,q=$
{{field-1}}

- A. $\frac{24}{5}$

Correct: \frac{24}{5}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{(9)(0)+(12)(3)+(0)(4)}{\sqrt{{0}^{2}+{3}^{2}+{4}^{2}}} \\  & =\frac{36}{\sqrt{25}} \\  & =\frac{36}{5}.\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{p}\,q & =\frac{p\cdot q}{|\,p\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{p}_{x}^{2}+{p}_{y}^{2}+{p}_{z}^{2}}} \\  & =\frac{36}{\sqrt{{9}^{2}+{12}^{2}+{0}^{2}}} \\  & =\frac{36}{\sqrt{225}} \\  & =\frac{12}{5}.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{q}\,p-{\text{comp}}_{p}\,q & =\frac{36}{5}-\frac{12}{5} \\  & =\frac{24}{5}.\end{aligned}
$$

---

## Original replay — easy
Template `q-318978`, profile `observed:q-318978`, seed 17.

Let $r=⟨-3,2,4⟩$ and $s=⟨1,2,-1⟩.$ Find the scalar projection of $r$ onto $s.$

${\text{comp}}_{s}\,r=$
{{field-1}}

- A. $-\frac{\sqrt{6}}{2}$

Correct: -\frac{\sqrt{6}}{2}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{s}\,r & =\frac{r\cdot s}{|\,s\,|} \\  & =\frac{{r}_{x}{s}_{x}+{r}_{y}{s}_{y}+{r}_{z}{s}_{z}}{\sqrt{{s}_{x}^{2}+{s}_{y}^{2}+{s}_{z}^{2}}} \\  & =\frac{(-3)(1)+(2)(2)+(4)(-1)}{\sqrt{{1}^{2}+{2}^{2}+(-1)^{2}}} \\  & =\frac{-3+4-4}{\sqrt{6}} \\  & =-\frac{3}{\sqrt{6}} \\  & =-\frac{\sqrt{6}}{2}.\end{aligned}
$$

---

## Original replay — easy
Template `q-318984`, profile `observed:q-318984`, seed 17.

Let $u=⟨3,1,-2⟩$ and $v=⟨1,1,1⟩.$ Find the scalar projection of $u$ onto $v.$

${\text{comp}}_{v}\,u=$
{{field-1}}

- A. $\frac{2}{\sqrt{3}}$

Correct: \frac{2}{\sqrt{3}}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{v}\,u & =\frac{u\cdot v}{|\,v\,|} \\  & =\frac{{u}_{x}{v}_{x}+{u}_{y}{v}_{y}+{u}_{z}{v}_{z}}{\sqrt{{v}_{x}^{2}+{v}_{y}^{2}+{v}_{z}^{2}}} \\  & =\frac{(3)(1)+(1)(1)+(-2)(1)}{\sqrt{{1}^{2}+{1}^{2}+{1}^{2}}} \\  & =\frac{3+1-2}{\sqrt{3}} \\  & =\frac{2}{\sqrt{3}}.\end{aligned}
$$

---

## Generated changed source-mask variant — unrated
Template `q-126501`, profile `observed:q-126501`, seed 21.

Let $c = ⟨-1, -2, 2⟩$ and $d = ⟨ - 1, 2, 2⟩$. Find $comp_{d}c + comp_{c}d$.

- A. $\left(\frac{1}{4}\right)\left(8\right)$
- B. $\left(\frac{1}{4}\right)\left(\frac{8}{3}\right)$
- C. $\left(\frac{1}{4}\right)\left(\frac{1}{3}\right)$
- D. $\left(\frac{1}{4}\right)\left(0\right)$
- E. $\left(\frac{1}{4}\right)\left(-6\right)$

Correct: absent in raw source evidence

Worked solution:
Absent in raw source evidence.

---

## Generated changed source-mask variant — easy
Template `q-18374`, profile `observed:q-18374`, seed 21.

Let $p=⟨\sqrt{1},1,\sqrt{2}⟩$ and $q=⟨\sqrt{8},-\sqrt{3},1⟩.$ Find the scalar projection of $p$ onto $q.$

- A. $\left(-\frac{\sqrt{3}}{2}-\frac{1}{2}+\frac{\sqrt{6}}{2}+\frac{3\sqrt{2}}{2}\right)\left(2\right)$
- B. $\left(-\frac{\sqrt{3}}{2}-\frac{1}{2}+\frac{\sqrt{6}}{2}+\frac{3\sqrt{2}}{2}\right)\left(\frac{\sqrt{3}-1}{2}\right)$
- C. $\left(-\frac{\sqrt{3}}{2}-\frac{1}{2}+\frac{\sqrt{6}}{2}+\frac{3\sqrt{2}}{2}\right)\left(\frac{\sqrt{3}-1}{2\sqrt{3}}\right)$
- D. $\left(-\frac{\sqrt{3}}{2}-\frac{1}{2}+\frac{\sqrt{6}}{2}+\frac{3\sqrt{2}}{2}\right)\left(2\sqrt{3}\right)$
- E. $\left(-\frac{\sqrt{3}}{2}-\frac{1}{2}+\frac{\sqrt{6}}{2}+\frac{3\sqrt{2}}{2}\right)\left(0\right)$

Correct: \left(-\frac{\sqrt{3}}{2}-\frac{1}{2}+\frac{\sqrt{6}}{2}+\frac{3\sqrt{2}}{2}\right)\left(\frac{\sqrt{3}-1}{2}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{\sqrt{1}\cdot \sqrt{8}+1\cdot (-\sqrt{3})+\sqrt{2}\cdot 1}{\sqrt{(\sqrt{8})^{2}+(-\sqrt{3})^{2}+{1}^{2}}} \\  & =\frac{-\sqrt{3}+3\sqrt{2}}{\sqrt{12}} \\  & =\frac{-\sqrt{3}+3\sqrt{2}}{2\sqrt{3}} \\  & =\frac{\sqrt{6}-1}{2}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-101526`, profile `observed:q-101526`, seed 21.

Let $a=⟨1,-1,-3⟩$ and $b=⟨4,4,2⟩.$ Find the scalar projection of $a$ onto $b.$

- A. $\left(-1\right)\left(2\right)$
- B. $\left(-1\right)\left(6\right)$
- C. $\left(-1\right)\left(\frac{1}{\sqrt{6}}\right)$
- D. $\left(-1\right)\left(\frac{1}{6}\right)$
- E. $\left(-1\right)\left(1\right)$

Correct: \left(-1\right)\left(1\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{1\cdot 4+(-1)\cdot 4+(-3)\cdot 2}{\sqrt{{4}^{2}+{4}^{2}+{2}^{2}}} \\  & =-\frac{6}{\sqrt{36}} \\  & =-1.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-101527`, profile `observed:q-101527`, seed 21.

Let $p=⟨-1,3,2⟩$ and $q=⟨1,-1,1⟩.$ Find the scalar projection of $p$ onto $q.$

- A. $\left(-1\right)\left(\frac{1}{4\sqrt{3}}\right)$
- B. $\left(-1\right)\left(\frac{2}{\sqrt{3}}\right)$
- C. $\left(-1\right)\left(\frac{1}{\sqrt{3}}\right)$
- D. $\left(-1\right)\left(\frac{1}{2\sqrt{3}}\right)$
- E. $\left(-1\right)\left(\frac{3}{\sqrt{3}}\right)$

Correct: \left(-1\right)\left(\frac{2}{\sqrt{3}}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{(-1)\cdot 1+3\cdot (-1)+2\cdot 1}{\sqrt{{1}^{2}+(-1)^{2}+{1}^{2}}} \\  & =-\frac{2}{\sqrt{3}}.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-101528`, profile `observed:q-101528`, seed 21.

Let $a=⟨-2,-1,2⟩$ and $b=⟨6,2,-3⟩.$ Find ${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b.$

- A. $\left(-5\right)\left(-\frac{4}{3}\right)$
- B. $\left(-5\right)\left(-1\right)$
- C. $\left(-5\right)\left(-\frac{2}{7}\right)$
- D. $\left(-5\right)\left(-\frac{4}{7}\right)$
- E. $\left(-5\right)\left(-\frac{16}{21}\right)$

Correct: \left(-5\right)\left(-\frac{16}{21}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(-2)\cdot 6+(-1)\cdot 2+2\cdot (-3)}{\sqrt{{6}^{2}+{2}^{2}+(-3)^{2}}} \\  & =-\frac{20}{\sqrt{49}} \\  & =-\frac{20}{7}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{-20}{\sqrt{(-2)^{2}+(-1)^{2}+{2}^{2}}} \\  & =-\frac{20}{\sqrt{9}} \\  & =-\frac{20}{3}.\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b & =-\frac{20}{7}-(-\frac{20}{3}) \\  & =(-20)(\frac{1}{7}-\frac{1}{3}) \\  & =(-20)(\frac{3}{21}-\frac{7}{21}) \\  & =\frac{80}{21}.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-101529`, profile `observed:q-101529`, seed 21.

Let $p=⟨-3,-\sqrt{1},-\sqrt{6}⟩$ and $q=⟨-7,\sqrt{6},3⟩.$ Find ${\text{comp}}_{q}\,p+{\text{comp}}_{p}\,q.$

- A. $\left(\frac{21}{8}-\frac{\sqrt{6}}{2}\right)\left(1\right)$
- B. $\left(\frac{21}{8}-\frac{\sqrt{6}}{2}\right)\left(2\right)$
- C. $\left(\frac{21}{8}-\frac{\sqrt{6}}{2}\right)\left(3\right)$
- D. $\left(\frac{21}{8}-\frac{\sqrt{6}}{2}\right)\left(\frac{1}{2}\right)$
- E. $\left(\frac{21}{8}-\frac{\sqrt{6}}{2}\right)\left(\frac{3}{2}\right)$

Correct: \left(\frac{21}{8}-\frac{\sqrt{6}}{2}\right)\left(3\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{(-3)\cdot (-7)+(-\sqrt{1})\cdot \sqrt{6}+(-\sqrt{6})\cdot 3}{\sqrt{(-7)^{2}+{\sqrt{6}}^{2}+{3}^{2}}} \\  & =\frac{21-4\sqrt{6}}{\sqrt{64}} \\  & =\frac{21-4\sqrt{6}}{8}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{p}\,q & =\frac{p\cdot q}{|\,p\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{p}_{x}^{2}+{p}_{y}^{2}+{p}_{z}^{2}}} \\  & =\frac{21-4\sqrt{6}}{\sqrt{(-3)^{2}+(-\sqrt{1})^{2}+(-\sqrt{6})^{2}}} \\  & =\frac{21-4\sqrt{6}}{\sqrt{16}} \\  & =\frac{21-4\sqrt{6}}{4}.\end{aligned}
$$

Therefore

$$
\begin{aligned}{\text{comp}}_{q}\,p+{\text{comp}}_{p}\,q & =\frac{21-4\sqrt{6}}{8}+\frac{21-4\sqrt{6}}{4} \\  & =\frac{63-12\sqrt{6}}{8}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-126502`, profile `observed:q-126502`, seed 21.

Let $p=⟨4,6,1⟩$ and $q=⟨2\sqrt{2},\sqrt{2},-2\sqrt{2}⟩.$ Find the scalar projection of $p$ onto $q.$

- A. $\left(2\right)\left(\frac{2\sqrt{2}}{3}\right)$
- B. $\left(2\right)\left(2\sqrt{2}\right)$
- C. $\left(2\right)\left(2\right)$
- D. $\left(2\right)\left(\frac{\sqrt{2}}{3}\right)$
- E. $\left(2\right)\left(\frac{2}{3}\right)$

Correct: \left(2\right)\left(2\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{4\cdot 2\sqrt{2}+6\cdot \sqrt{2}+1\cdot (-2\sqrt{2})}{\sqrt{(2\sqrt{2})^{2}+(\sqrt{2})^{2}+(-2\sqrt{2})^{2}}} \\  & =\frac{12\sqrt{2}}{\sqrt{18}} \\  & =\frac{12\sqrt{2}}{3\sqrt{2}} \\  & =4.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-18372`, profile `observed:q-18372`, seed 21.

Let $c=⟨0,2,0⟩$ and $d=⟨4,-1,0⟩.$ Find the scalar projection of $c$ onto $d.$

- A. $\left(\frac{1}{4}\right)\left(-4\right)$
- B. $\left(\frac{1}{4}\right)\left(-2\right)$
- C. $\left(\frac{1}{4}\right)\left(0\right)$
- D. $\left(\frac{1}{4}\right)\left(\sqrt{17}\right)$
- E. $\left(\frac{1}{4}\right)\left(-\frac{8}{\sqrt{17}}\right)$

Correct: \left(\frac{1}{4}\right)\left(-\frac{8}{\sqrt{17}}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{d}\,c & =\frac{c\cdot d}{|\,d\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}} \\  & =\frac{0\cdot 4+2\cdot (-1)+0\cdot 0}{\sqrt{{4}^{2}+(-1)^{2}+{0}^{2}}} \\  & =-\frac{2}{\sqrt{17}}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-19139`, profile `observed:q-19139`, seed 21.

Let $a=⟨-2,-1,3⟩$ and $b=⟨3,4,1⟩.$ Find the scalar projection of $a$ onto $b.$

- A. $\left(-\frac{7}{18}\right)\left(\frac{19}{\sqrt{14}}\right)$
- B. $\left(-\frac{7}{18}\right)\left(\frac{18}{\sqrt{26}}\right)$
- C. $\left(-\frac{7}{18}\right)\left(\frac{18}{\sqrt{14}}\right)$
- D. $\left(-\frac{7}{18}\right)\left(\frac{10}{\sqrt{26}}\right)$
- E. $\left(-\frac{7}{18}\right)\left(\frac{19}{\sqrt{26}}\right)$

Correct: \left(-\frac{7}{18}\right)\left(\frac{18}{\sqrt{26}}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(-2)\cdot 3+(-1)\cdot 4+3\cdot 1}{\sqrt{{3}^{2}+{4}^{2}+{1}^{2}}} \\  & =-\frac{7}{\sqrt{26}}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-19142`, profile `observed:q-19142`, seed 21.

Let $p=⟨1,-4,4⟩$ and $q=⟨2,3,3⟩.$ Find the scalar projection of $p$ onto $q.$

- A. $\left(\frac{2}{23}\right)\left(\frac{23}{3\sqrt{11}}\right)$
- B. $\left(\frac{2}{23}\right)\left(\frac{22}{\sqrt{23}}\right)$
- C. $\left(\frac{2}{23}\right)\left(\frac{23}{\sqrt{33}}\right)$
- D. $\left(\frac{2}{23}\right)\left(\frac{23}{\sqrt{22}}\right)$
- E. $\left(\frac{2}{23}\right)\left(\frac{23}{2\sqrt{11}}\right)$

Correct: \left(\frac{2}{23}\right)\left(\frac{23}{\sqrt{22}}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{1\cdot 2+(-4)\cdot 3+4\cdot 3}{\sqrt{{2}^{2}+{3}^{2}+{3}^{2}}} \\  & =\frac{2}{\sqrt{22}}.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-19143`, profile `observed:q-19143`, seed 21.

Let $a=⟨1,-2,-1⟩$ and $b=⟨1,4,2⟩.$ Find ${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b.$

- A. $\left(-\frac{9}{4}\right)\left(0\right)$
- B. $\left(-\frac{9}{4}\right)\left(\frac{4\sqrt{6}-\sqrt{21}}{\sqrt{126}}\right)$
- C. $\left(-\frac{9}{4}\right)\left(\frac{\sqrt{6}-\sqrt{21}}{\sqrt{126}}\right)$
- D. $\left(-\frac{9}{4}\right)\left(\frac{\sqrt{6}-4\sqrt{21}}{\sqrt{126}}\right)$
- E. $\left(-\frac{9}{4}\right)\left(\frac{4\sqrt{6}-4\sqrt{21}}{\sqrt{126}}\right)$

Correct: \left(-\frac{9}{4}\right)\left(\frac{4\sqrt{6}-4\sqrt{21}}{\sqrt{126}}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{1\cdot 1+(-2)\cdot 4+(-1)\cdot 2}{\sqrt{{1}^{2}+{4}^{2}+{2}^{2}}} \\  & =-\frac{9}{\sqrt{21}}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{-9}{\sqrt{{1}^{2}+(-2)^{2}+(-1)^{2}}} \\  & =-\frac{9}{\sqrt{6}}.\end{aligned}
$$

Therefore

$$
\begin{aligned}{\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b & =-\frac{9}{\sqrt{21}}-(-\frac{9}{\sqrt{6}}) \\  & =\frac{-9\sqrt{6}-(-9\sqrt{21})}{\sqrt{126}}.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-19145`, profile `observed:q-19145`, seed 21.

Let $c=⟨-3,0,-4⟩$ and $d=⟨2,1,2⟩.$ Find ${\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d.$

- A. $\left(-\frac{14}{11}\right)\left(\frac{55}{3}\right)$
- B. $\left(-\frac{14}{11}\right)\left(\frac{22}{15}\right)$
- C. $\left(-\frac{14}{11}\right)\left(0\right)$
- D. $\left(-\frac{14}{11}\right)\left(\frac{33}{15}\right)$
- E. $\left(-\frac{14}{11}\right)\left(\frac{33}{5}\right)$

Correct: \left(-\frac{14}{11}\right)\left(\frac{22}{15}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{d}\,c & =\frac{c\cdot d}{|\,d\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}} \\  & =\frac{(-3)\cdot 2+0\cdot 1+(-4)\cdot 2}{\sqrt{{2}^{2}+{1}^{2}+{2}^{2}}} \\  & =-\frac{14}{\sqrt{9}} \\  & =-\frac{14}{3}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{c}\,d & =\frac{c\cdot d}{|\,c\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{c}_{x}^{2}+{c}_{y}^{2}+{c}_{z}^{2}}} \\  & =\frac{-14}{\sqrt{(-3)^{2}+{0}^{2}+(-4)^{2}}} \\  & =-\frac{14}{\sqrt{25}} \\  & =-\frac{14}{5}.\end{aligned}
$$

Therefore

$$
\begin{aligned}{\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d & =-\frac{14}{3}-(-\frac{14}{5}) \\  & =(-14)(\frac{1}{3}-\frac{1}{5}) \\  & =(-14)(\frac{5}{15}-\frac{3}{15}) \\  & =-\frac{28}{15}.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-19146`, profile `observed:q-19146`, seed 21.

Let $a=⟨\sqrt{11},1,-\sqrt{4}⟩$ and $b=⟨4,3,\sqrt{11}⟩.$ Find ${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b.$

- A. $\left(\frac{3}{13}+\frac{2\sqrt{11}}{13}\right)\left(\frac{12}{13}\right)$
- B. $\left(\frac{3}{13}+\frac{2\sqrt{11}}{13}\right)\left(0\right)$
- C. $\left(\frac{3}{13}+\frac{2\sqrt{11}}{13}\right)\left(-\frac{12}{13}\right)$
- D. $\left(\frac{3}{13}+\frac{2\sqrt{11}}{13}\right)\left(-\frac{13}{12}\right)$
- E. $\left(\frac{3}{13}+\frac{2\sqrt{11}}{13}\right)\left(\frac{13}{12}\right)$

Correct: \left(\frac{3}{13}+\frac{2\sqrt{11}}{13}\right)\left(-\frac{13}{12}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{\sqrt{11}\cdot 4+1\cdot 3+(-\sqrt{4})\cdot \sqrt{11}}{\sqrt{{4}^{2}+{3}^{2}+(\sqrt{11})^{2}}} \\  & =\frac{3+2\sqrt{11}}{\sqrt{36}} \\  & =\frac{3+2\sqrt{11}}{6}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{3+2\sqrt{11}}{\sqrt{(\sqrt{11})^{2}+{1}^{2}+(-\sqrt{4})^{2}}} \\  & =\frac{3+2\sqrt{11}}{\sqrt{16}} \\  & =\frac{3+2\sqrt{11}}{4}.\end{aligned}
$$

Therefore, 

$$
\begin{aligned}{\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b & =\frac{3+2\sqrt{11}}{6}-\frac{3+2\sqrt{11}}{4} \\  & =(3+2\sqrt{11})(\frac{1}{6}-\frac{1}{4}) \\  & =(3+2\sqrt{11})(\frac{2}{12}-\frac{3}{12}) \\  & =-\frac{3+2\sqrt{11}}{12}.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-19147`, profile `observed:q-19147`, seed 21.

Let $p=⟨-2\sqrt{2},-1,4⟩$ and $q=⟨1,1,\sqrt{2}⟩.$ Find ${\text{comp}}_{q}\,p+{\text{comp}}_{p}\,q.$

- A. $\left(-\frac{1}{9}+\frac{2\sqrt{2}}{9}\right)\left(\frac{27}{10}\right)$
- B. $\left(-\frac{1}{9}+\frac{2\sqrt{2}}{9}\right)\left(\frac{32}{5}\right)$
- C. $\left(-\frac{1}{9}+\frac{2\sqrt{2}}{9}\right)\left(\frac{63}{10}\right)$
- D. $\left(-\frac{1}{9}+\frac{2\sqrt{2}}{9}\right)\left(\frac{29}{5}\right)$
- E. $\left(-\frac{1}{9}+\frac{2\sqrt{2}}{9}\right)\left(-\frac{29}{5}\right)$

Correct: \left(-\frac{1}{9}+\frac{2\sqrt{2}}{9}\right)\left(\frac{63}{10}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{(-2\sqrt{2})\cdot 1+(-1)\cdot 1+4\cdot \sqrt{2}}{\sqrt{{1}^{2}+{1}^{2}+(\sqrt{2})^{2}}} \\  & =\frac{-1+2\sqrt{2}}{\sqrt{4}} \\  & =\frac{-1+2\sqrt{2}}{2}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{p}\,q & =\frac{p\cdot q}{|\,p\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{p}_{x}^{2}+{p}_{y}^{2}+{p}_{z}^{2}}} \\  & =\frac{-1+2\sqrt{2}}{\sqrt{(-2\sqrt{2})^{2}+(-1)^{2}+{4}^{2}}} \\  & =\frac{-1+2\sqrt{2}}{\sqrt{25}} \\  & =\frac{-1+2\sqrt{2}}{5}.\end{aligned}
$$

Therefore

$$
\begin{aligned}{\text{comp}}_{q}\,p+{\text{comp}}_{p}\,q & =\frac{2\sqrt{2}-1}{2}+\frac{2\sqrt{2}-1}{5} \\  & =(-1+2\sqrt{2})(\frac{1}{2}+\frac{1}{5}) \\  & =(-1+2\sqrt{2})(\frac{5}{10}+\frac{2}{10}) \\  & =\frac{14\sqrt{2}-7}{10}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-275244`, profile `observed:q-275244`, seed 21.

Let $p=⟨-2,-1,2⟩$ and $q=⟨3,2,0⟩.$ Find the exact value of the scalar projection of $p$ onto $q.$

${\text{comp}}_{q}\,p=$
{{field-1}}

- A. $\left(-1\right)\left(\frac{8}{\sqrt{13}}\right)$

Correct: \left(-1\right)\left(\frac{8}{\sqrt{13}}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{(-2)\cdot 3+(-1)\cdot 2+2\cdot 0}{\sqrt{{3}^{2}+{2}^{2}+{0}^{2}}} \\  & =-\frac{8}{\sqrt{13}}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-275245`, profile `observed:q-275245`, seed 21.

Let $c=⟨1,3,-2⟩$ and $d=⟨2,1,2⟩.$ Find the scalar projection of $c$ onto $d.$

${\text{comp}}_{d}\,c=$
{{field-1}}

- A. $\left(-\frac{1}{2}\right)\left(-\frac{2}{3}\right)$

Correct: \left(-\frac{1}{2}\right)\left(-\frac{2}{3}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{d}\,c & =\frac{c\cdot d}{|\,d\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}} \\  & =\frac{1\cdot 2+3\cdot 1+(-2)\cdot 2}{\sqrt{{2}^{2}+{1}^{2}+{2}^{2}}} \\  & =\frac{1}{\sqrt{9}} \\  & =\frac{1}{3}.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-275247`, profile `observed:q-275247`, seed 21.

Let $c=⟨0,-3,4⟩$ and $d=⟨2,1,-2⟩.$ Find, ${\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d.$

${\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d=$
{{field-1}}

- A. $\left(-\frac{11}{5}\right)\left(\frac{2}{3}\right)$

Correct: \left(-\frac{11}{5}\right)\left(\frac{2}{3}\right)

Worked solution:
Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{d}\,c & =\frac{c\cdot d}{|\,d\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}} \\  & =\frac{0\cdot 2+(-3)\cdot 1+4\cdot (-2)}{\sqrt{{2}^{2}+{1}^{2}+(-2)^{2}}} \\  & =-\frac{11}{\sqrt{9}} \\  & =-\frac{11}{3}\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{c}\,d & =\frac{c\cdot d}{|\,c\,|} \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{\sqrt{{c}_{x}^{2}+{c}_{y}^{2}+{c}_{z}^{2}}} \\  & =\frac{-11}{\sqrt{{0}^{2}+(-3)^{2}+{4}^{2}}} \\  & =-\frac{11}{\sqrt{25}} \\  & =-\frac{11}{5} \\  & =-\frac{11}{5}.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{d}\,c-{\text{comp}}_{c}\,d & =-\frac{11}{3}-(-\frac{11}{5}) \\  & =-\frac{22}{15}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-318977`, profile `observed:q-318977`, seed 21.

Let $p=⟨-1,1,-4⟩$ and $q=⟨1,2,2⟩.$ Find the scalar projection of $p$ onto $q.$

${\text{comp}}_{q}\,p=$
{{field-1}}

- A. $\left(-\frac{7}{4}\right)\left(\frac{4}{3}\right)$

Correct: \left(-\frac{7}{4}\right)\left(\frac{4}{3}\right)

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{(-1)(1)+(1)(2)+(-4)(2)}{\sqrt{{1}^{2}+{2}^{2}+{2}^{2}}} \\  & =\frac{-1+2-8}{\sqrt{9}} \\  & =-\frac{7}{3}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-318979`, profile `observed:q-318979`, seed 21.

Let $a=⟨3,2,1⟩$ and $b=⟨2,1,-2⟩.$ Find the scalar projection of $a$ onto $b.$

${\text{comp}}_{b}\,a=$
{{field-1}}

- A. $\left(3\right)\left(\frac{2}{3}\right)$

Correct: \left(3\right)\left(\frac{2}{3}\right)

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(3)(2)+(2)(1)+(1)(-2)}{\sqrt{{2}^{2}+{1}^{2}+(-2)^{2}}} \\  & =\frac{6+2-2}{\sqrt{9}} \\  & =\frac{6}{3}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-318981`, profile `observed:q-318981`, seed 21.

Let $r=⟨2,-1,-3⟩$ and $s=⟨2,0,0⟩.$ Find the scalar projection of $r$ onto $s.$

${\text{comp}}_{s}\,r=$
{{field-1}}

- A. $\left(-2\right)\left(-1\right)$

Correct: \left(-2\right)\left(-1\right)

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{s}\,r & =\frac{r\cdot s}{|\,s\,|} \\  & =\frac{{r}_{x}{s}_{x}+{r}_{y}{s}_{y}+{r}_{z}{s}_{z}}{\sqrt{{s}_{x}^{2}+{s}_{y}^{2}+{s}_{z}^{2}}} \\  & =\frac{(2)(2)+(-1)(0)+(-3)(0)}{\sqrt{{2}^{2}+{0}^{2}+{0}^{2}}} \\  & =\frac{4}{\sqrt{4}} \\  & =2.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-318987`, profile `observed:q-318987`, seed 21.

Let $m=⟨0,-6,8⟩$ and $n=⟨0,5,12⟩.$ Find ${\text{comp}}_{n}\,m-{\text{comp}}_{m}\,n.$

${\text{comp}}_{n}\,m-{\text{comp}}_{m}\,n=$
{{field-1}}

- A. $\left(\frac{33}{20}\right)\left(-\frac{12}{13}\right)$

Correct: \left(\frac{33}{20}\right)\left(-\frac{12}{13}\right)

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{n}\,m & =\frac{m\cdot n}{|\,n\,|} \\  & =\frac{{m}_{x}{n}_{x}+{m}_{y}{n}_{y}+{m}_{z}{n}_{z}}{\sqrt{{n}_{x}^{2}+{n}_{y}^{2}+{n}_{z}^{2}}} \\  & =\frac{(0)(0)+(-6)(5)+(8)(12)}{\sqrt{{0}^{2}+{5}^{2}+{12}^{2}}} \\  & =\frac{66}{\sqrt{169}} \\  & =\frac{66}{13}.\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{m}\,n & =\frac{m\cdot n}{|\,m\,|} \\  & =\frac{{m}_{x}{n}_{x}+{m}_{y}{n}_{y}+{m}_{z}{n}_{z}}{\sqrt{{m}_{x}^{2}+{m}_{y}^{2}+{m}_{z}^{2}}} \\  & =\frac{66}{\sqrt{{0}^{2}+(-6)^{2}+{8}^{2}}} \\  & =\frac{66}{\sqrt{100}} \\  & =\frac{33}{5}.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{n}\,m-{\text{comp}}_{m}\,n & =\frac{66}{13}-\frac{33}{5} \\  & =\frac{66-\frac{429}{5}}{13} \\  & =-\frac{99}{65}.\end{aligned}
$$

---

## Generated changed source-mask variant — moderate
Template `q-318988`, profile `observed:q-318988`, seed 21.

Let $p=⟨-12,0,9⟩$ and $q=⟨0,3,4⟩.$ Find ${\text{comp}}_{q}\,p-{\text{comp}}_{p}\,q.$

${\text{comp}}_{q}\,p-{\text{comp}}_{p}\,q=$
{{field-1}}

- A. $\frac{24}{5}$

Correct: \frac{24}{5}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{q}\,p & =\frac{p\cdot q}{|\,q\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{(-12)(0)+(0)(3)+(9)(4)}{\sqrt{{0}^{2}+{3}^{2}+{4}^{2}}} \\  & =\frac{36}{\sqrt{25}} \\  & =\frac{36}{5}.\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{p}\,q & =\frac{p\cdot q}{|\,p\,|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{p}_{x}^{2}+{p}_{y}^{2}+{p}_{z}^{2}}} \\  & =\frac{36}{\sqrt{(-12)^{2}+{0}^{2}+{9}^{2}}} \\  & =\frac{36}{\sqrt{225}} \\  & =\frac{12}{5}.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{q}\,p-{\text{comp}}_{p}\,q & =\frac{36}{5}-\frac{12}{5} \\  & =\frac{24}{5}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-318978`, profile `observed:q-318978`, seed 21.

Let $r=⟨-4,-3,2⟩$ and $s=⟨1,2,-1⟩.$ Find the scalar projection of $r$ onto $s.$

${\text{comp}}_{s}\,r=$
{{field-1}}

- A. $\left(4\right)\left(-\frac{\sqrt{6}}{2}\right)$

Correct: \left(4\right)\left(-\frac{\sqrt{6}}{2}\right)

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{s}\,r & =\frac{r\cdot s}{|\,s\,|} \\  & =\frac{{r}_{x}{s}_{x}+{r}_{y}{s}_{y}+{r}_{z}{s}_{z}}{\sqrt{{s}_{x}^{2}+{s}_{y}^{2}+{s}_{z}^{2}}} \\  & =\frac{(-4)(1)+(-3)(2)+(2)(-1)}{\sqrt{{1}^{2}+{2}^{2}+(-1)^{2}}} \\  & =\frac{-4-6-2}{\sqrt{6}} \\  & =-\frac{12}{\sqrt{6}} \\  & =-2\sqrt{6}.\end{aligned}
$$

---

## Generated changed source-mask variant — easy
Template `q-318984`, profile `observed:q-318984`, seed 21.

Let $u=⟨2,-3,-1⟩$ and $v=⟨1,1,1⟩.$ Find the scalar projection of $u$ onto $v.$

${\text{comp}}_{v}\,u=$
{{field-1}}

- A. $\left(-1\right)\left(\frac{2}{\sqrt{3}}\right)$

Correct: \left(-1\right)\left(\frac{2}{\sqrt{3}}\right)

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{v}\,u & =\frac{u\cdot v}{|\,v\,|} \\  & =\frac{{u}_{x}{v}_{x}+{u}_{y}{v}_{y}+{u}_{z}{v}_{z}}{\sqrt{{v}_{x}^{2}+{v}_{y}^{2}+{v}_{z}^{2}}} \\  & =\frac{(2)(1)+(-3)(1)+(-1)(1)}{\sqrt{{1}^{2}+{1}^{2}+{1}^{2}}} \\  & =\frac{2-3-1}{\sqrt{3}} \\  & =-\frac{2}{\sqrt{3}}.\end{aligned}
$$

---

## Generated authored default — easy
Template `single_radical`, profile `single_method`, seed 0.

Let $a=⟨-\sqrt{2},\sqrt{6},2\sqrt{2}⟩$ and $b=⟨\sqrt{3},-\sqrt{3},-3⟩.$ Find the scalar projection of $a$ onto $b.$

${\text{comp}}_{b}\,a=$
{{field-1}}

- A. $-\frac{3\sqrt{30}}{5}-\frac{\sqrt{10}}{5}$

Correct: -\frac{3\sqrt{30}}{5}-\frac{\sqrt{10}}{5}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(-\sqrt{2})(\sqrt{3})+(\sqrt{6})(-\sqrt{3})+(2\sqrt{2})(-3)}{\sqrt{(\sqrt{3})^{2}+(-\sqrt{3})^{2}+(-3)^{2}}} \\  & =\frac{-\sqrt{6}-3\sqrt{2}-6\sqrt{2}}{\sqrt{15}} \\  & =\frac{-9\sqrt{2}-\sqrt{6}}{\sqrt{15}} \\  & =-\frac{3\sqrt{30}}{5}-\frac{\sqrt{10}}{5}.\end{aligned}
$$

---

## Generated authored default — easy
Template `single`, profile `single_method`, seed 1.

Let $a=⟨4,-2,-5⟩$ and $b=⟨1,-6,0⟩.$ Find the scalar projection of $a$ onto $b.$

- A. $\frac{16}{37}$
- B. $\frac{12\sqrt{37}}{37}$
- C. $-\frac{16\sqrt{37}}{37}$
- D. $\frac{16\sqrt{37}}{37}$
- E. $\frac{16\sqrt{5}}{15}$

Correct: \frac{16\sqrt{37}}{37}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(4)(1)+(-2)(-6)+(-5)(0)}{\sqrt{{1}^{2}+(-6)^{2}+{0}^{2}}} \\  & =\frac{4+12+0}{\sqrt{37}} \\  & =\frac{16}{\sqrt{37}} \\  & =\frac{16\sqrt{37}}{37}.\end{aligned}
$$

---

## Generated authored default — moderate
Template `pair_difference`, profile `pair_method`, seed 0.

Let $a=⟨3,4,0⟩$ and $b=⟨-5,0,-12⟩.$ Find ${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b.$

${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b=$
{{field-1}}

- A. $\frac{24}{13}$

Correct: \frac{24}{13}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(3)(-5)+(4)(0)+(0)(-12)}{\sqrt{(-5)^{2}+{0}^{2}+(-12)^{2}}} \\  & =\frac{-15+0+0}{\sqrt{169}} \\  & =\frac{-15}{\sqrt{169}} \\  & =-\frac{15}{13}.\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{b}_{x}{a}_{x}+{b}_{y}{a}_{y}+{b}_{z}{a}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{-15}{\sqrt{{3}^{2}+{4}^{2}+{0}^{2}}} \\  & =\frac{-15}{\sqrt{25}} \\  & =-3.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b & =-\frac{15}{13}-(-3) \\  & =\frac{24}{13}.\end{aligned}
$$

---

## Generated authored default — moderate
Template `pair_sum`, profile `pair_method`, seed 1.

Let $a=⟨1,3,-\sqrt{6}⟩$ and $b=⟨7,3,-\sqrt{6}⟩.$ Find ${\text{comp}}_{b}\,a+{\text{comp}}_{a}\,b.$

- A. $\frac{11}{4}$
- B. $\frac{33}{8}$
- C. $-\frac{33}{4}$
- D. $\frac{33}{4}$
- E. $-\frac{11}{4}$

Correct: \frac{33}{4}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(1)(7)+(3)(3)+(-\sqrt{6})(-\sqrt{6})}{\sqrt{{7}^{2}+{3}^{2}+(-\sqrt{6})^{2}}} \\  & =\frac{7+9+6}{\sqrt{64}} \\  & =\frac{22}{\sqrt{64}} \\  & =\frac{11}{4}.\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{b}_{x}{a}_{x}+{b}_{y}{a}_{y}+{b}_{z}{a}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{22}{\sqrt{{1}^{2}+{3}^{2}+(-\sqrt{6})^{2}}} \\  & =\frac{22}{\sqrt{16}} \\  & =\frac{11}{2}.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{b}\,a+{\text{comp}}_{a}\,b & =\frac{11}{4}+\frac{11}{2} \\  & =\frac{33}{4}.\end{aligned}
$$

---

## Generated authored default — hard
Template `pair_difference`, profile `pair_method`, seed 0.

Let $a=⟨4,-1,2⟩$ and $b=⟨-\sqrt{3},-\sqrt{3},1⟩.$ Find ${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b.$

${\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b=$
{{field-1}}

- A. $\frac{\sqrt{21}\left(2-3\sqrt{3}\right)-(\sqrt{7}\left(2-3\sqrt{3}\right))}{\sqrt{147}}$

Correct: \frac{\sqrt{21}\left(2-3\sqrt{3}\right)-(\sqrt{7}\left(2-3\sqrt{3}\right))}{\sqrt{147}}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(4)(-\sqrt{3})+(-1)(-\sqrt{3})+(2)(1)}{\sqrt{(-\sqrt{3})^{2}+(-\sqrt{3})^{2}+{1}^{2}}} \\  & =\frac{-4\sqrt{3}+\sqrt{3}+2}{\sqrt{7}} \\  & =\frac{2-3\sqrt{3}}{\sqrt{7}}.\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{b}_{x}{a}_{x}+{b}_{y}{a}_{y}+{b}_{z}{a}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{2-3\sqrt{3}}{\sqrt{{4}^{2}+(-1)^{2}+{2}^{2}}} \\  & =\frac{2-3\sqrt{3}}{\sqrt{21}}.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{b}\,a-{\text{comp}}_{a}\,b & =-\frac{-2+3\sqrt{3}}{\sqrt{7}}-(-\frac{-2+3\sqrt{3}}{\sqrt{21}}) \\  & =\frac{\sqrt{21}\left(2-3\sqrt{3}\right)-(\sqrt{7}\left(2-3\sqrt{3}\right))}{\sqrt{147}}.\end{aligned}
$$

---

## Generated authored default — hard
Template `pair_sum`, profile `pair_method`, seed 1.

Let $a=⟨2,\sqrt{6},\sqrt{5}⟩$ and $b=⟨-2,1,\sqrt{5}⟩.$ Find ${\text{comp}}_{b}\,a+{\text{comp}}_{a}\,b.$

- A. $\frac{1+\sqrt{6}}{\sqrt{10}}$
- B. $\frac{1+\sqrt{6}}{\sqrt{10}}+\frac{1+\sqrt{6}}{15}$
- C. $-(\frac{\sqrt{15}\left(1+\sqrt{6}\right)+\sqrt{10}\left(1+\sqrt{6}\right)}{\sqrt{150}})$
- D. $\frac{\sqrt{15}\left(1+\sqrt{6}\right)+\sqrt{10}\left(1+\sqrt{6}\right)}{\sqrt{150}}$
- E. $\frac{\sqrt{15}\left(1+\sqrt{6}\right)-\sqrt{10}\left(1+\sqrt{6}\right)}{\sqrt{150}}$

Correct: \frac{\sqrt{15}\left(1+\sqrt{6}\right)+\sqrt{10}\left(1+\sqrt{6}\right)}{\sqrt{150}}

Worked solution:
Using the scalar projection formula, we obtain

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{(2)(-2)+(\sqrt{6})(1)+(\sqrt{5})(\sqrt{5})}{\sqrt{(-2)^{2}+{1}^{2}+(\sqrt{5})^{2}}} \\  & =\frac{-4+\sqrt{6}+5}{\sqrt{10}} \\  & =\frac{1+\sqrt{6}}{\sqrt{10}}.\end{aligned}
$$

and

$$
\begin{aligned}{\text{comp}}_{a}\,b & =\frac{b\cdot a}{|\,a\,|} \\  & =\frac{{b}_{x}{a}_{x}+{b}_{y}{a}_{y}+{b}_{z}{a}_{z}}{\sqrt{{a}_{x}^{2}+{a}_{y}^{2}+{a}_{z}^{2}}} \\  & =\frac{1+\sqrt{6}}{\sqrt{{2}^{2}+(\sqrt{6})^{2}+(\sqrt{5})^{2}}} \\  & =\frac{1+\sqrt{6}}{\sqrt{15}}.\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\text{comp}}_{b}\,a+{\text{comp}}_{a}\,b & =\frac{1+\sqrt{6}}{\sqrt{10}}+\frac{1+\sqrt{6}}{\sqrt{15}} \\  & =\frac{\sqrt{15}\left(1+\sqrt{6}\right)+\sqrt{10}\left(1+\sqrt{6}\right)}{\sqrt{150}}.\end{aligned}
$$
