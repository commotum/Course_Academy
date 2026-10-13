#!/usr/bin/env python3
"""Rebuild private review/extraction evidence; no shared writes or transactions."""
import importlib.util,json,hashlib,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
cases=json.loads((HERE/'source-cases.json').read_text())

def put(name,text): (HERE/name).write_text(text.rstrip()+'\n')

classification='''# Classification, math basis 1356

Snapshot lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json` is the untouched capture wrapper. Seven practice questions: six observed easy, one unrated; no observed moderate/hard. Eight captured radio fields, all key `selection`, five complete choices each. q-37192 repeats the same widget as a legacy field and a current field. Normal questions have one five-option radio field. No practice prompt, bank, or solution has an image; plot rating **none** for all templates. The lesson introduction's explanatory tree is not part of any practice layout.

| Template | Source | Original name and target | Original structural demand | Level evidence |
|---|---|---|---|---|
| cross_theta | q-37192 | f, theta | 2xy+y²; three product contributions, double-angle collection | easy |
| log_linear_r | q-37196 | g, r | ln(x+y); common denominator and cancellation | unrated; authored easy assignment |
| cubic_r | q-94999 | h, r | x²y; two radial product contributions, cubic coefficient collection | easy |
| log_radial_r | q-95109 | w, r | ln(x²+y²); quotient partials and Pythagorean cancellation | easy |
| x_square_r | q-95112 | f, r | x²; one nonzero Cartesian partial, squared cosine | easy |
| y_square_theta | q-95113 | g, theta | y²; one nonzero Cartesian partial, double-angle identity | easy |
| radial_theta | q-95116 | w, theta | (x²+y²)/2; equal opposite angular terms cancel | easy |

Every original bank has its own `observed` profile; `cross_theta` also has `legacy`. The legacy/current banks are mathematically identical, with different captured notation/order. Source-cases retain both; normal output never asks for two duplicate selections.

## Missing-level scope

Prerequisites are Polar→Cartesian coordinate conversion (topic 936) and the Multivariable Chain Rule (3173). Canonical e-8294 differentiates ½x²+y² with respect to theta. Follow `activity/first-step` and `step/next`, not collection order: introduction (17592186125531) → this KP (17592186125532) → inverse-coordinate derivation (17592186125562) → polar-given function/Cartesian derivative sibling (17592186125533) → cylindrical tutorial/example (17592186125534/535) → spherical tutorial (17592186125563). Only the first two steps support this generator's assessed direction. The inverse sibling establishes a boundary and is excluded.

Moderate peer templates use nonzero unequal quadratic square coefficients plus a nonzero cross term, with target r or theta. Both Cartesian partials have two nonzero terms: four substitutions/products, one final collection; source cross_theta has three products. Coefficients are signed integers of absolute magnitude 1..4, square coefficients unequal. These are authored difficulty claims, not recovered labels, and the two derivative targets are peer tasks.

Hard peers are (a) a two-term cubic a x²y+b xy² with theta target, whose two two-term partials require four cubic angular products, and (b) ln(a x²+b xy+c y²) with theta target, whose four numerator products retain a common nonconstant angular denominator. Both extend observed cubic/log families rather than add another method. Coefficients are signed nonzero integers with absolute magnitude 1..4; logarithmic square coefficients are positive/unequal and 4ac>b². No angle evaluation, second derivative, inverse-coordinate derivative, cylindrical/spherical branch, or new function class is introduced. Each family samples equal-level peers, with no within-level progression.

Easy source-pattern sampling uses positive scale a∈{½,1,2,3,4,5,6}; each original is a=1. The scale multiplies the complete Cartesian function and every observed expression pattern. Function names f/g/h/w affect presentation only. There are 49 bounded easy function/target tasks. Moderate has at most 896 coefficient/target tasks, cubic hard at most 64; log-quadratic positive-definite triples are deduplicated by their Cartesian partials, so common positive argument scales do not inflate task counts. All authored defining coefficients stay nonzero on explicit inputs and sampling.
'''
put('classification.md',classification)

extraction='''# Template extraction

## 1. Specific originals

See classification for every exact Cartesian expression/target/name. All require a symbolic derivative expression, without an equation left-hand side, a numerical point, or a rounding instruction. Original source radio layout is a fixed `selection` field with five math answers. q-37196 has neither a difficulty, a correct ref, nor a worked solution. All other six have four worked display blocks: generic two-term chain rule, Cartesian partials, substituted polar partials, then ordered substitution/collection. Final block row counts are respectively 3, unavailable, 3, 3, 2, 2, 3. The easy formulas use polynomials of degree 2/3 and natural logs of linear/radial expressions; exact integer/rational coefficients, sin/cos(theta), and double angles. r>0 is the polar domain; ln(x+y) additionally requires r(cos(theta)+sin(theta))>0.

## 2. General pattern

For Cartesian-given F(x,y), calculate F_x and F_y. Substitute x=r cos(theta), y=r sin(theta), then form F_r=F_x cos(theta)+F_y sin(theta) or F_theta=-r F_x sin(theta)+r F_y cos(theta). Simplify only after the explicit substitution and original collection stages. Easy templates introduce a positive linear scale a. All observed full option expressions are correspondingly scaled: source expression-pattern preservation, not a fitted polynomial or recovered psychological error recipe. Because several original mistakes are underdetermined, default generation uses separately labeled authored operation banks. Observed/legacy banks remain complete replay profiles, never mixed into a pooled default.

## 3. Component and complete-bank map

The table below accounts for every raw captured option, including the duplicate legacy bank. Each displayed value is the full source expression; the parameterized recipe is a times that full expression. No option is dropped or silently interpreted as an operation. At a=1 all values match independently parsed mathematics. Current correct refs and absent refs are distinguished. Raw answer UUIDs remain in source.json; review output owns new field-specific UUIDs.

'''
for case in cases:
    q=g.RAW[case['source_id']];field=q[':question/answer-fields'][case['raw_field_index']]
    extraction+='### '+case['source_id']+' / '+case['profile']+'\n\n'
    extraction+='Prompt: '+q[':question/problem']+'\n\n'
    extraction+='| Captured answer | Complete parameterized recipe | Source designation | Intent |\n|---|---|---|---|\n'
    for a in field[':answer-field/choices']:
        correct=field.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id']
        designation='correct ref present' if correct else ('wrong under existing correct ref' if ':answer-field/correct' in field else 'no correct ref in capture')
        extraction+='| $'+a[':answer/value']+'$ | $a\\left('+g.normalize(a[':answer/value'])+'\\right)$ | '+designation+' | expression pattern; intended wrong operation unresolved |\n'
    extraction+='\n'
extraction+='''## 4. Reusable masks, domains, calculations and repairs

Fixed components: original prompt sentences, function-of-two-Cartesian-variables form, full source worked prose, four display blocks, and original final-stage sequence/row count. Variable complete components: Cartesian function RHS, its two partial RHSs, their polar substitution RHSs, every ordered final-stage RHS, target derivative/function labels, and each full bank expression. Formula insertion uses a complete RHS slot; it never blindly replaces x or y throughout text. `easy_components` contains explicit arithmetic stage masks; `calculation` supplies independent exact derivatives for bank correctness. A nonunit coefficient is inserted into every additive contribution, including both numerator terms of rational partials. Trig commands have explicit lexical separators, so implicit xy and sequential theta/r products are parsed and printed correctly. Named-function replacement touches only actual function labels, never variables or TeX command text.

All source solution prose paragraphs and every final mathematical stage replay in sequence. Generated math uses conventional \\sin/\\cos/\\ln rather than imported invisible application glyphs; brace/spacing conventions and punctuation inside displays are normalized. This is not byte-exact worked-solution reproduction: validation reports that denominator honestly, separately from complete mathematical-stage/prose fidelity. Raw source strings are unchanged in source.json. There is one fixed solution, independent of answer selection.

The source-format anomalies and minimal repairs are:

| Source | Raw evidence | Generated treatment | Fidelity denominator |
|---|---|---|---|
| q-37192 | Two fields both key selection; legacy lacks ref. Original MA JSON/screenshot shows one five-option widget. | One field; preserve both full banks as current/legacy replay profiles. Existing current correct ref selects 2r²cos(2theta)+r²sin(2theta). | 10/10 values, 2/2 banks; only one captured designation can match. |
| q-37196 | One five-choice widget, no correct marker/ref/difficulty/solution. | Independent derivative of ln(r(cos(theta)+sin(theta))) is 1/r; add mathematically derived ref, author easy assignment and common-method solution. | 5/5 values; 0 original designation available, never claimed matched; no original solution fidelity. |
| q-94999 | Generic radial chain formula labels its second partial as g, although function is h. | g→h only in that label. | Source teaching-label repair, not raw exact match. |
| q-95113 | Polar partial block labels the zero first partial as g_y. | First derivative label y→x. | Source teaching-label repair. |
| q-95116 | Polar partial block labels first partial as w_y. | First derivative label y→x. | Source teaching-label repair. |

Original MA authoritative widget evidence is saved in original-widgets.json; inspected screenshots are `/home/jake/Developer/MA/DATA/Lessons/1942/Source/Sections/03-question-37192.png` and `04-question-37196.png`. Both screenshots have exactly one radio widget with five options. Neither screenshot supplies the missing q-37196 designation. No source mathematical choice needs a value correction or exclusion.

Every complete observed/default/authored bank is rejected as a whole on equivalent values or a missing/ambiguous correct answer. Default authored easy operations include omitted coordinate derivatives/contributions, incorrect derivative target, lost power/Jacobian factors, reciprocal factors and sign errors; these are author metadata, with no invented distractor diagnosis in the learner solution. Moderate/hard defaults use correct, negated correct, one dropped radial factor, x-only contribution and y-only contribution, with eligibility enforced by whole-bank checks. Source profiles retain all five patterns rather than taking the first valid distractors.

No plots occur in these practices; steps 5/7 require no asset generator. No blank fields exist, so blank equivalence and the native “round” wording limitation do not apply. Native radio grading checks all five owned answer IDs, while independent exact mathematics checks every displayed option and row.
'''
put('template-extraction.md',extraction)

records=[];review='''# Originals and generated peers

Raw originals below are evidence, including incorrect/missing labels and refs. Generated records use the documented minimal teaching-label/layout repairs. Observed-bank variants are separate from default authored-bank variants. Moderate/hard are authored levels; source q-37196 is unrated. All examples are deterministic and use the normal generator.

'''
for source_id,q in g.RAW.items():
    review+='## Raw original '+source_id+'\n\n'+q[':question/problem']+'\n\n'
    for i,f in enumerate(q[':question/answer-fields']):
        review+='Field '+str(i)+'; '+f[':answer-field/key']+'; original correct: '+f.get(':answer-field/correct',{}).get(':answer/value','ABSENT')+'\n\n'
        for a in f[':answer-field/choices']:review+='- $'+a[':answer/value']+'$\n\n'
    review+='Original worked solution:\n\n'+q.get(':question/worked-solution','ABSENT; generated solution is authored.')+'\n\n'
for template,level in g.TEMPLATES.items():
    profiles=['observed','authored','legacy'] if template=='cross_theta' else ['observed','authored'] if level=='easy' else ['authored']
    for profile in profiles:
        for index,a in enumerate([2,3]):
            if level=='easy':p={'a':a,'name':['f','w'][index]}
            elif template=='cubic_sum_theta':p={'a':a,'b':-1-index,'name':['g','h'][index]}
            else:p={'a':a,'b':-1-index,'c':4,'name':['h','g'][index]}
            record=g.generate(level,seed=321+index,template=template,parameters=p,profile=profile)
            records.append(record)
            review+='## Generated '+level+' / '+template+' / '+profile+' / '+str(index+1)+'\n\n'
            review+='Parameters: `'+json.dumps(p,sort_keys=True)+'`. '+('Authored level and bank.' if level!='easy' else 'Authored default operation bank.' if profile=='authored' else 'Observed complete bank scaled as expression patterns.')+'\n\n'
            review+=g.markdown(record)+'\n\n'
put('review.md',review)
put('review.json',json.dumps(records,ensure_ascii=False,indent=2))
put('README.md','''# Plane polar derivatives

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124594/validate.py
.venv/bin/python generate/scratch/17592186124594/build_review.py
.venv/bin/python generate/scratch/17592186124594.py --difficulty all --seed 23 --count 2 --format markdown
```

Scope: Cartesian-given symbolic function → r/theta derivative through the two-term chain rule. Seven source families, all radio, no plots. Source cases include eight raw banks covering seven questions (one duplicated legacy field). Every missing reference is explicitly derived, not counted as matched. Default operation banks and absent moderate/hard levels are authored; exact observed banks remain profile options. See classification, extraction, review and validation.json for bounds, provenance and denominators. Source.json preserves raw basis-1356 capture. No EDB writes, registration, engine modifications or database-preparation artifacts.

The validator independently parses actual printed prompt formulas, all choices and every solution row, verifies full banks/stage order and formatting, exercises function renaming, explicit domain guards, deterministic content identity and mathematical deduplication, and invokes the shared real native grader in memory. No blank fields: no algebraic entry-equivalence claim. The output UUIDs and colon-key schema are local review records.
''')
put('plot-spec.md','''# Plot extraction / generation

All seven captured practice prompts, all forty raw captured options (including the duplicate legacy bank), and all six available worked solutions contain mathematical text only. No image/plot references occur. The lesson introduction contains a tree diagram, which is explanation context rather than a practice asset. None of the authored peers requires geometric information. Rating: none. No renderer/assets are needed; no direct SVG or image model is used.
''')
put('freeze.json',json.dumps({'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'review_records':len(records),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'steps':'3–7','database_writes':0},indent=2))
print('Wrote review for',len(records),'generated records; source capture untouched.')
