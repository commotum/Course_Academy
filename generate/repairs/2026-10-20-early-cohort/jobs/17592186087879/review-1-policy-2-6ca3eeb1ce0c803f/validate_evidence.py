"""Check report evidence references and the supplied pedagogical schema contract."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=Path('/home/jake/Developer/Course_Academy');P=R.parent/'workspace'
def validate(v,s,path='$'):
 typ=s.get('type')
 tests={'object':lambda:isinstance(v,dict),'array':lambda:isinstance(v,list),'string':lambda:isinstance(v,str),'integer':lambda:isinstance(v,int) and not isinstance(v,bool),'number':lambda:isinstance(v,(int,float)) and not isinstance(v,bool)}
 if typ:assert tests[typ](),(path,typ)
 if 'enum' in s:assert v in s['enum'],path
 if typ=='object':
  for k in s.get('required',[]):assert k in v,(path,k)
  if s.get('additionalProperties') is False:assert not set(v)-set(s.get('properties',{})),path
  for k,sub in s.get('properties',{}).items():
   if k in v:validate(v[k],sub,path+'.'+k)
 if typ=='array':
  assert len(v)>=s.get('minItems',0),path
  for i,z in enumerate(v):validate(z,s.get('items',{}),path+f'[{i}]')
 if typ=='string':assert len(v)>=s.get('minLength',0),path
 if typ in ['number','integer']:
  assert v>=s.get('minimum',float('-inf')) and v<=s.get('maximum',float('inf')),path
schema=json.load(open(ROOT/'generate/pipeline/pedagogical-variation.schema.json'));pv=json.load(open(R/'pedagogical-variation.json'));validate(pv,schema)
refs=[]
def collect(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['sample_refs','evidence_paths']:refs.extend(v)
   else:collect(v)
 elif isinstance(x,list):
  for z in x:collect(z)
result=json.load(open(R/'result.json'));collect(result);collect(pv)
for p in refs:
 f=R/p;assert not Path(p).is_absolute() and f.is_file() and f.stat().st_size>0,p
assert set(result['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
assert all(z['status']=='passed' and z['evidence_paths'] for z in result['checks'].values()) and result['findings']==[]
current={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};assert current==json.load(open(R/'package-before.json'))
(R/'package-integrity.json').write_text(json.dumps({'unchanged':True,'files':len(current)},indent=2))
(R/'contract-check.json').write_text(json.dumps({'pedagogical_schema':'passed','nonempty_evidence_references':len(refs),'eight_checks':'passed','package_unchanged':True},indent=2))
print(json.dumps({'schema':'passed','evidence_references':len(refs),'package_files_unchanged':len(current)}))
