"""Full-bank source replay, independent display proofs, scope and real grading."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as s
from mathcheck import parse,eq,prompt_curves,solution_check,T
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('slope',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
source=g.SOURCE['record'][':knowledge-point/questions']
cases=[];replays=[];fidelity=[];engine=[];reviews=[];proof_count=0

def check(r):
 global proof_count
 proof_count+=solution_check(r)
 q=r['question'];f=q[':question/answer-fields'][0];kind=f[':answer-field/type'].rsplit('/',1)[1]
 assert len(f[':answer-field/choices'])==(5 if kind=='radio' else 1)
 correct=f[':answer-field/correct'][1];a=f[':answer-field/choices'];assert len({v[':answer/id'] for v in a})==len(a)
 vals=[parse(v[':answer/value']) for v in a]
 x,y=prompt_curves(q[':question/problem']);u=s.sympify(r['generation']['parameters']['u']);m=s.simplify(s.diff(y,T).subs(T,u)/s.diff(x,T).subs(T,u))
 assert all(not v.has(s.zoo,s.oo,-s.oo,s.nan) and v.is_real is not False for v in vals)
 assert all(not eq(v,w) for i,v in enumerate(vals) for w in vals[i+1:])
 assert sum(eq(v,m) for v in vals)==1
 for v,value in zip(a,vals):assert eq(value,m)==(v[':answer/id']==correct)
 for ident in (q[':question/id'],f[':answer-field/id'],*[x[':answer/id'] for x in a]):uuid.UUID(ident)
 assert q[':question/problem'].count('{{field-1}}')==(kind=='blank')
 assert all('$' not in v[':answer/value'] for v in a)
 assert 'tangent to the curve' in q[':question/problem'] and 'undefined' not in q[':question/problem']
 rr=g.generate(q[':question/difficulty'].rsplit('/',1)[1],987,template=r['generation']['template'],parameters=r['generation']['parameters'],profile='observed' if r['generation']['presentation_profile']=='observed' and kind=='blank' else r['generation']['bank_profile'])
 assert rr['question'][':question/id']==q[':question/id']
 assert rr['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 checks=[]
 if kind=='radio':checks=[{'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==correct else 'rejected','purpose':'owned radio selection'} for v in a]
 else:
  value=a[0][':answer/value'];alternative=g.frac(g.tex(s.diff(y,T).subs(T,u)),g.tex(s.diff(x,T).subs(T,u)))
  if alternative==value:alternative=g.frac(g.tex(2*s.diff(y,T).subs(T,u)),g.tex(2*s.diff(x,T).subs(T,u)))
  assert alternative!=value and eq(parse(alternative),parse(value))
  checks=[{'submitted':value,'expected':'accepted','purpose':'canonical math fragment'},{'submitted':value.replace(r'\frac',r'\dfrac') if r'\frac' in value else value+r'\,','expected':'accepted','purpose':'supported LaTeX format normalization; not algebraic equivalence'}, {'submitted':alternative,'expected':'rejected' if r['generation']['presentation_profile']=='observed' else 'accepted','purpose':'documented original no-round native limitation' if r['generation']['presentation_profile']=='observed' else 'independently unreduced derivative quotient: meaningful algebraic equivalence'},{'submitted':g.tex(parse(value)+1),'expected':'rejected','purpose':'incorrect finite slope'}]
 engine.append({'label':r['generation']['template']+':'+q[':question/id'],'record':r,'checks':checks})
 return r

for q in source:
 proof_count+=solution_check({'question':q,'generation':{'parameters':g.PARAMETERS[q[':question/math-academy-id']], 'template':'source-'+q[':question/math-academy-id']}})
 qid=q[':question/math-academy-id'];template=g.SOURCE_TEMPLATE[qid];level=q[':question/difficulty'][':db/ident'].rsplit('/',1)[1];kind=g.TEMPLATES[template][1];profile='observed_'+qid if kind=='radio' else 'observed'
 case={'source_id':qid,'template':template,'parameters':g.PARAMETERS[qid],'bank_profile':profile if kind=='radio' else None,'profile':profile,'presentation_profile':'observed'};cases.append(case)
 r=check(g.generate(level,0,template=template,parameters=case['parameters'],profile=profile));replays.append(r)
 old=q[':question/answer-fields'][0];new=r['question'][':question/answer-fields'][0]
 actual=[parse(a[':answer/value']) for a in new[':answer-field/choices']];expected=[parse(a[':answer/value']) for a in old[':answer-field/choices']]
 assert len(actual)==len(expected)
 assert all(sum(eq(v,w) for w in actual)==1 for v in expected),(qid,expected,actual)
 corrected=next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);assert eq(parse(corrected),parse(old[':answer-field/correct'][':answer/value']))
 ox,oy=prompt_curves(q[':question/problem']);nx,ny=prompt_curves(r['question'][':question/problem']);assert eq(ox,nx) and eq(oy,ny),(qid,ox,oy,nx,ny)
 fixed=['We will use the formula','Differentiating $x$ and $y,$ we get','Therefore, when']
 assert all(v in q[':question/worked-solution'] and v in r['question'][':question/worked-solution'] for v in fixed)
 fidelity.append({'source_id':qid,'template':template,'bank':True,'values_matched':len(actual),'distractors_matched':len(actual)-1,'correct_designation_matched':True,'field_shape_matched':True,'curve_matched':True,'shared_solution_sentences':True,'exact_prompt':q[':question/problem']==r['question'][':question/problem'],'exact_solution':q[':question/worked-solution']==r['question'][':question/worked-solution'],'domain_repair':qid in ('q-20991','q-348305'),'notation':'standard equivalent LaTeX; preserved shared wording and worked stages'})
# Every observed template: two authored normal-bank variants, no level progression.
for template,(level,kind,f,q,plot) in g.TEMPLATES.items():
 for seed in (11,23):reviews.append(check(g.generate(level,seed,template=template)))
# Explicit profile variants ensure every retained complete bank generalizes.
for profile,template in g.BANK_PROFILES.items():
 if not profile.startswith('observed_'):continue
 level=g.TEMPLATES[template][0]
 for seed in (37,49):reviews.append(check(g.generate(level,seed,template=template,profile=profile)))
# Stress each template over varied structural coefficients/angles/evaluations.
counts={};fingerprints={}
for template,(level,kind,f,q,plot) in g.TEMPLATES.items():
 ids=set();maths=set()
 for seed in range(35):
  r=g.generate(level,seed+1000,template=template)
  proof_count+=solution_check(r)
  field=r['question'][':question/answer-fields'][0];values=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
  assert all(not eq(v,w) for i,v in enumerate(values) for w in values[i+1:])
  x,y=prompt_curves(r['question'][':question/problem']);u=s.sympify(r['generation']['parameters']['u']);m=s.simplify(s.diff(y,T).subs(T,u)/s.diff(x,T).subs(T,u))
  assert all(not v.has(s.zoo,s.nan,s.oo,-s.oo) and v.is_real is not False for v in values)
  assert sum(eq(v,m) for v in values)==1
  assert all(eq(v,m)==(a[':answer/id']==field[':answer-field/correct'][1]) for a,v in zip(field[':answer-field/choices'],values))
  ids.add(r['question'][':question/id']);maths.add(r['generation']['mathematical_fingerprint'])
 assert len(ids)>=25,(template,len(ids));counts[template]=len(ids);fingerprints[template]=len(maths)
# Explicit invalid inputs fail rather than silently replacing parameters/profile.
invalid=[('easy','cubic_radio',dict(a=1,b=1,u=0)),('hard','exp_root_blank',dict(a=3,b=3,u=-1)),('hard','reciprocal_exp_root_radio',dict(a=1,b=1,c=-1,u=1)),('moderate','harmonic_blank',dict(a=3,b=4,n=4,u='pi/3'))]
for l,t,p in invalid:
 try:g.generate(l,template=t,parameters=p)
 except ValueError:pass
 else:raise AssertionError(('invalid accepted',t,p))
# Cross-layout and equivalent parameter spellings deduplicate mathematically.
identity_radio=g.generate_easy(template='cubic_radio',parameters={'a':2,'b':1,'u':2})
identity_blank=g.generate_easy(template='cubic_blank',parameters={'a':2,'b':1,'u':'2'})
assert identity_radio['generation']['parameter_fingerprint']==identity_blank['generation']['parameter_fingerprint']
assert identity_radio['question'][':question/id']!=identity_blank['question'][':question/id']
write('source-cases.json',cases);write('source-replay.json',replays);write('review.json',reviews);write('engine-input.json',engine)
result=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-results.json')],capture_output=True,text=True)
if result.returncode:raise AssertionError(result.stderr+result.stdout)
print(result.stdout.strip());native=json.loads((HERE/'engine-results.json').read_text())
write('validation.json',{'passed':True,'blank_equivalence_complete':True,'source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_fidelity':{'questions':len(source),'complete_banks':len(fidelity),'values_matched':sum(v['values_matched'] for v in fidelity),'distractors_matched':sum(v['distractors_matched'] for v in fidelity),'correct_designations':len(fidelity),'field_shapes':len(fidelity),'curve_expressions':len(fidelity),'domain_repairs':2,'exact_prompt_strings':sum(v['exact_prompt'] for v in fidelity),'exact_solution_strings':sum(v['exact_solution'] for v in fidelity),'results':fidelity},'correctness':{'displayed_derivative_ratio_evaluation_equalities':proof_count,'normal_generated_variants':len(reviews),'stress_records':35*len(g.TEMPLATES),'unique_content_per_35':counts,'unique_math_per_35':fingerprints,'explicit_invalid_cases_rejected':len(invalid),'cross_layout_and_equivalent_parameter_math_identity':True},'native_grading':{k:v for k,v in native.items() if k!='records'},'grader_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'native_grading_limitations':[{'template':r['generation']['template'],'source_wording':'Do not round the answer.','effect':'compare_math_in_context treats round as form-sensitive and rejects algebraically equivalent unreduced dy/dt divided by dx/dt; canonical and supported TeX normalization accepted','implementation':'engine/rust/learning.rs:compare_math_in_context'} for r in [*replays,*reviews] if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank') and r['generation']['presentation_profile']=='observed'],'algebraic_blank_equivalence_accepted':sum(r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank') and r['generation']['presentation_profile']=='compatible-exact' for r in reviews),'unresolved_findings':[],'presentation_repair':'Normal blanks use Give an exact answer.; explicit observed presentation replays Do not round the answer. and records its native equivalence rejection.','database_writes':0})
# Review is source evidence + replay and two clearly labeled variants per template.
sections=['# Tangent slope generator review','Basis 1356. Original banks are shown in full. Variants are labeled as authored derivative-operation banks or explicit observed expression-pattern profiles. Source domains are repaired where explicitly stated; normal blank wording uses the exact-answer native-grading repair.']
for case,q,r in zip(cases,source,replays):
 original_prompt=q[':question/problem']
 for source_id,ref in g.SOURCE_ASSETS.items():
  if source_id==case['source_id']:original_prompt=original_prompt.replace(ref,str((HERE/'plots'/('source-'+source_id+'.png')).resolve()))
 sections+=['## Original '+case['source_id']+' — '+case['template'],original_prompt,'\nChoices: '+', '.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q[':question/worked-solution'],'### Parameterized replay',g.markdown(r)]
for r in reviews:sections+=['## Generated variant — '+r['generation']['template']+' / '+r['generation']['profile_origin']+' / '+str(r['generation']['bank_profile'])+' / '+r['generation']['presentation_profile']+' / seed '+str(r['generation']['seed']),g.markdown(r)]
(HERE/'review.md').write_text('\n\n'.join(sections)+'\n')
print('PASS:',len(source),'source questions;',sum(v['values_matched'] for v in fidelity),'source values;',proof_count,'displayed equalities;',35*len(g.TEMPLATES),'stress records.')
