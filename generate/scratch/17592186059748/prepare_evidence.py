#!/usr/bin/env python3
"""Read captured files, build this KP's evidence only; never contact EDB."""
import importlib.util,json,pathlib,shutil,hashlib,sys
sys.dont_write_bytecode=True
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('det_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
R=pathlib.Path('generate/runs/current')
for folder,identifier,target in [('sources',g.KP_ID,'source.json'),('topics',17592186049044,'topic.json'),('lessons',17592186049044,'lesson.json')]:shutil.copyfile(R/folder/(str(identifier)+'.json'),D/target)
source=json.loads((D/'source.json').read_text());qs=source['record'][':knowledge-point/questions']
cases=[];components=[]
for q in qs:
    sid=q[':question/math-academy-id'];ob=g.OBSERVED[sid];f=q[':question/answer-fields'][0];p=dict(zip('abcd',ob['matrix']))|{'name':ob['name']}
    det=ob['matrix'][0]*ob['matrix'][3]-ob['matrix'][1]*ob['matrix'][2]
    cases.append({'source_id':sid,'source_db_id':q[':db/id'],'source_question_id':q[':question/id'],'level':ob['level'],'level_assignment':'authored moderate, unrated original' if sid=='q-11648' else 'observed','template':ob['template'],'parameters':p,'bank_profile':sid,'original':q})
    choices=[]
    for a in f[':answer-field/choices']:
        coeff=str(g.sp.Rational(a[':answer/value'])/det)
        choices.append({'source_answer_id':a[':answer/id'],'field_key':f[':answer-field/key'],'exact_value':a[':answer/value'],'replay_recipe':'('+coeff+')*(a*d-b*c)','coefficient':coeff,'profile':sid,'observed_correct':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id'),'mathematically_correct':int(a[':answer/value'])==det,'reproduces_original':True,'error_intent':'unresolved scalar source; no recovery claim' if int(a[':answer/value'])!=det else 'direct determinant'})
    components.append({'source_id':sid,'parameters':p,'field_type':f[':answer-field/type'][':db/ident'],'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'choice_mapping':choices})
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'source-components.json').write_text(json.dumps(components,indent=2)+'\n')
authoritative=pathlib.Path('/home/jake/Developer/MA/DATA/Lessons/152/Source/152.json')
raw=json.loads(authoritative.read_text());item=next(x for x in raw['lesson']['items'] if x.get('question_id')=='11648')
(D/'authoritative-layout.json').write_text(json.dumps({'path':str(authoritative),'sha256':hashlib.sha256(authoritative.read_bytes()).hexdigest(),'item':item,'finding':'Five radio choices match captured EDB values; no captured correct designation or solution. 6 is inferred independently as 2*7-(-4)*(-2). Authoritative prompt is determinant-bar equals layout; EDB vmatrix question wording is retained for snapshot fidelity.'},indent=2)+'\n')
classification='''# Classification

Snapshot: database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All nine practice questions included; canonical example is separate evidence.

| Captured rating | Count | Layouts | Markdown/value templates | Complete banks | Plots |
|---|---:|---|---:|---:|---|
| easy | 4 | one 5-choice radio, three one-choice blanks | 2 | one radio profile; three blank cases | none |
| moderate | 4 | 5-choice radio | 3 | 4 profiles | none |
| missing | 1 | 5-choice radio | 1 | 1 profile | none |
| hard | 0 | authored radio and blank | reused integer layouts | authored operation bank | none |

Observed templates: named_dot q-1079; named_dot_indented q-1080 (four-space prompt indent); named_dot_swapped q-11646 (c*b substitution, not b*c); bare_dot q-127578/q-127580 (substitution appears on the first matrix row); named_parentheses_blank q-317335/q-317336/q-317342 (parenthesized multiplication, remove subtraction of negative at product stage, final period); vmatrix_dot q-11648 (no source solution). These different stage sequences and layouts are preserved.

q-11648 is unrated and lacks a correct ref and worked solution. Owning MA JSON confirms five choices and matrix. Independent determinant 2*7-(-4)*(-2)=6 supplies a correct ref; assigning moderate reflects two signed off-diagonal entries and nonzero products. This is an authored rating and inferred designation, never a matched original designation. Its new worked solution uses the source shared formula/prose and bare determinant sequence.

No source question contains graphics. The introductory tutorial image is outside the assessed question; generation therefore requires no plot renderer. Canonical example and introduction omit the symbolic ad-bc after the formula matrix in their captured prose; the eight practice solutions give the full correct formula, which normal generation preserves.

Curriculum route, followed through activity/first-step then step/next: Introduction -> integer determinant KP -> noninteger determinant KP -> unknown-entry determinant KP. Introduction to Matrices is this KP's sole key prerequisite. The tutorial explicitly says this lesson focuses on computing the determinant. Hard is authored integer arithmetic only: two nonunit signed diagonal products and their subtraction. Nonintegers, unknown entries, geometry, inverses and 3x3 determinants belong elsewhere and are excluded.
'''
(D/'classification.md').write_text(classification)
extraction='''# Four extraction stages

## 1. Specific sources

Every raw question, all original fields/UUIDs/choices, captured labels, full worked-solution prose and value-by-value mappings are retained in source.json, source-cases.json and source-components.json. q-1079 has zero diagonal product (1*0) and determinant -6. q-1080 has 40-(-3)=43; q-11646 has 12-(-10)=22 and reversed off-diagonal substitution order. q-127578 has 35-27=8; q-127580 has -5-20=-25. Blank sources give 32+15=47, 6-4=2 and 42+10=52. q-11648 asks for determinant of [2,-4;-2,7], giving 14-8=6; no observed correct label or solution exists.

## 2. Generalized pattern

Evaluate a supplied integer 2x2 determinant by the same ad-bc operation: locate the ordered diagonal entries, substitute both products, evaluate the two integer products, then subtract. Named forms include a separate determinant-to-matrix row; bare forms combine the matrix and substitution row. Radio responses are one exact integer from five; blank responses are a delimiter-free exact integer and retain their field-1 placeholder. No response-dependent solution or distractor feedback is added.

## 3. Components and full banks

source-components.json maps every original option to its field, exact value, profile and parameterized numerical covariance coefficient. All 33 source options (six 5-choice radios and three blanks), including 24 radio distractors, remain covered. One choice is correct mathematically in every complete bank. Eight designations are captured; the missing ninth is separately inferred.

The scalars alone do not recover mistake operations. An observed profile multiplies its documented scalar coefficient by the newly computed determinant, restricted to common nonzero integral matrix scaling, so both determinant and every replay option scale by t² and remain integers. At original parameters this matches the entire observed bank. This is an explicitly opaque numerical covariance extension, not a theory of the learner error. No arbitrary scalar fitting enters default banks. Original bank records are never returned as literal payloads or answer lookups; prompts/solutions/answers follow the same parameterized generation path.

The default authored 5-choice bank is one complete operation set: ad-bc (correct), ad+bc (add instead of subtract), bc-ad (reverse subtraction), ad (omit the other product), and ab-cd (multiply rows). Generate the complete bank and reject the whole instance if any pair coincides. No pooled first-valid distractors. Blank defaults compute only ad-bc. A profile's numerical reproduction is checked separately from the defensibility of authored default distractors.

## 4. Reusable templates, domains and scope

Fixed: complete source opening formula, transition sentence and paragraph/math layout. Slots: four ordered integer matrix entries, matrix name, both substitution factors, two products and final determinant. Conditional slots group negative factors after multiplication/subtraction; parenthesized blank templates turn subtraction of a negative product into addition. Source c*b ordering and first-row omissions are structural template attributes, never CAS simplifications. Full prose and every original stage are compared byte-for-byte on replay. No TeX repair is needed.

Easy default bounds: |entry|<=9, at most one zero and at most one negative, at least one product magnitude >=2; support source easy signed and zero cases without collapsing both products into zero. Moderate default bounds: nonzero |entry|<=10, at least one negative and at least one product magnitude >=10, matching observed signed arithmetic. Observed easy and moderate ratings overlap; these bounds are authored variation policies, not claims of recovered authoring code. Hard (absent from sources) bounds: each |entry| in 6..15, two or three negatives, both product magnitudes >=50 and at least one magnitude >=11. Thus hard always retains two nonunit products and signed integer subtraction. Arithmetic size/sign management is the only authored extra demand; no new algebraic skill. Every instance in a level has the same direct ad-bc workload, with no internal progression. All bounds apply to explicit authored inputs. Observed covariance replay has its separate finite scaling domain (all |entry|<=40); it is never used by default and is not counted as authored level variety.

Content UUIDs depend on actual printed prompt, full fixed solution, field layout and sorted complete bank. The mathematical fingerprint depends only on the ordered matrix; names, layout, profile, option order and seed cannot inflate assessed task counts. Choice shuffling is seeded after correct identity recording. Different banks on an identical matrix get different content IDs. Harmless profile aliases with identical learner output do not change IDs.

Plot extraction/spec: none. No assessed image references or parameter-dependent visual objects; no image renderer is needed at steps 5/7.
'''
(D/'template-extraction.md').write_text(extraction)
(D/'README.md').write_text('''# Integer 2x2 determinant generator

Verify using `.venv/bin/python generate/scratch/17592186059748/validate.py` from the repo root. Preview with `.venv/bin/python generate/scratch/17592186059748.py --difficulty all --count 2 --seed 42 --format markdown`.

API: generate_easy, generate_moderate, generate_hard, or generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Parameters require integer a,b,c,d and one supported name. Observed profiles are q IDs; authored_operations is the default. No DB access or registration.

All nine original prompts/banks are covered. Eight captured solutions/designations have full observed fidelity; q-11648 has a captured prompt/bank but an authored moderate rating, independently inferred correct designation and authored solution. Hard is explicitly authored direct integer determinant arithmetic. Six original radio banks are opaque scalar covariance replay profiles; default banks use complete defensible determinant operations. See validation.json for denominators and native grading checks; review.md displays all originals/replays and labeled variants at every level.
''')
print('Prepared source, classification, extraction and authoritative-layout evidence.')
