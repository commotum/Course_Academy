# Template extraction

Provenance and scope are in classification.md; all raw data is retained in source.json. No plots occur in source prompts, choices or solutions.

## Stage 1: specific source descriptions

### q-218516

The least common multiple of the polynomials $4{u}^{3}(v-2)^{2}$ and $5u(v-2)^{5}$ is{{field-1}}.

Contents a=4, b=5; factors u+(0) and v+(-2); exponent pairs (3,2) and (1,5). Field: factored_blank; captured difficulty: :question.difficulty/easy.

Complete observed values:

- `20{u}^{3}(v-2)^{5}` (captured correct)

12 shared paragraphs and three formal/reduction equalities; listing all multiples through the first common multiple plus one more multiple.

### q-76246

Find the least common multiple of the polynomials $4(x + 3)^{2}(y - 1)^{3}$ and $10(x + 3)^{2}(y - 1)$.

Contents a=4, b=10; factors x+(3) and y+(-1); exponent pairs (2,3) and (2,1). Field: factored_radio; captured difficulty: missing.

Complete observed values:

- `20(x + 3)^{4}(y - 1)^{4}`

- `20(x + 3)^{2}(y - 1)^{3}`

- `40(x + 3)^{2}(y - 1)^{3}`

- `40(x + 3)^{4}(y - 1)^{4}`

- `20(x + 3)^{3}(y - 1)^{2}`

No captured solution or correct reference. Its original choice ordering differs from Pull order; order-independent full-bank comparison is required.

### q-111597

Find the least common multiple of the polynomials $4(z+2)^{2}(w-5)^{2}$ and $7(z+2)^{3}(w-5)^{4}.$

Contents a=4, b=7; factors z+(2) and w+(-5); exponent pairs (2,2) and (3,4). Field: factored_radio; captured difficulty: :question.difficulty/easy.

Complete observed values:

- `42(z+2)^{2}(w-5)^{4}`

- `28(z+2)^{4}(w-5)^{6}`

- `28(z+2)^{3}(w-5)^{4}` (captured correct)

- `28(z+2)^{2}(w-5)^{4}`

- `42(z+2)^{2}(w-5)^{5}`

12 shared paragraphs and three formal/reduction equalities; listing all multiples through the first common multiple plus one more multiple.

### q-222107

The least common multiple of the polynomials $3(x-3)^{3}(y+1)$ and $5(x-3)(y+1)^{2}$ is{{field-1}}.

Contents a=3, b=5; factors x+(-3) and y+(1); exponent pairs (3,1) and (1,2). Field: factored_blank; captured difficulty: :question.difficulty/easy.

Complete observed values:

- `15(x-3)^{3}(y+1)^{2}` (captured correct)

12 shared paragraphs and three formal/reduction equalities; listing all multiples through the first common multiple plus one more multiple.

### q-222113

The least common multiple of the polynomials $9(y-2)^{5}(z+1)^{3}$ and $15(y-2)^{2}(z+1)^{6}$ is{{field-1}}.

Contents a=9, b=15; factors y+(-2) and z+(1); exponent pairs (5,3) and (2,6). Field: factored_blank; captured difficulty: :question.difficulty/moderate.

Complete observed values:

- `45(y-2)^{5}(z+1)^{6}` (captured correct)

12 shared paragraphs and three formal/reduction equalities; listing all multiples through the first common multiple plus one more multiple.

### q-222116

The least common multiple of the polynomials $12{z}^{6}(w-7)^{3}$ and $20{z}^{5}(w-7)^{4}$ is{{field-1}}.

Contents a=12, b=20; factors z+(0) and w+(-7); exponent pairs (6,3) and (5,4). Field: factored_blank; captured difficulty: :question.difficulty/moderate.

Complete observed values:

- `60{z}^{6}(w-7)^{4}` (captured correct)

12 shared paragraphs and three formal/reduction equalities; listing all multiples through the first common multiple plus one more multiple.

## Stage 2: generalized mathematical description

Given two already factored products a F^p G^q and b F^r G^s, where F=v+h and G=w+k use independent variables, compute the normalized integer-polynomial LCM l F^E G^H, with l=lcm(a,b), E=max(p,r), H=max(q,s). Return the complete product as a blank or select it among five complete products. Two bases are already visible, so no factorization is assessed.

## Stage 3: component and whole-bank map

All choices belong to the single source field (`field-1` for blanks or `selection` for radio). A blank singleton uses (l,E,H). For q-76246, complete pattern bank in captured EDB order is:

| Source value | Parameterized recipe | Interpretation |
|---|---|---|
|20(x+3)^4(y-1)^4|(l,p+r,q+s)|summed powers|
|20(x+3)^2(y-1)^3|(l,E,H)|correct; key missing, independently derived|
|40(x+3)^2(y-1)^3|(ab,E,H)|product contents|
|40(x+3)^4(y-1)^4|(ab,p+r,q+s)|combined product/sum|
|20(x+3)^3(y-1)^2|(l,H,E)|swapped maxima|

For q-111597 the complete captured bank is:

| Source value | Parameterized expression pattern | Interpretation limits |
|---|---|---|
|42(z+2)^2(w-5)^4|(3l/2,min(p,r),H)|3/2 coefficient intent unresolved|
|28(z+2)^4(w-5)^6|(l,2p,q+s)|doubled first input exponent intent unresolved; summed second|
|28(z+2)^3(w-5)^4|(l,E,H)|captured correct|
|28(z+2)^2(w-5)^4|(l,min(p,r),H)|lower first power|
|42(z+2)^2(w-5)^5|(3l/2,min(p,r),H+1)|compound observed pattern intent unresolved|

The 3/2-content patterns are explicit replay profiles requiring even l; they do not imply recovered wrong arithmetic. The doubled-first-power is one honest generalized expression pattern, not a claimed recovered misconception. The whole bank is rejected on collision. They are excluded from normal default generation but remain available and are tested under genuinely changed content/exponents, e.g. a5/b6, (2,1)/(3,4), l30.

Normal authored method_bank, selected as a complete unit: correct(l,E,H); minimum exponents(l,min(p,r),min(q,s)); wrong numerical gcd(gcd(a,b),E,H); summed exponents(l,p+r,q+s); swapped maxima(l,H,E). All choices are constructed before uniqueness checks. Thus equal maxima cannot produce a swapped-maxima radio, while the same mathematics is still eligible for a blank. No option diagnosis is shown to the learner.

## Stage 4: reusable Markdown and value template

Fixed prompt families:
- Blank: `The least common multiple of the polynomials $aF^pG^q$ and $bF^rG^s$ is{{field-1}}.`
- Radio: `Find the least common multiple of the polynomials $aF^pG^q$ and $bF^rG^s$.`

Fixed worked solution: (1) complete shared opening rule; (2) numeric formal LCM instruction; (3,4) complete ordered multiples lists ending one multiple after l; (5) numeric equality; (6) formal variable products and named bases; (7,8) each pair and its maximum; (9) raise both bases; (10) variable formal LCM equals separately displayed powers joined by cdot; (11) final multiply sentence; (12) full input-polynomial LCM equals l times both maximum powers. These are the original full common stages and sentences, not a collapsed CAS result.

Variable slots are complete bases, powers, products, numbers and lists. Do not replace variable-letter substrings in prose. Conditional slots: h=0 displays bare v, but its nonunit power displays `{v}^{n}`; shifted factors display parentheses; exponent1 omitted; sign chosen from integer shift; q-76246 spaces inside bases; q-111597 period inside final prompt math and solution; other blanks omit final solution period. Exact source punctuation is preserved. Normal outputs use a final period.

Each source uses the same fully parameterized recipe. `observed_q-*` retains raw omissions, while `completed_q-*` supplies q-76246's independently verified key, authored moderate level and common solution. No literal source payload return, answer lookup, extra stage or diagnosis. Explicit calls enforce all level bounds; invalid input raises instead of silently resampling. Random generation selects a complete bank first and retries the entire instance.

Sampling guards and authored difficulty rationale are in classification.md and the generator's separate level sections. Level membership is mathematical workload, never a progression. Native grading validates canonical, expanded and unreduced equivalent blank entries plus wrong integer content, negative associates, larger scalar multiple, and wrong polynomial. Whole radio values and intermediate stages are independently validated before grading. Blank values contain complete normalized products, without delimiters. Outer keys remain plain; inner schema keys remain colon-prefixed. Stable field-owned UUIDs depend on actual content, with bank and order-independent solution identity separated from the canonical mathematical fingerprint.

No plots: step5/7 are inapplicable; no source image references exist and no renderer is needed.


Native full-expansion restriction: the real parser enforces4096 bytes/512 tokens. Oversized fully expanded equivalent submissions are explicitly expected unresolved with the exact limit documented; canonical, shorter partially expanded and unreduced quotient equivalents are checked as accepted. Wrong content uses a compact factored quotient, avoiding accidental parser limits. No math/input requirement is weakened.
