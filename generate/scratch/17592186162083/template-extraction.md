# Source templates and slots

`source-questions.md` describes each complete original, including every bank,
key, prompt and solution. `source.json` retains exact source fields. `CASES` in
the generator records all original parameters, and `source-replay.json` reports
complete original bank and wording comparisons.

| Profile | Original supplied curve and substitution | Known integral; statement results | Ordered solution stages |
| --- | --- | --- | --- |
| q-122814 | (t⁴−3t²,t), 0≤t≤2; t=2u, 0≤u≤1 | 4; F,F,T | Orientation (I,III), reparametrization (II), Cartesian x=y⁴−3y² and range |
| q-122815 | (cos(u/2),sin(u/2)), 0≤u≤2π; u=2t, 0≤t≤π | 1; F,F,T | Reparametrization (I), half-circle radius and angle, orientation (II,III) |
| q-122816 | (t,t^(3/2)), 0≤t≤4; t=4u, 0≤u≤1 | 3; T,F,F | Orientation (I,II), reparametrization (III), Cartesian y=x^(3/2) and range |
| q-122851 | (sqrt(9t²+1),3t), 0≤t≤1/3; 3t=2u, 0≤u≤1/2 | arbitrary k; F,F,T | Orientation (I), reparametrization (II,III), Cartesian x=sqrt(y²+1) and range |
| q-122868 | (2t,2sqrt(t)), 0≤t≤2; t=2u, 0≤u≤1 | arbitrary k; T,F,T | Reparametrization (I,II), Cartesian y=sqrt(2x) and range, orientation (III) |

Observed Boolean profiles are field-owned false/true pairs. The incorrect
claims are respectively: negating the known value; scaling it by the parameter
speed; for q-122851 scaling k by b/a. These false claims are statements in the
prompt rather than pooled radio distractors. The complete Boolean banks remain
unchanged; all original values and designations must match. With arbitrary k,
false means not guaranteed for every k (a coincidence at k=0 does not make a
claim universally true). Concrete k is positive so negation and scaling cannot
coincide with the correct answer.

Conservative generalization, separately from the original parameters:

- q-122814: x=a y⁴−b y², a=1..3, b=1..6, y=0..T, T=2..6.
  r₂ substitutes t=T u. Concrete k is a positive integer. The three statement
  targets and their original order stay fixed because they define this profile.
- q-122815: radius R=1..8; first angular rate 1/d, d=2..4, second
  n=1..3. Upper bounds dπ and π/n guarantee one half-circle, same orientation.
  The false speed claim becomes dn times k. Curve radius is the genuine slot;
  speeds and integral values alone cannot produce distinct inventory content.
- q-122816: y=c x^(3/2), c=1..5, x=0..T, T in {4,9,16}.
  These perfect-square bounds keep the rescaled coefficient exact and integral.
  r₂ substitutes t=T u; false claim T times k. No new power or operation added.
- q-122851: x=sqrt(y²+h), h=1..9, y=0..L, L=1..5. Positive
  unequal integer rates a,b give t=L/a and u=L/b. Both stay on the positive
  square-root branch; II uses (b/a)k. Arbitrary k stays symbolic.
- q-122868: x=A t, y=B sqrt(t), A,B=2..6, t=0..T, T=2..5;
  r₂ substitutes t=s u, s=2..5. Cartesian y=sqrt((B²/A)x), 0≤x≤AT.
  Parameters are positive, so branch choice is unambiguous. At t=0 the square-root
  speed is singular, but the same trace has a regular y-parametrization and finite
  arc length; this is the original source endpoint and introduces no new issue.

All coefficients, ranges, integral values, false claims, solution equalities,
Cartesian equations and conclusion come from one parameter record. Every
source solution's sentences and math blocks are parameterized by simultaneous
whole-fragment replacement; no independently sampled solution values exist.
Source replay is exact at original parameters. Sampling uses a smaller bounded
policy for speed and k to avoid repeatedly counting equivalent curve geometry.
Geometry normalized over z∈[0,1] defines the mathematical fingerprint across
profiles. Seed, speed, option order and supplied integral value are omitted.

No target-position slots were declared: statement roles are fixed by the source
backbones; geometry, endpoints and speeds are the variable slots. Exhaustive
bounded-case validation reports their actual coverage. Original speed parameters
remain available for replay even when the normal bounded policy is narrower.
Easy lacks a rated source; this package does not invent a simpler response type
or family to fill it. Its nominal five-question shortage remains explicit.
New source evidence can reopen that exception.
