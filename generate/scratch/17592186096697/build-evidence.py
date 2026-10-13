"""Rebuild private review evidence before freezing; never mutates shared files."""
import importlib.util,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('g',HERE.parent/'17592186096697.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):
 (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n' if not isinstance(value,str) else value)
cases=[];masks=[];review=[];text=['# Second-order direct-integration review','', 'Raw originals and public generated replays preserve their attribute presence. Completed examples normalize presentation and remove legacy duplicate fields. Authored E/M/H variants are separate. No database writes.','']
for key,q in g.SOURCES.items():
 level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 cases.append({'source_id':key,'template':key,'parameters':{'scale':1},'level':level,'bank_profile':'observed-'+key})
 matrix={'source_id':key,'level':level,'parameters':{'scale':1},'profile':'observed-'+key,'eligible_default':False,'prompt_components':re.findall(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)',q[':question/problem'],re.S),'solution_components':re.findall(r'\$\$.*?\$\$',q.get(':question/worked-solution',''),re.S),'fields':[]}
 for f in q.get(':question/answer-fields',[]):
  matrix['fields'].append({'source_field_id':f[':answer-field/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'has_correct':':answer-field/correct' in f,'choices':[{'source_answer_id':a[':answer/id'],'complete_original':a[':answer/value'],'parameterized_recipe':'Scale the complete C,D-free forced components by scale; retain the observed arbitrary-constant basis. This is an explicit expression profile, not inferred error intent.','correct_designation':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')} for a in f[':answer-field/choices']]})
 masks.append(matrix)
 original=g.generate(level,profile='observed-'+key,parameters={'scale':1});changed=g.generate(level,profile='observed-'+key,parameters={'scale':2});completed=g.generate(level,profile='completed-'+key,parameters={'scale':'1/2'})
 for label,out in [('Original / exact parameter replay',original),('Generated observed profile at scale=2 (raw evidence)',changed),('Generated completed profile at scale=1/2',completed)]:
  review.append({'label':label,'source_id':key,'record':out});text+=['## '+level.title()+' — '+key+' — '+label,'',g.markdown(out),'']
for template,level in g.TEMPLATES.items():
 for seed in (21,54):
  out=g.generate(level,seed,template);review.append({'label':'Authored '+level+' variant','record':out});text+=['## Authored '+level+' — '+template+' — seed '+str(seed),'',g.markdown(out),'']
save('source-cases.json',cases);save('source-masks.json',masks);save('review.json',review);save('review.md','\n'.join(text))
# Capture authority evidence only for legacy field-layout resolution, without
# importing new questions or changing the basis-1356 source snapshot.
lesson=json.load(open('/home/jake/Developer/MA/DATA/Lessons/1061/Source/1061.json'));found=[]
def visit(o):
 if isinstance(o,dict):
  if str(o.get('question_id')) in ('50139','50148'):found.append(o)
  else:
   for v in o.values():visit(v)
 elif isinstance(o,list):
  for v in o:visit(v)
visit(lesson);save('authority-layout.json',{'path':'/home/jake/Developer/MA/DATA/Lessons/1061/Source/1061.json','topic_id':1061,'purpose':'Single selection widget confirms duplicate EDB fields are legacy artifacts; designated field retained in completion.','questions':found})
counts={l:sum(q[':question/difficulty'][':db/ident'].endswith('/'+l) for q in g.SOURCES.values()) for l in g.LEVELS}
save('classification.md',f'''# Classification

Database math, basis 1356, lineage {g.SOURCE['lineage']}. All eleven practice questions captured; canonical e-529 does not count as practice. Observed counts: easy {counts['easy']}, moderate {counts['moderate']}, hard {counts['hard']}. All fields are radio. Thirteen raw fields contain 65 choices; eleven correct designations exist, while two legacy fields have no correct reference. No question is fieldless, unrated, or missing a worked solution in this capture. Presence parity is still asserted individually.

Easy observed structures: constant q-50139, exponential q-119038, sine q-119041, and cubic power q-119039. Moderate: isolated exponential q-50148; exponential/power q-119042; two powers q-119043; base exponential/trigonometric q-119044; divide-by-x polynomial q-50146; fractional power q-79554; scalar rearrangement/power/trigonometric q-99009. These eleven prompt/stage carriers remain separate; numerical differences do not claim distinct skills. Each source has one complete bank profile; the two five-option legacy and authoritative banks of q-50139/q-50148 are both retained in raw replay.

All plots: none. No practice prompt, choice, or solution uses a plot. Canonical sibling sketches belong to another KP and are excluded.

Lesson route is followed through first-step and next: introduction 17592186097555 → first-order general integration 17592186097556 → this second-order KP 17592186097557 → sketching 17592186097558 → particular-solution narrative 17592186097559 → initial-condition sibling 17592186097560. The reverse topic links list verifying ODE solutions, exponential substitution and trigonometric substitution prerequisites. Integrating-factor and separation topics occur later and are excluded.

Authored default easy: one familiar power, exponential, sine or cosine term, direct y''=g(x). Moderate: exactly two nonzero familiar terms, with coefficient 2–4 on y'' and scalar isolation. Hard has no observed label: exactly three nonzero familiar terms and the same scalar isolation, preserving more component primitives across both integration stages. This authored workload claim is anchored to the existing mixed-term moderate sources and e-529's two independent constants; it adds no integration technique, IVP, dependent-variable forcing or nonlinear solving. Same-level families are alternatives with no progression.

Raw anomalies: q-50139 and q-50148 each retain two same-key selection fields, first lacking a correct ref. The original lesson single-widget evidence is in authority-layout.json; completion keeps only the designated bank. Decoded byte inspection finds zero consecutive macro-backslash bytes and zero literal backslash-u2061 sequences in these answer values; serialized tool output is not evidence of an escape anomaly. q-119044's final row uses the typographic ln spelling without a command; completion renders it as the standard natural-log operator. The byte counts are recorded by validation, and raw strings stay exact. q-119041's first evaluated derivative primitive omits C before the next row includes C. Raw stages are preserved; completion adds C to that one row. Native raw fidelity does not invent the missing correct designations.
''')
save('template-extraction.md','''# Four-stage extraction

## 1. Specific observed questions

The exhaustive component/choice matrix in source-masks.json lists all eleven prompts, ordered solution blocks, fields, 65 original option strings, choice IDs and known correct designations. q-50139 integrates a negative constant; q-119038 integrates a signed linear exponential twice; q-119041 integrates sine then cosine; q-119039 uses the power rule twice. The seven moderate carriers first isolate the second derivative, then use one or two familiar primitive components. q-50146 division by x requires an interval excluding zero; q-79554 uses sqrt(x) on x>=0. All constants C,D are arbitrary and independent when their basis is {x,1}.

## 2. Shared pattern

Isolate y'' as a function of x alone, integrate once to y'=F(x)+C, then integrate again to y=P(x)+Cx+D. Do not merge constants with different x dependence. Response validity requires the complete general family, not merely a function satisfying the ODE or two letters representing only one independent degree of freedom.

## 3. Components and banks

Every observed source bank is retained intact under its explicit observed-q-ID profile, with all original field layouts and omissions. The matrix maps each option to its complete mathematical expression. The single scale parameter multiplies all forced components while retaining arbitrary-constant components; it is a valid covariance recipe for the entire printed prompt, distributed integral terms, individually evaluated primitive terms, reduced rows and answer expressions. It is not a recovered explanation of the original distractor algorithm. In particular opaque options such as 3x^4+4x^2 and polynomial/trig options containing C+D are evidence-only expression profiles. All observed profiles are ineligible defaults. None of these inferred wrong-operation interpretations is presented to learners.

The separate authored complete bank has exactly five members: P+Cx+D, -P+Cx+D, F+Cx+D (one integration), P+D (lost first constant), P+Cx (lost second constant). Every operation uses the actual two primitives. The full bank is chosen before parameter sampling; all members must be unequal as complete affine families, and exactly one must span the required general family. Collisions such as an e^x forcing causing F=P reject the whole instance, including explicit inputs. There is no adaptive recipe pool or partial fallback.

## 4. Reusable templates

Source rendering masks complete delimited mathematics; it splits top-level complete additive components with brace/parenthesis depth, protects derivative coefficients and arbitrary constants, scales forced terms and recursively scales a formal integral's mixed argument. Shared original sentences, row order and redundancy remain fixed. Neutral scale=1 reproduces exact strings through this same recipe; scale=2 and 1/2 exercise public changed-parameter replay. Visible multiplication grouping protects positive and signed numeric products.

Authored templates keep the shared integration sentences and two-constant conclusion. Each integration has formal operator, distributed component integrals, individually evaluated coefficient-times-primitive components and reduced result. Easy uses one component, moderate two, hard three. Coefficients are nonzero integers of absolute magnitude at most 8; powers 0–3; frequencies ±1/2,±1,±2,±3; bases 2,3,4. Easy derivative coefficient is 1; moderate/hard 2–4. Explicit inputs face all workload guards. Source scale is positive rational at most 8 and retains original parameter features. Source scope restrictions remain attached; default sampled powers are ordinary nonnegative integers.

Parameter/function/domain metadata never appears inside learner prompts. Mathematical fingerprints depend on the canonical forcing function on the fixed source domain; banks and unused slots are excluded. Content UUIDs depend on displayed prompt, complete bank, key presence, fixed solution and generator version, with option-order-independent sorting. Seed shuffling cannot create new identity. Different arbitrary-constant bases are compared by their spans and affine displacement, allowing invertible constant reparameterization while rejecting rank-deficient/one-constant/particular families.

Original-bank fidelity, presentation completion, displayed mathematics and native selected-ID grading have separate denominators. Missing original designations are counted as preserved omissions, never matches. The native harness cannot grade an unknown designation, so only the two designation-less legacy fields are omitted from in-memory fixtures; public raw records remain intact.
''')
save('README.md','''# Second-order direct integration

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186096697.py --difficulty all --seed 21 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186096697/validate.py
```

Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Only radio fields are supported because all source fields are radio. Default profiles use a complete authored bank with eligible_for_learning=true and evidence_only=false. Observed and completed opaque expression banks expose eligible_for_learning=false and evidence_only=true; all records also expose bank_eligible_default. observed-q-ID profiles are raw evidence replays; completed-q-ID profiles repair presentation and remove redundant legacy fields. Explicit source replay parameters are {"scale":1}; any positive rational scale<=8 is supported.

The source snapshot, topic context and linked lesson route are basis 1356. Original sources are in source.json; source-cases.json replays all eleven through the public API. source-masks.json accounts for every original bank and mathematical stage. review.md/review.json include every source profile at original and changed parameters, every completion and two examples of every authored template at each difficulty. Hard is explicitly authored because no observed hard label exists. No plots, database writes, shared edits, or nested agents.

build-evidence.py is the private evidence producer; finish it before the final validation pass. validation.json reports frozen producer/artifact hashes and distinct source fidelity, completion, mathematical readback and real-engine grading counts. Raw legacy fields and the source's intermediate constant omission remain evidence; normal/completed output is checked separately. Decoded byte inspection finds no doubled macro-backslash or literal Unicode-escape anomaly. Missing correct references remain absent and never count as inferred matches.
''')
print(counts,'review records',len(review))
