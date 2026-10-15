# Four-stage template extraction

## 1. Source-by-source specific observations

### q-10143

Original parameters: `{"a": "7", "b": "0", "c": 1}`. Field radio, family sec_tan.

Calculate the integral $\int \operatorname{sec}⁡(7x)\operatorname{tan}⁡(7x)\,\text{d}x.$

- Answer `00a40602-52d1-5dc9-8e31-c35464767acf`: `$\frac{1}{7}\operatorname{sec}⁡(7x)+C$`; observed correct.

- Answer `3eec2768-c2bf-5731-b512-c6df48d8bb5c`: `$\operatorname{sec}⁡(7x)+C$`; source option.

- Answer `4e578f69-909a-523b-8577-e3cdb3de2088`: `$-7\operatorname{sec}⁡(7x)+C$`; source option.

- Answer `d4240689-1a4e-5384-9ef2-fdfe11a2085d`: `$-\frac{1}{7}\operatorname{sec}⁡(7x)+C$`; source option.

- Answer `e779e3e4-8675-5338-a515-5145e18de6ae`: `$7\operatorname{sec}⁡(7x)+C$`; source option.

### q-10157

Original parameters: `{"a": "8", "b": "0", "c": 1}`. Field radio, family csc_cot.

Calculate the integral $\displaystyle \int\csc (8x)\cot (8x)dx$.

- Answer `f85cf725-3237-5c2c-aa64-a45c7c2a4c32`: `$\csc (8x) + C$`; source option.

- Answer `f8a92f4d-c241-5c04-a633-0e1a6d38dbbd`: `$\frac{1}{8}\csc (8x) + C$`; source option.

- Answer `1639954a-f29a-5655-9185-4c5ede14b2a1`: `$8\csc (8x) + C$`; source option.

- Answer `3f09ad16-8c32-567b-88f6-1ca96ba704c6`: `$-\frac{1}{8}\csc (8x) + C$`; source option.

- Answer `4ff43ea7-a48a-5ab2-b9b1-77d7fc4ac4c2`: `$-8\csc (8x) + C$`; source option.

### q-113983

Original parameters: `{"a": "1", "b": "0", "c": 1, "d": 1}`. Field radio, family poly_sec.

Calculate the integral $\int ({sec}^{2}⁡x+1)\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x.$

- Answer `33da3ed1-1777-5bf4-8cfc-9e5a29ccb4c8`: `$\frac{{tan}^{3}⁡x}{3}+\operatorname{tan}⁡x+C$`; source option.

- Answer `62494273-c0c0-5f7f-8ebb-533f7f201a63`: `$\frac{{sec}^{2}⁡x}{2}+C$`; source option.

- Answer `89765658-5c5b-5edc-a80e-0d5330eacbc6`: `$\frac{{sec}^{3}⁡x}{3}+\operatorname{sec}⁡x+C$`; observed correct.

- Answer `8df579a6-b4b7-59be-810b-4b8fd64e8efe`: `$\frac{{sec}^{3}⁡x}{3}+C$`; source option.

- Answer `ce4aa2aa-cecd-5b62-ae9a-109027768536`: `$\frac{{tan}^{3}⁡x}{3}+\operatorname{sec}⁡x+C$`; source option.

### q-2203

Original parameters: `{"a": "10", "b": "0", "c": 1}`. Field radio, family sec_tan.

$\int \operatorname{sec}⁡(10x)\operatorname{tan}⁡(10x)\,\text{d}x=$

- Answer `5c351233-a918-5f2c-867c-b36c3e634b45`: `$10\operatorname{sec}⁡(10x)+C$`; source option.

- Answer `6387ca6c-9af3-5305-93ac-6ba215b43157`: `$\frac{1}{10}\operatorname{csc}⁡(10x)+C$`; source option.

- Answer `6c47091c-3dbb-514d-926c-70024a19ee8c`: `${sec}^{2}⁡(10x)+C$`; source option.

- Answer `9c25054c-c830-5cdc-9739-35307de9de4d`: `$\frac{1}{10}\operatorname{sec}⁡x+C$`; source option.

- Answer `a683964a-9c75-50e4-b041-7650006dc260`: `$\frac{1}{10}\operatorname{sec}⁡(10x)+C$`; observed correct.

### q-13663

Original parameters: `{"a": "3", "b": "0", "c": 2, "hi": "1/2", "lo": "1/3"}`. Field radio, family csc2.

Evaluate the integral ${\int }_{\pi /9}^{\pi /6}2{csc}^{2}⁡(3x)\,\text{d}x.$

- Answer `519b8fb0-5928-5ec9-8613-12c9d1306f72`: `$-\frac{\sqrt{3}}{2}$`; source option.

- Answer `60890db1-c6f4-5143-9b9a-ae422da31c9c`: `$2\sqrt{3}$`; source option.

- Answer `87157abc-6212-562b-a343-90c57626ecf4`: `$-\frac{2\sqrt{3}}{3}$`; source option.

- Answer `8b99c65a-2714-56e5-af5f-38d5a8ea0940`: `$\frac{2\sqrt{3}}{9}$`; observed correct.

- Answer `919ec147-de01-530b-97cb-da754894b913`: `$\frac{\sqrt{3}}{3}$`; source option.

### q-355818

Original parameters: `{"a": "5", "b": "0", "c": 5, "hi": "1/2", "lo": "1/4"}`. Field blank, family csc2.

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /20}^{\pi /10}5{csc}^{2}⁡(5x)\,\text{d}x=$
{{field-1}}

- Answer `bde6a22f-af92-5d05-a00e-ee43025b38b1`: `$1$`; observed correct.

### q-346368

Original parameters: `{"a": "1/4", "b": "0", "c": 1, "hi": "1/2", "lo": "1/6"}`. Field blank, family csc_cot.

Evaluate the following integral. Do not round the answer.

${\int }_{2\pi /3}^{2\pi }\operatorname{csc}⁡(\frac{x}{4})\operatorname{cot}⁡(\frac{x}{4})\,\text{d}x=$
{{field-1}}

- Answer `5eb82788-efbe-50de-b226-6bde5d6aedf2`: `$4$`; observed correct.

### q-350060

Original parameters: `{"a": "1", "b": "-1/4", "c": 3, "hi": "0", "lo": "-1/4"}`. Field blank, family sec2.

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /4}3{sec}^{2}⁡(x-\frac{\pi }{4})\,\text{d}x=$
{{field-1}}

- Answer `c9793ffe-67cc-5645-9b00-c140cc88e2aa`: `$3$`; observed correct.

### q-350071

Original parameters: `{"a": "1", "b": "-1/6", "c": 4, "hi": "1/2", "lo": "1/6"}`. Field blank, family csc_cot.

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /3}^{2\pi /3}4\operatorname{csc}⁡(x-\frac{\pi }{6})\operatorname{cot}⁡(x-\frac{\pi }{6})\,\text{d}x=$
{{field-1}}

- Answer `85c49c8e-61d5-5e58-a395-01a4e606b7d6`: `$4$`; observed correct.

### q-10578

Original parameters: `{"a": "1", "b": "-1/3", "c": 1, "hi": "1/6", "lo": "-1/3"}`. Field radio, family sec_tan.

${\int }_{0}^{\pi /2}\operatorname{sec}⁡(x-\frac{\pi }{3})\operatorname{tan}⁡(x-\frac{\pi }{3})\,\text{d}x=$

- Answer `02192a18-96df-5c9c-86d1-fd39f10cc96d`: `$\frac{2\sqrt{3}}{3}-2$`; observed correct.

- Answer `258b40a9-d7f7-5e38-ab76-8707b1a1a9b7`: `$-\frac{2\sqrt{3}}{3}-1$`; source option.

- Answer `59c2d43f-3033-53cf-a498-afe18808b478`: `$\sqrt{3}-1$`; source option.

- Answer `605c38a6-bd94-5054-abeb-196bc585d8b9`: `$-2\sqrt{3}+1$`; source option.

- Answer `f513628d-4c08-512b-85ac-0d46df6f115b`: `$\frac{\sqrt{3}}{3}+2$`; source option.

## 2. Shared mathematical and instructional backbone

Use one substitution u=ax+bπ (with the incompatible sec(x) source analyzed only as reference evidence), derive du/dx and dx, transform definite limits where supplied, apply a reciprocal-trig primitive, evaluate or substitute back. Answer fields retain the original radio/blank contract and five/single answer counts. Source-specific omitted rows remain omitted. The full served prose and ordered rows are assembled in core(), never returned from raw JSON. The nonlinear reference profile is restricted to its original coefficients and requires explicit template=q-113983, profile=observed; its eligible_for_learning flag is false.

## 3. Complete component and bank mapping

For linear primitives write r=c/a, z=ax, F=sec(z) or csc(z). q-10143 bank is [rF, cF, -caF, -rF, caF]+C with first correct; q-10157 is [cF,rF,caF,-rF,-caF]+C with fourth independently completed correct. q-2203 is [ca sec(z), r csc(z), c sec²(z), r sec(x), r sec(z)]+C with last correct. The unscaled-argument option is a complete argument mistake and changes independently when a changes.

For q-113983 bank is [c tan³(x)/3+d tan(x), c sec²(x)/2, c sec³(x)/3+d sec(x), c sec³(x)/3, c tan³(x)/3+d sec(x)]+C, with third correct. Every primitive bank is compared modulo arbitrary integration constants by differentiating all pairs, including wrong/wrong pairs.

For q-13663 let D=cot(lo)-cot(hi). Bank [-aD/c, caD, -cD, cD/a, D] has fourth correct. These reproduce all five options, including the compound reciprocal/sign coefficient; inferred error intent is not claimed. Entire colliding banks (e.g. c=a) are rejected, never thinned or patched.

For q-10578 observed profile write L=sec(lo), H=sec(hi). Complete bank r[H-L, -H-L/2, cot(hi)-L/2, -L cot(hi)+L/2, tan(hi)+L], first correct. These are empirical endpoint-expression patterns, and their original cognitive interpretation is unresolved. The endpoint multiplier1/2 is retained explicitly, not fitted polynomially. Source-profile variants remain public for faithful replay; normal method banks use [r(H-L), -r(H-L), r(H+L), rH, r(tan(hi)-tan(lo))], all interpretable endpoint/sign/function mistakes. Review preserves this distinction; authored banks are never counted as recovered source banks.

Blank answers are the complete evaluated definite integral, with no C or distractors. The key is c/a[P(hi)-P(lo)], with P=sec,-csc,tan,-cot for sec*tan,csc*cot,sec²,csc². All dependent lower/upper x endpoints are (angle-bπ)/a. For the ordinary linear families, the two table rows, all formal integral operands, differentials, signed primitive endpoints and final value derive from the same instance.

## 4. Stable slots, constraints and dependencies

All numerical slots are exact reduced rational strings a,b, integer c. The nonlinear reference fixes a=1,b=0,c=d=1 and admits no variable slots. x and u are fixed variable roles. Source-specific trig targets remain fixed because their complete banks and primitive stages depend on them; across templates all four reciprocal primitive targets occur. c1..6 (easy1..5); easy a2..10,b0; moderate a2..6,b0; reciprocal hard a1/2,1/3,1/4,b0; shifted hard a1..4,b in ±1/6,±1/4,±1/3. Hard shifts remain nonzero and reciprocal scales remain nonintegral. Every public explicit-parameter call enforces these same bounds and the complete bank constraint.

Endpoint pairs are a finite three-pair catalog per family, listed explicitly in ENDPOINTS. This limits familiar-angle arithmetic and connected real domains, while giving coefficient, scale, shift and endpoint variation without extra operators or reasoning stages. No poles may lie in the interval: sec-based transformed intervals lie inside (-π/2,π/2), csc-based intervals inside (0,π). No negative/inverted interval or improper integral is admitted. Counts use canonical printed integrand and actual x bounds; source IDs, profiles, seed, shuffling and C are excluded.

### Source errors and presentation repairs

q-10157 lacks an original key, solution and rating: all supplied values are explicitly authored completion, not matched missing evidence. q-10143 answer captures contain doubled command slashes in actual decoded strings; raw bytes remain source.json, while served choices are normalized bare TeX. The canonical e-465 correctly factors the coefficient5 in its first row; it is contextual evidence and is not counted as practice fidelity. No other practice mathematics is repaired. Exact-answer blanks retain 'Do not round the answer.' in observed replay; normal wording 'Give an exact answer.' preserves intent and avoids the grader's format-sensitive round detection. This wording repair is separate from mathematical fidelity.

