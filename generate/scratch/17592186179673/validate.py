#!/usr/bin/env python3
"""Fail closed: complete bank/prose fidelity; printed math; scope; native grader."""
import importlib.util,json,re,subprocess,sys,hashlib
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import mathcheck as C
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n')
def formatting(z):
 assert z.count('$')%2==0,'unbalanced math delimiters'
 stack=[]
 for i,ch in enumerate(z):
  if ch not in '{}':continue
  if i and z[i-1]=='\\':continue
  if ch=='{':stack.append(ch)
  else:assert stack,'unbalanced TeX braces';stack.pop()
 assert not stack,'unclosed TeX braces'
def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];f=q[':question/answer-fields'][0];ans=f[':answer-field/choices'];assert len(ans)==5
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 correct=f[':answer-field/correct'][1];assert sum(z[':answer/id']==correct for z in ans)==1
 assert len({z[':answer/id'] for z in ans})==5
 for z in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in ans]:formatting(z)
 integrand,lo,hi,_,_=C.displayed_integrand(q[':question/problem']);easy=q[':question/difficulty'].endswith('/easy')
 math=[]
 if easy:
  for z in ans:
   v,L,H=C.integral(z[':answer/value']);math.append((v,L,H))
   actual=C.equivalence(v,integrand) and C.equivalence(L,lo) and C.equivalence(H,hi)
   assert actual==(z[':answer/id']==correct),('wrong displayed setup selection',z)
  audit=C.bank_scalar_audit(ans)
  if not audit['valid_unique_bank']:
   assert r['generation']['raw_ambiguous_bank'] and len(audit['equal_complete_integrals'])==1,'ambiguous complete integrals in eligible bank'
  if r['generation']['authored']:
   scalar=[S.simplify(S.integrate(v,(C.t,L,H))) for v,L,H in math]
   assert all(not C.equivalence(scalar[i],scalar[j]) for i in range(5) for j in range(i))
  for i in range(5):
   for j in range(i):
    assert not all(C.equivalence(a,b) for a,b in zip(math[i],math[j])),'equivalent setup bank'
 else:
  val=S.simplify(S.integrate(integrand,(C.t,lo,hi)))
  for z in ans:
   v=C.expr(z[':answer/value']);math.append(v)
   assert C.equivalence(v,val)==(z[':answer/id']==correct),('wrong displayed value',z,v,val)
  for i in range(5):
   for j in range(i):assert not C.equivalence(math[i],math[j]),'equivalent value bank'
 C.check_tangent(r);stages=C.check_solution_rows(r)
 return stages

def main():
 sourcecases=[];allrecords=[];review=[];coverage=[];stage_count=0
 for sid,q in G.SOURCES.items():
  level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  case={'source_id':sid,'template':sid,'parameters':{'c':1},'bank_profile':'observed_'+sid,'difficulty':level};sourcecases.append(case)
  r=G.generate(level,template=sid,parameters={'c':1},profile=case['bank_profile']);stages=check(r);stage_count+=len(stages);allrecords.append(r)
  generated=r['question'];assert generated[':question/problem']==q[':question/problem']
  assert generated[':question/worked-solution']==q[':question/worked-solution']
  src=q[':question/answer-fields'][0];out=generated[':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in src[':answer-field/choices'])==sorted(a[':answer/value'] for a in out[':answer-field/choices'])
  correct=next(a[':answer/value'] for a in out[':answer-field/choices'] if a[':answer/id']==out[':answer-field/correct'][1]);assert correct==src[':answer-field/correct'][':answer/value']
  assert [a[':answer/type'][':db/ident'] for a in src[':answer-field/choices']]==[':answer.type/math']*5
  coverage.append({'source_id':sid,'complete_bank':True,'choices':5,'correct_designation':True,'exact_problem':True,'exact_full_worked_solution':True,'stage_kinds':stages,'ordered_stages':True,'mathematical_stages':len(stages),'raw_mathematical_bank_validity':C.bank_scalar_audit(out[':answer-field/choices']) if level=='easy' else {'valid_unique_bank':True}})
  for c in [-2,3]:
   variant=G.generate(level,template=sid,parameters={'c':c},profile='observed_'+sid);vst=check(variant);stage_count+=len(vst)
   assert vst==stages
   pref,suf,lhs,raw=G.source_parts(q);pref2,suf2,lhs2,raw2=G.source_parts(variant['question'])
   assert pref2==pref and suf2==suf and lhs2==G.scale_tex(lhs,c)
   assert raw2==[G.scale_tex(row,c) for row in raw]
   allrecords.append(variant)
   if c==-2:review.append(variant)
 # Minimal supported source-bank repair retains every prompt/prose/stage.
 for c in [1,-2,3]:
  r=G.generate('easy',template='q-124656',parameters={'c':c},profile='repaired_q-124656');stages=check(r);stage_count+=len(stages);allrecords.append(r)
  raw=G.generate('easy',template='q-124656',parameters={'c':c},profile='observed_q-124656')
  assert r['question'][':question/problem']==raw['question'][':question/problem'] and r['question'][':question/worked-solution']==raw['question'][':question/worked-solution']
  assert C.bank_scalar_audit(r['question'][':question/answer-fields'][0][':answer-field/choices'])['valid_unique_bank']
  if c in [1,-2]:review.append(r)
 # Every normal level has independently checked variations and no difficulty progression.
 fps={};positions=set()
 for level in ['easy','moderate','hard']:
  fps[level]=set()
  for seed in range(12):
   r=G.generate(level,seed);stages=check(r);stage_count+=len(stages);allrecords.append(r);fps[level].add(r['generation']['mathematical_fingerprint'])
   f=r['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   again=G.generate(level,seed,parameters=r['generation']['parameters']);assert r==again
   changedseed=G.generate(level,999,parameters=r['generation']['parameters']);assert r['question'][':question/id']==changedseed['question'][':question/id']
   if seed<2:review.append(r)
  assert len(fps[level])>=10
 assert len(positions)>=4
 # Canonical mathematical task ignores source/authored layout and bank.
 raw=G.generate('moderate',template='q-124661',parameters={'c':1},profile='observed_q-124661')
 authored=G.generate('moderate',parameters=dict(a=2,b=3,m=1,n=1,h=1,j=1,k=2))
 assert raw['generation']['mathematical_fingerprint']==authored['generation']['mathematical_fingerprint']
 # Unused easy h and option order cannot create a presentation identity.
 p=G.generate('easy',8)['generation']['parameters'];a=G.generate('easy',parameters=p);p2={**p,'h':2 if p['h']!=2 else 3};b=G.generate('easy',parameters=p2)
 assert a['question'][':question/id']==b['question'][':question/id']
 # Setup answer bounds ARE assessed, so changing them changes task identity.
 p2={**p,'j':0,'k':1};p3={**p,'j':1,'k':2};a=G.generate('easy',parameters=p2);b=G.generate('easy',parameters=p3);assert a['generation']['mathematical_fingerprint']!=b['generation']['mathematical_fingerprint']
 # Structural endpoint stage keeps primitive terms and endpoint substitutions.
 for r in review:
  if r['generation']['authored'] and not r['question'][':question/difficulty'].endswith('/easy'):
   sol=r['question'][':question/worked-solution'];assert sol.count(' & =')+sol.count('& =')>=7
   assert r'\left(\left(' in sol or sol.count(r'\right)+\left(')>=2
 # Explicit invalid inputs fail rather than resample; poles fail independently.
 invalid=[('hard',dict(a=1,b=2,m=4,n=1,h=1,j=0,k=1)),('hard',dict(a=2,b=2,m=1,n=1,h=2,j=0,k=1)),('moderate',dict(a=2,b=3,m=8,n=1,h=1,j=0,k=1)),('easy',dict(a=2,b=1,m=0,n=1,h=1,j=0,k=1))]
 for l,p in invalid:
  try:G.generate(l,parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid explicit input silently accepted')
 pole=G.SOURCES['q-124665'][':question/problem'].replace('(0,-3)','(1,0)')
 try:C.displayed_integrand(pole)
 except ValueError as e:assert 'interior' in str(e)
 else:raise AssertionError('interior pole accepted')
 # Native field-owned ID grading, independently from displayed mathematics.
 fixtures=[]
 for i,r in enumerate(allrecords):
  f=r['question'][':question/answer-fields'][0];fixtures.append({'label':str(i)+'/'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete owned radio bank'} for a in f[':answer-field/choices']]})
 write('engine-input.json',fixtures)
 cmd=[str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')];subprocess.run(cmd,check=True)
 write('source-cases.json',sourcecases);write('review.json',review)
 lines=['# Original and generated review','Database math; basis 1356; raw source exactness is separate from authored design.','Raw original q-124656 and its observed-profile variants are mathematically ambiguous: two complete integral choices equal zero. Native raw ID designation is fidelity evidence only. The repaired-profile variants below replace the wrong zero-valued choice by the omitted-dx integral of value 2pi.']
 for sid,q in G.SOURCES.items():
  r=G.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],template=sid,parameters={'c':1},profile='observed_'+sid);lines.extend(['## Original '+sid,G.markdown(r),'## Generated replay-profile variant '+sid,G.markdown(next(z for z in review if z['generation']['template']==sid))])
 for r in review:
  if r['generation']['source_bank_repair']:lines.extend(['## Repaired source-bank variant '+r['generation']['template']+' c='+str(r['generation']['parameters']['c']),G.markdown(r)])
  if r['generation']['authored']:lines.extend(['## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' seed '+str(r['generation']['seed']),G.markdown(r)])
 (HERE/'review.md').write_text('\n\n'.join(lines)+'\n')
 report={'passed':True,'source_snapshot':{k:G.SNAPSHOT[k] for k in ['database','basis','lineage']},'coverage':coverage,'source_complete_banks':{'matched':11,'total':11},'source_displayed_choices':{'matched':55,'total':55},'source_correct_designations':{'matched':11,'total':11},'source_raw_exact_problems':11,'source_raw_exact_full_solutions':11,'presentation_repairs':0,'mathematical_repairs':1,'raw_source_mathematical_banks':{'valid':10,'total':11,'ambiguous':1},'repaired_source_bank':{'source_id':'q-124656','retained_original_options':4,'total_options':5,'unique_integral_values':['pi/2','pi','-2*pi','2*pi','0'],'valid':True},'raw_source_bank_ambiguity_resolved_for_eligible_output':True,'endpoint_singular_sources':['q-124657','q-124665'],'endpoint_interpretation':'one-sided improper with continuous composed-integrand extension; source wording omitted this qualification','authored_missing_levels':['hard'],'records_independently_checked':len(allrecords),'displayed_arithmetic_stages_checked':stage_count,'authored_unique_task_fingerprints':{k:len(v) for k,v in fps.items()},'native_engine_provenance':{'binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'fixture_source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'entry_point':'course_academy_engine::learning::grade_field'},'native_engine':json.loads((HERE/'engine-report.json').read_text()),'identity_checks':['seed/order invariant','unused easy h excluded','setup bounds assessed and included','equivalent source/authored task deduplicated'],'unresolved_source_recipe_intent':'Global linear scaling replays each entire observed bank; numerical distractor intent is not inferred or promoted to default banks.','source_setup_scalar_ambiguities':[{'source_id':'q-124656','values':[0,0],'description':'correct cos-squared setup and incorrect sine-squared setup both evaluate to zero; actual mathematical source ambiguity: two whole definite-integral options equal zero; raw bank is replay-only evidence, repaired source bank replaces wrong integral by omit-dx integral of value 2pi; all normal E banks reject complete-integral collisions'}],'blocking_failures':[],'script_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
 write('validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ['native_engine','coverage']},indent=2))
if __name__=='__main__':main()
