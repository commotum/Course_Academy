# Four extraction stages

## 1. Specific source descriptions

q-31420 supplies x·8^(3x²), substitutes u=3x², differentiates to 6x and
isolates x dx=(1/6)du. q-31419 supplies x·4^(x²−7); q-73802 supplies the
same shifted-quadratic structure at base 7 with a different full bank. Each
isolates (1/2)du=x dx. q-31426 supplies x·5^(x²/3), differentiates the rational
quadratic to (2/3)x and uses (3/2)du=x dx. q-73665 supplies
4x·4^(4x²−3), initially extracts the outer scalar 4, uses (1/8)du=x dx,
then collects 4/8 into 1/2. Its outer-scalar stages are essential. q-73801
supplies 2x·6^(x²+1); du already equals 2x dx, so its chain has four rows
and omits a redundant scalar-extraction row. q-211989 supplies x²·4^(x³/5),
differentiates to (3/5)x² and uses (5/3)du=x² dx. These seven solutions
share the introduction “Let's introduce the new variable … Differentiating
gives”, a formal derivative and differential equality, then “Therefore,” and
the fixed ordered evaluation chain. Every option ends in +C and all banks have
five choices, no option feedback.

q-73800 supplies 3x²·3^(x³−5) with five options, but no difficulty, correct
designation or worked solution. Its unique correct primitive is independently
derived as 3^(x³−5)/ln(3)+C, since its derivative is the displayed integrand.
That mathematical inference is not an original-key match. Raw public replay
retains all three omissions and is ineligible; normal completion adds the
missing fields with explicit authoring provenance. No mathematical source
repair is needed in the seven complete banks.

## 2. Generalized pattern and purpose

Integrate P(x)b^U(x), where U=ax^n/d+s, P=kx^(n−1), b is an integer greater
than one, and P/U′ is the constant R=kd/(an). Set u=U, state U′ and the
differential relation, reorder the original integrand as in its source family,
substitute, extract the scalar if nonunit, integrate b^u as b^u/ln(b), and
substitute back. There is one concrete worked solution independent of which
option is selected. This is polynomial substitution into a general exponential;
no new operators or subsequent curriculum topics are introduced.

## 3. Complete component and option mapping

`source-components.json` records every source prompt, worked solution, source
field, original answer ID, exact complete answer value and its parameterized
expression recipe. `source-cases.json` maps every original MA record to the
public generator template, level placement, parameters and original bank
profile. Values compare one-to-one, ignoring shuffle only: 40/40 raw values,
8/8 full banks, 7/7 original keys and 7/7 original solutions. The five options
of q-73800 have no original key, and therefore do not inflate distractor/key
counts; the other originals supply 28 designated distractors.

Historical profiles replace the complete exponential-base token b₀^… and
its matching ln(b₀), retaining all other expression components. In q-73801 the
separate divisor 6, divisor 3 and ln(3) option remain literal observed components
under base transport. Those expressions cannot establish their historical error
operations. Every historical bank is therefore a public ineligible evidence
profile; the whole bank is transported, never replaced by selected options from
a pool. Changed-base examples and exhaustive base-domain checks establish
parameterized replay rather than an original-answer lookup.

The normal bank is separately authored from the method. For nonunit R it is
{R E/L, R E, R E L, E/(R L), E/L}+C with E=b^U and L=ln(b): correct,
omit the logarithm divisor, multiply by the logarithm, invert the differential
ratio, and omit the differential ratio. Direct-differential families instead
use {E/L, E, E L, E/(nL), nE/L}+C, representing a retained monomial-derivative
coefficient or an extra use of the supplied prefactor. These complete profiles
are selected before parameters; no first-valid replacement or unrelated
constant perturbation occurs. Whole instances reject collisions modulo C.

## 4. Backbone, slots and dependent construction

The actual finite domains are enforced in `DOMAINS` on random sampling and
explicit calls. All templates vary the base in 2..12. q-31420 varies its
quadratic multiplier a in 2..5. q-31419/q-73802 vary the negative shift −9..−1.
q-31426 varies the positive exponent divisor 3..9. q-73665 varies the tied
exponent/prefactor coefficient a=2..5 and negative shift −6..−1; its final
ratio stays 1/2, while its initial outer-scalar and derivative rows change.
q-73801 varies the positive shift 1..9. q-211989 varies the cubic divisor in
{2,4,5,7,8}, preserving a reduced nonunit rational scale. The q-73800 completion
varies its negative shift −9..−1 with prefactor 3x². Authored hard keeps n=4,
prefactor x³, a in {−1,−2,−3} and shift in {−5,…,−1,1,…,5}.

Source-family normal solutions use simultaneous complete-component masks,
including separate rational-power, derivative, differential-factor and final
fraction slots. They retain the exact full source wording and mathematical
stage order at original parameters and under changes. No single numeral is
blindly replaced across prose or unrelated roles. Source q-73665 retains its
outer coefficient in the first two rows and its combined 1/2 row; q-73801 retains
its omitted extraction row. Missing q-73800 and hard solutions are explicitly
authored from the same formal introduction, derivative/differential, reordered
integral, substitution, applicable extraction, primitive and back-substitution.

Real domain is all x∈R. Positive integer bases keep every exponential and every
constant logarithm real; no connected-interval, absolute-value or root branches
are needed. Banks are compared by derivatives, which identifies general
antiderivatives modulo the arbitrary additive constant C. Prime-factorized base
normalization deduplicates mathematically identical integrands across base-power
and coefficient/divisor spellings; banks/profiles do not enter that fingerprint.
Content identity separately includes actual displayed prompt, fixed solution,
bank and difficulty and is independent of seed or choice order.

`validate.py` exhausts the finite workload domains and all eight 11-base raw
profiles. It reads the actual exponent, u, formal derivative, differential
relation, every displayed integral/primitive row and complete bank; directed
interval witnesses disprove equality between wrong choices even modulo C.
Mutation regressions require rejection of wrong derivatives, wrong substituted
factors, a mathematically equal row that erases scalar extraction, and a C0
control-character corruption. Native grading and raw source fidelity have
separate counts and denominators in `validation.json`.
