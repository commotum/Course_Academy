# Template extraction

## 1. Specific source descriptions

| ID | Inputs (a,b;n,m;variable,shift) | Layout / source status | Exact source solution profile |
|---|---|---|---|
| q-222016 | 9,3;4,2;y,+7 | spaced blank; unrated; answer and solution absent | absent, not recovered |
| q-76460 | 2,3;2,1;y,−4 | spaced radio; unrated; correct and solution absent | absent, not recovered |
| q-218483 | 7,2;2,5;z,+3 | easy blank, no space after `is` | multiple indices [1,2,4] / [1,2,3,4,5,6,7,12]; no prose comma; part and final periods |
| q-222013 | 5,8;3,4;x,−1 | easy blank, no space after `is` | multiple indices1..8 /1..7; no prose comma; part period, no final period |
| q-222021 | 15,10;3,6;w,+3 | hard blank, no space after `is` | multiple indices1..4 /1..4; prose comma; no part or final period |
| q-222022 | 8,20;9,7;y,−2 | hard blank, no space after `is` | multiple indices1..5 /1..4; prose comma; part period, no final period |
| q-76457 | 10,15;6,4;y,+1 | hard radio, period inside second math span | multiple indices1..4 /1..3; prose comma; part and final periods |

Every polynomial is already factored: c(v+h)^k, a positive integer content and one monic binomial to a positive integer power. n≠m; the bigger power occurs in either input. Source coefficients are positive, shifts signed, answers exact factored polynomials; no answer fragments beyond the whole polynomial are supplied.

## 2. Generalized instructional pattern

Find l=lcm(a,b) and N=max(n,m), then return l(v+h)^N. Integer-content LCM and maximum common-factor exponent are separate decisions. The answer is the positive integer polynomial LCM in Z[v]; arbitrary nonzero scalar multiples are not interchangeable. This is the same method at every level and never calls for introducing another binomial or factoring an expanded polynomial.

## 3. Components and complete banks

Fixed learner prompt families: `The least common multiple of $aB^n$ and $bB^m$ is{{field-1}}.` and `Find the least common multiple of $aB^n$ and $bB^m.$` with source spacing/punctuation profiles. B=(v+h); coefficient1 and exponent1 are suppressed only when the resulting rendered factor remains unambiguous.

Fixed solution sentences are reproduced from the five captured solutions without prose changes. Sequence: common opening → numeric LCM introduction → two multiples lists → numeric LCM equality → maximum-power prose → variable LCM equality → final multiplication sentence → full polynomial LCM / coefficient×factor / answer equality. These are separate unevaluated displayed stages, even where some equality expressions happen to simplify to the same value. q-218483 skips some unlisted intermediate multiples without ellipses; all displayed numbers are genuine multiples and the first common multiple is present. Preserve that exact list evidence; do not silently claim exhaustive enumeration. Normal defaults list consecutive multiples through the LCM and one additional term.

Blank banks: q-218483 14(z+3)^5; q-222013 40(x−1)^4; q-222021 30(w+3)^6; q-222022 40(y−2)^9. The native answer values retain source TeX braces and no math delimiters. q-222016 has no source bank; 9(y+7)^4 is independently derived and appears only in labeled completion or metadata.

Complete observed radio bank `retain_inputs`, q-76460, with L=6,N=2:

| Exact source value | Recipe | Interpretation status |
|---|---|---|
| 6(y - 4)^3 | L B^(n+m) | adds input powers |
| 6(y - 4)^2 | L B^N | mathematical correct value; source designation absent |
| 2(y - 4)^2 | a B^N | retain first coefficient |
| 3(y - 4)^2 | b B^N | retain second coefficient |
| 3(y - 4) | b B^m | retain second input |

Complete observed radio bank `product_power`, q-76457, with L=30,N=6:

| Exact source value | Recipe | Interpretation status |
|---|---|---|
| 30(y+1)^6 | L B^N | captured correct |
| 30(y+1)^10 | L B^(n+m) | adds powers |
| 150(y+1)^10 | ab B^(n+m) | multiplies entire input polynomials |
| 30(y+1)^12 | L B^(2N) | observed twice-max-power pattern; original intent underdetermined |
| 150(y+1)^6 | ab B^N | multiplies contents |

Every option value and every available correct designation is compared one-to-one. Full banks are retained together, never mixed or reduced. The 2N expression is an explicit shape generalization, not proof of recovered author intent. It remains an explicit observed profile; normal defaults use the independently authored method bank.

Authored five-choice default `method_bank`: L B^N (correct), L B^min(n,m), L B^(n+m), gcd(a,b) B^N, L (omitted variable factor). All operations stem from the assessed content/exponent decisions. Bank selection precedes construction; any mathematical duplicate rejects the whole instance. In particular, `retain_inputs` requires the first exponent larger than the second, since otherwise bB^N and bB^m collide. Source profiles with fixed list-position patterns reject changed coefficient pairs if their lists omit the actual integer LCM. No arbitrary numeric perturbations or polynomial interpolation are used.

## 4. Reusable templates, bounds and calculations

Shared parameters: exact integers a,b,n,m,h and variable v∈{x,y,z,w,t}; B=v+h, 1≤|h|≤9, n≠m. Two source layouts with field-owned UUID answers and one worked solution independent of selected distractor. Profiles preserve list indices, binomial/answer spacing and punctuation. Any explicit invalid parameters raise ValueError; sampling rejects complete invalid instances. Profile aliases and shuffle order cannot alter identity when the displayed content is equal.

| Level | Content bounds | Power bounds | Authorship |
|---|---|---|---|
| easy | a,b2..9, unequal, coprime | max2..5, min≥1 | observed workload; radio layout supported by unrated q-76460 |
| moderate | a,b2..18, unequal, gcd>1, max coefficient≥9 | max4..5, min≥2 | missing-level authored definition, canonical/unrated anchor |
| hard | a,b8..24, unequal, shared content, neither divides the other | max6..9, min≥3 | observed workload |

All levels constrain lcm(a,b)≤120, preserving short integer arithmetic. Source originals remain valid under these same guards. Normal binomials remain monic and positive-leading; signed shifts do not change factor-content normalization. Variable aliases and input order are excluded from mathematical fingerprints; full prompt, fixed solution, field kind and complete displayed bank determine presentation identity. Coefficient choices, exponent decisions and signed binomial shifts all influence the actual task.

Additional variation is consciously authored: both layouts at every level and the default complete bank. Moderate is absent in source ratings; no authored instance is presented as observed difficulty evidence. No plotting is needed (steps5/7 documented as none). The validator independently reads displayed prompt expressions and solution stages, checks integer polynomial LCM (not scalar equivalence), formatting, identity and ownership, and uses the native grader for canonical, reordered, split-power, expanded and incorrect scalar submissions.

Source anomalies are missing captured fields only: q-222016 lacks choices/correct/difficulty/solution, q-76460 lacks correct/difficulty/solution. Their raw profiles preserve these omissions; derived profiles supply mathematically verified completions and authored labels. Available five solutions and all14 captured choices replay exactly; missing designations are excluded from designation-match denominators. There are no presentation or mathematical repairs to captured strings.
