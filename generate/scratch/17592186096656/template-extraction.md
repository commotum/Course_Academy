# Template extraction

Every source-specific prompt, solution, original parameter tuple, field type, choice value and recipe index is retained in template-extraction.json. source-cases.json maps every source to its complete bank. Recipes in bank() are mathematical expressions, not pooled labels. Psychological interpretations remain unresolved where the evidence only establishes a numerical expression.

Shared pattern: integrate a n^(kx+b), using u=kx+b and dx=du/k. The indefinite answer is a n^(kx+b)/(k ln n)+C. Definite answers evaluate that primitive at H and L; negative k reverses the transformed limits without changing the ordered x bounds. Fields preserve selection/radio with five owned choices, or field-1/blank with one canonical exact value. Answers are delimiter-free TeX; questions preserve the integral and field placeholder layout. No distractor feedback is added.

Write E=n^(kx+b), J=ln n, d=1/k, D=n^k-1. The complete observed profiles, in recipe order, are:

- q-31405: E/J; n^(kx/2+b)/k; E/k; E/(kJ); n^(kx/2+b)/J.
- q-31418 (k=-1, b<0): n^(-kx-b)/n; E/(kJ); -n^(-kx-b)/J; -n^(kx)/J; E/J.
- q-31412 (k=-1,b=0): E/(kJ); -E; n^x/J; E/J; -n^x/J.
- q-31413 (k>1,b=0): E/(kJ); E/k; E/J; -n^(kx-7)/(kJ); n^x/J. The observed altered constant -7 remains fixed; its error interpretation is unresolved.
- q-31417 (k=1/d,b=0,n!=d): n^x/(dJ); E/(dJ); dE/J; d n^x/ln d; E/ln d.
- q-30973 (k=6,n=3,L=0,H=1 originally): D/J; D/(2n); D/(kJ); D/(2J); (n^(k-1)-1)/(2J). The coefficient 2 is an observed fixed pattern; keep it rather than inventing an error explanation. Sampling is bounded to k in {4,6,8}, n in {2,...,6}, preserving these complete mathematical recipes.
- q-349625, q-349626, q-349631, q-349646, q-349648: one exact definite answer, no distractor recipes. Original tuples are (a,k,b,n,L,H)=(1,-2,7,3,1,2),(3,-1,5,2,1,3),(2,-1,1,4,0,1),(1,1,-1,5,0,2),(1,1,1,3,-1,1).

Observed easy tuples: q-31405 (1,6,-1,2); q-31418 (1,-1,-6,3); q-31412 (1,-1,0,5); q-31413 (1,5,0,4); q-31417 (1,1/3,0,6). Proposed bounds are separate: integer bases 2..6, positive integer outer coefficient 1..5 for blanks, bounded nonzero signed slopes, shifts -4..8 for blanks and bounded ordered integer limits -2<=L<H<=4. Easy profiles retain their specific signs, zero/nonzero shifts and unit/reciprocal slope constraints. Legacy positive shifts of either sign are an explicit extension. Blank positive slopes above 1 are an explicit extension requiring the conditional coefficient-pull line. No new difficulty is inferred from larger numbers.

Standardized TeX preserves the source substitution sentences, limit-table layout and worked method; differential direction and algebraic display formatting are normalized. Source-specific legacy solutions were missing and are newly authored from canonical e-460. Literal fidelity is reported separately from mathematical fidelity; source-bank replay requires all 35 choices across 11 banks, ignoring order while retaining correct designation where present. Exact numeric strings are never reused as unexplained source literals when parameterized recipes are known.

Sampling selects a complete profile first and rejects equivalent choices, extra correct answers, invalid domains and collapsed source features. Fingerprints use the simplified integrand and actual x bounds, ignoring seeds, UUIDs, profile choice, answer order and formatting. Existing mathematical tasks and the canonical example are excluded from new submissions. Hard is rejected. Bounded searches report explicit remaining shortages instead of duplicating content.
