# Four extraction stages

## 1. Specific originals

q-160365 gives `u=y−2x,v=y+x`, lines `y=2x−1,2x+1,1−x,2−x`, first quadrant. It asks area, radio 5, no solution, no rating, no key. Mapping gives rectangle `[-1,1]×[1,2]`; determinant −3, area 2/3. Source line forms and inline layout remain distinct from current display layout.

q-160379 gives `u=y/x²,v=xy`, curves `y=x²,2x²,1/x,4/x`, first quadrant, radio 5, no solution, rating, or key. Rectangle `[1,2]×[1,4]`, determinant −3y/x²=−3u, inverse −1/(3u), area ln2.

q-160870 gives `u=y−3x,v=y+2x`, lines `3x−2,3x+2,1−2x,3−2x`, radio 5, rated easy. Its full solution maps to `[-2,2]×[1,3]`, determinant −5, reciprocal −1/5, area 8/5. Its displayed first-quadrant claim is inconsistent: `x=(v−u)/5`, `y=(2u+3v)/5` are sometimes negative on that rectangle. Clipping to x,y≥0 subtracts uv-area 1/2+1/12; actual first-quadrant area is **89/60**, absent from the bank. Normal prompt removes “in the first quadrant,” preserving the intended four-line region and source teaching calculation. Raw source is retained, not counted mathematically correct for its literal quadrant claim.

q-160891 gives `u=1/(xy),v=x²y`, curves `1/(2x),1/(3x),1/x²,3/x²`, radio 5, moderate. The eleven display blocks contain: area integral; T; change formula; given U,V; T inverse; two boundary chains; rectangle; formal derivative matrix → substituted entries → determinant 1/y; reciprocal y → x²y²/(x²y) → 1/(u²v); integral → absolute Jacobian → nested integral → separation → endpoint arithmetic → ln3/6. The source's nested du dv is reversed relative to its displayed bounds; normal uses dv du. Negative sign inside absolute value does not alter area but contradicts the positive preceding determinant; normal corrects it.

## 2. Shared backbone

Given two independent boundary-coordinate functions, map each pair of curves to constant coordinate lines, display the rectangle, differentiate all four coordinate components, take determinant and its reciprocal, then integrate its absolute value over that rectangle. One fixed solution per instance; no response-dependent feedback. Scalar mathematical radio field, exactly five owned choices. No discover-the-transformation step or inverse-map solving.

## 3. Every observed bank

Let `L,H` be u bounds, `j,k` v bounds; `W=H−L,Z=k−j`; `D=a+b` in linear maps. Each row is one **complete** observed bank, never a pooled menu.

| Bank and original ordered values | Parameterized complete recipes | Interpretation limits |
|---|---|---|
| linear legacy: 2, 2/3, 1/3, 6, 4 | WZ, WZ/D, Z/D, DWZ, W²Z | omission/inversion recipes plausible; W²Z is opaque recorded pattern |
| linear: 5/6, 4/5, 8/3, 4/3, 8/5 | D/(W+Z), W/D, WZ/a, W/a, WZ/D | D/(W+Z) is opaque; others omit dimension or determinant component |
| quotient: 3ln2, 4ln2, ln4, ln2, (ln2)/2 | Z ln(H/L), k ln(H/L), ln(k/j), A, A/2 | factor recipes and wrong-bounds log; final half is unresolved historical operation |
| reciprocal: (ln3)/3, (ln3)/6, (ln2)/3, (ln2)/6, (ln3)/2 | ln(k/j)/H, A, ln(Z)/H, (1/L−1/H)ln(Z), ln(k/j)/L | endpoint omission, log of interval width instead of ratio |

All twenty exact values replay one-to-one. Two captured correct designations match. Two absent designations remain absent and cannot be counted matched. Scalar opaque expressions are evidence profiles, not promoted as recovered author intent. `source-cases.json` exposes all originals through `generate` with original parameters and profiles.

Normal authored banks follow the actual method and are chosen before parameters:

- Linear: `[A,WZ,DWZ,WZ/a,WZ/b]`: omit Jacobian, invert Jacobian, omit either determinant component. Requires `a,b>1` and `a≠b` for this authored bank; unit-coefficient originals remain available through their complete historical profiles. Collisions reject the whole instance.
- Quotient: `[A,Z ln(H/L),Z ln(H/L)/n,Z ln(H),Z ln(L)/(n+1)]`: omit factor n+1, use n, omit lower endpoint with Jacobian omitted, omit upper endpoint. Whole bank comparison rejects any collision.
- Reciprocal/scaled: with `C=c/(n−1),R=ln(k/j),F=C(1/L−1/H)`, `[A,CR/L,CR/H,F ln(k),F ln(j)]`: omit one u endpoint or one log endpoint. Whole bank comparison rejects `j=1` because the omitted-lower-log value becomes correct; it does not substitute an unrelated wrong option.

No distractor explanations appear to learners. Source answer feedback is absent and stays absent.

## 4. Slots and limits

Linear `a,b∈1..4`, `−5≤L<H≤9`, `1≤j<k≤10`, easy widths W≤8,Z≤6; sampler narrower signed L and small H. Normal drops quadrant restriction, allowing full line-bounded parallelograms. Quadratic quotient `n=2`, positive u bounds; reciprocal `c=d=1,n=2`; hard `c,d∈2..4,n=3`. Explicit calls enforce every limit; invalid explicit parameters are never resampled. All labels, boundary equations, four matrix entries, determinant, cancellation ratio, integration factors/bounds and endpoint arithmetic derive from the same instance.

Source source-shaped inline versus display masks are retained. Raw solution replacements use complete components and simultaneous longest-match slot insertion; never blindly replace a digit through prose. Anchor masks yield entire exact source chains; changing bound slots changes prompt, solution, answer bank and plot. Normal current chains retain eleven blocks and all operative source stages, including the reciprocal cancellation ratio. Normal quotient and hard are explicitly authored extensions using this same prose/chain.

Mathematical task identity includes supplied maps, actual bounds, actual area demand and authored workload level, excluding bank profiles, seed, notation aliases and choice order. Content identity hashes actual prompt, solution, sorted complete bank, and difficulty. Fixed inputs keep owned UUIDs across seed/order changes. Normal defaults cover all supported source-shaped families, not only explicit replay.

Finite sampler enumeration (`variety.py`, `variety.json`): **2916** eligible easy tasks (linear aliases counted once), **281** quadratic quotient moderate tasks, **224** reciprocal moderate tasks, **2016** authored hard tasks. Exact prime-exponent logarithm signatures reject every pairwise equivalent bank, including pairs of wrong answers. This enumeration does not count shuffles or labels as variation.

Separate **authored complete endpoint/coefficient banks** make normal completion possible at every source anchor; they are selected before random parameters, not patched into a partially built bank:

- Linear unit coefficient: exactly one of a,b is 1; `[A,WZ,DWZ,Z/D,(W+Z)/D]`. The last operation uses a sum of rectangle side lengths instead of their product; the others omit/invert Jacobian or omit the u width. Every collision rejects the whole instance. Normal source q-160365 therefore has an eligible method-derived bank at its original map/bounds despite the opaque historical last option.
- Quotient L=1: `[A,Z ln(H/L),Z ln(H/L)/n,(Z/(n+1))ln(k/j),(Z/(n+1))(H−L)]`. Wrong-coordinate log bounds and treating the u integral as a constant preserve a full distinctive bank when the lower logarithm vanishes.
- Reciprocal/scaled j=1: `[A,CR/L,CR/H,CR,C(1/L−1/H)(k−j)]`. Omitting the whole u integral and treating the v integral as a constant preserve full distinctiveness when the lower logarithm vanishes.

For explicit parameters without a requested profile, select their eligible complete profile from these declared predicates, before computing the bank. For random calls choose the complete profile first and constrain its parameter slots. Tests check the normal solution at all four original mathematical anchors, changed parameters, all default families and all default profiles. No individual option is replaced after collision detection.
