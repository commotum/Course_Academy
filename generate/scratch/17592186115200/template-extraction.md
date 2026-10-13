# Four-stage extraction

## 1. Original-specific description

The classification table and source-cases.json enumerate all nine originals and their parameters, preserving source.json with its provenance. q-26817 is 2^(x−1)=16^(x+1), five radio scalars, no difficulty/solution/correct ref. q-66877 is 12^(h−4)=144^(3h), same omissions. q-66864 is 9^(x−5)=3^x, easy, three exponential rows and three exponent-equation rows, fields absent. q-66863 is 4^(x+4)=16^x, easy, three exponential rows and only two exponent rows. q-66872 is 5^(m−10)=125^m, easy, three exponential and three exponent rows, with negative coefficient collection. q-110537 is 4^(k−1)=64^(2k), moderate, three exponential and three exponent rows; its initial prose names the wrong side. q-110539 is 81^(2a)=1/3^(a−1), hard, three rewrite rows, one negative-exponent row, four linear rows; fields absent and initial prose names the wrong side. q-100449 and q-3103 are respectively 8^(5a−12)=1/64^(a+4) and 5^(2a−5)=1/25^(a+1), hard, with the same 3+1+4 row structure and separate complete banks.

Every captured answer is a delimiter-free exact scalar, not an equation fragment. There are seven original banks, each with five values; there are no plots. Source-case levels for the two unrated records are explicitly authored, not recovered ratings.

## 2. General pattern

For positive integer B>1 and n in {2,3,4}, one displayed base is B^n. Rewrite that one base as a power of B, apply the power rule and equate real exponents. A reciprocal adds the negative-exponent step. Exponents remain affine, with a unique nonzero rational root. The required answer is the variable value. The common opening and source-specific prose, row count, collection orientation and omitted redundant collection row are maintained.

## 3. Components and complete banks

Parameters are B,n,a,c,b,d,v, with original affine exponents av+c and bv+d. Let the rewritten affine coefficients be A,C,B',D' and let z=(D'−C)/(A−B'). These letters in this document are author notation only. The script holds each complete bank together; no option pool or first-valid repair exists.

The following lists give ALL original options in captured order and their component recipes. Intent for opaque scalar choices is unresolved; these expressions define evidence-only parameterized replay profiles and do not claim to recover pedagogical mistakes. Normal learning output uses the independent authored bank below. No arbitrary polynomial fit or stored original answer payload is used.

| Profile | Full component recipe list | Original values |
|---|---|---|
| q-26817 | z, (−c−d+1)/(n−1), −n/(n−2), −c, (c−nd−2)/(n−1) | −5/3, 1/3, −2, 1, −7/3 |
| q-66877 | (nb−1)/c, −nb+1, c, z, 2n/(c−nb) | −5/4, −5, −4, −4/5, −2/5 |
| q-100449 | (a+n)/d, 1/(a+n), −d/a, z, −1/d | 7/4, 1/7, −4/5, 4/7, −1/4 |
| q-110537 | z, −c/(nb+a), c/b, −(nb+a), nb−a | −1/5, 1/7, −1/2, −7, 5 |
| q-3103 | −z, z, 0, (a+n+N)/(a+n), −(a+n+N)/N; N=D'−C | −3/4, 3/4, 0, 7/4, −7/3 |
| q-66863 | 0, c−1, 1, z, n | 0, 3, 1, 4, 2 |
| q-66872 | nc/2, −c, c/2+1, n, z | −15, 10, −4, 3, −5 |

These complete historical banks are not accepted as authored error models. Their mathematical correctness and exact presence are independently checked, and changed shifts/base variants are included in changed-profiles.json and review.md. Every raw profile explicitly sets evidence_only=true and eligible_for_learning=false, including fieldless ones. The opaque formulas may reject changed parameters when any denominator vanishes or choices collide.

The authored bank is a separate complete five-option profile, chosen before sampling:

- Ordinary right-base equations: correct; omit the power rule (when the original slopes differ), or substitute n for the entire scaled exponent when slopes agree; multiply the rewritten variable coefficient by n twice while multiplying its shift only once (when d=0 this also equals applying the whole power rule twice); reverse the sign during constant transposition; add slopes instead of subtracting them. Each value solves that particular altered linear equation.
- Ordinary left-base equations: correct; apply the power rule twice to both slope and shift; forget to scale the shift; reverse constant transposition; add slopes instead of subtracting. These operations preserve the particular displayed affine components.
- Reciprocal right-base equations: correct; forget the negative exponent; negate the variable term but not its shift; omit the inner power; reverse constant transposition.
- Reciprocal left-base equations with unshifted left exponent: correct; forget the reciprocal sign; omit the inner power; add n to the slope instead of multiplying it; reverse final division.

The bank is rejected as a whole for an undefined value or any mathematical collision. There is one solution independent of the chosen error; no diagnosis is inserted into learner-facing choices or prose.

## 4. Reusable masks and bounds

Power, reciprocal, affine-expression, nested-power and aligned-row masks build complete components before combining prose. Raw profiles select the captured punctuation, prompt wording and row sequence parametrically. No source payload is returned as a special-case answer. Source solution parity is byte-exact for all seven present solutions. Prompt parity is byte-exact for all nine originals. Answers match all 35 captured scalars exactly, irrespective of order.

Base catalog: {2,3,4,5,6,7,8,9,10,12}; n=2..4; displayed larger base≤1296. All coefficients/slopes are integers. The base catalog includes the original 12 and perfect powers 144/125/81/64/25/16/9. Familiar small perfect powers and linear-equation arithmetic anchor the extension bounds. Explicit calls enforce exactly the same domain as sampling.

Easy: original slopes a=b=1, d=0, nonzero |c|≤12. Left/right orientations and collection layouts retain one rewrite, one power-rule product and one linear solve. Moderate: a=1, b=2..5, d=0, 0<|c|≤12; the nonunit original slope adds a multiplication to the same method. The separately supported two-shift template has a=b=1 and nonzero c,d (|c|≤12, |d|≤6), based on unrated q-26817; it is available explicitly but not sampled as a default moderate alternative. Hard right: a=2..5, b=1, c=−12..−1, d=1..6. Hard left: a=2..5, b=1, c=0, d=−6..−1. Both hard orientations have exactly the observed rewrite, reciprocal negation, shifted-exponent distribution, collection and division stages (3+1+4 displayed rows), without nonlinear equations or logarithms. Differences in which side's slope is multiplied and which constants collect are unordered source-supported variations of that workload.

Variable aliases are x,m,h,k,a. They do not inflate mathematical task counts. Neither do bank profiles or the duplicate easy right collection layout. Counts are enumerated from the finite valid domains and reported per template, so overlapping template counts must not be added. Content identity hashes the actual displayed prompt, fixed solution, bank, attribute presence and correct designation. It excludes seed/ordering/profile labels. The mathematical fingerprint excludes variable aliases and answer banks; it retains the bases, rewrite orientation, reciprocal status and affine data because recognizing the perfect-power rewrite is assessed.

Raw prose anomalies: q-110537 says “left-hand side” while rewriting the right; q-110539 says “right-hand side” while rewriting the left. Raw replay retains both exact strings. Normal output derives the actual side from its displayed equation, giving a minimal teaching repair. Missing correct refs are independently derived as −5/3 and −4/5 only in separate native grading fixtures; raw refs stay absent. There are no mathematical choice-bank errors at the original parameters.
