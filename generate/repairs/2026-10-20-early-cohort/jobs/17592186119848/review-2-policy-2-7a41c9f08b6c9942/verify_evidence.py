"""Validate review evidence references, schema and exact check totals."""
import json,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent;R=Path('/home/jake/Developer/Course_Academy');W=E.parent/'workspace'
load=lambda p:json.loads(Path(p).read_text())
r=load(E/'result.json');v=load(E/'pedagogical-variation.json');schema=load(R/'generate/pipeline/pedagogical-variation.schema.json')
def validate(x,s,path='root'):
 if 'enum' in s:assert x in s['enum'],path
 t=s.get('type')
 if t=='object':
  assert isinstance(x,dict),path
  assert set(s.get('required',[]))<=set(x),path
  if s.get('additionalProperties') is False:assert set(x)<=set(s['properties']),path
  for k,val in x.items():
   if k in s.get('properties',{}):validate(val,s['properties'][k],path+'.'+k)
 elif t=='array':
  assert isinstance(x,list) and len(x)>=s.get('minItems',0),path
  for i,z in enumerate(x):validate(z,s['items'],path+'.'+str(i))
 elif t=='string':assert isinstance(x,str) and len(x)>=s.get('minLength',0),path
 elif t in ('integer','number'):
  assert isinstance(x,int if t=='integer' else (int,float)) and not isinstance(x,bool),path
  assert s.get('minimum',float('-inf'))<=x<=s.get('maximum',float('inf')),path
validate(v,schema)
refs=[]
def scan(x):
 if isinstance(x,dict):
  for k,val in x.items():
   if k in ('evidence_paths','sample_refs'):
    for name in val:
     p=E/name;assert not Path(name).is_absolute() and '..' not in Path(name).parts,name;assert p.is_file() and p.stat().st_size>0,name;refs.append(name)
   else:scan(val)
 elif isinstance(x,list):
  for z in x:scan(z)
scan(r);scan(v)
assert set(r['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
assert all(r['checks'][k]['status']=='passed' for k in r['checks'] if k!='decision_variation')
assert r['checks']['decision_variation']['status']=='failed' and r['verdict']=='revise'
names=['grader-results.json','targeted-grader-results.json','shortcut-grader-results.json','exclusive-grader-results.json'];grades={n:load(E/n) for n in names};total=sum(x['accepted_checks']+x['rejected_checks'] for x in grades.values());assert total==704 and all(x['documented_unresolved_checks']==0 for x in grades.values())
assert load(E/'exclusive-subset-results.json')['successes']==2 and load(E/'exclusive-subset-results.json')['attempts']==2
assert load(E/'exclusive-subset-catalog-results.json')['successes']==4 and load(E/'exclusive-subset-catalog-results.json')['attempts']==6
assert load(E/'prior-failure-reproduced.json')['passed'] is False and load(E/'current-batch-regression.json')['passed'] is True
final={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};assert final==load(E/'package-before.json')
report={'passed':True,'pedagogical_schema_valid':True,'referenced_files':len(set(refs)),'native_checks':total,'package_unchanged':True,'exact_batch_shortcut':'2/2 accepted;4/6 same-subgroup catalog control','result':'revise'}
(E/'evidence-contract.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
