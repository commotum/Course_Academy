# Template extraction

## Stage1 — specific source records

All originals are preserved verbatim in source.json and rendered with their complete banks in review.md. No inferred distractor label is shown to learners.

### q-20058

Find $b\cdot (c\times a)$, if $-a\cdot (3b\times (-2c))=24.$

Family scalar; requested vector order bca; field radio; original parameters `{"factors": ["-1", "3", "-2"], "rhs": "24"}`.

Worked solution has 2 row separators and 3 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-20062

Find $c\cdot (b\times a)$, if $b\times c=⟨2,3,0⟩$ and $a=⟨1,-2,2⟩.$

Family vector; requested vector order cba; field radio; original parameters `{"w": [2, 3, 0], "v": [1, -2, 2]}`.

Worked solution has 3 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-128352

Find $c\cdot (a\times b),$ if $a\cdot ((-3b)\times (-7c))=7.$

Family scalar; requested vector order cab; field radio; original parameters `{"factors": ["1", "-3", "-7"], "rhs": "7"}`.

Worked solution has 2 row separators and 3 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-128353

Find $b\cdot (a\times c),$ if $b\times c=⟨2,5,1⟩$ and $a=⟨6,1,-9⟩.$

Family vector; requested vector order bac; field radio; original parameters `{"w": [2, 5, 1], "v": [6, 1, -9]}`.

Worked solution has 3 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-128356

Find $c\cdot (b\times a),$ if $b\times c=⟨6,-1,3⟩$ and $a=⟨3,5,-4⟩.$

Family vector; requested vector order cba; field radio; original parameters `{"w": [6, -1, 3], "v": [3, 5, -4]}`.

Worked solution has 3 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-18658

Find $b\cdot (a\times c)$, if $4a\cdot (-b\times c)=12.$

Family scalar; requested vector order bac; field radio; original parameters `{"factors": ["4", "-1", "1"], "rhs": "12"}`.

Worked solution has 2 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-20057

Find $b\cdot (a\times c)$, if $3a\cdot (2b\times (-c))=8.$

Family scalar; requested vector order bac; field radio; original parameters `{"factors": ["3", "2", "-1"], "rhs": "8"}`.

Worked solution has 2 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-20059

Find $c\cdot (a\times b)$, if $3a\cdot (\sqrt{2}b\times 3c)=18\sqrt{2}.$

Family scalar; requested vector order cab; field radio; original parameters `{"factors": ["3", "sqrt(2)", "3"], "rhs": "18*sqrt(2)"}`.

Worked solution has 2 row separators and 3 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-20061

Find $c\cdot (b\times a)$, if $3a\cdot (6b\times c)=90.$

Family scalar; requested vector order cba; field radio; original parameters `{"factors": ["3", "6", "1"], "rhs": "90"}`.

Worked solution has 2 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-317343

Find $b\cdot (c\times a),$ if $b\times c=⟨4,-1,6⟩$ and $a=⟨2,3,-1⟩.$

$b\cdot (c\times a)=$
{{field-1}}

Family vector; requested vector order bca; field blank; original parameters `{"w": [4, -1, 6], "v": [2, 3, -1]}`.

Worked solution has 3 row separators and 3 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-73470

Find $c\cdot (b\times a)$, if $b\times c=⟨3,-1,2⟩$ and $a=⟨4,-2,6⟩.$

Family vector; requested vector order cba; field radio; original parameters `{"w": [3, -1, 2], "v": [4, -2, 6]}`.

Worked solution has 3 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-128349

Find $c\cdot (b\times a),$ if $2a\cdot ((-3b)\times c)=10.$

Family scalar; requested vector order cba; field radio; original parameters `{"factors": ["2", "-3", "1"], "rhs": "10"}`.

Worked solution has 2 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-317332

Find $a\cdot (c\times b)$, if $-3a\cdot ((-2b)\times (7c))=168.$

$a\cdot (c\times b)=$
{{field-1}}

Family scalar; requested vector order acb; field blank; original parameters `{"factors": ["-3", "-2", "7"], "rhs": "168"}`.

Worked solution has 3 row separators and 2 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-128355

Find $c\cdot (a\times b),$ if $b\times c=⟨4,3,-5⟩$ and $a=⟨-2,8,2⟩.$

Family vector; requested vector order cab; field radio; original parameters `{"w": [4, 3, -5], "v": [-2, 8, 2]}`.

Worked solution has 3 row separators and 3 display blocks. Exact original prose/stage sequence is replay-asserted.

### q-317329

Find $b\cdot (c\times a)$, if $-5a\cdot ((6b)\times (4c))=120.$

$b\cdot (c\times a)=$
{{field-1}}

Family scalar; requested vector order bca; field blank; original parameters `{"factors": ["-5", "6", "4"], "rhs": "120"}`.

Worked solution has 3 row separators and 3 display blocks. Exact original prose/stage sequence is replay-asserted.

## Stage2 — shared pattern

Recover a·(b×c) by factoring the supplied scalar coefficients or taking the dot product of a supplied cross product and supplied vector. Exchange exactly two vectors per source step to reach the requested order; each exchange reverses the scalar. Return one scalar, radio or blank. No cross product or determinant is computed.

## Stage3 — complete component/bank mapping

The complete original prompt/components and explicit normal parameters are in source-cases.json. For public historical bank generalization, let h=T/T₀ where T is the reconstructed base triple product and T₀ its captured original. Each scalar historical option x₀ maps to h·x₀; a historical vector option maps componentwise. This is an **opaque complete-bank homothety**, a documented numerical evidence extension, not recovery of an original error algorithm. These profiles are evidence-only and ineligible for learning. Every listed mapping exactly reproduces its source at h=1. Blank mappings are the correctly derived scalar rather than an error bank.

### q-20058 — observed:q-20058

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `8` | no | opaque homothety h·(8) |

| selection | `-4` | no | opaque homothety h·(-4) |

| selection | `4` | yes | derived correct |

| selection | `6` | no | opaque homothety h·(6) |

| selection | `-6` | no | opaque homothety h·(-6) |

### q-20062 — observed:q-20062

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `-4` | no | opaque homothety h·(-4) |

| selection | `4` | yes | derived correct |

| selection | `-6` | no | opaque homothety h·(-6) |

| selection | `⟨1,0,3⟩` | no | opaque homothety h·(⟨1,0,3⟩) |

| selection | `6` | no | opaque homothety h·(6) |

### q-128352 — observed:q-128352

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `7` | no | opaque homothety h·(7) |

| selection | `3` | no | opaque homothety h·(3) |

| selection | `-\frac{1}{3}` | no | opaque homothety h·(-\frac{1}{3}) |

| selection | `\frac{1}{3}` | yes | derived correct |

| selection | `-3` | no | opaque homothety h·(-3) |

### q-128353 — observed:q-128353

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `-8` | yes | derived correct |

| selection | `-2` | no | opaque homothety h·(-2) |

| selection | `2` | no | opaque homothety h·(2) |

| selection | `-6` | no | opaque homothety h·(-6) |

| selection | `8` | no | opaque homothety h·(8) |

### q-128356 — observed:q-128356

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `1` | no | opaque homothety h·(1) |

| selection | `-2` | no | opaque homothety h·(-2) |

| selection | `-3` | no | opaque homothety h·(-3) |

| selection | `2` | no | opaque homothety h·(2) |

| selection | `-1` | yes | derived correct |

### q-18658 — observed:q-18658

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `-3` | no | opaque homothety h·(-3) |

| selection | `12` | no | opaque homothety h·(12) |

| selection | `-4` | no | opaque homothety h·(-4) |

| selection | `4` | no | opaque homothety h·(4) |

| selection | `3` | yes | derived correct |

### q-20057 — observed:q-20057

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `-\frac{4}{3}` | no | opaque homothety h·(-\frac{4}{3}) |

| selection | `\frac{4}{3}` | yes | derived correct |

| selection | `\frac{8}{3}` | no | opaque homothety h·(\frac{8}{3}) |

| selection | `\frac{3}{4}` | no | opaque homothety h·(\frac{3}{4}) |

| selection | `-\frac{3}{4}` | no | opaque homothety h·(-\frac{3}{4}) |

### q-20059 — observed:q-20059

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `4` | no | opaque homothety h·(4) |

| selection | `2\sqrt{2}` | no | opaque homothety h·(2\sqrt{2}) |

| selection | `3\sqrt{2}` | no | opaque homothety h·(3\sqrt{2}) |

| selection | `\sqrt{2}` | no | opaque homothety h·(\sqrt{2}) |

| selection | `2` | yes | derived correct |

### q-20061 — observed:q-20061

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `6` | no | opaque homothety h·(6) |

| selection | `5` | no | opaque homothety h·(5) |

| selection | `18` | no | opaque homothety h·(18) |

| selection | `-5` | yes | derived correct |

| selection | `4` | no | opaque homothety h·(4) |

### q-317343 — observed:q-317343

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| field-1 | `-1` | yes | derived correct |

### q-73470 — observed:q-73470

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `-26` | yes | derived correct |

| selection | `-24` | no | opaque homothety h·(-24) |

| selection | `-28` | no | opaque homothety h·(-28) |

| selection | `26` | no | opaque homothety h·(26) |

| selection | `24` | no | opaque homothety h·(24) |

### q-128349 — observed:q-128349

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `-\frac{5}{3}` | no | opaque homothety h·(-\frac{5}{3}) |

| selection | `\frac{3}{5}` | no | opaque homothety h·(\frac{3}{5}) |

| selection | `-\frac{3}{5}` | no | opaque homothety h·(-\frac{3}{5}) |

| selection | `\frac{5}{3}` | yes | derived correct |

| selection | `5` | no | opaque homothety h·(5) |

### q-317332 — observed:q-317332

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| field-1 | `-4` | yes | derived correct |

### q-128355 — observed:q-128355

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| selection | `26` | no | opaque homothety h·(26) |

| selection | `6` | yes | derived correct |

| selection | `-22` | no | opaque homothety h·(-22) |

| selection | `22` | no | opaque homothety h·(22) |

| selection | `-6` | no | opaque homothety h·(-6) |

### q-317329 — observed:q-317329

| Source field | Exact source value | Correct? | Public evidence recipe |

|---|---|---|---|

| field-1 | `-1` | yes | derived correct |

### Authored normal complete banks

Scalar moderate banks: correct q; −q (miss the exchange parity); sR (omit all supplied coefficients); qf₁ (omit first nonunit supplied coefficient); qfₖ (omit last nonunit coefficient). Here s is requested permutation sign and R is the actual supplied RHS. If coefficients repeat or equal −1 and cause equality, the **whole** bank/instance is rejected; no replacement pool is used.

Supplied-vector radio banks: sΣtᵢ; −sΣtᵢ; and s(Σtᵢ−t₁), s(Σtᵢ−t₂), s(Σtᵢ−t₃), where each tᵢ is the actual printed supplied dot component. Zero/repeated components or accidental equality reject the complete bank. Supplied-vector blanks need only the correct value.

Easy banks: q; −q; sR; −sR; sfR. These correspond to missed parity, omitted supplied scalar (with/without parity), and multiplication instead of division. Factor magnitude≥2 makes the five values distinct for nonzero base.

Hard banks: q; −q; sT; sTu; sTv, where u,v are the two actual requested factors. They represent missed parity and omission of both/first/last requested factor. u=v or other equality rejects the whole bank.

## Stage4 — reusable masks and constraints

Source templates slot complete given triples, supplied vector tuples, the complete first aligned block’s factoring/dot operands and final numeric RHSs in swap blocks. Source equation punctuation, common prose, line counts, collected coefficient rows, field keys and placeholders stay fixed. The first factored row is built from the actual supplied factors; dot substitution uses all three printed products before the evaluated sum. Later swap values are determined by the actual printed vector order. Raw complete TeX components group negative products; no blind digit/short-letter replacement occurs.

Easy/hard add the documented same-method scopes in classification. Hard additionally factors the requested product, substitutes its signed scalar and evaluates it in three distinct operative rows. Normal identity includes actual displayed prompt, full fixed solution, complete bank and level; mathematical task fingerprint excludes seed, bank, profile and presentation mask aliases, retaining supplied factor/coordinate operands, requested order and requested factors.

No source-format attributes were absent and no source prose/TeX mathematical repairs are needed. Decoded source fraction values begin with character codes 92,102,114,97 (one slash then fra); JSON escaping is not a doubled-slash defect. q-20062’s vector distractor is a preserved scalar-response-shape anomaly; default generation replaces the entire historical bank with the separately labeled authored five-scalar operation bank.

No plots are present; steps 5/7 require no plot specification, renderer, image assets or cache.
