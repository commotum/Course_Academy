# Template extraction

## 1. Specific originals

q-12444 asks “Using the method of substitution, find the solution of” followed
by a semicolon-separated two-equation system. Its first equation has coefficients
(-3,1), its second (5,4); constants are -9,32. Isolating q gives q=3p-9;
substitution gives 5p+4(3p-9)=32, 17p=68, p=4, q=3. Five options are full named
p,q pairs. There is no captured solution, correct ref or rating.

q-12457 uses the same instructional sentence with a blank line before the system,
coefficients (-7,2),(-6,6), constants18,0 and full named a,b pairs. The second
row gives b=a, hence -5a=18 and **a=b=-18/5**. None of its five choices is correct:
every option instead has b=-a. The authoritative MA lesson 487 capture confirms
the exact equations and the exact five options. Neither changing the second
coefficient sign nor guessing an original correct choice is supported. The
repaired profile replaces the first displayed-bank value (-4,4) with the derived
correct pair; all remaining raw options are retained. That slot choice is an
authored minimal bank repair, not a recovered author designation.

q-18483 asks for p-q. Its first equation is already single-variable but still
requires dividing by5: q=-11. Substitute into 2p+3q+3=0; p=15, p-q=26. All five
options are scalar integer math strings; four wrong values are4,-4,-11,15.
Again there is no captured solution, correct ref or rating.

Canonical e-13010 prints 2u+9v-6=0 and 2u+6v-8=0. Its full prose numbers the
equations, isolates u using equation(2) with five rows, solves v in equation(1)
with six rows (original, substituted, distributed, collected, isolated, solved),
then finds u in equation(1) with six rows (original, substituted, evaluated,
collected, isolated, solved). The final named values and ordered pair are
u=6,v=-2/3,(6,-2/3). The generator preserves every shared sentence and row,
including the back-substitution into the original first equation. Whitespace
normalization and escape of the literal brace are the only canonical replay
presentation differences. Practice solutions are explicitly authored from this
canonical stage/prose sequence; their originals contain no solutions to match.

## 2. Shared mathematical pattern

Two integer-coefficient linear equations with a unique ordered solution are
combined by isolating a variable in one row and substituting its full affine
expression into the other. Distribution, signed collection, one-variable
division and back-substitution establish both values. The response is either a
full named pair or the source-supported scalar difference. Decimal/fractional
input coefficients, nonlinear equations, modeling and graph reading are outside
this KP. Fractional output is supported by the canonical example.

## 3. Components and complete bank accounting

`source-choice-map.json` records all15 original choice UUIDs, field UUIDs, raw
values, parameters, profile recipes and generated equivalent values. Source
banks are explicit profiles, never mixed or trimmed. Numerical reproduction of
an observed pair does not identify an author error algorithm.

With correct pair (X,Y), q12444's complete ordered bank is
(X,Y-1),(X,-Y/3),(X,Y),(Y,X),(-X,Y). The first two shapes are explicitly empirical
and underdetermined; swap/reverse-x are straightforward transformations but no
original intention is claimed. They reproduce every source value at(4,3), and
are exposed only through the explicit profile.

For q12457 let z=C/(|A|+B), which at source is18/9=2. Its complete empirical
bank is(-2z,2z),(3z/2,-3z/2),(2z,-2z),(z,-z),(-z,z). This summarizes the observed
opposite-sign multiples using a complete mathematical component, not a recovered assessment key. The scale z agrees with the magnitude obtained
from the incorrect relation b=-a; the multipliers2 and3/2 remain unexplained
empirical shapes, with no recovered intent claim. In this evidence profile D=-E, E>1,F=0.
The raw bank has no correct answer and **no correct ref**. The supported repaired
profile substitutes the actual solution for the first value. Empirical shape
intent remains unresolved; neither profile is used by default.

q18483's complete observed bank is X+Y,X-Y,-(X+Y),Y,X. These are plausible
whole-expression transformations, retained as observed shapes without an intent
claim. The source correct value26 is independently derived. Exactly2 source
banks have one mathematically valid choice; q12457 has zero. All3 raw banks and
15 values replay; missing correct designations have denominator0, not3.

Normal pair/canonical defaults choose a complete authored bank first: correct
pair; reverse the isolated affine slope and solve that altered substitution;
omit the outer multiplier on the substituted constant and solve; omit the final
division when solving the remaining variable then back-substitute; swap the two
values. All wrong values come from these operations on the printed equations.
Normal difference defaults use correct difference, sum, reversed difference,
first-variable-only, and a sign-reversed first isolation followed by actual
back-substitution. A nonfinite member, equivalent wrong/correct value or any
pairwise bank collision rejects the WHOLE instance. There is no first-valid pool,
option replacement, independent arbitrary random error or learner-facing diagnosis.

## 4. Reusable templates and constraints

Parameters A..F denote Ax+By=C and Dx+Ey=F, with variable-pair choices x/y,u/v,
p/q,a/b. All coefficients/constants are exact integers and determinant AE-BD
is nonzero. `pair_first` isolates the unit y coefficient of row1; `pair_second`
isolates y of row2; `canonical_second` isolates x of row2; `difference` solves a
nonunit single-variable row then substitutes into the other. Sign-aware terms
and parentheses preserve explicit distribution operands; exact rationals remain
fractional, not decimal. Complete rows survive parameter changes.

The learner sees only prompt, choices and the same fixed worked solution.
Parameters, source lineage, inferred recipes, authored levels and evidence-only
flags stay in generation metadata. Source replay uses these same public recipes
with explicit parameters/profiles; it never returns a literal copied payload.
The authored unit-isolation pair_first has3+6+6 rows, omitting division by1
and its redundant simplified row; this does not change the observed canonical
5+6+6 sequence. Seeded sampling covers signed coefficients, signs of values, integer/rational
solutions and all four variable pairs within the documented level bounds.

Canonical task fingerprints use the two actual linear coefficient rows divided
by their first nonzero coefficients and sorted, plus response criterion. Variable
spelling, common row scaling, bank profiles and choice ordering are excluded.
Content identity uses version, actual displayed prompt, fixed solution and full
sorted displayed bank and schema difficulty. Seed and shuffle do not change identity. Owned stable
answer UUIDs derive from field identity and displayed value; correct lookup refs
point to an answer in that field.

All raw captured system braces are unmatched TeX groups. Generated presentation
escapes only the opening literal brace as `\{`. Raw capture remains untouched.
Prompt fidelity is separately reported as raw0/3 and presentation-normalized3/3;
canonical solution fidelity is separately full-prose/row sequence after this
repair and whitespace normalization. Answer-bank mathematics is unchanged by
this presentation repair. No plots or image assets occur; steps5 and7 require
no renderer.
