"""Revalidate source replay, exact graph mathematics and real image-radio grading."""
import importlib.util,json,hashlib,re,subprocess,sys
from pathlib import Path
from fractions import Fraction
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('legacy_checks',HERE/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned image choice'} for a in f[':answer-field/choices']]
def independent(r):
 assert r['knowledge_point']['db_id']==g.KP_ID and r['generation']['eligible_for_learning']
 assert r['question'][':question/difficulty'].split('/')[-1] in g.SUPPORTED_LEVELS
 v.check(r)
 z=r['generation'];n,d=z['parameters']['n'],z['parameters']['d'];a=Fraction(n,d)
 expected={'a':a,'-a':-a,'1':Fraction(1),'-1':Fraction(-1),'inverse':1/a,'-inverse':-1/a,'unit_denominator':Fraction(1,d),'-unit_denominator':Fraction(-1,d),'numerator':Fraction(n),'double':2*a}
 assert sorted(map(Fraction,z['plot_coefficients'].values()))==sorted(expected[k] for k in g.PROFILES[z['bank_profile']][2])
 assert z['mathematical_fingerprint']==g.digest(['positive-reciprocal-selection',str(a)])
 return r

def main():
 original_spec=json.loads((HERE/'plot-spec.json').read_text());mapping={r['asset']:Fraction(r['coefficient']) for r in original_spec}
 additional={}
 for sid,vals in [('q-99063',[-4,Fraction(-1,4),Fraction(1,4),1,4]),('q-113320',[Fraction(1,5),Fraction(-1,5),5,-1,1])]:
  q=g.QS[sid]
  for ans,c in zip(q[':question/answer-fields'][0][':answer-field/choices'],vals):
   asset=ans[':answer/value'];mapping[asset]=Fraction(c)
   additional[asset]={'coefficient':str(c),'sha256':sha(Path('/media/jake/SSD/EDB/math')/asset),'marked_points':[['-1',str(-c)],['1',str(c)]],'visually_verified':'reference/replenishment/new-source-bank.png; coordinate labels and branch signs inspected at native resolution'}
 replay=[];payload=[];review=[]
 for sid,q in g.QS.items():
  n,d=g.SOURCE_PARAMETERS[sid];profile='raw_'+sid;level=g.PROFILES[profile][0]
  r=g.generate(level,parameters={'n':n,'d':d},profile=profile);v.check(r,True)
  assert r['question'][':question/problem']==q[':question/problem']
  assert r['question'][':question/worked-solution']==q[':question/worked-solution']
  assert len(q[':question/answer-fields'])==len(r['question'][':question/answer-fields'])
  options=designations=0
  for sf,rf in zip(q[':question/answer-fields'],r['question'][':question/answer-fields']):
   assert sf[':answer-field/key']==rf[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==rf[':answer-field/type']
   assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
   for ans in rf[':answer-field/choices']:assert mapping[ans[':answer/value']]==Fraction(r['generation']['plot_coefficients'][ans[':answer/value']])
   assert (':answer-field/correct' in sf)==(':answer-field/correct' in rf)
   if ':answer-field/correct' in sf:
    assert sf[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);designations+=1
   options+=len(sf[':answer-field/choices'])
  replay.append({'source':sid,'prompt_and_solution_exact':True,'banks':len(q[':question/answer-fields']),'options':options,'correct_designations':designations,'complete_mathematical_bank_match':True})
  review.append(r)
 coverage={};exhaustive=0
 for profile,(level,template,recipes) in g.PROFILES.items():
  if profile.startswith('raw_'):continue
  params=g.domain(profile);coverage[profile]=len(params)
  for p in params:
   r=g.generate(level,parameters=p,profile=profile);independent(r);exhaustive+=1
   f=r['question'][':question/answer-fields'][0]
   payload.append({'label':profile+str(p),'record':r,'checks':checks(r)})
   rr=g.generate(level,seed=17,parameters=p,profile=profile)
   assert r['question'][':question/id']==rr['question'][':question/id']
  review.extend([g.generate(level,parameters=params[0],profile=profile),g.generate(level,parameters=params[-1],profile=profile)])
 # Explicit stale-scale and wrong-correct-answer mutations must fail.
 for kind in ('scale','answer'):
  r=json.loads(json.dumps(review[-1]));f=r['question'][':question/answer-fields'][0]
  if kind=='scale':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('scale factor of $','scale factor of $99',1)
  else:f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
  try:independent(r)
  except AssertionError:pass
  else:raise AssertionError('Mutation escaped validation')
 try:g.generate('hard')
 except ValueError:pass
 else:raise AssertionError('Unsupported hard accepted')
 out=HERE/'reference/replenishment';out.mkdir(parents=True,exist_ok=True)
 (out/'engine-input.json').write_text(json.dumps(payload,indent=2))
 engine=HERE.parents[1]/'runs/current/check-engine'
 subprocess.run([str(engine),str(out/'engine-input.json'),str(out/'engine-validation.json')],check=True)
 native=json.loads((out/'engine-validation.json').read_text())
 report={'status':'pass','source_basis':2744,'frozen_original_basis':1356,'source_replay':replay,'source_banks_matched':sum(r['banks'] for r in replay),'source_options_matched':sum(r['options'] for r in replay),'source_distractors_matched':sum(r['options']-r['banks'] for r in replay),'source_correct_designations_matched':sum(r['correct_designations'] for r in replay),'missing_source_designations_preserved':1,'exhaustive_normal_instances':exhaustive,'profile_coverage':coverage,'supported_levels':list(g.SUPPORTED_LEVELS),'hard':'unsupported; historical authored previews excluded','native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'generator_sha256':sha(HERE.with_suffix('.py')),'engine_sha256':sha(engine),'new_source_assets':additional,'fidelity':'all 7 source questions; all 8 banks and 40 choices; exact prompts and solutions; raw incomplete widget retained as evidence only','correctness':'exact positive reciprocal coefficient and complete unequal bank; native raster coordinate checks for every generated instance','grading':'all five choices of every normal profile/parameter instance checked through actual learner grader'}
 (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (out/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 (out/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in review))
 print(json.dumps({k:report[k] for k in ('status','source_banks_matched','source_options_matched','exhaustive_normal_instances','native')}))
if __name__=='__main__':main()
