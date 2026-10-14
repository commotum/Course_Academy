# Four-stage template extraction

Captured provenance matches source.json. Every displayed choice is accounted for below; historical scalar distractor intentions are not claimed recovered.

##1. Specific source descriptions

### q-122474 (sum_difference, moderate)

Determine the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=\frac{y}{{x}^{2}+{y}^{2}}\,i+\frac{x}{{x}^{2}-{y}^{2}}\,j\,.
$$

Number-form anchor: `{"m": 1, "n": 1}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

### q-122657 (log_halfplane, moderate)

Determine the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=\operatorname{ln}⁡(x-y)\,i+\frac{1}{{x}^{2}+{y}^{2}}\,j\,.
$$

Number-form anchor: `{"m": 1, "b": 0}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

### q-122660 (atan_circle_line, moderate)

Determine the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=\operatorname{arctan}⁡(\frac{1}{{x}^{2}+{y}^{2}-4})\,i+\frac{xy}{x-1}\,j\,.
$$

Number-form anchor: `{"r2": 4, "c": 1}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

### q-122663 (log_parabola, moderate)

Determine the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=\operatorname{ln}⁡(x-{y}^{2})\,i+({x}^{2}+{y}^{2}){e}^{1/x}\,j\,.
$$

Number-form anchor: `{"m": 1, "b": 0}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

### q-122518 (open_disk_puncture, hard)

Determine which of the following shaded regions depicts the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=\frac{1}{\sqrt{9-{x}^{2}-{y}^{2}}}\,i+\frac{xy}{{x}^{2}+{y}^{2}}\,j\,.
$$

Number-form anchor: `{"r2": 9}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

### q-122671 (closed_disk_puncture, hard)

Determine which of the following shaded regions depicts the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=\sqrt{1-{x}^{2}-{y}^{2}}\,i+\frac{{e}^{x}}{{x}^{2}+{y}^{2}}\,j\,.
$$

Number-form anchor: `{"r2": 1}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

### q-122710 (rectangle, hard)

Determine which of the following shaded regions depicts the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=y\operatorname{ln}⁡(1-{x}^{2})\,i+x\sqrt{1-|y|}\,j\,.
$$

Number-form anchor: `{"a": 1, "b": 1}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

### q-122677 (half_disk, hard)

Determine which of the following shaded regions depicts the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=\frac{1}{\sqrt{y-x}}\,i+\sqrt{2-{x}^{2}-{y}^{2}}\,j\,.
$$

Number-form anchor: `{"r2": 2, "m": 1}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

### q-122554 (disk_line, hard)

Determine which of the following shaded regions depicts the domain of the vector field $F$ on ${R}^{2},$ given by

$$
F(x,y)=\frac{1}{\sqrt{3-{x}^{2}-{y}^{2}}}\,i+\frac{{x}^{2}+{y}^{2}}{x-y}\,j
$$

Number-form anchor: `{"r2": 3, "m": 1}`. One radio field,5 options. Full solution stages are preserved by complete component/constraint/radius/image masks.

##2. Shared pattern

Find the real domain of both planar component expressions and intersect those domains. Moderate requests a set-builder expression; hard requests a shaded region with correct strict versus nonstrict boundary inclusion. All solutions retain the formal F=P i+Q j row, explicit component row, separate component-rule paragraphs and solved-condition rows, followed by component domains or plots and final intersection. No feedback depends on selected wrong answer.

##3. Component and complete-bank map

### q-122474 / observed:q-122474

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`{(x,y)\in {R}^{2}\,|\,{x}^{2}+{y}^{2}\ge 1}`|opaque outside unit disk|

|1|`{(x,y)\in {R}^{2}\,|\,{x}^{2}+{y}^{2}<1}`|opaque interior unit disk|

|2|`{(x,y)\in {R}^{2}\,|\,y\ne \pm x}`|both factor lines excluded (correct)|

|3|`{(x,y)\in {R}^{2}\,|\,(x,y)\ne 0}`|only common origin excluded|

|4|`{(x,y)\in {R}^{2}\,|\,y\ne x}`|only positive factor line excluded|

Normal method bank sum_difference: ["{(x,y)\\in {R}^{2}\\,|\\,y\\ne \\pm x}", "{(x,y)\\in {R}^{2}\\,|\\,(x,y)\\ne (0,0)}", "{(x,y)\\in {R}^{2}\\,|\\,y\\ne x}", "{(x,y)\\in {R}^{2}\\,|\\,y\\ne -x}", "{(x,y)\\in {R}^{2}\\,|\\,\\text{all real }(x,y)}"].

### q-122657 / observed:q-122657

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`{(x,y)\in {R}^{2}\,|\,x<y}`|reverse logarithmic inequality|

|1|`{(x,y)\in {R}^{2}\,|\,x\ne y}`|replace positive by nonzero|

|2|`{(x,y)\in {R}^{2}\,|\,(x,y)\ne (0,0),\,x\ge y}`|replace strict by nonstrict plus origin excluded|

|3|`{(x,y)\in {R}^{2}\,|\,(x,y)\ne (0,0)}`|only denominator origin excluded|

|4|`{(x,y)\in {R}^{2}\,|\,x>y}`|strict logarithmic inequality (correct)|

Normal method bank log_halfplane: ["{(x,y)\\in {R}^{2}\\,|\\,x>y}", "{(x,y)\\in {R}^{2}\\,|\\,x<y}", "{(x,y)\\in {R}^{2}\\,|\\,x\\ne y}", "{(x,y)\\in {R}^{2}\\,|\\,(x,y)\\ne (0,0),\\,x\\ge y}", "{(x,y)\\in {R}^{2}\\,|\\,(x,y)\\ne (0,0)}"].

### q-122660 / observed:q-122660

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`{(x,y)\in {R}^{2}\,|\,{x}^{2}+{y}^{2}<4,\,x\ne 1}`|replace reciprocal nonzero by positive plus line exclusion|

|1|`{(x,y)\in {R}^{2}\,|\,{x}^{2}+{y}^{2}\ne 4}`|omit separate line exclusion|

|2|`{(x,y)\in {R}^{2}\,|\,{x}^{2}+{y}^{2}\ne 4,\,x\ne 1}`|both denominator exclusions (correct)|

|3|`{(x,y)\in {R}^{2}\,|\,{x}^{2}+{y}^{2}<4}`|replace reciprocal nonzero by positive and omit line|

|4|`{(x,y)\in {R}^{2}\,|\,{x}^{2}+{y}^{2}>4}`|replace reciprocal nonzero by negative and omit line|

Normal method bank atan_circle_line: ["{(x,y)\\in {R}^{2}\\,|\\,{x}^{2}+{y}^{2}\\ne 4,\\,x\\ne 1}", "{(x,y)\\in {R}^{2}\\,|\\,{x}^{2}+{y}^{2}<4,\\,x\\ne 1}", "{(x,y)\\in {R}^{2}\\,|\\,{x}^{2}+{y}^{2}\\ne 4}", "{(x,y)\\in {R}^{2}\\,|\\,{x}^{2}+{y}^{2}<4}", "{(x,y)\\in {R}^{2}\\,|\\,{x}^{2}+{y}^{2}>4}"].

### q-122663 / observed:q-122663

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`{(x,y)\in {R}^{2}\,|\,x<{y}^{2}}`|reverse logarithmic inequality|

|1|`{(x,y)\in {R}^{2}\,|\,x>0}`|omit squared-y term|

|2|`{(x,y)\in {R}^{2}\,|\,x>{y}^{2},\,x\ne 1}`|opaque spurious exclusion x=1|

|3|`{(x,y)\in {R}^{2}\,|\,x>{y}^{2}}`|positive log argument (correct)|

|4|`{(x,y)\in {R}^{2}\,|\,x>{y}^{2},\,x>1}`|opaque spurious restriction x>1|

Normal method bank log_parabola: ["{(x,y)\\in {R}^{2}\\,|\\,x>{y}^{2}}", "{(x,y)\\in {R}^{2}\\,|\\,x<{y}^{2}}", "{(x,y)\\in {R}^{2}\\,|\\,x>0}", "{(x,y)\\in {R}^{2}\\,|\\,x\\ge {y}^{2}}", "{(x,y)\\in {R}^{2}\\,|\\,x>{y}^{2},\\,x>1}"].

### q-122518 / observed:q-122518

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`images/e1/e1d9695fa4da169a7ec9c1f3ff20db320212bce34047fc13bb27028aadc95d79.png`|strict disk minus y=x with redundant origin removal|

|1|`images/30/30462ed1f25749ac4ef05cf9ca9573508ae28a0799d7986dd005f71fdac15679.png`|strict disk minus origin (correct)|

|2|`images/c6/c61552b7b9d8c24e438a8fa2d0a9248a3938c8e3512ca4a012d8b3342dd47a0f.png`|strict disk minus y=x|

|3|`images/23/237dbec35d2ea6556014373efccbf1d34c31404fde3a015feb3c433056c63a3a.png`|closed disk minus origin|

|4|`images/60/606f516cb05ba0922cc63cd672a0df864bea121d9c50982a50d3c6f61465f3bf.png`|closed disk|

Normal method bank open_disk_puncture: same geometric operations except q-122518 index0 becomes strict unpunctured disk.

### q-122671 / observed:q-122671

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`images/4a/4a15607520f8ef05913aab5d1724c8b3158457e56d455b6eb756707263494308.png`|strict disk minus y=x|

|1|`images/26/26709ab7fa3cf1962ff9dca9be510cf5c24f3568f82347a8349e77dc5095fb4c.png`|closed disk|

|2|`images/a3/a3884061e6c5f8b5310a8b0bcf06ac844b12b418497d9f6e5b3beced6147d964.png`|strict disk|

|3|`images/0e/0e6843335d08bc42a95a5801aa683aeb2a043df0cd7edc03ffbc36a9385fee2a.png`|strict disk minus origin|

|4|`images/24/2469abf572b9b6fd9da28ae81951b99acdca9b97275af2bc0a96d3411d7fbea1.png`|closed disk minus origin (correct)|

Normal method bank closed_disk_puncture: same geometric operations except q-122518 index0 becomes strict unpunctured disk.

### q-122710 / observed:q-122710

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`images/11/11cfd599bbfe85c9f3c7a23d5b95c6bd2b3ff199c6c0a4777429123afc74cb8c.png`|closed upper-half rectangle, y in[0,b]|

|1|`images/ff/ff0774689ae7215b624ea7eb3bed8f68a673fba4bcc4ceeb73f82b9081c32d4f.png`|x-open upper-half rectangle, y in[0,b)|

|2|`images/4a/4aeebc183f9a6676f7487fce53ec46ad0f2cc91a87847d8a230471dc638ea448.png`|closed rectangle|

|3|`images/de/de222a9251e08861dd06fdee593cc10557f0be1d2c7d891395512d699b35aa63.png`|x-closed/y-open full rectangle|

|4|`images/49/49000dd6905017bc64c9a67b6d8a2ea475a684477ac6e02d6ed15c4c7dbbb3aa.png`|open x sides and closed y sides (correct)|

Normal method bank rectangle: same geometric operations except q-122518 index0 becomes strict unpunctured disk.

### q-122677 / observed:q-122677

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`images/59/59ec29347dea9437c8217a208bde0a8b200e37fcbce9c223d0358011a0685297.png`|closed upper halfdisk including diameter|

|1|`images/27/27f151bdd3d619de0988b786e6b7517a7f7586844f9a7a35bf651063e7a7dfd1.png`|closed upper halfdisk excluding diameter (correct)|

|2|`images/fa/fadd7ae69d155ebf23586b88369da8f6624b1919942dad543917592f2d3c195c.png`|strict full disk excluding diameter|

|3|`images/cb/cb10aa8f4d930ec7422da7dedfa0650244dceb01afe7cc849ed2bb16ffd3e44d.png`|closed lower halfdisk excluding diameter|

|4|`images/a1/a1ee85bca08b21494e6f1f47de3abcbd71d2d01117795ef91d8ee3e038b36271.png`|closed full disk excluding diameter|

Normal method bank half_disk: same geometric operations except q-122518 index0 becomes strict unpunctured disk.

### q-122554 / observed:q-122554

|Choice index|Exact displayed value|Recipe / interpretation limit|

|---|---|---|

|0|`images/21/2132ac0140fb0b96a876fd04a1069d6922662c72d4d8f4b8880eacae458f8181.png`|strict disk|

|1|`images/fe/fefa684ba6cc6b2e8060c8b0860295177bade694786439317d6cee3d8cf51da8.png`|strict disk excluding opposite-slope diagonal|

|2|`images/55/559ffda45a088810dcaa81628b8767bfedc64ca7f6b7ebd82aebdb2ed4a7ba00.png`|strict disk excluding denominator diagonal (correct)|

|3|`images/45/459b65c41ef9535d55703a64f3c9e4bfe9ffd9263a6a0f5dbf68405fb22c347d.png`|closed disk|

|4|`images/9a/9a20235e26590dbc6ddc5bdaaaa5dd484f5caf02e510bfabf2139ed7add5fa2d.png`|closed disk excluding denominator diagonal|

Normal method bank disk_line: same geometric operations except q-122518 index0 becomes strict unpunctured disk.

##4. Reusable masks, computations, and exclusions

The generator masks complete mathematical components, complete solved constraints, the circle radius phrase, and image slots. It never substitutes short variable letters through prose. Masks are simultaneous longest-first and do not alter newly inserted text. Source parameters replay at anchors with exact prompts, solution strings and every choice value; changed inputs recalculate all constraints, curve features and radius labels. Nonanchor historical images use the same extracted geometric bank recipe.

Normal banks are chosen complete before parameter sampling. Every normal bank is independently checked for five inequivalent domains, one eligible actual displayed-domain answer, and correct UUID designation. Changing ordering or seed leaves question, field and answer identity unchanged when displayed content is fixed. Content identity uses difficulty, version, actual prompt, fixed solution and complete bank; mathematical fingerprint excludes bank/profile/order. The finite parameter spaces are enumerated in validation.

## Source findings and normal repairs

q-122474 states Q numerator y while the prompt numerator is x. Raw exact evidence remains unchanged; normal Q component is corrected to x. This numerator typo does not change domain. Its circle distractors are opaque and stay only in the observed profile; normal bank uses denominator omissions, single-factor omission and ignoring all restrictions.

q-122518 plotted choices0/2 are equivalent wrong sets: deleting the origin after deleting y=x adds no restriction. Raw diagram values and geometry are preserved, flagged evidence-only; normal index0 is the unpunctured strict disk, yielding5 distinct domains. Source correct choice1 is unique.

q-122663 prose before D2 says domain of P; normal says Q. Wrong x!=1/x>1 restrictions have no recoverable displayed-method justification; preserve them in observed evidence, use reversed, omitted-term, nonstrict and overrestricted logarithmic conditions in normal output.

q-122554 second component region label D1 is corrected to D2 normally. q-122671 calls a closed disk its interior; normal says closed disk. q-122710 missing when is a grammar correction. All raw strings remain public exact evidence. None of these prose fixes are reported as raw-exact normal fidelity.

Decoded source mathematical bytes were checked: no doubled backslashes or unintended C0 controls in the source. No blanket TeX normalization was applied. All9 raw source prompts/solutions reproduce exactly; source correct-ref presence is matched separately from value identity. All source question, field and choice attribute-presence sets are checked, with enum objects normalized to enum strings and correct entities normalized to lookup refs as required by local records. Original db IDs in evidence records are provenance, never transaction requests.

Parent normal presentation repair escapes complete outer set braces in solution sets and mathematical options, preserving every inner TeX group and all raw source strings. A normal-output regression rejects invisible unescaped set glyphs; this is recorded separately from mathematical/source-bank reproduction.
