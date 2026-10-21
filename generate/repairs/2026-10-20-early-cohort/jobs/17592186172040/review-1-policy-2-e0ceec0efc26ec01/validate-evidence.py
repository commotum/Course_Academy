"""Small validator for every keyword used by the supplied closed-object schema."""
from pathlib import Path
import json
E=Path(__file__).resolve().parent;R=Path('/home/jake/Developer/Course_Academy')
v=json.loads((E/'pedagogical-variation.json').read_text())
# Source account is a citation, not a sampled record, so keep sample_refs to actual test/sample files.
for p in v['shortcut_probes']:
 p['sample_refs']=[s for s in p['sample_refs'] if s!='source-analysis.json']
(E/'pedagogical-variation.json').write_text(json.dumps(v,indent=2)+'\n')
schema=json.loads((R/'generate/pipeline/pedagogical-variation.schema.json').read_text())
count=0
def validate(x,s,path='$'):
 global count
 count+=1
 known={'type','properties','required','additionalProperties','items','minItems','minLength','minimum','maximum','enum','$schema'}
 assert set(s)<=known,(path,'unknown validation keywords',set(s)-known)
 t=s.get('type')
 if t:
  ok={'object':isinstance(x,dict),'array':isinstance(x,list),'string':isinstance(x,str),'integer':type(x) is int,'number':type(x) in (int,float)}[t]
  assert ok,(path,t,x)
 if 'enum' in s:assert x in s['enum'],(path,x)
 if isinstance(x,dict):
  assert set(s.get('required',[]))<=x.keys(),path
  if s.get('additionalProperties') is False:assert set(x)<=set(s.get('properties',{})),path
  for k,val in x.items():
   if k in s.get('properties',{}):validate(val,s['properties'][k],path+'.'+k)
 if isinstance(x,list):
  assert len(x)>=s.get('minItems',0),path
  if 'items' in s:
   for i,val in enumerate(x):validate(val,s['items'],f'{path}[{i}]')
 if isinstance(x,str):assert len(x)>=s.get('minLength',0),path
 if 'minimum' in s:assert x>=s['minimum'],path
 if 'maximum' in s:assert x<=s['maximum'],path
validate(v,schema)
refs=[]
def walk(x):
 if isinstance(x,dict):
  for k,val in x.items():
   if k in ('sample_refs','evidence_paths'):refs.extend(val)
   else:walk(val)
 elif isinstance(x,list):
  for a in x:walk(a)
walk(v);walk(json.loads((E/'result.json').read_text()))
for p in refs:assert not Path(p).is_absolute() and (E/p).is_file() and (E/p).stat().st_size,p
c=json.loads((E/'evidence-contract.json').read_text());c['pedagogical_schema']='passed: every keyword in supplied schema validated by validate-evidence.py';c['validated_schema_nodes']=count;c['nonempty_relative_references']=len(refs)
(E/'evidence-contract.json').write_text(json.dumps(c,indent=2)+'\n')
print('schema validated',count,'nodes;',len(refs),'nonempty relative references')
