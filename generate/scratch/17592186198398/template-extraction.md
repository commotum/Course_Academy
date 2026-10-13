# Four-stage extraction

## 1. Describe every source specifically

`raw-recipes.json` records every complete prompt slot, answer atom, shared solution prefix and ordered arithmetic node with its source ID; `source.json` preserves all original attributes and UUID provenance. The following exact coordinates, bounds and densities account for all seven sources.

| Family | Given inverse coordinates | Box Δ | Transformed f before Jacobian | Forward signed determinant |
|---|---|---|---|---|
| power | u=3x−2y, v=y+2z, w=z | u:[0,3], v:[0,2], w:[0,1/2] | u²v | 3 |
| vcosu | u=x²+y, v=x+z, w=z | u:[π/6,π/2], v:[0,2], w:[−1,1] | v cos u | −1 |
| ucosv | u=x²+2y, v=x−z, w=z | u:[0,2], v:[0,π/2], w:[−1,1] | u cos v | −2 |
| sum | u=(2x−y)/2, v=y/2, w=z/3 | u:[0,1], v:[0,2], w:[0,1] | u+w | 1/6 |
| exp | u=x+y², v=y+z, w=2z | u:[0,3], v:[0,1], w:[0,8] | v e^u | 2 |
| zcosu | u=2x+3y, v=−2x+z, w=z/2 | u:[π/6,2π], v:[0,1], w:[0,3] | 4w² cos u | 3 |
| sinsin | u=x²+2y, v=x−2z, w=4z | u:[π/2,π], v:[π,2π], w:[0,4] | sin v sin u | −8 |

The legacy power source's last region relation is `0≤2z≤1` although w=z; the actual w upper bound is 1/2, not 1. The other legacy source has a negative z lower bound. Those printed inequalities are parsed independently during replay QA. Quadratic x² is a shear, not a root-inversion demand: x=v−dw/c is determined uniquely by the linear coordinate, then y=(u−x²)/b. No positivity-of-x assumption or principal square root is used.

The five complete worked solutions begin with transformation T and inverse T⁻¹ notation, state the full change-of-variables formula, then numbered domain/Jacobian/inverse-Jacobian/change steps. The Jacobian step displays all nine formal entries, then the numeric matrix. Quadratic/linear coupled rows expand the third-row cofactor and 2×2 minor; triangular rows use the diagonal product. Step 4 in sum has 11 RHS arithmetic nodes: substituted density → iterated integral → w primitive → w endpoint substitution → collection → v primitive → v endpoint factor → distribution → u primitive → u endpoint substitution → collected scalar. The other four worked solutions use separated products of primitive integrals, then endpoint arithmetic and final collection. The exact node counts are stored in recipe evidence and checked by complete string equality on every replay. The malformed ucosv endpoint closing parenthesis remains raw-only.

## 2. Generalized family descriptions

Evaluate a supplied-coordinate change over a region defined by those coordinates. Identify the resulting rectangular box, compute the determinant of the supplied inverse map, reciprocate and take absolute value, substitute the displayed density, and evaluate elementary one-variable primitives to give one exact scalar. Families differ only in the source-shaped density/shear and the source arithmetic mask, not in skill. All normal records preserve the single `selection` radio with five complete scalar answers.

## 3. Components and complete bank accounting

Every source choice belongs to its sole source field and explicit `raw-<DB-ID>` profile. Here k is a new actual integrand coefficient, k∈{−6,…,−1,1,…,6}. The public recipe uses k times EACH displayed source atom, and k times EACH actual ordered integration RHS. This is an evidence-only parameterized family: scaling the integrand scales the integral. It does not claim recovered distractor intentions or that historical numbers generalize into defensible learner errors.

| Profile suffix | Complete ordered atoms (each multiplied by k) | Observed correct atom |
|---|---|---|
| 17592186198623 | 3; −2; 4; 2; 1 | absent (3 inferred independently) |
| 17592186198964 | 2; 2√3; ln 2/4; √2; ln 2 | absent (2 inferred independently) |
| 17592186374090 | 2/3; 3; 1/2; 2; 5 | 2 |
| 17592186374097 | 12; 10; 15; 8; 7 | 12 |
| 17592186374125 | √2(e³−2); 2e³; e³−1; 4(e³−2); 2(e³−1) | 2(e³−1) |
| 17592186374132 | 9; −2/3; 1/6; −6; −1/9 | −6 |
| 17592186374139 | −8; −1/2; −1/4; −1; −2 | −1 |

All 35 choices, seven complete banks and five existing designations are retained, including exact original string spellings. The raw original no-correct designation cases do not count as matched correct designations. Source profiles have `evidence_only=true` and `eligible_for_learning=false`, even if their mathematics/format happens to be valid.

Normal banks are **authored**. They share the correct computed scalar I and two Jacobian-method errors: integrate f without inverse |J|; integrate f with forward |D| rather than reciprocal. The remaining TWO required recipes are chosen together by family before parameters:

| Family | Fourth complete value operation | Fifth complete value operation |
|---|---|---|
| power, moderate/hard | omit primitive denominator n+1 | omit primitive denominator 2 for v |
| power, easy | omit primitive denominator 2 for u | use original z bounds without w=c z scaling |
| vcosu | replace the cosine primitive by its derivative −sin, then integrate the wrong density | omit primitive denominator 2 for v |
| ucosv | omit primitive denominator 2 for u | replace the cosine primitive by its derivative −sin, then integrate the wrong density |
| sum | drop the u summand before integration | drop the w summand before integration |
| exp | omit the lower e^u primitive endpoint | omit primitive denominator 2 for v |
| zcosu | substitute z² as w², omitting 1/c² | omit primitive denominator 3 for w² |
| sinsin | use original z bounds without w=c z scaling | reverse one −cos endpoint difference |

The derivative-error densities are exact operation definitions rather than asserted source mistakes. Learner options show only mathematical values; the source has no option-specific diagnoses, and none are invented. Any collision of COMPLETE evaluated scalar integrals, invalid number or equal wrong/correct value rejects the WHOLE five-choice instance. No first-valid option pool or coefficient perturbation is used. A single method bank per family/level is selected before sampling, and no raw bank participates in default sampling.

## 4. Reusable masks and constraints

Normal mathematical parameters are a,b,c,d,n, lu,hu,lv,hv,lz,hz. Shears:

- power: u=ax+by, v=y+dz, w=cz, f=u^n v;
- vcosu/ucosv/sinsin: u=x²+by, v=x+dz, w=cz;
- sum: u=x−y/b, v=y/b, w=cz, f=u+w;
- exp: u=x+y², v=y+dz, w=cz, f=v e^u;
- zcosu: u=ax+by, v=dx+z, w=cz, f=(w/c)² cos u.

The displayed integrand is derived by substituting these actual coordinates into f. Its region is formed with u/v inequalities and a z interval. Δ is [lu,hu]×[lv,hv]×[c lz,c hz]. Every map has a constant nonzero signed determinant; c>0, so the ordered w bounds preserve orientation. All nine partial derivatives and the third-row cofactor are computed from the map, rather than copied from a source. The weight is always 1/|D|, including negative determinants.

Signed a,b,d are nonzero integers of magnitude at most 4 (quadratic b positive). Integer c is 2,3,4 for most families; sum uses c=1/2,1/3,1/4. Bounds are ordered integers −1…6 on nontrig axes, familiar 0,π/6,π/3,π/2,π,3π/2,2π on trig axes, with upper exponential endpoint at most 3. Easy adds a stricter coefficient/endpoint ceiling and n=1, all zero lower endpoints; moderate/hard power keeps n=2. Moderate always has at least one zero lower endpoint. Hard always has three positive lower endpoints and no vanishing lower primitive values. These are authored supported number forms, not inferred original author code. Fixed parameters are rejected if they fail any level or whole-bank guard.

Normal solutions keep the source common prose, formal transformation formula, box/Jacobian/inverse/change steps. The integration block is an explicitly authored expansion into successive w/v/u primitives. Each primitive is printed first, then its INDIVIDUAL endpoint substitutions, then individually evaluated signed components, then collection. The solution is fixed independently of the chosen wrong answer. Negative terms are grouped in every unevaluated arithmetic component. Rendering never collapses the component masks into repeated final rows.

Raw masks use complete mathematical components, never broad replacement of short numbers or coordinate letters. Their only parameter is k: they preserve the supplied transforms, bounds, bank shape, absent attributes and exact stage count. At k=1 normal coefficient formatting omits an unnecessary factor, giving exact reproduction through the same recipe; k≠1 scales the full mathematical component. This limited replay parameterization is disclosed and is not counted toward normal meaningful variety. Normal parameter fingerprints use the actual supplied coordinates, transformed f and bounds; they exclude unused metadata, seeds, raw/profile spelling and answer banks. Content identities use actual prompt, complete bank, correct designation, fixed solution and level/presence. Option order does not affect identity.

Steps 5 and 7: plot extraction/specification is **none**. No graphical asset is needed or created. The generator stops before database preparation.

The default finite domains contain **21,699** mathematically different eligible tasks after whole-bank collisions are removed, excluding raw replay scales and unused a/b/n metadata. Exact per-family/level counts and closed-form counting derivations are in `domain-counts.json`. They include 5,184 easy power tasks; moderate counts 3,888/972/324/225/216/3,024/108 and hard counts 2,592/972/648/162/144/3,024/216 in the listed family order. These are default sampler counts, not a claim about all wider explicit inputs; the validation report separately reports actual sampled unique tasks. Collision eliminations are 18 equal sum contributions at moderate, c=2 for exponential banks, and b|d|=c for z²-cosine banks. These counts are derived from the real transformed maps and bounds, not random seeds or bank aliases.
