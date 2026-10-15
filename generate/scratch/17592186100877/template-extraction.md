# Four extraction stages

## 1. Specific observations

`source.json` preserves every source prompt, complete bank, field contract,
correct-reference presence, and whole solution. `source-cases.json` records only
MA original parameters. The per-source classification records differences in
wording and ordered stages. Source q-12912/q-12917 omit both key and solution;
raw evidence is ineligible public replay. Normal output completes these omissions
using an independently integrated key and the shared lesson substitution method.
These are authored completions, not recovered source designations/solutions.

All sources integrate c*x^(n-1)/(a*x^n+b), except the observed hard source whose
denominator is sqrt((x²+1)³). Source parameters, including negative shifts,
negative numerator, and negative original lower limits, are retained explicitly
in CONFIG. Easy and moderate primitive forms are logarithmic. The hard primitive
is -2r/sqrt(u), r=c/(an). All transformed endpoints are positive.

## 2. Shared pattern and instructional purpose

Substitute the denominator's polynomial inner T=a*x^n+b; match its derivative,
change both bounds in their original order, rewrite the integral in u, apply
one logarithm or power primitive, evaluate the upper and lower terms separately,
and collect the exact result. The original x-bounds are data, not free u-bounds.
No improper integration, partial fractions, polynomial division, inverse
trigonometric substitution, or extra integration stage is introduced.

## 3. Component and whole-bank mapping

Let l=T(lo), h=T(hi), r=c/(an), A=r*ln(h/l), and K=sqrt(h), J=sqrt(l).
The following lists preserve original bank order. They are exact mathematical
recipes, not claims about the source author's intent. Several sparse scalar
banks underdetermine intent, so these profiles remain selectable observed-pattern
variants in normal generation; authored default radios use a distinct whole profile. No mixed pool or
first-valid distractor selection is used.

| Source | Complete observed recipe list |
| --- | --- |
| q-12912 | ln(h), 0, A, 2ln(h), r |
| q-12917 | r ln(K), 2r ln(K), ln(K), (3/2)ln(K), 2ln(K) |
| q-113747 | r ln(a), ln(h), an ln(h), ln(a), A |
| q-13189 | ln(cuberoot(h))-a ln(l), -r ln(cuberoot(h))-r ln(l), r ln(cuberoot(h))-r ln(l), A, -ln(cuberoot(h))-r ln(l) |
| q-15877 | -A, -A/2, A, 3A/4, -3A/4 |
| q-19129 | ln(rh), r ln(r), h ln(r), A, (c+2)ln(r) |
| q-73432 | 2r ln(J/hi), r ln(J/hi), r ln(hi), r ln(K/J), 2r ln(K/J) |
| q-73434 | 2ln(h/b), 2r ln(h), ln(h/b), A, n ln(h) |
| q-336717, q-336729 | singleton A |
| q-336745 | singleton -2r/sqrt(h)+2r/sqrt(l) |

Source source-cases give the exact parameter mapping for every option. The
validator compares every original option one-to-one with the generated bank,
ignoring order, and compares the nine existing keys. Missing keys are reported
separately. Whole profiles are rejected on ANY collision or missing unique key.

Authored radio bank: A, -A, an*A, A/(an), r*(h ln(h)-l ln(l)). These are omitted sign,
wrong derivative scale, inverse scale, and incorrect u ln(u) primitive operations. All are
computed together before acceptance; no replacement option is picked. A zero
or one result is not directly filtered. A collision can reject an entire bank;
blank families retain natural zero results and one endpoints.

## 4. Reusable backbone and slots

The fixed per-family degree n preserves the supplied polynomial form. Easy n=1,
moderate n=2/3/4 according to source family, hard n=2. Integer a=1..5,
b=-9..12, |c|=1..12, original bounds -3<=lo<hi<=8 with width<=4 are bounded
conservative extensions of the observed integer forms. Normal samplers use
familiar small numerator coefficients. Positive inner is checked at all extrema
of T on the entire closed original interval, with T<=150 there. Consequently the
real log/radical branch is valid and no pole can be crossed. Hard c>0 preserves
its source signed endpoint workload. Negative easy numerator is retained.

Sources that explicitly expand logs preserve perfect powers: q-13189 upper
inner is a cube; q-15877 upper inner is a square; q-73432 both inner endpoints
are squares. q-12917's upper inner remains a square for its observed bank.
Every dependent differential operand, bound table cell, formal integral,
primitive bar, separate signed endpoint contribution, and bank value derives
from these slots. Explicit calls share exactly the same guard as sampling.

Workload is fixed within each level: one substitution, two bounds, one primitive,
two endpoint evaluations. There is no ordered progression within a level.
Extra source log-power simplification rows are retained in their original
families. Prompt wording, blank placeholder and all four shared instructional
sentences are preserved. TeX typography is normalized by the frozen formatter.

# Curriculum boundary

`lesson-route.json` is the actual first-step→next traversal, not Pull order:
Introduction → Calculating a Definite Integral of Function Using Substitution
(KP17592186100874) → this rational-function KP. The introduction explicitly
requires changing both limits without substituting x back into the final answer.
Topic predecessors are Integration Using Substitution and The Sum and Constant
Multiple Rules for Definite Integrals. Topic successors include Improper
Integrals, Partial Fractions, inverse-trig substitution, Further Algebraic
Substitution, exponential/log/trig substitution and polynomial division; those
are excluded. The hard radical is directly observed here and uses exactly its
source inverse3/2 power method. No missing E/M/H level is invented.

The q-15877 lower transformed endpoint is fixed at one because its observed log-power rows drop ln(1). Its original x-lower bound remains variable.

The captured prerequisite Integration Using Substitution was also traversed by
its actual first-step→next links (`prerequisite-routes.json`): Introduction →
power function times derivative → constant multiple of derivative → rational
substitution → rational natural logarithms → other fractional expressions.
Its rational canonical is x²/(x³+1), and its fractional canonical is
x²/sqrt(1-x³). These support the derivative matching and fractional-power step
already present in this KP. The other named predecessor has no lesson wrapper
in the basis2275 capture; that evidence limit is recorded rather than silently
using a different basis or inventing its route.

The observed q-12917 whole bank explicitly requires transformed lower endpoint one, rather than relying on accidental key uniqueness to enforce its omitted log(lower) term.
