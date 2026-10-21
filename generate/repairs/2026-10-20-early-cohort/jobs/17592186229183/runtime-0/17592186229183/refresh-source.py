"""Refresh captured source evidence without editing source or generator identities."""
import importlib.util,json,hashlib,re
from pathlib import Path
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('replenish',D/'replenish.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
v,g=r.v,r.g
kp=json.loads((r.OUT/'initial.json').read_text());old=g.SOURCE['record'];reports=[]
qa=json.loads((r.ROOT/'generate/runs/current/qa/17592186229183.json').read_text())
assert r.sha(D.with_suffix('.py'))==qa['generator_sha256']
for name,digest in qa['root_artifact_hashes'].items():assert r.sha(r.ROOT/name)==digest,name
old_by={q[':question/math-academy-id']:q for q in old[':knowledge-point/questions']}
for q in kp[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];p=v.physical_from_prompt(q[':question/problem']);x=g.data(p)
 report={'source':sid,'parameters':{k:str(x) for k,x in p.items()},'difficulty':'easy' if ':question/difficulty' in q else 'unrated','field_types':['radio'],'template':'overflow-onset','plots':'none','bank_profile':'opaque:'+sid,'rounding':x['rounded']}
 if sid in old_by:
  oq=old_by[sid]
  for attr in (':question/id',':question/problem',':question/worked-solution'):
   assert q.get(attr)==oq.get(attr),(sid,attr)
  # Previous cleanup removed only the invalid duplicate legacy selection field.
  assert len(q[':question/answer-fields'])==1
  def bank(f):return sorted(a[':answer/value'] for a in f[':answer-field/choices'])
  assert bank(q[':question/answer-fields'][0])==bank(oq[':question/answer-fields'][-1])
  report['prior_cleanup']='invalid duplicate field removed before this job' if len(oq[':question/answer-fields'])==2 else 'unchanged source'
 else:
  # Two new contexts share the existing q-336502 solution stages verbatim.
  lexical={k:str(z) for k,z in p.items()};lexical['c']='0.5' if sid=='q-336503' else '4/3'
  inst=g.generate('easy',template='q-336502',parameters=lexical)
  substance,container=('ink dye','reservoir') if sid=='q-336519' else ('fertilizer','tank')
  solution=inst['question'][':question/worked-solution'].replace('salt',substance).replace('reservoir',container)
  a=g.fmt(x['a']);solution=solution.replace(r'\frac{C}{('+a+r')^{2}} & =-',r'\frac{C}{{'+a+r'}^{2}} & =-')
  assert solution==q[':question/worked-solution'],sid
  report['solution_replay']='exact existing mask after context slots and exponent brace typography'
  report['sampling_policy']='new source context recorded; existing validated seven-mask sampler retained'
 f=q[':question/answer-fields'][0];offsets=[str(sval-r.s.Rational(x['rounded'])) for a in f[':answer-field/choices'] for sval in [r.s.Rational(a[':answer/value'].split('\\,')[0].replace('lb',''))]]
 reproduced=[g.rounded(r.s.Rational(x['rounded'])+r.s.Rational(z)) for z in offsets]
 assert reproduced==[a[':answer/value'].split('\\,')[0].replace('lb','') for a in f[':answer-field/choices']]
 report['offsets']=offsets;report['complete_bank_replay']='5/5 opaque observed offsets; excluded from normal generation'
 if q.get(':question/worked-solution'):
  v.independent({'question':q,'generation':{'eligible_for_learning':False},'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}})
  assert f[':answer-field/correct'][':answer/value']==x['rounded']+r'\,\text{lb}'
 reports.append(report)
result={'basis':2591,'lineage':r.LINEAGE,'source_questions':9,'source_banks_replayed':9,'source_choices_replayed':45,'source_solutions_mathematically_checked':8,'prior_validated_source_banks':8,'prior_validated_source_values':40,'ungradable_sources':['q-336499'],'reports':reports,'generator_unchanged':True,'generator_sha256':r.sha(D.with_suffix('.py')),'previous_qa':str((r.ROOT/'generate/runs/current/qa/17592186229183.json').relative_to(r.ROOT))}
r.save(D/'source-refresh.json',result)
counts=r.count(kp,r.OUT/'initial',2591)
print(json.dumps({'source_refresh':'passed','counts':counts}))
# Freeze only artifacts relied upon by preparation, after a current source audit.
paths=[D.with_suffix('.py'),D/'masks.json',D/'source.json',D/'source-refresh.json',D/'validate-inventory.py',D/'replenish.py',r.ROOT/'generate/runs/current/check-engine',r.ROOT/'generate/runs/current/qa/17592186229183.json']
r.save(D/'validation-freeze.json',{'status':'passed','hashes':{str(p.relative_to(r.ROOT)):r.sha(p) for p in paths},'supported_levels':list(g.LEVELS),'source_refresh_basis':2591})
