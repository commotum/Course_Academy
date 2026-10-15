# Template extraction

## 1. Specific source observations

### q-10061

Observed slots `{"a": "2", "b": "0", "c": 1}`.

Calculate $\int \operatorname{sin}⁡(2x)\,\text{d}x.$

If we let $u=2x,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \operatorname{sin}⁡(2x)\,\text{d}x & =\int \operatorname{sin}⁡u\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int \operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{1}{2}\operatorname{cos}⁡u+C \\  & =-\frac{1}{2}\operatorname{cos}⁡(2x)+C\end{aligned}\end{aligned}
$$

- Field `selection`, answer `048c6daa-e4e3-5179-98af-42d15424d793`: `$\frac{1}{2}\operatorname{cos}⁡(2x)+C$`.

- Field `selection`, answer `4efd5467-419e-5ebc-874e-357ea2d654e0`: `$-2\operatorname{cos}⁡(2x)+C$`.

- Field `selection`, answer `5ca35220-86d9-5bb2-9102-bb7998d7eaae`: `$2\operatorname{cos}⁡(2x)+C$`.

- Field `selection`, answer `6b961eed-5742-57eb-946f-3d09fa13cffa`: `$-\frac{1}{2}\operatorname{sin}⁡(2x)+C$`.

- Field `selection`, answer `8c2ddb72-e009-5e99-a867-cfb791c5ece6`: `$-\frac{1}{2}\operatorname{cos}⁡(2x)+C$` (observed correct).

### q-2204

Observed slots `{"a": "5", "b": "0", "c": 1}`.

Calculate $\displaystyle \int\sin (5z)dz$.

Original solution missing; not matched.

- Field `selection`, answer `de554e76-bfb8-5794-8ac9-2f13ece1fe32`: `$\cos (5z) + C$`.

- Field `selection`, answer `3ad0e19c-1edb-590f-84f6-b82f05ab0eb0`: `$-\frac{1}{5}\cos (5z) + C$`.

- Field `selection`, answer `549694b4-3d4c-5ce6-b583-5bfbafb96c9e`: `$\frac{1}{5}\cos (5z) + C$`.

- Field `selection`, answer `5bbd1242-9e22-532a-8510-3e3cfc73a9c4`: `$-\frac{1}{5}\cos z + C$`.

- Field `selection`, answer `7113dc9f-2a7d-5f89-8a51-d7a03e51b01b`: `$5\cos (5z) + C$`.

### q-10064

Observed slots `{"a": "-9", "b": "3", "c": 1}`.

Calculate $\int \operatorname{cos}⁡(3-9x)\,\text{d}x.$

If we let $u=3-9x,$ then 

$$
\frac{\text{d}u}{\text{d}x}=-9\,⟹\,\text{d}x=-\frac{1}{9}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \operatorname{cos}⁡(3-9x)\,\text{d}x & =\int \operatorname{cos}⁡u\cdot (-\frac{1}{9}\,\text{d}u) \\  & =-\frac{1}{9}\int \operatorname{cos}⁡u\,\text{d}u \\  & =-\frac{1}{9}\operatorname{sin}⁡u+C \\  & =-\frac{1}{9}\operatorname{sin}⁡(3-9x)+C\end{aligned}
$$

- Field `selection`, answer `04550c7b-0d73-5442-a8c7-725dcd4c73b5`: `$-\frac{1}{3}\operatorname{sin}⁡(3-9x)+C$`.

- Field `selection`, answer `15ecb00b-13f7-5f52-9f60-143f66c29fe7`: `$-\frac{1}{9}\operatorname{sin}⁡(3-9x)+C$` (observed correct).

- Field `selection`, answer `beed3300-67b6-5a62-834b-6d15671e04c3`: `$\frac{1}{9}\operatorname{cos}⁡(3-9x)+C$`.

- Field `selection`, answer `eeddc196-9f5f-51b9-8377-d64ab696355d`: `$\frac{1}{9}\operatorname{sin}⁡(3-9x)+C$`.

- Field `selection`, answer `fa1174cf-350f-52d8-a72f-f4777b151d43`: `$-\frac{1}{9}\operatorname{cos}⁡(3-9x)+C$`.

### q-350040

Observed slots `{"a": "2", "b": "0", "c": 9, "hi": "1/2", "lo": "0"}`.

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /4}9\operatorname{sin}⁡(2x)\,\text{d}x=$

{{field-1}}

If we let $u=2x,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /4$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\pi /4}9\operatorname{sin}⁡(2x)\,\text{d}x & ={\int }_{0}^{\pi /2}9\operatorname{sin}⁡u\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{9}{2}{\int }_{0}^{\pi /2}\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{9}{2}\operatorname{cos}⁡u{|}_{0}^{\pi /2} \\  & =-\frac{9}{2}(\operatorname{cos}⁡(\frac{\pi }{2})-\operatorname{cos}⁡(0)) \\  & =-\frac{9}{2}(0-1) \\  & =\frac{9}{2}\end{aligned}
$$

- Field `field-1`, answer `eadacb51-45df-579b-815c-4ee743a75466`: `$\frac{9}{2}$` (observed correct).

### q-13647

Observed slots `{"a": "4", "b": "0", "c": 5, "hi": "1/2", "lo": "0"}`.

${\int }_{0}^{\pi /8}5\operatorname{sin}⁡(4x)\,\text{d}x=$

If we let $u=4x,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /8$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /8}5\operatorname{sin}⁡(4x)\,\text{d}x & ={\int }_{0}^{\pi /2}5\operatorname{sin}⁡u\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{5}{4}{\int }_{0}^{\pi /2}\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{5}{4}\operatorname{cos}⁡u{|}_{0}^{\pi /2} \\  & =-\frac{5}{4}(\operatorname{cos}⁡(\frac{\pi }{2})-\operatorname{cos}⁡(0)) \\  & =-\frac{5}{4}(0-1) \\  & =\frac{5}{4}\end{aligned}\end{aligned}
$$

- Field `selection`, answer `201f04d6-c002-5e0e-95fe-a7bfb6f3cd47`: `$0$`.

- Field `selection`, answer `4017a737-6567-579a-8f02-98712b431a35`: `$\frac{5}{4}$` (observed correct).

- Field `selection`, answer `928bb7be-da0b-5934-b68c-38f79005663e`: `$-\frac{5}{4}$`.

- Field `selection`, answer `932c94aa-6652-5204-910b-18fdb3861f29`: `$1$`.

- Field `selection`, answer `99faa052-1151-586c-8bf2-0746b9af0da9`: `$-1$`.

### q-346081

Observed slots `{"a": "1/4", "b": "0", "c": 1, "hi": "1/2", "lo": "0"}`.

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{2}\operatorname{cos}⁡(\frac{\pi x}{4})\,\text{d}x=$
{{field-1}}

If we let $u=\frac{\pi x}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{\pi }{4}\,⟹\,\text{d}x=\frac{4}{\pi }\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /2$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{2}\operatorname{cos}⁡(\frac{\pi x}{4})\,\text{d}x & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡u\cdot \frac{4}{\pi }\,\text{d}u \\  & =\frac{4}{\pi }{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\,\text{d}u \\  & =\frac{4}{\pi }\operatorname{sin}⁡u\,{|}_{0}^{\pi /2} \\  & =\frac{4}{\pi }(\operatorname{sin}⁡(\frac{\pi }{2})-\operatorname{sin}⁡(0)) \\  & =\frac{4}{\pi }(1-0) \\  & =\frac{4}{\pi }\end{aligned}
$$

- Field `field-1`, answer `2aace116-779e-5cd7-87fe-2a773103e41b`: `$\frac{4}{\pi }$` (observed correct).

### q-10574

Observed slots `{"a": "3", "b": "1/3", "c": 1, "hi": "2/3", "lo": "1/3"}`.

Calculate ${\int }_{0}^{\pi /9}\operatorname{sin}⁡(3x+\frac{\pi }{3})\,\text{d}x.$

If we let $u=3x+\frac{\pi }{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /9$ |
| --- | --- | --- |
| $u$ | $\pi /3$ | $2\pi /3$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /9}\operatorname{sin}⁡(3x+\frac{\pi }{3})\,\text{d}x & ={\int }_{\pi /3}^{2\pi /3}\operatorname{sin}⁡u\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{1}{3}{\int }_{\pi /3}^{2\pi /3}\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{1}{3}\operatorname{cos}⁡u{|}_{\pi /3}^{2\pi /3} \\  & =-\frac{1}{3}(\operatorname{cos}⁡(\frac{2\pi }{3})-\operatorname{cos}⁡(\frac{\pi }{3})) \\  & =-\frac{1}{3}(-\frac{1}{2}-\frac{1}{2}) \\  & =\frac{1}{3}\end{aligned}\end{aligned}
$$

- Field `selection`, answer `027cbe6b-cc9e-5232-a368-f7d9b5981f38`: `$\frac{1}{2}$`.

- Field `selection`, answer `4952b9e8-bbdc-5ebd-87ec-3e2a8e0abe98`: `$\frac{1}{3}$` (observed correct).

- Field `selection`, answer `c99d3fe5-21ad-5042-83f6-cbfa8e3c7e98`: `$\frac{2}{3}$`.

- Field `selection`, answer `d0f5b679-6496-55a2-9c95-8d9e7d1b6239`: `$\frac{1}{6}$`.

- Field `selection`, answer `d6fa740d-7171-561d-a05a-6cdf9a71c7c4`: `$\frac{3}{2}$`.

## 2. Generalized backbone

Compute one real affine argument u=ax+b, its nonzero constant derivative, and solved dx; substitute into the sine/cosine integral, extract c/a, integrate, and substitute back for indefinite integrals. For definite integrals, transform both bounds, then use six ordered rows: substituted integral, factored integral, primitive evaluation bar, explicit endpoint trig expressions, individually evaluated endpoint constants, final result. Source prompts, variable roles, field type and key, and complete source banks remain fixed by template. Every served row is parameterized; raw JSON is evidence only, never a returned worked solution.

## 3. Complete component/bank recipe mapping

Let z=ax+b, c the amplitude, r=c/a. All indefinite values include arbitrary +C and compare modulo constants.

- q10061: [r cos(z), -ca cos(z), ca cos(z), -r sin(z), -r cos(z)] +C, last correct. These are sign, scale and primitive-function mistakes.
- q2204: [c cos(z), -r cos(z), r cos(z), -r cos(x), ca cos(z)] +C, second independently completed correct. Variable is z in the served question, with x above denoting its variable role. The fourth omits the argument scale; it is not a stale variable.
- q10064: [-c/b sin(z), r sin(z), -r cos(z), -r sin(z), r cos(z)] +C, second correct. The first divides by the constant shift instead of slope. This is an empirical expression recipe with inferred error intent; b stays positive, never equals -a, so complete bank members remain distinct.
- q13647: [0,V,-V,1,-1], V=c/a[cos(lo)-cos(hi)], second correct. Cases V in {0,1,-1} reject the entire five-option bank. Literal 0 and ±1 are observed bank components, not fabricated coefficient transport.
- q10574 and authored-hard: [cD/2,V,2V,V/2,caD/2], where D=cos(lo)-cos(hi), V=cD/a, second correct. Observed empirical scale patterns generalize the complete [1/2,1/3,2/3,1/6,3/2] bank at a3,c1,D1; cognitive explanations are not claimed. Any pairwise equivalence rejects the entire bank, never replacing a choice.
- q350040 and q346081 blank: one exact evaluated value, no C, no distractors. Their original keys field-1 and selection for radios persist.

All source choices map one-to-one at original parameters. q2204's missing original designation is reported as authored, never source fidelity. Raw doubled command slashes in answer captures and nested aligned environments are retained in raw evidence but normalized in served content. These are presentation repairs, no mathematical correction. No source wrong/wrong duplicate was found at original parameters; every sampled bank is checked pairwise modulo C.

## 4. Explicit finite slots and dependencies

Parameters use reduced rational strings a,b,lo,hi and strict builtin integer c (bool rejected). a is the slope except q346081, whose slope is a*pi. b is an ordinary constant for indefinite templates and b*pi for definite templates. lo,hi are transformed endpoint angles divided by pi. Actual x bounds are (lo*pi-b)/a with actual slope and shift substituted, so each table, formal operand and endpoint expression derives from one instance.

q10061/q2204: a2..10,b0,c1..4. q10064: a=-10..-4,b1..4,c1..4. Positive shift remains nonzero, negative slope remains negative. q350040/q13647: a2..6,b0,c2..9. q346081: a in 1/2,1/3,1/4,1/5; b0,c1..4. q10574/authored-hard: a2..6,b in ±1/3,±1/6;c1..4. Definite endpoint pairs are exactly ENDPOINTS in the script: three familiar pairs per source. They change endpoint arithmetic without introducing new operations. All are ordered, finite, and sine/cosine have no real poles, so the unique real component is all of R. Public explicit-parameter calls enforce exactly this full finite domain, with no wider hidden acceptance.

The family/function/variable/field/count/stage sequence is fixed because changing it changes observed banks or response contracts. Numerical amplitude, scale, shift and eligible familiar endpoint pairs vary within this defined backbone. Distinctness uses the actual integrand and x bounds; templates, prose, answer order, seed, profile and arbitrary constants do not create practice novelty. Metadata carries seed, parameters, selected complete bank, version and frozen basis. Option shuffling uses an independent RNG; content identities do not depend on seed or option order.

Exact-answer wording is preserved for profile=observed. Normal method blanks use Give an exact answer, since the unchanged native grader interprets Do not round as a restrictive format policy. This authored wording repair retains the response shape and exactness; source wording fidelity is validated separately. Unknown/incomplete source references remain source-cases and raw evidence. q2204 observed replay is explicitly evidence_only and ineligible_for_learning; its ordinary completed profile is eligible and carries authored-completion metadata. Complete source profiles and all mathematically valid scoped pi outputs remain eligible: native comparison gaps do not justify excluding valid tasks. Three wrong submissions of 1 against 4/pi, 2sqrt(3)/pi and 3/pi are unresolved by the unchanged native grader, with per-case evidence separate from malformed notation.

