# Template extraction

## Stage 1 — Specific source descriptions

### q-43277

What is the amplitude of the function $f(x) = 5\cos x$?

Parameters: `{"A": 5, "B": 1, "C": 0, "D": 0}`; function `cos`; operator spelling `\cos `. Mask `legacy_direct`.

Worked solution (complete captured prose and stage sequence):

Absent, preserved as absent.

Original response layout: five-option math radio, key `selection`.

### q-43278

What is the amplitude of the function $f(x) = \frac{3 - 2\cos x}{13}$?

Parameters: `{"B": 1, "C": 0, "D": 3, "N": -2, "Q": 13}`; function `cos`; operator spelling `\cos `. Mask `legacy_quotient`.

Worked solution (complete captured prose and stage sequence):

Absent, preserved as absent.

Original response layout: five-option math radio, key `selection`.

### q-117568

What is the amplitude of the function $f(x)=\frac{3}{2}\operatorname{cos}(2x-1)?$

Parameters: `{"A": "3/2", "B": 2, "C": -1, "D": 0}`; function `cos`; operator spelling `\operatorname{cos}`. Mask `direct`.

Worked solution (complete captured prose and stage sequence):

Given a function in the form $f(x)=A\operatorname{cos}(Bx+C)+D,$ the amplitude is $|A|.$

Since $A=\frac{3}{2},$ we have that the amplitude is $|A|=|\frac{3}{2}|=\frac{3}{2}.$

Original response layout: no answer-field attribute.

### q-117575

What is the amplitude of the function $f(x)=-5\operatorname{sin}(3x-\pi )-3?$

Parameters: `{"A": -5, "B": 3, "C": "-pi", "D": -3}`; function `sin`; operator spelling `\operatorname{sin}`. Mask `direct_pi`.

Worked solution (complete captured prose and stage sequence):

Given a function in the form $f(x)=A\operatorname{sin}(Bx+C)+D,$ the amplitude is $|A|.$

Since $A=-5,$ we have that the amplitude is $|A|=|-5|=5.$

Original response layout: no answer-field attribute.

### q-117569

What is the amplitude of the function $f(x)=\operatorname{sin}⁡(\frac{x}{3}+\frac{1}{4})?$

Parameters: `{"A": 1, "B": "1/3", "C": "1/4", "D": 0}`; function `sin`; operator spelling `\operatorname{sin}⁡`. Mask `unit_divx`.

Worked solution (complete captured prose and stage sequence):

Given a function in the form $f(x)=A\operatorname{sin}⁡(Bx+C)+D,$ the amplitude is $|A|.$ 

Since $A=1,$ we have that the amplitude is $|A|=|1|=1.$

Original response layout: five-option math radio, key `selection`.

### q-117570

What is the amplitude of the function $f(x)=4\operatorname{cos}⁡(2x+3)?$

Parameters: `{"A": 4, "B": 2, "C": 3, "D": 0}`; function `cos`; operator spelling `\operatorname{cos}⁡`. Mask `direct`.

Worked solution (complete captured prose and stage sequence):

Given a function in the form $f(x)=A\operatorname{cos}⁡(Bx+C)+D,$ the amplitude is $|A|.$

Since $A=4,$ we have that the amplitude is $|A|=|4|=4.$

Original response layout: five-option math radio, key `selection`.

### q-117574

What is the amplitude of the function $f(x)=-7\operatorname{cos}⁡(3x+1)?$

Parameters: `{"A": -7, "B": 3, "C": 1, "D": 0}`; function `cos`; operator spelling `\operatorname{cos}⁡`. Mask `direct`.

Worked solution (complete captured prose and stage sequence):

Given a function in the form $f(x)=A\operatorname{cos}⁡(Bx+C)+D,$ the amplitude is $|A|.$

Since $A=-7,$ we have that the amplitude is $|A|=|-7|=7.$

Original response layout: five-option math radio, key `selection`.

### q-117576

What is the amplitude of the function $f(x)=\frac{3-9\operatorname{sin}⁡x}{5}?$

Parameters: `{"B": 1, "C": 0, "D": 3, "N": -9, "Q": 5}`; function `sin`; operator spelling `\operatorname{sin}⁡`. Mask `quotient`.

Worked solution (complete captured prose and stage sequence):

First, notice that we can rewrite the function as follows:

$$
f(x)=\frac{3-9\operatorname{sin}⁡x}{5}=-\frac{9}{5}\cdot \operatorname{sin}⁡x+\frac{3}{5}
$$

Now, given a function in the form $f(x)=A\operatorname{sin}⁡(Bx+C)+D,$ the amplitude is $|A|.$

In our case, we have that $A=-\frac{9}{5}.$ Therefore, the amplitude is $|A|=|-\frac{9}{5}|=\frac{9}{5}.$

Original response layout: five-option math radio, key `selection`.

### q-53428

What is the amplitude of the function $f(x)=\operatorname{cos}⁡(\frac{1}{2}x+\frac{1}{3})?$

Parameters: `{"A": 1, "B": "1/2", "C": "1/3", "D": 0}`; function `cos`; operator spelling `\operatorname{cos}⁡`. Mask `unit`.

Worked solution (complete captured prose and stage sequence):

Given a function in the form $f(x)=A\operatorname{cos}⁡(Bx+C)+D,$ the amplitude is $|A|.$ 

Since $A=1,$ we have that the amplitude is $|A|=|1|=1.$

Original response layout: five-option math radio, key `selection`.

## Stage 2 — Shared mathematical pattern

Extract the coefficient of one sine or cosine term in A trig(Bx+C)+D, then return |A|. Argument scaling, phase and constant vertical shifts are distractor-bearing information, not additional requested outputs. The quotient family first splits the numerator across its denominator; its full rewrite must remain visible. All functions are nonconstant (B and sinusoidal coefficient nonzero), with real x and exact numerical coefficients.

## Stage 3 — Complete source component and bank map

Each recipe below is evaluated at the explicit source parameters by generate(..., profile="raw:<source>"). Option order is immaterial; all values and every present correct designation are compared one-to-one. Scalar recipes are numerical structure evidence. Labels below distinguish plausible method confusion from unresolved intention.

### raw:q-43277

| Source field | Original answer UUID | Exact value | Parameterized recipe | Interpretation | Designation |
|---|---|---|---|---|---|
| selection | 816a4e1d-d69b-52a5-a083-0588e4b07a6c | `\frac{1}{5}` | `1/abs(A)` | reciprocal vertical coefficient | absent |
| selection | bd8912f9-2470-59f1-81f4-c35ff720a74a | `10` | `2*abs(A)` | full vertical extent rather than half extent | absent |
| selection | c24339f5-5e2b-57ab-9584-16f3d693b470 | `\frac{5}{2}` | `abs(A)/2` | half coefficient; intention unresolved | absent |
| selection | 28837de8-80ec-5647-81ce-a458630192ca | `5` | `abs(A)` | amplitude | absent |
| selection | 6bb34917-5998-59ce-92ad-24caa605c5f3 | `25` | `A**2` | squared coefficient; intention unresolved | absent |

### raw:q-43278

| Source field | Original answer UUID | Exact value | Parameterized recipe | Interpretation | Designation |
|---|---|---|---|---|---|
| selection | 80a2470a-f69e-54ae-a935-d38c0ebd4cfa | `3` | `D` | numerator constant instead of coefficient | absent |
| selection | 85439c6b-3f28-5694-ab5c-887e29b56abc | `13` | `Q` | denominator instead of coefficient | absent |
| selection | 8fdfb56b-fca0-5ef1-a0c8-76b370700b78 | `\frac{2}{13}` | `abs(N/Q)` | amplitude | absent |
| selection | b6126d03-9b54-566e-8e16-f0eaedc60110 | `2` | `abs(N)` | omitted denominator | absent |
| selection | 0694b357-9426-5245-a8a9-9dc14aa6cfd8 | `-\frac{2}{13}` | `N/Q` | signed coefficient without absolute value | absent |

### raw:q-117568

No source field or bank; raw API output keeps absence. Normal field completion is authored.

### raw:q-117575

No source field or bank; raw API output keeps absence. Normal field completion is authored.

### raw:q-117569

| Source field | Original answer UUID | Exact value | Parameterized recipe | Interpretation | Designation |
|---|---|---|---|---|---|
| selection | 43205661-f460-56f1-adb1-c7d5bd58eadd | `3` | `1/B` | reciprocal horizontal coefficient | incorrect |
| selection | 72935ca7-a8c2-5ce6-aa26-184f0bd6b12c | `4` | `1/C` | reciprocal argument constant | incorrect |
| selection | ac96fb00-96df-5ad0-90c8-7963646933e2 | `\frac{1}{3}` | `B` | horizontal coefficient | incorrect |
| selection | dc1ac960-b896-5229-8bcd-ecd0c03b1345 | `1` | `abs(A)` | amplitude | correct |
| selection | efa437e0-6950-5962-9ef4-226f957d0c60 | `\frac{1}{4}` | `C` | argument constant | incorrect |

### raw:q-117570

| Source field | Original answer UUID | Exact value | Parameterized recipe | Interpretation | Designation |
|---|---|---|---|---|---|
| selection | 42d9acc7-d7bc-5ee0-a5fe-5e4dd49f1b24 | `\frac{1}{2}` | `1/B` | reciprocal horizontal coefficient | incorrect |
| selection | 62a72008-6a6e-556c-809d-015ca2b2740f | `2` | `B` | horizontal coefficient | incorrect |
| selection | d1881db5-b1bc-59b9-9956-32e11311533c | `8` | `abs(A)*B` | multiplied external/internal coefficients | incorrect |
| selection | f784db78-b2a6-5828-92f9-43c51bb6371d | `4` | `abs(A)` | amplitude | correct |
| selection | fdfe367d-16eb-5c43-87a8-b57680a82f9b | `\frac{1}{4}` | `1/abs(A)` | reciprocal external coefficient | incorrect |

### raw:q-117574

| Source field | Original answer UUID | Exact value | Parameterized recipe | Interpretation | Designation |
|---|---|---|---|---|---|
| selection | 089d4f87-485b-5461-9e38-0c474aed1222 | `\frac{1}{7}` | `1/abs(A)` | reciprocal external coefficient magnitude | incorrect |
| selection | 6c26512d-349b-5bc4-abc3-ee0cf9a396c3 | `3` | `B` | horizontal coefficient | incorrect |
| selection | a34d5453-3ac9-5200-8049-277e8f45c436 | `\frac{1}{3}` | `1/B` | reciprocal horizontal coefficient | incorrect |
| selection | d5f0adbe-2e89-5266-86ad-6f1c9bc6aa57 | `7` | `abs(A)` | amplitude | correct |
| selection | f815c935-e682-5043-be95-7be9b3b3c52a | `1` | `C` | argument constant | incorrect |

### raw:q-117576

| Source field | Original answer UUID | Exact value | Parameterized recipe | Interpretation | Designation |
|---|---|---|---|---|---|
| selection | 0aadff32-d8e0-5eea-8f1f-2f63a134c39f | `\frac{1}{5}` | `1/Q` | unit numerator divided by Q | incorrect |
| selection | 3acd747a-676c-53ac-a0b1-66a6584544d0 | `\frac{3}{5}` | `D/Q` | vertical constant divided by Q | incorrect |
| selection | 535dc4a7-779d-5aa4-84ff-894b2006269b | `\frac{9}{5}` | `abs(N/Q)` | amplitude | correct |
| selection | dfcaf382-661a-5eed-a5ae-ca4d55214483 | `3` | `D` | omitted division of vertical constant | incorrect |
| selection | e0d7f858-fa72-532e-b037-12bd5a63a44f | `9` | `abs(N)` | omitted division of sinusoidal coefficient | incorrect |

### raw:q-53428

| Source field | Original answer UUID | Exact value | Parameterized recipe | Interpretation | Designation |
|---|---|---|---|---|---|
| selection | 3e616922-3cb9-5d0d-adb4-d5f2e9937e8c | `2` | `1/B` | reciprocal horizontal coefficient | incorrect |
| selection | 49dad8f8-1906-5970-a75a-02b096c82478 | `\frac{1}{2}` | `B` | horizontal coefficient | incorrect |
| selection | 516a2115-a7cd-5bc8-a211-941eb2a6c091 | `6` | `1/(B*C)` | reciprocal product of argument parameters; intention unresolved | incorrect |
| selection | 806611f0-40df-5c8d-9ad4-4c05dfff9ea6 | `\frac{1}{3}` | `C` | argument constant | incorrect |
| selection | becedc42-47cd-5039-8a91-00d39f0721ef | `1` | `abs(A)` | amplitude | correct |

## Stage 4 — Reusable masks, domains and extensions

The script uses complete coefficient, argument, numerator, denominator and conclusion components. It does not find/replace single digits across prose or return a literal source question payload. Raw prompt styles place the question mark inside/outside math exactly as observed; worked prose and optional rewrite display are also retained. Scalar A and its absolute value are separately rendered in the final prose chain. All generated choice IDs are field-owned UUIDs; field UUIDs derive from stable content identity. Raw local representations normalize enum objects into enum strings and correct entities into lookup refs; database IDs are not part of local question records.

Normal authored notation uses \sin/\cos and preserves the same explanation sentences. This is explicitly authored notation, not a claim of exact source formatting. Missing fields, missing source labels and missing correct refs are not repaired inside raw evidence. Raw masks reject parameters their printed structure cannot show, e.g. a bare-x mask requires B=1,C=0.

| Normal family | Level and workload | Parameters and complete bank |
|---|---|---|
| positive | easy: identify positive external coefficient | A reduced positive rational, numerator 1..12, denominator 1..6; A=1 would collide in this bank and belongs to unit instead. B integer 2..6, D=0. [abs(A),1/abs(A),B,1/B,abs(A)B] |
| unit | easy: recognize implicit coefficient 1 | A=1,D=0; B=1/b,C=1/c, b,c integer 2..9, b≠c. [1,B,1/B,abs(C),1/abs(C)] |
| negative | moderate: identify negative coefficient then take magnitude | A negative reduced rational, absolute numerator 1..13, denominator 1..6; B integer 2..6,D integer -6..6. [abs(A),A,B,1/B,abs(C)] |
| quotient | moderate: one division, then magnitude | N negative integer -13..-2, Q integer 3..13, gcd(abs(N),Q)=1, N/Q noninteger; D integer 1..9; B=1,C=0. Either complete bank [abs(N/Q),abs(N),abs(D/Q),abs(D),1/Q] or [abs(N/Q),abs(N),D,Q,N/Q]. |
| factored | hard: two coefficient operations, then magnitude | P integer ±2..±4; N integer ±2..±13; Q 3..13; gcd(abs(PN),Q)=1 and gcd(abs(N),Q)=1; abs(PN)≤36; abs(N)≠abs(P) for the complete bank; D 1..9,E nonzero integer -6..6; B integer 1..4,C nonzero. [abs(PN/Q),abs(N/Q),abs(PN),abs(PD/Q),abs(P/Q)] |

Except unit's explicitly bounded reciprocals, C is a reduced rational with |numerator|≤6 and denominator≤6, or a rational multiple of pi with |numerator|≤3 and denominator≤6; |C|≤3pi. These incidental arguments do not require trigonometric evaluation. Raw evidence profiles may use broader exact parameters but remain ineligible.

All normal banks are selected before sampling parameters; the entire instance is rejected on any duplicate, equivalent, missing or invalid option. There is no first-valid option replacement. Recipes derive actual parameter confusion or an omitted multiplication/division/absolute-value step. In particular, the hard bank forgets outer P, forgets Q, selects the numerator constant instead of its sinusoidal coefficient, or ignores N. No learner-facing diagnosis has been invented.

The authored hard scope follows the source quotient rewrite plus the prerequisite's vertical scale: P(D+N trig(Bx+C))/Q+E. Every hard instance exposes two nonunit coefficient operations (multiply P and divide Q), with primitive reduced inputs preventing collapse to moderate's one division or easy's directly supplied coefficient. It adds no graph reading, trig identity, period, range, midline or extrema task. This is an authored difficulty claim, not an observed hard label. Signed P/N, sine/cosine, familiar horizontal shifts and constant offsets are unordered same-level variations. Each hard worked solution has original expression, explicitly unevaluated product/quotient row, collected sinusoidal form, then source-style |A| conclusion.

Mathematical task fingerprints retain only assessed coefficient extraction demand: implicit unit; direct signed reduced A; primitive N/Q; or the hard P,N,Q operation tree. Trig alias, B,C,D,E, choice order and profile are incidental and excluded. Presentation identity includes actual difficulty, prompt, fixed complete solution, complete sorted displayed bank and presence state. Thus changing a distractor-bearing offset changes presentation identity but does not inflate substantive task counts.

Finite eligible mathematical-task domain counts are established by exhaustive candidate signature enumeration with a valid complete bank witness for each signature (no offset/bank/letter multiplicity):

| Level | Eligible substantive tasks | Sampled tasks in validation |
|---|---:|---:|
| easy | 46 | 37 |
| moderate | 136 | 87 |
| hard | 536 | 151 |

All samplers and explicit calls share guards. The validator tests displayed prompt, every rewrite row and the concluding coefficient/absolute-value chain, whole banks, exact source strings/presence, seed-stable identities, numeric aliases, substantive-domain witnesses, and native grading.
