# Template extraction



## 1. Specific source inventory



### q-75798

Find the polynomial $P(x)$ given that

$x^{4} + x^{3} - x^{2} + x - 2 = (x + 2)(x - 1)P(x)$.

Original parameters: `{'r1': -2, 'r2': 1, 'a': 1, 'b': 0, 'c': 1}`; P={x}^{2}+1, discriminant -4. First divisor root -2, second divisor root 1; intermediate cubic {x}^{3}-{x}^{2}+x-1 and signed quadratic {x}^{2}+1.

Attributes present: `[':db/id', ':question/answer-fields', ':question/id', ':question/math-academy-id', ':question/problem']`.

### q-75803

Find the polynomial $P(x)$ given that

$-3x^{4} + 16x^{3} - 4x^{2} - 4x - 5 = - (x - 5)(x - 1)P(x)$.

Original parameters: `{'r1': 5, 'r2': 1, 'a': 3, 'b': 2, 'c': 1}`; P=3{x}^{2}+2x+1, discriminant -8. First divisor root 5, second divisor root 1; intermediate cubic -3{x}^{3}+{x}^{2}+x+1 and signed quadratic -3{x}^{2}-2x-1.

Attributes present: `[':db/id', ':question/answer-fields', ':question/id', ':question/math-academy-id', ':question/problem']`.

### q-76184

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x-5)(x+1)P(x).
$$

Original parameters: `{'r1': -1, 'r2': 5, 'a': 2, 'b': -2, 'c': 1}`; P=2{x}^{2}-2x+1, discriminant -4. First divisor root -1, second divisor root 5; intermediate cubic 2{x}^{3}-12{x}^{2}+11x-5 and signed quadratic 2{x}^{2}-2x+1.

Attributes present: `[':db/id', ':question/difficulty', ':question/id', ':question/math-academy-id', ':question/problem', ':question/worked-solution']`.

### q-112651

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)^{2}P(x).
$$

Original parameters: `{'r1': 5, 'r2': 5, 'a': 1, 'b': 0, 'c': 9}`; P={x}^{2}+9, discriminant -36. First divisor root 5, second divisor root 5; intermediate cubic {x}^{3}-5{x}^{2}+9x-45 and signed quadratic {x}^{2}+9.

Attributes present: `[':db/id', ':question/answer-fields', ':question/difficulty', ':question/id', ':question/math-academy-id', ':question/problem', ':question/worked-solution']`.

### q-18852

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)(x+1)P(x).
$$

Original parameters: `{'r1': 3, 'r2': -1, 'a': 1, 'b': 0, 'c': 1}`; P={x}^{2}+1, discriminant -4. First divisor root 3, second divisor root -1; intermediate cubic {x}^{3}+{x}^{2}+x+1 and signed quadratic {x}^{2}+1.

Attributes present: `[':db/id', ':question/answer-fields', ':question/difficulty', ':question/id', ':question/math-academy-id', ':question/problem', ':question/worked-solution']`.

### q-75800

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x+1)(x-2)P(x).
$$

Original parameters: `{'r1': 2, 'r2': -1, 'a': 2, 'b': -1, 'c': 1}`; P=2{x}^{2}-x+1, discriminant -7. First divisor root 2, second divisor root -1; intermediate cubic 2{x}^{3}+{x}^{2}+1 and signed quadratic 2{x}^{2}-x+1.

Attributes present: `[':db/id', ':question/answer-fields', ':question/difficulty', ':question/id', ':question/math-academy-id', ':question/problem', ':question/worked-solution']`.

### q-270972

Find the polynomial $P(x)$ given that $2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192=(x+4)(x-6)P(x).$

$P(x)=$
{{field-1}}

Original parameters: `{'r1': -4, 'r2': 6, 'a': 2, 'b': -3, 'c': 8}`; P=2{x}^{2}-3x+8, discriminant -55. First divisor root -4, second divisor root 6; intermediate cubic 2{x}^{3}-15{x}^{2}+26x-48 and signed quadratic 2{x}^{2}-3x+8.

Attributes present: `[':db/id', ':question/answer-fields', ':question/difficulty', ':question/id', ':question/math-academy-id', ':question/problem', ':question/worked-solution']`.

### q-328607

Find the polynomial $P(x)$ given that $-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60=-(x+3)(x-4)P(x).$

$P(x)=$
{{field-1}}

Original parameters: `{'r1': -3, 'r2': 4, 'a': 3, 'b': -1, 'c': 5}`; P=3{x}^{2}-x+5, discriminant -59. First divisor root -3, second divisor root 4; intermediate cubic -3{x}^{3}+13{x}^{2}-9x+20 and signed quadratic -3{x}^{2}+x-5.

Attributes present: `[':db/id', ':question/answer-fields', ':question/difficulty', ':question/id', ':question/math-academy-id', ':question/problem', ':question/worked-solution']`.



## 2. Shared pattern



Given an explicit quartic identity f(x)=s(x−r1)(x−r2)P(x), recover P. Use the supplied first linear factor for a complete synthetic division, show its quotient and factor equality, use the second factor for another complete synthetic division, show its quotient and full factorization, calculate the remaining quadratic discriminant, conclude irreducibility over the reals and identify P. Repeated roots retain multiplicity rather than inventing two distinct roots. The outside negative requires signed quotients and a separate extraction of −1. Blanks request only the polynomial fragment; radios retain five polynomial choices. q-18852 includes its extra f(x) equality; q-270972 includes its aligned row; q-76184 reverses the supplied final factor order.



## 3. Complete component and bank map



Historical bank formulas below preserve complete observed values and notation, including the squared answer. The coefficient-role recipes are explicit reproducible evidence generalizations, not recovered error intent. The source polynomial quotient is derived independently. Every full bank is preserved together, and a collision rejects the whole instance. Opaque observed profiles are never default learning banks.



### observed_q-75798



| Field | Original answer | Parameterized recipe | Mathematically correct? |

| --- | --- | --- | --- |

| selection | $x^{2} + 1$ | `(1)a*x^2+(b+(0)a)*x+(1)c; opaque coefficient-role preservation` | True |

| selection | $x^{2} - 2x + 1$ | `(1)a*x^2+(b+(-2)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | $x^{2} + x + 1$ | `(1)a*x^2+(b+(1)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | $x^{2} - x + 1$ | `(1)a*x^2+(b+(-1)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | $(x + 1)^{2}$ | `a*(x+c)^2 (opaque observed square shape)` | False |

### observed_q-75803



| Field | Original answer | Parameterized recipe | Mathematically correct? |

| --- | --- | --- | --- |

| selection | $3x^{2} - 1$ | `(1)a*x^2+(b+(-2/3)a)*x+(-1)c; opaque coefficient-role preservation` | False |

| selection | $3x^{2} - 3x + 1$ | `(1)a*x^2+(b+(-5/3)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | $3x^{2} + 2x + 1$ | `(1)a*x^2+(b+(0)a)*x+(1)c; opaque coefficient-role preservation` | True |

| selection | $3x^{2} + 1$ | `(1)a*x^2+(b+(-2/3)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | $3x^{2} - 4x + 1$ | `(1)a*x^2+(b+(-2)a)*x+(1)c; opaque coefficient-role preservation` | False |

### observed_q-76184



| Field | Original answer | Parameterized recipe | Mathematically correct? |

| --- | --- | --- | --- |

Source has no field or bank. Normal authored inference adds a single blank containing the independently derived quadratic fragment, with its matching field-1 placeholder.

### observed_q-112651



| Field | Original answer | Parameterized recipe | Mathematically correct? |

| --- | --- | --- | --- |

| selection | ${x}^{2}+3$ | `(1)a*x^2+(b+(0)a)*x+(1/3)c; opaque coefficient-role preservation` | False |

| selection | ${x}^{2}-3x+9$ | `(1)a*x^2+(b+(-3)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | ${x}^{2}+2$ | `(1)a*x^2+(b+(0)a)*x+(2/9)c; opaque coefficient-role preservation` | False |

| selection | ${x}^{2}+9$ | `(1)a*x^2+(b+(0)a)*x+(1)c; opaque coefficient-role preservation` | True |

| selection | ${x}^{2}-4x+6$ | `(1)a*x^2+(b+(-4)a)*x+(2/3)c; opaque coefficient-role preservation` | False |

### observed_q-18852



| Field | Original answer | Parameterized recipe | Mathematically correct? |

| --- | --- | --- | --- |

| selection | ${x}^{2}+x+1$ | `(1)a*x^2+(b+(1)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | ${x}^{2}-x+1$ | `(1)a*x^2+(b+(-1)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | ${x}^{2}+1$ | `(1)a*x^2+(b+(0)a)*x+(1)c; opaque coefficient-role preservation` | True |

| selection | ${x}^{2}-1$ | `(1)a*x^2+(b+(0)a)*x+(-1)c; opaque coefficient-role preservation` | False |

| selection | ${x}^{2}-2x+1$ | `(1)a*x^2+(b+(-2)a)*x+(1)c; opaque coefficient-role preservation` | False |

### observed_q-75800



| Field | Original answer | Parameterized recipe | Mathematically correct? |

| --- | --- | --- | --- |

| selection | $2{x}^{2}+3x+1$ | `(1)a*x^2+(b+(2)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | $2{x}^{2}-x+1$ | `(1)a*x^2+(b+(0)a)*x+(1)c; opaque coefficient-role preservation` | True |

| selection | $2{x}^{2}-2x+1$ | `(1)a*x^2+(b+(-1/2)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | $2{x}^{2}-6x+1$ | `(1)a*x^2+(b+(-5/2)a)*x+(1)c; opaque coefficient-role preservation` | False |

| selection | $2{x}^{2}-4x+1$ | `(1)a*x^2+(b+(-3/2)a)*x+(1)c; opaque coefficient-role preservation` | False |

### observed_q-270972



| Field | Original answer | Parameterized recipe | Mathematically correct? |

| --- | --- | --- | --- |

| field-1 | $2{x}^{2}-3x+8$ | `(1)a*x^2+(b+(0)a)*x+(1)c; opaque coefficient-role preservation` | True |

### observed_q-328607



| Field | Original answer | Parameterized recipe | Mathematically correct? |

| --- | --- | --- | --- |

| field-1 | $3{x}^{2}-x+5$ | `(1)a*x^2+(b+(0)a)*x+(1)c; opaque coefficient-role preservation` | True |



## 4. Reusable backbone and variable slots



| Slot | Domain/role | Dependent components |

| --- | --- | --- |

| r1 | First division root, nonzero integer −6..6 | First factor wording, first table root/products/sums, cubic quotient, equations |

| r2 | Second division root, nonzero integer −6..6 | Second factor wording, second table, quadratic quotient, final factorization |

| a | Positive quadratic leading coefficient 1..3 | Quartic coefficients, cubic arithmetic, signed quadratic, all options and discriminant |

| b | Quadratic x coefficient −4..4 | Full dividend/quotients, discriminant and all applicable bank coefficients |

| c | Positive quadratic constant 1..9 | Full dividend/quotients, discriminant, fragments and all options |

| s | Fixed by family: +1 moderate/easy, −1 hard | Outside sign, both signed quotients, hard sign extraction |



Easy fixes a=1,b=0,r1=r2 and varies r and c, preserving observed even quadratic/repeated-divisor workload. Moderate/hard require distinct roots. b²−4ac<0 is enforced on sampled and explicit parameters. Coefficients remain within source number forms (a up to3,c up to9, root magnitude up to6). Each level is an unordered same-workload family; none introduces complex arithmetic, unknown-root search, extra factors, integration or another skill. Parent canonical rational roots are not added merely to inflate hard variety. Factor order, seed, variable aliases and bank aliases do not increase capacity.



Normal solution wording is reconstructed from each family with shared sentences and all original operative stages. Source omissions remain absent in raw replay; normal q-75798 and q-75803 receive authored versions of the matching positive/signed two-division method. Normal q-76184 infers a supported blank. Source original answer feedback is absent and remains absent.



### Authored default complete radio bank



P; P−2r1*a*x; P−r2*a*x; P−2r1*(b−r2*a); a*x²+b*x−c. The wrong x coefficients model reversing the first multiplication contribution in the synthetic cubic x² stage and omitting the second multiplication contribution to the quadratic x stage. The constant error reverses the first multiplication contribution to the synthetic cubic x stage, propagated into the final quadratic constant. The last option reverses the final constant sign. Errors are isolated arithmetic operations; the displayed worked solution is the same fixed correct solution regardless of learner response. Five options are computed together and the entire instance is rejected if any coincide. Blanks have only the correct derived P, no invented distractors.



### Evidence, corrections and fidelity denominators



All 8 raw prompts, 6 present complete solutions, 7 present banks/27 choices, and 5 present correct designations are compared exactly. The two missing original refs do not count as matched designations; their values x²+1 and3x²+2x+1 follow independently from exact polynomial division. Archive /home/jake/Developer/MA/DATA/Lessons/104/Source/104.json confirms both historical five-choice widgets; its complete relevant rows are copied to widget-evidence.json. q-76184 has no source field; inferred supported blank is labeled authored.



q-112651 has a genuine second quotient denominator error: numerator x³−5x²+9x−45 divided by x−2 is not x²+9. Raw reproduces the x−2 anchor as the explicit erroneous divisor recipe x−(r2−3), evidence-only. Normal uses x−r2. Both raw tables correctly use root5 and remainder0; normal retains all source rows and sentences. Raw source full solution fidelity is separate from corrected mathematical correctness. q-18852 final prose p(x) becomes f(x) in normal output. Six historical nested Unicode underbrace markings become canonical TeX underbrace in normal output. These are explicitly reported separately from exact raw matching.



No plots: only two synthetic Markdown tables. The source wrapper retains its basis and lineage, and no database transaction or registration follows this work.
