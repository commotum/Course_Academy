from pathlib import Path
import json,sys,importlib.util,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;R=H.parents[2]
s=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
classification='''# Classification at frozen basis 2275

Database math; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. This is a private revalidation draft for a registered numeric generator. The 111-file numeric script/evidence pathset and all hashes are preserved in registered-baseline.json; no registered artifact is edited.

The frozen source has nine MA originals: three easy, four moderate and two unrated. Seven have complete captured solutions and answer designations; q-30990 and q-47905 lack difficulty, key and solution. Six radio fields have five choices each and three blanks have one answer each: 33 original answer values. Every raw record, including all omitted attributes, is replayed exactly as evidence. There are nine separately retained prompt/solution/field masks: changing response layout, prime notation, evaluation stages or combination of functions retains separate masks even when the mathematical skill overlaps. There are six complete radio bank profiles, including the two unrated original banks, and no merged/pool bank.

Three additional records have no MA ID. They are independently authored inventory, not original MA evidence: one moderate coefficient variant of q-103081, and two easy radical-plus-tangent blank variants of q-341495. Their exact records and relationship_to_source_templates are preserved in independent-inventory.json. They establish no original hard source coverage.

The frozen topic has prerequisites Finding Trigonometric Ratios of Special Angles Using the Unit Circle and Calculating the Equation of a Tangent Line Using Differentiation. Product Rule for Differentiation and Second and Higher-Order Derivatives are successors. The actual activity 17592186059951 starts at 17592186060528 (standard sin/cos/tan derivative tutorial), proceeds to 17592186060529 (sine/cosine expression KP), then 17592186060530 (this tangent-expression KP). Later tutorials justify the derivative formulas; the last says quotient rule is learned very soon. No chain, product, quotient, reciprocal-function derivative, implicit or higher-order differentiation is introduced by this generator.

Easy uses a tangent term plus a linear, sine, square-root or quadratic term, with constant-factor expansion where observed. Moderate computes a derivative then substitutes a regular familiar unit-circle point. Hard has no observed MA source. Its explicitly authored peer family uses a distributed three-trig sum plus one polynomial: a(tan x+b sin x−c cos x)+d x^n. It adds bounded sum/constant-multiple workload while using only the same lesson’s already available sin/cos/tan rules and prerequisite polynomial power rule. It has no new method or extra target. Hard supports radio and blank layouts, both explicitly authored. Moderate’s authored familiar-point peer makes the actual evaluation input a slot while preserving differentiate-then-evaluate stages. All normal easy, moderate and hard defaults produce eligible peers; source-shaped fields remain fixed.

Plot rating is none for every original, canonical example and authored family. All mathematical content is textual TeX; no images or plots are present.
'''
(H/'classification.md').write_text(classification)
text='''# Template extraction

## 1. Specific original records

Each record is retained at frozen basis 2275 in source.json. observed_raw is evidence-only and returns the exact record including original question/field/answer identities, complete banks, raw Markdown, all available attrs and all absent attrs. It does not invent missing metadata. Normal source-pattern instances use the explicitly defined original masks and complete parameterized recipes below. All original feedback is absent and remains absent.

'''
recipes={
'q-341495':['a/(2 sqrt(x))+b sec²(x)'],
'q-47983':['(a+b sqrt(x) sec²(x))/(2 sqrt(x))','(a+2b sec²(sqrt(x)))/(2 sqrt(x))','(a+2b x sec²(x))/(2 sqrt(x))','(a+2b sqrt(x) sec(x))/(2 sqrt(x))','a/(2 sqrt(x))+b sec²(x)'],
'q-70911':['2a−a cos²(x)+c','a−ab sec²(x)','2ax−b sec²(x)','2ax−ab sec²(x)','x−a sec(x)+c'],
'q-103081':['b+2a','b','b−a sqrt(2)','−b−2a','b−2a'],
'q-17912':['−a','−a sqrt(2)','a/sqrt(3)','a sqrt(2)','a'],
'q-341825':['a'],
'q-341858':['a+b'],
'q-30990':['−a csc²(x)−bx','−a sec²(x)−bx','a sec²(x)−b','a csc²(x)+b','a csc(x)−b'],
'q-47905':['a sec(x)−b cos(x)','a sec²(x)−b cos(x)','a sec(x)+b cos(x)','a sec²(x)+b cos(x)','−a sec²(x)+b cos(x)']}
backbones={
'q-341495':'f(x)=a sqrt(x)+b tan(x). Blank is the whole derivative RHS. Stages: formal derivative of the supplied sum; distribute a,b to individual formal derivatives; apply sqrt and tangent derivative formulas; simplify the radical coefficient. Positive radical branch x>0, cos(x)≠0.',
'q-47983':'y=a sqrt(x)+b tan(x). Radio asks for the whole derivative. Stages: derivative of supplied sum; a/(2 sqrt(x))+b sec²(x); combine over 2 sqrt(x). Distractor profiles change tangent coefficient, tangent input to sqrt(x), spurious x factor, or secant power. These are explicit observed expression patterns; their historical error intent is not claimed recovered. x>0 and cos(x)≠0.',
'q-70911':'y=a(x²−b tan(x))+c. Radio asks y′. Stages: formal derivative of original parentheses; expand outer a; differentiate expanded terms; simplify. Every bank expression retains its source’s distinct x/constant/power pattern. cos(x)≠0.',
'q-103081':'y=bx−a tan(x), evaluation input pi/4. Radio derivative value. Stages: formal derivative; b−a sec²(x); substitute actual pi/4; use sec(pi/4)=sqrt(2); square and collect b−2a. Fixed source target is a conservative replay policy, not an intrinsic method restriction.',
'q-17912':'f(x)=−a tan(x), evaluation input pi. Radio derivative value. Stages: formal derivative; −a sec²(x); substitute pi; sec(pi)=−1 squared; simplify −a. Historical incorrect radical values retain their full observed patterns.',
'q-341825':'f(x)=a tan(x)−b x² at zero. Blank f′(0). Stages: derivative; a sec²(x)−2bx; substitute zero; sec(0) via reciprocal cosine; evaluate cos(0)=1; simplify to a. b remains a real supplied-expression slot even though the derivative value at zero is independent of it.',
'q-341858':'y=a tan(x)+b sin(x) at zero. Blank y′(0). Stages: derivative; a sec²(x)+b cos(x); evaluate zero; use sec²(0)=cos(0)=1; collect a+b.',
'q-30990':'f(x)=a tan(x)−b x. Radio whole derivative. Captured unrated source has no solution or key. Unique mathematically correct third choice is authored as a repair, together with easy difficulty and full formal derivative/sum-and-constant stage/result. Source csc errors are just bank values; their derivative formulas are not taught or required.',
'q-47905':'f(x)=a tan(x)−b sin(x). Radio whole derivative. Captured unrated source has no solution or key. Unique correct second choice is authored as a repair, together with easy difficulty and full formal derivative/sum-and-constant stage/result.'}
sourcecases=[]
for sid,old in g.SOURCES.items():
 f=old[':question/answer-fields'][0];p=g.PROFILES[sid][1]
 text+='### '+sid+'\n\n'+old[':question/problem']+'\n\nOriginal parameters '+str(p)+'. Difficulty '+old.get(':question/difficulty',{}).get(':db/ident','absent')+'; field '+f[':answer-field/type'][':db/ident']+'; key '+f[':answer-field/key']+'.\n\n'+backbones[sid]+'\n\n'
 text+='| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |\n|---|---|---|---|\n'
 for a,recipe in zip(f[':answer-field/choices'],recipes[sid]):
  right=a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') if ':answer-field/correct' in f else 'designation absent'
  text+='| '+a[':answer/id']+' | `'+a[':answer/value']+'` | '+recipe+' | '+str(right)+' |\n'
 text+='\n'
 sourcecases.append({'source_id':sid,'source_uuid':old[':question/id'],'source_db_id':old[':db/id'],'raw_record':old,'normal_template':sid,'normal_profile':'source-pattern','normal_parameters':p,'captured_difficulty':old.get(':question/difficulty'),'authored_repair':sid not in g.ORIGINALS,'bank_recipes':recipes[sid]})
text+='''## 2. Generalized backbone and scope

Differentiate the actual displayed tangent expression using the sum, constant multiple and power rules and the learned sin/cos/tan rules. Preserve the displayed variable x, function/prime notation, requested complete derivative or derivative-at-point, response field, original operative stage order and concrete evaluation target. For moderate, compute the derivative before substituting the actual input. Original masks remain separate by field type, supplied functions and operative layout. Every original answer bank is selected as one whole profile, not a pool of errors.

## 3. Components and parameter dependencies

Source-pattern normal masks are parameterized by a,b,c and rendered from the original complete prompt/solution strings using full mathematical component substitutions. Numeric derivative-at-point banks are rendered field-by-field, never by global digit replacement. Coefficients appearing in derivatives, expanded expressions, evaluated terms and final prose all depend on the same supplied expression. The 1 coefficient suppresses itself where the source did; no cosmetic label/option shuffle is used for variation. The two unrated repairs retain the captured exact prompt backbone and full mathematical banks but add only explicitly authored difficulty, key and same-method solution. No option-specific feedback is invented.

A recipe is the complete mathematical expression printed above, including changed powers, constants, coefficients and operator inputs. q-47983’s second option differentiates a tangent at sqrt(x), not at x; its full input remains part of the recipe. q-70911’s five banks preserve their compound wrong operations and retained constants exactly. Ambiguity rejects an entire bank. In particular, a=1 in q-70911 makes the third choice equal its correct fourth choice, so those radio instances are rejected. No fallback radio-to-blank conversion occurs. Every source bank is fully replayed at its original parameters and changed parameters, including both incomplete source banks; only original captured designations are counted as recovered keys.

The authored moderate point family supplies bx−a tan(x) at a regular point. Its correct answer is b−a sec²(t). Its whole bank uses correct; tangent-derivative sign error b+a sec²(t); omit tangent derivative b; omit secant square b−a sec(t); negate both derivative components −b−a sec²(t). Some familiar points make that five-value bank ambiguous; radios reject those entire combinations, while separately authored blanks may use them. The emitted solution has actual formal input, constant-multiple formal stage, derivative result, explicit point substitution, component evaluation and final exact answer. The moderate point slot has a changed-input test with a=2,b=3 held fixed.

The authored hard expression is a(tan(x)+b sin(x)−c cos(x))+d x^n. Correct derivative is a(sec²(x)+b cos(x)+c sin(x))+dn x^(n−1). Its complete bank changes sec² to sec; keeps the erroneous negative cosine-derivative sign; omits power multiplier n; or omits outer factor a on all three trig derivatives. These are independently authored method errors, explicitly separate from observed banks. Its actual formal input is differentiated independently, then the solution distributes coefficients to the four formal derivatives and gives the concrete result. Hard is a bounded workload extension in the same KP’s learned rules; there is no source hard difficulty claim.

## 4. Slots, bounds, domains and identities

All complete source coefficients a,b,c range over positive integers 1..6. q-30990 allows a 1..8 so its original coefficient 8 is included; b stays 1..6. Every declared coefficient is enforced exactly and extra/missing/fractional/unbounded parameters reject. q-70911’s additive constant c changes the actual supplied expression but does not add differentiation workload; it is not counted as a fresh derivative target by itself. All source evaluation targets remain at their captured points to preserve their exact operative sequence; this conservative policy is extended explicitly by the authored point family.

Authored moderate a,b range 1..6 and point∈{0,pi/4,−pi/4,pi,−pi}. These are all regular unit-circle points supported by the topic’s prerequisite. Hard a∈{2,3,4}, b,c,d∈{1,2,3}, n∈{2,3,4}. a excludes 1 so the distribution-error bank remains meaningful. Every hard trig and polynomial component is present; n is an actual supplied polynomial exponent and all subsequent derivative powers/coefficient stages must change together. No tan argument other than x appears in an eligible prompt. The derivative-at-point stages separately use the actual chosen point. Coefficient and exponent changes remain within comparable arithmetic workload at each difficulty.

Domain is real x with cos(x)≠0 for tangent expressions. Radical masks also require x>0 for their derivative; the original sqrt function at zero does not provide a finite derivative there. Every evaluation input is regular and explicitly checked. Distractor values are read as complete expressions; the q-47983 sqrt(x) input and csc distractors are permitted only as incorrect banks, not supplied-function branches. Secant poles are never valid evaluation points.

Mathematical task fingerprints depend on actual expanded supplied expression and actual evaluation input, not seed, identities, fields, option order, aliases or bank selection. A constant-only change in q-70911 is not a new assessed derivative task: the validator’s distinct derivative-task counts remove additive constants for unevaluated derivative requests, while the content identity still retains the supplied prompt. Source field contract/solution/backbone is fixed. Content identities depend on normalized prompt, full solution, difficulty, field layout, complete bank and correct designation. Answer identities belong to their field.

## Source omissions and supported presentation repairs

q-30990 and q-47905 omit difficulty, key and worked solution. Exact observed_raw preserves all omissions and is ineligible; normal source-pattern repairs independently author easy assignment, infer the unique mathematical key and supply the three same-method derivative stages. No missing metadata is described as recovered source evidence.

The frozen bank values for q-341495 and q-47983 have actual two-backslash command tokens before frac/sqrt. This is checked on the deserialized string rather than inferred from JSON appearance. Raw evidence keeps them. Served normal values repair only two-backslash frac/sqrt command prefixes to one canonical slash before shared normalization. Complete mathematical banks are compared separately from typography. Raw question/problem and solution layouts are retained for all seven complete source cases; shared normalize_prose is applied before served IDs. Bare answer values contain no dollar delimiters. No other source math errors were identified. Original feedback/unknown attrs remain solely exact evidence when not part of the standard generated serving record; source absence of feedback remains absence in normal output.
'''
# Actual task counts remove additive constant; adjust definition consistent with implementation later.
(H/'template-extraction.md').write_text(text)
(H/'source-cases.json').write_text(json.dumps(sourcecases,indent=2,ensure_ascii=False)+'\n')
(H/'plot-extraction.md').write_text('# Plot extraction and generation\n\nRating none. Nine original practice records, all three independent inventory records, the canonical example and authored extensions contain no image or mathematical plot references. No plot generator or assets are required.\n')
(H/'README.md').write_text('''# Basis-2275 registered-generator revalidation draft

Only 17592186059676-draft.py and its private evidence folder are modified. registered-baseline.json contains the entire 111-file original numeric script/evidence pathset with SHA-256 values; validation checks exact preservation. No DB writes, registration, engine or shared QA edits.

```sh
.venv/bin/python generate/scratch/17592186059676-draft/validate.py
.venv/bin/python generate/scratch/17592186059676-draft.py --difficulty all --count 2 --seed 7 --format markdown
.venv/bin/python generate/scratch/17592186059676-draft.py --difficulty easy --template q-30990 --profile observed_raw
.venv/bin/python generate/scratch/17592186059676-draft.py --difficulty moderate --template authored-point --field-type blank --parameters '{"a":2,"b":3,"point":0}'
```

JSON CLI output is a list of records; --difficulty all emits easy, moderate and hard records in that order. Public generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None), with easy/moderate/hard wrappers. observed_raw is exact ineligible evidence; source-pattern normal output uses the full original source recipe banks, preserving captured field shapes. Missing-source metadata is an authored repair. authored-method supplies a familiar evaluation-point moderate peer and a same-method four-term hard workload peer. Full bounded banks reject as a whole if ambiguous. Normal defaults cover all nine source families and both authored families.

source.json, topic.json and lesson.json are frozen basis-2275 snapshots. independent-inventory.json holds all three exact independent records with role and relationship_to_source_templates. source-cases.json retains every raw original and explicit full-bank recipe. source-replay.json separates attrs/omissions/raw fidelity from normal math and teaching authorship. The validator reads the actual supplied expression, actual point, full banks, every formal derivative operand, all algebraic/evaluated stages, conclusions, prime input, domains and contracts. Native grade_field checks cover all radio IDs and canonical/equivalent/wrong blank values. Structural mutations deliberately change the actual math/layout/key/domain. Review includes raw originals, normal replays, changed coefficients, point-only changes and a hard instance.
''')
print('documentation built')
