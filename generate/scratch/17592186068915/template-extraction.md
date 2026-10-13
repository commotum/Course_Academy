# Template extraction

General pattern: substitute u=b*x+c, divide dx by nonzero b, integrate sine/cosine, restore the original variable or transform both definite bounds. Return a complete antiderivative including C or an exact definite scalar. Preserve each source field key, field shape, bank count and supplied solution. No inferred misconception feedback is presented.

Policy extension: for positive integer k in 1..12, transport the entire source problem by x -> k*x, original bounds -> bounds/k and every primitive/scalar bank value -> its transported value/k. This deliberately narrow transport policy is mathematical and reproducible; it does not claim unobserved conceptual distractor recipes. Positive k preserves endpoint order. Original parameters occur at k=1. Source signed slope -9, positive shift 3, pi/3 shift, pi/4 slope, amplitudes 1,5,9 and variable z are all retained. Arbitrary amplitudes, shifts and negative dilations are outside this version.

All numerical source components are preserved in source.json; source.edn retains exact typed IDs and refs. Each mapping below binds the complete bank, not pooled distractors.

## q-13647

${\int }_{0}^{\pi /8}5\operatorname{sin}⁡(4x)\,\text{d}x=$

Parameters: {'function': 'sin', 'amplitude': '5', 'slope': '4', 'shift': '0', 'lower': '0', 'upper': 'pi/8'}. Field selection (:answer-field.type/radio); plot none.

Fixed sequence: u substitution and dx factor; definite bound table when applicable; transformed integral; trig antiderivative; exact endpoint evaluation or back substitution. Exact supplied solution retained at k=1; variant notation uses one aligned block. q-2204 completion is explicit authored content.

- Option 1: `0`; recipe `(0).subs(x,k*x)/k`; source owned answer 201f04d6-c002-5e0e-95fe-a7bfb6f3cd47; correct=False.

- Option 2: `\frac{5}{4}`; recipe `(5/4).subs(x,k*x)/k`; source owned answer 4017a737-6567-579a-8f02-98712b431a35; correct=True.

- Option 3: `-\frac{5}{4}`; recipe `(-5/4).subs(x,k*x)/k`; source owned answer 928bb7be-da0b-5934-b68c-38f79005663e; correct=False.

- Option 4: `1`; recipe `(1).subs(x,k*x)/k`; source owned answer 932c94aa-6652-5204-910b-18fdb3861f29; correct=False.

- Option 5: `-1`; recipe `(-1).subs(x,k*x)/k`; source owned answer 99faa052-1151-586c-8bf2-0746b9af0da9; correct=False.

## q-2204

Calculate $\displaystyle \int\sin (5z)dz$.

Parameters: {'function': 'sin', 'amplitude': '1', 'slope': '5', 'shift': '0', 'lower': 'None', 'upper': 'None'}. Field selection (:answer-field.type/radio); plot none.

Fixed sequence: u substitution and dx factor; definite bound table when applicable; transformed integral; trig antiderivative; exact endpoint evaluation or back substitution. Exact supplied solution retained at k=1; variant notation uses one aligned block. q-2204 completion is explicit authored content.

- Option 1: `\cos (5z) + C`; recipe `(cos(5*x)).subs(x,k*x)/k + arbitrary C`; source owned answer de554e76-bfb8-5794-8ac9-2f13ece1fe32; correct=False.

- Option 2: `-\frac{1}{5}\cos (5z) + C`; recipe `(-cos(5*x)/5).subs(x,k*x)/k + arbitrary C`; source owned answer 3ad0e19c-1edb-590f-84f6-b82f05ab0eb0; correct=True.

- Option 3: `\frac{1}{5}\cos (5z) + C`; recipe `(cos(5*x)/5).subs(x,k*x)/k + arbitrary C`; source owned answer 549694b4-3d4c-5ce6-b583-5bfbafb96c9e; correct=False.

- Option 4: `-\frac{1}{5}\cos z + C`; recipe `(-cos(x)/5).subs(x,k*x)/k + arbitrary C`; source owned answer 5bbd1242-9e22-532a-8510-3e3cfc73a9c4; correct=False.

- Option 5: `5\cos (5z) + C`; recipe `(5*cos(5*x)).subs(x,k*x)/k + arbitrary C`; source owned answer 7113dc9f-2a7d-5f89-8a51-d7a03e51b01b; correct=False.

## q-10061

Calculate $\int \operatorname{sin}⁡(2x)\,\text{d}x.$

Parameters: {'function': 'sin', 'amplitude': '1', 'slope': '2', 'shift': '0', 'lower': 'None', 'upper': 'None'}. Field selection (:answer-field.type/radio); plot none.

Fixed sequence: u substitution and dx factor; definite bound table when applicable; transformed integral; trig antiderivative; exact endpoint evaluation or back substitution. Exact supplied solution retained at k=1; variant notation uses one aligned block. q-2204 completion is explicit authored content.

- Option 1: `\frac{1}{2}\operatorname{cos}⁡(2x)+C`; recipe `(cos(2*x)/2).subs(x,k*x)/k + arbitrary C`; source owned answer 048c6daa-e4e3-5179-98af-42d15424d793; correct=False.

- Option 2: `-2\operatorname{cos}⁡(2x)+C`; recipe `(-2*cos(2*x)).subs(x,k*x)/k + arbitrary C`; source owned answer 4efd5467-419e-5ebc-874e-357ea2d654e0; correct=False.

- Option 3: `2\operatorname{cos}⁡(2x)+C`; recipe `(2*cos(2*x)).subs(x,k*x)/k + arbitrary C`; source owned answer 5ca35220-86d9-5bb2-9102-bb7998d7eaae; correct=False.

- Option 4: `-\frac{1}{2}\operatorname{sin}⁡(2x)+C`; recipe `(-sin(2*x)/2).subs(x,k*x)/k + arbitrary C`; source owned answer 6b961eed-5742-57eb-946f-3d09fa13cffa; correct=False.

- Option 5: `-\frac{1}{2}\operatorname{cos}⁡(2x)+C`; recipe `(-cos(2*x)/2).subs(x,k*x)/k + arbitrary C`; source owned answer 8c2ddb72-e009-5e99-a867-cfb791c5ece6; correct=True.

## q-10064

Calculate $\int \operatorname{cos}⁡(3-9x)\,\text{d}x.$

Parameters: {'function': 'cos', 'amplitude': '1', 'slope': '-9', 'shift': '3', 'lower': 'None', 'upper': 'None'}. Field selection (:answer-field.type/radio); plot none.

Fixed sequence: u substitution and dx factor; definite bound table when applicable; transformed integral; trig antiderivative; exact endpoint evaluation or back substitution. Exact supplied solution retained at k=1; variant notation uses one aligned block. q-2204 completion is explicit authored content.

- Option 1: `-\frac{1}{3}\operatorname{sin}⁡(3-9x)+C`; recipe `(sin(9*x - 3)/3).subs(x,k*x)/k + arbitrary C`; source owned answer 04550c7b-0d73-5442-a8c7-725dcd4c73b5; correct=False.

- Option 2: `-\frac{1}{9}\operatorname{sin}⁡(3-9x)+C`; recipe `(sin(9*x - 3)/9).subs(x,k*x)/k + arbitrary C`; source owned answer 15ecb00b-13f7-5f52-9f60-143f66c29fe7; correct=True.

- Option 3: `\frac{1}{9}\operatorname{cos}⁡(3-9x)+C`; recipe `(cos(9*x - 3)/9).subs(x,k*x)/k + arbitrary C`; source owned answer beed3300-67b6-5a62-834b-6d15671e04c3; correct=False.

- Option 4: `\frac{1}{9}\operatorname{sin}⁡(3-9x)+C`; recipe `(-sin(9*x - 3)/9).subs(x,k*x)/k + arbitrary C`; source owned answer eeddc196-9f5f-51b9-8377-d64ab696355d; correct=False.

- Option 5: `-\frac{1}{9}\operatorname{cos}⁡(3-9x)+C`; recipe `(-cos(9*x - 3)/9).subs(x,k*x)/k + arbitrary C`; source owned answer fa1174cf-350f-52d8-a72f-f4777b151d43; correct=False.

## q-346081

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{2}\operatorname{cos}⁡(\frac{\pi x}{4})\,\text{d}x=$
{{field-1}}

Parameters: {'function': 'cos', 'amplitude': '1', 'slope': 'pi/4', 'shift': '0', 'lower': '0', 'upper': '2'}. Field field-1 (:answer-field.type/blank); plot none.

Fixed sequence: u substitution and dx factor; definite bound table when applicable; transformed integral; trig antiderivative; exact endpoint evaluation or back substitution. Exact supplied solution retained at k=1; variant notation uses one aligned block. q-2204 completion is explicit authored content.

- Option 1: `\frac{4}{\pi }`; recipe `(4/pi).subs(x,k*x)/k`; source owned answer 2aace116-779e-5cd7-87fe-2a773103e41b; correct=True.

## q-350040

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /4}9\operatorname{sin}⁡(2x)\,\text{d}x=$

{{field-1}}

Parameters: {'function': 'sin', 'amplitude': '9', 'slope': '2', 'shift': '0', 'lower': '0', 'upper': 'pi/4'}. Field field-1 (:answer-field.type/blank); plot none.

Fixed sequence: u substitution and dx factor; definite bound table when applicable; transformed integral; trig antiderivative; exact endpoint evaluation or back substitution. Exact supplied solution retained at k=1; variant notation uses one aligned block. q-2204 completion is explicit authored content.

- Option 1: `\frac{9}{2}`; recipe `(9/2).subs(x,k*x)/k`; source owned answer eadacb51-45df-579b-815c-4ee743a75466; correct=True.

## q-10574

Calculate ${\int }_{0}^{\pi /9}\operatorname{sin}⁡(3x+\frac{\pi }{3})\,\text{d}x.$

Parameters: {'function': 'sin', 'amplitude': '1', 'slope': '3', 'shift': 'pi/3', 'lower': '0', 'upper': 'pi/9'}. Field selection (:answer-field.type/radio); plot none.

Fixed sequence: u substitution and dx factor; definite bound table when applicable; transformed integral; trig antiderivative; exact endpoint evaluation or back substitution. Exact supplied solution retained at k=1; variant notation uses one aligned block. q-2204 completion is explicit authored content.

- Option 1: `\frac{1}{2}`; recipe `(1/2).subs(x,k*x)/k`; source owned answer 027cbe6b-cc9e-5232-a368-f7d9b5981f38; correct=False.

- Option 2: `\frac{1}{3}`; recipe `(1/3).subs(x,k*x)/k`; source owned answer 4952b9e8-bbdc-5ebd-87ec-3e2a8e0abe98; correct=True.

- Option 3: `\frac{2}{3}`; recipe `(2/3).subs(x,k*x)/k`; source owned answer c99d3fe5-21ad-5042-83f6-cbfa8e3c7e98; correct=False.

- Option 4: `\frac{1}{6}`; recipe `(1/6).subs(x,k*x)/k`; source owned answer d0f5b679-6496-55a2-9c95-8d9e7d1b6239; correct=False.

- Option 5: `\frac{3}{2}`; recipe `(3/2).subs(x,k*x)/k`; source owned answer d6fa740d-7171-561d-a05a-6cdf9a71c7c4; correct=False.
