# Four-stage template extraction

## 1. Specific original questions

`source.json` is the complete immutable evidence; `source-cases.json` lists all
nine MA originals with source_id, difficulty, template, parameters and
bank_profile. Raw `profile="evidence"` uses the same coefficient/factor recipes
as changed variants, preserves strings and attribute presence, and remains
ineligible. No original-parameter branch returns a copied payload.

q1886 has f=11cos(x)−sec(x)+1/x at sqrt(3). Its four derivative rows preserve the
formal supplied reciprocal, a second formal row rewriting 1/x as x^-1,
substitution of each derivative, and sign collection. Its two evaluation rows
substitute sqrt(3) and simplify only its reciprocal square; trig values remain
unevaluated. q1905 is f=2x−sqrt(2)sec(x) atpi/4: two derivative rows and four
evaluation rows retain actual trig substitution, special-angle values, 2−2,
and zero. q104437 is f=x*cot(x) atpi/4: formal product derivative, substituted
cot+x(-csc²), distributed result, then three evaluation rows. It has no captured
answer fields. q340642 is g=csc(x)cot(x) atpi/2: formal derivative, both product
rule terms, factored-csc result; three evaluation rows keep both cot² and csc²
and their zero/one squared values.

q104442 has f=sec(x)/sqrt(3)+3x²/pi atpi/3; two derivative rows followed by four
substitution, individual-evaluation, 2+2 and final4 rows. q1904 has f=−x²+5csc(x)
atpi/6, three derivative rows including 2*(-x)+5*(-csc*cot), then three
evaluation rows. q340630 has h=e^x+3sec(x) atpi: two derivative rows and three
slope rows preserve the sec(pi)=-1 and tan(pi)=0 contribution before collection.
q340660 has f=4x/sec(x) at0: formal whole derivative, formal quotient rule with
ordered d/dx(4x) and d/dx(sec(x)), substituted quotient, factored numerator,
and cancellation of one secant; three evaluation rows retain zero-tangent and
unit-secant substitution. q70874 has f=ln(x)+3csc(x) atpi/3: formal derivative,
substituted components, reduced derivative; then four rows retain 2/sqrt(3),
1/sqrt(3), their product2/3, and final3/pi−2.

## 2. Generalized backbones

Every question asks for one scalar tangent slope by differentiating the supplied
function then substituting the stated point. Easy families use established sum
rules and source familiar angles. Moderate preserves the source reciprocal
rewrite, product-rule or quotient-rule backbone rather than replacing them by
an equivalent shortcut. The hard extension keeps canonical e3648's complete
quotient structure and worked solution. Trig arguments remain exactly x,
function labels and source target roles remain consistent, derivative order is
one, and each generated instance has one fixed worked solution.

The variable slot is an existing scalar a, not a new operation. In q1886 it is
the cosine coefficient; in q1905 the linear coefficient; in q104437 the linear
factor coefficient; in q340642 the first csc factor coefficient; in q104442
the quadratic numerator coefficient; in q1904 and q70874 the csc coefficient;
in q340630 the exponential coefficient; in q340660 the numerator's linear
coefficient. Coefficient1 is implicit only where the source uses an implicit
factor. Whole mathematical components are masked before rendering, never
single variable letters or function arguments inside prose. Hard's angle is a
complete point slot and updates all prompt, prose, derivative labels, substituted
function arguments and evaluated components together.

## 3. Every original complete bank

Let A=sqrt(3), U=sin(A), V=sec(A)tan(A), W=csc(A)cot(A). Let P=pi/6 and Q=pi/3.
The following lists are complete banks in captured order, with zero-based
correct indices. Every displayed value and source designation is replayed;
choice order is shuffled only after field-owned answer identities are fixed.

| Family | Complete parameterized bank | Correct |
|---|---|---|
| q1886, a=11 | −U−W−1/3; −aU−V−1/3; −aU+V+1/3; aU−V−1/3; −aU−W−1 | 1 |
| q1905, a=2 | a+2; a−6sqrt(2); a+3sqrt(2); a−2; a−3sqrt(2) | 3 |
| q104437, a=1 | No captured fields; authored normal blank a(1−pi/2) | inferred |
| q340642, a=1 | Blank −a | 0 |
| q104442, a=3 | 2−2a/3; −2−2a/3; 2; 2+2a/3; −2a/3 | 3 |
| q1904, a=5 | −2P−a sqrt(3); 2P−2a sqrt(3); −P−2a sqrt(3); 2P+2a sqrt(3); −2P−2a sqrt(3) | 4 |
| q340630, a=1 | Blank a e^pi | 0 |
| q340660, a=4 | Blank a | 0 |
| q70874, a=3 | 2a/3−1/Q; 1/Q−2a/3; pi−2a/3; 1/Q; 1/Q+2a/3 | 1 |

q1886's first wrong value combines omitted cosine coefficient and the csc/cot
pair in place of sec/tan; the third reverses secant/reciprocal signs; fourth
reverses cosine sign; fifth substitutes the reciprocal-trig pair and omits the
reciprocal-square evaluation. q104442's wrong operations subtract the two
correct derivative contributions, reverse the entire result, omit the
quadratic contribution, or retain the negative quadratic contribution alone.
q1904 omits the csc value2, reverses the quadratic sign, omits its power-rule
factor2, or reverses both signs. q70874 reverses the result, uses Q instead of
1/Q for the log derivative, omits csc's contribution, or reverses its sign.
These mappings reproduce the whole original values; they do not add learner
feedback absent from the captures.

q1905's values involving 3sqrt(2) and 6sqrt(2) do not uniquely identify source
error operations. They remain opaque historical formulas; only the actual
linear coefficient varies, while those fixed historical constants stay fixed.
This profile is ineligible for learning. The authored default uses the complete
method-derived bank a−2 (correct), a+2 (secant derivative sign), a−sqrt(2)
(omit the supplied sqrt(2) coefficient), a−2sqrt(2) (confuse secant derivative
with sec²), and a*pi/4−2 (retain the linear term without differentiating).
No arbitrary fitted recipe is promoted as recovered intent. Sourcea=2 has
correct0, a=3 has correct1; neither is excluded.

## 4. Reusable masks, constraints and authored hard

`templates.json` freezes every original prompt, prose sentence, field contract
and operative row, with complete coefficient/component slots. Source layouts
with dy/dx evaluation bars remain dy/dx evaluation bars. Scalar masks derive
a, 2a, 2a/3 and a*pi/2 from one exact instance, retaining individual arithmetic
rows rather than asking SymPy to collapse the teaching sequence. Normal output
uses proper TeX function commands, removes invisible application glyphs, and
flattens redundant nested aligned wrappers. Exact raw replay retains original
bytes; those presentation changes never alter an original mathematical value.

All sampler and explicit-input domains are the same finite tuples. Numeric
coefficients are strict Python integers (bool rejected), with the documented
bounds; hard angles are exact strings pi/6, pi/4 or pi/3. Complete eligible
profiles are selected before parameters and all five choices are built. Any
ambiguity invalidates the whole instance; there is no pooled-first-valid bank
construction. The finite domain is independently checked with exact SymPy
mathematics; nonzero scalar differences involving sqrt(3) trigonometry are
certified by 50-digit interval arithmetic. Every original and changed bank is
checked pairwise, including two wrong choices.

The missing hard family is authored from canonical e3648: f=−a*cot(x)/sin(x),
a=1..24, with first-quadrant familiar angles pi/6, pi/4, pi/3. Its four derivative
rows are formal whole derivative; formal quotient with ordered numerator and
denominator derivatives; substituted components; csc²(x)sin(x)=csc(x)
reduction. Its four evaluation rows are actual point substitution; individual
csc/cot/cos/sin values; computed numerator over evaluated sin² denominator;
final scalar. Both derivative contributions are nonzero throughout this hard
domain. The canonical a=2,pi/4 gives6sqrt(2). This is a supported missing-level
design, not an observed hard label or a new quotient/chain-rule skill.

Domains specify the connected real pole-free component containing the stated
point, with cos(x)!=0 for secant families, sin(x)!=0 for cosecant/cotangent,
x!=0 for the reciprocal family and x>0 for logarithms. No formal cancellation
extends the supplied quotient's original domain. The full source contracts,
formal-operator ordering, intermediate structures, zero contributions and
contextual m=blank are independently read from learner strings. Seed/order do
not change content IDs, and mathematical task fingerprints exclude bank/profile
and display aliases. Default finite batches deduplicate the actual function
and evaluation point, not IDs or unused parameters. No plots are required.
