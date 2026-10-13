# Template extraction

## Stage 1 — describe each original

Source-cases.json retains the exact vector entries and source IDs; source.json is the authoritative raw prompt, field, bank, missing attributes, rating and solution evidence. Classification lists every original individually. Each assessed response is a nonnegative scalar volume. Existing solutions compute the determinant by first-row cofactor expansion, show substituted scalar products, evaluate weighted minors, collect the triple product, then apply absolute value.

### q-40214

Calculate the volume of the parallelepiped spanned by $x = ⟨3, 5, 0⟩$, $y = ⟨3, 2, 0⟩$ and $z = ⟨3, 4, 5⟩$.

Parameter properties: {'vectors': [['3', '5', '0'], ['3', '2', '0'], ['3', '4', '5']]}. Exact integer entries; signed triple product -45, volume 45. Minor values [10, 15, 6]; signed weighted terms [30, -75, 0].

Field: :answer-field.type/radio; source key selection. Complete choices: 63, 37, 45, 24, 19.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'full', 'full'), False, (), False).

### q-42052

Calculate the volume of the parallelepiped spanned by $a = ⟨ - 3, 0,-2⟩$, $b = ⟨1, 5,-3⟩$, and $c = ⟨2,-1, 4⟩$.

Parameter properties: {'vectors': [['-3', '0', '-2'], ['1', '5', '-3'], ['2', '-1', '4']]}. Exact integer entries; signed triple product -29, volume 29. Minor values [17, 10, -11]; signed weighted terms [-51, 0, 22].

Field: :answer-field.type/radio; source key selection. Complete choices: 79, 29, 22, 39, 51.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'full', 'full'), False, (), False).

### q-128421

Calculate the volume of the parallelepiped spanned by $p=⟨2,2,3⟩,$ $q=⟨4,2,-1⟩,$ and $r=⟨-5,0,3⟩.$

Parameter properties: {'vectors': [['2', '2', '3'], ['4', '2', '-1'], ['-5', '0', '3']]}. Exact integer entries; signed triple product 28, volume 28. Minor values [6, 7, 10]; signed weighted terms [12, -14, 30].

Field: :answer-field.type/radio; source key selection. Complete choices: 14, 4, 42, 28, 56.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'full', 'full'), True, (), False).

### q-128433

Calculate the volume of the parallelepiped spanned by $a=⟨0,-1,4⟩,$ $b=⟨3,9,2⟩,$ and $c=⟨2,7,6⟩.$

Parameter properties: {'vectors': [['0', '-1', '4'], ['3', '9', '2'], ['2', '7', '6']]}. Exact integer entries; signed triple product 26, volume 26. Minor values [40, 14, 3]; signed weighted terms [0, 14, 12].

Field: :answer-field.type/radio; source key selection. Complete choices: 66, 7, 38, 26, 2.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('zero', 'omit', 'full'), True, (0,), False).

### q-18259

Calculate the volume of the parallelepiped spanned by $a=⟨-3,3,1⟩$, $b=⟨2,-1,3⟩$ and $c=⟨0,4,1⟩.$

Parameter properties: {'vectors': [['-3', '3', '1'], ['2', '-1', '3'], ['0', '4', '1']]}. Exact integer entries; signed triple product 41, volume 41. Minor values [-13, 2, 8]; signed weighted terms [39, -6, 8].

Field: :answer-field.type/radio; source key selection. Complete choices: 32, 41, 15, 53, 35.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'full', 'omit'), True, (), False).

### q-280670

Calculate the volume $V$ of the parallelepiped spanned by $x=⟨1,2,3⟩$, $y=⟨0,1,-1⟩$, and $z=⟨2,0,1⟩.$

$V=${{field-1}}

Parameter properties: {'vectors': [['1', '2', '3'], ['0', '1', '-1'], ['2', '0', '1']]}. Exact integer entries; signed triple product -9, volume 9. Minor values [1, 2, -2]; signed weighted terms [1, -4, -6].

Field: :answer-field.type/blank; source key field-1. Complete choices: 9.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'full', 'full'), False, (), False).

### q-280671

Calculate the volume $V$ of the parallelepiped spanned by $x=⟨1,1,2⟩$, $y=⟨-3,2,0⟩$, and $z=⟨4,-2,1⟩.$

$V=${{field-1}}

Parameter properties: {'vectors': [['1', '1', '2'], ['-3', '2', '0'], ['4', '-2', '1']]}. Exact integer entries; signed triple product 1, volume 1. Minor values [2, -3, -2]; signed weighted terms [2, 3, -4].

Field: :answer-field.type/blank; source key field-1. Complete choices: 1.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'full', 'full'), False, (), False).

### q-280712

Compute the volume $V$ of the parallelepiped spanned by the vectors $a=⟨1,2,3⟩$, $b=⟨0,5,0⟩$, and $c=⟨4,0,6⟩.$

$V=${{field-1}}

Parameter properties: {'vectors': [['1', '2', '3'], ['0', '5', '0'], ['4', '0', '6']]}. Exact integer entries; signed triple product -30, volume 30. Minor values [30, 0, -20]; signed weighted terms [30, 0, -60].

Field: :answer-field.type/blank; source key field-1. Complete choices: 30.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'full', 'full'), False, (), True).

### q-280716

Compute the volume $V$ of the parallelepiped spanned by the vectors $x=⟨3,1,4⟩$, $y=⟨0,2,5⟩$, and $z=⟨6,0,1⟩.$

$V=${{field-1}}

Parameter properties: {'vectors': [['3', '1', '4'], ['0', '2', '5'], ['6', '0', '1']]}. Exact integer entries; signed triple product -12, volume 12. Minor values [2, -30, -12]; signed weighted terms [6, 30, -48].

Field: :answer-field.type/blank; source key field-1. Complete choices: 12.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'omit', 'full'), False, (), False).

### q-40221

Calculate the volume of the parallelepiped spanned by $a=⟨-5,3,0⟩$, $b=⟨2,-1,4⟩$ and $c=⟨1,1,1⟩.$

Parameter properties: {'vectors': [['-5', '3', '0'], ['2', '-1', '4'], ['1', '1', '1']]}. Exact integer entries; signed triple product 31, volume 31. Minor values [-5, -2, 3]; signed weighted terms [25, 6, 0].

Field: :answer-field.type/radio; source key selection. Complete choices: 59, 31, 32, 22, 16.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('full', 'full', 'zero'), True, (2,), False).

### q-42050

Calculate the volume of the parallelepiped spanned by $a=⟨1,-2,1⟩$, $b=⟨2,-4,1⟩$ and $c=⟨0,2,5⟩.$

Parameter properties: {'vectors': [['1', '-2', '1'], ['2', '-4', '1'], ['0', '2', '5']]}. Exact integer entries; signed triple product 2, volume 2. Minor values [-22, 10, 4]; signed weighted terms [-22, 20, 4].

Field: :answer-field.type/radio; source key selection. Complete choices: 2, 5, 4, 3, 7.

Layout controls (coeff modes; commute second factor pair; omit zero weighted term; evaluate minors early): (('omit', 'full', 'omit'), True, (), False).

## Stage 2 — shared pattern

Given three supplied 3D vectors, calculate their scalar triple product as a 3×3 determinant and give its absolute value. Radio and blank fields share this method, with volume fragment as the complete scalar answer. No diagram, unknown parameter, vertex displacement, physical unit conversion, or symbolic branch is needed.

## Stage 3 — component and complete bank mapping

Each source question has a separate full layout recipe. Prompt tuples are complete mathematical slots; comma/space scaffolding and each atom’s spaced-minus style are retained. In solutions, the complete aligned component is a slot with five structurally distinct rows: 3×3 matrix, three 2×2 cofactor matrices, substituted products (or source q-280712 evaluated minors), signed weighted sum, collected determinant. The final V=|det|=volume component is a separate slot. Shared surrounding prose, whitespace and every existing stage are preserved byte-for-byte at original parameters. Source-specific omissions require actual zero terms; omitted unit factors require actual unit coefficients. No blind digit substitution is used.

bank-extraction.json maps every one of the seven radio banks, all 35 scalar choices (including 28 mathematically incorrect values), source answer/field IDs, exact value, volume ratio, and known/absent correct designation. The four blanks add four answer scalars (39 source values overall). Scalar wrong-choice intent is underdetermined, so no observed bank is promoted to inferred method-based generation. Every source profile uses the explicitly evidence-only formula abs(det)*ratio for its ENTIRE original bank. This proportional catalog is a recoverable numerical profile, not a cognitive error recipe, and has no learner-facing diagnosis. It is publicly replayable through generate(..., profile="observed_q-..."). A sign flip of the second vector exercises each original layout/bank with changed mathematical parameters.

The normal authored radio bank has exactly five operations chosen together: abs(T1+T2+T3), abs(T1+T2) (omit third), abs(T1+T3) (omit second), abs(T2+T3) (omit first), abs(T1−T2+T3) (reverse middle). Here Ti are the three signed cofactor contributions read from the actual supplied matrix. This is separately labeled authored-method. Bank ambiguity or zero values rejects the whole instance; no member is patched or replaced. Blanks contain only the positive scalar volume.

## Stage 4 — reusable Markdown/value template and bounds

Fixed: supplied-vector volume prompt, determinant/cofactor method, formal first-row signs, five ordered math rows, shared absolute-value closing prose, one fixed solution independent of the chosen wrong option. Variable: all nine vector components (with source-layout zero/unit guards), exact row labels from the source layout, all matrix/minor/substitution/evaluation numbers, signed determinant, volume and full owned bank. Conditional: source zero-term omission, unit-coefficient omission, product-factor commuting, early evaluated minors, original V/Compute/Calculate wording, existing blank placeholder. Optional: solution/correct/difficulty only when actually absent in raw public replay. The two originals remain fully preserved in observed profiles; observed_q-40214_repaired and observed_q-42052_repaired add independently derived keys45 and29, an authored easy rating, and the same five-stage solution; these cannot count as observed correct-designation matches.

Source errors/limitations: q-40214 and q-42052 contain five choices but no key, rating or worked solution. Authoritative local MA lesson JSON has one multiple-choice widget per question with exactly the same bank and no hidden explanation/key/rating; legacy-widgets.json preserves those records and its path/hash. Independent determinants are −45 and −29, so volume selects45 and29. The mathematical key inference is separate from 9/9 observed designation matches. Existing9 solutions,11 prompts and39 values need no repair. Decoded string inspection shows no erroneous adjacent TeX slashes: each adjacent pair is an intended aligned row separator, and no source command has doubled literal slashes. No visual-serialization claim of an escape error is made.

Sampling: normal easy uses signed integers within source magnitude9 and one to three zeros; moderate/hard bounds are in classification and enforced on reduced scalars for explicit and sampled inputs. Source-specific changed variants preserve zero/unit layout constraints by scaling only the second supplied vector by1,2 or−1 within magnitude9. Fixed explicit mathematical parameters/template/profile determine content independent of seed and option ordering. Content identity binds actual prompt, fixed solution, complete bank, version, correct availability and rating availability. Mathematical fingerprints use exact normalized supplied vectors and exclude field layout, bank profile and choice order. Author metadata never enters the learner prompt.

## Steps 5 and 7 — plots

Plot rating none: no practice/canonical prompt, answer, or worked solution has a plot. The route introduction/proof contains explanatory diagrams, outside this assessment; they are neither needed nor reused. No renderer or assets are required.

