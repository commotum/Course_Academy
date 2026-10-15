# Four-stage extraction

## 1. Describe each original

`source.json` retains the complete prompt, all attributes, each ordered worked chain, every choice, raw UUID and correct designation where present. `source-bank-mapping.json` below supplies a per-answer inventory rather than replacing the immutable source with a summary. All functions have inner argument x; every question asks for the first derivative. There are no trigonometric chain-rule inner functions.

| Family | Original expression; answer shape | Ordered stages |
| --- | --- | --- |
| q-1892 | -2sin x + sec x -3tan x +11x; entire derivative radio | solution absent, normal authored termwise differentiation |
| q-31280 | 3sec x -3; entire derivative radio | solution absent, normal authored formalD, differentiate terms, remove zero |
| q-1883 | 3/x² +cos x -3sec x; fieldless | formal derivative in negative powers, power multiplication, collect, reciprocal notation |
| q-1938 | sec x/(4x); fieldless | formalD, substituted quotient rule, expanded numerator, extract common coefficient, cancel coefficient |
| q-337182 | 3sec x/(5x²); blank x tan x -2 inside supplied prefactor | formalD, quotient factors, expand products, factor5x sec, cancel one5x, extract3 |
| q-104325 | 3sec x/e^x; entire derivative radio | formalD, substituted quotient rule, factor3e^x sec, cancel exponential |
| q-105314 | 5^x sec x; entire derivative radio | formalD, expanded product derivative, factor common product |
| q-105316 | 3sin x +sec x; entire derivative radio | formalD, termwise derivative |
| q-340608 | 2sec x -4^x; blank secant derivative term only | formalD, termwise derivative |
| q-340611 | e^x sec x; blank inside factored derivative | formalD, expanded product derivative, factor common product |
| q-340620 | 4sec x +e^x at0; scalar blank1 | formalD, derivative; substitute0 symbolically, substitute arguments, evaluate trig/exponential factors, collect |

## 2. Shared pattern and purpose

Apply d(sec x)/dx=sec x tan x inside the source's existing sum, product or quotient. Maintain each family's arithmetic and factoring workload, complete derivative versus supplied-fragment contract, and fixed solution sequence. A family is a presentation/operation structure, not a distinct new mathematical skill. Equal-level instances have unordered coefficient/base choices and no progression.

## 3. Component and choice inventory

`source-bank-mapping.json` maps every original answer, full raw record, field and key, original parameters, profile, exact value and parameterized operation pattern. The renderer operates on immutable source strings with whole numeric math tokens, protecting all exponents and leaving field keys/prose untouched. This is a bounded algebraic reconstruction of displayed operations, not a claim to possess MA's original randomizer.

q-1892 bank has sec→csc², wrong sine sign, unchanged sine, and tan→csc² errors. q-31280 includes negative derivative, retained constant, omitted coefficient and sec·cot. q-105314 includes omitted ln(base), sign flips, and omitted exponential-derivative product. q-105316's `3tan x` and q-104325's `sec x(3-tan x)` do not establish a defensible author intention; their COMPLETE historical banks remain public bounded evidence profiles, explicitly ineligible. Normal q-105316 uses both term sign mistakes, both wrong signs, and omitted sec derivative; normal q-104325 uses quotient plus sign, omitted denominator derivative, missed exponential cancellation, and reversed quotient subtraction. No bank is pooled or filled with first-valid values; a whole collision rejects an instance.

Missing original correct designations count as missing, not matched. Mathematical normal completions infer q-1892's `sec x tan x -2cos x -3sec²x +11` and q-31280's `3sec x tan x`; each follows independently from the actual displayed prompt. Missing solutions receive the minimal termwise chains described above. Fieldless originals receive a normal blank expecting the whole derivative. The raw absence of each attribute survives public observed replay.

## 4. Reusable backbone and slots

The ordered chain and all function arguments/orders stay fixed. `a` replaces the original coefficient(s) with all dependent arithmetic updated; q-1892 varies2, q-31280 varies both appearances of3, q-1883 varies both source3 coefficients and derivative6, q-1938 varies denominator4 and its square16, q-337182 varies numerator3 and denominator5 with dependent6,10,15,25,30, q-104325 varies numerator3, q-105316 varies sine3. q-105314 varies the base5 and its logarithm together. q-340608 varies secant coefficient2 and exponential base4. q-340611 varies exponential base e to e or2..9; its first product derivative includes ln(base), and factored fragment is ln(base)+tan x. That product workload is already observed in q-105314. q-340620 varies secant coefficient4 and the exponential coefficient1, keeping argumentx and endpoint0; zero is never excluded and a correct1 is allowed.

The shared explicit/sampler finite domains are published by `domain`: single coefficients2..9; q-337182 and q-340608 numerator/sec coefficient1..6 and denominator/base2..6; q-340611 base e or2..9; hard two coefficients1..6. These bounds keep small positive integer arithmetic, the same derivative rules, and the same operative rows. Source anchors are included. Booleans, floats, unknown keys and out-of-domain explicit parameters are rejected. Parameters that collapse a required complete bank are rejected as a whole, with no valid replacement option selected afterward.

Real domain: exclude all secant poles x=pi/2+kpi and use each connected interval between them; reciprocal-power families also exclude0. Hard evaluation0 lies in (-pi/2,pi/2). No branch-crossing identity or pole evaluation is used. All originals and normals have exactly the same first-derivative order and innerx arguments.

Identity hashes full prompt, fixed solution, difficulty, complete unordered field-owned banks and correct values. Seed/profile aliases and option ordering are excluded. Mathematical fingerprint uses the canonical actual function and evaluation point and excludes notation, answer bank and target fragment/radio roles. Thus product radio and product-fragment tasks with the same function share fingerprints. Hard retains derivative computation before the scalar evaluation; changing its secant coefficient changes that displayed mathematical task even when the final value is unchanged.
